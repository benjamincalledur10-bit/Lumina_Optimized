"""Deriva variantes de una sola fuente packwiz, sin instancias independientes."""
import json
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]

def profiles():
    return json.loads((ROOT / "variants/profiles.json").read_text())

def descriptors(profile):
    paths = {p.name: p for p in (ROOT / "pack/mods").glob("*.pw.toml")}
    for name in profile.get("remove", []):
        if name not in paths:
            raise ValueError("Mod no encontrado: " + name)
        del paths[name]
    for name in profile.get("add", []):
        if name in paths:
            raise ValueError("Mod repetido: " + name)
        paths[name] = ROOT / "variants" / name
    return sorted(paths.values())

def configs(profile):
    present = {p.name for p in descriptors(profile)}
    mapping = {
        "entityculling.pw.toml": "entityculling.json",
        "moreculling.pw.toml": "moreculling.json",
        "better-block-entities.pw.toml": "BBEConfig.json",
    }
    result = {"config/" + filename: (ROOT / "pack/config" / filename).read_bytes()
              for mod, filename in mapping.items() if mod in present}
    if profile.get("bbe_enabled"):
        path = "config/BBEConfig.json"
        if path not in result:
            raise ValueError("Activación BBE sin BBE")
        config = json.loads(result[path])
        for option in config["bbe.config.storage.main"]:
            if option["option"] == "optimize.master":
                option["value"] = True
        result[path] = (json.dumps(config, indent=2) + "\n").encode()
    if "c2me-fabric.pw.toml" in present:
        result["config/c2me.toml"] = (ROOT / "variants/c2me.toml").read_bytes()
    return result

def pack_version():
    return tomllib.loads((ROOT / "pack/pack.toml").read_text())["version"]
