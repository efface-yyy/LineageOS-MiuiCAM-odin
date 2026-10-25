# Changelog

[English](CHANGELOG.md) | [简体中文](CHANGELOG.zh-CN.md)

## 0.12.0 — 2026-10-26

- Initialize only a missing first-use hint after user unlock; keep existing preferences and CTA/network consent unchanged.
- Add a module action button to retry after camera data clearing.
- APK, native algorithms, HAL and stabilization patches are byte-identical to 0.11.
- ReSukiSU app profiles are not automatically changed.

## 0.11.0 — 2026-10-20

- Fix SSC synchronous gyro range-start omission by using the existing bounded timestamp scan from the oldest valid ring index.
- Retain original Vidhance processing and real samples/timestamps.
- Include a dedicated 0.10 rollback package accepting the current HAL hash.
- Ordinary EIS and static/rotation super-steady checks completed on the exact target build.

## 0.10.0

- Exact ambilight loader/ION allocator compatibility, preserving plugin/allocator processing instructions.

## 0.8.0

- Re-query compressed capture availability after POLLIN, repairing the second concurrent recording audio path.

## 0.7.0 and earlier

- Original wide OIS post-init submission compatibility for the identified driver.
- Codec declarations, thumbnail copy fallback, Surface and Camera2 ABI, vendor stream/gralloc and targeted SELinux compatibility.

0.9's unsuccessful private allocator preload experiment is superseded and is not a recommended release.
