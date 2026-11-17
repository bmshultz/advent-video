# User-B r2 reduced preview — NOT approved final art/implementation

Start:numbered-review-6x.png (1440×480). Native:numbered-review-native.png (240×80). Pose1–3 walking;4 original idle/stop;5 original chin-up look. This is the LATEST source-B r2,not rejected B or A.

All5transparent cells48×56. Visible sizes:17×42,14×42,15×42,10×42,11×42 respectively. Every frame has topy6,bottomy47,common pivot[24,48]. One identical isotropic scale0.03045685279 maps the700×1440source registration canvas into a padded48×56cell;no squishing or per-pose fitting. Static pose original lower-body registration retained;up-tilt not canceled by separately re-centering the head.

Clean atlas:sprite-atlas-48x56.png (240×56);enlarged atlas:sprite-atlas-6x.png (1440×336). Individual files01-walk-01-48x56.png through05-look-UP-48x56.png. Binary0/255alpha,no smoothing. Baked checker removed from original static pose copies by subject mask;black sunglasses/skin/hair source colors retained. No checker carried into reduced PNGs. Original full-resolution static files untouched.

Walk:walk-220ms-native.gif48×56;walk-220ms-6x.gif288×336. THREE unique walk sprites,order1→2→3→2. Verified GIF encoding220ms×4=880ms loop. Optional walk-stop-look-UP-6x.gif includes original stop then original up-look;not a newly animated head tilt.

Numbers are separate review pixels,not in atlas/frames. First number ink row68;rows48–67are exactly20empty logical rows after lowest sprite pixel47. At6×the gap is120displaypixels. Source original cropped soles remain cropped;the common pivot is based on source crop,not a recovered true shoe sole or gameplay ground contact.

Inspected actual6×numbered sheet:source-B identity retained,clear idle/chin-up difference,none clipped,bodyaspect preserved,no visible checker. Tiny reduction loses some face detail and subtle r2arm movement;pixel stair-stepping/aliasing is expected from nearest-neighbor,not a redesigned pose. This is a size comparison for Brian,not approval of a final palette,scale,scene or engine implementation. No shoe reconstruction,new anatomy,or new face. Scale and resulting artwork remain unapproved.

Source edits/rebuild:../../source/user-b-reduced-preview/build_reduced.py. Metadata/checks:manifest.json,qa-metrics.json. Previous r2source/assets/JPEG unchanged(hash comparisons passed).
