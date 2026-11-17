# Star of Bethlehem lyric video

Starter GDevelop 5 project for a 320×180 pixel-art lyric video of "Star of Bethlehem". This is the first slice: the scene, the walk-in, parallax scrolling, and a timing readout. It is not a finished video.

The project file was written for the JSON that **GDevelop 5.6.287** (4 November 2026, the latest stable release at the time) saves. `gdVersion` is major 5, minor 6, build 287, revision 0, and `initialGDVersion` is `5.6.287`.

## Open it in GDevelop

1. Install [GDevelop 5 desktop](https://github.com/4ian/GDevelop/releases/tag/v5.6.287) (5.6.287 or newer). The web editor at <https://editor.gdevelop.io> can open the same `game.json`.
2. Choose **Open** and select `game.json` in this folder. Resource paths are relative to that file.
3. Add the song, as described below, before previewing.
4. Press **Preview**.

`python3 tools/validate_project.py` checks that `game.json` parses and that every referenced file exists in the repo, except the git-ignored song.

## Audio (not in this repo)

The repository is public, and the song has not been approved for commit. `audio/` is in `.gitignore`. Do not add the OGG.

Create the folder yourself and put your copy at:

`audio/star-of-bethlehem-2024.ogg`

The file the cues were measured against is stereo Vorbis, 44,100 Hz, duration **183.212 s**, SHA-256:

`b44a5a86f02192f5589e409383429dbc334f3624ea0daa3564b9ebcc2226c933`

The scene plays that resource on music channel 0 once, at volume 100. Positions and the HUD read `MusicChannelPlayingOffset(0)`. Without the file, the preview still opens and the offset stays 0, so Walker does not walk in.

## What the scene does

Resolution is **320×180**. Sampling is **nearest**, pixel rounding is on, image smoothing is off, and antialiasing is `none`. The game resolution does not adapt at runtime (`adaptGameResolutionAtRuntime` is false, resize mode is empty), so the logical scene stays 320×180. A window with another aspect gets black margins rather than a different game size.

One scene, `Main`, base layer then `HUD`:

| Object | Top-left | Z | Notes |
|---|---:|---:|---|
| Sky | (0, 0) | 0 | 320×180, does not scroll |
| HillsFar | (0, 0) and (640, 0) | 10 | scrolls at 4 px/s |
| HillsMid | (0, 0) and (640, 0) | 20 | scrolls at 8 px/s |
| TreesMid | (0, 0) and (640, 0) | 30 | scrolls at 12 px/s |
| Ground | (0, 0) and (640, 0) | 40 | scrolls at 20 px/s |
| Walker | (-48, 109) | 50 | walks to x = 136 |
| SnowStill | (0, 0) | 60 | static overlay, does not scroll |
| BethlehemStar | (239, 30) | 70 | hidden until a later slice |
| SongTime, CueMarks | HUD |  | timing tool |

Walker starts one 48×56 cell off the left edge, so it walks into frame. That start X was not given as a number; -48 is the off-screen cell. The centered top-left is (136, 109). It moves right at 20 px/s until X is 136 (9.2 s of music), then stays there while the four tile layers scroll. Each layer is two sprites one 640 px period apart. Their X is `-mod(speed * ScrollSeconds, 640) + TileCopy * 640`, so they wrap every 640 px.

Parallax speeds are starter defaults in the scene variables: far hills 4, mid hills 8, trees 12, and ground 20 px/s. The import notes leave the rates unset. Ground matches the walk speed. Sky and the static snow overlay stay in place.

The Walk animation is frames 1, 2, 3, 2 at 0.22 s, looping. Idle and LookUp are in the object and are not played yet. The origin stays the default top-left. Point `Pivot` is the artist's (24, 48) registration. The star's point `Anchor` is (11, 11). Neither point is the object origin, so the placed coordinates stay top-left.

The Walk cycle uses GDevelop's sprite animation clock. Positions and the HUD use the music offset, not a scene timer.

On the HUD layer, `SongTime` shows the channel-0 offset rounded to 0.01 s (`roundTo`, then `ToString`; trailing zeros are not padded). While the music is playing, Space (just pressed, so once per press) appends that offset and a newline to `CueMarks`.

Scene background color is the sky image's top-left pixel, RGB (17, 29, 53). The sky image covers the frame.

## Done in this slice

- `game.json` in the 5.6.287 project shape, scene `Main`.
- The nine selected images: sky, far hills, mid hills, trees, ground, static snow, the 24×24 scene star, and the two flake sprites. PNGs are unmodified. `bethlehem_star_chorus.png` and the review/seam stills are not imported.
- Walker frames from `art/assets/user-b-reduced-preview/`, unmodified.
- Music on channel 0, walk-in, then wrapping parallax.
- HUD song time and Space cue marks.
- `qa/cues.json` registered as the JSON resource `cues`. The file is the measured draft, timings unchanged.

## TODO

- Show the star before each chorus, play Idle then LookUp, and pan or zoom to the 5× chorus view (120×120, top-left (100, 30)). When the chorus ends, hide the star and return to Walk. Draft section times are in `qa/cues.json` and `qa/timing-notes.md`. Any of that still has to read the music offset.
- Falling snow. `SnowFlakeSmall` and `SnowFlakeNear` are objects with no instances. `SnowStill` is only the static overlay.
- Current lyric line. Loading `cues` into a scene variable needs the experimental [JSON Resource Loading](https://wiki.gdevelop.io/gdevelop5/extensions/jsonresource-loader/) extension (`JSONResourceLoader::LoadJSONToVariable`). It is not installed here. The cues are an automated draft (13 low confidence, 15 medium, none high), not a final sync.

The same TODOs are comment events at the top of the `Main` sheet.

## Art and cue status

`art/assets/user-b-reduced-preview/manifest.json` still says `UNAPPROVED_REDUCTION_PREVIEW_NOT_FINAL_IMPLEMENTATION`. The owner picked that set to import. Do not redraw, recolor, or resize it.

`qa/cues.json` is an automated measurement, not final-media approval. Do not edit the timings. `qa/lyrics-approved.txt`, `qa/timing-notes.md`, `qa/handoff.md`, and `art/selected-snow-import.md` are the notes that came with the inputs.

## A preview is not a video

GDevelop Preview, and a web or desktop export, run the scene as a game. They do not encode a lyric video. Capturing the picture and writing a video file is a later, separate step.

## What was checked

`python3 tools/validate_project.py` checks the JSON, the resource paths, the image hashes, and the scene layout.

The same `game.json` was loaded with the official editor core from <https://editor.gdevelop.io/libGD.js> and `libGD.wasm` (GDevelop **5.6.287-0**, platforms initialized with `gd.initializePlatforms()`). GDCore unserialized the project, read the Walker frames and the 0.22 s walk timing, and its expression validator accepted the event expressions, including `CueMarks.Text::Value()`. The Space condition stores the string expression `"Space"`.

The scene was not previewed or played. No desktop editor and no web export was launched, so playback, the parallax wrap, and the HUD are unverified at runtime.
