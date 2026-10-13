# CurseForge — Lumina Optimized v26.2-beta.1

Archivo: **`Lumina-Optimized-26.2-beta.1-curseforge.zip`**, para **Minecraft 26.2, Java 25 y Fabric Loader 0.19.5**.

## Composición

**48 referencias oficiales: 43 JAR, 3 resource packs y 2 shaders**, con `manifest.json`, `modlist.html` y 13 overrides. Ningún JAR, recurso o shader se distribuye como binario externo en overrides: todos se referencian mediante IDs de proyecto/archivo de CurseForge, con hashes oficiales que coinciden exactamente con Modrinth. Los archivos están disponibles, aprobados y publicados para 26.2; mods Fabric y shaders Iris comprobados. No hay bloqueos de contenido externo ni sustituciones.

**Mandala es la única omisión**, por petición expresa: se retira de ambas listas de recursos en `options.txt`, sin modificar su ZIP. Los otros recursos siguen activos. La variante Modrinth conserva Mandala 2.1 y sus 49 referencias.

Text Placeholder API **3.1.0-beta.1+26.2** se proporciona dentro de ServerCore, con coincidencia exacta de hash contra CurseForge **proyecto 1037459/archivo 8271471**. No se descarga una segunda copia. Se verifican las dependencias obligatorias y los conflictos de los 48 archivos.

Se conservan los ajustes de la beta: **16 chunks de renderizado, 5 de simulación, Prefer Vulkan, nubes OFF, distancia de nubes 26, partículas disminuidas**, perfil Custom, BBE activo/Sodium/Smart, tick culling con modo seguro, shaders y luces dinámicas apagados, reducción de resolución macOS apagada. Todos los overrides coinciden con Modrinth salvo la omisión de Mandala en `options.txt`.

## Importar y reexportar

1. En CurseForge App, elige **Minecraft → Create Custom Profile → Import** y selecciona el ZIP en Descargas.
2. Espera la descarga e instalación de las 48 referencias. Usa **Java 25 ARM64 en Apple Silicon**; comprueba que el perfil muestra Minecraft 26.2/Fabric 0.19.5.
3. Arranca y confirma los tres recursos activos, BBE Sodium/Smart y las preferencias indicadas. Juega 10–15 minutos; explora, guarda, sal y reabre el mundo.
4. Usa **Export Profile** y selecciona los mods, los tres recursos, ambos shaders y la carpeta `config` más `options.txt`. Conserva los shaders apagados. No incluyas mundos, logs ni cuentas del launcher.
5. Entrega el ZIP reexportado para comparar sus IDs, hashes y overrides con esta definición antes de sustituir el archivo publicado.

Este archivo fue generado mediante packwiz y está preparado para importar. **No es todavía una reexportación de CurseForge App**. La importación, descarga e instalación en la app, el juego y la reexportación están pendientes del usuario. Un arranque aislado no prueba esas operaciones.

## Reproducir la exportación

```sh
python 3 scripts/export_curseforge_262.py --packwiz .tools/bin/packwiz
python 3 scripts/export_curseforge_262.py --verify-only
```

[Mappings e IDs](curseforge-mapping.json) · [Metadatos oficiales](curseforge-publications.json) · [Validación](validation-curseforge.json) · [Versiones](versions.md).

Arranque real aislado de 45 segundos en macOS ARM64/Java 25 con los mismos bytes y overrides del ZIP: Vulkan, 166 IDs y tres recursos cargados; ajustes 16/5 y BBE Sodium/Smart conservados. No sustituye la importación o reexportación en la app. [Runtime](runtime-curseforge.json).
