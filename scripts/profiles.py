"""Una composición principal; las matrices anteriores están en el historial."""
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]

def profiles():
    manifest = tomllib.loads((ROOT / 'pack/pack.toml').read_text())
    return {'main': {key: manifest[key] for key in ('name', 'description')}}

def descriptors(profile):
    return sorted((ROOT / 'pack/mods').glob('*.pw.toml'))

def resource_descriptors(profile):
    return sorted((ROOT / 'pack/resourcepacks').glob('*.pw.toml'))

def shader_descriptors(profile):
    return sorted((ROOT / 'pack/shaderpacks').glob('*.pw.toml'))

def downloads(profile):
    return descriptors(profile) + resource_descriptors(profile) + shader_descriptors(profile)

def download_path(descriptor):
    pin = tomllib.loads(descriptor.read_text())
    return descriptor.parent.name + '/' + pin['filename']

def configs(profile):
    files = {p.relative_to(ROOT / 'pack').as_posix(): p.read_bytes()
            for p in sorted((ROOT / 'pack/config').rglob('*')) if p.is_file()}
    options = ROOT / 'pack/options.txt'
    if options.exists():
        files['options.txt'] = options.read_bytes()
    return files

def pack_version():
    return tomllib.loads((ROOT / 'pack/pack.toml').read_text())['version']

def artifact_name(profile='main'):
    if profile != 'main':
        raise ValueError('Solo existe una composición principal')
    return f'Lumina-Optimized-{pack_version()}.mrpack'
