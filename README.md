# 字体文件目录 / Font Files Directory

## 📁 目录说明

此目录用于存放自定义字体文件，以确保在所有平台上（特别是 Linux）都能正确显示中文字幕。

## 🎯 使用方法

### 1. 下载字体文件

推荐使用以下免费开源字体：

- **Noto Sans CJK SC (思源黑体)** - 适合通用场景
  - 下载地址：https://github.com/googlefonts/noto-cjk/releases
  - 推荐文件：`NotoSansCJK-Regular.ttc`

- **Source Han Sans CN (思源黑体)** - Adobe 开源字体
  - 下载地址：https://github.com/adobe-fonts/source-han-sans/releases
  - 推荐文件：`SourceHanSansCN-Regular.otf`

- **文泉驿微米黑** - 轻量级中文字体
  - 下载地址：https://sourceforge.net/projects/wqy/files/wqy-microhei/
  - 文件：`wqy-microhei.ttc`

### 2. 放置字体文件

将下载的字体文件（`.ttf`、`.otf` 或 `.ttc` 格式）直接复制到此目录：

```bash
# 示例：
haigc_toolkit/font/
├── NotoSansCJK-Regular.ttc
├── SourceHanSansCN-Bold.otf
└── custom-font.ttf
```

### 3. 重启 ComfyUI

放置字体文件后，重启 ComfyUI，字体会自动出现在节点的"字体选择"下拉列表中。

## ✅ 支持的字体格式

- `.ttf` - TrueType Font
- `.otf` - OpenType Font  
- `.ttc` - TrueType Collection (包含多个字体)

## 📝 注意事项

1. **文件命名**：字体文件名（去掉扩展名）会显示在字体选择列表中
   - 例如：`思源黑体.ttf` 会显示为 "思源黑体"
   - 例如：`MyFont.otf` 会显示为 "MyFont"

2. **文件大小**：中文字体文件通常较大（10-50MB），这是正常的

3. **版权问题**：
   - 个人使用：可以使用上述开源字体
   - 商业使用：请确保字体授权许可允许商业使用

4. **Git 忽略**：字体文件不会被提交到 Git 仓库（已在 .gitignore 中配置）

## 🐛 故障排查

### 问题：字体文件已放置，但列表中没有显示

**解决方法：**
1. 确认文件扩展名是 `.ttf`、`.otf` 或 `.ttc`
2. 重启 ComfyUI
3. 检查 ComfyUI 日志是否有字体加载错误

### 问题：选择字体后仍然显示乱码

**解决方法：**
1. 确认字体文件支持中文（可用字体查看软件验证）
2. 检查字体文件没有损坏（尝试重新下载）
3. 查看 ComfyUI 日志中的字体加载信息

## 📚 更多帮助

详细的字体配置指南请查看：[../FONT_GUIDE.md](../FONT_GUIDE.md)

如有问题，请提交 Issue：https://github.com/HAIGC/haigc_toolkit/issues

