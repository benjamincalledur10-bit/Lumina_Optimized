# Variante CurseForge — v1.21.11-beta.1

**Minecraft 1.21.11 · Java 21 · Fabric Loader 0.19.5.** Archivo `Lumina-Optimized-1.21.11-beta.1-curseforge.zip`, exportado con packwiz desde la misma base que el `.mrpack`.

Incluye `manifest.json`, `modlist.html` y 12 overrides de configuración/opciones. **50 referencias oficiales de CurseForge**, sin binarios externos en overrides: 44 JAR (36 principales, 7 bibliotecas y PolyTone), 4 recursos y 2 shaders. Todas las publicaciones se comprobaron para 1.21.11 y el cargador correspondiente; todos los JAR se publican para Fabric. IDs/hashes/nombres/tamaños en [curseforge-mapping.json](curseforge-mapping.json), evidencia oficial de API en [curseforge-publications.json](curseforge-publications.json).

## Mandala: diferencia entre plataformas

Se aplica la sustitución que el usuario aprobó antes para la variante CurseForge, comunicada nuevamente antes de incorporarla en 1.21.11: **Mandala 2.1 → 2.6**, proyecto **664719**, archivo **7564677**, [publicación oficial](https://www.curseforge.com/minecraft/texture-packs/mandalas-gui-dark-mode/files/7564677), publicada para 1.21.9–1.21.11. El original 2.1 no tiene archivo idéntico entre las publicaciones oficiales revisadas. No se incrusta su ZIP para eludir ese requisito ni se elimina el recurso.

Mandala 2.6 tiene SHA-1 `8b38d5c6da5e00f5816f7b2b7bf836655c985748`, tamaño 727411 bytes y formato 75. Frente a 2.1 cambia 14 texturas y elimina dos archivos de tooltip; esta edición visual no fue la usada en la prueba de juego reportada por el usuario. El `.mrpack` conserva **Mandala 2.1**. En el ZIP, `options.txt` cambia solo las dos apariciones del nombre del recurso para mantenerlo activado. Los demás recursos, shaders y todas las configuraciones de mods son idénticos al `.mrpack`.

## Dependencias y validación

Cloth Config **21.11.153+fabric** tiene publicación oficial Fabric/1.21.11 con SHA-1 coincidente con Modrinth. Esta edición no utiliza el archivo snapshot 26.3.159. No se extrapola la situación de 26.3 a esta edición.

CurseForge declara MidnightLib para Cull Leaves y Text Placeholder API para Mod Menu. Se verificaron los bytes integrados contra los archivos oficiales de CurseForge y Modrinth: **MidnightLib 1.9.2** y **Text Placeholder API 2.8.2+1.21.10**; no se añaden JAR duplicados. Dependencias obligatorias y conflictos de catálogo comprobados.

Siete grupos superados: publicaciones/IDs/hashes/compatibilidad, dependencias/conflictos, proveedores integrados, CRC/rutas seguras, manifest completo, configs/recursos y `.mrpack` intacto. [Informe](validation-curseforge.json). BBE activo, tick culling/modo seguro activos, Gnetum ausente, shaders/luces apagados y reducción de resolución de macOS activada por defecto. No se cambia la composición de 26.3.

## Comprobaciones pendientes

El usuario reportó la prueba breve de juego de la composición Modrinth sin problemas; esa evidencia no valida la apariencia de Mandala 2.6 ni la importación en CurseForge. No se garantiza rendimiento, importación o aprobación por moderación.

Para enviar a CurseForge: **importar este ZIP en CurseForge App, comprobar que conserva versiones/recursos y reexportarlo desde esa aplicación**. Es un requisito de su [política de moderación](https://support.curseforge.com/support/solutions/articles/9000197279-moderation-policies); el ZIP de packwiz no se presenta como una exportación ya realizada por la app. Ver también el [formato y requisitos oficiales](https://support.curseforge.com/support/solutions/articles/9000197908-exporting-a-modpack-for-curseforge-project-submission). La comprobación técnica del ZIP sí está terminada; la prueba de importación/reexportación sigue pendiente.

## Reconstrucción

```sh
python3 scripts/edition_12111.py --build --packwiz .tools/bin/packwiz
python3 scripts/export_curseforge_12111.py --packwiz .tools/bin/packwiz
python3 scripts/export_curseforge_12111.py --verify-only
```

La auditoría conserva solo metadatos oficiales públicos, sin claves/headers de API ni URLs de descarga transitorias. La validación de bytes usa URLs oficiales de Modrinth y un enlace público estable del archivo aprobado de Mandala. No se añaden archivos locales al repositorio.

## Arranque de la variante CurseForge — 12 de octubre de 2026

Inicio aislado de **45 segundos en macOS ARM64/Java 21**: 166 IDs iguales a la composición Modrinth, inicialización y recarga terminadas; parada deliberada con SIGTERM (143). **Mandala 2.6 presenta un fallo real:** `pack.mcmeta` declara formato 75 sin los campos obligatorios `min_format` y `max_format`. El juego registra el rechazo de sus metadatos; que su nombre aparezca en la recarga no demuestra que se aplique. Se conserva el archivo oficial sin alterarlo; el ZIP no se considera completamente funcional en sus cuatro recursos hasta resolverlo. No se prueba un mundo ni CurseForge App. Errores de autenticación corresponden a la cuenta aislada sin autenticar. [Registro](runtime-curseforge.json) · [Log](startup-curseforge.log).
