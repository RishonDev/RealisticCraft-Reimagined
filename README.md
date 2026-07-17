# RealisticCraft Reimagined

A Modrinth-format modpack (`.mrpack`) built from the RealisticCraft PrismLauncher instance, updated for Minecraft 26.2 / Fabric Loader 0.19.3. See [MIGRATION.md](MIGRATION.md) first for *why* the mod list looks the way it does (what got replaced, what has no update yet, what got added).

## Variants

- **RealisticCraft-Reimagined-PhysicsOn.mrpack** — full pack, 53 mods, includes Physics Mod (3.1.45).
- **RealisticCraft-Reimagined-PhysicsOff.mrpack** — 52 mods, identical pack with Physics Mod removed and its config dropped, for better performance or a vanilla-feel physics experience.

Both variants bundle a resource pack ([3D Default](https://modrinth.com/resourcepack/3d-default) v1.15.0, GPL-3.0) and a shader pack (`Bliss v2.1.2`, a Chocapic13 edit) directly — but **disabled by default**. They're there to opt into from the in-game resource pack / Iris shader menus, not applied automatically (`options.txt` only activates `vanilla`, and the packaged `iris.properties` forces `enableShaders=false` regardless of what's active on the source instance).

The resource pack was originally the "RealisCraft [Demo]" pack that ships with the source instance, but that's an unlicensed demo/trial pack not cleared for redistribution — swapped for 3D Default instead, which is explicitly GPL-3.0 licensed (its LICENSE file is bundled in the pack itself, confirmed) and adds real 3D block geometry rather than flat textures, so it still looks distinctly non-vanilla with or without the shader active.

## Installing

Import the `.mrpack` file directly in PrismLauncher (Add Instance → Import) or the Modrinth App. Mods are fetched from Modrinth on first launch; the custom-built ToughAsNails jar (not published anywhere), the bundled resource/shader packs, and a handful of config files are bundled directly in the pack as overrides.

## Full mod list (physics-on variant; physics-off omits only Physics Mod)

| File | Version | Modrinth page |
|---|---|---|
| AmbientSounds_FABRIC_v6.3.6_mc26.2.jar | 6.3.6 | https://modrinth.com/mod/fM515JnW |
| c2me-fabric-mc26.2-0.4.2-alpha.0.18.jar | 0.4.2-alpha.0.18+26.2 | https://modrinth.com/mod/VSNURh3q |
| CameraOverhaul-v2.0.6-fabric+mc[1.21.11-plus].jar | 2.0.6-fabric+mc.1.21.11-plus | https://modrinth.com/mod/m0oRwcZx |
| cicada-lib-0.15.2+26.2.jar | 0.15.2+26.2 | https://modrinth.com/mod/IwCkru1D |
| cloth-config-26.2.155.jar | 26.2.155+fabric | https://modrinth.com/mod/9s6osm5g |
| CreativeCore_FABRIC_v2.14.16_mc26.2.jar | 2.14.16 | https://modrinth.com/mod/OsZiaDHq |
| do_a_barrel_roll-fabric-3.8.4+26.2.jar | 3.8.4+26.2-fabric | https://modrinth.com/mod/6FtRfnLg |
| drippyloadingscreen_fabric_3.1.4_MC_26.2(1).jar | 3.1.4-26.2-fabric | https://modrinth.com/mod/v3CYg2V9 |
| dynamic-fps-3.11.9+minecraft-26.2.0-fabric.jar | 3.11.9 | https://modrinth.com/mod/LQ3K71Q1 |
| dynamiccrosshair-9.13+26.2-fabric.jar | 9.13+26.2-fabric | https://modrinth.com/mod/ZcR9weSm |
| entityculling-fabric-1.10.5-mc26.2.jar | 1.10.5 | https://modrinth.com/mod/NNAgCjsB |
| fabric-api-0.155.0+26.2.jar | 0.155.0+26.2 | https://modrinth.com/mod/P7dR8mSH |
| FallingTree-26.2-25.jar | 26.2-26.2.0.3 | https://modrinth.com/mod/Fb4jn8m6 |
| fancymenu_fabric_3.9.8_MC_26.2(1).jar | 3.9.8-26.2-fabric | https://modrinth.com/mod/Wq5SjeWM |
| ferritecore-9.0.0-fabric.jar | 9.0.0-fabric | https://modrinth.com/mod/uXXizFIs |
| firstperson-fabric-2.7.2-mc26.2.jar | 2.7.2 | https://modrinth.com/mod/H5XMjpHi |
| ForgeConfigAPIPort-v26.2.1-mc26.2.x-Fabric.jar | 26.2.1 | https://modrinth.com/mod/ohNO6lps |
| GlitchCore-fabric-26.2-26.2.0.0.0.jar | 26.2.0.0.0 | https://modrinth.com/mod/s3dmwKy5 |
| ice_boat_nerf-1.3.1+MC26.1-26.2.x.jar | 1.3.1+MC26.1-26.2.x | https://modrinth.com/mod/Udjno5eL |
| ImmediatelyFast-Fabric-1.16.2+26.2.jar | 1.16.2+26.2-fabric | https://modrinth.com/mod/5ZwdcRci |
| iris-fabric-1.11.2+mc26.2.jar | 1.11.2+26.2-fabric | https://modrinth.com/mod/YL57xq9U |
| Ixeris-4.5.2+26.2-fabric.jar | 4.5.2+26.2-fabric | https://modrinth.com/mod/p8RJPJIC |
| konkrete_fabric_1.11.1_MC_26.2(1).jar | 1.11.1-26.2-fabric | https://modrinth.com/mod/J81TRJWm |
| lithium-fabric-0.25.2+mc26.2.jar | mc26.2-0.25.2-fabric | https://modrinth.com/mod/gvQqBUqZ |
| lithostitched-1.7.13-fabric-26.2.jar | 1.7.13-fabric-26.2 | https://modrinth.com/mod/XaDC71GB |
| melody_fabric_1.0.17_MC_26.2(1).jar | 1.0.17-26.2-fabric | https://modrinth.com/mod/CVT4pFB2 |
| modmenu-20.0.1.jar | 20.0.1 | https://modrinth.com/mod/mOgUt4GM |
| moreculling-fabric-26.2-1.8.0.jar | 1.8.0 | https://modrinth.com/mod/51shyZVL |
| mru-1.0.31+26.2-fabric.jar | 1.0.31+26.2-fabric | https://modrinth.com/mod/SNVQ2c0g |
| no_sneaking_over_magma-1.7.0+MC26.2.x.jar | 1.7.0+MC26.2.x | https://modrinth.com/mod/cqDlVM1w |
| NoChatReports-FABRIC-26.2-v2.20.1.jar | Fabric-26.2-v2.20.1 | https://modrinth.com/mod/qQyHxfxd |
| notenoughanimations-fabric-1.12.4-mc26.2.jar | 1.12.4 | https://modrinth.com/mod/MPCX6s5C |
| physics-mod-3.1.45-mc-26.2-fabric.jar *(physics-on only)* | 3.1.45 | https://modrinth.com/mod/Xy8aRQKS |
| placeholder-api-3.1.0-beta.1+26.2.jar | 3.1.0-beta.1+26.2 | https://modrinth.com/mod/eXts2L7r |
| PlayerAnimationLibMerged-1.2.4+mc.26.2.jar | 1.2.4 | https://modrinth.com/mod/ha1mEyJS |
| PresenceFootsteps-1.13.3+26.2.jar | 1.13.3+26.2 | https://modrinth.com/mod/rcTfTZr3 |
| raised-fabric-26.2-5.1.2.jar | Fabric-26.2-5.1.2 | https://modrinth.com/mod/nCQRBEiR |
| reimagined-intro-1.0.0(1).jar | 1.0.0 | https://modrinth.com/mod/BsnF5g7E |
| SereneSeasons-fabric-26.2-26.1.2.0.4.jar | 26.1.2.0.4 | https://modrinth.com/mod/e0bNACJD |
| ShoulderSurfing-Fabric-26.2-5.0.7.jar | 26.2-5.0.7+fabric | https://modrinth.com/mod/kepjj2sy |
| skinlayers3d-fabric-1.11.2-mc26.2.jar | 1.11.2 | https://modrinth.com/mod/zV5r3pPn |
| sodium-fabric-0.9.1+mc26.2.jar | mc26.2-0.9.1-fabric | https://modrinth.com/mod/AANobbMI |
| sound-physics-remastered-fabric-1.5.1+26.2.jar | fabric-1.5.1+26.2 | https://modrinth.com/mod/qyVF9oeo |
| sounds-2.5.1+edge+26.2-fabric.jar | 2.5.1+edge+26.2-fabric | https://modrinth.com/mod/ZouiUX7t |
| survivalistessentials-26.2-fabric-6.3.2.6-FABRIC.jar | 26.2-6.3.2.6-FABRIC | https://modrinth.com/mod/hFW7KOhm |
| tectonic-3.0.26-fabric-26.2.jar | 3.0.26-fabric-26.2 | https://modrinth.com/mod/lWDHr9jE |
| Terralith_26.2_v2.6.4.jar | 2.6.4 | https://modrinth.com/mod/8oi3bsk5 |
| ToughAsNails-fabric-26.2-21.11.0.7.jar *(custom build, bundled as override — not on Modrinth)* | 21.11.0.7 | [upstream PR #959](https://github.com/Glitchfiend/ToughAsNails/pull/959) |
| visuality-0.7.14+26.2.jar | 0.7.14+26.2 | https://modrinth.com/mod/rI0hvYcd |
| vmp-fabric-mc26.2-0.2.0+beta.7.236-all.jar | 0.2.0+beta.7.236+26.2 | https://modrinth.com/mod/wnEe9KBa |
| voxy-0.2.18-beta.jar | 0.2.18-beta | https://modrinth.com/mod/fxxUqruK |
| yeetusexperimentus-fabric-102.0.0.jar | 102.0.0 | https://modrinth.com/mod/HaaH232J |
| yet_another_config_lib_v3-3.9.5+26.2-fabric.jar | 3.9.5+26.2-fabric | https://modrinth.com/mod/1eAoo2KR |
| zfastnoise-1.0.39+26.2.jar | 1.0.39+26.2 | https://modrinth.com/mod/OnlVIpq5 |

54 mods total in the physics-on variant (53 resolved via Modrinth + the ToughAsNails override); 53 in physics-off.

## Known issues carried over from the source instance

See [MIGRATION.md](MIGRATION.md) for full detail on each of these:

- **Camera Overhaul** loads but its mixins fail to apply against 26.2 (no compatible build exists yet) — effectively inert, kept enabled in case that changes.
- **Distant Horizons is not included** — its only 26.2 build has severe LOD rendering artifacts. **Voxy** is included in its place as a replacement.
- **Better Combat is not included** — its 1.21.11 build hard-crashes on MC 26.2 (`NoClassDefFoundError`), and no 26.2 build exists.
- **C2ME can flatten terrain near Terralith villages** — under concurrent worldgen, C2ME's chunk system can read a neighboring chunk's terrain before it's finished shaping (`Detected unsafe terrain read during worldgen`), and Terralith's `fortified_village` structure was seen doing this thousands of times in one world, terracing against incomplete height data. Setting `optimizeStructureWeightSampler = false` under `[vanillaWorldGenOptimizations]` in `config/c2me.toml` targets the specific vanilla optimization involved, without giving up C2ME's other performance benefits. Already applied in this pack's bundled config.
- `env` (client/server requirement) is set uniformly to `client: required, server: unsupported` for every mod in the manifest, for simplicity — not individually verified per mod, so a dedicated-server host may need to adjust some entries (e.g. c2me, lithium, vmp are primarily server/world-gen optimizations and could plausibly run server-side).

## Recommended seeds

World seeds confirmed to generate good Tectonic/Terralith terrain with this pack's mod set and config:

- `6316397256416279899` — notable terrain around `X -1376, Z -1904`

## Regenerating the pack

`build_pack.py` is self-contained — no external cache or machine-specific setup beyond having the source instance installed. Run it with Python 3:
```
python build_pack.py
```
By default it reads from `%APPDATA%\PrismLauncher\instances\RealisticCraft\minecraft\mods`. To point it at a differently-named instance or a non-default PrismLauncher install location, set either env var before running:
```
set PRISMLAUNCHER_INSTANCE=MyInstanceName
set PRISMLAUNCHER_ROOT=D:\SomeOtherPath\PrismLauncher
```
It resolves each active (non-`.disabled`) jar to its Modrinth project/version by SHA-1 hash lookup (`GET /v2/version_file/{hash}`), caching the result in `_cache/` (gitignored) so re-runs don't re-hit the API for unchanged mods — delete that folder to force a full re-resolve. Anything that doesn't resolve on Modrinth (currently only the custom `ToughAsNails-fabric-26.2-21.11.0.7.jar` build) gets bundled as a raw override instead of a download reference.

Config overrides are copied from the instance's `config/` folder, excluding:
- `config/fancymenu/assets` (456 MB of regenerable intro-video cache, not user config)
- `config/DistantHorizons.toml` and `config/bettercombat` (disabled mods, no longer part of the pack)
- `*.bak` backup files
- `config/physicsmod` (physics-off variant only)

The `RESOURCEPACKS` / `SHADERPACKS` lists at the top of `build_pack.py` name which files under the instance's `resourcepacks/` and `shaderpacks/` folders get bundled as overrides — update those lists to add or remove bundled packs. The script always forces `enableShaders=false` in the packaged `iris.properties` regardless of what's currently active on the source instance, so bundled shaders never end up auto-enabled.
