# Lumina Optimized v1.21.11-beta.1

Minecraft **1.21.11**, **Java 21**, **Fabric Loader 0.19.5**. Primera beta de esta edición; la edición 26.3 y las releases anteriores se conservan.

- Promociona la composición final de alpha.1: **36 mods principales, 7 bibliotecas y PolyTone**, 4 resource packs activados y 2 shaders Lumina instalados pero apagados.
- Sodium **0.8.14** e Iris **1.10.8**. BBE activo; luces dinámicas apagadas; tick culling activo con modo seguro. Gnetum ausente.
- Language Reload **1.7.7+1.21.11**, ScalableLux **0.1.6+fabric.c25518a** y Text Placeholder API **2.8.2+1.21.10** integrado, sin JAR duplicado.
- **Reducir resolución en Mac** activado por defecto por petición del usuario; reversible desde Sodium Extra. Puede reducir la nitidez. No se fijan distancias ni límite de FPS.
- Conserva corrección ModernFix/Lithium y ServerCore sin cambios automáticos de distancias, mobcaps o comportamiento.
- Siete comprobaciones estáticas superadas. El inicio aislado de la composición final alpha completó la recarga; la beta conserva exactamente sus archivos y configuraciones. **El usuario reportó su prueba breve en Mac sin problemas**; no se recibieron logs ni resultados individuales.
- La captura del usuario muestra 381 FPS a 1470×923. No se afirma una ganancia a igual resolución ni se garantiza esa cifra. Pendientes: validación independiente, sesiones largas, pruebas específicas de shaders/iluminación/modelos y Windows/Linux.

[Versiones](versions.md) · [Validación](validation.md) · [Reporte de juego](user-play.json)

La variante [CurseForge](curseforge.md) conserva mods/configuraciones y usa Mandala **2.6**, siguiendo el cambio aprobado para esa plataforma. ZIP validado con 50 referencias; importación/reexportación desde CurseForge App pendientes. El `.mrpack` mantiene Mandala 2.1.

## Historial local de la alpha

# Lumina Optimized v1.21.11-alpha.1

Primera edición para **Minecraft 1.21.11 · Java 21 · Fabric Loader 0.19.5**. Preparada localmente, sin commit, push ni publicación.

## Selección

- Definición independiente en `packs/1.21.11/`; se conserva intacta la edición 26.3 y su historial.
- Se revisan los 49 archivos de la composición actual: 35 mods principales, 7 bibliotecas, PolyTone, 4 resource packs y 2 shaders. Todos tienen publicación oficial para la versión objetivo. Sin omisiones ni sustituciones de proyectos.
- Pareja **Sodium 0.8.14 / Iris 1.10.8**; Reese’s Sodium Options 2.2.4 y Sodium Extra 0.9.4 satisfacen sus requisitos. Todas las versiones exactas y los cambios respecto a 26.3 están en [versions.md](versions.md).
- BBE 1.3.4, Lithium 0.21.4, FerriteCore 8.2.0, ImmediatelyFast 1.14.3, C2ME 0.3.6.0.0 y ServerCore 1.5.15 usan sus archivos Fabric para 1.21.11.
- Fresh Animations pasa de 1.10.5 a **1.10.4**, y Fullbright UB de 7.0 a **6.0**, usando las publicaciones de 1.21.11. Se conservan Translations for Sodium 8.19.0 y Mandala 2.1.
- Se conservan Lumina Event Horizon **1.3.9** y Lumina Lite **1.2.9**, publicados para Iris/1.21.11. Ambos comienzan apagados.
- Bibliotecas fijadas: **Fabric API 0.141.6+1.21.11**, **Cloth Config 21.11.153+fabric**, **Fabric Language Kotlin 1.14.2+kotlin.2.4.21**, **Forge Config API Port 21.11.1**, **GeckoLib 5.4.5**, **YACL 3.8.2+1.21.11-fabric**, **ZConfig 1.0.0+1.21.x**. PolyTone de soporte: **1.21.11-6.6.0**.
- MidnightLib y Text Placeholder API se satisfacen con las versiones integradas verificadas por SHA-512. MixinExtras procede de Fabric Loader. No se añaden copias externas.
- Fast Noise **1.0.40+1.21.11** no requiere ZConfig en esta publicación. ZConfig se conserva; sus copias de Night Config se resuelven con las de otros mods.

## Configuraciones

- BBE activo; animaciones conservadas. Se elimina su opción ausente `misc.shademode`.
- Recursos activados por defecto. Se conserva la aceptación explícita del formato antiguo de Mandala 2.1; apariencia pendiente.
- Shaders y luces dinámicas apagados. LambDynamicLights recibe únicamente la opción real `mode="off"`; las demás usan los valores predeterminados de 4.9.1.
- Corrección de temperatura ModernFix/Lithium confirmada de nuevo por inspección del código y aplicada durante el arranque.
- Cull Leaves y More Culling evitan superponer el culling de hojas. ServerCore conserva desactivados los cambios automáticos de distancias, mobcaps y comportamiento.
- Se adapta el `data_version` de `options.txt` a **4671**. No se fijan resolución, distancias, calidad ni límite de FPS.

## Validación y pendientes

Siete comprobaciones estáticas pasaron: publicaciones/hashes, integridad recursiva de JAR, dependencias, conflictos declarados, configuraciones reales, índice packwiz y exportación completa. El `.mrpack` contiene **49 referencias oficiales** y **13 overrides**. Una exportación inicial incompleta por timeouts fue rechazada y regenerada con una caché de bytes ya verificados.

El arranque aislado con **Java 21 ARM64 en macOS** completó inicialización y recarga de recursos durante 45 segundos. Se detuvo deliberadamente; no se entró en un mundo. Fabric seleccionó los módulos compatibles y descartó el módulo nativo opcional de C2ME que exige Java 22.

Pendientes: importación mediante launcher, juego, exploración, guardado/reapertura con FastQuit/C2ME, HUD montado con Gnetum/ImmediatelyFast, modelos BBE/EMF, renderizado con Sodium 0.8.14, ambos shaders, estabilidad, Windows/Linux y rendimiento. Se documentan advertencias de compatibilidad opcional de More Culling/Sodium y la recomendación no obligatoria Nautilus Studio de PolyTone.

**No se afirma ninguna mejora de FPS.** [Validación y evidencia](validation.md).

## Actualización local tras la primera prueba — 12 de octubre de 2026

Se conserva el nombre `1.21.11-alpha.1`; no se publica una nueva versión. La definición y evidencia anteriores a estos cambios están preservadas localmente en `.build/edition-1.21.11/initial-alpha1/`, y su validación/arranque se conservan en [history/initial-alpha1/](history/initial-alpha1/).

- Añadido **Language Reload 1.7.7+1.21.11** (`rJRsdV10`), con Fabric API ya incluido; sin biblioteca adicional.
- Añadido **ScalableLux 0.1.6+fabric.c25518a** (`PV9KcrYQ`), publicación estable Fabric compatible con 1.21.11. Conserva valores predeterminados, proporciona `starlight` y no requiere otro JAR externo. Interacción con C2ME pendiente en mundo.
- **Text Placeholder API 2.8.2+1.21.10** (`qxjzQ9xY`) ya integrado y verificado dentro de Mod Menu. Sin duplicación externa.
- Entity Culling: **`tickCulling=true` y `safeMode=true`**. Hojas sólidas desactivadas y calidad visual/distancias/resolución conservadas.
- Comparación opcional con **Gnetum OFF**, generada desde la misma base. Mantiene el JAR y solo cambia su interruptor maestro; el principal conserva ON.
- Total actualizado: **37 principales + PolyTone + 7 bibliotecas externas = 45 JAR**; 4 recursos y 2 shaders = **51 referencias oficiales**, 13 overrides. Los 119 IDs integrados activos siguen separados del conteo principal.
- Ambas exportaciones pasan siete grupos estáticos; se documenta por separado el nuevo arranque aislado y las pruebas de exploración/guardado/estabilidad pendientes. [Validación](validation.md).

Los FPS mostrados por el usuario en la alpha inicial no son mediciones de estos cambios. La observación de 331 FPS tras desvincular FO tampoco demuestra una mejora causada por desvincular. El 12 de octubre se observó en los archivos de sus instancias `reduce_resolution_on_mac=true` en FO y `false` en Lumina, así como fullscreen true/false respectivamente: comparar exige comprobar resolución efectiva y ventana, además del mismo mundo. No se alteraron dichas instancias.

**No se afirma un aumento de FPS ni se garantiza el objetivo del 10 %.** La edición 26.3 y sus dos artefactos distribuidos permanecen intactos; sin commit, push ni publicación.

## Retirada de Gnetum — 12 de octubre de 2026

- Se elimina **Gnetum 4.6.3+1.21.11-fabric** del `.mrpack` de 1.21.11 y se retira `config/gnetum.json`. No se sustituye por otro mod. **26.3 permanece intacto**.
- Se conserva Language Reload, ScalableLux, Text Placeholder integrado, tick culling con modo seguro y el resto de los mods/recursos/configuraciones. No cambian resolución, distancias, calidad ni límites de FPS.
- Nuevo conteo: **36 principales + PolyTone + 7 bibliotecas = 44 JAR**, 119 IDs integrados activos, 4 recursos y 2 shaders. **50 referencias oficiales y 12 overrides**.
- La variante anterior Gnetum OFF deja de generarse. Sus validaciones y arranques, así como el principal anterior, se conservan en [history/with-gnetum-additions/](history/with-gnetum-additions/); los artefactos previos se archivan en `.build/edition-1.21.11/before-gnetum-removal/`.
- Se regenera el principal con packwiz, se repiten las siete comprobaciones estáticas y se ejecuta un nuevo inicio aislado, separado de juego y rendimiento. El mismo nombre local `1.21.11-alpha.1` no implica que el archivo siga siendo el anterior: consulta su SHA-256 actualizado.

La captura del usuario muestra 178 FPS, p50=181, p98=129 y p99.5=121 en 2940×1846, render 16/simulación 5. Está orientada al sur, mientras la captura anterior apuntaba al oeste. Estas imágenes no constituyen una comparación controlada ni permiten atribuir el resultado a Gnetum o ScalableLux. La observación de FO a 331 FPS al desvincular tampoco tiene una causa demostrada; su ajuste de reducción de resolución en Mac permanece activado. No se promete reproducir 331 FPS ni se afirma una ganancia.

## Reducir resolución en macOS por defecto — 12 de octubre de 2026

- A petición del usuario se activa **Sodium Extra → Reducir resolución en Mac** (`extra_settings.reduce_resolution_on_mac=true`) únicamente en la edición 1.21.11. Es reversible desde los ajustes de vídeo de Sodium Extra; reiniciar si es necesario. No fija una resolución concreta.
- Se conserva la composición: **36 principales + PolyTone + 7 bibliotecas**, 4 recursos y 2 shaders. Gnetum sigue ausente; no se añade contenido. Distancias, animaciones, shaders/luces inicialmente apagados y los demás ajustes se mantienen.
- Se actualizan la comprobación de configuración y la documentación. Se regenera el `.mrpack`, se validan hashes/índice/exportación y se realiza otro inicio aislado. El arranque previo a este cambio está archivado en `history/without-gnetum-full-resolution/`.
- La captura aportada por el usuario muestra 311 FPS (p50=324) a 1920×1206; la previa mostraba 178 FPS a 2940×1846. La resolución reducida puede afectar la nitidez y no se presenta como una mejora de rendimiento a igual calidad ni como una cifra garantizada. Falta jugar 10–15 minutos, explorar y guardar/reabrir con esta composición final.
- Edición 26.3 intacta; sin commit, push ni publicación.

La variante CurseForge completó el inicio aislado de 45 segundos, pero **Mandala 2.6 fue rechazado por metadatos incompletos (`min_format`/`max_format`)**. Se conserva el original; su aplicación/aspecto y la importación en CurseForge App siguen pendientes. El `.mrpack` mantiene Mandala 2.1. [Evidencia](runtime-curseforge.json).
