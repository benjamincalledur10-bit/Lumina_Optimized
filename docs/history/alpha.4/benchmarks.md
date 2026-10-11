# Revisión jugando 10–15 minutos

Esta revisión busca fluidez percibida, errores y capacidad de guardar; **no es un benchmark ni demuestra mejoras de FPS**. El protocolo anterior y las mediciones informadas por el usuario se conservan en `history/`.

1. Importar Core alpha.4 en una instancia nueva y seleccionar Java 25. Mantener exactamente la resolución, distancias, animaciones y calidad que usabas en alpha.3. No copiar configs de otra instancia. Comprobar BBE activo. Better Biome Blend comienza en 5×5; si alpha.3 usaba otra mezcla, igualar ese radio. No activar reducción de resolución en macOS, ajustes dinámicos de distancias ni opciones que oculten errores.
2. Crear un mundo de prueba nuevo. Jugar 10–15 minutos: caminar/correr hacia chunks nuevos, colocar y romper bloques luminosos, abrir cofres, revisar partículas, césped/nieve, agua y zonas de sombra. Recoger experiencia y probar Mending si está disponible.
3. Revisar hotbar, corazones, chat, inventario y mapas; alternar F1 y redimensionar la ventana. Gnetum puede actualizar el HUD menos frecuentemente: anotar si la respuesta molesta, aunque el mundo parezca fluido.
4. Guardar, salir al menú, cerrar el juego y reabrir ese mundo. Comprobar chunks, iluminación, bloques y entidades. Guardar `latest.log` y cualquier crash report, indicando paquete exacto, SO y Java.
5. Para Shaders, importar otra instancia. Comprobar primero que arranca **sin shaders**; después, si quieres, activar un shader y anotar su nombre/versión/preset. Comparar con los mismos ajustes; no mezclar la revisión sin shader y con shader.

Si hay problemas, repetir en `core-conservative` (sin C2ME/ScalableLux/Gnetum). Para un problema solo del HUD, usar `gnetum-control` (ImmediatelyFast permanece). Para comparar con lo anterior, usar `alpha3-reference`. Mantener mundos de prueba separados: no generar regiones con varios perfiles y luego atribuir el resultado a uno.

More Culling aplica ahora el TOML conservador que antes no leía del JSON. Esa corrección debe anotarse al comparar con alpha.3; no atribuir cualquier diferencia solo a los siete mods nuevos.

Basta anotar: paquete, equipo/Java, entró al mundo sí/no, exploró sí/no, guardó/reabrió sí/no, fluidez percibida y errores del log. No hacen falta FPS grabados ni herramientas nuevas para esta revisión. Una sesión buena de 15 minutos no certifica estabilidad prolongada o compatibilidad en los otros sistemas operativos.

## Combinaciones que debes revisar

Probar C2ME/ScalableLux/Fast Noise/Fast Surface/ZConfig generando y reabriendo chunks, incluidas otras dimensiones. Probar Krypton/C2ME entrando y saliendo de un servidor de prueba además del mundo local. Verificar que ServerCore no ajusta distancias, mobcaps ni comportamiento. Las versiones ya están incluidas y pasaron resolución/inicialización anterior a SDL; esas comprobaciones no sustituyen jugar ni generar/guardar chunks. ServerCore tiene los cambios dinámicos y de comportamiento apagados. Mantener apagados los shaders en la primera revisión.
