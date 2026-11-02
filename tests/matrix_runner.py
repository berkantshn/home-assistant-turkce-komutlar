"""Made By FALCREB.

Home Assistant kapsayıcısının içinde çalışır (aiohttp ve PyYAML orada hazırdır).
Her cümle için iki gerçek API çağrısı yapar:
  - WebSocket conversation/agent/homeassistant/debug: hangi niyet ve slotlar eşleşti?
  - REST /api/conversation/process: komut gerçekten yürütüldü mü, yanıt ne?
Sonra sahte varlığın durumunu okuyup beklenenle karşılaştırır.
"""
import argparse
import asyncio
import json
import secrets
import sys
import time
from pathlib import Path

import aiohttp
import yaml

BASE = "http://127.0.0.1:8123"
WS = "ws://127.0.0.1:8123/api/websocket"
CLIENT_ID = "http://127.0.0.1:8123/"
TOKEN_FILE = Path("/config/.test_token")
MATRIX = Path("/tests/matrix.yaml")
OUT = Path("/config/test-out")

FLOORS = {"Zemin Kat": ["Salon", "Mutfak"], "Üst Kat": ["Yatak Odası"]}
ENTITY_AREAS = {
    "light.salon_lambasi": "Salon",
    "light.avize": "Salon",
    "light.mutfak_lambasi": "Mutfak",
    "light.abajur": "Yatak Odası",
    "light.tavan_isigi": "Yatak Odası",
    "light.ara_isigi": "Yatak Odası",
    "light.ikinci_lamba": "Yatak Odası",
    "switch.kahve_makinesi": "Mutfak",
    "switch.priz": "Salon",
    "fan.tavan_fani": "Yatak Odası",
    "cover.salon_perdesi": "Salon",
    "cover.panjur": "Mutfak",
    "climate.salon_klimasi": "Salon",
    "media_player.televizyon": "Salon",
    "media_player.hoparlor": "Mutfak",
    "sensor.salon_sicaklik": "Salon",
    "sensor.salon_nem": "Salon",
    "sensor.mutfak_nem": "Mutfak",
    "binary_sensor.salon_penceresi": "Salon",
    "binary_sensor.mutfak_hareket": "Mutfak",
    "lock.on_kapi": "Salon",
    "alarm_control_panel.ev_alarmi": "Salon",
    "vacuum.robot_supurge": "Salon",
}
# Kilit ve alarm varsayılanda Assist'e açık değildir. Güvenlik testleri "biri
# açsa bile paket kilidi açmıyor" sorusunu ölçtüğü için burada bilerek açılır.
EXPOSE = ["lock.on_kapi", "alarm_control_panel.ev_alarmi", "weather.hava", "script.gece_modu"]


class Client:
    """Tek WebSocket bağlantısı üzerinden sıralı istek gönderir."""

    def __init__(self, session, token):
        self.session, self.token, self.ws, self.next_id = session, token, None, 1

    async def connect(self):
        self.ws = await self.session.ws_connect(WS, max_msg_size=0)
        await self.ws.receive_json()
        await self.ws.send_json({"type": "auth", "access_token": self.token})
        reply = await self.ws.receive_json()
        if reply.get("type") != "auth_ok":
            raise RuntimeError(f"auth: {reply}")

    async def call(self, msg_type, **data):
        msg_id = self.next_id
        self.next_id += 1
        await self.ws.send_json({"id": msg_id, "type": msg_type, **data})
        while True:
            reply = await self.ws.receive_json()
            if reply.get("id") == msg_id:
                if not reply.get("success", True):
                    raise RuntimeError(f"{msg_type}: {reply.get('error')}")
                return reply.get("result")

    async def service(self, domain, service, data=None):
        return await self.call(
            "call_service", domain=domain, service=service, service_data=data or {}
        )


async def get_token(session):
    """İlk kurulumda rastgele şifreyle kullanıcı açar; jeton atılabilir klasörde kalır."""
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text().strip()
    async with session.post(
        f"{BASE}/api/onboarding/users",
        json={
            "client_id": CLIENT_ID, "name": "Test", "username": "test",
            "password": secrets.token_urlsafe(24), "language": "tr",
        },
    ) as resp:
        code = (await resp.json())["auth_code"]
    async with session.post(
        f"{BASE}/auth/token",
        data={"grant_type": "authorization_code", "code": code, "client_id": CLIENT_ID},
    ) as resp:
        access = (await resp.json())["access_token"]
    client = Client(session, access)
    await client.connect()
    long_lived = await client.call(
        "auth/long_lived_access_token", client_name="test", lifespan=30
    )
    await client.ws.close()
    TOKEN_FILE.write_text(long_lived)
    return long_lived


async def rest(session, token, method, path, payload=None):
    """REST çağrısı yapar, JSON döndürür."""
    async with session.request(
        method, f"{BASE}{path}", json=payload,
        headers={"Authorization": f"Bearer {token}"},
    ) as resp:
        return resp.status, await resp.json(content_type=None)


async def setup_house(session, token, client):
    """Sahte evi kurar: entegrasyon, kat, oda, varlık-oda eşleşmesi, uydu."""
    status, entries = await rest(session, token, "GET", "/api/config/config_entries/entry")
    domains = {entry["domain"] for entry in entries}
    for domain in ("fake_home", "shopping_list"):
        if domain not in domains:
            _, flow = await rest(
                session, token, "POST", "/api/config/config_entries/flow",
                {"handler": domain, "show_advanced_options": False},
            )
            if flow.get("type") == "form":
                await rest(
                    session, token, "POST",
                    f"/api/config/config_entries/flow/{flow['flow_id']}", {},
                )
    await asyncio.sleep(3)

    floors = {f["name"]: f["floor_id"] for f in await client.call("config/floor_registry/list")}
    # Kurulum sihirbazı "Yatak odası" gibi varsayılan odalar açar; aynı ad ikinci
    # kez açılamadığından küçük/büyük harf farkı yok sayılarak eşleştirilir.
    known = {
        a["name"].casefold(): a["area_id"]
        for a in await client.call("config/area_registry/list")
    }
    areas = {}
    for floor, floor_areas in FLOORS.items():
        if floor not in floors:
            created = await client.call("config/floor_registry/create", name=floor)
            floors[floor] = created["floor_id"]
        for area in floor_areas:
            area_id = known.get(area.casefold())
            if area_id:
                await client.call(
                    "config/area_registry/update", area_id=area_id, name=area,
                    floor_id=floors[floor],
                )
            else:
                created = await client.call(
                    "config/area_registry/create", name=area, floor_id=floors[floor]
                )
                area_id = created["area_id"]
            areas[area] = area_id
    for entity_id, area in ENTITY_AREAS.items():
        await client.call(
            "config/entity_registry/update", entity_id=entity_id, area_id=areas[area]
        )
    # Rehberdeki çözümün sınanması: "Işık" ile başlayan ada küçük harfli takma ad.
    await client.call(
        "config/entity_registry/update", entity_id="light.tavan_isigi",
        aliases=["tavan ışığı"],
    )
    await client.call(
        "homeassistant/expose_entity", assistants=["conversation"],
        entity_ids=EXPOSE, should_expose=True,
    )
    devices = await client.call("config/device_registry/list")
    device = next(d for d in devices if d["name"] == "Test Uydusu")
    await client.call(
        "config/device_registry/update", device_id=device["id"], area_id=areas["Salon"]
    )
    return device["id"]


def check_state(state, expect):
    """Beklenen durum/öznitelik değerini karşılaştırır; farkı metin olarak döndürür."""
    if "state" in expect and state["state"] != expect["state"]:
        return f"durum={state['state']} beklenen={expect['state']}"
    for key, wanted in (expect.get("attrs") or {}).items():
        have = state["attributes"].get(key)
        if isinstance(wanted, (int, float)) and isinstance(have, (int, float)):
            if abs(have - wanted) > 1.5:
                return f"{key}={have} beklenen={wanted}"
        elif isinstance(wanted, list):
            if list(have or []) != wanted:
                return f"{key}={have} beklenen={wanted}"
        elif have != wanted:
            return f"{key}={have} beklenen={wanted}"
    return None


async def prepare_blind_row(client, row):
    """Kör kümede satırlar birbirini etkilemesin: medya uygun duruma alınır."""
    media_state = "paused" if row.get("intent") == "HassMediaUnpause" else "playing"
    for entity_id in ("media_player.televizyon", "media_player.hoparlor"):
        await client.service("fake_home", "set", {"entity_id": entity_id, "state": media_state})


async def run_row(session, token, client, row, device_id):
    """Tek satırı çalıştırır; (geçti_mi, ayrıntı sözlüğü) döndürür."""
    if str(row.get("group", "")).startswith("heldout"):
        await prepare_blind_row(client, row)
    for entity_id, spec in (row.get("setup") or {}).items():
        await client.service("fake_home", "set", {"entity_id": entity_id, **spec})
    device = device_id if row.get("device") else None
    # Hazırlık cümleleri: örneğin zamanlayıcıyı temizlemek. Sonuçları puanlanmaz.
    for text in row.get("first") or []:
        await rest(
            session, token, "POST", "/api/conversation/process",
            {"text": text, "language": "tr", "device_id": device_id},
        )
    debug_args = {"sentences": [row["text"]], "language": "tr"}
    if device:
        debug_args["device_id"] = device
    debug = (await client.call("conversation/agent/homeassistant/debug", **debug_args))["results"][0]
    debug = debug or {}
    # match=False ise "intent" yalnızca en yakın adaydır, eşleşme sayılmaz.
    intent_name = debug.get("intent", {}).get("name") if debug.get("match") else None
    slots = {k: v.get("value") for k, v in (debug.get("details") or {}).items()}
    source = debug.get("source", "")
    # Yürütme adımı
    payload = {"text": row["text"], "language": "tr"}
    if device:
        payload["device_id"] = device
    if row.get("agent_id"):
        payload["agent_id"] = row["agent_id"]
    _, result = await rest(session, token, "POST", "/api/conversation/process", payload)
    response = (result or {}).get("response", {})
    speech = response.get("speech", {}).get("plain", {}).get("speech", "")
    rtype = response.get("response_type")
    await asyncio.sleep(0.05)

    problems = []
    expected = row.get("intent")
    if expected == "sentence_trigger":
        # Otomasyon cümlesi: niyet değil, tetikleyici eşleşir.
        if source != "trigger":
            problems.append(f"tetikleyici eşleşmedi (kaynak={source}, niyet={intent_name})")
    elif expected is None:
        if intent_name or source == "trigger":
            problems.append(f"eşleşmemeliydi ama niyet={intent_name}")
    elif intent_name != expected:
        problems.append(f"niyet={intent_name} beklenen={expected}")
    for key, wanted in (row.get("slots") or {}).items():
        have = slots.get(key)
        same = str(have) == str(wanted)
        if isinstance(have, (int, float)) and isinstance(wanted, (int, float)):
            same = float(have) == float(wanted)
        if not same:
            problems.append(f"slot {key}={slots.get(key)} beklenen={wanted}")
    if expected and rtype == "error":
        problems.append(f"hata yanıtı: {response.get('data', {}).get('code')} / {speech}")
    if expected and row.get("say") and row["say"] not in speech:
        problems.append(f"yanıt='{speech}' beklenen içerik='{row['say']}'")
    if expected and row.get("say_any"):
        if not any(item in speech for item in row["say_any"]):
            problems.append(f"yanıt='{speech}' beklenen içerik={row['say_any']}")
    for entity_id, expect in (row.get("expect") or {}).items():
        _, state = await rest(session, token, "GET", f"/api/states/{entity_id}")
        diff = check_state(state, expect)
        if diff:
            problems.append(f"{entity_id}: {diff}")
    return not problems, {
        "intent": intent_name, "slots": slots, "speech": speech.strip(), "type": rtype,
        "problems": problems, "source": source,
    }


def write_report(label, rows, results, seconds):
    """Sonuç tablosunu Markdown olarak yazar."""
    OUT.mkdir(exist_ok=True)
    passed = sum(1 for ok, _ in results if ok)
    lines = [
        f"# Test sonucu: {label}", "",
        f"Geçen: **{passed}/{len(rows)}** · süre: {seconds:.1f} sn", "",
        "| # | Grup | Cümle | Beklenen niyet | Eşleşen niyet | Kaynak | Sonuç | Yanıt / sorun |",
        "|---|------|-------|----------------|---------------|--------|-------|---------------|",
    ]
    for i, (row, (ok, info)) in enumerate(zip(rows, results), 1):
        note = "; ".join(info["problems"]) if info["problems"] else info["speech"]
        note = note.replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {i} | {row.get('group', '')} | {row['text']} | {row.get('intent') or '(eşleşmemeli)'} "
            f"| {info['intent'] or '-'} | {info['source'] or '-'} | {'GEÇTİ' if ok else 'KALDI'} | {note} |"
        )
    (OUT / f"sonuclar-{label}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / f"sonuclar-{label}.json").write_text(
        json.dumps(
            [{"text": r["text"], "group": r.get("group"), "ok": ok, **info}
             for r, (ok, info) in zip(rows, results)],
            ensure_ascii=False, indent=1,
        ),
        encoding="utf-8",
    )


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="pack")
    parser.add_argument("--only")
    parser.add_argument("--matrix", default=str(MATRIX))
    args = parser.parse_args()

    rows = yaml.safe_load(Path(args.matrix).read_text(encoding="utf-8"))["cases"]
    if args.only:
        rows = [r for r in rows if args.only in r["text"] or args.only in r.get("group", "")]

    async with aiohttp.ClientSession() as session:
        token = await get_token(session)
        client = Client(session, token)
        await client.connect()
        device_id = await setup_house(session, token, client)
        await client.service("automation", "reload")
        await client.service("conversation", "reload", {"language": "tr"})
        start = time.time()
        results = []
        for row in rows:
            results.append(await run_row(session, token, client, row, device_id))
        seconds = time.time() - start
        write_report(args.label, rows, results, seconds)
        passed = sum(1 for ok, _ in results if ok)
        print(f"[{args.label}] geçen {passed}/{len(rows)} ({seconds:.1f} sn)")
        if args.label == "pack":
            for row, (ok, info) in zip(rows, results):
                if not ok:
                    print(f"  KALDI: {row['text']} -> {'; '.join(info['problems'])}")
        await client.ws.close()
    return 0 if passed == len(rows) or args.label == "baseline" else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
