# HAIGC Toolkit for ComfyUI

<div align="center">

[中文](README.md) | [English](README_EN.md)

[![Version](https://img.shields.io/badge/version-3.3.8-blue.svg)](version.py)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![ComfyUI](https://img.shields.io/badge/ComfyUI-Compatible-orange.svg)](https://github.com/comfyanonymous/ComfyUI)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)

**🎬 Professional Video and Image Processing Toolkit for ComfyUI**

Powerful node collection focused on subtitle processing and video transitions

[Features](#-key-features) • [Installation](#-installation) • [User Guide](#-user-guide) • [Nodes](#-node-list) • [Changelog](#-changelog)

</div>

---

## 📦 Node List

### 🎬 Subtitle Nodes

#### 1️⃣ Video Subtitle Enhanced v2.5.0
**Best for**: Single subtitle with rich styles and creative effects

**Core Features**:
- ✨ **Horizontal/Vertical Layout** - Perfect support for CJK vertical text
- ✨ **Font Rotation** - 0-360° free rotation
- ✨ **Multiple Gradients** - Linear, radial, diagonal gradients
- ✨ **Stroke Position** - Outer/center/inner three modes
- ✨ **Shadow Effects** - Full control of angle, distance, intensity, blur
- ✨ **28 Animations** - Rich effects from basic to advanced
- ✨ **Position Presets** - 12 common positions with one click
- ✨ **Letter Spacing** - Fine adjustment from -50 to +200px
- ✨ **Font Weight** - 4 levels: regular/bold/extra-bold/ultra-bold

**Use Cases**:
- Title subtitles
- Creative text display
- Vertical poetry
- Rotation effect subtitles

---

#### 2️⃣ Video Subtitle Timestamp Pro v2.7.0
**Best for**: Multiple subtitles with timeline management

**Core Features**:
- ✨ **4 Formats** - SRT/Simple/Parenthesis/No Timestamp
  - **SRT Format**: `00:00:01,000 --> 00:00:02,000`
  - **Simple Format**: `0.0-0.26 text`
  - **Parenthesis Format**: `(0.0, 0.26) text` ⭐New
  - **No Timestamp**: Auto-calculate time
- ✨ **Symbol Removal** - 5 intelligent modes ⭐New
  - None/Chinese punctuation/English punctuation/All punctuation/All symbols
- ✨ **Scrolling Credits** - Perfect end credits scrolling effect
- ✨ **32 Animations** - More effects than Enhanced version
- ✨ **Font Weight** - 4 levels
- ✨ **Shadow System** - Complete shadow parameter control
- ✨ **Gradient Colors** - 2-3 color gradients, 3 directions
- ✨ **Position Presets** - 12 quick positions
- ✨ **Canvas Constraints** - Auto-scale/crop by character

**Use Cases**:
- Video subtitling
- SRT subtitle import
- Multi-segment dialogue subtitles
- End credits scrolling

---

### 🎞️ Video Processing Nodes

#### 3️⃣ Video Transition v3.2.1
**26 Professional Transition Effects for Smooth Video Concatenation**

**Basic Transitions**:
- 🔀 Direct Concat - No transition, direct concatenation
- 🌅 Cross Fade - Classic fade in/out
- ↔️ Wipe - Left/Right/Up/Down 4 directions
- 🔍 Zoom - Zoom in/out

**Gradient Wipe** (4 directions):
- ⬅️ Left to Right
- ➡️ Right to Left
- ⬆️ Top to Bottom
- ⬇️ Bottom to Top

**Radial Effects** (2 types):
- ⭕ Circle Wipe
- ⬜ Box Wipe

**Creative Effects**:
- 🎯 Blinds - Horizontal/Vertical
- ♟️ Checkerboard
- 📐 Diagonal Wipe - Top-left/Bottom-right
- 🌊 Ripple Effect
- 🕐 Clock Wipe
- 🎨 Mosaic Transition
- 📖 Page Turn - Left/Right

**Features**:
- ⚡ GPU accelerated processing
- 🎬 Professional transition quality
- 🔧 Easy to use
- 📊 Supports high-resolution videos

---

#### 4️⃣ Video Last Frame v1.0.0
**Functions**:
- Extract last N frames from video
- Flexible frame count control
- Quick preview of video ending

---

### 🖼️ Image Processing Nodes

#### 5️⃣ Image Accumulator v1.0.0
**Functions**:
- Smart batch image accumulation
- Automatic batch processing management
- Optimized workflow

---

## 🚀 Installation

### Method 1: ComfyUI Manager (Recommended)
1. Open ComfyUI Manager
2. Search for `HAIGC Toolkit`
3. Click Install
4. Restart ComfyUI

### Method 2: Manual Installation
```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/your-repo/haigc_toolkit.git
cd haigc_toolkit
pip install -r requirements.txt
```

### Method 3: One-Click Install Script (Windows)
```powershell
# Download and run install script
# install.bat
```

---

## 📋 Requirements

```
numpy>=1.24.0
pillow>=10.0.0
```

ComfyUI will automatically install these dependencies.

---

## 📖 User Guide

### 🎯 Subtitle Node Selection Guide

| Need | Recommended Node | Reason |
|------|------------------|--------|
| Single subtitle | Enhanced | Simple operation, rich styles |
| Multiple subtitles | Pro | Timeline management, batch processing |
| Vertical text | Enhanced | Perfect vertical support |
| SRT import | Pro | Native SRT support |
| Scrolling credits | Pro | Dedicated scrolling mode |
| Creative titles | Enhanced | More flexible rotation and gradients |
| Dialogue subtitles | Pro | Precise timestamp control |

### 🔄 Parameter Alignment Between Two Subtitle Nodes

The same function parameters of the two subtitle nodes are aligned for seamless switching:

**Common Parameters**:
- 📝 **Font Style** - Font, size, weight, color, opacity
- 🖊️ **Stroke Settings** - Size, color, position, opacity
- 🌟 **Shadow Settings** - Angle, distance, intensity, blur
- 📍 **Position & Alignment** - Preset positions, alignment, X/Y percentage
- 🎬 **Animation Effects** - Effect type, intensity, duration

---

## 📝 Subtitle Format Details

### 1️⃣ SRT Format (Standard Subtitle Format)

```srt
1
00:00:01,000 --> 00:00:02,000
The wind as you turn

2
00:00:04,000 --> 00:00:05,000
Leaves lying on the ground

3
00:00:06,000 --> 00:00:08,000
Breeze lifts them
```

**Format Description**:
- Line 1: Index number
- Line 2: Timestamp (HH:MM:SS,mmm --> HH:MM:SS,mmm)
- Line 3: Subtitle text
- Blank line separates each subtitle

---

### 2️⃣ Simple Format (Quick Input)

```
0.0-0.26 Nobita,
0.3-1.4 I'm here to participate,
1.5-2.26 Tell me quickly,
2.32-2.94 I'm the first.
```

**Format Description**:
- `start_time-end_time text`
- Time unit: seconds
- Supports decimals

---

### 3️⃣ Parenthesis Format (New Format) ⭐

```
(0.0, 0.26) Nobita,
(0.3, 1.4) I'm here to participate,
(1.5, 2.26) Tell me quickly,
(2.32, 2.94) I'm the first.
```

**Format Description**:
- `(start_time, end_time) text`
- Time unit: seconds
- Supports integers and decimals
- **Default format**, most concise and intuitive

---

### 4️⃣ No Timestamp Format

```
Nobita,
I'm here to participate,
Tell me quickly,
I'm the first.
```

**Set Parameters**:
- Start time: 0 seconds
- Display duration per segment: 2 seconds
- Subtitle interval: 0.5 seconds

**Auto Calculation**:
- Segment 1: 0.0-2.0 seconds
- Segment 2: 2.5-4.5 seconds
- Segment 3: 5.0-7.0 seconds
- And so on...

---

## 🎨 Key Features Details

### ⭐ Symbol Removal (v2.7.0 New)

**5 Removal Modes**:

| Mode | Description | Example |
|------|-------------|---------|
| **None** | Keep original | `Nobita, I'm here!` |
| **Chinese Punctuation** | Remove ，。！？etc. | `Nobita I'm here` |
| **English Punctuation** | Remove ,.!?etc. | `Hello world` |
| **All Punctuation** | Remove all punctuation | `NobitaImhereHelloWorld` |
| **All Symbols** | Keep only text and numbers | `NobitaImhere2023` |

**Use Cases**:
- 🎨 Clean subtitles - Cleaner without punctuation
- 📱 Small screen display - Save space
- 🌍 Multi-language processing - Unified punctuation format
- 🎭 Artistic subtitles - Pure text display

---

### 🎭 Font Weight (4 Levels)

| Level | Effect | Use Case |
|-------|--------|----------|
| **Regular** | Standard weight | Body subtitles |
| **Bold** | Moderate bold | Emphasis subtitles |
| **Extra Bold** | Obviously bold | Title subtitles |
| **Ultra Bold** | Maximum bold | Poster subtitles |

**Features**:
- ✅ Supports horizontal and vertical layout
- ✅ Supports gradient and stroke
- ✅ Smart margin adjustment

---

### 🌟 Shadow Effects (Professional)

**4 Parameters**:
- **Shadow Angle**: 0-360°, controls shadow direction
- **Shadow Distance**: 0-100px, controls offset
- **Shadow Intensity**: 0.0-1.0, controls opacity
- **Shadow Blur**: 0-30px, controls edge blur

**Preset Schemes**:
- 📺 **Bottom-Right Shadow**: Angle 135°, Distance 5, Intensity 0.75, Blur 4
- 🎬 **Bottom Shadow**: Angle 180°, Distance 8, Intensity 0.6, Blur 5
- ✨ **Soft Shadow**: Angle 135°, Distance 3, Intensity 0.5, Blur 8

---

### 📍 Position Presets (12 Types)

| Preset | X% | Y% | Description |
|--------|----|----|-------------|
| Bottom Center | 50 | 85 | Default subtitle position |
| Top Center | 50 | 15 | Top subtitle |
| Center | 50 | 50 | Screen center |
| Bottom Left | 15 | 85 | Bottom left position |
| Bottom Right | 85 | 85 | Bottom right position |
| Top Left | 15 | 15 | Top left position |
| Top Right | 85 | 15 | Top right position |
| Left Center | 15 | 50 | Left middle |
| Right Center | 85 | 50 | Right middle |
| Bottom Third | 50 | 75 | Lower third |
| Top Third | 50 | 25 | Upper third |
| Custom | - | - | Manual setting |

---

### 📐 Alignment Modes (3 Types)

```
┌─────────────────┐
│  Left Align      │  Text extends right from X position
│   Center Align   │  Text centered at X position
│      Right Align │  Text extends left from X position
└─────────────────┘
```

**Combined Use**:
- Left Align + X=10% = Text starts from left
- Center Align + X=50% = Text centered
- Right Align + X=90% = Text starts from right

---

### 🖼️ Canvas Constraints (3 Modes)

| Mode | Description | Use Case |
|------|-------------|----------|
| **No** | Allow overflow | Normal subtitles |
| **Auto Scale** | Auto reduce font size | Long subtitles |
| **Crop by Character** | Crop by character | Scrolling credits |

**Crop by Character Details**:
- 🔍 Smart recognition of each character boundary
- ✂️ Characters overflow are completely hidden
- ✅ Characters not overflow are completely preserved
- 🎬 Perfect support for scrolling credits and marquee effects

---

### 🎬 Animation Effects

#### Enhanced Version (28 Types)
**Basic**: Fade In, Fade Out, Scroll Up, Scroll Down, Typewriter, Zoom In

**Fly In**: Fly Left, Fly Right, Fly Up, Fly Down

**Bounce**: Bounce, Rotate Fade, Wave, Blink, Shake

**Advanced**: Gradual Zoom, Split Merge, Elastic, 3D Flip

**Enhanced**: Explosion, Spiral, Particle, Light Speed, Spring Shake, Page Turn, Liquid Flow, Lightning, Fragment Rebuild

#### Pro Version (32 Types)
Includes all Enhanced effects, plus:
- Breathing
- Heartbeat
- Shock Wave
- Twist
- Blur Focus
- Rainbow Gradient
- **Scrolling Credits** (End credits dedicated)

---

## ⚡ Performance Optimization

### GPU Optimization
- ✅ Automatic GPU memory management
- ✅ Batch processing memory optimization
- ✅ Regular memory cleanup (every 100 frames)
- ✅ Smart CPU/GPU scheduling

### Font Cache
- ✅ LRU font cache mechanism
- ✅ Cache size: 20 fonts
- ✅ Auto cache cleanup
- ✅ Reduce repeated IO operations

### Gradient Optimization
- ✅ NumPy vectorized calculation
- ✅ 10-100x performance improvement
- ✅ Gradient cache system
- ✅ Smart stroke algorithm

### Resource Management
- ✅ Explicit PIL object cleanup
- ✅ Forced gc.collect() every 50 frames
- ✅ Windows resource exhaustion fix
- ✅ Supports long video processing

---

## 💡 Usage Tips

### 🎯 Subtitle Positioning Tips
1. **Bottom Subtitle**: Select "Bottom Center" preset
2. **Top Subtitle**: Select "Top Center" preset
3. **PIP Subtitle**: Custom X/Y for precise positioning
4. **Bilingual Subtitle**: Stack two nodes, adjust Y position

### 🎨 Style Matching Suggestions
**Clear & Readable**:
- Font: White + Black stroke (3-5px)
- Shadow: 135° + 5px + 0.75 intensity

**Creative Title**:
- Gradient: Three-color gradient + diagonal direction
- Animation: Explosion + 1.5x intensity

**Retro Style**:
- Font weight: Extra bold or ultra bold
- Color: Yellow #FFD700
- Shadow: Strong shadow effect

### ⚙️ Performance Optimization Suggestions
1. **Long Video Processing**:
   - Enable auto-scale to reduce computation
   - Restart ComfyUI regularly to release memory

2. **Many Subtitles**:
   - Use SRT format for batch import
   - Reduce gradient color count

3. **HD Video**:
   - Appropriately reduce font size
   - Reduce animation intensity

---

## ❓ FAQ

<details>
<summary><b>Q1: Font displays as squares or garbled?</b></summary>

**Solution**:
1. Ensure font files are in `font/` folder
2. Font file formats: `.ttf`, `.otf`, `.ttc`
3. Font name without extension
4. Default font: `AlibabaHealthFont2.0CN-45R`

</details>

<details>
<summary><b>Q2: Subtitles overflow the screen?</b></summary>

**Solution**:
- Method 1: Enable "Auto Scale", auto adjust font size
- Method 2: Manually reduce font size
- Method 3: Use "Crop by Character" mode

</details>

<details>
<summary><b>Q3: Out of memory when processing long videos?</b></summary>

**Solution**:
1. Auto memory cleanup every 100 frames (built-in)
2. Reduce gradient color count (from 3 to 2)
3. Reduce font cache size
4. Process long videos in segments

</details>

<details>
<summary><b>Q4: SRT subtitle timing inaccurate?</b></summary>

**Check**:
1. Is video frame rate set correctly (default 30fps)
2. SRT timestamp format: `00:00:01,000` (comma separates milliseconds)
3. Timestamp arrow: `-->` (two dashes)

</details>

<details>
<summary><b>Q5: How to remove punctuation from subtitles?</b></summary>

**Steps**:
1. Use "Video Subtitle Timestamp Pro" node
2. Find "Symbol Removal" in "⚙️ Advanced Settings"
3. Select appropriate mode:
   - All Punctuation: Remove all Chinese and English punctuation
   - All Symbols: Keep only text and numbers

</details>

<details>
<summary><b>Q6: What's the difference between Parenthesis and Simple format?</b></summary>

**Difference**:
- **Parenthesis Format**: `(0.0, 0.26) text` - Uses parentheses and comma
- **Simple Format**: `0.0-0.26 text` - Uses dash

Both formats have identical functionality, choose what you prefer.

</details>

---

## 🔄 Changelog

### v3.3.8 (2025-11-02) Current Version
- 🧹 Cleanup: Removed outdated and unused files
- ✅ Deleted 7 outdated markdown documents
- ✅ Streamlined requirements.txt
- 📝 New: Created concise README.md user guide
- 🎯 Optimization: Cleaner project structure

### v2.7.0 - Subtitle Timestamp Pro (2025-11-03)
- ✨ New: Symbol removal feature (5 modes)
- 📝 Modes: None/Chinese punctuation/English punctuation/All punctuation/All symbols
- 🎯 Application: Auto process all subtitle segments and scrolling credits
- 🧠 Smart: Preserve Chinese, letters, numbers, spaces

### v2.6.2 - Subtitle Timestamp Pro (2025-11-03)
- ✨ New: Parenthesis format support `(time1, time2) text`
- 📝 Example: `(0.0, 0.26) Nobita,`
- 🎯 Default: Subtitle format changed to "Parenthesis Format"

### v2.5.0 - Subtitle Enhanced (2025-11-02)
- 🎯 Alignment: Parameter order consistent with Pro version
- 📐 Optimization: Same function modules in unified positions
- ✅ Improvement: Easy to switch between two nodes

### v3.3.5 (2025-11-02)
- 🐛 Fix: Windows system resource exhaustion error
- 🔧 Optimization: Explicit PIL object cleanup
- 💪 Stability: Greatly improved stability when processing many frames

### v3.2.0 (2025-11-02)
- 🧹 Simplification: Removed all color matching features
- ✅ Improvement: Video concatenation preserves original colors
- 📦 Optimization: Clearer code structure

[View Complete Version History](version.py)

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

**Contributing Guidelines**:
1. Fork this repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details

---

## 📧 Contact

- 💬 **Issue Reporting**: Submit an Issue on GitHub
- 💡 **Feature Suggestions**: Welcome to discuss in Issues
- 📮 **Email Contact**: [your-email@example.com]

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=your-username/haigc_toolkit&type=Date)](https://star-history.com/#your-username/haigc_toolkit&Date)

---

## 💖 Support the Author

If this project helps you, feel free to donate! Your support motivates me to keep updating 🚀

<div align="center">

### Scan to Donate - WeChat / Alipay

<img src="./images/payment_qr.png" alt="Donation QR Code" width="600"/>

**Thank you for your support! ❤️**

Your donation will be used for:
- 🔧 Continuous maintenance and updates
- ✨ Developing more useful features
- 📚 Improving documentation and tutorials
- 🐛 Quick bug fixes

</div>

---

### 🌟 Recommended Cloud Platform

#### 🇨🇳 Chinese Website
**ComfyUI Workflow Cloud Platform - Register to Get 1000 Computing Points**  
**ComfyUI 工作流云平台推荐，点击链接注册领取 1000 算力积分**

👉 [立即注册 | Register Now](https://www.runninghub.cn/user-center/1887871050510716930/userPost?inviteCode=rh-v1127)

#### 🌍 International Website
**International Cloud Platform - Register to Get 1000 Computing Points**  
**国际版云平台，点击链接注册领取 1000 算力积分**

👉 [Register Now | 立即注册](https://www.runninghub.ai/user-center/1939305513756864513/userPost?inviteCode=rh-v1127)

---

<div align="center">

**HAIGC Toolkit** - Making ComfyUI's Video Subtitle Processing More Professional 🎬

Made with ❤️ by HAIGC Team

[⬆ Back to Top](#haigc-toolkit-for-comfyui)

</div>

