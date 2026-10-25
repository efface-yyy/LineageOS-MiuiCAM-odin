# Source and build materials

[English](BUILDING.md) | [简体中文](BUILDING.zh-CN.md)

This is an audit and patch-source release, not a one-command clean source build of MIUI Camera. Proprietary Xiaomi/Qualcomm processing source and signing private keys are not available here. Tools use exact byte/hash assertions and must not be retargeted by deleting assertions.

## Included materials

- `tools/build_compat.py`: AArch64 producer-listener ABI bridge assembly/ELF generation, plus the legacy MIVI null-probe guard.
- `tools/StreamMapBridge.java`, `tools/patch_streammap.py`: Android 17 Camera2 constructor adaptation.
- `tools/SessionTrace.java`, `tools/prepare_trace.py`: local metadata-only diagnostic hook retained in the released app.
- `tools/build_frame_bridge.py`, `tools/patch_frame_decoder.py`, `patches/0001-stagefright-frame-decoder-copy-fallback.patch`: native copy fallback and corresponding framework source patch.
- `tools/patch_cameraserver.py`, `patch_custom_stream.py`, `patch_surface_connect.py`, `patch_codec_xml.py`: allocation, vendor stream, Surface and codec compatibility.
- `tools/patch_ois_post_init.py`: exact-driver original OIS post-init command reuse.
- `tools/patch_tinycompress_read.py`: concurrent capture AVAIL re-query; original tinycompress source excerpts with license headers are in `third_party/tinycompress`.
- `tools/package_ambilight_module.py`: exact cached ambilight loader-name adaptation and private original allocator alias. Both underlying `.text` sections are asserted unchanged.
- `tools/package_ncs_module.py`: the 0.11 eight-byte SSC timestamp-range entry repair.
- `tools/package_ncs_rollback.py`: dedicated rollback installer allowlist, unchanged 0.10 payload.
- `module-template/`: exact current text configuration and Magisk scripts; native binaries/APK are release assets, not in Git history.
- `records/`: exact hashes, patch sites and payload manifest for review.

## Inputs and environment

Historical scripts expect the original local `work/` layout: extracted odin OS1.0.8.0.UKMCNXM Android 14 partitions in `work/hyper14`, exact target Lineage binaries in `work/lineage-hal`, intermediate signed APKs/frameworks, and earlier staging directories for the sequential packaging scripts. The target driver hash is `054b477e19cd0cb8a015f0ce28295db6c688e14a022fed90ad5919caa12ef51c`. Library baselines are guarded in each generator and installer.

Native bridges are assembled using Keystone and linked using Android SDK build-tools 36.0.0 `lld`; Java bridges use JDK / Android platform classes, d8 and smali tooling. Python tools use LIEF, pyelftools, Keystone and Capstone. Host-specific SDK paths in this source copy were normalized to `C:/Android/Sdk`; adjust them for your own toolchain. Historical files are supplied for inspection and porting, not as an automated promise of byte-identical rebuilding on arbitrary dependency versions.

The base module builder's previous-port META-INF input was normalized to `../previous-port-inputs`. The exact release META-INF text is available in `module-template/META-INF`. No files from another private workspace are required just to inspect the current release. Re-signing an app requires your own key and can affect upgrades; no private signing material is provided.

The latest NCS patch is directly reproducible once the 0.10 module payload is extracted to `work/module-ambilight` and its guarded HAL matches. Run `python tools/package_ncs_module.py` to produce the guarded 0.11 payload, then `python tools/package_ncs_rollback.py` for rollback. ZIP container timestamps/compression may change the archive SHA; compare per-file payload hashes in `records/ncs-module-manifest.json`. Historical earlier patches have additional original-input requirements described by their paths and assertions.

No kernel build is needed or included. Kernel/device source links are in README. Source materials do not grant rights over proprietary OEM components; see third-party notices.


## 0.12 packaging

`python tools/package_first_start_module.py BASE_0_11_ZIP OUTPUT_ZIP` preserves all binary payloads and verifies the APK/HAL hashes. Only module.prop/service.sh/customize.sh are replaced; first-start.sh and action.sh are added from module-template. See records/first-start-build.json.
