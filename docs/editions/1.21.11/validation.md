# Validación — v1.21.11-beta.1

Evidencia del **12 de octubre de 2026**. Se promociona la composición final de alpha.1 a beta.1 por solicitud del usuario, sin modificar los archivos descargados ni las configuraciones.

## Archivos, dependencias y exportación

`python3 scripts/edition_12111.py --build --packwiz .tools/bin/packwiz` completa siete grupos. Los resultados exactos, hashes e inventario están en [validation.json](validation.json).

| Comprobación | Alcance |
|---|---|
| Publicaciones y hashes oficiales | 50 versiones/IDs, etiquetas para 1.21.11/cargador, URLs, tamaños, SHA-1 y SHA-512 de Modrinth; pins fijos. Loader coincide con Fabric Maven. |
| Integridad recursiva | CRC, metadatos `fabric.mod.json` y bibliotecas integradas; JAR originales intactos. |
| Dependencias | Predicados de Fabric para Java 21 y Loader 0.19.5; requisitos de catálogo, pareja exacta Sodium/Iris y bibliotecas integradas. |
| Conflictos declarados | Ningún requisito, `breaks` o `conflicts` incompatible en la selección efectiva. No demuestra ausencia de conflictos de juego. |
| Configuraciones | Claves de versiones reales mediante `javap`, JSON/TOML y YAML con el SnakeYAML de ServerCore. BBE activo, tick culling y modo seguro activos, shaders/luces apagados, hojas sin superposición, ModernFix/Lithium corregido, reducción de resolución de macOS activada por petición del usuario, sin cambios de distancias/comportamiento. Gnetum ausente de selección, pins y configuración. |
| Índice packwiz | Hash del índice y de todas sus entradas. |
| Exportación | CRC, rutas seguras, identidad/plataforma, 50 referencias con URL/hash/tamaño exactos, 12 overrides idénticos a la definición; sin binarios en overrides. |

La selección tiene **36 principales, 7 bibliotecas y PolyTone**, 44 JAR raíz; **119 IDs integrados activos**, incluido MixinExtras de Loader, y 151 apariciones de candidatos integrados contando duplicados/inactivos. Con Minecraft, Java y Loader son 166 IDs. Estos IDs no equivalen a 166 descargas independientes.

Text Placeholder API 2.8.2 está integrado en Mod Menu; su SHA-512 coincide con `qxjzQ9xY` y prevalece sobre 2.8.1 de ServerCore. No se duplica. C2ME descarta su módulo opcional `c2me-opts-natives-math`, que exige Java 22. El resolvedor estático se contrasta con el arranque real; no reemplaza el SAT de Fabric.

Language Reload 1.7.7+1.21.11 tiene bytecode Java 21 y sus módulos Fabric API requeridos están incluidos. ScalableLux 0.1.6+fabric.c25518a está publicado para Fabric/1.21.11, tiene bytecode Java 17 compatible, proporciona `starlight` y declara incompatibilidad con Phosphor, ausente. Conserva ajustes predeterminados; El usuario reportó la prueba breve sin problemas; no hay resultados individuales de iluminación o guardado para ScalableLux/C2ME.

## Arranque y evidencia

El nuevo arranque con la reducción de resolución de macOS activada completó inicialización y recarga de recursos; Fabric cargó 166 IDs coincidentes con la selección estática y Gnetum está ausente tanto de los JAR como de las configuraciones. El arranque aislado sin Gnetum se registra en [runtime.json](runtime.json) y [startup.log](startup.log). Se usa Java 21.0.12.1 ARM64, Minecraft 1.21.11 y Loader 0.19.5 en Apple M4/macOS, sin cuenta del usuario ni mundos personales. Límite de 45 segundos; SIGTERM deliberado/código 143. No equivale a una prueba de juego o de cierre normal.

Se comprueba inicialización de ventana OpenGL, recarga de los cuatro recursos, atlas/EMF/ETF, BBE activo, shaders y luces dinámicas apagados, tick culling/modo seguro activos, ModernFix/Lithium corregido, `reduce_resolution_on_mac=true` persistente y ausencia de Gnetum en la lista cargada. El inventario efectivo debe coincidir con la validación estática.

Los logs y validaciones previos con Gnetum ON/OFF están en [history/with-gnetum-additions/](history/with-gnetum-additions/); el primer arranque está en [history/initial-alpha1/](history/initial-alpha1/). No se reutiliza su éxito como evidencia del paquete nuevo. Los logs sustituyen rutas personales por `${HOME}`/`${REPO}`.

## Limitaciones conservadas

- Mandala 2.1 se publica para 1.21.11 pero declara formato 64, anterior al 75 actual; se acepta explícitamente el ZIP original, apariencia pendiente.
- More Culling tiene un mixin opcional para una clase antigua de Sodium ausente; el inicio continúa. Su culling de bloques está desactivado. BBE permite Sodium 0.8.14 en metadatos, aunque las notas de BBE anuncian hasta 0.8.13-beta.2; modelos BBE/EMF/Fresh Animations requieren revisión.
- ModernFix aplica nuestra corrección de temperatura y desactiva otras tres opciones por compatibilidad con C2ME. FastQuit detecta Ixeris y evita múltiples servidores simultáneos; el reporte de juego no incluye un resultado individual de guardado/reapertura.
- PolyTone recomienda Nautilus Studio, no obligatorio. Hay avisos de refmaps e integraciones opcionales, mensajes del enlazador OpenGL y errores de autenticación/servicios externos con la cuenta de prueba; el log conserva su contexto.

## Prueba de juego reportada y pruebas pendientes

El usuario reportó haber completado la prueba breve recomendada sin problemas en su Mac. Se registra como **PASS reportado por el usuario**, separado del arranque ejecutado por el agente. No se aportaron logs, duración exacta ni resultados individuales: [user-play.json](user-play.json).

Pendientes de comprobación independiente o específica: cambio de idioma, luz en bordes de chunks con ScalableLux/C2ME, guardado/reapertura con FastQuit, modelos/animaciones, HUD montado, ambos shaders por separado, sesiones largas, Windows/Linux y una comparación controlada de rendimiento. El ajuste de reducción de resolución es explícito y reversible; su efecto no se presenta como mejora a igual resolución.

El usuario probó la composición final de alpha.1; la beta solo cambia su identidad y documentación. La equivalencia de ambas exportaciones se comprueba comparando referencias y overrides. No se atribuyen ganancias a retirar Gnetum y no se prometen 331 FPS. Para comparar FO/Lumina, igualar mundo, cámara, recursos, resolución efectiva y modo de ventana; usar el mismo valor de reducción de resolución en Mac en ambos y comprobar la resolución efectiva; desactivarlo en ambos para comparar a resolución nativa.

La definición `pack/` de 26.3 y sus dos artefactos distribuidos se contrastan con la instantánea SHA-256 inicial. El historial, tags, releases y cambios locales anteriores se conservan.

La comparación directa con el principal inmediatamente anterior (ya sin Gnetum) confirma que solo cambia `overrides/config/sodium-extra-options.json`: `reduce_resolution_on_mac` pasa de false a true. Las 50 URLs/hashes y todos los demás overrides son idénticos. La copia de Descargas coincide byte por byte.

## Ajuste de macOS y observación del usuario

Se inspeccionó `MacReducedResolution` del JAR oficial Sodium Extra 0.9.4 mediante `javap`: `isEnabled()` comprueba el sistema operativo además del booleano y las rutas de reducción distinguen el backend OpenGL. El nuevo valor se guarda en el archivo real serializado con `LOWER_CASE_WITH_UNDERSCORES`. No se impone una resolución fija ni se cambia otra plataforma. La evidencia anterior sin reducción está archivada en [history/without-gnetum-full-resolution/](history/without-gnetum-full-resolution/).

La captura del usuario del 12 de octubre a las 12:32 muestra **311 FPS, p50=324, p98=189, p99.5=159**, render 16/simulación 5 y display **1920×1206**. La captura anterior mostraba display 2940×1846; también cambia ligeramente la cámara. Es una observación de juego aportada por el usuario, no una prueba controlada, un resultado garantizado ni evidencia de que desvincular el launcher aumente FPS.

## Promoción a beta.1

La comprobación de arranque registrada en `runtime.json` corresponde al SHA-256 de la alpha final, conservado en ese registro. No se presenta como otra ejecución del ZIP beta: sus 50 referencias y 12 overrides se comparan con la alpha y deben ser idénticos; solo cambian la identidad de versión y su resumen descriptivo en el manifiesto de exportación. La composición de la beta se validó de nuevo con las siete comprobaciones estáticas.

La captura más reciente del usuario muestra 381 FPS, p50=402, p98=181 y p99.5=160 a 1470×923 (la mitad de 2940×1846 en cada eje). No es una medición de ganancia a igual resolución, estabilidad a largo plazo ni rendimiento garantizado.

La variante CurseForge completó el inicio aislado de 45 segundos, pero **Mandala 2.6 fue rechazado por metadatos incompletos (`min_format`/`max_format`)**. Se conserva el original; su aplicación/aspecto y la importación en CurseForge App siguen pendientes. El `.mrpack` mantiene Mandala 2.1. [Evidencia](runtime-curseforge.json).
