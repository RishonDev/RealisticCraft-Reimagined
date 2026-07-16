# RealisticCraft: Minecraft 26.2 Migration

Record of the mod-update pass that brought the source RealisticCraft instance from MC 1.21.11 (mostly) to 26.2, plus everything that came out of it: two mods that couldn't be updated, one mod replaced outright, a couple of performance mods added, and a source-level fork/port of ToughAsNails to unblock the one mod with no available 26.2 build.

Loader: Fabric Loader 0.19.3, Minecraft 26.2

## Ground rule: nothing gets deleted

Every superseded jar was renamed to `<name>.jar.disabled` rather than removed, so the previous 1.21.11 (and, for a couple of mods, 26.1.2) state is fully recoverable by stripping the `.disabled` suffix. The source instance's `mods/` folder ended up with 54 active jars and 46 `.disabled` ones.

## Bulk update (39 mods)

For every mod, the currently-installed version was queried against Modrinth's API for a `game_versions=["26.2"]` + `loaders=["fabric"]` match. 39 mods had one and were downloaded straight from Modrinth's CDN, old versions disabled:

AmbientSounds, CreativeCore, FallingTree, Forge Config API Port, GlitchCore, ImmediatelyFast, NoChatReports, Player Animation Library, Presence Footsteps, Serene Seasons, Shoulder Surfing Reloaded, Terralith, ToughAsNails (later superseded again, see below), cloth-config, dynamiccrosshair, ferritecore, first-person, ice-boat-nerf, iris, lithium, lithostitched, modmenu, moreculling, mru, no-sneaking-over-magma, notenoughanimations, physics-mod, placeholder-api, raised, sodium, sound-physics-remastered, sounds, survivalistessentials, tectonic, visuality, vmp, yeetus-experimentus, yet-another-config-lib, zfastnoise.

`fabric-api` and `c2me` were bumped a second time after the first pass, since the installed copies (added manually before this update pass started) weren't the latest available (`0.154.0`→`0.155.0+26.2`, `0.4.1-beta.1.0`→`0.4.2-alpha.0.18`).

## Mods with no 26.2 build available — left disabled

Two mods had no compatible release from their authors at the time of this migration:

- **Better Combat** (`bettercombat-fabric-3.0.1+1.21.11.jar.disabled`) — worse than just "no update": its old 1.21.11 build was left *active* initially, and it hard-crashed the game (`NoClassDefFoundError: net/minecraft/class_2396` inside its own `TrailParticles` init, referencing a stale intermediary class name). Disabled after the crash was diagnosed.
- **Camera Overhaul** (`CameraOverhaul-v2.0.6-fabric+mc[1.21.11-plus].jar`) — still **active**, unlike Better Combat. Its mixins target vanilla classes that no longer exist under those names in 26.2 and all fail with "Mixin target ... was not found" warnings at startup, but Fabric tolerates missing mixin targets as non-fatal, so the mod loads without crashing — it just doesn't do much. Left enabled since it isn't actively breaking anything; worth revisiting if/when a real 26.2 build ships.

Check Modrinth periodically for updates to both; nothing else needs to change to pick them up.

## Distant Horizons → replaced with Voxy

Distant Horizons' only available 26.2 build (`3.2.0-b-26.2`, the newest on Modrinth at the time) logs on startup:

> Deprecated Rendering Engine. DH is currently rendering via raw OpenGL... there may be visual issues.

In practice this produced severe visual artifacts — vertically-smeared black "curtain" streaks hanging off the horizon where LOD terrain should render, essentially breaking the whole point of the mod. This is a bug in DH's own renderer failing to adapt to MC 26.x's new rendering pipeline (the same `GuiGraphicsExtractor` / `RenderPipelines` / `GuiRenderState` rewrite that also broke several APIs the [ToughAsNails 26.2 port](https://github.com/Glitchfiend/ToughAsNails/pull/959) depended on). DH is hosted on GitLab, not GitHub, so there was no quick upstream issue search to confirm a known bug, but the in-game log message is a direct admission of the problem.

Decision: disabled DH (`DistantHorizons-3.2.0-b-26.2-fabric-neoforge.jar.disabled`), replaced with **Voxy** (`voxy-0.2.18-beta.jar`), a different LOD-terrain mod that's actively maintained through 26.2 and shares no dependency conflicts (needs `fabric-api` and `sodium`, both already at the right versions). Not a drop-in equivalent in features, but functional where DH currently isn't. Revisit if DH ships a real 26.2 renderer.

## Performance mods added

Two extra mods pulled from another PrismLauncher instance ("Fabulously Optimized"), chosen specifically for having **no visual effect**:

- **Dynamic FPS** (`dynamic-fps-3.11.9+minecraft-26.2.0-fabric.jar`) — throttles resource usage while the window is unfocused/idle.
- **Ixeris** (`Ixeris-4.5.2+26.2-fabric.jar`) — buffered raw input + threaded event polling (input-latency reduction). Fetched the newer `4.5.2` from Modrinth rather than the `4.5.1` sitting in the source instance.

Other candidates from that instance (ferritecore, lithium, sodium, moreculling, entityculling, immediatelyfast, fabric-api) were already present at equal or newer versions and skipped. `debugify` and `sodium-extra` were deliberately passed over — both touch visual/rendering behavior, which was explicitly out of scope for this pass.

## ToughAsNails: no update existed, so it got built from source

ToughAsNails had no 26.2 build available anywhere (Modrinth's newest was `26.1.2`), so it was ported from source rather than left disabled:

- Cloned `Glitchfiend/ToughAsNails`, branched off their `26.1.2` branch.
- Fixed MC 26.2 API breaks (`Gui`→`Hud` rename, `CriteriaTriggers` package move, `Tuple` removal, `Options.hideGui` removal) across the common/Fabric/Forge/NeoForge source sets.
- Along the way, found and fixed unrelated pre-existing breakage in the NeoForge datagen providers (broken since MC 1.21.6, unrelated to this port — Mojang removed `KeyTagProvider`/`IntrinsicHolderTagsProvider` upstream a while back and nobody had recompiled that module since).
- Built and installed the resulting `ToughAsNails-fabric-26.2-21.11.0.7.jar` — it's a custom build, not published on Modrinth (bundled directly in this pack as an override instead of a download reference), so it won't auto-update; check the PR below for when/if it lands officially.
- Opened upstream PR: **https://github.com/Glitchfiend/ToughAsNails/pull/959** ("Port to MC 26.2 (Fabric, Forge, NeoForge)").

## Verification

- Compile-time: all mixins and access-wideners were fixed twice — once when a stale Fabric-side mixin crashed the game at launch (`Mixin transformation of net.minecraft.client.gui.Gui failed`), and the underlying issue (mixins aren't checked by the Java compiler, only at runtime) meant a second, unrelated crash from Better Combat showed up only after that first fix.
- Runtime: confirmed the source instance launches, loads a world, and runs normally with the final mod set.
- Distant Horizons' replacement (Voxy) has not yet been verified in-game — installed but not launch-tested at the time of writing.

## This pack

This document describes the source instance; the mod set it describes is what got packaged into this repo's two `.mrpack` variants (Physics Mod on/off) — see the main [README](README.md) for the full current mod list.
