# 源码与构建材料

[English](BUILDING.md) | [简体中文](BUILDING.zh-CN.md) · [项目首页](../README.zh-CN.md)

本项目发布兼容代码、二进制补丁生成器和技术记录，供审阅及移植参考，不是能从零一键编译的完整 MIUI 相机源码。小米／高通专有处理算法源码和签名私钥没有包含在内。工具中的字节和哈希断言用于限定准确输入，请勿删除保护后套用其它二进制。

## 材料索引

- `tools/build_compat.py`：AArch64 producer-listener ABI 桥接汇编／ELF 生成及旧 MIVI 空探测保护。
- `tools/StreamMapBridge.java`、`tools/patch_streammap.py`：Android 17 Camera2 构造适配。
- `tools/SessionTrace.java`、`tools/prepare_trace.py`：当前应用保留的本地元数据诊断。
- `tools/build_frame_bridge.py`、`tools/patch_frame_decoder.py`、`patches/0001-stagefright-frame-decoder-copy-fallback.patch`：缩略图转换的缓冲区复制回退及对应框架源码改动。
- `tools/patch_cameraserver.py`、`patch_custom_stream.py`、`patch_surface_connect.py`、`patch_codec_xml.py`：分配、厂商流、Surface 和编解码声明适配。
- `tools/patch_ois_post_init.py`：针对精确旧驱动重用原始 OIS post-init 命令。
- `tools/patch_tinycompress_read.py`：双路采集音频的 AVAIL 重查，相关上游源码片段及许可头位于 `third_party/tinycompress`。
- `tools/package_ambilight_module.py`：精确缓存插件的 loader 名称适配及原分配器别名，两库处理代码段保持不变。
- `tools/package_ncs_module.py`：0.11 的 8 字节 SSC 取样起点修复。
- `tools/package_ncs_rollback.py`：专用回退安装器允许列表，保留原样 0.10 内容。
- `module-template/`：当前模块文本配置及 Magisk 脚本；APK 和 native 二进制在发布附件中，不写入 Git 历史。
- `records/`：精确哈希、补丁地址和发布内容清单。

## 输入与工具环境

历史脚本需要原始 `work/` 布局：`work/hyper14` 中的 odin OS1.0.8.0.UKMCNXM Android 14 提取分区、`work/lineage-hal` 中的精确 Lineage 库、已签名 APK／框架中间产物，以及按版本顺序建立的模块暂存目录。目标驱动 SHA-256 为 `054b477e19cd0cb8a015f0ce28295db6c688e14a022fed90ad5919caa12ef51c`，其它基线由各脚本和安装器断言限定。

Native 桥接使用 Keystone 组装及 Android SDK build-tools 36.0.0 的 lld 链接；Java 桥接使用 JDK、Android 平台类、d8 和 smali 工具。Python 依赖 LIEF、pyelftools、Keystone、Capstone。公开源码中的主机 SDK 路径统一为 `C:/Android/Sdk`，需按自己的环境调整。材料用于审阅及适配，不保证任意依赖版本下自动得到字节完全一致的构建。

初始模块脚本的旧项目 META-INF 输入路径已规范为 `../previous-port-inputs`；当前发布所用的准确文本位于 `module-template/META-INF`。审阅当前发布内容无需访问另一个私人工作目录。重新签名需使用自己的私钥，并可能影响升级兼容；本项目没有提供签名私钥。

将 0.10 模块内容提取至 `work/module-ambilight` 且 HAL 匹配断言后，可运行 `python tools/package_ncs_module.py` 生成 0.11，再运行 `python tools/package_ncs_rollback.py` 生成回退包。ZIP 容器时间戳及压缩参数可能使整体哈希不同，应结合 `records/ncs-module-manifest.json` 校验逐文件内容。更早的补丁还需要对应脚本列出的原始输入。

无需编译内核，本模块也不提供替代内核。设备树和内核源码链接见项目首页。专有组件权利不因本源码材料公开而变更，详见[第三方说明](../THIRD_PARTY_NOTICES.zh-CN.md)。


## 0.12 打包

运行 `python tools/package_first_start_module.py BASE_0_11_ZIP OUTPUT_ZIP`，保留所有二进制内容并校验 APK／HAL 哈希。仅替换 module.prop、service.sh、customize.sh，从 module-template 添加 first-start.sh 和 action.sh，记录见 records/first-start-build.json。
