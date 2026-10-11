# Changelog 0.1.0-alpha.5

Preparado el **2026-10-11**, en `modpackdev`, desde alpha.4 (`7b135ef`). Minecraft 26.3 / Java 25 / Fabric Loader 0.19.5. Una composición principal con Iris; desaparece la matriz activa Core/Shaders de alpha.4.

## Reconstrucción

Se seleccionaron de nuevo las 42 entradas solicitadas. No se incorporaron Structure Layout Optimizer, Resourceful Config, ScalableLux, Krypton, Jasione, Async Logger, Better Biome Blend, Fast Surface ni FastMapCodec. No son sustituidos. Alpha.4 permanece reproducible desde su commit/tag y conserva una instantánea de fuentes, scripts, validación y checksums en `history/alpha.4/`.

Respecto a alpha.4, entran EMF, ETF, Better Mount HUD, Debugify, e4mc, Fabric Language Kotlin, FastQuit, Forge Config API Port, LambDynamicLights, Reese’s Sodium Options, Remove Reloading Screen, Skyboxify, Sodium Shadowy Path Blocks, YACL, Zoomify, Cull Leaves y GeckoLib. Entity Culling pasa de 1.11.2 a 1.11.3; Fabric API de 0.161.0 a 0.162.0+26.3; C2ME de alpha.0.89 a alpha.0.90. El resto de las entradas comunes mantiene sus versiones al coincidir con la selección actual compatible.

Se mantiene Sodium 0.9.2 estable: la [publicación de Iris 1.11.7](https://modrinth.com/mod/iris/version/vTN4NRGW) exige su ID exacto `bAZQdGpg`; se descarta Sodium 0.9.3-alpha.1. Reese’s 2.2.5 y Sodium Extra 0.9.4 aceptan esa combinación. No se añade Sodium Options API; Greenlight viene integrado.

Zoomify **2.16.3+26.3** se selecciona desde su publicación exclusiva Fabric. No se usa 2.17.0 universal: sus metadatos comunes incluyen Kotlin for Forge/NeoForge como obligatorio, además de Fabric Language Kotlin. Esto no demuestra un fallo del JAR universal, pero impide cerrar sus dependencias de publicación sin una excepción; se evita esa ambigüedad en esta base.

## Mods principales: 35

| Mod | Versión publicada fijada | ID de versión |
| --- | --- | --- |
| BadOptimizations | 2.4.1 | [Sp0ctspw](https://modrinth.com/mod/badoptimizations/version/Sp0ctspw) |
| Better Block Entities | 1.3.9+mc26.3 | [9VvhfLcA](https://modrinth.com/mod/better-block-entities/version/9VvhfLcA) |
| Better Mount HUD | 1.3.1 | [M3Fe5t0L](https://modrinth.com/mod/better-mount-hud/version/M3Fe5t0L) |
| BetterGrassify | 1.8.8+fabric.26.3 | [8qcmuwZa](https://modrinth.com/mod/bettergrassify/version/8qcmuwZa) |
| Concurrent Chunk Management Engine (Fabric) | 0.4.2-alpha.0.90+26.3 | [ODMLK8M9](https://modrinth.com/mod/c2me-fabric/version/ODMLK8M9) |
| Chunky | 1.5.3 | [4Eotm6ov](https://modrinth.com/mod/chunky/version/4Eotm6ov) |
| Clumps | 26.3.2 | [J4I1wxJZ](https://modrinth.com/mod/clumps/version/J4I1wxJZ) |
| Crash Assistant | 1.11.14 | [alR3tamq](https://modrinth.com/mod/crash-assistant/version/alR3tamq) |
| Cull Leaves | 4.1.2+26.3-fabric | [jqOVPlQ8](https://modrinth.com/mod/cull-leaves/version/jqOVPlQ8) |
| Debugify | 26.3.0.0 | [FMaS2nZn](https://modrinth.com/mod/debugify/version/FMaS2nZn) |
| e4mc | 6.2.3-fabric-modern | [RNDvrMAd](https://modrinth.com/mod/e4mc/version/RNDvrMAd) |
| [EMF] Entity Model Features | 3.3.11-fabric-26.3 | [N7d5LddE](https://modrinth.com/mod/entity-model-features/version/N7d5LddE) |
| Entity Culling | 1.11.3 | [X1g3VhTx](https://modrinth.com/mod/entityculling/version/X1g3VhTx) |
| [ETF] Entity Texture Features | 7.2.5-fabric-26.3 | [O8J3sxxp](https://modrinth.com/mod/entitytexturefeatures/version/O8J3sxxp) |
| Fast IP Ping | v1.0.12-mc26.3 | [N6hOHbOO](https://modrinth.com/mod/fast-ip-ping/version/N6hOHbOO) |
| FastQuit | 3.1.5+mc26.2 | [ZZ5dfboC](https://modrinth.com/mod/fastquit/version/ZZ5dfboC) |
| FerriteCore | 9.0.0-fabric | [d5ddUdiB](https://modrinth.com/mod/ferrite-core/version/d5ddUdiB) |
| Gnetum | 4.6.3+26.3-fabric | [F4CsYAnb](https://modrinth.com/mod/gnetum/version/F4CsYAnb) |
| ImmediatelyFast | 1.17.1+26.3-fabric | [3MP9UR23](https://modrinth.com/mod/immediatelyfast/version/3MP9UR23) |
| Iris Shaders | 1.11.7+26.3-fabric | [vTN4NRGW](https://modrinth.com/mod/iris/version/vTN4NRGW) |
| Ixeris | 4.6.8+26.3-fabric | [QocCYDs0](https://modrinth.com/mod/ixeris/version/QocCYDs0) |
| LambDynamicLights - Dynamic Lights | 4.13.0+26.3 | [rylKnJ4M](https://modrinth.com/mod/lambdynamiclights/version/rylKnJ4M) |
| Lithium | mc26.3-0.26.2-fabric | [xS0Q8LSi](https://modrinth.com/mod/lithium/version/xS0Q8LSi) |
| ModernFix-mVUS | 5.27.20-build.2 | [pa9cAfYg](https://modrinth.com/mod/modernfix-mvus/version/pa9cAfYg) |
| Mod Menu | 21.0.0 | [kyy7dbrZ](https://modrinth.com/mod/modmenu/version/kyy7dbrZ) |
| More Culling | 1.9.0 | [t7vAlfgO](https://modrinth.com/mod/moreculling/version/t7vAlfgO) |
| Reese's Sodium Options | mc26.3-2.2.5+fabric | [EfchygKx](https://modrinth.com/mod/reeses-sodium-options/version/EfchygKx) |
| Remove Reloading Screen | 5.2.8+mc26.3 | [CAVJGGfj](https://modrinth.com/mod/rrls/version/CAVJGGfj) |
| ServerCore | 1.5.20+26.3 | [LCG1Bm84](https://modrinth.com/mod/servercore/version/LCG1Bm84) |
| Skyboxify | 3.4 | [LSewIGOo](https://modrinth.com/mod/skyboxify/version/LSewIGOo) |
| Sodium Extra | mc26.3-0.9.4+fabric | [te2y9qZn](https://modrinth.com/mod/sodium-extra/version/te2y9qZn) |
| Sodium | mc26.3-0.9.2-fabric | [bAZQdGpg](https://modrinth.com/mod/sodium/version/bAZQdGpg) |
| Sodium Shadowy Path Blocks (SSPB) | 8.0.0-fabric | [gobiZrtK](https://modrinth.com/mod/sodium-shadowy-path-blocks/version/gobiZrtK) |
| Fast Noise | 1.1.1+26.3 | [cCGI5KLE](https://modrinth.com/mod/zfastnoise/version/cCGI5KLE) |
| Zoomify (Zoom) | 2.16.3+26.3 | [bvz5KJLQ](https://modrinth.com/mod/zoomify/version/bvz5KJLQ) |

## Bibliotecas externas: 7

| Biblioteca | Versión | Motivo |
| --- | --- | --- |
| [Cloth Config API](https://modrinth.com/mod/cloth-config/version/fg2uyxOW) | 26.3.159+fabric | More Culling, FastQuit y pantallas de configuración |
| [Fabric API](https://modrinth.com/mod/fabric-api/version/v2j28coa) | 0.162.0+26.3 | API y módulos requeridos por diversos mods |
| [Fabric Language Kotlin](https://modrinth.com/mod/fabric-language-kotlin/version/SKW1BTL3) | 1.14.2+kotlin.2.4.21 | Zoomify; bibliotecas Kotlin integradas |
| [Forge Config API Port](https://modrinth.com/mod/forge-config-api-port/version/JpKvrr9J) | 26.3.1 | Entrada solicitada; configuración compatible con Fabric |
| [Geckolib](https://modrinth.com/mod/geckolib/version/kSxHvs99) | 5.5.7 | Entrada solicitada; sin consumidor obligatorio adicional identificado |
| [YetAnotherConfigLib (YACL)](https://modrinth.com/mod/yacl/version/s9SjoFu1) | 3.9.7+26.3-fabric | Skyboxify y Zoomify |
| [ZConfig](https://modrinth.com/mod/zconfig/version/tsgt79sG) | 1.0.0+26.x | Dependencia adicional obligatoria de Fast Noise |

Text Placeholder API **3.2.0+26.3**, ID `lXytLqWj`, está integrada en Mod Menu y ServerCore: sus bytes coinciden con el SHA-512 publicado. No se descarga un tercer proveedor. La lista solicitada contiene 35 principales y 7 bibliotecas; seis bibliotecas son externas y una integrada. ZConfig eleva a siete las bibliotecas externas de la distribución, sin elevar el número de principales.

## Módulos integrados y validación

**142 apariciones**, **117 IDs distintos**, **116 IDs seleccionados** en el análisis estático. Se excluye Loader de ese conteo; sus módulos se registran aparte. Fabric enumera **162 IDs** reales en el arranque. Las copias anidadas originales se conservan; no se extraen ni reempaquetan. [Inventario completo](validation.json).

BBE queda activado, Iris y LambDynamicLights apagados inicialmente. Se mantiene la corrección de temperatura ModernFix/Lithium, ServerCore conserva comportamiento vanilla y no se distribuyen ajustes de resolución/distancias. More Culling no solapa las hojas de Cull Leaves. Sodium Extra fija su opción real `extra_settings.reduce_resolution_on_mac=false`; Gnetum mantiene `downscale=OFF`.

Todos los pins y los 43 registros de publicación (42 descargas + Placeholder integrado) fueron contrastados con Modrinth el 2026-10-11. No quedan archivos objetivo sin publicación Fabric 26.3 ni hashes pendientes. El arranque encontró una limitación EMF/BBE que se documenta, no se oculta ni se presenta como compatibilidad completa. FastQuit protege la coexistencia con Ixeris desactivando servidores simultáneos en código; guardado/reapertura con C2ME y HUD con Gnetum/ImmediatelyFast/Better Mount HUD siguen pendientes.

[Configuración y limitaciones](configuration-alpha.5.md) · [Validación y arranque](validation-alpha.5.md) · [Prueba en Mac](benchmarks.md). No se añadieron nuevas mediciones ni se prometen 200 FPS. No hay entradas retiradas por falta de archivo; la compatibilidad visual EMF/BBE permanece pendiente de juego.
