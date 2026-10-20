# Install and roll back

[English](INSTALL.md) | [简体中文](INSTALL.zh-CN.md)

## Before installing

Use only Xiaomi MIX 4 / odin on Inkypen LineageOS 24.0-20260815-UNOFFICIAL-gapps-odin with the matching libraries and driver. Have a working recovery/ADB route and a backup. Keep the rollback ZIP available outside the phone. Other camera-replacement modules can conflict; do not combine them blindly. The tested device's existing healthhal_autofix module was retained.

## Installation

1. Download the **0.11 Magisk module ZIP** and `SHA256SUMS.txt` from this repository's release.
2. Verify the ZIP hash. For example, on PowerShell use `Get-FileHash -Algorithm SHA256 <zip>`; on Linux use `sha256sum -c SHA256SUMS.txt` with the listed files present.
3. In Magisk, open Modules, choose Install from storage, and select the ZIP. If the installer rejects a hash or driver, stop; do not remove the guard.
4. Reboot, then open MIUI Camera and review its permissions/settings. Optional OEM features may need the original matching plugin cache; see README.

The source-materials ZIP and GitHub source-code archives are not Magisk install packages. Installing this module does not require formatting data or flashing kernel/persist partitions. Disable it before changing ROM builds; an installer check cannot automatically protect an already mounted module after an OTA.

## Roll back from 0.11

Install `odin_lineage_miuicamera_0.10.0-rollback-from-0.11.zip` through Magisk and reboot. It has exactly the 0.10 payload; only its installer allowlist additionally recognizes the 0.11 HAL hash. The old original 0.10 ZIP will reject a direct downgrade while the 0.11 HAL is mounted.

To remove the port, disable or uninstall `odin_lineage_miuicamera` in Magisk and reboot. Systemless library mounts/properties and the ambilight bind overlay are then removed. Camera app data, optional cached modules, trace files and captured media may remain; uninstalling the module does not erase them. Do not delete unrelated modules or camera media.

If Android cannot be reached, use your existing recovery/root access to disable only this module and reboot. Preserve other working modules. Recovery commands and encryption access differ between installations.
