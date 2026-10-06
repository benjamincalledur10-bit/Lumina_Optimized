"""Validación estática de metadatos, descargas, JAR anidados y exportaciones.

No inicia Minecraft ni sustituye al resolvedor de Fabric durante el arranque.
"""
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import tomllib
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".build/downloads"

def require(condition, message):
    if not condition:
        raise ValueError(message)

def fetch(url):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / hashlib.sha256(url.encode()).hexdigest()
    if not path.exists():
        request = urllib.request.Request(url, headers={"User-Agent": "Lumina-Optimized/0.1.0-alpha.1"})
        with urllib.request.urlopen(request, timeout=60) as response:
            path.write_bytes(response.read())
    return path.read_bytes()

def numbers(version):
    return tuple(int(x) for x in version.split("+")[0].split("-")[0].split("."))

def matches(version, expressions):
    if isinstance(expressions, list):
        return any(matches(version, x) for x in expressions)
    for part in expressions.split():
        if part == "*":
            continue
        if part.endswith((".x", ".*")):
            if numbers(version)[:len(numbers(part[:-2]))] != numbers(part[:-2]):
                return False
            continue
        match = re.fullmatch(r"(>=|<=|>|<|=|~|\^)?(\d+(?:\.\d+)*(?:-[\w.]+)?(?:\+[\w.]+)?)", part)
        require(match is not None, f"Predicado no soportado: {part}")
        op, expected = match.groups()
        a, b = numbers(version), numbers(expected)
        length = max(len(a), len(b))
        a, b = a + (0,) * (length-len(a)), b + (0,) * (length-len(b))
        if op in ("~", "^"):
            # Los predicados de esta base son ~26.3 o ~26.1: misma major.
            require(len(numbers(expected)) == 2 and op == "~", f"Rango no soportado: {part}")
            passed = a >= b and a[0] == b[0]
        else:
            passed = {None: a == b, "=": a == b, ">=": a >= b, "<=": a <= b, ">": a > b, "<": a < b}[op]
        if not passed:
            return False
    return True

def inspect_jar(data, origin, inventory):
    with zipfile.ZipFile(io.BytesIO(data)) as jar:
        require(jar.testzip() is None, f"JAR corrupto: {origin}")
        if "fabric.mod.json" not in jar.namelist():
            return
        metadata = json.loads(jar.read("fabric.mod.json"))
        inventory.append({"origin": origin, "id": metadata["id"], "version": metadata["version"],
                          "jar_sha512": hashlib.sha512(data).hexdigest(),
                          "depends": metadata.get("depends", {}), "breaks": metadata.get("breaks", {}),
                          "environment": metadata.get("environment", "*")})
        for nested in metadata.get("jars", []):
            inspect_jar(jar.read(nested["file"]), origin + "!" + nested["file"], inventory)

def check_index(folder):
    manifest = tomllib.loads((folder / "pack.toml").read_text())
    index_bytes = (folder / manifest["index"]["file"]).read_bytes()
    require(hashlib.new(manifest["index"]["hash-format"], index_bytes).hexdigest() == manifest["index"]["hash"], "Hash del índice inválido")
    index = tomllib.loads(index_bytes.decode())
    for entry in index.get("files", []):
        data = (folder / entry["file"]).read_bytes()
        require(hashlib.new(entry.get("hash-format", index["hash-format"]), data).hexdigest() == entry["hash"], f"Hash de fuente inválido: {entry['file']}")

def main():
    check_index(ROOT / "pack")
    for variant in ("core", "shaders"):
        check_index(ROOT / ".build" / variant)
    loader_url = "https://maven.fabricmc.net/net/fabricmc/fabric-loader/0.19.5/fabric-loader-0.19.5.jar"
    loader = fetch(loader_url)
    require(hashlib.sha1(loader).hexdigest() == fetch(loader_url + ".sha1").decode().strip(), "Hash de Loader inválido")
    loader_inventory = []
    with zipfile.ZipFile(io.BytesIO(loader)) as jar:
        for name in jar.namelist():
            if name.startswith("META-INF/jars/") and name.endswith(".jar"):
                inspect_jar(jar.read(name), "fabric-loader!" + name, loader_inventory)
    descriptors = sorted((ROOT / "pack/mods").glob("*.pw.toml")) + [ROOT / "variants/iris.pw.toml"]
    sources, inventories, projects = {}, {}, {}
    for path in descriptors:
        mod = tomllib.loads(path.read_text())
        require(mod.get("pin") is True, f"Versión no fijada: {path}")
        version = json.loads(fetch("https://api.modrinth.com/v2/version/" + mod["update"]["modrinth"]["version"]))
        require(version["project_id"] == mod["update"]["modrinth"]["mod-id"], "Proyecto incorrecto")
        require("26.3" in version["game_versions"] and "fabric" in version["loaders"], "Publicación incompatible")
        file = next(f for f in version["files"] if f["filename"] == mod["filename"])
        require(file["url"] == mod["download"]["url"], "URL diferente de la publicación")
        data = fetch(file["url"])
        for algorithm, expected in file["hashes"].items():
            require(hashlib.new(algorithm, data).hexdigest() == expected, f"Hash de JAR inválido: {path.name}")
        require(hashlib.new(mod["download"]["hash-format"], data).hexdigest() == mod["download"]["hash"], "Hash packwiz inválido")
        require(len(data) == file["size"], "Tamaño de JAR incorrecto")
        inventory = []
        inspect_jar(data, mod["filename"], inventory)
        sources["mods/" + mod["filename"]] = (mod, file, data)
        inventories[path.stem] = inventory
        projects[version["project_id"]] = version
    reports = {}
    core_names = {"mods/" + tomllib.loads(p.read_text())["filename"] for p in descriptors[:-1]}
    for variant in ("core", "shaders"):
        selected = core_names if variant == "core" else set(sources)
        inventory = loader_inventory.copy()
        for key, records in inventories.items():
            if variant == "shaders" or key != "iris.pw":
                inventory.extend(records)
        available = {"minecraft": "26.3", "java": "25", "fabricloader": "0.19.5"}
        jar_hashes = {}
        for record in inventory:
            require(record["id"] not in available or available[record["id"]] == record["version"], "Versiones duplicadas diferentes: " + record["id"])
            require(record["id"] not in jar_hashes or jar_hashes[record["id"]] == record["jar_sha512"], "JAR duplicado con contenido diferente: " + record["id"])
            jar_hashes[record["id"]] = record["jar_sha512"]
            available[record["id"]] = record["version"]
        for record in inventory:
            for dependency, predicate in record["depends"].items():
                require(dependency in available and matches(available[dependency], predicate), f"Dependencia no resuelta: {record['id']} -> {dependency} {predicate}")
            for conflict, predicate in record["breaks"].items():
                require(conflict not in available or not matches(available[conflict], predicate), f"Incompatibilidad: {record['id']} -> {conflict}")
        for project, version in projects.items():
            if variant == "core" and version["project_id"] == "YL57xq9U":
                continue
            for dep in version["dependencies"]:
                if dep["dependency_type"] == "required":
                    require(dep["project_id"] in projects and (not dep["version_id"] or projects[dep["project_id"]]["id"] == dep["version_id"]), "Dependencia Modrinth incorrecta")
        path = ROOT / "dist" / f"Lumina-Optimized-0.1.0-alpha.1-{variant}.mrpack"
        with zipfile.ZipFile(path) as archive:
            require(archive.testzip() is None, "Exportación corrupta")
            require(set(archive.namelist()) == {"modrinth.index.json", "overrides/"}, "Overrides inesperados: conservar defaults")
            manifest = json.loads(archive.read("modrinth.index.json"))
            require(manifest["formatVersion"] == 1 and manifest["game"] == "minecraft", "Formato incorrecto")
            require(manifest["versionId"] == "0.1.0-alpha.1", "Versión incorrecta")
            require(manifest["name"] == ("Lumina Optimized" if variant == "core" else "Lumina Optimized Shaders"), "Nombre incorrecto")
            require(manifest["dependencies"] == {"minecraft": "26.3", "fabric-loader": "0.19.5"}, "Dependencias de exportación incorrectas")
            require(len(manifest["files"]) == len(selected) and {f["path"] for f in manifest["files"]} == selected, "Contenido incorrecto")
            for entry in manifest["files"]:
                require(not PurePosixPath(entry["path"]).is_absolute() and ".." not in PurePosixPath(entry["path"]).parts, "Ruta insegura")
                mod, file, data = sources[entry["path"]]
                require(entry["downloads"] == [file["url"]] and entry["fileSize"] == len(data), "Descarga incorrecta")
                require({"sha1", "sha512"} <= set(entry["hashes"]), "Faltan hashes")
                for algorithm, expected in entry["hashes"].items():
                    require(hashlib.new(algorithm, data).hexdigest() == expected, "Hash de exportación inválido")
                require(entry["env"] == {"client": "required", "server": "unsupported" if mod["side"] == "client" else "required"}, "Lado incorrecto")
        reports[variant] = {"files": len(selected), "resolved": available, "jar_metadata": inventory,
                            "mrpack_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    for line in (ROOT / "dist/SHA256SUMS").read_text().splitlines():
        expected, filename = line.split("  ", 1)
        require(hashlib.sha256((ROOT / "dist" / filename).read_bytes()).hexdigest() == expected, "SHA256SUMS inválido")
    report = {"scope": "Validación estática; sin arranque, importación en launcher ni benchmarks", "variants": reports}
    (ROOT / "docs/validation.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print("OK: fuentes, índices, JAR, dependencias integradas, conflictos declarados y ambas exportaciones")

if __name__ == "__main__":
    main()
