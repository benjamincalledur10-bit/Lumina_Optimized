# Alpha.3: matriz de ensayo

Estado inicial: `modpackdev`, limpio, HEAD `35ddfc4` (alpha.2). Publicación prevista: tag `v0.1.0-alpha.3` en `modpackdev`; notas en `releases/v0.1.0-alpha.3.md`. Minecraft 26.3 / Java 25 / Loader 0.19.5; nueve mods base sin actualizar.

**Referencia: alpha.2 `core-bbe-enabled`**, no alpha.2 Core publicado con BBE apagado. El perfil nuevo `baseline` conserva los mismos nueve JAR y overrides de esa referencia; el identificador del pack pasa a alpha.3. Todos los perfiles nuevos tienen BBE activo. Esto no certifica paridad de BBE con vanilla.

## Paquetes

Nombre completo: `dist/Lumina-Optimized-0.1.0-alpha.3-<perfil>.mrpack`. La columna JAR cuenta descargas externas, no módulos anidados.

| Perfil | JAR | Contenido |
| --- | ---: | --- |
| `baseline` | 9 | Referencia alpha.2 + BBE activo |
| `bad` | 10 | Referencia + BadOptimizations |
| `resourceful-control` | 10 | Referencia + Resourceful Config solamente |
| `structure` | 11 | Referencia + SLO y Resourceful Config |
| `zconfig-control` | 10 | Referencia + ZConfig solamente |
| `fastnoise` | 11 | Referencia + Fast Noise y ZConfig |
| `dependencies` | 11 | Referencia + ambas bibliotecas |
| `core` | 14 | Referencia + los tres candidatos y ambas bibliotecas |
| `shaders` | 15 | Core + Iris |
| `baseline-shaders` | 10 | Referencia + Iris |
| `baseline-noif` | 8 | Referencia sin ImmediatelyFast |
| `gnetum` | 10 | Referencia + Gnetum |
| `gnetum-noif` | 9 | Referencia + Gnetum, sin ImmediatelyFast |
| `gnetum-shaders` | 11 | Referencia + Gnetum + Iris |
| `c2me` | 10 | Referencia + C2ME experimental |
| `c2me-all` | 15 | Core + C2ME experimental |
| `c2me-shaders` | 16 | Shaders + C2ME experimental |

El ZIP `...-test-packages.zip` reúne los 17 paquetes y SHA256SUMS; extraer e importar un solo `.mrpack`. Core/Shaders contienen candidatos, no son una recomendación de rendimiento demostrado. Gnetum no está en Core/Shaders. C2ME no está en Core/Shaders.

## Incorporaciones fijadas con packwiz

Se usó `packwiz modrinth add --project-id <id> --version-id <id> -y` en staging. Se conservaron solo los seis metadatos nuevos en `variants/`, se fijaron con `pin=true` y se mantuvo Fabric API 0.161.0+26.3 de la base. No se editaron JAR de terceros.

- [BadOptimizations 2.4.1](https://modrinth.com/mod/badoptimizations/version/Sp0ctspw).
- [Structure Layout Optimizer 1.1.4+26.3-fabric](https://modrinth.com/mod/structure-layout-optimizer/version/crWm7jXS).
- [Resourceful Config 6.0.1](https://modrinth.com/mod/resourceful-config/version/IFB0XCI9).
- [Fast Noise 1.1.1+26.3](https://modrinth.com/mod/zfastnoise/version/cCGI5KLE).
- [ZConfig 1.0.0+26.x](https://modrinth.com/mod/zconfig/version/tsgt79sG).
- [Gnetum 4.6.3+26.3-fabric](https://modrinth.com/mod/gnetum/version/F4CsYAnb).

- BadOptimizations: optimizaciones de trabajo/cachés del cliente, con defaults del autor. Requiere Loader >=0.18.4 y MC >=26.3. Sus exclusiones internas para otros mods no detectan nombres presentes en esta base; esto no elimina conflictos de mixins no declarados. Evaluar cámara fija, cambios de luz/cielo/FOV y rutas pregeneradas.
- SLO: trabajo de distribución de piezas de estructuras; requiere Loader >=0.19.5, Java >=25, Fabric API y Resourceful Config. No necesita Sodium/Iris directamente. Se fija la deduplicación desactivada y se comparan estructuras generadas, además del tiempo de generación.
- Fast Noise: modifica etapas de biomas/ruido de generación. Requiere Loader >=0.19.5, Java >=25, MC ~26.3 y ZConfig >=1.0.0+26.x. Declara `breaks` para `moonrise` y `antixray`, también incompatibles en Modrinth. Recomienda C2ME, pero no lo exige. Probar Overworld/Nether/End y biomas/bloques; no deducir ganancias de FPS de un tiempo de generación.
- Resourceful Config 6.0.1 tiene publicación Fabric 26.3 y no añade dependencias externas nuevas. ZConfig 1.0.0+26.x declara Java >=25 y Loader >=0.19.3; su publicación incluye 26.3. Ninguna biblioteca queda en `baseline`.

No hay exclusión declarada de Sodium 0.9.2 ni Iris 1.11.7 en estos JAR/publicaciones. Los requisitos del conjunto pasan la comprobación estática; carga de mixins, interacción visual y estabilidad de esa combinación permanecen pendientes.

## Gnetum e ImmediatelyFast

Gnetum requiere Fabric API, Loader >=0.16.0 y MC >=26.3. Distribuye actualizaciones del HUD entre cuadros y las limita: puede bajar su frecuencia aunque el mundo siga renderizando a más FPS. Se deja separado, con defaults y sin downscale. No se incluye como mejora de calidad idéntica.

La [documentación del autor](https://modrinth.com/mod/gnetum) declara compatibilidad con ImmediatelyFast para 1.20.1, 1.21.1 y 1.21.11; no certifica 26.3. En el [código fijado 4.6.3](https://github.com/decce/gnetum/tree/307d4ba0d262b91cdbcd3909bb4269251311ea3c), `versions/26.3-fabric/gradle.properties` no define `deps.immediatelyfast`; el helper está condicionado por esa dependencia. El JAR publicado revisado no contiene referencias de clases a ImmediatelyFast. No se encontró un `breaks/conflicts` entre ambos, pero eso no prueba interacción correcta.

Comparación 2×2: `baseline` / `baseline-noif` / `gnetum` / `gnetum-noif`. Para Iris: `baseline-shaders` contra `gnetum-shaders`. Comprobar capas, texto, hotbar, corazones, chat, inventario, cambios de escala GUI y HUD tras F1/resize; medir respuesta y cadencia del HUD por separado de FPS del mundo. No cambiar la config de ImmediatelyFast para ocultar un conflicto.

## Historial y estado

`docs/history/alpha.2/` conserva README, matriz, protocolo, dependencias, validación, estado original y checksums. El usuario informa mediciones con BBE activo; no se recibieron valores ni archivos crudos. El informe original sin mediciones realizadas por el agente se preserva como histórico, no se reescribe como un resultado nuevo.

No existen mediciones de alpha.3. Las validaciones estáticas y pruebas pendientes están en [validation-alpha.3.md](validation-alpha.3.md).
