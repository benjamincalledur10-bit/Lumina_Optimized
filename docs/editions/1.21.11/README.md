# Lumina Optimized v1.21.11-beta.1

Edición independiente para **Minecraft 1.21.11, Java 21 y Fabric Loader 0.19.5**, mantenida en `modpackdev` y `1.21.11dev`. La edición 26.3, los cambios locales anteriores, los tags y las releases existentes se conservan. Esta beta conserva la composición final de alpha.1 y se identifica con el tag `v1.21.11-beta.1`.

Importa **`dist/Lumina-Optimized-1.21.11-beta.1.mrpack`** en una instancia nueva de Modrinth App o Prism Launcher. Selecciona **Java 21 ARM64 en Apple Silicon**. No lo importes sobre la instancia 26.3; crea un mundo de prueba 1.21.11.

## Composición

- **36 mods principales**, más **PolyTone** como soporte de Fullbright, y **7 bibliotecas externas**: **44 archivos JAR**.
- **4 resource packs activados:** Translations for Sodium 8.19.0, Fresh Animations 1.10.4, Fullbright UB 6.0 y Mandala’s GUI – Dark mode 2.1.
- **2 shaders instalados y apagados:** Lumina Event Horizon 1.3.9 y Lumina Lite 1.2.9. Iris 1.10.8 está incluido junto con Sodium 0.8.14.
- Fabric resolvió **119 módulos integrados activos**, incluido MixinExtras proporcionado por Loader: 118 proceden de los mods. Hay 151 apariciones de candidatos integrados contando duplicados y candidatos descartados. La lista del arranque muestra 166 IDs: 44 JAR raíz + 119 integrados + Minecraft, Java y Loader. Estos IDs no son 166 mods instalados por separado.

Todos los componentes seleccionados tienen publicación oficial compatible. Gnetum se retira únicamente de 1.21.11 por solicitud del usuario; no se sustituye. No se añaden otros mods de alpha.4. Las versiones, dependencias y enlaces oficiales están en [versions.md](versions.md); el inventario con hashes está en [selection.json](selection.json).

## Configuración inicial

BBE está activo y conserva las animaciones. Se retira `misc.shademode` porque no existe en BBE 1.3.4. Los shaders empiezan apagados; puedes elegir uno en **Opciones → Ajustes de vídeo → Shader Packs**. LambDynamicLights está instalado con `mode="off"`; actívalo desde **Mods → LambDynamicLights → Configurar** o su menú de luces dinámicas en vídeo.

Por petición del usuario, Sodium Extra activa por defecto **Reducir resolución en Mac** (`extra_settings.reduce_resolution_on_mac=true`). Es una [función de Sodium Extra específica de macOS](https://github.com/FlashyReese/sodium-extra/wiki/Features): puede reducir la nitidez para disminuir el trabajo de renderizado. Puedes desactivarla en **Opciones → Ajustes de vídeo → Extra → Reducir resolución en Mac**; reinicia si es necesario. No se fuerza una resolución concreta como 1920×1206, ni se cambian distancias, animaciones, límite de FPS o los demás ajustes gráficos. `options.txt` sigue conteniendo solo la versión de datos y selección de recursos.

Cull Leaves se ocupa de las hojas. More Culling conserva `leavesCullingMode="DEFAULT"`, `useBlockStateCulling=false` e `includeMangroveRoots=false`, para evitar superponer ambos tratamientos. Entity Culling conserva `safeMode=true` y activa `tickCulling=true`: evita algunas actualizaciones de entidades ocultas en el cliente; no cambia la simulación del servidor. Las hojas sólidas siguen desactivadas. Comprueba las animaciones al volver a mostrar criaturas; para comparar, puedes desactivar tick culling en su configuración y reiniciar.

La corrección **ModernFix/Lithium** se verificó de nuevo: ambos sobrescriben `Biome.method_21740(BlockPos,int)`. Se desactiva solamente `mixin.perf.remove_biome_temperature_cache` de ModernFix. ModernFix también desactiva por su propia compatibilidad con C2ME tres opciones de chunks; el log registra esas decisiones del autor.

ServerCore mantiene desactivados los ajustes dinámicos de distancias, los mobcaps adicionales, breeding cap, activation range y lobotomización de aldeanos. Su configuración se comprobó con el esquema de 1.5.15 y el SnakeYAML integrado. C2ME conserva sus ajustes predeterminados salvo el límite de interfaz y el protocolo de distancia extendida desactivado; no cambia la distancia de renderizado seleccionada.

## Incorporaciones y comparación

Se añaden **Language Reload 1.7.7+1.21.11** y **ScalableLux 0.1.6+fabric.c25518a**. Se elige la publicación estable de ScalableLux compatible con Fabric/1.21.11; también existe una alpha más reciente, que no se añade. Language Reload cubre la recarga al cambiar idioma; no se presenta como una mejora de FPS durante el juego. ScalableLux cambia el motor de iluminación y proporciona el alias `starlight`; el usuario reportó su prueba breve de juego sin problemas; las comprobaciones específicas de iluminación con C2ME y sesiones largas no tienen resultados individuales. No se cambia su configuración predeterminada ni se instala Starlight adicional.

**Text Placeholder API 2.8.2+1.21.10** ya está integrado en Mod Menu y publicado para 1.21.11. Su SHA-512 oficial y selección por Fabric se comprobaron; cumple la incorporación solicitada sin duplicar el JAR externo. Las siete bibliotecas externas siguen siendo siete.

**Gnetum se ha eliminado del paquete 1.21.11**, tanto el JAR como su configuración. Se conserva el resto de la selección y los ajustes. La comparación anterior ON/OFF queda como evidencia histórica en `history/with-gnetum-additions/`; ya no se genera. La composición final se promociona a `1.21.11-beta.1` sin añadir mods ni cambiar sus configuraciones.

Para comparar brevemente con FO, usa copias del mismo mundo y mantén posición, cámara, recursos, resolución efectiva, renderizado 16, simulación 5, VSync OFF y los demás ajustes iguales. Usa el mismo valor de **Reducir resolución en Mac** en ambas instancias y el mismo modo de ventana/pantalla completa; compara también la resolución efectiva. Para una comparación a resolución nativa, desactiva esa opción en ambas. Espera a que se carguen los chunks y observa aproximadamente un minuto con F3 en el mismo estado. La reducción de resolución está documentada como una elección del usuario; sus FPS no se presentan como una mejora a igual calidad.

## Limitaciones y prueba breve

**Prueba de juego reportada por el usuario: completada sin problemas en su Mac el 12 de octubre de 2026.** No se recibieron logs ni duración exacta o resultados por función. [Registro del reporte](user-play.json). El agente ejecutó únicamente las comprobaciones estáticas y el arranque aislado. La captura más reciente muestra 381 FPS (p50=402) a 1470×923; es una observación con resolución reducida, no una ventaja demostrada a igual calidad.

**Las siete comprobaciones estáticas del paquete sin Gnetum pasaron**. La evidencia del arranque de la composición final alpha, idéntica a esta beta salvo su identidad, se registra en [runtime.json](runtime.json); las comprobaciones anteriores con Gnetum instalado se conservan en `history/with-gnetum-additions/` y el inicio sin Gnetum con resolución nativa en `history/without-gnetum-full-resolution/`. El inicio aislado no valida juego, guardado, estabilidad ni rendimiento. La captura del usuario muestra 311 FPS (p50=324) a 1920×1206; la anterior mostraba 178 FPS a 2940×1846. La resolución y el ángulo de cámara cambiaron, por lo que no son una prueba controlada de ganancias atribuibles a mods. [Detalles de validación](validation.md).

- C2ME y ScalableLux se siguen tratando como experimentales. El módulo nativo opcional de C2ME exige Java 22 y Fabric lo descarta con Java 21; se conserva el JAR oficial intacto. FastQuit reconoce Ixeris y evita servidores integrados simultáneos mediante su comprobación de compatibilidad. El usuario reportó la prueba breve sin problemas; no aportó resultados individuales de guardado/reapertura ni sesiones largas.
- Mandala 2.1 está publicado para 1.21.11, pero su `pack.mcmeta` declara formato 64, anterior al 75 de esta versión. Se mantiene el original y se acepta su formato en `incompatibleResourcePacks`; la recarga funcionó, pero su aspecto y todas sus pantallas requieren revisión. Es distinto del Mandala 2.6 usado en la exportación CurseForge de 26.3.
- BBE 1.3.4 declara Sodium ≥0.8.7 sin límite superior, pero sus notas anuncian hasta 0.8.13-beta.2. El inicio con 0.8.14 funcionó; revisa cofres, carteles y shulkers. La interacción BBE/EMF con Fresh Animations puede alterar modelos.
- More Culling intenta encontrar una clase antigua de Sodium que ya no existe. El mixin es opcional (`@Pseudo`), el inicio continuó y el culling de bloques de More Culling está desactivado. Su interacción durante el juego sigue pendiente.
- PolyTone recomienda Nautilus Studio; no es obligatorio y no se añadió. Fullbright, BetterGrassify, SSPB y los recursos pueden cambiar la apariencia; desactiva los resource packs desde **Opciones → Paquetes de recursos** para compararlos.

Prueba durante **10–15 minutos** con tus ajustes habituales:

1. Importa y abre un mundo nuevo; confirma los cuatro recursos activos y los shaders/luces dinámicas apagados.
2. Camina o vuela generando chunks. Revisa tirones, errores gráficos y el HUD; monta un caballo para probar Better Mount HUD.
3. Coloca y abre cofres, shulkers y carteles; observa las animaciones de criaturas y la vegetación.
4. Sal al menú, espera a que termine el guardado de FastQuit, reabre el mismo mundo y comprueba lo construido.
5. Opcionalmente activa cada shader Lumina por separado y después vuelve a apagarlos. Registra cualquier error de compilación o renderizado.

Para informar un fallo, guarda `logs/latest.log`, el crash report si existe y qué estabas haciendo. No se requiere una matriz de benchmarks. Windows/Linux, multijugador, compilación de shaders y rendimiento sostenido quedan pendientes.

## Reconstrucción y validación

Desde la raíz del repositorio, con Python 3.11+ y un JDK en `PATH`:

```sh
python3 scripts/edition_12111.py --build --packwiz .tools/bin/packwiz
```


Si packwiz está instalado en `PATH`, puedes omitir `--packwiz`. El comando valida publicaciones y bytes, prepara una caché aislada de archivos verificados, ejecuta `packwiz refresh` y `packwiz modrinth export`, y rechaza exportaciones incompletas. No modifica `pack/`. Sin `--build` valida el paquete ya generado.

Definición: [`packs/1.21.11/`](../../../packs/1.21.11/pack.toml). Artefactos locales: `dist/Lumina-Optimized-1.21.11-beta.1.mrpack` y `dist/SHA256SUMS-1.21.11-beta.1`. [Changelog](changelog.md).

## Variante CurseForge

[ZIP e instrucciones de CurseForge](curseforge.md): `Lumina-Optimized-1.21.11-beta.1-curseforge.zip`. Usa Mandala **2.6** únicamente en esa variante; el `.mrpack` conserva 2.1. Mismos mods/configuraciones y 50 referencias oficiales comprobadas. Importación y reexportación desde CurseForge App pendientes antes de su envío a la plataforma.

La variante CurseForge completó el inicio aislado de 45 segundos, pero **Mandala 2.6 fue rechazado por metadatos incompletos (`min_format`/`max_format`)**. Se conserva el original; su aplicación/aspecto y la importación en CurseForge App siguen pendientes. El `.mrpack` mantiene Mandala 2.1. [Evidencia](runtime-curseforge.json).
