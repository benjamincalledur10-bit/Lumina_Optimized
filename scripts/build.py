"""Exporta Core y Shaders con packwiz sin duplicar las fuentes de la base."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tomllib
import re

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--packwiz", default="packwiz")
    args = parser.parse_args()
    executable = shutil.which(args.packwiz)
    if not executable:
        parser.error("Instala packwiz o proporciona --packwiz /ruta/al/binario")
    executable = str(Path(executable).resolve())
    subprocess.run([executable, "refresh"], cwd=ROOT / "pack", check=True)
    version = tomllib.loads((ROOT / "pack/pack.toml").read_text())["version"]
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    for variant in ("core", "shaders"):
        stage = ROOT / ".build" / variant
        if stage.exists():
            shutil.rmtree(stage)
        shutil.copytree(ROOT / "pack", stage)
        if variant == "shaders":
            overlay = json.loads((ROOT / "variants/shaders.json").read_text())
            for filename in overlay["add"]:
                shutil.copy2(ROOT / "variants" / filename, stage / "mods" / filename)
            manifest = stage / "pack.toml"
            source = manifest.read_text()
            for key in ("name", "description"):
                source = re.sub(rf"^{key} = .*?$", lambda _: key + " = " + json.dumps(overlay[key], ensure_ascii=False), source, count=1, flags=re.MULTILINE)
            manifest.write_text(source)
        subprocess.run([executable, "refresh"], cwd=stage, check=True)
        target = out / f"Lumina-Optimized-{version}-{variant}.mrpack"
        subprocess.run([executable, "modrinth", "export", "--output", str(target)], cwd=stage, check=True)
        if not target.is_file():
            raise RuntimeError(f"packwiz no generó {target}")
    targets = sorted(out.glob(f"Lumina-Optimized-{version}-*.mrpack"))
    (out / "SHA256SUMS").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in targets))

if __name__ == "__main__":
    main()
