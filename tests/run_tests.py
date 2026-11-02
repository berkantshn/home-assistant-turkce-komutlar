#!/usr/bin/env python3
"""Made By FALCREB.

Test düzenini baştan sona kurar ve çalıştırır. Gereken: Docker ve Python 3.

Akış:
  1. Bridge ağında, yalnızca 127.0.0.1'e açık bir Home Assistant kapsayıcısı başlatır.
  2. tests/ha_config içindeki sahte evi çalışma klasörüne kopyalar.
  3. Matrisi önce paketsiz (taban ölçüm), sonra paketli çalıştırır.
  4. Yalnızca kendi oluşturduğu kapsayıcıyı ve ağı siler.

Kullanım:
  python tests/run_tests.py
  python tests/run_tests.py --workdir /bir/klasor --keep

Depoda gizli bilgi yoktur: test kullanıcısının şifresi her kurulumda rastgele
üretilir ve yalnızca atılabilir çalışma klasöründe kalır.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS = ROOT / "tests"
CONTAINER = "ha-tr-komut-test"
NETWORK = "ha-tr-komut-net"
LABEL = "ha-tr-komut-test=1"
IMAGE = "ghcr.io/home-assistant/home-assistant:stable"
PORT = 18123


def docker(*args, check=True, capture=True):
    """Docker komutu çalıştırır."""
    return subprocess.run(
        ["docker", *args], check=check, text=True, encoding="utf-8",
        capture_output=capture,
    )


def exists(kind, name):
    """Adı verilen kapsayıcı/ağ bu test etiketiyle var mı?"""
    result = docker(
        kind, "ls", *(["-a"] if kind == "container" else []),
        "--filter", f"name=^{name}$", "--filter", f"label={LABEL}",
        "--format", "{{.Names}}" if kind == "container" else "{{.Name}}",
        check=False,
    )
    return bool(result.stdout.strip())


def ensure_container(workdir):
    """Kapsayıcı çalışmıyorsa başlatır; etiketsiz bir şeye dokunmaz."""
    if exists("container", CONTAINER):
        docker("start", CONTAINER)
        return
    foreign = docker("ps", "-a", "--filter", f"name=^{CONTAINER}$", "--format", "{{.Names}}")
    if foreign.stdout.strip():
        sys.exit(f"{CONTAINER} adlı, bu betiğe ait olmayan bir kapsayıcı var; durduruldu.")
    if not exists("network", NETWORK):
        docker("network", "create", "--driver", "bridge", "--label", LABEL, NETWORK)
    docker(
        "run", "-d", "--name", CONTAINER, "--label", LABEL, "--network", NETWORK,
        "-p", f"127.0.0.1:{PORT}:8123",
        "-e", "TZ=Europe/Istanbul",
        "-v", f"{workdir}:/config",
        "-v", f"{TESTS}:/tests:ro",
        IMAGE,
    )


def wait_ready(timeout=300):
    """Yalnızca 127.0.0.1 üzerinden Home Assistant'ın açılmasını bekler."""
    url = f"http://127.0.0.1:{PORT}/api/onboarding"
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=3):
                return
        except urllib.error.HTTPError as err:
            if err.code < 500:
                return
        except OSError:
            pass
        time.sleep(2)
    print(docker("logs", "--tail", "40", CONTAINER, check=False).stderr)
    sys.exit("Home Assistant zamanında açılmadı.")


def prepare_workdir(workdir, with_pack=False):
    """Sahte ev yapılandırmasını kopyalar; paket isteğe bağlı eklenir."""
    workdir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(TESTS / "ha_config", workdir, dirs_exist_ok=True)
    shutil.copy(ROOT / "examples" / "otomasyonlar.yaml", workdir / "automations.yaml")
    target = workdir / "custom_sentences" / "tr"
    if target.exists():
        shutil.rmtree(target)
    if with_pack:
        shutil.copytree(ROOT / "custom_sentences" / "tr", target)


def run_matrix(label, workdir, only=None, matrix="/tests/matrix.yaml"):
    """Matrisi kapsayıcının içindeki Python ile çalıştırır."""
    (workdir / "test-out").mkdir(exist_ok=True)
    args = [
        "exec", CONTAINER, "python3", "-I", "/tests/matrix_runner.py",
        "--label", label, "--matrix", matrix,
    ]
    if only:
        args += ["--only", only]
    result = subprocess.run(
        ["docker", *args], text=True, encoding="utf-8", capture_output=True, check=False
    )
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.returncode


def write_summary(out):
    """Grup başına paketsiz ve paketli sonucu yan yana yazar."""
    runs = {
        label: json.loads((out / f"sonuclar-{label}.json").read_text(encoding="utf-8"))
        for label in ("baseline", "pack")
    }
    groups = {}
    for label, rows in runs.items():
        for row in rows:
            entry = groups.setdefault(row["group"], {"baseline": 0, "pack": 0, "toplam": 0})
            entry[label] += row["ok"]
            if label == "pack":
                entry["toplam"] += 1
    lines = [
        "# Özet: paketsiz ve paketli", "",
        "| Grup | Satır | Paketsiz geçen | Paketli geçen |", "|---|---|---|---|",
    ]
    for name, entry in groups.items():
        lines.append(f"| {name} | {entry['toplam']} | {entry['baseline']} | {entry['pack']} |")
    total = {k: sum(g[k] for g in groups.values()) for k in ("toplam", "baseline", "pack")}
    lines.append(f"| **Toplam** | **{total['toplam']}** | **{total['baseline']}** | **{total['pack']}** |")
    (TESTS / "results" / "ozet.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, help="Atılabilir yapılandırma klasörü")
    parser.add_argument("--keep", action="store_true", help="Kapsayıcıyı silme")
    parser.add_argument("--only", help="Yalnızca adında bu metin geçen satırlar")
    parser.add_argument("--no-baseline", action="store_true", help="Paketsiz ölçümü atla")
    args = parser.parse_args()

    workdir = (args.workdir or Path(tempfile.mkdtemp(prefix="ha-tr-test-"))).resolve()
    print(f"Çalışma klasörü: {workdir}")
    if not exists("container", CONTAINER):
        prepare_workdir(workdir)
    ensure_container(workdir)
    wait_ready()

    code = 0
    try:
        if not args.no_baseline:
            prepare_workdir(workdir, with_pack=False)
            run_matrix("baseline", workdir, args.only)
            run_matrix("kor-kume-2-paketsiz", workdir, None, "/tests/kor_kume_2.yaml")
        prepare_workdir(workdir, with_pack=True)
        code = run_matrix("pack", workdir, args.only)
        # Kör kümeler: paketi görmeden yazılmış cümleler. Sonuçları genel başarıya
        # katılmaz, paketin yeni cümlelerde ne kadar tuttuğunu ölçer.
        run_matrix("kor-kume-1", workdir, None, "/tests/kor_kume_1.yaml")
        run_matrix("kor-kume-2", workdir, None, "/tests/kor_kume_2.yaml")
        out = workdir / "test-out"
        for name in (
            "sonuclar-pack.md", "sonuclar-baseline.md",
            "sonuclar-kor-kume-1.md", "sonuclar-kor-kume-2.md",
            "sonuclar-kor-kume-2-paketsiz.md",
        ):
            if (out / name).exists():
                shutil.copy(out / name, TESTS / "results" / name)
        if (out / "sonuclar-baseline.json").exists():
            write_summary(out)
    finally:
        if not args.keep:
            # Yalnızca bu betiğin oluşturduğu kapsayıcı ve ağ silinir.
            if exists("container", CONTAINER):
                docker("rm", "-f", CONTAINER, check=False)
            if exists("network", NETWORK):
                docker("network", "rm", NETWORK, check=False)
    return code


if __name__ == "__main__":
    sys.exit(main())
