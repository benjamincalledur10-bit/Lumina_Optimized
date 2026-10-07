# Lumina Optimized

**0.1.0-alpha.4**, preparación local en `modpackdev`.
Minecraft **26.3**, Java **25 de 64 bits**, Fabric Loader **0.19.5**.

**Core: 29 mods principales + 4 dependencias externas. Shaders: 30 + 4**, incluyendo Iris 1.11.7. [Versiones y changelog](docs/changelog-alpha.4.md).

## Importar

Importa uno de estos archivos de `dist/` en una instancia nueva de Modrinth App o Prism Launcher. Selecciona Java 25 nativo; ARM64 en Apple Silicon. El launcher necesita conexión para descargar los JAR desde sus URLs oficiales.

- [Core](dist/Lumina-Optimized-0.1.0-alpha.4-core.mrpack): sin Iris.
- [Shaders](dist/Lumina-Optimized-0.1.0-alpha.4-shaders.mrpack): misma base + Iris, **shaders inicialmente desactivados**, sin shader pack incluido.
- `...-core-conservative.mrpack` / `...-shaders-conservative.mrpack`: alternativas sin C2ME, ScalableLux ni Gnetum para aislar problemas.

BBE permanece activo; se conservan las configuraciones de alpha.3 y `deduplicateShuffledTemplatePoolElementList=false`. More Culling ahora recibe los valores conservadores en el TOML que realmente lee; el JSON histórico y la referencia alpha.3 se conservan. La corrección ModernFix/Lithium desactiva solo el caché de temperatura de ModernFix. ServerCore mantiene desactivados ajustes dinámicos, distancias/mobcaps y cambios de comportamiento.

No se fijan resolución, distancias ni animaciones a valores inferiores. Better Biome Blend usa **5×5**, igual al valor inicial de Minecraft, en vez de su default 29×29: el único `options.txt` distribuido contiene la versión del formato y los dos radios de mezcla. Si tu referencia usaba otro radio, iguala ese ajuste antes de comparar. BetterGrassify cambia césped/nieve y Better Biome Blend cambia las transiciones de colores; Gnetum puede actualizar el HUD menos frecuentemente. **C2ME y ScalableLux son experimentales.**

## Comprobaciones y prueba pendiente

Se verificaron JAR, hashes fijados, dependencias Fabric e integradas, conflictos declarados, configuraciones y siete exports; pasaron **17 pruebas estáticas**. Los **34 archivos únicos coinciden con hashes publicados**: los cuatro SHA-512 pendientes se contrastaron con la evidencia aportada por el usuario, recuperada de Modrinth el **2026-10-06**, comprobando versiones/IDs, JAR locales, packwiz y exports. Para esos cuatro aún faltan los metadatos completos de publicación; el contraste de hashes está cerrado. [Detalle de validación](docs/validation-alpha.4.md).

Core y Shaders aceptaron la resolución real de Fabric y llegaron a inicialización, pero **SDL sigue fallando por falta de pantalla**. No se llegó a un mundo ni se midieron FPS. Tu prueba en el Mac: importar, jugar **10–15 minutos**, explorar, revisar luz/HUD/cofres, guardar y reabrir. [Pasos](docs/benchmarks.md).

## Regenerar

Python 3.11+, packwiz fijado en `scripts/toolchain.json` y JDK 17+ para inspección; jugar requiere Java 25:

```sh
python3 scripts/build.py --packwiz .tools/bin/packwiz --cache .build/packwiz-cache
python3 scripts/test_static.py
python3 scripts/verify.py
```

La caché aislada permite exportar sin red en este workspace. En otro equipo con red, omite `--cache`; instala packwiz según la versión fijada. `pack/` y `variants/` mantienen una sola base con versiones, IDs, URLs y hashes fijos. JAR locales, cachés y `dist/` están fuera de Git; el `.mrpack` contiene URLs y configuraciones, no los JAR. `SHA256SUMS-0.1.0-alpha.4` acompaña los paquetes. El ZIP de ensayos debe extraerse antes de importar un `.mrpack`.

Historiales y mediciones previas conservados. Sin nuevas mediciones ni ganancias de FPS afirmadas.
