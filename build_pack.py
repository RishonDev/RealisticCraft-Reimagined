import json, os, shutil, zipfile

MODS = r"C:\Users\PC\AppData\Roaming\PrismLauncher\instances\RealisticCraft\minecraft\mods"
MC = r"C:\Users\PC\AppData\Roaming\PrismLauncher\instances\RealisticCraft\minecraft"
PROJECT = r"C:\Users\PC\dev\RealisticCraft-Reimagined"
SCRATCH = r"C:\Users\PC\AppData\Local\Temp\claude\C--Users-PC\65f71e53-8f88-4b8d-a641-9b73a71fd90f\scratchpad"

with open(os.path.join(SCRATCH, 'resolved_mods.json'), encoding='utf-8') as f:
    resolved = json.load(f)

PHYSICS_FILE = "physics-mod-3.1.45-mc-26.2-fabric.jar"
CUSTOM_FILE = "ToughAsNails-fabric-26.2-21.11.0.7.jar"

MC_VERSION = "26.2"
FABRIC_LOADER_VERSION = "0.19.3"
PACK_VERSION = "1.1.0"

# Bundled directly (not on Modrinth / not worth hash-resolving) but shipped disabled by
# default -- present in resourcepacks/shaderpacks so players can opt in from the in-game
# menus, without being auto-enabled by the pack itself.
RESOURCEPACKS = ["§5RealisCraft §6[v1.38.1] §f[Demo].zip"]
SHADERPACKS = ["Bliss_v2.1.2_(Chocapic13_Shaders_edit).zip"]

# Config folders/files to exclude from overrides (disabled mods, huge caches, backups)
EXCLUDE_CONFIG = {
    "fancymenu/assets",   # 456MB regenerable video/image cache for reimagined-intro
    "DistantHorizons.toml",
    "bettercombat",
    "shouldersurfing-client-1.toml.bak",
}

def should_exclude(rel_path):
    rel_path = rel_path.replace("\\", "/")
    for ex in EXCLUDE_CONFIG:
        if rel_path == ex or rel_path.startswith(ex + "/"):
            return True
    return False

def build_index(name, summary, include_physics):
    files = []
    for m in resolved:
        if not include_physics and m['filename'] == PHYSICS_FILE:
            continue
        files.append({
            "path": f"mods/{m['filename']}",
            "hashes": {"sha1": m['sha1'], "sha512": m['sha512']},
            "env": {"client": "required", "server": "unsupported"},
            "downloads": [m['url']],
            "fileSize": m['size'],
        })

    return {
        "formatVersion": 1,
        "game": "minecraft",
        "versionId": PACK_VERSION,
        "name": name,
        "summary": summary,
        "files": files,
        "dependencies": {
            "minecraft": MC_VERSION,
            "fabric-loader": FABRIC_LOADER_VERSION,
        },
    }

def build_variant(variant_dir, name, summary, include_physics):
    os.makedirs(variant_dir, exist_ok=True)
    index = build_index(name, summary, include_physics)
    with open(os.path.join(variant_dir, "modrinth.index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    overrides_mods = os.path.join(variant_dir, "overrides", "mods")
    os.makedirs(overrides_mods, exist_ok=True)
    shutil.copy2(os.path.join(MODS, CUSTOM_FILE), os.path.join(overrides_mods, CUSTOM_FILE))

    overrides_config = os.path.join(variant_dir, "overrides", "config")
    src_config = os.path.join(MC, "config")
    for dirpath, dirnames, filenames in os.walk(src_config):
        rel_dir = os.path.relpath(dirpath, src_config)
        for fn in filenames:
            rel_path = fn if rel_dir == "." else os.path.join(rel_dir, fn)
            if should_exclude(rel_path):
                continue
            if not include_physics and rel_path.replace("\\", "/").startswith("physicsmod"):
                continue
            dest = os.path.join(overrides_config, rel_path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(os.path.join(dirpath, fn), dest)

    if os.path.exists(os.path.join(MC, "options.txt")):
        shutil.copy2(os.path.join(MC, "options.txt"), os.path.join(variant_dir, "overrides", "options.txt"))

    # Resource packs / shader packs: bundled so they're present to opt into, but shipped
    # disabled by default (options.txt's resourcePacks list already only has "vanilla",
    # and we force-disable Iris shaders below regardless of the live instance's current state).
    if RESOURCEPACKS:
        dest_rp = os.path.join(variant_dir, "overrides", "resourcepacks")
        os.makedirs(dest_rp, exist_ok=True)
        for rp in RESOURCEPACKS:
            src = os.path.join(MC, "resourcepacks", rp)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(dest_rp, rp))

    if SHADERPACKS:
        dest_sp = os.path.join(variant_dir, "overrides", "shaderpacks")
        os.makedirs(dest_sp, exist_ok=True)
        for sp in SHADERPACKS:
            src = os.path.join(MC, "shaderpacks", sp)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(dest_sp, sp))

    # Force shaders off in the packaged iris.properties, independent of whatever the
    # live instance currently has active.
    iris_props_dest = os.path.join(overrides_config, "iris.properties")
    if os.path.exists(iris_props_dest):
        with open(iris_props_dest, encoding="utf-8") as f:
            lines = f.readlines()
        with open(iris_props_dest, "w", encoding="utf-8") as f:
            for line in lines:
                if line.startswith("enableShaders="):
                    f.write("enableShaders=false\n")
                else:
                    f.write(line)

    return len(index["files"])

def zip_pack(variant_dir, out_path):
    if os.path.exists(out_path):
        os.remove(out_path)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for dirpath, dirnames, filenames in os.walk(variant_dir):
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, variant_dir)
                zf.write(full, rel)

on_dir = os.path.join(PROJECT, "_build", "physics-on")
off_dir = os.path.join(PROJECT, "_build", "physics-off")

n_on = build_variant(
    on_dir,
    "RealisticCraft Reimagined",
    "RealisticCraft, rebuilt for Minecraft 26.2 — Physics Mod enabled.",
    include_physics=True,
)
n_off = build_variant(
    off_dir,
    "RealisticCraft Reimagined (No Physics)",
    "RealisticCraft, rebuilt for Minecraft 26.2 — Physics Mod disabled for better performance / vanilla-feel physics.",
    include_physics=False,
)

zip_pack(on_dir, os.path.join(PROJECT, "RealisticCraft-Reimagined-PhysicsOn.mrpack"))
zip_pack(off_dir, os.path.join(PROJECT, "RealisticCraft-Reimagined-PhysicsOff.mrpack"))

print(f"physics-on: {n_on} mod entries")
print(f"physics-off: {n_off} mod entries")
print("Done.")
