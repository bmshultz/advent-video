# Timing handoff — Star of Bethlehem

**Status: automated cues measured; NOT final-media approved.** 28 approved-line cues; **13 low / 15 medium / 0 high**. Manual listening/uncertainty resolution is required before frame-accurate implementation. Shared OGG hash matches builder report; duration **183.212 s**, stereo Vorbis, 44,100 Hz.

| Section | Start (s) | End (s) | Confidence |
|---|---:|---:|---|
| INTRO | 0.000 | 36.180 | low |
| V1 | 36.180 | 72.840 | low |
| PRE-CH1 | 72.560 | 72.840 | low |
| CH1 | 72.560 | 90.580 | low |
| V2 | 90.640 | 107.760 | medium |
| BR | 108.160 | 125.460 | medium |
| PRE-CH2 | 125.460 | 126.320 | low |
| CH2 | 126.320 | 144.510 | low |
| PRE-CH3-INSTRUMENTAL | 144.510 | 159.840 | medium |
| CH3 | 159.840 | 180.140 | low |
| OUTRO | 180.140 | 183.212 | medium |

- Structure supports **3 chorus passes total**: CH1, then CH2/CH3 (two closing passes). BR labels the I-pray section; it may be called bridge or verse continuation editorially.
- No confirmed lyric discrepancy. Chorus ASR is too inconsistent to certify exact words. Approved text unchanged.
- No clean measured pre-CH1 / pre-CH2 instrumental gap: CH1 overlaps preceding modeled tail; CH2 nominal 0.860 s is uncertain, not silence. Before CH3: main-vocal gap 144.510–159.840 (15.330 s).
- Open: listen to all low-confidence cues, especially first verse onset and all chorus syllables/tails; settle display-clear convention; supply delivered frame rate; agree proposed ±2-frame onset tolerance (about ±80 ms at 25 fps). This draft does NOT demonstrate that precision.
- Provenance: verified only shared copy against builder-reported hash; no hash comparison with original chat attachment was established.

Files: `cues.json`, `timing-notes.md`, untouched `lyrics-approved.txt`; reproducible measurements/clips/logs in `work/`, all under `/workspace/lyric-video/qa/`.
