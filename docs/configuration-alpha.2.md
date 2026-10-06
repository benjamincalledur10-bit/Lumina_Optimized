# Configuraciones de alpha.2

Solo se guardan opciones reales de las versiones fijadas. Las opciones omitidas
conservan sus defaults. No se incluye `options.txt` ni una configuración de Sodium
que cambie resolución, render/simulation distance, entity distance o calidad.
Estas decisiones priorizan la referencia visual; no son optimizaciones medidas.

## Entity Culling 1.11.2 — `config/entityculling.json`

Fuente fijada: [Config.java](https://github.com/tr7zw/EntityCulling/blob/ae786c8921de5ea52c06481dfa47180e42bbd54d/EntityCulling-Versionless/src/main/java/dev/tr7zw/entityculling/versionless/Config.java).

- `configVersion = 9`: evita migraciones de esquemas antiguos.
- `safeMode = true`: conserva extracción de datos segura; no mueve accesos al mundo a otro hilo.
- `tickCulling = false`: se evalúa ocultación de renderizado sin reducir ticks/animaciones del cliente.
- `solidLeaves = false`, `forceDisplayCulling = false`: no tratar hojas transparentes como paredes ni forzar culling de displays.
- `renderNametagsThroughWalls = true`, `blockEntityFrustumCulling = true` y ambos `skip* = false`: valores predeterminados explícitos.
- No se vacían las listas de excepciones: se mantienen las inicializadas por el mod, incluida `minecraft:beacon`. `tracingDistance`, `captureRate`, `sleepDelay` y `hitboxLimit` conservan defaults.

Falta comprobar oclusión al girar la cámara, balizas, displays, cofres animados y
sombras con Iris. Un resultado de compatibilidad de metadatos no asegura sombras
correctas. La tecla debug configurable del mod permite comparar culling; para
mediciones formales se usan instancias separadas.

## More Culling 1.9.0 — `config/moreculling.json`

Fuente fijada: [MoreCullingConfig.java](https://github.com/fxmorin/moreculling/blob/23e0f29f0f6b146916bd293a79e8fafcbba596af/common/src/main/java/ca/fxco/moreculling/config/MoreCullingConfig.java).

- `version = 1`: esquema actual; evita la conversión histórica de rangos cuadrados.
- `useItemFrameLOD = false`, `useItemFrame3FaceCulling = false`: no simplificar objetos con la distancia.
- `leavesCullingMode = "DEFAULT"`, `includeMangroveRoots = false`: sin modos agresivos de hojas.
- `rainCulling = false`, `signTextCulling = false`, `endGatewayCulling = false`: conservar lluvia, texto y portal para revisión visual.
- `useBlockStateCulling = false`, `useOnModdedBlocksByDefault = false`: no combinar culling agresivo de modelos con geometría generada por BBE antes de probarlo.
- `useCustomItemFrameRenderer = true`, `itemFrameMapCulling = true`, `paintingCulling = true`: evaluar caras ocultas de marcos/mapas/cuadros; requieren prueba visual con transparencias y sombras.
- `enableSodiumMenu = true`: permite inspección desde Sodium sin añadir Mod Menu.

No se configura un supuesto límite de FPS ni se bajan distancias. La ganancia
potencial se limita a las funciones que quedan activas y debe medirse.

## Better Block Entities 1.3.9 — `config/BBEConfig.json`

El formato real usa arrays `{ "option": ..., "value": ... } bajo
`bbe.config.storage.main`, no claves booleanas planas. Se revisaron
[ConfigBuilder](https://github.com/ceeden/betterblockentities/blob/7ecbd75b8f893f7b9912c76fa3eab142a9264bfd/common/src/main/java/betterblockentities/client/gui/config/builder/ConfigBuilder.java)
y [BBEConfig](https://github.com/ceeden/betterblockentities/blob/7ecbd75b8f893f7b9912c76fa3eab142a9264bfd/common/src/main/java/betterblockentities/client/gui/config/BBEConfig.java).

**Core/Shaders contienen BBE con `optimize.master = false`.** Su renderizador
híbrido puede mostrar bloques entidad a distancia de terreno; no ofrece una
opción general que garantice igual distancia visual que vanilla. Su checker de
animación inmediata tiene un umbral interno de 20 bloques. Activarlo y declarar
paridad de distancias/animaciones sin pruebas incumpliría la referencia.

Los perfiles `bbe`, `bbe-shaders`, `core-bbe-enabled` y `shaders-bbe-enabled`
cambian solamente `optimize.master` a `true` sobre la configuración compartida.
Son **ensayos experimentales**: no se certifica paridad visual global.

Para esos ensayos se mantienen `animation.chest/shulker/bell/decoratedpot = true`,
`misc.shademode = 1` (VANILLA), `misc.banner_graphics = 1` (FANCY),
`misc.christmas_chest = true` y `misc.sign_text = true`. Se desactiva
`optimize.banner`: el modelo horneado utiliza una pose fija. Se desactiva
`optimize.sign`: evita sustituir el tratamiento de distancia del texto por el
default propio de 16 bloques. `misc.sign_text_culling = false` y
`misc.update_scheduler = 0` (FAST) evitan añadir otra variable de prueba.

Comparar primero cofres/shulkers/campanas/macetas cercanos y animados; después
revisar visibilidad a mayor distancia, geometría, sombras y modelos. Si no hay
paridad, sus FPS no cuentan como mejora equivalente. Desactivar master y reiniciar
restaura el control. No se llama "beneficio BBE" a la mera presencia del JAR.

## C2ME — solo variantes de prueba

Versión `0.4.2-alpha.0.89+26.3`; contiene sus módulos y bibliotecas anidados.
Se revisaron `ConfigSystem` y `client.uncapvd.common.Config` con `javap` del JAR
publicado para comprobar el esquema y claves, además de sus metadatos.

`config/c2me.toml` usa `version = 3`,
`clientSideConfig.modifyMaxVDConfig.maxViewDistance = 32` y
`enableExtRenderDistanceProtocol = false`. El máximo del menú no establece la
distancia efectiva; mantener render 12 y simulación 8 en el ensayo existente.
Los demás valores, paralelismo y módulos conservan sus defaults.

C2ME incluye `notickvd`; para aislar la exploración puede desactivarse con la
propiedad JVM real `-Dcom.ishland.c2me.notickvd.disable=true`. Registrar su estado
en cada ensayo y no mezclar resultados. `.mrpack` no impone argumentos JVM:
si se usa ese control, debe configurarse explícitamente en el launcher.

El mod modifica carga/generación de chunks del servidor integrado, no el mismo
pool que reconstruye mallas en Sodium. Debe comprobarse competencia de CPU,
memoria, MSPT y latencia visual, no solo chunks/s. No se desactivan detectores
de errores de concurrencia ni se habilitan distancias ampliadas.

## Qué se validó

Los nombres de opciones se contrastaron con código fijado y con los campos/
strings del bytecode de los JAR exactos. Los JSON/TOML se parsean y sus bytes
se cotejan dentro de cada exportación. Queda pendiente comprobar que los mods
los carguen y conserven los valores efectivos al arrancar Minecraft.
