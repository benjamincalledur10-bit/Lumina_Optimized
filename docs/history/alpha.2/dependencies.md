# Dependencias actuales

La matriz y las publicaciones exactas de alpha.2 están en [alpha.2.md](alpha.2.md).
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
