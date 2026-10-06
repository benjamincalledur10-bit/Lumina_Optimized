# Alpha.2: paquetes y estado

Minecraft 26.3, Java 25, Fabric Loader 0.19.5. Se mantienen Sodium 0.9.2,
Lithium 0.26.2, FerriteCore 9.0.0, ImmediatelyFast 1.17.1 e Iris 1.11.7.

## Incorporaciones fijas

| Publicación Fabric 26.3 | Requisitos reales principales |
| --- | --- |
| [Entity Culling 1.11.2](https://modrinth.com/mod/entityculling/version/F4loCvYt) | Fabric API completo; integra TRansition y TRender |
| [More Culling 1.9.0](https://modrinth.com/mod/moreculling/version/t7vAlfgO) | Loader >=0.15.0, Java >=25, Cloth Config >=16.0.0; Sodium >0.6.6, si existe; integra conditional-mixin |
| [Better Block Entities 1.3.9+mc26.3](https://modrinth.com/mod/better-block-entities/version/9VvhfLcA) | Loader >=0.16.7, Minecraft >=26.3-rc.1, Sodium >=0.9.2-beta.2; Modrinth fija exactamente Sodium bAZQdGpg |
| [Fabric API 0.161.0+26.3](https://modrinth.com/mod/fabric-api/version/bNnaTiuM) | Loader >=0.19.3, Java >=25; integra sus módulos |
| [Cloth Config 26.3.159](https://modrinth.com/mod/cloth-config/version/fg2uyxOW) | Loader >=0.14.0, Minecraft >=26.3-; integra basic-math |
| [C2ME 0.4.2-alpha.0.89+26.3](https://modrinth.com/mod/c2me-fabric/version/FXjQDzq7) | Solo pruebas: Loader >=0.18.3, Java >=25, c2me-base integrado y otros módulos transitivos |

Iris 1.11.7 y BBE comparten la publicación exacta de Sodium 0.9.2. No hay
conflictos declarados entre las versiones seleccionadas. BBE declara soporte
de shaders en su [página oficial](https://modrinth.com/mod/better-block-entities).
Esto no certifica los mixins o sombras del conjunto: falta el arranque real.

Fabric API y Sodium/Iris aportan algunos módulos con el mismo ID. El validador
ya no los trata como mods externos duplicados inválidos: recoge candidatos
anidados, compara con el parser de Loader 0.19.5 y comprueba el candidato más
reciente contra los requisitos presentes. Las alternativas y el origen elegido
se registran. Es una verificación estática de este conjunto, no el resolvedor
SAT completo de Fabric ni una prueba de inicialización.

## Matriz generada desde la misma base

Todas las variantes se describen en `variants/profiles.json`. Las configuraciones
se incluyen solo cuando su mod existe. No hay dos bases independientes.

| Sufijo del `.mrpack` | Contenido respecto a alpha.1 |
| --- | --- |
| `baseline` | Los cuatro mods originales, sin configs nuevas; etiqueta alpha.2 para control |
| `dependencies` | Baseline + Fabric API + Cloth Config |
| `dependencies-shaders` | Control anterior + Iris |
| `entity`, `entity-shaders` | Control con bibliotecas + Entity Culling; sin/con Iris |
| `more`, `more-shaders` | Control con bibliotecas + More Culling; sin/con Iris |
| `bbe`, `bbe-shaders` | Control con bibliotecas + BBE activo experimental; sin/con Iris |
| `entity-more` | Entity Culling + More Culling sobre el mismo control |
| `core`, `shaders` | Todos los anteriores; BBE incluido con master apagado para preservar referencia |
| `core-bbe-enabled`, `shaders-bbe-enabled` | Solo activación experimental de master BBE sobre Core/Shaders |
| `c2me`, `c2me-shaders` | Core/Shaders + C2ME; BBE sigue apagado |

Integración acumulativa: `dependencies → entity → entity-more → core`.
El último paso verifica presencia/conflictos de BBE, no su beneficio, pues está
apagado. Comparar `core → core-bbe-enabled` para su activación. Los perfiles
aislados separan interacción y efecto; las versiones de bibliotecas son iguales.

## Pruebas y conservación de alpha.1

No hubo mediciones de rendimiento en alpha.1. Se conserva ese hecho en
`docs/history/alpha.1/measurements.json`, el reporte original y SHA256SUMS.
Los dos `.mrpack` originales permanecen intactos en `dist/` y en la pre-release
publicada. No se reemplazan ni se inventan números de FPS/memoria/chunks.

Aplicar [el protocolo original](benchmarks.md) con ajustes/world snapshot
idénticos y cinco repeticiones. Separar shaders apagados de un shader fijado.
Para Entity Culling: escena ocluida y abierta. Para More Culling: marcos/mapas/
cuadros y bosque. Para BBE: almacenaje cercano estático y animado; paridad visual
primero. Para C2ME: terreno pregenerado y generación nueva por separado.

Mantener comparaciones por hardware: macOS ARM64, Windows x64 y Linux x64.
Además de promedio/p99/1% low, registrar chunks hasta servidor/cliente visible,
MSPT, memoria residente/heap/nativa y crecimiento de colas. No atribuir a un mod
el cambio entre alpha.1 y el conjunto completo.

## Validaciones realizadas / pendientes

Realizadas: sintaxis, versiones/IDs, hashes/tamaños, integridad de JAR y archivos
anidados, predicados con API real de Fabric, conflictos declarados, nombres de
opciones, índices, lados cliente/servidor, contenido de los 16 `.mrpack`, overrides
y bundle, conservación de alpha.1. Tests de controles aislados, dependencias
ausentes y selección entre versiones de módulos; parche Sodium aplicable.

Pendientes: importación, arranque, aceptación efectiva de configs, mixins,
estabilidad, sombras/animaciones/modelos y rendimiento en Minecraft. El JDK
local usado para inspección es 21; no se ha arrancado el juego con Java 25.

La [mejora propia](research/sodium-upload-budget.md) es una hipótesis con parche
activable/desactivable. No se compila ni se incluye todavía en los paquetes.

Estado de ejecución: **todos los ensayos de Minecraft siguen PENDIENTES**.
