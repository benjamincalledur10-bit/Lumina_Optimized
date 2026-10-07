# Validación alpha.4

## Archivos, dependencias y exportaciones

Se continuaron los cambios locales existentes en `modpackdev`, HEAD `46b27a1`. Se conservan los nueve archivos base y las configuraciones previas; `alpha3-reference` reproduce los archivos/overrides de Core alpha.3 con BBE activo. Las versiones de Minecraft, Java y Loader no cambiaron.

Se localizaron los siete JAR en Descargas. Se comprobó ZIP/CRC, `fabric.mod.json`, versiones internas, bibliotecas anidadas, SHA-1/SHA-256/SHA-512 y tamaño. No se modificaron los originales ni se suben al repositorio; los `.mrpack` contienen manifest con URLs oficiales y overrides, sin JAR.

**Contraste de hashes publicados: 34 de 34 archivos únicos.** Para 30 archivos se cuenta con metadatos completos de publicación conservados en caché. Los SHA-512 restantes se contrastaron el **7 de octubre de 2026** con los valores que el usuario recuperó de los metadatos oficiales de Modrinth el **6 de octubre de 2026**. Esta evidencia fue aportada por el usuario; no se presenta como una consulta fresca a la API realizada por el agente.

| Mod / versión | ID de versión | JAR local | Pin packwiz | Exports que lo incluyen |
| --- | --- | --- | --- | --- |
| Jasione 1.0.9+26.1.2-fabric | kbKBk4b3 | Coincide SHA-512 | Coincide | 6 de 6 |
| Better Biome Blend 26.3-1.4.0-fabric | Oag8dQao | Coincide SHA-512 | Coincide | 5 de 5 |
| Fast Surface 1.0.0+26.3 | yOBmJfgG | Coincide SHA-512 | Coincide | 6 de 6 |
| FastMapCodec 1.0.4 | I6Iu1TAV | Coincide SHA-512 | Coincide | 6 de 6 |

Antes de acreditar los hashes se comprobó la identidad de versión/proyecto/archivo de los pins y la versión interna de cada JAR. Better Biome Blend declara internamente 1.4.0, en el archivo Fabric para 26.3. Los originales ya no están en Descargas; se usaron las copias locales verificadas de la caché de descarga, sin alterar los bytes. Las URLs oficiales y SHA-512 de packwiz y `modrinth.index.json` coinciden con la evidencia. **No hay discrepancias ni hashes pendientes. No fue necesario cambiar pins, configuración o paquetes.**

[Evidencia fechada y los cuatro SHA-512 completos](research/modrinth-sha512-alpha.4.json). Para esos cuatro archivos aún falta obtener los **metadatos completos** de la publicación exacta —dependencias y listas de compatibilidad— porque no se proporcionaron en este extracto y la API no fue accesible. Las dependencias obligatorias de los JAR siguen verificadas; la coincidencia del hash no sustituye la revisión del metadato completo.

Se verificaron dependencias obligatorias de todos los `fabric.mod.json`, aliases, predicados de Java/Minecraft/Loader, `breaks`, `conflicts` e incompatibles de las publicaciones disponibles. Placeholder integrado coincide con su publicación; Loader proporciona MixinExtras. Sodium Extra no requiere Sodium Options API. [Inventario y estado por publicación](validation.json), [evidencia local](research/local-jars-alpha.4.json).

More Culling 1.9.0 usa TOML, confirmado en su serializador real y archivo generado. Se añade `moreculling.toml` con los valores conservadores del JSON histórico; el JSON se conserva y el perfil de referencia alpha.3 permanece intacto. En los intentos finales Core y Shaders, el archivo generado confirma que todos esos valores se aplicaron. La comparación con medidas antiguas debe reconocer que entonces se aplicaban defaults por el formato equivocado.

Configuraciones anteriores, SLO false, Iris false y opción ModernFix comprobados contra clases de sus JAR. ServerCore se analizó con `javap`: nombres `ConfKey`, defaults y rutas reales. Los dos YAML pasan el parser **SnakeYAML 2.7 integrado** y controles de comportamiento/distancias/mobcaps desactivados; queda pendiente la lectura completa del config principal al crear el servidor integrado. Async Logger leyó los valores sin filtros y completó los defaults de su archivo en el intento real.

Better Biome Blend usa otra opción de `Options`, `betterBiomeBlendRadius`, cuyo default interno es 14 (29×29). Se distribuye únicamente `version:5023`, `biomeBlendRadius:2` y `betterBiomeBlendRadius:2`: formato de Minecraft 26.3 y mezcla inicial 5×5. Se contrastaron clave/persistencia en `MixinOptions` y el default vanilla 2 en el cliente local 26.3. No se fijan otros ajustes gráficos. Los intentos reales de Core y Shaders leyeron/guardaron ambos radios en 2; la mezcla visual en el mundo sigue pendiente.

**Siete exports packwiz completos**: inventario exacto, IDs/URLs/hashes fijados, tamaños, manifest/dependencias, configuración, CRC, SHA256SUMS y bundle. El exportador falla si packwiz omite una descarga aunque termine con código 0. **17 pruebas estáticas pasaron**, incluyendo referencia histórica, BBE/configs constantes, Iris aislado/apagado, etapas de integración, alternativas, conteos, control de HUD y resolución de dependencias. Los hashes históricos de 2 paquetes alpha.1, 16 alpha.2 y 17 alpha.3 presentes localmente se conservan. Sin mediciones nuevas.

## Inicialización real: alcance limitado

Se ejecutaron Core y Shaders completos en instancias aisladas, con cliente local Minecraft 26.3, Loader 0.19.5 y **Azul Zulu Java 25.0.4.1 ARM64**, usuario offline de prueba. No se leyeron cuentas ni se modificaron mundos/instancias del usuario.

- El resolvedor real aceptó las versiones y enumeró **120 IDs en Core / 124 en Shaders**, incluidos módulos del entorno. Se inicializaron ServerCore y Krypton; Jasione y Async Logger participaron en prelaunch. Esto valida más que una inspección ZIP, pero no todos los mixins que se cargarían en un mundo.
- La corrección `mixin.perf.remove_biome_temperature_cache=false` de ModernFix se leyó; no reapareció el overwrite `getTemperature` con Lithium. Se mantiene el aviso inicial anterior como evidencia. C2ME provoca además cuatro desactivaciones automáticas de ModernFix; se respetan.
- C2ME desactivó automáticamente `natives_math`: falta `osx-aarch_64-libc2me-opts-natives-math.dylib`. No fue la excepción fatal. Se registran avisos de refmaps y clases de integración opcionales, incluido MaterialRuleInterpreter; no se añaden esos proyectos como dependencias obligatorias.
- **Ambos intentos terminan en `Unable to initialize SDL: The video driver did not add any displays`.** La referencia alpha.3 mostró el mismo fallo en la preparación anterior. No hay pantalla disponible en esta sesión; no se llegó al menú ni a un mundo.
- Crash Assistant tampoco pudo preparar su GUI por restricción `sysctl`; consultas a servicios/actualizaciones fallaron por red restringida. No se certifica su funcionamiento normal desde el launcher.

[Evidencia resumida y hashes de logs](research/runtime-alpha.4.json). Logs completos en `.build/runtime-alpha4/<perfil>/`, excluidos de Git. La inspección estática usa JDK 21; los intentos reales usaron Java 25. No se montaron benchmarks adicionales.

## Pendiente en el Mac

| Prueba | Estado |
| --- | --- |
| Importación desde `.mrpack` | Pendiente |
| Menú y entrada al mundo | Bloqueado aquí por SDL; pendiente en el Mac |
| Exploración, iluminación, guardado y reapertura | No ejecutado |
| C2ME + ScalableLux + Fast Noise + Fast Surface + ZConfig | Resolución/prepantalla aceptada; generar y reabrir chunks pendiente |
| Krypton + C2ME | Resolución/inicialización aceptada; mundo y conexión real pendientes |
| ServerCore sin ajuste de distancias/mobcaps/comportamiento | Esquema y YAML comprobados; config principal/servidor integrado pendiente |
| HUD Gnetum + ImmediatelyFast / visuales BBE y mezcla de biomas | Pendiente de inspección visual |
| Estabilidad y fluidez 10–15 min | No ejecutado |
| Shaders activos, Windows y Linux | No ejecutado |
| Hashes de las cuatro publicaciones | VERIFICADOS con evidencia aportada del 2026-10-06 |
| Metadatos completos de esas cuatro publicaciones | Pendiente; el extracto suministra SHA-512, versiones e IDs |

No se presentan FPS, ganancias de memoria o tiempos de generación. Las alternativas conservadoras están exportadas para aislar errores; su funcionamiento en juego tampoco quedó certificado. [Prueba sencilla](benchmarks.md).

## Reproducir

```sh
python3 scripts/build.py --packwiz .tools/bin/packwiz --cache .build/packwiz-cache
python3 scripts/test_static.py
python3 scripts/verify.py
git diff --check
```

Para completar los cuatro metadatos de publicación cuando haya red, ejecutar `python3 scripts/verify.py --require-publications`. Ese modo exige respuestas reales de publicación para todos los pins, sin fallback local; no reemplaza los pins por versiones nuevas. Si los hashes publicados difieren, detener la importación y revisar el archivo antes de continuar.
