# Lumina Optimized

Modpack de **Fabric** centrado en rendimiento, fluidez y opciones visuales, con tres ediciones independientes. Todas están en **beta**: no se garantiza una mejora de FPS sin mediciones comparables.

[Modrinth](https://modrinth.com/modpack/lumina-optimized) · [CurseForge](https://www.curseforge.com/minecraft/modpacks/lumina-optimized) · [GitHub Releases](https://github.com/benjamincalledur10-bit/Lumina_Optimized/releases)

**Estado del enlace de Modrinth (17 de octubre de 2026):** la página devuelve «Project not found». Mientras no esté accesible, descarga el `.mrpack` desde la release de tu edición en GitHub.

## Ediciones y descargas

Todas usan **Fabric Loader 0.19.5**. En **Apple Silicon**, selecciona **Java ARM64** de la versión indicada; en otros equipos usa Java de 64 bits adecuado para tu arquitectura.

| Minecraft | Versión del pack | Java | Rama | Descargas | Documentación |
| --- | --- | --- | --- | --- | --- |
| **26.3** | **v26.3-beta.1** | **25** | [`26.3dev`](https://github.com/benjamincalledur10-bit/Lumina_Optimized/tree/26.3dev) | [`.mrpack`](https://github.com/benjamincalledur10-bit/Lumina_Optimized/releases/download/v26.3-beta.1/Lumina-Optimized-26.3-beta.1.mrpack) · [ZIP CurseForge](https://github.com/benjamincalledur10-bit/Lumina_Optimized/releases/download/v26.3-beta.1/Lumina.Optimized-26.3-beta.1.zip) | [Versiones y changelog](docs/changelog-26.3-beta.1.md) · [Validación](docs/validation-26.3-beta.1.md) |
| **26.2** | **v26.2-beta.1** | **25** | [`26.2dev`](https://github.com/benjamincalledur10-bit/Lumina_Optimized/tree/26.2dev) | [`.mrpack`](https://github.com/benjamincalledur10-bit/Lumina_Optimized/releases/download/v26.2-beta.1/Lumina-Optimized-26.2-beta.1.mrpack) · [ZIP CurseForge](https://github.com/benjamincalledur10-bit/Lumina_Optimized/releases/download/v26.2-beta.1/Lumina.Optimized-26.2-beta.1.zip) | [Guía](docs/editions/26.2/README.md) · [Versiones](docs/editions/26.2/versions.md) · [Validación](docs/editions/26.2/validation.md) |
| **1.21.11** | **v1.21.11-beta.1** | **21** | [`1.21.11dev`](https://github.com/benjamincalledur10-bit/Lumina_Optimized/tree/1.21.11dev) | [`.mrpack`](https://github.com/benjamincalledur10-bit/Lumina_Optimized/releases/download/v1.21.11-beta.1/Lumina-Optimized-1.21.11-beta.1.mrpack) · [ZIP CurseForge](https://github.com/benjamincalledur10-bit/Lumina_Optimized/releases/download/v1.21.11-beta.1/Lumina.Optimized-1.21.11-beta.1.zip) | [Guía](docs/editions/1.21.11/README.md) · [Versiones](docs/editions/1.21.11/versions.md) · [Validación](docs/editions/1.21.11/validation.md) |

`modpackdev` presenta el proyecto común; cada rama de edición mantiene su selección y configuración. Las alphas y releases anteriores se conservan. `v<versión de Minecraft>-beta.<número>` identifica la edición del juego.

## Instalación

Crea **una instancia independiente para cada edición**. Importa el **`.mrpack`** en Modrinth App o Prism Launcher, o el **ZIP** en CurseForge App; también puedes instalar desde el catálogo de CurseForge. Selecciona la versión correcta de Java y evita importar sobre otra edición o abrir mundos de una versión posterior en una anterior. Usa copias de seguridad y un mundo de prueba.

**Los tres ZIP publicados ya fueron exportados desde CurseForge App** y se verificaron sus referencias y configuraciones. No son los ZIP iniciales de packwiz pendientes de reexportación. Esa comprobación no sustituye las pruebas de juego, guardado o estabilidad. Los nombres descargables de GitHub normalizan los espacios como puntos.

## Diferencias y ajustes iniciales

| Edición | Composición y ajustes específicos |
| --- | --- |
| **26.3** | **43 JAR**, Sodium **0.9.2** e Iris **1.11.7**. Conserva los ajustes gráficos de referencia del juego; no fija resolución, distancias ni límite de FPS. Gnetum incluido. |
| **26.2** | **43 JAR**, Sodium **0.9.2** e Iris **1.11.4**. **Renderizado 16 chunks, simulación 5, Prefer Vulkan, nubes apagadas, distancia de nubes 26 y partículas disminuidas**. Perfil gráfico Custom para conservarlos; BBE con **Shade Mode Sodium** y **Update Scheduler Smart**. No activa la reducción de resolución en Mac. Prefer Vulkan puede recurrir a OpenGL si Vulkan no está disponible. |
| **1.21.11** | **44 JAR**, Sodium **0.8.14** e Iris **1.10.8**. Añade **Language Reload 1.7.7** y **ScalableLux 0.1.6**; **sin Gnetum**. Activa **Reducir resolución en Mac** en Sodium Extra: reduce carga de renderizado y puede reducir nitidez. Desactívalo en sus ajustes para recuperar resolución nativa; no se fuerza una resolución concreta ni las distancias. |

Los conteos JAR incluyen bibliotecas y PolyTone: 26.3/26.2 llevan **35 mods principales + 7 bibliotecas + PolyTone**; 1.21.11 lleva **36 + 7 + PolyTone**. Los módulos integrados en esos archivos no son instalaciones adicionales.

En las tres ediciones, **BBE está activo; los shaders y las luces dinámicas empiezan apagados**. Se incluyen **Lumina Event Horizon 1.3.9** y **Lumina Lite 1.2.9**: selecciona uno en **Opciones → Ajustes de vídeo → Shader Packs**. Para activar luces dinámicas, abre la configuración de **LambDynamicLights** desde Mod Menu. Ambas opciones pueden aumentar el coste de renderizado.

Se conserva la corrección **ModernFix/Lithium del caché de temperatura**. ServerCore mantiene desactivados los cambios automáticos de distancias, mobcaps y comportamiento; Cull Leaves y More Culling evitan superponer sus ajustes de hojas. Las opciones gráficas siguen siendo modificables por el usuario.

## Recursos por plataforma

Los recursos incluidos comienzan activados. Puedes desactivarlos en **Opciones → Paquetes de recursos**.

| Edición | Modrinth / `.mrpack` | CurseForge / ZIP |
| --- | --- | --- |
| **26.3** | **4**, con Mandala **2.1** | **4**, con Mandala **2.6** |
| **26.2** | **4**, con Mandala **2.1** | **3**, sin Mandala |
| **1.21.11** | **4**, con Mandala **2.1** | **3**, sin Mandala |

Los otros tres son **Translations for Sodium 8.19.0**, **Fresh Animations** y **Fullbright UB**, con EMF/ETF y PolyTone como soporte ya instalado. 26.3/26.2 usan Fresh Animations **1.10.5** y Fullbright **7.0**; 1.21.11 usa **1.10.4** y **6.0**. Cambian traducciones, animaciones/modelos, iluminación visual e interfaz; no son una referencia visual vanilla.

Mandala 2.1 conserva el archivo oficial con formato anterior aceptado explícitamente; su aspecto completo sigue pendiente, especialmente en 26.3/26.2. Mandala 2.6 de CurseForge 26.3 tiene avisos por metadatos incompletos, aunque la recarga terminó. En CurseForge 26.2/1.21.11 **Mandala se omite**, también de `options.txt`; no se modifica el ZIP del autor para forzar compatibilidad.

## Validaciones y pruebas pendientes

Se comprobaron versiones, URLs y hashes oficiales, dependencias externas e integradas, conflictos declarados, configuraciones, integridad de exportaciones y referencias de los ZIP publicados. Hay arranques aislados de aproximadamente **45 segundos en macOS ARM64** con recarga de recursos; no equivalen a una sesión de juego ni validan cierre normal. El arranque inicial de 26.3 precede a la incorporación de los dos shaders; su mera inclusión no demuestra que compilen.

El usuario reportó pruebas breves favorables en Mac para 1.21.11 y 26.2. Las capturas y reportes no son comparaciones controladas: resolución efectiva, cámara, mundo y ajustes pueden variar. **No se afirma una ganancia de FPS general ni un objetivo de FPS garantizado**; compara con la misma resolución efectiva, recursos, backend, mundo y ajustes.

Siguen vigentes estas limitaciones:

- **C2ME** es experimental; **ScalableLux en 1.21.11** y **PolyTone alpha en 26.3** requieren más pruebas en sus combinaciones. Faltan sesiones largas y comprobaciones específicas de FastQuit/C2ME al guardar y reabrir.
- **BBE/EMF/ETF con Fresh Animations** puede afectar modelos, en especial shulkers, cofres y carteles; se registraron avisos de recreación de modelos. Revisa también atriles en 26.2 y las pantallas de Mandala. En 1.21.11 persiste un aviso de integración opcional de More Culling con Sodium.
- **Gnetum**, presente en 26.3/26.2, puede refrescar el HUD menos frecuentemente; comprueba su interacción con ImmediatelyFast y Better Mount HUD al montar.
- Faltan validación completa de **ambos shaders**, estabilidad prolongada, multijugador y pruebas en **Windows/Linux**. La comprobación de archivos y la exportación desde CurseForge App no resuelven esas pruebas.

Para una revisión sencilla, juega **10–15 minutos**: explora, revisa recursos/modelos y el HUD, construye algo, sal al menú esperando el guardado y reabre el mundo. Prueba cada shader por separado si lo vas a usar. Conserva `logs/latest.log` y cualquier crash report. No hace falta una matriz de benchmarks.

## Créditos y soporte

Gracias a los autores de los mods y bibliotecas, a los traductores de **Sodium**, a **FreshLX** (Fresh Animations), **World Resource Pack** (Fullbright UB) y **CesarZorak / Mandala Creations** (Mandala’s GUI).

Shaders Lumina de **Benjiaa**, basados en [Complementary Reimagined](https://www.complementary.dev/). Se conservan archivos y licencias originales; Lumina Optimized asume la responsabilidad de su integración conforme a Complementary License Agreement 1.6, sin atribuir al autor original el soporte del modpack.

[Reportar un problema](https://github.com/benjamincalledur10-bit/Lumina_Optimized/issues): indica edición, launcher, sistema operativo, versión de Java, pasos para reproducirlo y adjunta el log o crash report.
