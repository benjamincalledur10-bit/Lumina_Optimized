# Validación alpha.3

## Realizado: archivos y metadatos

- Repositorio inicialmente limpio en `modpackdev`, HEAD `35ddfc4`. Publicación de esta alpha mediante el tag `v0.1.0-alpha.3`; notas en `releases/v0.1.0-alpha.3.md`.
- Incorporación con packwiz por IDs exactos; seis publicaciones Fabric compatibles con 26.3, sus dependencias externas fijadas con `pin=true`. Base alpha.2 sin actualización de mods.
- Construcción completa con packwiz fijado: **17 `.mrpack`** y ZIP de ensayos. Core/Shaders derivan del mismo perfil base; no hay dos árboles mantenidos.
- **13 pruebas estáticas** de composición/resolución: candidatos aislados, BBE constante, referencia alpha.2, unión de candidatos, matriz Gnetum con/sin ImmediatelyFast, C2ME separado, deduplicación SLO false e incompatibilidades Modrinth.
- `scripts/verify.py`: índices packwiz, URLs/publicaciones, tamaños, SHA-1/SHA-512 de descargas; CRC de JAR/ZIP; módulos integrados recursivos, requisitos Java/MC/Loader, aliases, `breaks`, `conflicts` e incompatibles Modrinth. SHA-256 de exportaciones, contenido exacto de overrides, manifest y ZIP de ensayos.
- Predicados evaluados con la API real de Fabric Loader 0.19.5. Se selecciona el candidato más reciente por ID de módulo anidado; no se ejecuta el resolvedor SAT completo de Fabric.
- Opciones de configs anteriores contrastadas con sus clases publicadas; SLO false, su clave y ruta JSONC verificadas con bytecode de SLO y Resourceful Config. No se alteraron los tres archivos fuente de configuración anteriores, C2ME ni metadatos de los nueve mods base.
- `baseline` conserva descargas/hashes y configs de alpha.2 `core-bbe-enabled`; solo cambia la identidad del pack. Historial y hashes de **2 paquetes alpha.1 y 16 alpha.2** presentes localmente verificados intactos. Mediciones alpha.2 informadas por el usuario, datos crudos no recibidos.
- `git diff --check`: sin errores de espacios.

Informe detallado: [validation.json](validation.json). Publicaciones fijadas y evidencia: [candidates-alpha.3.json](research/candidates-alpha.3.json). Inspección con Temurin JDK **21.0.9**, no con runtime de Minecraft; el juego requiere **Java 25**.

Reproducir desde la raíz:

```sh
python3 scripts/build.py --packwiz .tools/bin/packwiz
python3 scripts/test_static.py
python3 scripts/verify.py
git diff --check
```

`verify.py` escribe el informe solo tras comprobar la matriz completa. Artefactos ignorados por Git en `dist/`; toolchain fijado en `scripts/toolchain.json`.

## Pendiente: Minecraft real

| Prueba | Estado | Evidencia necesaria |
| --- | --- | --- |
| Importación en launcher | PENDIENTE | Instancia nueva, versiones efectivas y modlist |
| Arranque con Java 25 | PENDIENTE | `latest.log`, carga real de mixins y bibliotecas |
| Compatibilidad Sodium/Iris/candidatos | PENDIENTE | Mundo renderizado, reload, logs y capturas |
| SLO/Fast Noise: paridad del mundo | PENDIENTE | Comparación bloques/biomas/piezas para iguales mundos |
| Gnetum + ImmediatelyFast | PENDIENTE | Comparación 2×2, capas/cadencia/respuesta del HUD |
| C2ME + ZConfig/NightConfig | PENDIENTE | Arranque, generación, nativos, guardado/reapertura |
| Estabilidad sostenida en cada SO | PENDIENTE | Sesiones prolongadas, cambios de dimensión, errores |
| FPS/frametimes/memoria/chunks | PENDIENTE | Cinco repeticiones, datos crudos y ajustes iguales |

No se ejecutó Minecraft en esta tarea. Ausencia de conflictos declarados no garantiza compatibilidad funcional. La integración OpenCL anidada de Fast Noise no demuestra aceleración activada. No se atribuye mejora de FPS, tirones, memoria o generación a ningún candidato sin medición.

Protocolo y orden de comparación: [benchmarks.md](benchmarks.md). Plantilla sin resultados: [test-results-alpha.3.csv](test-results-alpha.3.csv).
