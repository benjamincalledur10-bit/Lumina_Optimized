# Lumina Optimized v26.2-beta.1

Primera beta para **Minecraft 26.2, Java 25 y Fabric Loader 0.19.5**, preparada localmente en `26.2dev`.

## Cambios desde alpha.1

- Activa **Entity Culling tick culling** (`tickCulling=true`), conservando **modo seguro** (`safeMode=true`). Es el único ajuste de mods modificado; las demás claves y las otras 11 configuraciones se conservan.
- Conserva **35 mods principales, 7 bibliotecas externas y PolyTone: 43 JAR**, con **Sodium 0.9.2 e Iris 1.11.4**, las mismas versiones, URLs y hashes oficiales de alpha.1. No se añaden ni retiran mods.
- Conserva **4 resource packs activados** y **2 shaders Lumina instalados y apagados**: **49 referencias**, 13 overrides. Mandala 2.1 conserva su archivo oficial sin modificar; se incluye únicamente en Modrinth por petición expresa, con su formato antiguo aceptado. Su apariencia en todas las pantallas sigue sin verificarse; para CurseForge se omite.
- **BBE activo**, luces dinámicas apagadas, resolución de macOS sin reducción. Distancias, calidad, animaciones y límite de FPS quedan en manos del usuario. ServerCore sigue sin cambios automáticos de distancias, mobcaps o comportamiento.
- Conserva la corrección de **ModernFix/Lithium**, la configuración de hojas sin superposición y Gnetum con downscale apagado.
- Archiva la definición y evidencia de alpha.1; conserva su `.mrpack`, las otras ediciones, los cambios locales previos, tags y releases.

## Validación y pruebas pendientes

- Siete grupos estáticos comprobados: publicaciones/hashes, JAR y dependencias integradas, dependencias externas, conflictos declarados, configuraciones, packwiz y exportación. Comparación con alpha.1: las 49 referencias, `options.txt` y las otras 11 configuraciones permanecen iguales.
- Comprobación real aislada de **45 segundos en macOS ARM64/Java 25**: arranque y recarga de los cuatro recursos. Se verifica que tick culling y modo seguro permanecen activados tras el inicio. No incluye entrada a un mundo, guardado ni pruebas de rendimiento.
- **EMF conserva avisos de recreación excesiva de modelos**, también presentes en la base. BBE/EMF/Fresh Animations, atriles, criaturas/HUD, apariencia de Mandala, ambos shaders, guardado/reapertura y sesiones largas requieren prueba de juego. C2ME sigue siendo experimental. Windows/Linux pendientes.
- El usuario reportó **117 FPS OpenGL y 147 FPS Vulkan, sin reducir resolución en macOS**, para alpha.1. Son observaciones de su equipo, no un benchmark controlado ni una prueba del nuevo ajuste. **No se afirma una ganancia de FPS de beta.1.**

## Instalación y comparación

Importa `Lumina-Optimized-26.2-beta.1.mrpack` desde Descargas en una instancia nueva de Modrinth App o Prism Launcher, con **Java 25 ARM64 en Apple Silicon**. Juega 10–15 minutos, revisa criaturas y guarda/reabre el mundo.

Para comparar, cambia únicamente `tickCulling` a `false` en la configuración de Entity Culling y reinicia. Mantén el modo seguro y los mismos ajustes. Si aparecen anomalías de animación, vuelve a desactivarlo.

[Versiones](versions.md) · [Validación](validation.md) · [Alpha archivada](history/alpha.1/changelog.md). Todo local, sin commit, push ni publicación.
