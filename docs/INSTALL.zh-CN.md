# 安装与回退

[English](INSTALL.md) | [简体中文](INSTALL.zh-CN.md) · [项目首页](../README.zh-CN.md)

## 安装前

仅用于小米 MIX 4／odin、Inkypen LineageOS 24.0-20260815-UNOFFICIAL-gapps-odin 及匹配的库和相机驱动。请准备备份及可用的 recovery／ADB 恢复方式，在手机之外保留回退包。其它相机替换模块可能冲突，避免盲目叠加；实测手机原有的 healthhal_autofix 模块予以保留。

## 安装步骤

1. 从 [v0.12.0 发布页](https://github.com/efface-yyy/LineageOS-MiuiCAM-odin/releases/tag/v0.12.0) 下载 **0.12 Magisk 模块 ZIP** 和 `SHA256SUMS.txt`。
2. 校验 SHA-256。PowerShell 可使用 `Get-FileHash -Algorithm SHA256 <zip>`；Linux 在所列文件齐全时可使用 `sha256sum -c SHA256SUMS.txt`。
3. 在 Magisk 的模块页面选择“从本地安装”，选中 ZIP。若安装器拒绝库或驱动哈希，请停止，不要移除保护条件。
4. 重启，打开 MIUI 相机并检查权限和设置。部分可选功能需要原始匹配插件缓存，详见项目首页。

源码材料 ZIP 和 GitHub 自动生成的源码压缩包都不能作为安装包。无需格式化数据或刷写内核／persist 分区。更换 ROM 构建前应先禁用模块；安装时的哈希检查不能自动保护 OTA 后已经挂载的旧模块。

## 从 0.11／0.12 回退

仅在需要降级时，通过 Magisk 安装 `odin_lineage_miuicamera_0.10.0-rollback-from-0.11.zip` 并重启。该包包含原样的 0.10 内容，仅安装器额外接受 0.11 HAL 哈希。旧的原始 0.10 安装包会拒绝直接覆盖已挂载的 0.11 HAL。

**正常使用安装 0.12 即可，不需要同时安装 0.10。**

若要移除移植，在 Magisk 中禁用或卸载 `odin_lineage_miuicamera` 并重启。系统无损挂载、属性和长曝光 bind 覆盖会撤销；相机应用数据、可选缓存插件、跟踪文件和拍摄媒体可能仍保留，模块卸载不会清除它们。不要删除其它模块或相机媒体。

若无法进入 Android，请使用现有 recovery／root 恢复途径，仅禁用本模块后重启。恢复命令与加密数据访问方式因安装环境而异。

## 首次引导初始化

启动后最多等待主用户（用户 0）解锁五分钟，仅在首次引导键缺失时初始化，不代同意联网／隐私协议。需要写入时会先停止相机，避免偏好覆盖；已有偏好在原目录私有备份，已有键保留。清除相机数据或较晚解锁后，请先点击模块操作按钮再打开相机。仅处理用户 0；停用模块不会撤销已写入的应用偏好。

ReSukiSU 用户仍需手动为相机关闭“卸载模块”；若桌面图标缺失，桌面也需保留挂载。无需授予 root，模块不会修改 root 管理器应用配置。
