#!/usr/bin/env python3
"""Check the GDevelop starter project against the files in this repo.

This does not open the project in GDevelop. It checks that game.json parses,
that its resource paths resolve, and that the scene matches the starter slice.
"""

import hashlib
import json
import pathlib
import struct
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
GAME_JSON = ROOT / "game.json"
AUDIO = "audio/star-of-bethlehem-2024.ogg"

# SHA-256 of the PNGs and cues.json copied byte-for-byte from the starter inputs.
EXPECTED_SHA256 = {
    "art/assets/snow-star-review-v1/bethlehem_star_scene.png":
        "8ef287d5fa1d3b95e0dc41dab153f7c44435e2ce62c37ae58bd6f24a4b2631d2",
    "art/assets/snow-star-review-v1/snow_flake_near.png":
        "9534bb3c4d54d08aabdffa1060ca87353c975e53bd3e44c84a1a0eae4c10cc5b",
    "art/assets/snow-star-review-v1/snow_flake_small.png":
        "b5a4b3b80884eb3644e2b65b43becd59ba43996013893e9d0eedc426dab1b9db",
    "art/assets/snow-star-review-v1/snow_hills_far_tile.png":
        "38458fc4592bffc75dd147ae4289c7a7a22afe97db86532decb6609b09514019",
    "art/assets/snow-star-review-v1/snow_hills_mid_tile.png":
        "edd571819c0ffa3ab03cdecfcd2f36ea47bd7d44ad3903614786936e33ecf998",
    "art/assets/snow-star-review-v1/snow_path_ground_tile.png":
        "91dd4e152731829071ad1c7106949157b00f9574da22215e09fb80ed8cd6f2b5",
    "art/assets/snow-star-review-v1/snow_sky_base.png":
        "4bfda09c9e3080322bc588ef114e017917e80b82409ef2abdc292976d1f3e158",
    "art/assets/snow-star-review-v1/snow_trees_mid_tile.png":
        "b8b5f13125d4a885bb179d2ecf509c00c264c069cbcaebce806eafc5a75a7d60",
    "art/assets/snow-star-review-v1/snow_verse_static_overlay.png":
        "12f41ea99058a5a98bd4dd336a86c7abba5d75ad708e040a019d22b021f36c11",
    "art/assets/user-b-reduced-preview/01-walk-01-48x56.png":
        "08e5ccf225538f4321bb2845104b811537905ed7b5a7dcb0c00351f8a78985c4",
    "art/assets/user-b-reduced-preview/02-walk-02-48x56.png":
        "8e8b4da750aad992fc93a27b073c9b3cfc370997ed39eabae480f6c17aca9568",
    "art/assets/user-b-reduced-preview/03-walk-03-48x56.png":
        "29c474c65e3ab89be0ed9737ddd4ed6c76b827e31396e0ffd57c338ec2de9e56",
    "art/assets/user-b-reduced-preview/04-idle-48x56.png":
        "43c0df44108959308303951bc0550f97d53bd945d40a186a3dc8237b7315b5fe",
    "art/assets/user-b-reduced-preview/05-look-UP-48x56.png":
        "a3a257c4fce3cb156c5d1757d8129c68ddfe386591550c7eaef10b13dd6d1b24",
    "qa/cues.json":
        "e5996e5a6bc1120fc01e6444f601afc46f4b6f7df00c5a7ed8cb6e30791ae3d5",
}

EXPECTED_PNG_SIZE = {
    "snow_sky_base.png": (320, 180),
    "snow_hills_far_tile.png": (640, 180),
    "snow_hills_mid_tile.png": (640, 180),
    "snow_trees_mid_tile.png": (640, 180),
    "snow_path_ground_tile.png": (640, 180),
    "snow_verse_static_overlay.png": (320, 180),
    "bethlehem_star_scene.png": (24, 24),
    "snow_flake_small.png": (3, 3),
    "snow_flake_near.png": (5, 5),
    "01-walk-01-48x56.png": (48, 56),
    "02-walk-02-48x56.png": (48, 56),
    "03-walk-03-48x56.png": (48, 56),
    "04-idle-48x56.png": (48, 56),
    "05-look-UP-48x56.png": (48, 56),
}

FORBIDDEN_BASENAMES = {
    "bethlehem_star_chorus.png",
    "verse-snow-review.png",
    "verse-snow-review-6x.png",
    "stop-look-UP-star-review.png",
    "stop-look-UP-star-review-6x.png",
    "chorus-star-integer5x-review.png",
    "chorus-star-integer5x-review-6x.png",
    "chorus-star-designed-review.png",
    "chorus-star-designed-review-6x.png",
    "star-options-designed-left-integer-right.png",
    "seam3-far.png",
    "seam3-mid.png",
    "seam3-trees.png",
    "seam3-ground.png",
    "seam3-combined.png",
}


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def sha256(path):
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def png_size(path):
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} is not a PNG")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def instruction_types(events):
    found = []
    for event in events:
        if event.get("type") != "BuiltinCommonInstructions::Standard":
            continue
        for key in ("conditions", "actions"):
            for instruction in event.get(key, []):
                type_info = instruction.get("type", {})
                if isinstance(type_info, dict):
                    found.append(type_info.get("value", ""))
                else:
                    found.append(str(type_info))
        found.extend(instruction_types(event.get("events", [])))
    return found


def main():
    errors = 0
    if not GAME_JSON.is_file():
        return fail(f"missing {GAME_JSON}")
    try:
        project = json.loads(GAME_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return fail(f"game.json is not valid JSON: {exc}")

    version = project.get("gdVersion", {})
    if version != {"build": 287, "major": 5, "minor": 6, "revision": 0}:
        errors += fail(f"gdVersion is {version}, expected 5.6.287 revision 0")
    if project.get("initialGDVersion") != "5.6.287":
        errors += fail("initialGDVersion is not 5.6.287")
    if project.get("firstLayout") != "Main":
        errors += fail("firstLayout is not Main")

    properties = project["properties"]
    expected_props = {
        "windowWidth": 320,
        "windowHeight": 180,
        "scaleMode": "nearest",
        "pixelsRounding": True,
        "antialiasingMode": "none",
        "adaptGameResolutionAtRuntime": False,
        "sizeOnStartupMode": "",
    }
    for key, expected in expected_props.items():
        if properties.get(key) != expected:
            errors += fail(f"properties.{key} is {properties.get(key)!r}, expected {expected!r}")

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    if "audio/" not in gitignore.splitlines():
        errors += fail(".gitignore does not ignore audio/")
    tracked = subprocess.check_output(
        ["git", "ls-files"], cwd=ROOT, text=True
    ).splitlines()
    audio_tracked = [line for line in tracked if line.startswith("audio/")]
    if audio_tracked:
        errors += fail(f"audio files are tracked: {audio_tracked}")

    resources = project["resources"]["resources"]
    resource_names = {}
    for resource in resources:
        name = resource["name"]
        relative = resource["file"].replace("\\", "/")
        basename = pathlib.PurePosixPath(relative).name
        if basename in FORBIDDEN_BASENAMES or "bethlehem_star_chorus" in relative:
            errors += fail(f"forbidden resource {relative}")
        if relative == AUDIO:
            if resource.get("kind") != "audio" or resource.get("preloadAsMusic") is not True:
                errors += fail("song resource must be audio preloaded as music")
            if (ROOT / relative).exists():
                errors += fail("the song file is present in the worktree; do not commit it")
        else:
            path = ROOT / relative
            if not path.is_file():
                errors += fail(f"resource file does not exist: {relative}")
            elif relative in EXPECTED_SHA256 and sha256(path) != EXPECTED_SHA256[relative]:
                errors += fail(f"hash mismatch for {relative}")
        if resource.get("kind") == "image":
            if resource.get("smoothed") is not False:
                errors += fail(f"image {name} has smoothing enabled")
            if basename in EXPECTED_PNG_SIZE and (ROOT / relative).is_file():
                size = png_size(ROOT / relative)
                if size != EXPECTED_PNG_SIZE[basename]:
                    errors += fail(f"{relative} is {size}, expected {EXPECTED_PNG_SIZE[basename]}")
        resource_names[name] = relative

    for relative, digest in EXPECTED_SHA256.items():
        path = ROOT / relative
        if not path.is_file():
            errors += fail(f"missing expected file {relative}")
        elif sha256(path) != digest:
            errors += fail(f"hash mismatch for {relative}")

    cues = json.loads((ROOT / "qa/cues.json").read_text(encoding="utf-8"))
    if cues.get("cue_count") != 28 or len(cues.get("cues", [])) != 28:
        errors += fail("qa/cues.json does not contain 28 cues")
    if cues.get("source_audio", {}).get("sha256") != (
        "b44a5a86f02192f5589e409383429dbc334f3624ea0daa3564b9ebcc2226c933"
    ):
        errors += fail("qa/cues.json audio hash changed")

    layouts = project["layouts"]
    if len(layouts) != 1 or layouts[0]["name"] != "Main":
        errors += fail("expected one scene named Main")
        return errors
    scene = layouts[0]
    objects = {obj["name"]: obj for obj in scene["objects"]}
    expected_objects = {
        "Sky", "HillsFar", "HillsMid", "TreesMid", "Ground", "Walker",
        "SnowStill", "BethlehemStar", "SnowFlakeSmall", "SnowFlakeNear",
        "SongTime", "CueMarks",
    }
    if set(objects) != expected_objects:
        errors += fail(f"scene objects are {sorted(objects)}, expected {sorted(expected_objects)}")

    walker = objects.get("Walker", {})
    animations = {anim["name"]: anim for anim in walker.get("animations", [])}
    if list(animations) != ["Walk", "Idle", "LookUp"]:
        errors += fail(f"Walker animations are {list(animations)}")
    else:
        walk = animations["Walk"]["directions"][0]
        frames = [sprite["image"] for sprite in walk["sprites"]]
        if frames != [
            "01-walk-01-48x56.png",
            "02-walk-02-48x56.png",
            "03-walk-03-48x56.png",
            "02-walk-02-48x56.png",
        ]:
            errors += fail(f"Walk frames are {frames}")
        if walk.get("looping") is not True or walk.get("timeBetweenFrames") != 0.22:
            errors += fail("Walk must loop with 0.22 s between frames")
        for anim_name in ("Walk", "Idle", "LookUp"):
            for sprite in animations[anim_name]["directions"][0]["sprites"]:
                origin = sprite["originPoint"]
                if (origin["x"], origin["y"]) != (0, 0):
                    errors += fail(f"{anim_name} origin is not top-left")
                pivots = [p for p in sprite["points"] if p["name"] == "Pivot"]
                if pivots != [{"name": "Pivot", "x": 24, "y": 48}]:
                    errors += fail(f"{anim_name} Pivot point is {pivots}")
                if sprite["image"] not in resource_names:
                    errors += fail(f"Walker image {sprite['image']} is not a resource")

    star = objects.get("BethlehemStar", {})
    star_frames = star.get("animations", [{}])[0].get("directions", [{}])[0].get("sprites", [])
    if len(star_frames) != 1 or star_frames[0].get("image") != "bethlehem_star_scene.png":
        errors += fail("BethlehemStar must use only bethlehem_star_scene.png")
    elif [p for p in star_frames[0]["points"] if p["name"] == "Anchor"] != [
        {"name": "Anchor", "x": 11, "y": 11}
    ]:
        errors += fail("BethlehemStar Anchor point is missing or not (11, 11)")

    for obj in objects.values():
        if obj["type"] == "Sprite":
            for anim in obj["animations"]:
                for direction in anim["directions"]:
                    for sprite in direction["sprites"]:
                        if sprite["image"] not in resource_names:
                            errors += fail(f"{obj['name']} image {sprite['image']} is not a resource")

    expected_instances = {
        ("Sky", 0, 0, 0, "", False),
        ("HillsFar", 0, 0, 10, "", False),
        ("HillsFar", 640, 0, 10, "", False),
        ("HillsMid", 0, 0, 20, "", False),
        ("HillsMid", 640, 0, 20, "", False),
        ("TreesMid", 0, 0, 30, "", False),
        ("TreesMid", 640, 0, 30, "", False),
        ("Ground", 0, 0, 40, "", False),
        ("Ground", 640, 0, 40, "", False),
        ("Walker", -48, 109, 50, "", False),
        ("SnowStill", 0, 0, 60, "", False),
        ("BethlehemStar", 239, 30, 70, "", True),
        ("SongTime", 2, 2, 0, "HUD", False),
        ("CueMarks", 2, 16, 1, "HUD", False),
    }
    found_instances = set()
    for inst in scene["instances"]:
        if inst["name"] not in objects:
            errors += fail(f"instance of unknown object {inst['name']}")
        found_instances.add(
            (
                inst["name"],
                inst["x"],
                inst["y"],
                inst["zOrder"],
                inst["layer"],
                bool(inst.get("hidden", False)),
            )
        )
        tile_copies = [
            var for var in inst.get("initialVariables", []) if var["name"] == "TileCopy"
        ]
        if inst["name"] in {"HillsFar", "HillsMid", "TreesMid", "Ground"}:
            expected_copy = 0 if inst["x"] == 0 else 1
            if len(tile_copies) != 1 or tile_copies[0].get("value") != expected_copy:
                errors += fail(f"{inst['name']} at x={inst['x']} TileCopy is {tile_copies}")
    if found_instances != expected_instances:
        errors += fail(
            "instances differ:\n  missing "
            + str(sorted(expected_instances - found_instances))
            + "\n  extra "
            + str(sorted(found_instances - expected_instances))
        )
    flake_instances = [
        inst["name"] for inst in scene["instances"]
        if inst["name"] in {"SnowFlakeSmall", "SnowFlakeNear"}
    ]
    if flake_instances:
        errors += fail(f"flake instances should not exist yet: {flake_instances}")

    layer_names = [layer["name"] for layer in scene["layers"]]
    if layer_names != ["", "HUD"]:
        errors += fail(f"layers are {layer_names}")

    variable_values = {var["name"]: var["value"] for var in scene["variables"]}
    expected_variables = {
        "WalkSpeedPxPerSec": 20,
        "WalkerStartX": -48,
        "WalkerCenterX": 136,
        "TilePeriodPx": 640,
        "ScrollFarPxPerSec": 4,
        "ScrollMidPxPerSec": 8,
        "ScrollTreesPxPerSec": 12,
        "ScrollGroundPxPerSec": 20,
    }
    for name, value in expected_variables.items():
        if variable_values.get(name) != value:
            errors += fail(f"scene variable {name} is {variable_values.get(name)!r}")

    types = instruction_types(scene["events"])
    joined = "\n".join(
        json.dumps(event) for event in scene["events"]
        if event.get("type") == "BuiltinCommonInstructions::Standard"
    )
    if "MusicChannelPlayingOffset(0)" not in joined:
        errors += fail("events do not read MusicChannelPlayingOffset(0)")
    play_music = [
        instruction
        for event in scene["events"]
        for instruction in event.get("actions", [])
        if instruction.get("type", {}).get("value") == "PlayMusicOnChannel"
    ]
    if play_music != [
        {
            "type": {"value": "PlayMusicOnChannel"},
            "parameters": ["", "star-of-bethlehem-2024.ogg", "0", "no", "100", "1"],
        }
    ]:
        errors += fail(f"PlayMusicOnChannel parameters are {play_music}")
    if "DepartScene" not in types:
        errors += fail("music is not started at the beginning of the scene")
    space_key = [
        instruction
        for event in scene["events"]
        for instruction in event.get("conditions", [])
        if instruction.get("type", {}).get("value") == "KeyFromTextJustPressed"
    ]
    if space_key != [
        {
            "type": {"value": "KeyFromTextJustPressed"},
            "parameters": ["", '"Space"'],
        }
    ]:
        errors += fail(f"Space cue key parameters are {space_key}")
    if "MusicPlaying" not in types:
        errors += fail("Space cue marker does not require the music to be playing")
    for forbidden in ("StartSceneTimer", "SceneTimer", "Wait", "TimerElapsed"):
        if forbidden in types:
            errors += fail(f"events use {forbidden}")
    if "JSONResourceLoader::LoadJSONToVariable" in types:
        errors += fail("lyric loader action was not part of this slice")

    if errors:
        print(f"{errors} check(s) failed", file=sys.stderr)
        return 1
    print("OK: game.json parsed; resources, art hashes, and scene checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
