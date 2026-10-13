## Lumina Optimized v26.2-beta.1

First beta for **Minecraft 26.2, Java 25 and Fabric Loader 0.19.5**.

- **35 main mods, 7 external libraries and PolyTone: 43 JARs**, with **Sodium 0.9.2 and Iris 1.11.4**.
- Defaults: **render distance 16, simulation distance 5, Prefer Vulkan, clouds OFF, cloud distance 26 and decreased particles**. Custom graphics preset preserves these settings. Resolution and FPS limits are not set by the pack.
- **BBE enabled, Sodium shading and Smart update scheduler**. Entity tick culling enabled with safe mode. Shaders and dynamic lights start disabled; macOS resolution reduction remains disabled.
- **Modrinth:** 4 enabled resource packs, including original Mandala 2.1, plus 2 optional Lumina shaders; 49 references.
- **CurseForge:** same mods, configs and shaders, with Mandala omitted; 3 enabled resources and 48 official project/file references. No external binaries or silent replacements.

### Validation and limitations

Dependencies, nested providers, official hashes, declared conflicts, configuration keys and both exports checked. Isolated 45-second macOS ARM64/Java 25 startup and resource reload checked; requested preferences retained and Vulkan initialized. These checks are separate from gameplay and launcher import.

The user supplied a screenshot showing 318 FPS at 1920×1200 with Vulkan on an Apple M4. This is an observation of one scene, not a controlled performance comparison or FPS guarantee.

**CurseForge App import/install and re-export remain pending.** Extended gameplay, save/reopen, both shaders and Windows/Linux tests remain pending. C2ME is experimental. EMF model-recreation warnings remain documented. Mandala 2.1 uses a manually accepted legacy format in Modrinth; full GUI appearance on 26.2 remains unverified.

### Installation

Import **`Lumina-Optimized-26.2-beta.1.mrpack`** into a new Modrinth App/Prism instance, or **`Lumina-Optimized-26.2-beta.1-curseforge.zip`** into CurseForge App, using **Java 25** (ARM64 on Apple Silicon). The CurseForge ZIP is a packwiz export prepared for import and subsequent re-export in the app.

[Versions](https://github.com/benjamincalledur10-bit/Lumina_Optimized/blob/v26.2-beta.1/docs/editions/26.2/versions.md) · [Validation](https://github.com/benjamincalledur10-bit/Lumina_Optimized/blob/v26.2-beta.1/docs/editions/26.2/validation.md) · [CurseForge import/export](https://github.com/benjamincalledur10-bit/Lumina_Optimized/blob/v26.2-beta.1/docs/editions/26.2/curseforge.md).
