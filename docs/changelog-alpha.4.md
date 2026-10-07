# Changelog 0.1.0-alpha.4

Preparación local en `modpackdev`, sobre alpha.3 (`46b27a1`), continuando los cambios anteriores. Minecraft **26.3**, Java **25** y Fabric Loader **0.19.5** permanecen fijos. Los cambios de esta alpha se preparan para publicar en `modpackdev`; tag previsto `v0.1.0-alpha.4`.

## Añadidos e integración

Se completan los siete JAR pendientes: **ServerCore 1.5.20+26.3, Krypton 0.3.2, Jasione 1.0.9+26.1.2-fabric, Async Logger 2.2.2+26.1.2-fabric, Better Biome Blend (archivo 26.3-1.4.0), Fast Surface 1.0.0+26.3 y FastMapCodec 1.0.4 Fabric**. Se inspeccionaron desde Descargas; solo sus metadatos y configuraciones se incorporan al repositorio. Los pins conservan las URLs oficiales de CDN Modrinth, sin rutas `file://` ni JAR subidos.

`alpha3-reference` conserva Core alpha.3 y sus mediciones como referencia, BBE activo. `optimizations` añade las optimizaciones primero (C2ME, ScalableLux, Gnetum, Sodium Extra, Ixeris, ModernFix, Clumps, ServerCore, Krypton, Jasione, Async Logger, Fast Surface y FastMapCodec). Después `core` añade utilidades y opciones visuales: Fast IP Ping, Crash Assistant, Chunky, Mod Menu, BetterGrassify y Better Biome Blend. `shaders` deriva del mismo conjunto y solo añade Iris. No se mantienen dos copias independientes.

Las cuatro versiones que requerían elección ya fueron fijadas en la preparación anterior: **Crash Assistant 1.11.14, BetterGrassify 1.8.8+fabric.26.3, Clumps 26.3.2 y Mod Menu 21.0.0**, con archivos Fabric/26.3 verificados contra publicación, hash y tamaño. Las demás versiones de alpha.3 se conservan.

Los metadatos packwiz usan `pin=true`, IDs exactos y SHA-512. Se generan desde publicaciones conservadas en caché y, para cuatro archivos sin API accesible, desde el JAR descargado con evidencia de URL oficial y hash local; se refrescan/exportan con packwiz fijado. No se afirma haber ejecutado `packwiz modrinth add` con descarga de red satisfactoria. [Publicaciones disponibles](research/publications-alpha.4.json), [siete descargas locales y alcance](research/local-jars-alpha.4.json).

## Versiones principales

| Nº | Mod / publicación | Versión fijada | Estado |
| ---: | --- | --- | --- |
| 1 | [Sodium](https://modrinth.com/mod/sodium/version/bAZQdGpg) | 0.9.2+mc26.3 | Incluido |
| 2 | [Iris](https://modrinth.com/mod/iris/version/vTN4NRGW) | 1.11.7+mc26.3 | Solo Shaders |
| 3 | [Entity Culling](https://modrinth.com/mod/entityculling/version/F4loCvYt) | 1.11.2 | Incluido |
| 4 | [FerriteCore](https://modrinth.com/mod/ferrite-core/version/d5ddUdiB) | 9.0.0-fabric | Incluido |
| 5 | [Lithium](https://modrinth.com/mod/lithium/version/xS0Q8LSi) | 0.26.2+mc26.3 | Incluido |
| 6 | [ImmediatelyFast](https://modrinth.com/mod/immediatelyfast/version/3MP9UR23) | 1.17.1+26.3 | Incluido |
| 7 | [Sodium Extra](https://modrinth.com/mod/sodium-extra/version/te2y9qZn) | 0.9.4+mc26.3 | Incluido |
| 8 | [More Culling](https://modrinth.com/mod/moreculling/version/t7vAlfgO) | 1.9.0 | Incluido |
| 9 | [BadOptimizations](https://modrinth.com/mod/badoptimizations/version/Sp0ctspw) | 2.4.1 | Incluido |
| 10 | [C2ME](https://modrinth.com/mod/c2me-fabric/version/FXjQDzq7) | 0.4.2-alpha.0.89+26.3 | Experimental |
| 11 | [Fast IP Ping](https://modrinth.com/mod/fast-ip-ping/version/N6hOHbOO) | v1.0.12-mc26.3 | Incluido |
| 12 | [Crash Assistant](https://modrinth.com/mod/crash-assistant/version/alR3tamq) | 1.11.14 | Incluido |
| 13 | [Chunky](https://modrinth.com/mod/chunky/version/4Eotm6ov) | 1.5.3 Fabric | Incluido |
| 14 | [BetterGrassify](https://modrinth.com/mod/bettergrassify/version/8qcmuwZa) | 1.8.8+fabric.26.3 | Incluido |
| 15 | [Ixeris](https://modrinth.com/mod/ixeris/version/QocCYDs0) | 4.6.8+26.3-fabric | Incluido |
| 16 | [Better Block Entities](https://modrinth.com/mod/better-block-entities/version/9VvhfLcA) | 1.3.9+mc26.3 | Incluido |
| 17 | [ModernFix-mVUS](https://modrinth.com/mod/modernfix-mvus/version/pa9cAfYg) | 5.27.20-build.2 | Incluido |
| 18 | [Fast Noise](https://modrinth.com/mod/zfastnoise/version/cCGI5KLE) | 1.1.1+26.3 | Incluido |
| 19 | [Gnetum](https://modrinth.com/mod/gnetum/version/F4CsYAnb) | 4.6.3+26.3-fabric | Incluido |
| 20 | [Better Biome Blend](https://modrinth.com/mod/better-biome-blend/version/Oag8dQao) | 26.3-1.4.0-fabric | Incluido; SHA-512 contrastado (2026-10-06) |
| 21 | [Clumps](https://modrinth.com/mod/clumps/version/J4I1wxJZ) | 26.3.2 | Incluido |
| 22 | [Structure Layout Optimizer](https://modrinth.com/mod/structure-layout-optimizer/version/crWm7jXS) | 1.1.4+26.3-fabric | Incluido |
| 23 | [Jasione](https://modrinth.com/mod/jasione/version/kbKBk4b3) | 1.0.9+26.1.2-fabric | Incluido; SHA-512 contrastado (2026-10-06) |
| 24 | [Fast Surface](https://modrinth.com/mod/zfastsurface/version/yOBmJfgG) | 1.0.0+26.3 | Incluido; SHA-512 contrastado (2026-10-06) |
| 25 | [ScalableLux](https://modrinth.com/mod/scalablelux/version/g4eqNSKd) | 0.3.0-alpha.0.6+26.3 | Experimental |
| 26 | [Krypton](https://modrinth.com/mod/krypton/version/UugdIYJw) | 0.3.2 | Incluido |
| 27 | [ServerCore](https://modrinth.com/mod/servercore/version/LCG1Bm84) | 1.5.20+26.3 | Incluido |
| 28 | [Async Logger](https://modrinth.com/mod/asynclogger/version/Ert0LmWj) | 2.2.2+26.1.2-fabric | Incluido |
| 29 | [FastMapCodec](https://modrinth.com/mod/fastmapcodec/version/I6Iu1TAV) | 1.0.4 | Incluido; SHA-512 contrastado (2026-10-06) |
| 30 | [Mod Menu](https://modrinth.com/mod/modmenu/version/kyy7dbrZ) | 21.0.0 | Incluido |

Iris solo está en Shaders. Fast IP Ping declara internamente 1.0.12 y FerriteCore 9.0.0. Better Biome Blend declara **1.4.0**; su archivo Fabric identifica Minecraft 26.3. Jasione y Async Logger conservan el sufijo 26.1.2 del archivo; sus predicados aceptan 26.3. Async Logger también aparece publicado para 26.3 en los metadatos conservados; para Jasione el SHA-512 de su versión exacta coincide con la evidencia aportada del 2026-10-06; los metadatos completos de publicación siguen pendientes.

## Dependencias y recuento

| Dependencia externa | Versión | Uso |
| --- | --- | --- |
| Fabric API | 0.161.0+26.3 | Módulos base, ServerCore, Better Biome Blend y otras publicaciones |
| Cloth Config API | 26.3.159+fabric | More Culling y opciones existentes |
| Resourceful Config | 6.0.1 | Structure Layout Optimizer |
| ZConfig | 1.0.0+26.x | Fast Noise y Fast Surface |

No fue necesario agregar una quinta dependencia externa según los JAR y las publicaciones disponibles. Placeholder API **3.2.0+26.3** está integrado en Mod Menu y ServerCore; se verificó su hash publicado y se selecciona una sola copia. ServerCore incluye DazzleConf **1.3.0-M2** y SnakeYAML **2.7**; Krypton, Velocity Native **3.4.0-SNAPSHOT**. Sodium Extra integra Greenlight API **0.1.0+mc26.3** y no requiere Sodium Options API. Loader proporciona MixinExtras **0.5.5**; no se duplica externamente. Async Logger incluye Disruptor y NightConfig sombreado; Jasione incluye NightConfig sombreado. [Requisitos y bibliotecas](dependencies.md).

| Perfil | Principales | Dependencias externas | IDs integrados seleccionados | JAR descargables |
| --- | ---: | ---: | ---: | ---: |
| `alpha3-reference` | 10 | 4 | 51 | 14 |
| `optimizations` | 23 | 4 | 83 | 27 |
| `core` | 29 | 4 | 83 | 33 |
| `shaders` | 30 | 4 | 86 | 34 |
| `core-conservative` | 26 | 4 | 57 | 30 |
| `shaders-conservative` | 27 | 4 | 60 | 31 |
| `gnetum-control` | 28 | 4 | 83 | 32 |

Los IDs integrados se seleccionan entre módulos anidados de los JAR del pack; se excluyen los aportados por Loader y el entorno. Core: 101 apariciones anidadas / 84 IDs distintos / 83 seleccionados; Shaders: 106 / 87 / 86. Las clases de bibliotecas sombreadas no se cuentan como módulos Fabric adicionales. Fabric real enumera 120 y 124 IDs totales, respectivamente; no son mods principales.

## Configuraciones conservadas y ajustes justificados

- **BBE activo** en todos los paquetes (`optimize.master=true`). Las demás opciones, animaciones y configuraciones de alpha.3 se conservan.
- **More Culling:** 1.9.0 usa `Toml4jConfigSerializer` y `moreculling.toml`. El JSON histórico no imponía los valores acordados: en el primer intento se generaron defaults con LOD/3-face/sign/rain/block-state culling activos. Se añade TOML con exactamente los valores del JSON conservador, sin LOD ni esos recortes; se conserva el JSON y la referencia alpha.3 sin cambios. Esta corrección afecta la configuración efectiva y debe tenerse en cuenta al comparar con las mediciones históricas.
- SLO mantiene **`deduplicateShuffledTemplatePoolElementList=false`**. Iris comienza con **`enableShaders=false`**, sin shader pack.
- **ModernFix/Lithium:** se conserva `mixin.perf.remove_biome_temperature_cache=false`. Desactiva el caché duplicado de ModernFix que produjo un overwrite de `getTemperature`; Lithium se mantiene. Las repeticiones reales leen el flag y no muestran de nuevo ese aviso. ModernFix desactiva automáticamente cuatro opciones ante C2ME; se respetan esas decisiones.
- **ServerCore:** YAML contrastado con las clases de 1.5.20+26.3. `dynamic.enabled=false`, sin defaults que impongan distancias ni lista de ajustes dinámicos. Activation range, lobotomización, breeding caps y mobcaps especiales apagados. Las categorías de spawning conservan los valores vanilla calculados por el autor; radios de fusión e intervalo de guardado conservan defaults. `reduce-sync-loads=false` evita cambiar qué chunks actualizan mapas; `fast-biome-lookups` y `cancel-duplicate-fluid-ticks` permanecen false. Solo `cache-ticking-chunks` conserva su default true entre opciones del YAML de optimizaciones.
- **Better Biome Blend:** su default usa índice 14 (29×29), mientras Minecraft 26.3 usa 2 (5×5). El override mínimo de `options.txt` fija ambos radios a 2 y la versión de formato a 5023. No incluye resolución, distancias ni otros ajustes gráficos; si la referencia del usuario usaba otro radio, debe igualarse antes de comparar. La [mezcla 3D y OKLab](https://modrinth.com/mod/better-biome-blend) cambia las transiciones incluso con el mismo radio. No se presenta como apariencia idéntica.
- **BetterGrassify:** defaults FANCY/LAMBDA conservados; modifica laterales de césped y nieve. No se desactivan animaciones o se reduce calidad para atribuir una mejora.
- **Gnetum:** conserva defaults de alpha.3 (HUD 60, pantallas 20, downscale apagado). Puede disminuir la frecuencia del HUD. `gnetum-control` quita solo ese mod, con ImmediatelyFast constante.
- **Async Logger:** activo, sin filtros ni supresión de debug, sin prueba de rendimiento automática. Su intento real leyó la configuración; no se ocultan errores de la alpha.
- C2ME conserva su config y el protocolo de distancia extendida apagado. C2ME y ScalableLux siguen siendo experimentales. `core-conservative`/`shaders-conservative` eliminan únicamente C2ME, ScalableLux y Gnetum.
- Chunky no inicia pregeneración automáticamente. Clumps agrupa orbes: revisar XP y Mending durante juego.

## Interacciones y límites

No apareció un conflicto cruzado declarado **Krypton/C2ME**; ambos inicializaron antes del bloqueo gráfico. **C2ME + ScalableLux + Fast Noise + Fast Surface + ZConfig** pasaron predicados y resolución real. Fast Surface exige MixinExtras ≥0.5.0 y comparte ZConfig, ya cubiertos. Esto no comprueba iluminación, exploración, generación o guardado. Jasione declara Redirector incompatible; Fast Surface, Moonrise. Esos mods no están presentes. La [incompatibilidad de FastMapCodec con Sodium Extra](https://modrinth.com/mod/fastmapcodec) es específica de NeoForge, no de los JAR Fabric usados.

C2ME desactivó automáticamente `natives_math` por falta de biblioteca macOS ARM64. Se registran también avisos de refmaps/clases opcionales, servicios de red bloqueados y restricción `sysctl` de Crash Assistant. No se añade una dependencia obligatoria por una clase de compatibilidad opcional ausente.

## Validado y pendiente

Se generaron **7 `.mrpack`** con packwiz, completos y con hashes/manifests/overrides comprobados; pasaron **17 pruebas estáticas**. Las dependencias reales e integradas de todos los JAR se revisaron. **34 de 34 archivos únicos** tienen contraste de hashes publicados. El **7 de octubre de 2026** se comprobaron los cuatro restantes contra los SHA-512 aportados por el usuario, recuperados de metadatos oficiales Modrinth el **6 de octubre de 2026**: Jasione `kbKBk4b3`, Better Biome Blend `Oag8dQao`, Fast Surface `yOBmJfgG` y FastMapCodec `I6Iu1TAV`. Coinciden versiones/IDs, JAR locales, pins packwiz y todos los exports que los incluyen. No hubo discrepancias; los paquetes existentes no se modificaron ni regeneraron. [Evidencia fechada](research/modrinth-sha512-alpha.4.json). Los metadatos completos de esas cuatro publicaciones siguen pendientes; el extracto de hashes no incluye dependencias ni listas de compatibilidad y no se presentó como respuesta fresca de API. No quedan JAR objetivo pendientes de incorporación.

Los intentos reales finales con Java 25 de Core y Shaders aceptaron el resolvedor Fabric, pero **SDL sigue sin encontrar pantalla**. No se llegó a un mundo. Importación, arranque completo, estabilidad, exploración, guardado/reapertura y fluidez deben revisarse en el Mac durante **10–15 minutos**. Sin benchmarks adicionales, mediciones nuevas ni afirmaciones de ganancia de FPS. Los paquetes/mediciones históricos quedan intactos.

[Validación detallada](validation-alpha.4.md), [prueba sencilla](benchmarks.md). Paquetes en `dist/`, junto con `SHA256SUMS-0.1.0-alpha.4`; los artefactos y JAR no se incluyen en Git.
