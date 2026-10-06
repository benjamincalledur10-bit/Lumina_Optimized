# Configuraciones alpha.3

Los tres archivos `pack/config/` de alpha.2 permanecen byte a byte sin cambios; [justificación anterior](configuration-alpha.2.md). `scripts/profiles.py` transforma únicamente `optimize.master` de BBE a true para todos los perfiles nuevos. Animaciones, banners, signos, resolución, distancias y calidad permanecen como la referencia alpha.2 con BBE activo. No se distribuyen opciones gráficas nuevas.

## Structure Layout Optimizer

`variants/structure_layout_optimizer.jsonc` se copia únicamente cuando SLO está incluido a `config/structure_layout_optimizer.jsonc`:

```json
{"deduplicateShuffledTemplatePoolElementList": false}
```

Se comprobó `SloConfig` del JAR 1.1.4+26.3-fabric, su `@Config("structure_layout_optimizer")` y `@ConfigEntry` BOOLEAN. Resourceful Config 6.0.1 (`ParsedConfig.getConfigFile` y `Loader.loadConfig`) carga la clave booleana al nivel superior desde `config/<id>.jsonc` (también migra `.json` antiguo). Es JSON válido dentro del formato JSONC; no es una ruta o clave inventada.

La [opción del autor](https://modrinth.com/mod/structure-layout-optimizer) puede alterar la distribución para una misma semilla. Se mantiene false, igual al default inspeccionado. Eso no sustituye las pruebas de paridad de todas las otras transformaciones de generación.

## Otros candidatos

No se añaden overrides de BadOptimizations, Fast Noise, ZConfig o Gnetum: se mantienen defaults de las publicaciones fijadas. Tras el primer arranque guardar los archivos efectivos que generen, sus hashes y los logs; comprobar que no existan configs heredadas de otra instancia.

Fast Noise 1.1.1+26.3 (`FastNoiseConfigEntries` inspeccionado): `perf.biomes.end=true`, `perf.biomes.tree=false`, `perf.biomes.fixed=true`; mixins `perf.biome=true`, `perf.noise=true`; `debug.disable_carve_features_and_entities=false`. End/tree tienen exclusión automática para Biolith. No se activa ese modo debug ni se elimina generación para producir una mejora artificial. Son defaults observados, no mediciones.

Gnetum 4.6.3 (`GnetumConfig` del JAR y fuente fijada): enabled ON, showHudFps ON, downscale OFF, fastFboBlit ON, numberOfPasses 3, maxFps 60 del HUD y screenMaxFps 20. No son límites de FPS del mundo. Registrar mapa efectivo de elementos, opciones y la cadencia observada; tratar la menor actualización temporal como una diferencia de comportamiento, incluso sin downscale.

C2ME conserva `variants/c2me.toml` versión 3 y protocolo de distancia extendida desactivado. No se cambia su configuración ni se impone un flag JVM. Revisar módulo `notickvd`, distancias efectivas, nativos y logs; es experimental.
