# Third-party components and attribution

[English](THIRD_PARTY_NOTICES.md) | [简体中文](THIRD_PARTY_NOTICES.zh-CN.md)

This repository does not claim ownership of Xiaomi MIUI Camera, Qualcomm camera/vendor libraries, Magisk, Android, LineageOS, Intel tinycompress or any firmware algorithms. There is no blanket relicensing of the packaged OEM application, vendor blobs or upstream code. Each third-party component retains its upstream terms. Compatibility sources are published for review; no whole-project license is asserted over mixed third-party material.

- Xiaomi: MIUI Camera 5.1.001130.2 and original odin OS1.0.8.0.UKMCNXM application/framework/allocator inputs. Proprietary algorithm source is not included.
- Qualcomm and vendor contributors: target ROM camera HAL/EIS/Vidhance stack. The Lineage target HAL is retained with exact compatibility edits; no full stock HAL replacement or replacement kernel is shipped.
- Inkypen: odin LineageOS/device/kernel integration. Device tree: https://github.com/Inkypen79/device_xiaomi_odin ; kernel: https://github.com/Inkypen79/kernel_xiaomi_odin ; OIS reference: https://github.com/Inkypen79/kernel_xiaomi_odin/pull/4 .
- AOSP / LineageOS framework media components: source reference https://android.googlesource.com/platform/frameworks/av/ and https://github.com/LineageOS/android_frameworks_av . Corresponding FrameDecoder source change and exact binary adaptation are included.
- tinycompress: https://github.com/LineageOS/android_external_tinycompress . Source excerpts preserve their original dual BSD/LGPL notices below. The compatibility change and exact original/patched library hashes are included; no kernel code is redistributed by this module.
- Magisk: https://github.com/topjohnwu/Magisk . Module install scaffolding uses Magisk's normal update-binary flow; see its upstream terms.
- Build tooling (not bundled): LIEF, Keystone, Capstone, pyelftools, Android SDK, smali tooling, Java.

## tinycompress source notice

```text
/*
 * BSD LICENSE
 *
 * tinycompress library for compress audio offload in alsa
 * Copyright (c) 2011-2012, Intel Corporation
 * All rights reserved.
 *
 * Author: Vinod Koul <vinod.koul@linux.intel.com>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 * Neither the name of Intel Corporation nor the names of its contributors
 * may be used to endorse or promote products derived from this software
 * without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
 *
 * LGPL LICENSE
 *
 * tinycompress library for compress audio offload in alsa
 * Copyright (c) 2011-2012, Intel Corporation.
 *
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms and conditions of the GNU Lesser General Public License,
 * version 2.1, as published by the Free Software Foundation.
 *
 * This program is distributed in the hope it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
 * License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program; if not, write to
 * the Free Software Foundation, Inc.,
 * 51 Franklin St - Fifth Floor, Boston, MA 02110-1301 USA.
 */
```
