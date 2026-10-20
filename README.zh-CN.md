# MIX 4 / LineageOS MIUI 相机移植

[English](README.md) | [简体中文](README.zh-CN.md)

面向小米 MIX 4（odin）的 **MIUI 相机 5.1.001130.2** 兼容移植，以 Magisk 模块形式发布。当前版本：**0.11.0-ncs-timestamp-range**，发布日期：2026-10-20。

## 支持环境

- Inkypen 的 LineageOS **24.0-20260815-UNOFFICIAL-gapps-odin**，Android 17 / SDK 37。
- 与该构建匹配的 5.4.302-inkypen-v2+ 相机驱动及系统、vendor 库。安装器会校验精确哈希，设备代号相同并不足以保证兼容。
- 实测使用 Magisk 30.7，SELinux 保持 **Enforcing**。模块不会刷入替代内核，也不刷写系统或 persist／校准分区。

这是针对特定构建的兼容版本，请勿绕过哈希检查，也不要直接套用于其它月份的 ROM、其它系统或设备。

## 下载

请前往 [v0.11.0 发布页](https://github.com/efface-yyy/LineageOS-MiuiCAM-odin/releases/tag/v0.11.0) 下载安装包。GitHub 自动生成的 Source code 压缩包不能作为 Magisk 模块安装。

| 文件 | 用途 |
|---|---|
| [0.11 安装包](https://github.com/efface-yyy/LineageOS-MiuiCAM-odin/releases/download/v0.11.0/odin_lineage_miuicamera_0.11.0-ncs-timestamp-range.zip) | 当前推荐安装的 Magisk 模块 |
| [0.10 专用回退包](https://github.com/efface-yyy/LineageOS-MiuiCAM-odin/releases/download/v0.11.0/odin_lineage_miuicamera_0.10.0-rollback-from-0.11.zip) | 仅在需要从 0.11 降级时使用，不需要同时安装 |
| [源码材料压缩包](https://github.com/efface-yyy/LineageOS-MiuiCAM-odin/releases/download/v0.11.0/odin_miuicamera_0.11.0-source-materials.zip) | 兼容代码、补丁生成脚本、模块文本配置和技术记录，不能刷入 |
| [SHA256SUMS.txt](https://github.com/efface-yyy/LineageOS-MiuiCAM-odin/releases/download/v0.11.0/SHA256SUMS.txt) | 发布附件的 SHA-256 校验值 |

安装前请阅读[安装与回退说明](docs/INSTALL.zh-CN.md)。

## 主要改动

保留小米原有处理路径，适配 Android 17 接口及分配器、编解码行为，包括 Camera2 构造函数、Surface ABI、缩略图转换回退、指定旧驱动的原厂 OIS post-init 提交、双路录像音频可用量重查，以及精确匹配的长曝光插件 ION 分配器适配。

0.11 修复了 SSC 陀螺取样窗口起点索引遗漏：原 HAL 按设定采样周期估算起点，实际采样周期较短时可能跳过已存在的真实样本。补丁仅修改两条指令，从最老有效索引进入原有的有界时间戳扫描。没有伪造样本或修改采样时间戳，保留 Vidhance 算法。

## 验证结论

**防抖功能已修复，本次转动实测未发现防抖功能异常，验收通过。** 修复前 6068 个短窗口中有 2177 个前端遗漏，修复后 6335 个短窗口中为 0。最终约 41 秒超级防抖转动录像的 1226 个视频帧、1919 个音频 buffer 均完整解码至 EOS，缩略图正常，未出现陀螺补偿失败、空 OIS 或 EIS 执行失败。

此结论针对本机、本构建及已执行的测试，不表示已证明所有场景与官方固件画质一致。详细范围及时间戳技术备注见[验证记录](docs/VALIDATION.zh-CN.md)。按设备持有者要求，0.11 后未追加测试其它模式。

## 依赖与运行行为

- 长曝光目前依赖相机已缓存的官方 **ambilight v1.3.5@20220126** 插件，适配有精确哈希保护。本发布包**没有打包全部九个可选原厂扩展模块**，未验证无缓存全新安装下的每项可选功能。
- 模块启动脚本会授予相机、录音、位置、存储权限并设置 appops。可查看 [service.sh](module-template/service.sh) 和 [SELinux 规则](module-template/sepolicy.rule)。
- 当前构建保留本地会话元数据跟踪，文件位于相机私有目录 `files/session-trace`。开启位置标记时，请求元数据可能含位置信息。兼容跟踪代码没有网络上传器，分享日志前请自行检查。
- 公开仓库不包含实机照片、视频、设备原始日志、用户设置、校准转储或签名私钥。

## 源码与致谢

本仓库提供兼容代码与二进制补丁生成器，**不是**小米／高通专有算法源码，也不是完整 ROM 或内核源码树。原始二进制仍属于相应第三方组件，历史工具需要匹配的原始输入。详见[源码与构建材料](docs/BUILDING.zh-CN.md)及[第三方说明](THIRD_PARTY_NOTICES.zh-CN.md)。

- 小米 MIUI 相机与高通 vendor 组件：原始应用、处理算法及硬件栈。
- Inkypen：[设备树](https://github.com/Inkypen79/device_xiaomi_odin)、[设备内核源码](https://github.com/Inkypen79/kernel_xiaomi_odin)、[原 ROM 帖子](https://xdaforums.com/t/rom-17-0-unofficial-lineageos-24-0-for-xiaomi-mix-4.4394723/)。
- [OIS post-init 上游修复](https://github.com/Inkypen79/kernel_xiaomi_odin/pull/4)：兼容提交的参考，本模块没有提供替代内核。
- AOSP、LineageOS、tinycompress 贡献者和 Magisk。

本模块问题请通过 GitHub Issues 反馈，附系统构建、模块版本和复现步骤。分享前检查日志，不要默认上传私人相机媒体或设备标识。
