# Prueba sencilla alpha.5 en Mac: 10–15 minutos

Importa `dist/Lumina-Optimized-0.1.0-alpha.5.mrpack` en una instancia nueva y selecciona Java 25 ARM64 en Apple Silicon. Las importaciones, mundos y FPS aún no están comprobados aquí. No necesitas una matriz de benchmarks.

1. Comprueba que inicia, BBE está activo, Iris tiene shaders apagados y LambDynamicLights está Off. No instales recursos ni shaders para esta primera prueba.
2. Usa un mundo de prueba nuevo o una copia. Mantén tu resolución, distancia de renderizado/simulación, calidad gráfica, animaciones y límite de FPS/VSync habituales; anótalos si quieres comparar con alpha.4. C2ME y Chunky no deben cambiar tus distancias ni pregenerar chunks automáticamente.
3. Juega y explora durante unos 5 minutos. Revisa tirones al cargar terreno y hojas vistas desde dentro y fuera del bosque. Si usas Chunky manualmente, no mezcles esa sesión con una comparación de exploración sin pregeneración.
4. Dedica unos minutos a cofres dobles, shulkers, banners y macetas decoradas. BBE/EMF tienen una limitación de modelos personalizados; revisa geometría y animaciones aunque esta base no lleve recursos externos.
5. Monta un caballo y revisa salud, hambre y barra de salto/experiencia con Better Mount HUD. Gnetum puede refrescar el HUD más lentamente. Si ves retrasos o elementos congelados, desactiva Gnetum en sus opciones y repite esa acción; conserva ImmediatelyFast con sus valores predeterminados.
6. Explora otra zona, coloca bloques y objetos en un cofre, guarda y vuelve al menú. Espera la notificación de guardado de FastQuit, reabre y confirma posición, bloques e inventario. Repite una salida/reentrada mientras guarda para comprobar la protección de FastQuit; no cierres a la fuerza.
7. Cierra normalmente Minecraft y vuelve a abrir ese mundo. Revisa `logs/latest.log` y `crash-reports/` si aparecen errores. Anota fluidez, errores visuales y el FPS que observes, junto con modelo del Mac y ajustes.

Para probar luces dinámicas después: Mods → LambDynamicLights → configuración → modo Fancy/Fast. Hazlo después de la referencia Off. Los shaders requieren instalar un pack aparte y son otra prueba visual, no están incluidos.

Si falla: guarda el log y el paso exacto. Para aislar guardado/carga prueba quitando temporalmente C2ME o FastQuit en una copia de la instancia; para HUD desactiva Gnetum. No hace falta mantener paquetes adicionales. C2ME y Remove Reloading Screen se distribuyen en canal alpha.

El objetivo de acercarse a 200 FPS no está demostrado. Si comparas con alpha.4, repite el mismo recorrido y ajustes, sin rebajar resolución, distancias o calidad. Las mediciones históricas permanecen en sus archivos previos; no se reinterpretan como mediciones de alpha.5.
