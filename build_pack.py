"""
Builds both RealisticCraft Reimagined .mrpack variants from a local PrismLauncher
instance's mods folder. Self-contained: resolves every active (non-.disabled) jar to
its Modrinth project/version by SHA-1 hash, with no external cache or dependency
beyond network access to api.modrinth.com.

Configure via environment variables (all optional, defaults match the original
RealisticCraft instance layout):
  PRISMLAUNCHER_INSTANCE   PrismLauncher instance name (default: RealisticCraft)
  PRISMLAUNCHER_ROOT       PrismLauncher root dir (default: %APPDATA%\\PrismLauncher)
"""
import hashlib, json, os, shutil, time, urllib.request, zipfile

PRISMLAUNCHER_ROOT = os.environ.get(
    "PRISMLAUNCHER_ROOT", os.path.join(os.environ["APPDATA"], "PrismLauncher")
)
INSTANCE_NAME = os.environ.get("PRISMLAUNCHER_INSTANCE", "RealisticCraft")

MC = os.path.join(PRISMLAUNCHER_ROOT, "instances", INSTANCE_NAME, "minecraft")
MODS = os.path.join(MC, "mods")
PROJECT = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(PROJECT, "_cache", "resolved_mods.json")

PHYSICS_FILE = "physics-mod-3.1.45-mc-26.2-fabric.jar"
CUSTOM_FILE = "ToughAsNails-fabric-26.2-21.11.0.7.jar"  # not on Modrinth, bundled as override

MC_VERSION = "26.2"
FABRIC_LOADER_VERSION = "0.19.3"
PACK_VERSION = "1.2.0"

# Bundled directly (not on Modrinth / not worth hash-resolving) but shipped disabled by
# default -- present in resourcepacks/shaderpacks so players can opt in from the in-game
# menus, without being auto-enabled by the pack itself.
RESOURCEPACKS = ["3D Default 1.21.2+ v1.15.0.zip"]
SHADERPACKS = ["Bliss_v2.1.2_(Chocapic13_Shaders_edit).zip"]

# Config folders/files to exclude from overrides (disabled mods, huge caches, backups)
EXCLUDE_CONFIG = {
    "fancymenu/assets",   # regenerable video/image cache for reimagined-intro, can be huge
    "DistantHorizons.toml",
    "bettercombat",
}


def should_exclude(rel_path):
    rel_path = rel_path.replace("\\", "/")
    if rel_path.endswith(".bak"):
        return True
    for ex in EXCLUDE_CONFIG:
        if rel_path == ex or rel_path.startswith(ex + "/"):
            return True
    return False


def sha1_of(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_one(fname):
    """Hash a single mod jar and look it up on Modrinth. Returns a file record or None."""
    path = os.path.join(MODS, fname)
    h = sha1_of(path)
    url = f"https://api.modrinth.com/v2/version_file/{h}?algorithm=sha1"
    req = urllib.request.Request(url, headers={"User-Agent": "RealisticCraft-Reimagined-packer/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.load(r)
    except Exception:
        return None
    primary = next((fl for fl in data["files"] if fl.get("primary")), data["files"][0])
    return {
        "filename": fname,
        "project_id": data["project_id"],
        "version_id": data["id"],
        "version_number": data["version_number"],
        "sha1": primary["hashes"]["sha1"],
        "sha512": primary["hashes"]["sha512"],
        "url": primary["url"],
        "size": primary["size"],
    }


def get_resolved_mods(refresh=False):
    """Resolve every active (non-.disabled) mod jar to its Modrinth project/version.

    Incremental: reuses cached entries (keyed by filename) across runs and only hits
    the Modrinth API for jars that are new since the last run, or all of them if
    refresh=True or the cache doesn't exist yet.
    """
    active = sorted(f for f in os.listdir(MODS) if f.endswith(".jar"))

    cached_by_name = {}
    if not refresh and os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, encoding="utf-8") as f:
            cached_by_name = {m["filename"]: m for m in json.load(f)}

    resolved, unresolved = [], []
    for fname in active:
        if fname in cached_by_name:
            resolved.append(cached_by_name[fname])
            continue
        record = resolve_one(fname)
        if record is not None:
            resolved.append(record)
        else:
            unresolved.append(fname)
        time.sleep(0.1)

    if unresolved:
        expected_unresolved = {CUSTOM_FILE}
        surprising = set(unresolved) - expected_unresolved
        if surprising:
            print(f"WARNING: {len(surprising)} active mod(s) didn't resolve on Modrinth "
                  f"and won't be in the pack manifest: {sorted(surprising)}")

    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(resolved, f, indent=2)
    return resolved


def build_index(resolved, name, summary, include_physics):
    files = []
    for m in resolved:
        if not include_physics and m["filename"] == PHYSICS_FILE:
            continue
        files.append({
            "path": f"mods/{m['filename']}",
            "hashes": {"sha1": m["sha1"], "sha512": m["sha512"]},
            "env": {"client": "required", "server": "unsupported"},
            "downloads": [m["url"]],
            "fileSize": m["size"],
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


def build_variant(resolved, variant_dir, name, summary, include_physics):
    if os.path.exists(variant_dir):
        shutil.rmtree(variant_dir)
    os.makedirs(variant_dir, exist_ok=True)
    index = build_index(resolved, name, summary, include_physics)
    with open(os.path.join(variant_dir, "modrinth.index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    overrides_mods = os.path.join(variant_dir, "overrides", "mods")
    os.makedirs(overrides_mods, exist_ok=True)
    custom_src = os.path.join(MODS, CUSTOM_FILE)
    if os.path.exists(custom_src):
        shutil.copy2(custom_src, os.path.join(overrides_mods, CUSTOM_FILE))

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
                f.write("enableShaders=false\n" if line.startswith("enableShaders=") else line)

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


def main():
    resolved = get_resolved_mods()

    on_dir = os.path.join(PROJECT, "_build", "physics-on")
    off_dir = os.path.join(PROJECT, "_build", "physics-off")

    n_on = build_variant(
        resolved, on_dir,
        "RealisticCraft Reimagined",
        "RealisticCraft, rebuilt for Minecraft 26.2 — Physics Mod enabled.",
        include_physics=True,
    )
    n_off = build_variant(
        resolved, off_dir,
        "RealisticCraft Reimagined (No Physics)",
        "RealisticCraft, rebuilt for Minecraft 26.2 — Physics Mod disabled for better performance / vanilla-feel physics.",
        include_physics=False,
    )

    zip_pack(on_dir, os.path.join(PROJECT, "RealisticCraft-Reimagined-PhysicsOn.mrpack"))
    zip_pack(off_dir, os.path.join(PROJECT, "RealisticCraft-Reimagined-PhysicsOff.mrpack"))

    print(f"physics-on: {n_on} mod entries")
    print(f"physics-off: {n_off} mod entries")
    print("Done.")


if __name__ == "__main__":
    main()
