# Protocolo reproducible (pendiente de ejecutar)

Este protocolo conserva la referencia de alpha.1. Alpha.2 añade los perfiles
aislados y acumulativos de [alpha.2.md](alpha.2.md), sin cambiar los ajustes de
comparación. No existen mediciones previas: [estado histórico](history/alpha.1/measurements.json).

## Instancias

Crear cuatro instancias nuevas, sin reutilizar cachés/configs de otros packs:

| Nombre | Contenido |
| --- | --- |
| Vanilla | Minecraft 26.3 |
| Fabric | Minecraft 26.3 + Loader 0.19.5, sin mods |
| Fabric + Sodium | Fabric + el Sodium exacto de `pack/mods/sodium.pw.toml` |
| Lumina | Exportación Core 0.1.0-alpha.1 |

Shaders es una extensión separada: comparar Core con Iris sin shader, después
con un shader cuyo ZIP, hash, versión y preset se registren. No mezclar resultados
con/sin shaders. No añadir mods de medición solamente a una instancia.

## Ajustes y entorno

Primero guardar los defaults generados por cada instancia; no distribuir esos
archivos como overrides. Preparar después un perfil de benchmark separado con
los mismos ajustes efectivos en las cuatro instancias. Si Sodium cambia nombres
o defaults, documentar la equivalencia y comprobarla visualmente.

- Resolución efectiva 1920x1080; registrar escalado Retina/DPI y modo de ventana.
- Gráficos Fancy, render distance 12, simulation distance 8, FOV 70, nubes Fancy,
  partículas All, mipmap 4, entity distance 100%, iluminación suave activada
  cuando exista la opción. Registrar también biome blend y todas las opciones
  restantes; si una opción desapareció en 26.3, documentarlo en lugar de inventarla.
- Sin shaders ni resource packs externos. VSync desactivado, FPS ilimitados.
  Repetir sesión sostenida con límite de 60 FPS en todas las instancias.
- Java 25 con proveedor/build idénticos por equipo, heap máximo 4 GiB, mismos
  argumentos y recolector efectivo. Registrar arquitectura, SO, CPU, GPU,
  controlador, backend gráfico, RAM y launcher. No cambiar el backend entre A/B;
  si no es posible, declarar ese factor como limitación.
- Equipo conectado a corriente, modo energético fijo, sin grabación de pantalla
  ni aplicaciones variables en segundo plano. Registrar temperatura y clocks si
  están disponibles. Mantener el foco de la ventana.

## Mundo y escenarios

Preparar un mundo maestro con seed **2603001**, tipo normal y dificultad Normal.
Guardar un archivo del mundo y su SHA-256: usar una copia idéntica antes de cada
ejecución, pues la seed por sí sola no fija el estado. Fijar mediodía y tiempo
despejado, desactivar avance del tiempo/clima y aparición natural de mobs en el
mundo de prueba. Mantener iguales los gamerules y registrar sus valores efectivos.

Antes de medir, guardar `scenarios.json` con coordenadas, orientación, entidades,
duración y rutas exactas. El mundo y este archivo aún están pendientes; no
presentar resultados reproducibles hasta disponer de ambos.

1. Cámara fija en terreno pregenerado: captura de 5 minutos tras estabilizar chunks.
2. Ruta pregenerada: movimiento automatizado con cámara/velocidad idénticas durante
   5 minutos; mide lectura desde disco y construcción de geometría.
3. Ruta sin generar: desde un límite conocido del mundo maestro, repetir una ruta
   automatizada de 5 minutos en una copia nueva; mide generación y carga.
4. Escena fija de 200 entidades sin IA, 200 cofres, mapas y texto; guardar su
   distribución. Añadir otra escena con IA/redstone determinista para medir ticks.
5. Sesión sostenida de 30 minutos y recorrido con cambios de dimensión; restaurar
   el mundo y repetir la misma secuencia de acciones.

El instrumento de rutas debe ser el mismo en todas las instancias y funcionar
en vanilla; validar que no cambie simulación o carga. Evitar recorridos manuales
para las comparaciones publicadas.

## Captura y análisis

Cinco ejecuciones independientes por escenario/instancia, proceso nuevo,
3 minutos de calentamiento y 5 minutos de captura (30 minutos para estabilidad).
Alternar el orden A/B/C/D entre repeticiones; no seleccionar solo el mejor ensayo.
Separar carga fría y caliente de archivos y registrar la política de caché del SO.

Validar primero un capturador por fotograma compatible con 26.3/backend en cada
SO, su sobrecarga y si mide CPU o presentación en GPU. No usar lecturas puntuales
de F3. Comparar captura activada/desactivada antes de usarla como evidencia.

Guardar CSV de tiempos por fotograma y metadatos de cada ensayo. Calcular:

- FPS promedio = número de fotogramas / segundos de captura.
- Frametime p50, p95, p99 y p99.9.
- 1% low = 1000 / media del 1% de fotogramas más lentos, en ms.
- Fotogramas >33.3 ms y >50 ms por minuto.
- Heap utilizado, memoria residente del proceso (RSS), pausas de GC y memoria GPU
  si es accesible. No confundir heap máximo asignado con memoria utilizada.
- Tiempo hasta chunk disponible en servidor y hasta visible en cliente, por
  separado; chunks completados/s sobre el mismo conjunto. La instrumentación de
  eventos es pendiente: no inferir generación de chunks únicamente de FPS.
- MSPT p50/p95/p99 del servidor integrado para las pruebas de simulación.

Los perfiles JVM y de ticks se recogen en ensayos diagnósticos separados para
evitar contaminar los FPS principales. Registrar el instrumento y su versión.

Publicar datos crudos, mediana y dispersión entre los cinco ensayos; calcular
cambios respecto a Vanilla y Fabric + Sodium dentro del mismo equipo. Un cambio
dentro de la variabilidad es no concluyente. No sumar porcentajes de mods.

## Matriz y aceptación

Pendientes: macOS ARM64, Windows x64 y Linux x64; añadir macOS Intel si se declara
soporte para esa arquitectura. Resultados de equipos distintos no se agrupan
como una comparación directa. Verificar GPU/controlador y backend en cada uno.

Antes de llamar funcional a la alpha: importar Core y Shaders en instancias
limpias, arrancar, crear/abrir/guardar/reabrir mundo, cargar chunks, cambiar
dimensiones, conectar a servidor vanilla 26.3 y comprobar HUD, mapas, cofres,
partículas, transparencias y sombras. Revisar logs y crashes. Probar Iris tanto
sin shader como con un shader fijado, incluyendo recarga.

Para cada prueba marcar PASS/FAIL/PENDIENTE y adjuntar evidencia. Un `.mrpack`
validado estáticamente no equivale a un modpack arrancado ni a una mejora medida.
