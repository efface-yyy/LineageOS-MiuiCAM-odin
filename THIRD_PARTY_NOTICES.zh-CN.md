# 第三方组件与致谢

[English](THIRD_PARTY_NOTICES.md) | [简体中文](THIRD_PARTY_NOTICES.zh-CN.md) · [项目首页](README.zh-CN.md)

本项目不主张对小米 MIUI 相机、高通 vendor 库、Magisk、Android、LineageOS、Intel tinycompress 或固件算法的所有权，也没有为这些混合第三方材料统一重新授权。各组件保留原有条款；兼容源码公开用于审阅，不代表专有组件权利随之改变。

| 组件 | 来源与说明 |
|---|---|
| 小米 MIUI 相机 | 5.1.001130.2，以及 odin OS1.0.8.0.UKMCNXM 原始应用／框架／分配器输入；未包含专有算法源码 |
| 高通及 vendor 贡献者 | 目标 ROM 的相机 HAL／EIS／Vidhance 栈；保留 Lineage 目标 HAL 并作精确兼容改动，不整体替换为官方 HAL，也不分发替代内核 |
| Inkypen | [设备树](https://github.com/Inkypen79/device_xiaomi_odin)、[设备内核](https://github.com/Inkypen79/kernel_xiaomi_odin)、[OIS 参考修复](https://github.com/Inkypen79/kernel_xiaomi_odin/pull/4) |
| AOSP／LineageOS 媒体框架 | [AOSP frameworks/av](https://android.googlesource.com/platform/frameworks/av/)、[LineageOS frameworks_av](https://github.com/LineageOS/android_frameworks_av)；包含对应 FrameDecoder 源码补丁及精确二进制适配 |
| tinycompress | [上游仓库](https://github.com/LineageOS/android_external_tinycompress)；所附源码片段保留 BSD／LGPL 双许可声明，兼容改动及原始／修改后库哈希一并提供 |
| Magisk | [上游项目](https://github.com/topjohnwu/Magisk)；模块使用标准 update-binary 安装流程，条款以其上游为准 |
| 构建工具（不随包提供） | LIEF、Keystone、Capstone、pyelftools、Android SDK、smali 工具及 Java |

tinycompress 完整英文许可头保留在 [英文第三方说明](THIRD_PARTY_NOTICES.md#tinycompress-source-notice) 及 `third_party/tinycompress` 源码内，本中文说明不替代原始许可文本。本模块没有分发内核代码。
