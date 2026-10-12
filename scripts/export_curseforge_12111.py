"""Export/validate the CurseForge variant from the 1.21.11 Modrinth base.

Uses the audited official IDs in docs/editions/1.21.11. No JAR is committed
or embedded in overrides. Only the previously approved CF-specific Mandala
2.1 -> 2.6 replacement changes resource selection.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tomllib
import zipfile

from verify import fetch, require

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs/editions/1.21.11'
PACK = ROOT / 'packs/1.21.11'
VERSION = '1.21.11-beta.1'
SOURCE = ROOT / ('dist/Lumina-Optimized-' + VERSION + '.mrpack')
OUTPUT = ROOT / ('dist/Lumina-Optimized-' + VERSION + '-curseforge.zip')


def expected_overrides(archive, mapping):
    result = {n: archive.read(n) for n in archive.namelist()
              if n.startswith('overrides/') and not n.endswith('/')}
    mandala = next(r for r in mapping['files'] if r['replacement'])
    old, new = Path(mandala['source_path']).name, Path(mandala['path']).name
    data = result['overrides/options.txt']
    require(data.count(old.encode()) == 2, 'Unexpected resource selection')
    result['overrides/options.txt'] = data.replace(old.encode(), new.encode())
    return result


def verify_mapping(mapping):
    require(hashlib.sha256(SOURCE.read_bytes()).hexdigest() == mapping['source_mrpack_sha256'], 'Source changed')
    require(mapping['version'] == VERSION and len(mapping['files']) == 50, 'Incomplete mapping')
    publications = json.loads((DOCS / 'curseforge-publications.json').read_text())['data']
    files = {f['id']: f for f in publications['files']['data']}
    projects = {p['id']: p for p in publications['projects']['data']}
    present = {r['project_id'] for r in mapping['files']} | {p['project_id'] for p in mapping['embedded_providers']}
    require(len({r['project_id'] for r in mapping['files']}) == 50, 'Duplicate project')
    replacements = [r for r in mapping['files'] if r['replacement']]
    require(len(replacements) == 1 and (replacements[0]['project_id'], replacements[0]['file_id']) == (664719, 7564677), 'Unauthorized replacement')
    source_files = {}
    with zipfile.ZipFile(SOURCE) as archive:
        source_files = {f['path']: f for f in json.loads(archive.read('modrinth.index.json'))['files']}
    require(set(source_files) == {r['source_path'] for r in mapping['files']}, 'Source content omitted')
    downloaded = {}
    for row in mapping['files']:
        file, project = files[row['file_id']], projects[row['project_id']]
        require(file['modId'] == project['id'] and file['fileName'] == Path(row['path']).name, 'IDs/name differ')
        require(file['isAvailable'] and file['fileStatus'] == 4 and project['isAvailable'] and project['status'] == 4, 'Unapproved content')
        require('1.21.11' in file['gameVersions'], 'Not published for 1.21.11')
        require(project['classId'] == {'mods': 6, 'resourcepacks': 12, 'shaderpacks': 6552}[row['kind']], 'Wrong content class')
        if row['kind'] == 'mods': require('Fabric' in file['gameVersions'], 'Not Fabric')
        if row['kind'] == 'shaderpacks': require('Iris' in file['gameVersions'], 'Not Iris')
        require(source_files[row['source_path']]['hashes'] == {'sha1': row['source_sha1'], 'sha512': row['source_sha512']}, 'Source hashes changed')
        data = fetch(row['validation_url']); downloaded[row['source_path']] = data
        require(len(data) == row['size'] == file['fileLength'], 'Size differs')
        require(hashlib.sha512(data).hexdigest() == row['sha512'] and hashlib.sha1(data).hexdigest() == row['sha1'], 'Byte hashes differ')
        require(any(h['algo'] == 1 and h['value'] == row['sha1'] for h in file['hashes']), 'Official SHA-1 differs')
        if not row['replacement']:
            require(row['source_sha512'] == row['sha512'] and row['source_path'] == row['path'], 'Unexpected content change')
        for dependency in file['dependencies']:
            if dependency['relationType'] == 3: require(dependency['modId'] in present, 'Missing catalog dependency')
            if dependency['relationType'] == 5: require(dependency['modId'] not in present, 'Declared catalog conflict')
    for provider in mapping['embedded_providers']:
        origin, nested_path = provider['origin'].split('!', 1)
        container = downloaded['mods/' + origin]
        with zipfile.ZipFile(io.BytesIO(container)) as jar:
            nested = jar.read(nested_path)
        require(hashlib.sha1(nested).hexdigest() == provider['sha1'] and hashlib.sha512(nested).hexdigest() == provider['sha512'], 'Embedded provider differs')
        key = 'embedded_placeholder_files' if provider['slug'] == 'placeholder-api' else 'embedded_midnight_files'
        meta = next(f for f in publications[key]['data'] if f['id'] == provider['official_file_id'])
        require(meta['modId'] == provider['project_id'] and meta['isAvailable'] and meta['fileStatus'] == 4 and '1.21.11' in meta['gameVersions'] and 'Fabric' in meta['gameVersions'], 'Embedded publication incompatible')
        require(any(h['algo'] == 1 and h['value'] == provider['sha1'] for h in meta['hashes']), 'Embedded official hash differs')
        with zipfile.ZipFile(io.BytesIO(nested)) as jar:
            meta = json.loads(jar.read('fabric.mod.json'))
            require(meta['id'] == provider['fabric_id'] and meta['version'] == provider['fabric_version'], 'Embedded identity differs')


def build(mapping, packwiz):
    stage = ROOT / '.build/curseforge-1.21.11-beta1/export'
    if stage.exists(): shutil.rmtree(stage)
    stage.mkdir(parents=True)
    for name in ('pack.toml', 'index.toml', '.packwizignore'):
        if (PACK / name).exists(): shutil.copy2(PACK / name, stage / name)
    with zipfile.ZipFile(SOURCE) as archive:
        for name, data in expected_overrides(archive, mapping).items():
            path = stage / name.removeprefix('overrides/')
            path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
    for row in mapping['files']:
        source = tomllib.loads((PACK / row['kind'] / row['descriptor']).read_text())
        path = stage / row['kind'] / row['descriptor']; path.parent.mkdir(exist_ok=True)
        path.write_text(f'name = {json.dumps(source["name"])}\nfilename = {json.dumps(Path(row["path"]).name)}\nside = {json.dumps(source["side"])}\npin = true\n\n[download]\nhash-format = "sha512"\nhash = "{row["sha512"]}"\nmode = "metadata:curseforge"\n\n[update.curseforge]\nproject-id = {row["project_id"]}\nfile-id = {row["file_id"]}\n')
    executable = shutil.which(packwiz); require(executable is not None, 'packwiz missing')
    command = [str(Path(executable).resolve()), '--cache', str(ROOT / '.build/edition-1.21.11/packwiz-cache'), '-y']
    subprocess.run([*command, 'refresh'], cwd=stage, check=True)
    subprocess.run([*command, 'curseforge', 'export', '--side', 'client', '--output', str(OUTPUT)], cwd=stage, check=True)


def verify_zip(mapping):
    with zipfile.ZipFile(SOURCE) as before, zipfile.ZipFile(OUTPUT) as archive:
        require(archive.testzip() is None, 'Corrupt ZIP')
        names = [n for n in archive.namelist() if not n.endswith('/')]
        require(len(names) == len(set(names)) and all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names), 'Unsafe ZIP paths')
        overrides = expected_overrides(before, mapping)
        require(set(names) == {'manifest.json', 'modlist.html', *overrides}, 'Unexpected files or embedded binaries')
        require(all(archive.read(n) == data for n, data in overrides.items()), 'Configuration changed')
        manifest = json.loads(archive.read('manifest.json'))
        require(manifest['name'] == 'Lumina Optimized' and manifest['version'] == VERSION and manifest['manifestType'] == 'minecraftModpack' and manifest['manifestVersion'] == 1 and manifest['overrides'] == 'overrides', 'Wrong manifest identity')
        require(manifest['minecraft'] == {'version': '1.21.11', 'modLoaders': [{'id': 'fabric-0.19.5', 'primary': True}]}, 'Wrong target')
        expected = sorted((r['project_id'], r['file_id'], True) for r in mapping['files'])
        require(sorted((r['projectID'], r['fileID'], r['required']) for r in manifest['files']) == expected, 'Incomplete manifest')
        require(json.loads(archive.read('overrides/config/sodium-extra-options.json'))['extra_settings']['reduce_resolution_on_mac'], 'macOS default changed')
    require(hashlib.sha256(SOURCE.read_bytes()).hexdigest() == mapping['source_mrpack_sha256'], 'Modrinth export changed')
    sha = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    report = {'version': VERSION, 'evidence_date': mapping['verified_on'], 'archive': OUTPUT.name, 'sha256': sha, 'size': OUTPUT.stat().st_size,
              'checks': {k: 'PASS' for k in ('official_ids_hashes_and_compatibility', 'catalog_dependencies_and_conflicts', 'nested_providers', 'zip_crc_and_safe_paths', 'complete_manifest', 'configs_and_resources', 'modrinth_unchanged')},
              'counts': {'manifest_references': 50, 'external_binaries_in_overrides': 0, 'overrides': 12}, 'approved_replacements': mapping['approved_replacements'],
              'pending': mapping['publication_pending'], 'minecraft_tests': 'Modrinth selection tested by user; Mandala 2.6 variant not covered by that report. No CurseForge App import or re-export claimed.'}
    (DOCS / 'validation-curseforge.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    (OUTPUT.parent / (OUTPUT.name + '.sha256')).write_text(sha + '  ' + OUTPUT.name + '\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packwiz', default='packwiz')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    mapping = json.loads((DOCS / 'curseforge-mapping.json').read_text())
    verify_mapping(mapping)
    if not args.verify_only: build(mapping, args.packwiz)
    verify_zip(mapping)


if __name__ == '__main__': main()
