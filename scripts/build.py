"""Exporta la matriz de ensayo desde una sola base con packwiz."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import zipfile
from profiles import ROOT, configs, descriptors, pack_version, profiles

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--packwiz', default='packwiz')
    parser.add_argument('--profile', action='append', help='Construir solo este perfil (repetible)')
    args = parser.parse_args()
    executable = shutil.which(args.packwiz)
    if not executable:
        parser.error('Instala packwiz o usa --packwiz /ruta/al/binario')
    executable = str(Path(executable).resolve())
    matrix = profiles()
    if args.profile and set(args.profile) - matrix.keys():
        parser.error('Perfil desconocido')
    subprocess.run([executable, 'refresh'], cwd=ROOT / 'pack', check=True)
    out = ROOT / 'dist'
    out.mkdir(exist_ok=True)
    targets = []
    for name, profile in matrix.items():
        if args.profile and name not in args.profile:
            continue
        stage = ROOT / '.build' / name
        if stage.exists():
            shutil.rmtree(stage)
        (stage / 'mods').mkdir(parents=True)
        for filename in ('pack.toml', 'index.toml', '.packwizignore'):
            shutil.copy2(ROOT / 'pack' / filename, stage / filename)
        for descriptor in descriptors(profile):
            shutil.copy2(descriptor, stage / 'mods' / descriptor.name)
        for path, data in configs(profile).items():
            target = stage / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        manifest = stage / 'pack.toml'
        source = manifest.read_text()
        for key in ('name', 'description'):
            source = re.sub(rf'^{key} = .*?$', lambda _: key + ' = ' + json.dumps(profile[key], ensure_ascii=False), source, count=1, flags=re.MULTILINE)
        manifest.write_text(source)
        subprocess.run([executable, 'refresh'], cwd=stage, check=True)
        target = out / f'Lumina-Optimized-{pack_version()}-{name}.mrpack'
        subprocess.run([executable, 'modrinth', 'export', '--output', str(target)], cwd=stage, check=True)
        if not target.is_file():
            raise RuntimeError(f'packwiz no generó {target}')
        targets.append(target)
    checksum = out / f'SHA256SUMS-{pack_version()}'
    checksum.write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in sorted(targets)))
    if not args.profile:
        with zipfile.ZipFile(out / f'Lumina-Optimized-{pack_version()}-test-packages.zip', 'w', zipfile.ZIP_DEFLATED) as bundle:
            for path in [*targets, checksum]:
                bundle.write(path, path.name)

if __name__ == '__main__':
    main()
