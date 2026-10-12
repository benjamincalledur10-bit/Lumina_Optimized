# Changelog v26.3-beta.1 — 2026-10-11

Primera beta identificada por la versión del juego. Se conserva la composición de alpha.5 y sus configuraciones; Minecraft 26.3, Java 25 y Loader 0.19.5. Tag nuevo `v26.3-beta.1`; historial y releases anteriores intactos.

## Añadido

Los cuatro resource packs se descargan por packwiz desde Modrinth y quedan activados por solicitud del usuario. `options.txt` solo contiene versión de datos 5023, lista de recursos y aceptación del formato anterior de Mandala; no fija resolución, distancias, animaciones, calidad ni FPS.

| Recurso | Versión | ID de versión | Estado |
| --- | --- | --- | --- |
| [Translations for Sodium](https://modrinth.com/resourcepack/translations-for-sodium/version/JeuAsdpW) | v8.19.0 | `JeuAsdpW` | Publicado para 26.3; activo |
| [Fresh Animations](https://modrinth.com/resourcepack/fresh-animations/version/RGIzA5em) | 1.10.5 | `RGIzA5em` | Publicado para 26.3; activo |
| [Fullbright UB](https://modrinth.com/resourcepack/fullbright-ub/version/SmHiPjfF) | 7.0 | `SmHiPjfF` | Publicado para 26.3; activo |
| [Mandala's GUI - Dark mode](https://modrinth.com/resourcepack/mandalas-gui-dark-mode/version/Z2ajDlEE) | 2.1 | `Z2ajDlEE` | **Hasta 1.21.11; compatibilidad visual pendiente**; activo |

Créditos: Translations for Sodium y sus traductores; **FreshLX** por Fresh Animations; **World Resource Pack** por Fullbright UB; **CesarZorak / Mandala Creations** por Mandala’s GUI. Archivos originales sin modificaciones: el .mrpack contiene URLs/hashes, no los ZIP de terceros. Fresh Animations y Mandala permiten su inclusión en modpacks; créditos y fuentes oficiales conservados.

**PolyTone 26.3-6.8.6-alpha**, ID `qM0zPlR5`, Fabric 26.3: soporte de Fullbright con Sodium según la descripción del autor. JAR interno `26.3-6.8.6`; necesita Loader >=0.19.3 y Fabric API >=0.162.0+26.3, ya satisfechos; declara incompatible Sodium <0.9, y usamos 0.9.2. Integra CodecUI 26.3-1.4.7 (Loader >=0.19.5), exp4j 0.4.8 y nexp 1.2.1; no se duplican externamente. Publicación alpha, validación de juego pendiente.

Fullbright altera la iluminación visual; Fresh Animations cambia modelos/animaciones y Mandala la interfaz. No se atribuyen mejoras de FPS a estos recursos. No se añadieron extensiones de Fresh Animations. BBE continúa activo; su compatibilidad con modelos EMF/ETF, especialmente shulkers, requiere comprobación visual.

## Revisión de shaders sobre la misma beta.1

Por solicitud del usuario se mantiene `v26.3-beta.1` y se reemplaza el `.mrpack` publicado. Se añaden mediante packwiz, con versiones fijas y SHA-1/SHA-512 oficiales:

| Shader | Versión | ID de versión | Estado inicial |
| --- | --- | --- | --- |
| [Lumina Event Horizon](https://modrinth.com/shader/lumina-shader-event-horizon/version/pZJyyZZ4) | 1.3.9 | `pZJyyZZ4` | Instalado; apagado |
| [Lumina Lite](https://modrinth.com/shader/lumina-shader-lite/version/AC7c1gBI) | 1.2.9 | `AC7c1gBI` | Instalado; apagado |

Ambos están publicados para Minecraft 26.3 e Iris. No se cambia ningún mod, recurso ni configuración de la beta anterior. En Iris se elige un shader a la vez; no se activa ninguno automáticamente. Créditos: **Benjiaa**, shaders basados en [Complementary Reimagined](https://www.complementary.dev/). Los ZIP originales se descargan desde Modrinth, conservando Complementary License Agreement 1.6; no se redistribuyen como binarios en overrides. El autor de Lumina Optimized asume la responsabilidad de la integración conforme a su sección 1.2.

Se verifican publicaciones, versiones, hashes, integridad ZIP, raíz `shaders/`, licencias y exportación. La compilación y el uso en Minecraft quedan pendientes. El arranque de 45 segundos previo no valida esta revisión ni shaders activados. No se afirma mejora de FPS. El ZIP CurseForge adjunto corresponde a la composición anterior, sin estos dos shaders, y mantiene sus bloqueos de publicación.

## Inventario fijo completo

35 principales + 7 bibliotecas externas + 1 mod de soporte de recursos = **43 JAR**. Cuatro resource packs y dos shader packs separados = **49 archivos descargables**. El conteo de módulos integrados consta en la validación; no se suman como principales ni se añaden JAR duplicados.

| Nombre | Versión | Clase |
| --- | --- | --- |
| [BadOptimizations](https://modrinth.com/mod/badoptimizations/version/Sp0ctspw) | 2.4.1 | Principal |
| [Better Block Entities](https://modrinth.com/mod/better-block-entities/version/9VvhfLcA) | 1.3.9+mc26.3 | Principal |
| [Better Mount HUD](https://modrinth.com/mod/better-mount-hud/version/M3Fe5t0L) | 1.3.1 | Principal |
| [BetterGrassify](https://modrinth.com/mod/bettergrassify/version/8qcmuwZa) | 1.8.8+fabric.26.3 | Principal |
| [Concurrent Chunk Management Engine (Fabric)](https://modrinth.com/mod/c2me-fabric/version/ODMLK8M9) | 0.4.2-alpha.0.90+26.3 | Principal |
| [Chunky](https://modrinth.com/mod/chunky/version/4Eotm6ov) | 1.5.3 | Principal |
| [Cloth Config API](https://modrinth.com/mod/cloth-config/version/fg2uyxOW) | 26.3.159+fabric | Biblioteca externa |
| [Clumps](https://modrinth.com/mod/clumps/version/J4I1wxJZ) | 26.3.2 | Principal |
| [Crash Assistant](https://modrinth.com/mod/crash-assistant/version/alR3tamq) | 1.11.14 | Principal |
| [Cull Leaves](https://modrinth.com/mod/cull-leaves/version/jqOVPlQ8) | 4.1.2+26.3-fabric | Principal |
| [Debugify](https://modrinth.com/mod/debugify/version/FMaS2nZn) | 26.3.0.0 | Principal |
| [e4mc](https://modrinth.com/mod/e4mc/version/RNDvrMAd) | 6.2.3-fabric-modern | Principal |
| [[EMF] Entity Model Features](https://modrinth.com/mod/entity-model-features/version/N7d5LddE) | 3.3.11-fabric-26.3 | Principal |
| [Entity Culling](https://modrinth.com/mod/entityculling/version/X1g3VhTx) | 1.11.3 | Principal |
| [[ETF] Entity Texture Features](https://modrinth.com/mod/entitytexturefeatures/version/O8J3sxxp) | 7.2.5-fabric-26.3 | Principal |
| [Fabric API](https://modrinth.com/mod/fabric-api/version/v2j28coa) | 0.162.0+26.3 | Biblioteca externa |
| [Fabric Language Kotlin](https://modrinth.com/mod/fabric-language-kotlin/version/SKW1BTL3) | 1.14.2+kotlin.2.4.21 | Biblioteca externa |
| [Fast IP Ping](https://modrinth.com/mod/fast-ip-ping/version/N6hOHbOO) | v1.0.12-mc26.3 | Principal |
| [FastQuit](https://modrinth.com/mod/fastquit/version/ZZ5dfboC) | 3.1.5+mc26.2 | Principal |
| [FerriteCore](https://modrinth.com/mod/ferrite-core/version/d5ddUdiB) | 9.0.0-fabric | Principal |
| [Forge Config API Port](https://modrinth.com/mod/forge-config-api-port/version/JpKvrr9J) | 26.3.1 | Biblioteca externa |
| [Geckolib](https://modrinth.com/mod/geckolib/version/kSxHvs99) | 5.5.7 | Biblioteca externa |
| [Gnetum](https://modrinth.com/mod/gnetum/version/F4CsYAnb) | 4.6.3+26.3-fabric | Principal |
| [ImmediatelyFast](https://modrinth.com/mod/immediatelyfast/version/3MP9UR23) | 1.17.1+26.3-fabric | Principal |
| [Iris Shaders](https://modrinth.com/mod/iris/version/vTN4NRGW) | 1.11.7+26.3-fabric | Principal |
| [Ixeris](https://modrinth.com/mod/ixeris/version/QocCYDs0) | 4.6.8+26.3-fabric | Principal |
| [LambDynamicLights - Dynamic Lights](https://modrinth.com/mod/lambdynamiclights/version/rylKnJ4M) | 4.13.0+26.3 | Principal |
| [Lithium](https://modrinth.com/mod/lithium/version/xS0Q8LSi) | mc26.3-0.26.2-fabric | Principal |
| [ModernFix-mVUS](https://modrinth.com/mod/modernfix-mvus/version/pa9cAfYg) | 5.27.20-build.2 | Principal |
| [Mod Menu](https://modrinth.com/mod/modmenu/version/kyy7dbrZ) | 21.0.0 | Principal |
| [More Culling](https://modrinth.com/mod/moreculling/version/t7vAlfgO) | 1.9.0 | Principal |
| [Reese's Sodium Options](https://modrinth.com/mod/reeses-sodium-options/version/EfchygKx) | mc26.3-2.2.5+fabric | Principal |
| [Remove Reloading Screen](https://modrinth.com/mod/rrls/version/CAVJGGfj) | 5.2.8+mc26.3 | Principal |
| [ServerCore](https://modrinth.com/mod/servercore/version/LCG1Bm84) | 1.5.20+26.3 | Principal |
| [Skyboxify](https://modrinth.com/mod/skyboxify/version/LSewIGOo) | 3.4 | Principal |
| [Sodium Extra](https://modrinth.com/mod/sodium-extra/version/te2y9qZn) | mc26.3-0.9.4+fabric | Principal |
| [Sodium](https://modrinth.com/mod/sodium/version/bAZQdGpg) | mc26.3-0.9.2-fabric | Principal |
| [Sodium Shadowy Path Blocks (SSPB)](https://modrinth.com/mod/sodium-shadowy-path-blocks/version/gobiZrtK) | 8.0.0-fabric | Principal |
| [YetAnotherConfigLib (YACL)](https://modrinth.com/mod/yacl/version/s9SjoFu1) | 3.9.7+26.3-fabric | Biblioteca externa |
| [ZConfig](https://modrinth.com/mod/zconfig/version/tsgt79sG) | 1.0.0+26.x | Biblioteca externa |
| [Fast Noise](https://modrinth.com/mod/zfastnoise/version/cCGI5KLE) | 1.1.1+26.3 | Principal |
| [Zoomify (Zoom)](https://modrinth.com/mod/zoomify/version/bvz5KJLQ) | 2.16.3+26.3 | Principal |
| [Polytone](https://modrinth.com/mod/polytone/version/qM0zPlR5) | 26.3-6.8.6-alpha | Soporte de recursos |

Text Placeholder API 3.2.0+26.3 sigue integrado en Mod Menu/ServerCore; no JAR externo. Los pins anteriores y bytes de configuraciones se contrastan con alpha.5. Se mantiene BBE activo, Iris apagado, luces Off, corrección de caché ModernFix/Lithium, ServerCore conservador y las opciones de hojas acordadas.

## Evidencia y pendientes

[Validación de esta beta](validation-26.3-beta.1.md). Las comprobaciones de publicación, hashes, dependencias, configuraciones y exportación se separan del arranque y del juego. El reporte positivo del usuario y sus lecturas de FPS pertenecen a **alpha.5 sin estos recursos**, no a beta.1. No se afirma mejora de FPS. Pendientes: importación, mundo, exploración, aspecto/HUD con recursos, guardar/reabrir FastQuit/C2ME, estabilidad prolongada y Windows/Linux.
