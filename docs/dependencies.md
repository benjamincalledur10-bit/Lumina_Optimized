# Dependencias alpha.5

35 principales + 7 bibliotecas externas, 42 descargas. La biblioteca solicitada Text Placeholder API 3.2.0+26.3 se acredita por SHA-512 dentro de Mod Menu y ServerCore. ZConfig 1.0.0+26.x es la única incorporación fuera de la lista objetivo, exigida por Fast Noise 1.1.1+26.3.

Se compararon publicaciones completas de Modrinth (Fabric y game_versions incluyen 26.3), depends/breaks/conflicts/provides de cada fabric.mod.json y todos los JAR anidados declarados. Las dependencias opcionales/recomendadas no se convierten automáticamente en descargas. Minecraft 26.3, Java 25 y Loader 0.19.5 satisfacen los predicados seleccionados. Sin conflictos declarados entre las entradas finales; esto no descarta conflictos visuales o de ejecución.

Bibliotecas integradas: Placeholder API, MidnightLib 1.9.3 (Cull Leaves), Greenlight API (Sodium Extra), LambDynamicLights API, SpruceUI, Pride, Yumi Commons/Foundation, módulos de Fabric API, bibliotecas Kotlin, NightConfig y módulos C2ME, DazzleConf/SnakeYAML de ServerCore y bibliotecas Iris. Las clases NightConfig sombreadas de LambDynamicLights y otras bibliotecas sin fabric.mod.json no reciben un ID de mod adicional ni otra descarga.

Loader aporta MixinExtras 0.5.5; la copia 0.5.4 de ModernFix queda superada. NightConfig compartido de C2ME/ZConfig se selecciona por ID/versión; no se añaden copias externas. Fast Noise integra zfastnoise-ocl; su presencia no confirma ejecución OpenCL. No se añade Sodium Options API.

Conteos integrados: 142 apariciones, 117 IDs distintos, 116 seleccionados estáticamente excluyendo Loader; el arranque real enumera 162 IDs incluyendo plataforma. Los duplicados originales permanecen dentro de los JAR oficiales. El resolvedor estático usa VersionPredicate del Loader y no sustituye su SAT real; el SAT real aceptó el arranque.

Zoomify 2.16.3 evita las dependencias de publicación mezcladas de 2.17.0 universal. FastQuit conserva el nombre mc26.2 y LambDynamicLights integra Yumi Foundation con nombre 26.2; sus publicaciones/predicados permiten 26.3. BetterGrassify requiere lectura permisiva de un control literal en description; el parser real Fabric aceptó el JAR sin alterar sus bytes.

[Versiones/IDs](changelog-alpha.5.md) · [Selección y hashes](research/selection-alpha.5.json) · [Publicaciones completas](research/publications-alpha.5.json) · [Inventario y predicados](validation.json) · [Interacciones pendientes](configuration-alpha.5.md).

## Beta 26.3-beta.1

La selección anterior se conserva. Se añade PolyTone 26.3-6.8.6-alpha para Fullbright: Fabric API >=0.162.0+26.3 y Loader >=0.19.3 satisfechos. Sus tres bibliotecas integradas se resuelven con Loader 0.19.5 sin JAR duplicados. Translations requiere Sodium; Fresh Animations requiere EMF/ETF según su descripción, ya instalados. Mandala no tiene publicación 26.3. Véanse [changelog](changelog-26.3-beta.1.md), [selección](research/selection-26.3-beta.1.json) y [recursos](research/resourcepacks-26.3-beta.1.json).
