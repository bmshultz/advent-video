# Selected snow scene + chunky star — import appendix

## Selection and scope
Builder relays Brian explicitly selected **“Use the snowy scene with the chunky enlarged right star.”** Builder also relays direct confirmation of **GDevelop scene320×180** and sprite object **Walker**. This records builder-relayed user selection,not independent verification by this art executor. It supersedes the earlier open star-choice question in root handoff. Selected:snow-star-review-v1 landscape +24×24 SCENE star enlarged intentionally by integer5×for closeup. **Do NOT select the separately designed128×128 `bethlehem_star_chorus.png`.** Historical review manifests retain their original proposal provenance/status unchanged.

## Coordinate convention
All coordinates below are logical320×180scene pixels,zero-based. XY is the IMAGE CELL TOP-LEFT,not opaque bounding box. PNGs do not encode a GDevelop custom origin. Suggested depths merely reproduce compositing order back→front;builder must verify engine origin,scale,pixel snapping,filtering,tiling and Z behavior. No motion/sync/export certification.

## Separate scenery imports (all file dimensions checked with Pillow)

| Suggested object | Exact box path | Image dimensions / alpha | Reference top-left | Suggested depth | Repeat |
|---|---|---|---|---:|---|
|Sky|`/workspace/lyric-video/art/assets/snow-star-review-v1/snow_sky_base.png`|320×180;opaque|[0, 0]|0|none|
|HillsFar|`/workspace/lyric-video/art/assets/snow-star-review-v1/snow_hills_far_tile.png`|640×180;binary transparent|[0, 0]|10|horizontal640px only;no vertical repeat|
|HillsMid|`/workspace/lyric-video/art/assets/snow-star-review-v1/snow_hills_mid_tile.png`|640×180;binary transparent|[0, 0]|20|horizontal640px only;no vertical repeat|
|TreesMid|`/workspace/lyric-video/art/assets/snow-star-review-v1/snow_trees_mid_tile.png`|640×180;binary transparent|[0, 0]|30|horizontal640px only;no vertical repeat|
|Ground|`/workspace/lyric-video/art/assets/snow-star-review-v1/snow_path_ground_tile.png`|640×180;binary transparent|[0, 0]|40|horizontal640px only;no vertical repeat|
|SnowStill|`/workspace/lyric-video/art/assets/snow-star-review-v1/snow_verse_static_overlay.png`|320×180;binary transparent|[0, 0]|60|none|
|BethlehemStar|`/workspace/lyric-video/art/assets/snow-star-review-v1/bethlehem_star_scene.png`|24×24;binary transparent|[239, 30]|70|none|

Each640×180layer begins at[0,0];the review samples its left320columns,not a resized tile. Adjacent repeats have top-lefts[−640,0],[0,0],[640,0],etc.;period is640,not641. All4tile layers have exact matching boundary RGBA columns and3tile seam tests in review folder. Sky stays separate/opaque. Main star and Walker are NOT baked into tiles. No parallax rates or scroll speeds prescribed.

`SnowStill` is a SINGLE STATIC placement overlay,NOT falling-snow animation. For independently moving flakes instead,optional small imports are:
- `/workspace/lyric-video/art/assets/snow-star-review-v1/snow_flake_small.png` — 3×3,binary transparency,suggested object`SnowFlakeSmall`,depth60. No fixed XY or motion assumed.
- `/workspace/lyric-video/art/assets/snow-star-review-v1/snow_flake_near.png` — 5×5,binary transparency,suggested object`SnowFlakeNear`,depth60. No fixed XY or motion assumed.

To reproduce the existing overlay using separate flakes:small source-cell ink at[1,1],so subtract[1,1]from target ink locations[19,42],[67,96],[102,113],[215,104],[302,73],[292,127],[37,152],[229,161]. Near-flake ink starts[2,2],so subtract[2,2]from target ink origins[77,143],[258,148],[13,112]. These describe only the reviewed STILL,not approved animation or density changes.

## Walker — existing selected source B,not A/rejected redraw
Suggested depth50;all cells48×56,no resizing. Native image top-left[136,109]. Existing local reference ground anchor[24,48]therefore maps to scene[160,157];last opaque foot/crop row47 maps to scene y156. Ground boundary y157 is a source-crop registration reference,NOT recovered anatomical sole or collision certification. If builder configures custom object origin[24,48],the equivalent position is[160,157];do not use top-left[136,109]as though already a pivot coordinate.

Exact frames:
1. `/workspace/lyric-video/art/assets/user-b-reduced-preview/01-walk-01-48x56.png`
2. `/workspace/lyric-video/art/assets/user-b-reduced-preview/02-walk-02-48x56.png`
3. `/workspace/lyric-video/art/assets/user-b-reduced-preview/03-walk-03-48x56.png`
4. `/workspace/lyric-video/art/assets/user-b-reduced-preview/04-idle-48x56.png`
5. `/workspace/lyric-video/art/assets/user-b-reduced-preview/05-look-UP-48x56.png`

Walk uses THREE unique frames,sequence1→2→3→2 at220ms/beat(880ms loop);frame4is idle/stop,frame5original chin-up. The review verse uses frame1;look-up still uses frame5. Sprite pixel files and visual source remain unchanged. No numbered sheets or enlarged previews should be used as Walker animation images.

## Selected star: exact scene and close-up mappings
**Import:** `/workspace/lyric-video/art/assets/snow-star-review-v1/bethlehem_star_scene.png` —24×24,binary transparency,visible bounds[2,2,22,22)exclusive,suggested depth70. It is the same star for BOTH distant scene and selected chunky close-up.

- Scene review:scale1,image top-left[239,30]. Authored local custom anchor[11,11]maps to scene[250,41]. Full-cell geometric center[12,12]maps to[251,42]. These are deliberately distinguished;do not silently treat the custom anchor as the geometric center.
- Selected RIGHT comparison close-up:nearest-neighbor integer5×of24×24→120×120,top-left[100,30]. Full-cell geometric center becomes[160,90]. Scaled custom anchor[55,55]maps to[155,85]. To reproduce selected reviewed image,keep these values.
- If builder instead intentionally centers the CUSTOM anchor at[160,90],top-left would be[105,35]. That is a5px repositioning versus reviewed image,not its recorded placement.
- With custom origin enabled,coordinate/scale math is a reference mapping only;builder verifies GDevelop's object-origin behavior. Do not invent a change of pivot while swapping between reference XY conventions. Integer enlargement adds NO detail. Use nearest sampling,not filtered bloom/smooth blur.

Close-up reference uses **Sky + enlarged scene star only**:same sky top-left[0,0],no hills,Walker or snow in that particular star study. Scene still uses all layers above. Director/builder owns transitions and timing;none specified by this import map.

Reference compositions (OPAQUE review images,NOT separate star or scenery-layer imports):
- `/workspace/lyric-video/art/assets/snow-star-review-v1/verse-snow-review.png`320×180
- `/workspace/lyric-video/art/assets/snow-star-review-v1/stop-look-UP-star-review.png`320×180
- `/workspace/lyric-video/art/assets/snow-star-review-v1/chorus-star-integer5x-review.png`320×180 — selected chunky close-up reference
- `star-options-designed-left-integer-right.png`640×180 — RIGHT selected;LEFT not selected.

Do NOT import `bethlehem_star_chorus.png`,designed-star closeup,comparison sheet or6×review PNGs as the selected scene star. No new star asset or art redraw was necessary. Review layer files unchanged. JSON counterpart:`/workspace/lyric-video/art/selected-snow-import.json`includes verified dimensions,source paths,mappings and original review-file hashes.

## Remaining implementation limits
Selection is visual,not certification of engine execution. Original source soles remain cropped,alpha estimated;lyrics placement,camera/scroll timing,snow animation,locomotion displacement,collision/ground alignment and export/sync behavior are builder/director responsibilities. Review-v1palette/detail files stay intact;no retroactive rewriting of historical approval status.
