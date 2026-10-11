"""Una composición explícita de alpha.5; las matrices anteriores están en el historial."""
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]

def profiles():
    manifest = tomllib.loads((ROOT / 'pack/pack.toml').read_text())
    return {'main': {key: manifest[key] for key in ('name', 'description')}}

def descriptors(profile):
    return sorted((ROOT / 'pack/mods').glob('*.pw.toml'))

def configs(profile):
    return {p.relative_to(ROOT / 'pack').as_posix(): p.read_bytes()
            for p in sorted((ROOT / 'pack/config').rglob('*')) if p.is_file()}

def pack_version():
    return tomllib.loads((ROOT / 'pack/pack.toml').read_text())['version']

def artifact_name(profile='main'):
    if profile != 'main':
        raise ValueError('Alpha.5 tiene una sola composición principal')
    return f'Lumina-Optimized-{pack_version()}.mrpack'
