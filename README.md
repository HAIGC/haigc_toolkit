# HAIGC Toolkit for ComfyUI

<div align="center">

**专业的ComfyUI视频和图片处理工具集**

[![Version](https://img.shields.io/badge/version-2.0.1-blue.svg)](https://github.com/yourusername/haigc_toolkit)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![ComfyUI](https://img.shields.io/badge/ComfyUI-Compatible-orange.svg)](https://github.com/comfyanonymous/ComfyUI)

</div>

---

## 📖 简介

HAIGC Toolkit 是一套专为 ComfyUI 设计视频添加字幕节点。提供专业级的字幕添加、视频过渡，全中文界面，开箱即用。

## ✨ 核心特性

- 🎬 **专业字幕系统** - 支持渐变、描边、动效、横竖排版
- 🎨 **丰富视觉效果** - 28种字幕动效、3种渐变模式
- 🎯 **精确时间控制** - 支持帧数/秒数双模式
- 🌐 **全中文界面** - 无需英文基础，直观易用

## 📦 安装方法

### 方法一：手动安装（推荐）

1. 进入 ComfyUI 的 `custom_nodes` 目录
2. 克隆本仓库：
```bash
git clone https://github.com/HAIGC/haigc_toolkit.git
```

3. 安装依赖：
```bash
cd haigc_toolkit
pip install -r requirements.txt
```

4. **配置中文字体**（Linux 用户必读）：
   - 如果你使用 Linux 系统，需要安装中文字体以避免乱码
   - 详细配置指南：[字体配置指南](FONT_GUIDE.md)
   - 快速安装（Ubuntu/Debian）：
   ```bash
   sudo apt install fonts-noto-cjk
   fc-cache -fv
   ```

5. 重启 ComfyUI

### 方法二：直接下载

1. 下载本仓库的 ZIP 文件
2. 解压到 `ComfyUI/custom_nodes/haigc_toolkit`
3. 安装依赖（同上）
4. 配置中文字体（Linux 用户，参考上方步骤 4）
5. 重启 ComfyUI

### ⚠️ 重要提示

**Linux 用户必读：** 如果字幕显示为方框或乱码，说明系统缺少中文字体。请查看 [字体配置指南](FONT_GUIDE.md) 解决。

**Windows 用户：** 系统自带中文字体，无需额外配置。

## 🎯 节点列表

### 1. 视频字幕增强版 🎬

**节点名称：** `HAIGC_VideoSubtitleEnhanced`

强大的视频字幕添加节点，支持业界领先的特效和动画系统。

#### 核心功能

- **文字效果**
  - 3种渐变模式（线性、径向、对角）
  - 3级描边位置（外部、居中、内部）
  - 4级字体粗细（常规、粗体、特粗、超粗）
  - 字间距精细控制（-50到200px）
  - 横竖排版完整支持

- **动画效果**（28种）
  - 基础：淡入、淡出、滚动、飞入、缩放
  - 进阶：弹跳、旋转、波浪、闪烁、抖动
  - 专业：爆炸、螺旋、粒子聚合、光速飞入、弹簧抖动
  - 电影级：翻书、液体流动、闪电、碎片重组

- **精确控制**
  - 精确到百分位的时间控制（0.01秒）
  - 动效速度调节（0.1x - 5.0x）
  - 投影系统（角度、距离、强度、模糊）
  - 位置百分比定位
  - 不透明度控制

#### 使用示例

```
输入：
- 图像序列（IMAGE）
- 字幕文本："欢迎使用HAIGC工具集"
- 字体大小：48
- 动效类型：爆炸进入（增强）
- 开始时间：0秒
- 结束时间：5秒

输出：
- 带字幕的图像序列
- 视频时长
- 总帧数
- 字幕开始时间
- 字幕结束时间

```

---

### 2. 视频拼接过渡 🎞️

**节点名称：** `HAIGC_VideoTransition`

将两段视频平滑拼接，提供多种专业级过渡效果。

#### 过渡效果（15种）

- **基础过渡**：交叉淡化、淡入淡出（黑场/白场）
- **方向擦除**：左右上下渐变擦除、推移
- **几何扩散**：圆形扩散、方形扩散
- **创意效果**：溶解、缩放过渡

#### 高级特性

- 5种缓动函数（线性、缓入、缓出、缓入缓出、弹性）
- 可选颜色匹配（自动调整色调）
- 可选亮度平滑（避免明暗突变）
- 边缘羽化控制
- 灵活的过渡位置（视频A末尾/视频B开头/两者中间）

---

### 4. 视频尾帧提取 🖼️

**节点名称：** `HAIGC_VideoLastFrame`

从视频序列中提取尾帧，支持多种提取模式。

#### 提取模式

- **最后一帧**：提取视频的最后一帧
- **最后N帧**：提取视频的最后N帧
- **倒数第N帧**：提取特定位置的帧

#### 实用功能

- 重复输出控制（1-1000次）
- 帧信息详细输出
- 支持批量处理

---

### 5. 图片批次累积 📊

**节点名称：** `HAIGC_ImageAccumulator`

智能累积输入的图片，在合适时机批量输出，适用于批处理工作流。

#### 核心功能

- 智能累积管理
- 批次重复功能
- 手动/自动触发输出
- 缓存管理
- 实时状态监控

#### 使用场景

- 批量图片处理
- 视频帧序列合成
- 动态批次生成
- 工作流缓冲

---

## 🎨 功能展示

### 字幕效果组合示例

| 效果类型 | 支持横排 | 支持竖排 | 组合支持 |
|---------|---------|---------|---------|
| 渐变 | ✅ | ✅ | 渐变+描边+粗细 |
| 描边 | ✅ | ✅ | 描边+粗细+竖排 |
| 字体粗细 | ✅ | ✅ | 粗细+渐变+竖排 |
| 字间距 | ✅ | ✅ | 所有效果 |
| 动效 | ✅ | ✅ | 所有效果 |

---

### 基础工作流示例

```
[加载视频] → [视频字幕增强版] → [保存视频]
                  ↓
              字幕文本："你好，ComfyUI"
              动效类型：淡入
              开始时间：0秒
              结束时间：3秒
```

### 高级工作流示例

```
[视频A] →                    
         [视频拼接过渡] → [字幕节点]
[视频B] →                    ↓
                         [保存视频]
```

---

### 推荐配置

- **内存**：8GB+ RAM
- **显存**：4GB+ VRAM（用于视频处理）

---


## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - 强大的图像生成工作流平台
- 所有为本项目提供反馈和建议的用户

---

## 📮 联系方式
- **问题反馈**：请在 [GitHub Issues](https://github.com/yourusername/haigc_toolkit/issues) 提交
- **功能建议**：欢迎在 Issues 中讨论

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！**
Comfyui工作流云平台推荐：https://www.runninghub.cn/user-center/1887871050510716930/userPost?inviteCode=rh-v1127
国际站：https://www.runninghub.ai/user-center/1939305513756864513/userPost?inviteCode=rh-v1127

Made with ❤️ by HAIGC

</div>
