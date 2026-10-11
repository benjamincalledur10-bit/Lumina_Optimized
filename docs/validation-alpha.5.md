# Validación alpha.5 — 2026-10-11

## Archivos y dependencias: completado

- Selección limpia: 42 entradas objetivo representadas; 35 principales, 7 bibliotecas externas, 42 JAR descargables. Placeholder API integrado, ZConfig adicional obligatorio.
- 43 registros completos de publicación contrastados: 26.3 entre game_versions, Fabric entre loaders, versión/ID/nombre/URL/tamaño/SHA-1/SHA-512. Los tres JAR cuya descarga se interrumpía —LambDynamicLights, Fabric Language Kotlin y GeckoLib— se obtuvieron de la instancia local y coinciden con los hashes oficiales. No se suben JAR ni rutas de instancias privadas.
- fabric.mod.json y JAR anidados, CRC ZIP, predicados reales de Fabric, depends/breaks/conflicts/provides y dependencias required/incompatible de Modrinth. Sin dependencias obligatorias pendientes ni conflictos declarados en la selección final.
- 142 apariciones integradas, 117 IDs distintos, 116 seleccionados estáticamente; módulos Loader contados aparte. No se duplican Placeholder, MidnightLib, Greenlight ni MixinExtras externos.
- Nombres/formato de configuraciones contrastados con las clases/serializadores de los JAR; ServerCore YAML parseado con su SnakeYAML integrado. BBE activo, Iris/LambDynamicLights apagados, sin reducción automática de resolución/distancias. More Culling/Cull Leaves sin ajustes de hojas superpuestos.
- packwiz add con IDs/archivos concretos, pin=true, refresh y export. La comprobación rechaza un export incompleto aunque packwiz termine con código 0.
- Inventario exacto, entornos, URLs, tamaños, SHA-1/SHA-512 y bytes de overrides del .mrpack comprobados. Índices packwiz SHA-256 y checksum del artefacto verificados. Sin JAR, shader packs, resource packs ni options.txt dentro del ZIP.
- 7 pruebas estáticas de composición y resolución pasaron. Checksums históricos alpha.1–alpha.4 conservados; archivos presentes sin cambios. No se modificó Git history, tags ni releases.

Artefacto: `dist/Lumina-Optimized-0.1.0-alpha.5.mrpack`. SHA-256:

```text
5b003ae8ea2e318184a63af9a08a99336f920dc6f2626ea653af9f7673bae6d0
```

## Ejecución real: parcial

Java Zulu 25.0.4.1 ARM64, Minecraft 26.3 y Loader 0.19.5, instancia temporal aislada, token ficticio. Fabric aceptó el SAT real y enumeró **162 IDs**. Se creó la ventana **SDL cocoa**, se cargaron recursos y se retiró el overlay de recarga. La limitación previa de falta de pantalla **no ocurrió en esta sesión**.

El harness detuvo el cliente a los 45 segundos: exit 143 por SIGTERM, **no un crash espontáneo**. Se verificó la configuración generada: BBE activo, shaders false, luces Off, More Culling DEFAULT, reducción de resolución Mac false. No se observaron errores fatales de mixins antes de detenerlo.

EMF registró su guarda de modelos creados más de 64 veces. Su código conserva el ModelPart original, pero la compatibilidad con modelos personalizados de BBE es limitada y debe revisarse visualmente. C2ME no encontró la biblioteca matemática nativa macOS ARM64 y desactivó esa aceleración. Los errores 401/Realms corresponden al token ficticio, no prueban un fallo de una cuenta real. Se registran también avisos de clases opcionales y refmaps.

**Pendiente:** importar en launcher, entrar a un mundo, explorar, revisar HUD con Gnetum/ImmediatelyFast/Better Mount HUD, guardar/reabrir con FastQuit/C2ME/Ixeris, cerrar normalmente y jugar 10–15 minutos. No se dispuso de control interactivo del cliente para completar esas acciones; las fuentes locales de launch/assets estaban disponibles. No se midió FPS ni se confirmó estabilidad prolongada o soporte efectivo Windows/Linux.

[Prueba sencilla en Mac](benchmarks.md) · [Evidencia del arranque](research/runtime-alpha.5.json) · [Inventario estático](validation.json) · [Publicaciones](research/publications-alpha.5.json) · [Interacciones](configuration-alpha.5.md).
