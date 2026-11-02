"""Made By FALCREB.

Üst projenin (home-assistant/intents) kendi Türkçe test cümlelerini, Home Assistant
imajındaki hassil ile paketli ve paketsiz dener. Amaç: paket, üst projede çalışan
bir cümleyi başka bir niyete kaydırıyor mu?

Üst projenin dosyaları depoya kopyalanmaz (lisansı CC BY 4.0); testte okumak için
ayrı bir klon verilir:

  git clone --depth 1 https://github.com/home-assistant/intents.git /bir/klasor
  docker run --rm --network none --entrypoint python3 \
    -v /bir/klasor:/up:ro -v "$PWD":/repo:ro \
    ghcr.io/home-assistant/home-assistant:stable -I \
    /repo/tests/upstream_regression.py /up /repo/custom_sentences/tr
"""
import copy
import sys
from pathlib import Path

import yaml
from hassil import Intents, recognize_best
from hassil.intents import TextSlotList
from hassil.util import merge_dict
from home_assistant_intents import get_intents

# Cümle içindeki değerlerin bir kısmı yerel listelerden çıkar (ör. perde -> curtain).
FALLBACK_AREA = "Test Odası"


def build(pack_dir=None):
    """Yerleşik Türkçe niyetlere isteğe bağlı olarak paketi ekler."""
    data = copy.deepcopy(get_intents("tr"))
    if pack_dir:
        for path in sorted(Path(pack_dir).glob("*.yaml")):
            merge_dict(data, yaml.safe_load(path.read_text(encoding="utf-8")))
    return Intents.from_dict(data)


def slot_lists(spec):
    """Testin varlık ve oda tanımlarından ad ve oda listeleri üretir."""
    names = [
        (e["name"], e["name"], {"domain": e.get("domain"), **(e.get("attributes") or {})})
        for e in spec.get("entities") or []
    ]
    areas = [(a["name"], a["name"]) for a in spec.get("areas") or []]
    areas = areas or [("Kullanılmayan Oda", "Kullanılmayan Oda")]
    names = names or [("Kullanılmayan Ad", "Kullanılmayan Ad", {"domain": "none"})]
    return {
        "name": TextSlotList.from_tuples(names, allow_template=False),
        "area": TextSlotList.from_tuples(areas, allow_template=False),
        "floor": TextSlotList.from_tuples(
            [("Kullanılmayan Kat", "Kullanılmayan Kat")], allow_template=False
        ),
    }


def check(intents, text, intent_name, lists, slots):
    """Cümleyi tanır; (geçti_mi, açıklama) döndürür."""
    result = recognize_best(
        text, intents, slot_lists=lists, intent_context={"area": FALLBACK_AREA},
        best_slot_name="name",
    )
    if result is None:
        return False, "eşleşme yok"
    if result.intent.name != intent_name:
        return False, f"niyet {result.intent.name}"
    for key, wanted in (slots or {}).items():
        entity = result.entities.get(key)
        have = entity.value if entity else None
        if isinstance(wanted, (int, float)) and isinstance(have, (int, float)):
            if float(wanted) == float(have):
                continue
        if str(have) != str(wanted):
            return False, f"slot {key}={have} beklenen={wanted}"
    return True, ""


def main():
    upstream, pack_dir = Path(sys.argv[1]), sys.argv[2]
    base, packed = build(), build(pack_dir)
    total = base_ok = pack_ok = 0
    regressions = []
    for path in sorted((upstream / "tests" / "tr").rglob("*.yaml")):
        spec = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not spec or "tests" not in spec:
            continue
        intent_name = path.parent.name
        lists = slot_lists(spec)
        for test in spec["tests"]:
            for text in test["sentences"]:
                total += 1
                ok_base, why_base = check(base, text, intent_name, lists, test.get("slots"))
                ok_pack, why_pack = check(packed, text, intent_name, lists, test.get("slots"))
                base_ok += ok_base
                pack_ok += ok_pack
                if ok_base and not ok_pack:
                    regressions.append(f"{intent_name}: {text} -> {why_pack}")
                elif not ok_base:
                    print(f"paketsiz de kalıyor: {intent_name}: {text} -> {why_base}")
    print(f"Üst proje Türkçe test cümlesi: {total}")
    print(f"Paketsiz geçen: {base_ok}, paketli geçen: {pack_ok}")
    print(f"Paket yüzünden bozulan: {len(regressions)}")
    for line in regressions:
        print("  " + line)
    return 1 if regressions else 0


if __name__ == "__main__":
    sys.exit(main())
