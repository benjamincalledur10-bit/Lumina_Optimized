# Validación v26.3-beta.1 — 2026-10-11

## Archivos y dependencias

Completado: selección heredada de alpha.5 con sus versiones y configuraciones conservadas, 1 nuevo soporte PolyTone y 4 resource packs. Pins packwiz, IDs de Modrinth, archivos, URLs, tamaños, SHA-1/SHA-512, ZIP CRC, metadatos internos, dependencias y conflictos declarados verificados. Archivos locales usados como caché solo tras coincidir los hashes oficiales; no se suben JAR/ZIP al repositorio.

35 mods principales + 7 bibliotecas externas + PolyTone = 43 JAR. Cuatro resource packs y dos shader packs = 49 archivos descargables. 145 apariciones de módulos integrados, 119 IDs distintos, 118 seleccionados estáticamente; plataforma/Loader contados aparte. El arranque real enumera 165 IDs. CodecUI, exp4j y nexp se proporcionan dentro de PolyTone; no copias externas.

Las dependencias de PolyTone y CodecUI se satisfacen con Loader 0.19.5, Fabric API 0.162.0+26.3 y Sodium 0.9.2. No conflicto obligatorio declarado. `nautilus_studio` es una recomendación opcional, no instalado. Fresh Animations necesita EMF/ETF según su descripción; ya presentes. Translations requiere Sodium.

Excepción explícita: **Mandala 2.1 no publicado para 26.3**, formato interno 64. Se conserva el ZIP original y se activa por petición del usuario, aceptando ese formato en `incompatibleResourcePacks`; su compatibilidad visual sigue pendiente. No se modifican metadatos del autor para aparentar compatibilidad. Los otros tres sí publican 26.3.

Pasaron 8 pruebas estáticas, incluida la selección de los dos shaders solicitados. Índice packwiz SHA-256, hashes exportados, URLs, entornos client-only de recursos, inventario completo y bytes de overrides comprobados. `options.txt` solo contiene versión de datos y selección/aceptación de packs; conserva los ajustes gráficos predeterminados del juego. Lumina Event Horizon 1.3.9 y Lumina Lite 1.2.9 fijados en `shaderpacks/`, descargados desde Modrinth; hashes oficiales, tamaño, CRC, rutas, raíz de Iris y licencias verificados. Ambos publicados para Iris/26.3; sin nuevos JAR ni dependencias externas. BBE activo, Iris apagado y luces Off. Checksums históricos alpha.1–alpha.5 conservados y archivos locales intactos.

Artefacto: `dist/Lumina-Optimized-26.3-beta.1.mrpack` (12829 bytes).
SHA-256: `f2af6114bf8fb0ec649bc44e539b8a4c1c72b2618ce2edd560fd0dfce079b0a4`.

## Ejecución real anterior a la revisión de shaders

El siguiente arranque corresponde al paquete anterior, sin los dos shaders añadidos. No se ejecutó una nueva sesión ni se compilaron shaders en Minecraft para esta revisión.

Java 25.0.4.1 ARM64, Minecraft 26.3/Loader 0.19.5 en instancia temporal aislada con token ficticio. Ventana SDL cocoa creada. La recarga enumeró los **cuatro recursos activos**, PolyTone cargó sus entradas y el overlay se retiró. No fallo fatal de mixins ni fallo de recarga observado antes de la parada. Se detuvo mediante SIGTERM a los 45 segundos, exit 143; no prueba de cierre normal.

**Interacción detectada:** BadOptimizations desactiva automáticamente sus cachés de lightmap y color de cielo al encontrar PolyTone. Se mantiene esa protección incorporada; las configuraciones distribuidas de alpha.5 no cambian. No se mide ni se atribuye ganancia de rendimiento a esta combinación.

Persisten avisos EMF/BBE de modelos recreados y la desactivación de matemáticas nativas C2ME en macOS ARM64. Errores de autenticación/Realms se deben al token ficticio. Warnings de enlazado de shaders no impidieron finalizar la recarga. [Evidencia](research/runtime-26.3-beta.1.json).

## Juego y rendimiento

El usuario informó fluidez favorable en **alpha.5** y aportó capturas en M4 con lecturas 149.22 FO y 197.49 Lumina, ambos Prefer Vulkan según su reporte, resolución 2940×1846, misma semilla en mundos distintos. No son promedios controlados ni resultados de beta.1 con recursos. [Registro](research/user-play-alpha.5.json).

**Pendiente en beta.1:** importación en launcher, mundo, exploración, animaciones/modelos, Fullbright y GUI, Prefer Vulkan del usuario, HUD a caballo, guardado/reapertura FastQuit/C2ME, cierre normal, estabilidad 10–15 minutos y FPS. Windows/Linux no ejecutados. [Prueba sencilla en Mac](benchmarks.md).

La comparación contra el `.mrpack` anterior conserva exactamente sus 47 referencias y todos los overrides. Solo se añaden las dos referencias `shaderpacks/`. [Comparación de revisión](research/shader-revision-26.3-beta.1.json).
