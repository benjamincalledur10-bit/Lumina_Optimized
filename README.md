# Lumina Optimized

Modpack de optimización **0.1.0-alpha.1** para Minecraft Java **26.3** y Fabric
Loader **0.19.5**. Desarrollo en `modpackdev`. No hay mediciones de rendimiento
ni pruebas de arranque realizadas todavía.

## Instalar

1. Usa un launcher que importe `.mrpack`, como Modrinth App o Prism Launcher.
2. Importa `dist/Lumina-Optimized-0.1.0-alpha.1-core.mrpack` en una instancia nueva.
3. Selecciona Java **25 de 64 bits**, nativo para tu arquitectura. En Apple Silicon,
   usa ARM64. Comprueba la versión efectiva en el launcher.
4. Conserva los ajustes predeterminados. La referencia de memoria es un máximo de
   4 GiB; registra el heap y recolector reales al medir, pues dependen del launcher.

La variante `...-shaders.mrpack` añade Iris. No contiene shader packs ni activa
shaders por defecto. Es una alternativa a Core: importa una de las dos, no ambas
en la misma instancia. Cualquier shader añadido necesita sus propias pruebas.

## Versiones fijas

| Componente | Versión | Lado |
| --- | --- | --- |
| Minecraft Java | 26.3 | Ambos |
| Java | 25 (requisito del runtime, no incluido en `.mrpack`) | Ambos |
| Fabric Loader | 0.19.5 | Ambos |
| Sodium | 0.9.2+mc26.3 | Cliente |
| Lithium | 0.26.2+mc26.3 | Ambos |
| FerriteCore | 9.0.0-fabric | Ambos |
| ImmediatelyFast | 1.17.1+26.3 | Cliente |
| Iris, variante Shaders | 1.11.7+mc26.3 | Cliente |

Sodium incorpora los módulos de Fabric API que necesita; Loader incorpora
MixinExtras 0.5.5 para Lithium. No se añade Fabric API completo ni otra copia de
esas dependencias. Consulta [dependencias](docs/dependencies.md).

## Construir y validar

Necesitas Python **3.11+**, packwiz y conexión a Internet. El commit de packwiz
utilizado está fijado en `scripts/toolchain.json`. Con Go instalado:

```sh
go install github.com/packwiz/packwiz@ef87d964f8cbd52b3b13ea42453ef322290e2b9e
python3 scripts/build.py --packwiz /ruta/al/binario/packwiz
python3 scripts/verify.py
```

`pack/` es la única base. `variants/` contiene únicamente Iris y la descripción
de su variante. El script combina ambos en `.build/` y exporta con packwiz a
`dist/`, incluyendo `SHA256SUMS`. Los metadatos `.pw.toml` fijan ID, URL, hash
SHA-512 y `pin = true`; una actualización requiere modificar las fuentes y
revalidar. No se incluyen configuraciones: se generarán los defaults al arrancar.

`verify.py` comprueba índices, hashes descargados, JAR anidados, requisitos y
conflictos declarados del conjunto fijado, y ambos manifiestos exportados.
Guarda la evidencia en [validation.json](docs/validation.json). La comprobación
es estática, no una ejecución del resolvedor de Fabric ni una importación real.

## Limitaciones

- macOS, Windows y Linux son plataformas objetivo; ninguna está certificada aún.
  La compatibilidad publicada de los mods no garantiza funcionamiento en toda GPU.
- Sodium declara incompatibilidades con OptiFabric, Canvas, VulkanMod y Embeddium;
  ImmediatelyFast documenta incompatibilidad con OptiFine/OptiFabric. No añadas
  renderizadores alternativos a esta base.
- FerriteCore declara incompatibilidad con Hydrogen <=0.3.
- El soporte de shaders requiere validar Iris, GPU, controlador y shader concreto.
- Lithium y FerriteCore en el cliente no optimizan el servidor remoto. Este
  proyecto distribuye principalmente una instancia cliente; los lados se declaran
  correctamente en el paquete, pero no se ha probado una instalación servidor.
- Entity Culling, More Culling, Dynamic FPS y C2ME quedan fuera de esta alpha.
- No se promete un aumento de FPS o reducción de memoria sin mediciones.

Pruebas pendientes y método: [protocolo](docs/benchmarks.md).

## Fuentes

- [Fabric para 26.3](https://fabricmc.net/2026/09/15/263.html)
- [Java 25 y defaults introducidos en 26.1](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-1)
- Publicaciones exactas: [Sodium](https://modrinth.com/mod/sodium/version/bAZQdGpg),
  [Lithium](https://modrinth.com/mod/lithium/version/xS0Q8LSi),
  [FerriteCore](https://modrinth.com/mod/ferrite-core/version/d5ddUdiB),
  [ImmediatelyFast](https://modrinth.com/mod/immediatelyfast/version/3MP9UR23),
  [Iris](https://modrinth.com/mod/iris/version/vTN4NRGW).
- [Exportación packwiz](https://packwiz.infra.link/tutorials/hosting/modrinth/)
- [Formato `.mrpack`](https://support.modrinth.com/en/articles/8802351-modrinth-modpack-format-mrpack)
