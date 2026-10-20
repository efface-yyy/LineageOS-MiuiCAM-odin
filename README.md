# MIUI Camera for MIX 4 / LineageOS

[English](README.md) | [简体中文](README.zh-CN.md)

MIUI Camera **5.1.001130.2** compatibility port for **Xiaomi MIX 4 (odin)**, distributed as a Magisk module. Current release: **0.11.0-ncs-timestamp-range**, 2026-10-20.

## Supported target

- Inkypen LineageOS **24.0-20260815-UNOFFICIAL-gapps-odin**, Android 17 / SDK 37.
- Matching 5.4.302-inkypen-v2+ camera driver and system/vendor libraries. The installer checks exact hashes; matching device name alone is insufficient.
- Tested with Magisk 30.7 and SELinux **Enforcing**. No kernel, calibration/persist or system partition flashing is performed.

This is a build-specific compatibility release. Do not bypass the hash checks or assume support for a different monthly build, ROM or device.

## Downloads

Use the [v0.11.0 release](https://github.com/efface-yyy/LineageOS-MiuiCAM-odin/releases/tag/v0.11.0), not GitHub's automatically generated source ZIP, for installation.

| File | Purpose |
|---|---|
| odin_lineage_miuicamera_0.11.0-ncs-timestamp-range.zip | Current Magisk module |
| odin_lineage_miuicamera_0.10.0-rollback-from-0.11.zip | Dedicated rollback to 0.10; recognizes the 0.11 HAL hash |
| odin_miuicamera_0.11.0-source-materials.zip | Compatibility source, patch generators, module text files and technical records; not flashable |
| SHA256SUMS.txt | SHA-256 checksums of the assets |

Read [installation and rollback](docs/INSTALL.md) before installing.

## What changed

The port adapts Android 17 interfaces and allocation/codec behavior while retaining the original Xiaomi processing paths. It includes Camera2 constructor and Surface ABI compatibility, thumbnail decoding fallback, original wide OIS post-init submission on the identified older driver, concurrent recording audio availability re-query, and an ION allocator compatibility route for the exact cached ambilight plugin.

0.11 fixes an SSC gyro range-start selection defect. The HAL estimated the start index using a configured sample period, which could omit existing real samples when the actual period was shorter. Two instructions now enter the existing bounded timestamp scan from the oldest valid index. Samples and timestamps are not fabricated or retimed; Vidhance is retained.

## Validation

**Stabilization was accepted on the tested device/build: no stabilization function error was observed in the final rotation test.** In 6,335 short raw requests after the fix, no known existing front-of-window sample was omitted, compared with 2,177 omissions in 6,068 requests before the fix. The final approximately 41-second super-steady rotation recording decoded all 1,226 video frames and 1,919 audio buffers to EOS, with a valid thumbnail and no gyro compensation failure, empty OIS or EIS execution failure.

This is not a promise of identical stock-firmware image quality or exhaustive correctness. See [validation scope and timing notes](docs/VALIDATION.md). Other modes were not retested after 0.11, at the device owner's request.

## Important dependencies and behavior

- Long exposure currently depends on the official ambilight **v1.3.5@20220126** plugin already cached by the camera. Its loader adaptation is exact-hash guarded. The nine optional OEM split modules are **not** all bundled in this release; a clean install without the cache was not validated for every optional feature.
- The module grants camera/audio/location/storage permissions and configures app operations in its service script. Review `module-template/service.sh` and `module-template/sepolicy.rule`.
- The build retains local metadata session tracing under the camera's private `files/session-trace` directory. Capture-request metadata may contain location when location tagging is enabled. There is no network uploader in the compatibility trace code. Do not publish those files without reviewing them.
- No test photos, videos, device logs, user preferences, calibration dumps or signing private keys are included in this repository.

## Source and credits

This repository contains compatibility code and binary patch generators, **not** Xiaomi/Qualcomm proprietary algorithm source or a full ROM/kernel tree. Original binaries remain third-party components. Historical tools require the exact original inputs; see [source/build materials](docs/BUILDING.md) and [third-party notices](THIRD_PARTY_NOTICES.md).

- Xiaomi / MIUI Camera and Qualcomm vendor components: original application, processing and hardware stack.
- [Inkypen's device tree](https://github.com/Inkypen79/device_xiaomi_odin) and [device kernel source](https://github.com/Inkypen79/kernel_xiaomi_odin).
- [Original LineageOS ROM thread](https://xdaforums.com/t/rom-17-0-unofficial-lineageos-24-0-for-xiaomi-mix-4.4394723/).
- [Inkypen kernel OIS post-init fix](https://github.com/Inkypen79/kernel_xiaomi_odin/pull/4), used as the reference for the compatibility submission; this module does not ship a replacement kernel.
- AOSP, LineageOS, tinycompress contributors and Magisk.

Use GitHub Issues for this module, with ROM/build, module version, reproduction steps and only carefully reviewed logs. Do not post private camera media or device identifiers by default.
