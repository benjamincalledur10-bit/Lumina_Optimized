# Lumina Optimized

**0.1.0-alpha.3** · Minecraft **26.3** · Java **25 de 64 bits** · Fabric Loader **0.19.5**.
Candidatos de prueba; todavía no hay mediciones de estos candidatos ni pruebas de arranque realizadas aquí.

## Instalar y elegir

Importa **un `.mrpack`** de `dist/` en una instancia nueva de Modrinth App o Prism Launcher. Selecciona Java 25 nativo (ARM64 en Apple Silicon). El ZIP de ensayos se extrae primero; no se importa directamente.

- `...-baseline.mrpack`: alpha.2 con **BBE activado**, referencia de tus últimas mediciones.
- `...-bad.mrpack`, `...-structure.mrpack`, `...-fastnoise.mrpack`: esa base con cada candidato y sus dependencias.
- `...-core.mrpack`: los tres candidatos juntos. `...-shaders.mrpack`: mismo conjunto + Iris; sin shader packs incluidos.
- `...-gnetum.mrpack`: ensayo separado del HUD. Puede **reducir su frecuencia de actualización**. Su interacción con ImmediatelyFast en 26.3 está pendiente de probar.
- `...-c2me.mrpack`: referencia + C2ME experimental; `...-c2me-all.mrpack` y `...-c2me-shaders.mrpack`: combinación experimental.

Los **17 perfiles**, incluidos controles de bibliotecas y Gnetum sin ImmediatelyFast, están descritos en [alpha.3.md](docs/alpha.3.md). Archivos: `dist/Lumina-Optimized-0.1.0-alpha.3-<perfil>.mrpack`.

## Versiones fijadas

| Mod | Versión |
| --- | --- |
| Sodium | 0.9.2+mc26.3 |
| Lithium | 0.26.2+mc26.3 |
| FerriteCore | 9.0.0-fabric |
| ImmediatelyFast | 1.17.1+26.3 |
| Entity Culling / More Culling | 1.11.2 / 1.9.0 |
| Better Block Entities | 1.3.9+mc26.3 |
| Fabric API / Cloth Config | 0.161.0+26.3 / 26.3.159+fabric |
| BadOptimizations | 2.4.1 |
| Structure Layout Optimizer / Resourceful Config | 1.1.4+26.3-fabric / 6.0.1 |
| Fast Noise / ZConfig | 1.1.1+26.3 / 1.0.0+26.x |
| Iris, opcional | 1.11.7+mc26.3 |
| Gnetum, solo ensayo | 4.6.3+26.3-fabric |
| C2ME, experimental | 0.4.2-alpha.0.89+26.3 |

Las configuraciones anteriores se conservan; todos los perfiles nuevos derivan BBE activo cambiando solamente `optimize.master`. SLO fija `deduplicateShuffledTemplatePoolElementList=false`. No se distribuyen `options.txt` ni cambios de resolución, distancias, animaciones o calidad visual. Gnetum introduce un cambio temporal del HUD, por eso está separado. [Opciones y justificación](docs/configuration-alpha.3.md).

## Construir y validar

Python 3.11+, packwiz y conexión a Internet. Validación con JDK 17+ (`java`, `javac`, `javap`); **jugar requiere Java 25**. Packwiz se fija en `scripts/toolchain.json`.

```sh
go install github.com/packwiz/packwiz@ef87d964f8cbd52b3b13ea42453ef322290e2b9e
python3 scripts/build.py --packwiz /ruta/al/binario/packwiz
python3 scripts/test_static.py
python3 scripts/verify.py
```

`pack/` conserva la base alpha.2. `variants/profiles.json` añade candidatos desde metadatos packwiz fijados, sin mantener copias independientes. Core y Shaders se generan de esa misma fuente. `dist/SHA256SUMS-0.1.0-alpha.3` contiene los hashes de los 17 `.mrpack`; `.build/`, herramientas y exportaciones no se versionan en Git. Ejecuta la construcción completa antes de validar.

[validation.json](docs/validation.json) comprueba índices, publicaciones, descargas, hashes, requisitos transitivos, conflictos declarados, configs y exportaciones. Usa los predicados reales de Loader 0.19.5; **no ejecuta su resolvedor completo, mixins, bibliotecas nativas ni Minecraft**. Pasar estas comprobaciones no demuestra estabilidad ni mejores FPS.

## Qué falta probar

Importación, arranque y logs en macOS/Windows/Linux; paridad visual y generación del mundo; estabilidad sostenida; rendimiento A/B según [benchmarks.md](docs/benchmarks.md). Mantén los ajustes efectivos de tus mediciones anteriores. Fast Noise declara incompatibilidad con Moonrise y AntiXray; no los añadas. C2ME es alpha; revisar también bibliotecas NightConfig compartidas con ZConfig.

El usuario informa mediciones de alpha.2 con BBE activo, pero sus cifras y ajustes no fueron entregados al repositorio: [registro conservado](docs/history/alpha.2/measurements.json). No hay resultados nuevos inventados. La [hipótesis Sodium](docs/research/sodium-upload-budget.md) sigue siendo un parche de investigación, no está incluida en los paquetes. Dynamic FPS sigue fuera.

Publicaciones exactas, requisitos y evidencia: [alpha.3](docs/alpha.3.md), [dependencias](docs/dependencies.md). Historial alpha.1 y alpha.2 conservado en `docs/history/`.
