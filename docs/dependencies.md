# Dependencias de la alpha

Se inspeccionan los JAR descargados por hash, no solo la lista de Modrinth.
La evidencia completa se genera con `python3 scripts/verify.py` en `validation.json`.

| Mod | Requisitos externos declarados en el JAR |
| --- | --- |
| Sodium 0.9.2 | Minecraft 26.3.x; Loader >=0.16.0; fabric-block-getter-api-v2 `*`, fabric-rendering-fluids-v1 >=2.0.0 y fabric-resource-loader-v0 `*` |
| Lithium 0.26.2 | Minecraft ~26.3; Loader >=0.19.5; MixinExtras >=0.5.5 |
| FerriteCore 9.0.0 | Minecraft >=26.1 <27; Loader >=0.14.21 |
| ImmediatelyFast 1.17.1 | Java >=25; Minecraft 26.3.x; Loader >=0.19.3 |
| Iris 1.11.7 | Loader >=0.12.3; Sodium 0.9.x; Modrinth exige ID bAZQdGpg |

Sodium contiene fabric-api-base, fabric-block-getter-api-v2,
fabric-lifecycle-events-v1, fabric-renderer-api-v1, fabric-rendering-fluids-v1,
fabric-rendering-v1, fabric-resource-loader-v0, fabric-resource-loader-v1 y
fabric-transitive-access-wideners-v1. Sus requisitos transitivos también se revisan.

Loader 0.19.5 contiene `mixinextras-fabric-0.5.5.jar`. Iris contiene los módulos
fabric-api-base y fabric-key-mapping-api-v1, además de bibliotecas ANTLR,
glsl-transformer y jcpp. Una biblioteca sin `fabric.mod.json` se valida como ZIP,
pero no se trata como un mod Fabric.

Sodium e Iris incorporan la misma versión de fabric-api-base. Se acepta esa copia
idéntica como candidato compartido; cualquier duplicado con distinta versión
debe revisarse antes de aprobar una nueva combinación.

La validación está limitada a los predicados presentes en estas versiones y falla
ante formatos no soportados. No analiza bytecode, comportamiento de mixins,
bibliotecas nativas ni todos los casos del resolvedor de Fabric. El arranque real
de ambas variantes sigue siendo obligatorio.

No se requiere Fabric API completo para este conjunto. No se fuerzan opciones
de compatibilidad ni se desactivan optimizaciones.
