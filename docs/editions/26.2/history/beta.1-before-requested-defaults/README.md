# Lumina Optimized v26.2-beta.1

Edición independiente para **Minecraft 26.2, Java 25 y Fabric Loader 0.19.5**, preparada localmente en **`26.2dev`** desde `pack/` (26.3-beta.1). No modifica las ediciones 26.3/1.21.11, sus cambios locales, tags o releases.

Importa **`Lumina-Optimized-26.2-beta.1.mrpack`** de Descargas en **una instancia nueva de Modrinth App o Prism Launcher**, usando Java 25 **ARM64 en Apple Silicon**. No lo importes encima de otra edición ni abras tus mundos personales de otra versión; usa un mundo nuevo de prueba.

## Composición y ajustes

- **35 mods principales, 7 bibliotecas externas y PolyTone: 43 JAR**. Fabric Loader se fija aparte. [Versiones exactas](versions.md).
- **4 resource packs activados:** Translations for Sodium 8.19.0, Fresh Animations 1.10.5, Fullbright UB 7.0 y Mandala’s GUI – Dark mode 2.1. Pueden cambiar traducciones, modelos/animaciones y apariencia de iluminación.
- **2 shaders instalados y apagados:** Lumina Event Horizon 1.3.9 y Lumina Lite 1.2.9. Iris **1.11.4** y Sodium **0.9.2** forman la pareja comprobada.
- **Mandala se incluye solo en Modrinth**, por petición expresa: archivo oficial 2.1 sin modificar, publicado hasta 1.21.11, con formato antiguo 64 aceptado explícitamente en `options.txt`. No se presenta como publicación para 26.2. Su recarga se comprobó; falta revisar el aspecto de los menús. Para CurseForge se mantiene la regla de omitirlo; no se genera ZIP CurseForge de 26.2 en esta tarea. [Metadatos y decisión](mandala-review.json).

BBE está activo, con las animaciones de la base conservadas. Shaders y LambDynamicLights empiezan apagados. Para probar un shader, usa **Opciones → Ajustes de vídeo → Shader Packs**; para activar luces, usa la configuración de LambDynamicLights desde Mod Menu.

Se conservan byte por byte 11 de las 12 configuraciones de la base 26.3. El único cambio de beta.1 es **tickCulling=true con safeMode=true** en Entity Culling; todas las demás claves permanecen iguales y se comprueban contra los JAR reales. Para comparar, cambia solo `tickCulling` a `false` desde la configuración de Entity Culling y reinicia; Cull Leaves controla hojas sin superponer More Culling; Gnetum sigue activo con downscale apagado y puede actualizar el HUD con menor frecuencia. **Reduce Resolution on Mac permanece apagado**, como en 26.3. No se cambian automáticamente resolución, distancias, animaciones, calidad ni límite de FPS. Es distinto del ajuste solicitado para 1.21.11.

Se vuelve a verificar y conservar la corrección **ModernFix/Lithium**: ambos sobrescriben `Biome.getTemperature(BlockPos,int)`; se desactiva solo `mixin.perf.remove_biome_temperature_cache` de ModernFix. ServerCore sigue sin cambios automáticos de distancias, mobcaps o comportamiento. `options.txt` solo fija la versión de datos **4903** y los cuatro recursos; la lista de formatos aceptados manualmente contiene únicamente Mandala 2.1.

## Comprobaciones y limitaciones

**Siete grupos estáticos superados:** publicaciones/hashes, integridad recursiva de JAR, dependencias obligatorias externas/integradas, conflictos declarados, configuración real, índice packwiz y exportación. Las 49 referencias y los demás ajustes coinciden con alpha.1. Text Placeholder API 3.1.0-beta.1+26.2 se proporciona dentro de ServerCore sin duplicación; se comprueba su publicación y SHA-512.

**Arranque real aislado de 45 segundos en macOS ARM64/Java 25:** ventana OpenGL, atlas y recarga completados. Los cuatro recursos, incluido Mandala 2.1, se cargan sin rechazo de metadatos. Esto no valida la apariencia de todas las pantallas. Los **166 IDs cargados** coinciden con la resolución estática. Parada deliberada SIGTERM/143; no se entra en un mundo ni se prueba guardado, cierre normal o rendimiento. [Validación](validation.md) · [Registro](runtime.json).

- **EMF registra recreación repetida de modelos** de cofres, shulkers, banners y cobre, y deja de procesar esos modelos. El inicio continúa; el mismo aviso existe en la base 26.3. No se afirma que Fresh Animations/BBE estén visualmente validados. Revisa esos modelos y sus animaciones dentro del mundo.
- BBE 1.3.7 declara Sodium ≥0.9.0; sus notas anuncian 0.9.0–0.9.1, mientras usamos 0.9.2 por la dependencia exacta de Iris. El arranque funciona, pero faltan comprobaciones visuales de BBE. La beta BBE 1.3.8 anuncia una corrección de libros en atriles; esa beta no se instala aquí. Revisa también los atriles.
- C2ME es alpha y se trata como experimental. Exploración, carga de chunks, guardado/reapertura con FastQuit e iluminación no están probados en un mundo. FastQuit conserva su comprobación con Ixeris para evitar servidores integrados simultáneos.
- Gnetum + ImmediatelyFast + Better Mount HUD arrancan juntos sin conflicto declarado; frecuencia del HUD y comportamiento al montar quedan pendientes de juego.
- Hay avisos de integraciones opcionales ausentes y del enlazador OpenGL. Los errores de autenticación/Realms corresponden a la cuenta aislada sin autenticar. No son una prueba de multijugador.
- Ambos shaders encendidos, estabilidad prolongada y Windows/Linux siguen pendientes. **El usuario reportó 117 FPS OpenGL y 147 Vulkan en alpha.1 sin reducir resolución en macOS; son observaciones, no un benchmark controlado ni una medición del nuevo ajuste. No se afirma una ganancia de esta beta.**

## Prueba sencilla en tu Mac

1. Importa el `.mrpack`, arranca y confirma los cuatro recursos activos y revisa los menús de Mandala; shaders y luces apagados.
2. Juega **10–15 minutos**: explora, revisa hojas, criaturas, cofres, shulkers, carteles y atriles. Monta un caballo para comprobar el HUD. Mira y deja de mirar criaturas para revisar animaciones al entrar y salir de la cámara con tick culling.
3. Construye algo, sal al menú, espera el guardado y reabre el mismo mundo; comprueba que lo construido permanece.
4. Opcionalmente activa cada shader Lumina por separado y vuelve a apagarlos. Guarda `logs/latest.log` y cualquier crash report si aparece un fallo.

No hace falta una matriz de benchmarks. Si comparas FPS, usa el mismo mundo, cámara, resolución efectiva, distancias, recursos, backend y ajustes; el arranque no aporta resultados de rendimiento.

## Reconstrucción

```sh
python3 scripts/edition_262.py --build --packwiz .tools/bin/packwiz
python3 scripts/edition_262.py
```

Python 3.11+ y un JDK con `java`, `javac`, `javap`; el juego requiere Java 25. El primer comando verifica archivos oficiales, prepara caché aislada, ejecuta `packwiz refresh`/`packwiz modrinth export` y comprueba que no falta ninguna descarga. No modifica otros packs. El segundo valida sin reconstruir.

La evidencia de alpha.1 está archivada en `docs/editions/26.2/history/alpha.1/`; el paquete anterior permanece en `dist/`. Definición: `packs/26.2/`. Evidencia e inventario: `docs/editions/26.2/`. Artefactos locales: `dist/Lumina-Optimized-26.2-beta.1.mrpack` y `dist/SHA256SUMS-26.2-beta.1`. [Changelog](changelog.md). Sin commit, push o publicación.
