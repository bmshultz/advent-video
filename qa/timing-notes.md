# Lyric timing measurements — automated draft, not media approval

## Source identity and timebase
- Supplied file: `/workspace/lyric-video/audio/star-of-bethlehem-2024.ogg`; **SHA-256 MATCH**: `b44a5a86f02192f5589e409383429dbc334f3624ea0daa3564b9ebcc2226c933`; 4,550,618 bytes.
- Vorbis in OGG, stereo, 44,100 Hz. Decoded length: 8,079,647 samples = 183.211950113 s (displayed 183.212 s).
- Seconds from decoded sample 0, three decimals; no leading-silence trimming or offset correction. ffprobe start_time 0, initial_padding 0. No extra encoder offset was established. Three decimals are formatting, not claimed millisecond accuracy.
- FFmpeg -50 dB silence detector: near-silence 0.000–0.983424 and 182.471474–183.211950 s. Intro includes the first interval. Demucs padded its end by 33 samples; excess end samples were not used as song duration.

## Method and what was actually measured
1. ffprobe and SHA-256 against the supplied file only; FFmpeg decoded all 8,079,647 samples.
2. stable-ts forced alignment with **small.en and medium.en**, CPU int8, on unchanged approved text, one output cue per approved sung line. The final `chorus x2` instruction was expanded into two working-copy chorus passes, not written into or substituted for the approved file.
3. Demucs htdemucs vocal isolation (shifts=0), then section-constrained forced alignment. Full-track alignment was rejected because it collapsed early verse lines into the intro. Section windows were informed by ASR/energy, not a presumed beat grid. Later expanded chorus windows exposed substantial window sensitivity.
4. Free transcription was only a cross-check: full mix small.en, isolated vocals medium.en, and extracted vocal clips at 36–42, 72.5–90.6, 120.9–126.4, 126.1–146.5, and 161–182 s. Raw results and clips are in `work/`. The vocal ASR is especially unreliable on chorus growls; hallucinated intro syllables and end “Thank you” are not accepted lyrics.
5. Vocal-band RMS (200–5000 Hz Butterworth, 10 ms bins) sanity checks. CH3 onset = sustained 80 ms above -35 dBFS at 159.840. CH2/CH3 main-vocal ends = sustained 150 ms below -35 dBFS at 144.510 / 180.140. These are reproducible acoustic thresholds, not proof of a word boundary. In particular first-verse lead-in, chorus syllables and tails remain uncertain.

No human listening pass was performed. There are **28 line cues, 13 low-confidence, 15 medium-confidence; none rated high**. The results are automated measurements with explicit unresolved timing, not a frame-accurate approved sync sheet. Confidence reasons and alternate model boundaries are attached to every cue.

## Structure and measured intervals
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

Three chorus passes are supported by the repeated phrase blocks: one after verse 1 and two after the I-pray section, with an instrumental interlude before the final pass. No fourth full chorus detected. This supports the supplied `chorus x2` reading, but does not certify every chorus word. BR is a convenient editorial label for the I-pray section, not an objectively named musical section.

Pre-chorus warning: CH1 overlaps the prior modeled God tail by 0.280 s. CH2 has a nominal 0.860 s interval between selected endpoints but continuous vocal energy and uncertain onset: **not an established instrumental gap**. Before CH3 there is a 15.330 s main-vocal gap, 144.510–159.840, with initial reverb/leakage. Use none of these as a designed star cue without resolving the uncertain cases. No scene design was done.

## Transcription discrepancies (separate from timing)
**No confirmed text discrepancy established.** Approved text was preserved. Some ASR runs propose words such as “Why/But I'm” instead of “I'm”, or “open hand” instead of “open hands”; other runs contradict them and heavily corrupt adjacent chorus words. These are unconfirmed transcription candidates, not grounds to edit lyrics. Vocal-like intro effects and ASR-generated final “Thank you” were not promoted to lyric cues. Exact wording, especially all chorus lines, still needs a human listen. Metadata UNSYNCEDLYRICS retains the old manager/woul typos; metadata is not evidence that those typos were sung. The approved corrections remain manger/would.

## Timing uncertainties (separate from transcription)
- V1-L01 chosen 36.180 onset comes from short-clip ASR; forced alignments stick to 35/36 s window edges. First strong isolated-vocal attack is nearer 37.1 s. Actual first lexical attack unresolved.
- V1-L02 and V2-L02 onsets differ by 0.340 s between models; BR-L06 end differs by 0.400 s.
- Every chorus line is low-confidence. Sustained/distorted vocals cause zero-duration tokens, missed words, and crop-edge pinning. CH1-L01 tail: tight models end 76.500–76.560 but expanded result 78.380. CH2-L01 onset: expanded result falsely pins to 124.500; narrow runs give 126.540–126.640; selected full-vocal ASR estimate 126.320 remains provisional. CH3 onset has acoustic support at 159.840, but tight-window aligners miss it by over two seconds. CH3-L01 aligned tail 164.980 is not a demonstrated end of all sustained/backing vocals.
- CH1-L03 onset differs from free-ASR estimates by roughly 0.7–1.1 s. Chorus tails overlap other vocal activity; end times are not automatic text-clear commands.
- CH2/CH3 main-vocal ends use explicit energy thresholds; diffuse reverb continues later. Energy cannot by itself separate lead words from breaths/backing vocals or leakage.
- No final video, delivered frame rate, or rendered soundtrack offset has been checked. Do not certify final media from this sheet.

## PROPOSED final-media QA tolerance — Brian agreement pending
After uncertain references are resolved, propose lyric onset within **±2 frames at the delivered frame rate**: ±83.3 ms at 24 fps, ±80 ms at 25 fps, ±66.7 ms at 30 fps. Agree a held-note-tail/text-clear convention separately; do not silently cut the display at an ASR word end. This is a proposed acceptance tolerance, **not achieved accuracy of this draft**.

## Provenance limitation
The builder reported that the shared file is an unmodified copy of its mounted bot-files OGG. This QA run independently confirms the shared file's bytes/hash match the builder-reported values. **The builder could not hash-compare that mounted file with the original chat attachment; no such comparison is claimed here.** The public song URL was not downloaded or used as the timing reference. `lyrics-approved.txt` was left untouched; its old NOT YET ACCESSIBLE header is historical, superseded by these notes.

## Tools / evidence
FFmpeg/ffprobe 7.1.5; package versions: `{"stable-ts": "2.19.1", "faster-whisper": "1.2.1", "torch": "2.15.0+cpu", "torchaudio": "2.11.1+cpu", "demucs": "4.1.0", "av": "16.1.0", "numpy": "2.5.4", "scipy": "1.18.1", "soundfile": "0.14.0"}`. Working scripts, model outputs, five extracted clips, separated vocals, decoded reference, energy arrays and logs are in `work/`; QA-local environment/cache are `.venv/` and `.cache/`. All project writes were confined to `qa/`.
