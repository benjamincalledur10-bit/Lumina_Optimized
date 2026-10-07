# Dependencias actuales

La matriz y las publicaciones exactas de alpha.3 están en [alpha.3.md](alpha.3.md).
El reporte [validation.json](validation.json) contiene todos los metadatos
anidados, predicados y candidatos seleccionados para cada perfil.

- Entity Culling requiere **Fabric API completo** y aporta TRansition/TRender.
- More Culling requiere **Cloth Config**, que aporta basic-math. More Culling aporta conditional-mixin.
- BBE exige la publicación exacta de Sodium 0.9.2, igual que Iris 1.11.7 en Modrinth.
- Sodium/Iris siguen incorporando módulos Fabric; el API completo introduce candidatos adicionales con los mismos IDs. Se comparan con la API de versiones de Loader, sin extraer/eliminar/reempaquetar los JAR de sus autores.
- Loader 0.19.5 aporta MixinExtras 0.5.5 para Lithium.
- C2ME contiene c2me-base y sus otros módulos, bibliotecas de concurrencia/configuración y MixinSquared. Solo se añade a perfiles de ensayo.

Se validan hashes del contenedor, CRC de archivos, módulos anidados transitivos,
requisitos, aliases `provides`, incompatibilidades `breaks` y advertencias
`conflicts`. Para módulos con varios candidatos se prueba el más reciente. Si
no satisface el conjunto, la validación falla y requiere revisión; no busca
combinaciones alternativas como el resolvedor SAT completo de Fabric.

Los campos `suggests` no son requisitos obligatorios. La disponibilidad publicada
para 26.3 y los metadatos compatibles no prueban inicialización de mixins, carga
de bibliotecas nativas ni comportamiento de shaders. El juego requiere Java 25;
la inspección estática con JDK 21 no es una prueba de ese runtime.

El reporte de alpha.1 y su explicación original se conservan en
[history/alpha.1](history/alpha.1/dependencies.md). Alpha.1 no necesitaba Fabric
API completo; alpha.2 sí lo incluye por Entity Culling.


## Candidatos alpha.3

- SLO -> Resourceful Config 6.0.1 y Fabric API existente; requiere Java 25 y Loader 0.19.5. Resourceful no exige nuevas descargas externas.
- Fast Noise -> ZConfig 1.0.0+26.x; incorpora `zfastnoise-ocl` 1.0.0-beta.1+26.3. Ese módulo integrado no añade un mod C2ME-OpenCL externo al pack; su presencia no demuestra que exista aceleración OpenCL activa.
- ZConfig -> NightConfig core/toml **3.8.3** integrados. C2ME incluye candidatos **3.6.5** de los mismos IDs. El validador selecciona 3.8.3 en el conjunto por la API de versiones de Loader; que los predicados lo acepten no garantiza compatibilidad binaria o funcional del código C2ME. Revisar arranque y generación en `c2me-all`/`c2me-shaders`.
- BadOptimizations no requiere una biblioteca externa nueva. Gnetum requiere Fabric API existente; no declara incompatibilidad con ImmediatelyFast. No se certifica esa interacción para 26.3.
- AntiXray y Moonrise están excluidos por los `breaks` de Fast Noise y sus incompatibilidades Modrinth. El validador comprueba ambos tipos de metadatos.

Las versiones exactas, requisitos y enlaces de publicación figuran en [alpha.3.md](alpha.3.md). Los JAR anidados se verifican recursivamente sin extraerlos a `mods/`, ni duplicarlos ni reempaquetarlos. Historial alpha.2: [reporte original](history/alpha.2/validation.json).
