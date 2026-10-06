# Lumina Optimized

**0.1.0-alpha.2**, paquetes locales de prueba en `modpackdev`.
Minecraft Java **26.3**, Java **25 de 64 bits**, Fabric Loader **0.19.5**.
No hay mediciones de rendimiento ni pruebas de arranque realizadas.

## Instalar

Importa un `.mrpack` de `dist/` en una instancia nueva de Modrinth App o Prism
Launcher. Selecciona Java 25 nativo para la arquitectura del equipo (ARM64 en
Apple Silicon). Comprueba su versión efectiva en el launcher.

- `Lumina-Optimized-0.1.0-alpha.2-core.mrpack`: base con Entity Culling y More Culling configurados de forma conservadora. BBE incluido, **desactivado** para conservar la referencia visual.
- `...-shaders.mrpack`: misma base + Iris, sin shader packs ni shaders activados por defecto.
- `...-c2me.mrpack` y `...-c2me-shaders.mrpack`: Core/Shaders + C2ME experimental para carga/exploración.
- `...-test-packages.zip`: los **16 perfiles**, incluidos controles, cada incorporación aislada y BBE activado experimentalmente. Extrae e importa un `.mrpack`, no el ZIP completo.

Mantén resolución, calidad visual, distancias y ajustes del mundo iguales a la
referencia. No se incluye `options.txt` ni ajustes de Sodium que los cambien.
Para comparar BBE activo, revisa primero las limitaciones visuales indicadas abajo.

## Versiones fijadas

| Mod | Versión |
| --- | --- |
| Sodium | 0.9.2+mc26.3 |
| Lithium | 0.26.2+mc26.3 |
| FerriteCore | 9.0.0-fabric |
| ImmediatelyFast | 1.17.1+26.3 |
| Entity Culling | 1.11.2 |
| More Culling | 1.9.0 |
| Better Block Entities | 1.3.9+mc26.3 |
| Fabric API | 0.161.0+26.3 |
| Cloth Config | 26.3.159+fabric |
| Iris, variante Shaders | 1.11.7+mc26.3 |
| C2ME, solo ensayos | 0.4.2-alpha.0.89+26.3 |

IDs, URLs, hashes SHA-512, lado de instalación y `pin = true` están en los
metadatos packwiz. Se verifican también JAR anidados. Dynamic FPS sigue fuera.

## Construir y validar

Necesitas Python **3.11+**, packwiz y conexión a Internet. Para validar, un JDK
**17+** con `java`, `javac` y `javap`; para jugar y compilar Sodium, Java **25**.
El commit de packwiz se fija en `scripts/toolchain.json`.

```sh
go install github.com/packwiz/packwiz@ef87d964f8cbd52b3b13ea42453ef322290e2b9e
python3 scripts/build.py --packwiz /ruta/al/binario/packwiz
python3 scripts/verify.py
python3 scripts/test_static.py
```

`pack/` es la única base. `variants/profiles.json` elimina/añade mods y activa
BBE únicamente para ensayos. Los archivos temporales se generan en `.build/`.
`dist/SHA256SUMS-0.1.0-alpha.2` cubre todos los `.mrpack` nuevos; alpha.1 se conserva.
Los bins, staging y paquetes se excluyen de Git.

La validación genera [validation.json](docs/validation.json). Usa el parser de
versiones de Fabric Loader 0.19.5 y comprueba candidatos anidados, configuraciones,
índices, descargas y exportaciones. **No ejecuta el resolvedor completo de Fabric,
los mixins ni Minecraft.** Un ZIP válido no demuestra arranque o mejores FPS.

## Decisiones y limitaciones

- Entity Culling conserva `safeMode` y desactiva tick culling para mantener animaciones. More Culling desactiva LOD, culling de tres caras y modos agresivos.
- BBE puede ampliar visibilidad y alterar el tratamiento de animaciones/texto. Se incluye apagado en Core/Shaders; los perfiles `bbe`, `bbe-shaders`, `core-bbe-enabled` y `shaders-bbe-enabled` permiten evaluarlo activo con advertencia de paridad visual pendiente.
- C2ME es alpha. Mantener distancias iguales; registrar el estado de su módulo `notickvd`. El `.mrpack` no impone argumentos JVM.
- macOS, Windows y Linux son objetivos, aún sin certificación de arranque, estabilidad o shaders. No añadir OptiFine/OptiFabric, Canvas, VulkanMod ni otros renderizadores alternativos.
- No se promete mejora de rendimiento. Alpha.1 tampoco tuvo mediciones: su historial declara esa ausencia explícitamente.
- La mejora propia de presupuesto de uploads es **un parche de investigación**, no un mod incluido. Requiere compilar el fork para que su flag JVM funcione.

Detalles: [matriz y compatibilidad](docs/alpha.2.md),
[opciones y justificación](docs/configuration-alpha.2.md),
[pruebas reproducibles](docs/benchmarks.md),
[hipótesis propia y parche](docs/research/sodium-upload-budget.md),
[historial alpha.1](docs/history/alpha.1/measurements.json).

## Fuentes

Las publicaciones exactas y el código fijado están enlazados en los documentos.
[Fabric para 26.3](https://fabricmc.net/2026/09/15/263.html),
[requisito Java 25](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-1),
[exportación packwiz](https://packwiz.infra.link/tutorials/hosting/modrinth/),
[formato `.mrpack`](https://support.modrinth.com/en/articles/8802351-modrinth-modpack-format-mrpack).
