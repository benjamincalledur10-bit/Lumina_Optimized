# Dependencias alpha.4

Core contiene **29 principales + 4 dependencias externas** (33 JAR descargables); Shaders **30 + 4** (34). Fabric API **0.161.0+26.3**, Cloth Config **26.3.159+fabric**, Resourceful Config **6.0.1** y ZConfig **1.0.0+26.x** permanecen fijados. Minecraft 26.3 / Java 25 / Loader 0.19.5 satisfacen los requisitos efectivos de todos los JAR revisados.

## Bibliotecas proporcionadas e integradas

- Mod Menu y ServerCore integran **Placeholder API 3.2.0+26.3**, con bytes idénticos a la publicación `lXytLqWj`. Loader selecciona un proveedor; no se añade otra descarga externa.
- ServerCore integra además **DazzleConf core/ext-snakeyaml 1.3.0-M2** y **SnakeYAML 2.7**. Necesita los módulos Fabric API base, comandos y lifecycle ya proporcionados por Fabric API.
- Krypton integra **Velocity Native 3.4.0-SNAPSHOT**. No hay una dependencia cruzada obligatoria/incompatible con C2ME en su `fabric.mod.json`.
- Sodium Extra 0.9.4 integra **Greenlight API 0.1.0+mc26.3**; no requiere instalar Sodium Options API.
- Loader integra **MixinExtras 0.5.5**; ModernFix contiene 0.5.4, descartado a favor del proveedor del Loader. Fast Surface exige MixinExtras ≥0.5.0 en su configuración de mixins; ya está satisfecho.
- C2ME integra sus módulos, NightConfig **3.6.5** y otras bibliotecas. ZConfig integra NightConfig **3.8.3**, seleccionado por Loader; Fast Noise y Fast Surface usan el mismo ZConfig externo.
- Fast Noise integra `zfastnoise-ocl` **1.0.0-beta.1+26.3**; su presencia no demuestra que se use OpenCL.
- Jasione y Async Logger incluyen clases NightConfig bajo sus propios namespaces `shadow`. Async Logger incluye clases Disruptor. Son bibliotecas dentro del JAR, sin IDs Fabric separados; no se cuentan como principales ni requieren otro archivo. Jasione usa ASM del classpath de lanzamiento Fabric; no se añade un mod ASM.

Core: **101 apariciones** de módulos anidados, **84 IDs distintos**, **83 IDs seleccionados**. Shaders: **106 / 87 / 86**, respectivamente. Se excluyen los módulos proporcionados por Loader de este recuento; MixinExtras del Loader se registra aparte. Los duplicados anidados pertenecen a los JAR originales: no se extraen ni reempaquetan. La enumeración real de Fabric cuenta también el entorno: 120 IDs en Core y 124 en Shaders.

## Dependencias y conflictos de los siete JAR recibidos

| Mod | Requisitos adicionales efectivos | Incompatibilidades declaradas |
| --- | --- | --- |
| ServerCore 1.5.20+26.3 | Loader ≥0.19.5, Minecraft ≥26.3-, tres módulos Fabric API | Cardboard |
| Krypton 0.3.2 | Loader ≥0.18.4, Minecraft ≥26.2; Velocity integrado | Ninguna en fabric.mod.json |
| Jasione 1.0.9+26.1.2-fabric | Loader ≥0.16.0, Minecraft ≥26.1 | Redirector |
| Async Logger 2.2.2+26.1.2-fabric | Loader ≥0.16.0, Minecraft ≥26.1 | Ninguna en fabric.mod.json |
| Better Biome Blend 1.4.0 (archivo 26.3) | Loader ≥0.19.5, Fabric API, Minecraft ~26.3, Java ≥25 | Ninguna en fabric.mod.json |
| Fast Surface 1.0.0+26.3 | Loader ≥0.19.5, Minecraft ~26.3, Java ≥25, ZConfig ≥1.0.0+26.x, MixinExtras ≥0.5.0 | Moonrise |
| FastMapCodec 1.0.4 Fabric | Loader ≥0.19.3, Minecraft ≥1.21, Java ≥21 | Ninguna en fabric.mod.json |

Fast Surface **recomienda** `zmatcomp`, pero no lo exige. El inicio real avisa de su ausencia; no se añade una quinta dependencia por esa recomendación. Su regla de mixin de superficie también declara incompatibilidad con Biolith; Biolith no está en el pack.

Ninguno de los incompatibles está incluido. ScalableLux proporciona `starlight` y declara Phosphor incompatible; Fast Noise declara Moonrise y AntiXray incompatibles. Se comprobó el inventario completo, aliases, `depends`, `breaks` y `conflicts`; no apareció un conflicto cruzado declarado Krypton/C2ME. El [aviso de FastMapCodec con Sodium Extra](https://modrinth.com/mod/fastmapcodec) corresponde a NeoForge, no a estos archivos Fabric.

La resolución real previa a SDL aceptó C2ME + ScalableLux + Fast Noise + Fast Surface + ZConfig y Krypton + C2ME. **No valida la generación, iluminación, conexión a servidores ni guardado durante juego.** Gnetum + ImmediatelyFast requieren inspección visual del HUD; se conserva el perfil que quita solo Gnetum.

Las dependencias de publicación se contrastaron para 30 de los 34 archivos únicos. La API no permitió obtener las publicaciones de Jasione, Better Biome Blend, Fast Surface y FastMapCodec: sus dependencias de publicación permanecen pendientes, aunque las obligatorias de sus JAR y bibliotecas sí se revisaron y pasaron el resolvedor Fabric. Sus SHA-512 ya coinciden con los valores aportados por el usuario desde metadatos oficiales recuperados el **2026-10-06**, comprobados el 2026-10-07 contra las versiones/IDs, JAR locales, pins y exports. Esto cierra los hashes pendientes, pero no aporta las dependencias/listas de compatibilidad de publicación faltantes. [Evidencia SHA-512](research/modrinth-sha512-alpha.4.json). [Evidencia de descargas](research/local-jars-alpha.4.json).

BetterGrassify contiene un salto literal en `description`; el inspeccionador registra una lectura permisiva y el parser real de Fabric aceptó el JAR original sin modificar sus bytes.

[Versiones y recuentos](changelog-alpha.4.md), [inventario completo](validation.json), [alcance del inicio real](research/runtime-alpha.4.json). Historiales de alpha.1/2/3 preservados.
