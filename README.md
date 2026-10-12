# Lumina Optimized

**v26.3-beta.1** · Minecraft **26.3** · Java **25, 64 bits** · Fabric Loader **0.19.5**.

[Descargar el .mrpack](https://github.com/benjamincalledur10-bit/Lumina_Optimized/releases/download/v26.3-beta.1/Lumina-Optimized-26.3-beta.1.mrpack) e importarlo en una instancia nueva de Modrinth App o Prism Launcher. Apple Silicon: Java 25 ARM64. El launcher descarga los archivos desde sus URLs oficiales.

Conserva los **35 mods principales y 7 bibliotecas externas de alpha.5**, añade **PolyTone** para Fullbright y **4 resource packs**: 43 JAR + 4 resource packs + 2 shader packs = **49 archivos descargables**. Las versiones de los mods anteriores y sus configuraciones permanecen fijas. [Versiones y changelog](docs/changelog-26.3-beta.1.md) · [Validación](docs/validation-26.3-beta.1.md).

Los cuatro recursos están **activados de forma predeterminada**:

- **Translations for Sodium v8.19.0:** traducciones de sus opciones.
- **Fresh Animations 1.10.5:** animaciones/modelos de criaturas mediante EMF y ETF, ya incluidos.
- **Fullbright UB 7.0:** iluminación visual de cuevas y noche; PolyTone **26.3-6.8.6-alpha** incluido como soporte.
- **Mandala’s GUI - Dark mode 2.1:** interfaz oscura. Publicado hasta 1.21.11, formato 64; se acepta su formato anterior por petición del usuario. Su aspecto completo en 26.3 sigue pendiente y puede mostrar aviso de incompatibilidad.

Para desactivar cualquiera: **Opciones → Paquetes de recursos**, moverlo a disponibles y pulsar Hecho. `options.txt` solo selecciona estos recursos y su excepción de formato; resolución, distancias, calidad y FPS conservan los valores del juego. Revisa comparaciones con los mismos recursos activos.

BBE sigue activo. Iris incluido con shaders apagados. Se incluyen **Lumina Event Horizon 1.3.9** y **Lumina Lite 1.2.9**, disponibles en **Opciones → Ajustes de vídeo → Paquetes de shaders**. Elige uno y activa los shaders para probarlo; no se pueden usar ambos simultáneamente. Los shader packs alteran el aspecto y su coste de rendimiento está pendiente de medir. LambDynamicLights permanece Off; se activa en **Mods → LambDynamicLights → configuración → modo Fancy/Fast**. ServerCore conserva las funciones que alteran distancias, mobcaps y comportamiento desactivadas. Se mantiene la corrección ModernFix/Lithium del caché de temperatura y Cull Leaves sin superposición con More Culling.

**Beta:** C2ME y PolyTone son experimentales. BBE documenta límites con modelos personalizados EMF/ETF; revisa especialmente shulkers con Fresh Animations. Gnetum puede refrescar el HUD menos frecuentemente. [Configuraciones heredadas](docs/configuration-alpha.5.md) · [Prueba de 10–15 minutos en Mac](docs/benchmarks.md).

Las capturas del usuario en alpha.5 muestran 149.22 FPS en FO y 197.49 en Lumina a 2940×1846 en M4, usando Prefer Vulkan según su reporte. Son lecturas puntuales en mundos distintos de la misma semilla; no prueban una ventaja general ni el rendimiento de esta beta con recursos. [Evidencia y límites](docs/research/user-play-alpha.5.json).

Los shaders son de **Benjiaa**, basados en [Complementary Reimagined](https://www.complementary.dev/). Se conservan sus archivos/licencias y se descargan mediante las referencias oficiales de Modrinth. Lumina Optimized asume la responsabilidad de su integración conforme a Complementary License Agreement 1.6; esto no atribuye al autor original el soporte del modpack.

La revisión de shaders reemplaza el `.mrpack` de **v26.3-beta.1**, sin crear beta.2. El arranque de 45 segundos documentado corresponde al paquete anterior sin estos shaders; la importación y compilación de ambos en Minecraft siguen pendientes.

Las alphas, sus tags y releases se conservan. La nueva nomenclatura `v<versión de Minecraft>-beta.<número>` identifica la edición para cada versión del juego.
