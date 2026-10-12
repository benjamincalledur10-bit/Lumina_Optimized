# Lumina Optimized

**0.1.0-alpha.5** · Minecraft **26.3** · Java **25, 64 bits** · Fabric Loader **0.19.5**.

[Descargar Lumina-Optimized-0.1.0-alpha.5.mrpack](https://github.com/benjamincalledur10-bit/Lumina_Optimized/releases/download/v0.1.0-alpha.5/Lumina-Optimized-0.1.0-alpha.5.mrpack) en una instancia **nueva** de Modrinth App o Prism Launcher. Usa Java 25 ARM64 en Apple Silicon; el launcher necesita conexión para descargar los JAR oficiales. No mezcles la carpeta `mods` de alpha.4.

La lista de 42 entradas está representada: **35 mods principales + 7 bibliotecas externas = 42 JAR descargables**, más Text Placeholder API integrado. ZConfig es la única entrada adicional, requerida por Fast Noise. Hay **116 IDs de módulos integrados seleccionados** por la comprobación estática; el arranque real de Fabric enumera **162 IDs** incluyendo plataforma y módulos. [Versiones completas](docs/changelog-alpha.5.md) · [Validación](docs/validation-alpha.5.md).

BBE activo; Iris incluido con shaders apagados; LambDynamicLights instalado con `mode="off"`. Para activar las luces: **Mods → LambDynamicLights → configuración → modo de luces dinámicas**, por ejemplo Fancy. También se puede cambiar `mode` en `config/lambdynlights.toml`. No se incluyen shaders ni paquetes de recursos. No se distribuye `options.txt`, ni se fijan resolución, distancias o un límite de FPS.

Cull Leaves controla las hojas; More Culling conserva `DEFAULT` y no realiza culling de bloques. Gnetum no reduce la resolución del HUD, pero puede actualizarlo menos frecuentemente. BetterGrassify y Sodium Shadowy Path Blocks alteran el aspecto de césped/nieve y sombreado; revisa que te guste el resultado. C2ME y Remove Reloading Screen son publicaciones alpha.

**Limitación conocida:** [BBE documenta incompatibilidades con modelos personalizados EMF/ETF](https://github.com/EdeenMC/betterblockentities#mod-compatibility). El arranque registró avisos de creación repetida de modelos EMF y continuó. No instales recursos que cambien modelos de entidades de bloque sin revisar sus optimizaciones individuales. [Configuraciones e interacciones](docs/configuration-alpha.5.md).

Se verificaron publicaciones Fabric 26.3, JAR y bibliotecas integradas, dependencias, conflictos declarados, SHA-1/SHA-512, índices packwiz y exportación; pasaron **7 pruebas estáticas**. El arranque aislado con Java 25 ARM64 creó la ventana SDL y cargó recursos. **No se probó importación en un launcher, entrada a un mundo, exploración, guardado/reapertura ni rendimiento.** [Prueba sencilla de 10–15 minutos en tu Mac](docs/benchmarks.md). Acercarse a 200 FPS sigue siendo un objetivo; no hay una ganancia medida.

## Regenerar

Python 3.11+, packwiz fijado en `scripts/toolchain.json` y JDK 17+ para inspección; jugar requiere Java 25:

```sh
python3 scripts/build.py --packwiz .tools/bin/packwiz --cache .build/packwiz-cache
python3 scripts/test_static.py
python3 scripts/verify.py
```

En otro equipo con conexión puedes omitir `--cache`. `pack/` es la única composición activa; todos los pins fijan ID, versión, URL y SHA-512. Los JAR y `dist/` están fuera de Git. La exportación contiene URLs y configuraciones. `dist/SHA256SUMS-0.1.0-alpha.5` permite comprobar el paquete.

Alpha.1–alpha.4, sus evidencias y las mediciones previas se conservan. La fuente completa anterior está en `docs/history/alpha.4/`; los commits, tags y releases anteriores permanecen intactos. Alpha.5 corresponde a `modpackdev` y al tag `v0.1.0-alpha.5`: [pre-release](https://github.com/benjamincalledur10-bit/Lumina_Optimized/releases/tag/v0.1.0-alpha.5).
