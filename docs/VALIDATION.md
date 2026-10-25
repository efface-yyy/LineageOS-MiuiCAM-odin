# Validation scope

[English](VALIDATION.md) | [简体中文](VALIDATION.zh-CN.md)

Test date: 2026-10-20. Device: MIX 4 / odin. Target: Inkypen LineageOS 24.0-20260815, Android 17, matching 5.4.302 kernel driver. SELinux Enforcing. No replacement kernel was flashed. Stock-firmware side-by-side comparison was cancelled by the device owner.

## 0.11 stabilization acceptance

No stabilization function error was observed in the final USB-connected slow-rotation test. It ran without Frida or kernel hooks; an independent read-only gyro/accelerometer observer confirmed actual movement. Recording-window gyro count was 4,288; peak 1.515 rad/s and 95th percentile 0.996 rad/s.

| Check | Result |
|---|---|
| Raw short-request start omission, before | 2,177 of 6,068 requests, window at most 100ms |
| Raw short-request start omission, after | 0 of 6,335 requests; original sample values/timestamps retained |
| Ordinary EIS, 0.11 | 24.978s; 745 video frames and 1,170 audio buffers decoded to EOS; valid thumbnail |
| Static super steady, 0.11 | 40.917s; 1,226 video / 1,918 audio to EOS; no compensation failure |
| Slow-rotation super steady, 0.11 | 40.955s; 1,226 video / 1,919 audio to EOS; no compensation failure, empty OIS, EIS execution failure or fatal |

Ordinary EIS frequency-variation messages were checked separately: all 3,072 observed native validation calls returned valid, including 1,536 OIS calls. The over-1% variation branch logs and continues; it was not disabled.

### Timing and coverage notes

The rotation clip retains two PTS intervals around 66.6ms: frame index 275 at 9.241033s (66.667ms), and index 284 at 9.574167s (66.556ms). Neither coincided with a logged gyro compensation failure. Their origin was not established, so they are not classified as a confirmed stabilization fault. Complete decode does not establish that upstream delivered every nominal frame.

The raw trace also contains one startup query longer than the available cache and three short-request tail snapshot differences. The reported zero refers specifically to the repaired front-index omission, not full coverage of every possible request. Hooked read latency p50/p95 was 1/3ms after and 1/4ms before; this is diagnostic observation, not a performance benchmark. An initial tracing-tool loader-lock stall was cleared before successful later runs and is not counted as a passing test.

Only slow rotation was repeated after the fix, not another walking or stock-ROM comparison. Sparse image checks found no sampled black frames; no numerical stabilization-gain claim is made.

## Earlier functional evidence

Earlier module versions were exercised for front/rear JPEG, HDR multi-frame processing, night mode, 108MP, physical telephoto still capture in bright conditions, 1080p/4K60/8K, HDR10+ dynamic metadata, RAW, slow motion, timelapse, dual recording, thumbnails and ambilight long exposure. 0.10 fixed dual recording's second audio path and the exact ambilight allocator incompatibility.

Those are earlier-version results, not a claim that all modes were retested on 0.11. Full moving panorama stitching, complete VLOG template assembly, real moon/dark-scene quality, uninterrupted physical-telephoto video and every parameter combination were not exhaustively validated. Further non-stabilization testing was cancelled by the device owner. Private captures and raw device logs are intentionally excluded from this release.

## 0.12 startup regression — 2026-10-26

Magisk 30.7 installation and reboot passed. A deliberately missing first-use hint was restored by the boot worker after unlock; CTA remained false. Repeated module action execution preserved the preference-file hash. Camera cold start and preview passed with SELinux Enforcing. This update did not repeat capture/video or the full feature matrix. See records/first-start-validation.json.
