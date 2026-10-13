# Validación — v26.2-alpha.1

Evidencia del **12 de octubre de 2026**. Resultado estático en [validation.json](validation.json); publicaciones y metadatos completos en [selection.json](selection.json), candidatos oficiales/Fabric en [publication-audit.json](publication-audit.json) y plataforma Mojang en [minecraft-publication.json](minecraft-publication.json).

## Archivos, configuración y exportación

| Comprobación | Resultado y alcance |
|---|---|
| Publicación/hashes | PASS: 49 archivos oficiales; 48 publicados para 26.2/cargador y Mandala 2.1 como excepción expresa, solo Modrinth; IDs/proyectos, URL, tamaño, SHA-1/SHA-512 verificados contra bytes. Sodium 0.9.2 coincide con el ID obligatorio de Iris 1.11.4. Loader estable 0.19.5 para 26.2 y hash Maven comprobados. |
| Integridad recursiva | PASS: CRC de JAR y ZIP, `fabric.mod.json`, jars anidados, hashes de cada contenedor. Text Placeholder integrado coincide con publicación oficial. |
| Dependencias | PASS: predicados Fabric con Minecraft 26.2/Java 25/Loader 0.19.5, dependencias obligatorias de catálogo y alias/proveedores integrados. No se añaden duplicados. |
| Conflictos declarados | PASS: ningún `breaks`/`conflicts` activado en la selección efectiva. Esto no garantiza comportamiento visual o estabilidad en juego. |
| Configuraciones | PASS: JSON/TOML, nombres reales mediante `javap`, default TOML de LambDynamicLights y SnakeYAML/esquema real ServerCore. 12 configs de mods idénticos a 26.3; BBE activo, hojas sin superposición, shaders/luces apagados, Gnetum ON/downscale OFF, resolución Mac sin reducción. ModernFix/Lithium sobrescriben la misma firma y se mantiene su corrección. |
| Recursos | PASS: tres recursos publicados para 26.2 y `min_format`/`max_format` internos incluyen **88.0**, formato extraído del client oficial. Fullbright declara `pack_format=97` pero rango 15–1000 y se acepta sin forzar incompatibilidad. Mandala 2.1 conserva su ZIP oficial con formato 64; se acepta solo ese archivo antiguo por petición expresa. No está publicado para 26.2. La recarga real confirma aceptación, sin validar toda su apariencia. |
| Índice/exportación | PASS: índices/hashes packwiz, CRC/rutas seguras, identidad y plataforma, 49 descargas exactas con URL/hash/tamaño oficiales, client requerido, 13 overrides idénticos a la definición; sin JAR/ZIP incrustados en overrides. |
| Preservación | PASS: los 393 archivos preexistentes capturados, incluidas definiciones, documentación/cambios locales previos y artefactos de 26.3/1.21.11, mantienen SHA-256. Solo se añaden archivos de la edición nueva y se crea la rama local 26.2dev. |

Conteo: **35 principales + 7 bibliotecas externas + PolyTone = 43 JAR**; **4 recursos + 2 shaders = 49 descargas**. Fabric resuelve 120 módulos integrados activos (MixinExtras de Loader incluido) y 147 candidatos contando duplicados/inactivos. Los 166 IDs reales incluyen Minecraft, Java y Loader. Estos IDs no son mods adicionales descargados.

La lista de archivos del endpoint de versiones puede incluir un UUID de archivo que el endpoint individual omite; se comparan todos los campos de descarga salvo ese UUID opcional, conservando igualdad estricta de URL, filename, hashes, tamaño, tipo y primary. Los IDs de proyecto y versión sí se fijan y verifican.

## Arranque ejecutado

[Runtime](runtime.json) · [Log saneado](startup.log). Se ejecutó el cliente oficial verificado de Minecraft **26.2**, Loader **0.19.5**, Java **Zulu 25.0.4.1 ARM64**, en Apple M4/macOS. Carpeta aislada en `.build/runtime-26.2-alpha1-mandala`, cuenta de prueba sin autenticar y sin mundos del usuario. Ventana OpenGL, atlas y recarga completados durante **45 segundos**; parada SIGTERM deliberada (143). Los 166 IDs/versiones coinciden exactamente con el resolvedor estático.

Se cargaron los cuatro recursos seleccionados, incluido Mandala 2.1, y no hay rechazos de metadatos. Polytone carga nueve entradas de configuración; eso no sustituye una inspección visual de Fullbright en un mundo. Mandala 2.1 se instala y su recarga termina sin error de metadatos; todavía no se inspeccionaron todas las pantallas. Sus metadatos originales y la falta de publicaciones están en [mandala-review.json](mandala-review.json).

**Avisos reales:** EMF informa recreación excesiva de 12 modelos (cofres, shulkers, banners y cobre), y deja de procesar esos modelos. El inicio continúa; el mismo patrón existe en el log de la base 26.3. No se oculta ni se presenta como validación visual completa. Hay warnings de mixins opcionales para mods ausentes y del enlazador OpenGL. Los errores HTTP401/Realms son consecuencia de la cuenta aislada sin autenticar.

## Pruebas pendientes

- Importación del `.mrpack` en Modrinth App/Prism Launcher y juego 10–15 minutos en un mundo nuevo.
- Exploración/chunks con C2ME/Fast Noise, iluminación y guardado/reapertura con FastQuit/Ixeris.
- Apariencia de los menús de Mandala en 26.2. Modelos/animaciones BBE/EMF/Fresh Animations, cofres/shulkers/banners/atriles y HUD al montar con Gnetum/ImmediatelyFast.
- Los dos shaders activos por separado y luces dinámicas al activarlas.
- Sesiones largas, Windows/Linux y rendimiento. **No se midieron FPS ni se afirma una ganancia.**

Se entrega solo el `.mrpack` solicitado. No hay exportación CurseForge de esta edición ni publicación, commit o push.
