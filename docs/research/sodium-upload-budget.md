# Hipótesis propia: presupuesto mínimo de uploads en Sodium

Estado: **propuesta experimental, sin compilar ni medir en Minecraft**. No se
incluye un Sodium modificado en los `.mrpack`. El parche es concreto y aplicable
al código fijado; su flag solo funcionará después de compilar e instalar ese fork.

## Código revisado

Sodium **0.9.2 para 26.3**, tag `mc26.3-0.9.2`, commit
`03198cb36ab831c99694403d18e4cf4a1726df72`. No se usa `dev` para inferir la alpha.

- [`ChunkBuilder.java`](https://github.com/CaffeineMC/sodium/blob/03198cb36ab831c99694403d18e4cf4a1726df72/common/src/main/java/net/caffeinemc/mods/sodium/client/render/chunk/compile/executor/ChunkBuilder.java): workers con contexto propio, prioridad reducida, elección automática de hilos, cola prioritaria y ejecución de tareas robadas por el hilo principal al esperar trabajo urgente.
- [`RenderSectionManager.java`](https://github.com/CaffeineMC/sodium/blob/03198cb36ab831c99694403d18e4cf4a1726df72/common/src/main/java/net/caffeinemc/mods/sodium/client/render/chunk/RenderSectionManager.java): `updateChunks` reparte trabajos en bloqueantes del fotograma actual, del siguiente y diferidos. Limita envíos por duración estimada de workers, duración estimada de upload y capacidad del staging buffer.
- `collectChunkBuildResults` recoge los resultados disponibles; `processChunkBuildResults` aplica las salidas y entrega geometría a `regions.uploadResults` en el hilo de render. La generación de chunks del servidor no ocurre en estos workers.

Ya existen presupuestos de tiempo, estimadores, prioridad por cercanía/visibilidad,
workers configurables, diferimiento, culling asíncrono y ordenación de transparencias.
Crear otro pool o simplemente proponer un presupuesto adaptativo duplicaría parte
del trabajo existente. También revisamos la petición histórica
[Sodium #691](https://github.com/CaffeineMC/sodium/issues/691); no la usamos como
prueba de un fallo actual, pues el código moderno ya tiene presupuestos.

## Problema identificable y alcance

En `RenderSectionManager`, la fórmula actual es:

```java
max(averageFrameDuration * 0.3f, MIN_UPLOAD_DURATION_BUDGET)
```

La constante es **10_000_000 ns (10 ms)**, aunque su comentario dice `2ms`.
La discrepancia es comprobable; no demuestra que 10 ms sea un error ni que
corregir el comentario deba cambiar el comportamiento.

Con un fotograma de referencia de 16.67 ms, el suelo eleva el presupuesto estimado
de 5 ms a 10 ms. Hipótesis: durante exploración a FPS altos, ese suelo permite
enviar suficiente geometría diferida para contribuir a ráfagas de procesamiento
y upload que empeoren p99. Un suelo de 2 ms podría distribuir mejor esos envíos
entre fotogramas, a costa de aumentar la latencia hasta ver chunks.

**No es un diagnóstico medido de tirones.** Se descarta la hipótesis si las trazas
no relacionan los fotogramas lentos con este trabajo o si el control no alcanza
ese suelo. El presupuesto limita trabajo estimado que se envía, no impone un
límite duro al tiempo de GPU ni fracciona uploads ya completados.

## Cambio concreto y activación

[Parche](../../experiments/sodium-upload-budget.patch): cambiar solamente el
valor mínimo mediante `Boolean.getBoolean("lumina.experimentalUploadBudget")`.

- Control: flag ausente o `-Dlumina.experimentalUploadBudget=false`; suelo 10 ms.
- Experimento: `-Dlumina.experimentalUploadBudget=true`; suelo 2 ms.
- Reiniciar la instancia entre A/B. Mantener exactamente el mismo JAR parcheado
  en ambas condiciones; cambiar solo la propiedad JVM.

No cambiar hilos, prioridades, render distance, simulation distance, geometría,
animaciones, sombras, capacidad del staging buffer ni reglas de urgencia. Los
trabajos importantes que permiten ignorar el presupuesto y `updateImmediately`
conservan sus rutas originales. BBE redirige `BuilderTaskOutput.destroy()` en
`processChunkBuilds`; el parche no toca ese método ni el ciclo de destrucción.

## Medición que puede aceptar o rechazar la hipótesis

1. Compilar el fork fijado con Java 25 y su Gradle wrapper. Reemplazar únicamente
   Sodium en una copia de la variante `dependencies` (sin C2ME/BBE inicialmente).
   El script de build del pack no realiza ni publica ese reemplazo.
2. Instrumentar `updateChunks`, los collectors, `processChunkBuildResults` y
   `regions.uploadResults`: frame ID, presupuesto, bytes estimados/reales,
   cantidad de tareas, bloqueo de workers, cola de resultados, duración CPU
   y latencia desde recepción del chunk hasta geometría visible. Usar trazas
   separadas o registrar la sobrecarga de instrumentación.
3. Repetir cinco recorridos pregenerados y cinco hacia chunks nuevos por estado;
   alternar A/B, mismo mundo restaurado, gráficos, Java/GC y hardware. C2ME queda
   apagado para aislar la causa; después repetir el par con C2ME y con Iris.
4. Evaluar FPS, p99/p99.9 de frametime, tirones >33.3/50 ms, tiempo de upload,
   MSPT, cola, memoria nativa y p95 de latencia visible. No basta ganar FPS
   retrasando indefinidamente los chunks.
5. Criterio propuesto antes del ensayo: mejora de p99 mayor que la variabilidad
   entre repeticiones y latencia visible p95 que no empeore más del 10%; sin
   crecimiento sostenido de cola/memoria, huecos ni errores de transparencias.
   Ese 10% es un umbral de aceptación propuesto, no una mejora observada.

Primero verificar paridad visual, cambios inmediatos de bloques, carga/descarga,
cambios de dimensión, cancelaciones y cierre limpio. Si falla, volver al control.

## Validación realizada

Se comprobó que el parche aplica al commit revisado y se probó la fórmula en
rangos de fotogramas en el script de tests estáticos. No se compiló el fork,
no se ejecutó el flag en Minecraft y no hay resultados de FPS o chunks.
