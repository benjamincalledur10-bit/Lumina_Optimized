# Configuración e interacciones alpha.5

Solo se incluyen excepciones justificadas y referencias conservadoras. Los ajustes no enumerados usan los defaults de las versiones fijadas. No se exporta `options.txt`.

| Archivo | Decisión y evidencia |
| --- | --- |
| `BBEConfig.json` | `optimize.master=true`; banners y signs desactivados, animaciones de cofres/shulkers/campanas/macetas conservadas. Opciones contrastadas con ConfigBuilder del JAR. |
| `entityculling.json` | Se conserva safeMode, sin tick culling ni solid leaves; esquema revisado en Config. |
| `moreculling.toml` | Serializer real Toml4j. Hojas `DEFAULT`, `useBlockStateCulling=false`, raíces de manglar false, sin LOD ni culling de tres caras. El código devuelve false para customShouldDrawFace con DEFAULT. |
| `cullleaves.json` | `enabled=true`, `cullRoots=false`: Cull Leaves controla hojas; no modifica raíces de manglar. Campos MidnightConfig del JAR e integración Sodium revisados. Puede alterar el aspecto de hojas interiores; revisar en bosque. |
| `iris.properties` | `enableShaders=false`, leído por IrisConfig. No hay shader pack. |
| `lambdynlights.toml` | Default TOML del JAR salvo `mode="off"`. DynamicLightsConfig lee mode y DynamicLightsMode acepta Off; el arranque confirma carga. Activación desde Mods o cambiando mode. |
| `sodium-extra-options.json` | `extra_settings.reduce_resolution_on_mac=false`. Gson usa LOWER_CASE_WITH_UNDERSCORES; se revisó el serializador y el archivo generado en el arranque. Los nombres Java camelCase no son claves JSON válidas aquí. |
| `gnetum.json` | Defaults: ON, 3 passes, HUD máximo 60 FPS, pantallas 20 FPS, `downscale=OFF`, fast FBO blit ON. No limita el render del mundo, pero sí puede espaciar la actualización del HUD. |
| `modernfix-mixins.properties` | Se mantiene `mixin.perf.remove_biome_temperature_cache=false`. Las mismas versiones ModernFix 5.27.20-build.2/Lithium 0.26.2 mantienen el mixin que colisionó en alpha.4; el nuevo arranque reconoce la excepción y no muestra aquella colisión. |
| `c2me.toml` | Referencia conservadora anterior: sin protocolo de distancia extendida y máximo de slider 32, sin fijar la distancia elegida. Se conserva el formato C2ME 3; en runtime reconoce ambas claves. El mensaje «Config version: 6» corresponde a BadOptimizations, no a una migración de C2ME. Publicación experimental alpha.0.90. |
| `servercore/config.yml` | Dynamic, breeding-cap, activation-range, lobotomización y refuerzos/portales/spawners/infested con mobcaps especiales desactivados; XP/items/autosave conservan valores de referencia. Sin categorías personalizadas. |
| `servercore/optimizations.yml` | Solo cache-ticking-chunks, default del autor, permanece true. Reduce-sync-loads y las demás alteraciones quedan false. SnakeYAML integrado y anotaciones ConfKey revisados; main config aún necesita mundo integrado real. |

## Interacciones revisadas

- **Sodium/Iris/Reese’s y complementos:** Iris exige el ID estable de Sodium 0.9.2. Reese’s 2.2.5 y Sodium Extra 0.9.4 cumplen predicados; Sodium Shadowy Path Blocks 8.0.0 incorpora compatibilidad con Iris y exige Sodium. El arranque acepta los mixins de la combinación; la representación dentro del mundo sigue pendiente.
- **Gnetum/ImmediatelyFast/Better Mount HUD:** no hay conflicto obligatorio declarado. Gnetum reparte el HUD en pases; Better Mount HUD modifica su salud, hambre, aire y experiencia/jump. [La declaración pública de compatibilidad Gnetum/ImmediatelyFast](https://modrinth.com/mod/gnetum) enumera versiones anteriores, no constituye una prueba visual de 26.3. Mantener la detección de conflictos de ImmediatelyFast; revisar a caballo y cambiar Gnetum ON/OFF si se congela un elemento.
- **FastQuit/C2ME/Ixeris:** FastQuit 3.1.5 lleva `mc26.2` en el nombre, pero su publicación incluye 26.3 y su predicado acepta ≥26.2/Java 25. Su código `allowMultipleServers()` devuelve false al detectar Ixeris, aunque el default guardado muestre true. No se altera esa protección. No hay breaks C2ME declarados; el guardado, la espera al reabrir y la persistencia requieren una prueba real.
- **ModernFix/C2ME/Lithium:** conservar los cuatro overrides automáticos de ModernFix para C2ME; no forzarlos a true. La excepción de temperatura solo desactiva la implementación duplicada de ModernFix.
- **EMF/ETF/BBE:** [el autor de BBE documenta límites para modelos personalizados](https://github.com/EdeenMC/betterblockentities#mod-compatibility). EMF registró su guarda de más de 64 creaciones y dejó de envolver esos modelos; el código devuelve el ModelPart original, no un crash fatal. BBE permanece activo; no se apaga EMF silenciosamente ni se eleva el límite. No hay packs de modelos externos. Si se añaden, hay que desactivar en BBE las optimizaciones de las entidades concretas que esos packs modifican; no se promete compatibilidad completa.
- **Visuales:** BetterGrassify aplica césped/nieve; Sodium Shadowy Path Blocks modifica sombras de senderos y, por default, puede afectar otras superficies. Skyboxify/EMF/ETF aportan capacidades de recursos personalizados, pero aquí no se suministran packs. LambDynamicLights apagado evita añadir luz dinámica a la referencia. No se fuerzan animaciones reducidas, radios de renderizado ni resolución menor.

Los avisos de clases de Jade/Xaero/VulkanMod/Starlight ausentes corresponden a rutas opcionales de integración, no a dependencias obligatorias añadidas. Los errores de autenticación/Realms del inicio aislado usan un token ficticio: no se prueba una cuenta ni acceso multijugador.

En este Mac ARM64 C2ME no encontró `osx-aarch_64-libc2me-opts-natives-math.dylib` y desactivó automáticamente ese módulo de aceleración nativa. C2ME continuó inicializándose; no se afirma que esa aceleración funcione en macOS.
