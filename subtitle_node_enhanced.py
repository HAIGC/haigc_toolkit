"""
视频字幕添加节点 - 增强版（v2.0.0-stable）
支持渐变、多段字幕、横竖排版、旋转等高级功能
性能优化、质量提升、稳定性增强
"""

import torch
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import math
from typing import Tuple, Dict, Any, Optional
import folder_paths

class VideoSubtitleEnhancedNode:
    """视频字幕添加节点 - 增强版（v2.0.0-stable）
    
    特性：
    - 高性能渐变算法（使用numpy矢量化）
    - 高质量描边（优化算法）
    - 丰富的动效（28种）
    - 完整的错误处理和输入验证
    - 字体缓存机制
    - 横竖排全功能支持
    """
    
    # 类级别的字体缓存
    _font_cache = {}
    
    def __init__(self):
        self.type = "HAIGC_VideoSubtitleEnhanced"
        
    @classmethod
    def INPUT_TYPES(cls):
        fonts_list = cls.get_available_fonts()
        
        return {
            "required": {
                "images": ("IMAGE",),
                "字幕文本": ("STRING", {
                    "default": "这是字幕文本",
                    "multiline": True
                }),
                "字体大小": ("INT", {
                    "default": 48,
                    "min": 12,
                    "max": 300,
                    "step": 1
                }),
                "字间距": ("INT", {
                    "default": 0,
                    "min": -50,
                    "max": 200,
                    "step": 1,
                    "display": "number"
                }),
                "字体颜色": ("STRING", {
                    "default": "#FFFFFF",
                    "multiline": False,
                    "placeholder": "十六进制(#FFFFFF)或十进制(16777215)"
                }),
                "渐变效果": (["无", "线性渐变", "径向渐变", "对角渐变"], {
                    "default": "无"
                }),
                "渐变开头颜色": ("STRING", {
                    "default": "#FFFFFF",
                    "multiline": False,
                    "placeholder": "十六进制或十进制"
                }),
                "渐变中间颜色": ("STRING", {
                    "default": "#FFFF00",
                    "multiline": False,
                    "placeholder": "十六进制或十进制"
                }),
                "渐变末尾颜色": ("STRING", {
                    "default": "#FF0000",
                    "multiline": False,
                    "placeholder": "十六进制或十进制"
                }),
                "渐变过渡强度": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.05
                }),
                "不透明度": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "排版方向": (["横排", "竖排"], {
                    "default": "横排"
                }),
                "字体角度": ("INT", {
                    "default": 0,
                    "min": -180,
                    "max": 180,
                    "step": 1
                }),
                "位置X百分比": ("FLOAT", {
                    "default": 50.0,
                    "min": 0.0,
                    "max": 100.0,
                    "step": 0.1
                }),
                "位置Y百分比": ("FLOAT", {
                    "default": 85.0,
                    "min": 0.0,
                    "max": 100.0,
                    "step": 0.1
                }),
                "投影角度": ("INT", {
                    "default": 135,
                    "min": 0,
                    "max": 360,
                    "step": 1
                }),
                "投影距离": ("INT", {
                    "default": 5,
                    "min": 0,
                    "max": 100,
                    "step": 1
                }),
                "投影强度": ("FLOAT", {
                    "default": 0.75,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "投影模糊": ("INT", {
                    "default": 4,
                    "min": 0,
                    "max": 30,
                    "step": 1
                }),
                "字体选择": (fonts_list, {
                    "default": "KaiTi"
                }),
                "字体粗细": (["常规", "粗体", "特粗", "超粗"], {
                    "default": "常规"
                }),
                "描边大小": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 50,
                    "step": 1,
                    "display": "number"
                }),
                "描边颜色": ("STRING", {
                    "default": "#000000",
                    "multiline": False,
                    "placeholder": "十六进制或十进制"
                }),
                "描边位置": (["外部", "居中", "内部"], {
                    "default": "外部"
                }),
                "描边不透明度": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "display": "number"
                }),
                "动效类型": ([
                    "无", "淡入", "淡出", "滚动上升", "滚动下降", 
                    "打字机", "缩放出现", "左飞入", "右飞入", "上飞入", "下飞入",
                    "弹跳出现", "旋转淡入", "波浪效果", "闪烁", "抖动出现",
                    "渐进放大", "分裂合并", "弹性进入", "3D翻转",
                    "爆炸进入（增强）", "螺旋出现（增强）", "粒子聚合（增强）", 
                    "光速飞入（增强）", "弹簧抖动（增强）", "翻书效果（增强）",
                    "液体流动（增强）", "闪电出现（增强）", "碎片重组（增强）"
                ], {
                    "default": "无"
                }),
                "动效强度": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 3.0,
                    "step": 0.1
                }),
                "动效时长": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.01,
                    "max": 300.0,
                    "step": 0.01,
                    "display": "number"
                }),
                "动效速度调节": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 5.0,
                    "step": 0.1,
                    "display": "number"
                }),
                "开始时间": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 3600.0,
                    "step": 0.01
                }),
                "结束时间": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 3600.0,
                    "step": 0.01
                }),
                "时间单位": (["帧数", "秒数"], {
                    "default": "秒数"
                }),
                "视频帧率": ("FLOAT", {
                    "default": 30.0,
                    "min": 1.0,
                    "max": 120.0,
                    "step": 0.01
                }),
            },
        }
    
    RETURN_TYPES = ("IMAGE", "FLOAT", "INT", "STRING", "FLOAT", "FLOAT")
    RETURN_NAMES = ("图像", "视频时长秒", "视频总帧数", "字幕文本", "开始时间", "结束时间")
    FUNCTION = "add_subtitle"
    CATEGORY = "HAIGC工具集/视频处理"
    
    @staticmethod
    def get_available_fonts():
        """获取可用字体列表（包含自定义字体）"""
        # 系统字体
        system_fonts = ["KaiTi", "Microsoft YaHei", "SimHei", "SimSun", "Arial"]
        
        # 扫描 font 文件夹中的自定义字体
        custom_fonts = []
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_dir = os.path.join(current_dir, "font")
        
        if os.path.exists(font_dir):
            for filename in os.listdir(font_dir):
                if filename.lower().endswith(('.ttf', '.otf', '.ttc')):
                    # 使用文件名（不含扩展名）作为字体名称
                    font_name = os.path.splitext(filename)[0]
                    custom_fonts.append(font_name)
        
        # 自定义字体排在前面
        return custom_fonts + system_fonts
    
    @classmethod
    def get_font_path(cls, font_name: str) -> Optional[str]:
        """根据字体名称获取字体文件路径（支持自定义字体）"""
        
        # 优先查找自定义 font 文件夹
        current_dir = os.path.dirname(os.path.abspath(__file__))
        custom_font_dir = os.path.join(current_dir, "font")
        
        if os.path.exists(custom_font_dir):
            # 查找匹配的字体文件
            for ext in ['.ttf', '.otf', '.ttc']:
                custom_font_path = os.path.join(custom_font_dir, font_name + ext)
                if os.path.exists(custom_font_path):
                    print(f"[字体加载] 使用自定义字体: {font_name}{ext}")
                    return custom_font_path
        
        # 如果没有找到自定义字体，使用系统字体
        font_map = {
            "Arial": "arial.ttf",
            "SimHei": "simhei.ttf",
            "Microsoft YaHei": "msyh.ttc",
            "SimSun": "simsun.ttc",
            "KaiTi": "simkai.ttf",
        }
        
        if os.name == 'nt':
            font_dir = "C:/Windows/Fonts/"
        else:
            font_dir = "/usr/share/fonts/truetype/"
            
        font_file = font_map.get(font_name, "arial.ttf")
        full_path = os.path.join(font_dir, font_file)
        
        if not os.path.exists(full_path):
            print(f"[字体加载] 字体不存在: {font_name}，使用默认字体")
            try:
                return ImageFont.load_default()
            except:
                return None
                
        return full_path
    
    @classmethod
    def get_cached_font(cls, font_name: str, size: int) -> Optional[ImageFont.FreeTypeFont]:
        """获取缓存的字体对象（性能优化）"""
        cache_key = f"{font_name}_{size}"
        
        if cache_key in cls._font_cache:
            return cls._font_cache[cache_key]
        
        font_path = cls.get_font_path(font_name)
        try:
            if isinstance(font_path, str):
                font = ImageFont.truetype(font_path, size)
            else:
                font = font_path
            
            # 限制缓存大小
            if len(cls._font_cache) > 50:
                # 清理一半缓存
                keys_to_remove = list(cls._font_cache.keys())[:25]
                for key in keys_to_remove:
                    del cls._font_cache[key]
            
            cls._font_cache[cache_key] = font
            return font
        except Exception as e:
            print(f"字体加载失败: {e}")
            return ImageFont.load_default()
    
    def parse_color(self, color_input: str) -> Tuple[int, int, int]:
        """解析颜色输入（支持十六进制和十进制）
        
        支持的格式：
        - 十六进制：#FFFFFF 或 FFFFFF
        - 十进制：16777215
        """
        if not color_input:
            return (255, 255, 255)
        
        try:
            if isinstance(color_input, str):
                color_input = color_input.strip()
                
                # 十六进制格式
                if color_input.startswith('#') or any(c in 'abcdefABCDEF' for c in color_input):
                    hex_color = color_input.lstrip('#')
                    if len(hex_color) != 6:
                        raise ValueError(f"无效的十六进制颜色: {color_input}")
                    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                else:
                    # 十进制格式
                    decimal_value = int(color_input)
                    if decimal_value < 0 or decimal_value > 16777215:
                        raise ValueError(f"颜色值超出范围: {decimal_value}")
                    r = (decimal_value >> 16) & 0xFF
                    g = (decimal_value >> 8) & 0xFF
                    b = decimal_value & 0xFF
                    return (r, g, b)
            elif isinstance(color_input, int):
                r = (color_input >> 16) & 0xFF
                g = (color_input >> 8) & 0xFF
                b = color_input & 0xFF
                return (r, g, b)
        except Exception as e:
            print(f"颜色解析失败: {color_input}, 错误: {e}, 使用默认白色")
            return (255, 255, 255)
        
        return (255, 255, 255)
    
    def create_gradient_image_optimized(self, width: int, height: int, 
                                       start_rgb: Tuple[int, int, int],
                                       mid_rgb: Tuple[int, int, int],
                                       end_rgb: Tuple[int, int, int],
                                       gradient_type: str, intensity: float) -> Image.Image:
        """使用numpy创建高性能渐变图像"""
        
        # 创建坐标网格
        if gradient_type == "线性渐变":
            # 横向渐变
            x = np.linspace(0, 1, width) * intensity
            x = np.clip(x, 0, 1)
            progress = np.tile(x, (height, 1))
            
        elif gradient_type == "径向渐变":
            # 径向渐变
            y, x = np.ogrid[:height, :width]
            center_y, center_x = height // 2, width // 2
            max_dist = np.sqrt(center_x**2 + center_y**2)
            dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            progress = np.clip(dist / max_dist * intensity, 0, 1)
            
        elif gradient_type == "对角渐变":
            # 对角渐变
            y, x = np.ogrid[:height, :width]
            progress = (x / width + y / height) / 2 * intensity
            progress = np.clip(progress, 0, 1)
        else:
            # 无渐变，纯色
            gradient_img = Image.new('RGB', (width, height), start_rgb)
            return gradient_img
        
        # 计算渐变颜色（三段式：开头→中间→末尾）
        rgb = np.zeros((height, width, 3), dtype=np.uint8)
        
        # 前半段：开头→中间
        mask1 = progress < 0.5
        t1 = progress * 2
        for i, (s, m) in enumerate(zip(start_rgb, mid_rgb)):
            rgb[:, :, i] = np.where(mask1, 
                                   s * (1 - t1) + m * t1,
                                   rgb[:, :, i])
        
        # 后半段：中间→末尾
        mask2 = progress >= 0.5
        t2 = (progress - 0.5) * 2
        for i, (m, e) in enumerate(zip(mid_rgb, end_rgb)):
            rgb[:, :, i] = np.where(mask2,
                                   m * (1 - t2) + e * t2,
                                   rgb[:, :, i])
        
        gradient_img = Image.fromarray(rgb, mode='RGB')
        return gradient_img
    
    def create_gradient_text(self, text: str, font: ImageFont.FreeTypeFont, 
                           渐变效果: str, 开头颜色: str, 中间颜色: str, 末尾颜色: str, 
                           过渡强度: float, 排版方向: str = "横排", 字间距: int = 0,
                           字体粗细: str = "常规") -> Image.Image:
        """创建渐变文字图像（全功能版 - 支持字体粗细）"""
        
        # 计算文本尺寸
        temp_img = Image.new('RGBA', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        
        # 计算文本边界
        if 排版方向 == "竖排":
            chars = list(text.replace('\n', ''))
            char_info = []
            max_width = 0
            total_height = 0
            for char in chars:
                bbox = temp_draw.textbbox((0, 0), char, font=font)
                char_width = bbox[2] - bbox[0]
                char_height = bbox[3] - bbox[1]
                char_info.append((char, char_width, char_height))
                max_width = max(max_width, char_width)
                total_height += char_height
            text_width = max_width
            text_height = total_height + (len(chars) - 1) * max(0, 字间距)
        else:
            if 字间距 != 0:
                chars = list(text.replace('\n', ''))
                total_width = 0
                max_height = 0
                for char in chars:
                    bbox = temp_draw.textbbox((0, 0), char, font=font)
                    total_width += bbox[2] - bbox[0]
                    max_height = max(max_height, bbox[3] - bbox[1])
                text_width = total_width + (len(chars) - 1) * max(0, 字间距)
                text_height = max_height
            else:
                bbox = temp_draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
        
        # 添加边距
        padding = 50
        canvas_width = text_width + padding * 2
        canvas_height = text_height + padding * 2
        
        # 解析颜色
        start_rgb = self.parse_color(开头颜色)
        mid_rgb = self.parse_color(中间颜色)
        end_rgb = self.parse_color(末尾颜色)
        
        # 如果无渐变，直接绘制纯色文字
        if 渐变效果 == "无":
            text_img = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(text_img)
            
            if 排版方向 == "竖排":
                y_offset = padding
                for char, char_width, char_height in char_info:
                    x_offset = (canvas_width - char_width) // 2
                    draw.text((x_offset, y_offset), char, font=font, fill=start_rgb + (255,))
                    y_offset += char_height + max(0, 字间距)
            else:
                if 字间距 != 0:
                    # 横排有字间距，逐字符绘制
                    chars = list(text.replace('\n', ''))
                    char_widths = []
                    for char in chars:
                        bbox = temp_draw.textbbox((0, 0), char, font=font)
                        char_widths.append(bbox[2] - bbox[0])
                    total_width = sum(char_widths) + (len(chars) - 1) * max(0, 字间距)
                    x_offset = (canvas_width - total_width) // 2
                    for char, char_width in zip(chars, char_widths):
                        char_x = x_offset + char_width // 2
                        draw.text((char_x, canvas_height // 2), char, 
                                font=font, fill=start_rgb + (255,), anchor='mm')
                        x_offset += char_width + max(0, 字间距)
                else:
                    draw.text((canvas_width // 2, canvas_height // 2), text, 
                            font=font, fill=start_rgb + (255,), anchor='mm')
            return text_img
        
        # 创建渐变背景（高性能numpy版本）
        gradient_img = self.create_gradient_image_optimized(
            text_width, text_height, start_rgb, mid_rgb, end_rgb, 
            渐变效果 if 排版方向 == "横排" else "线性渐变", 过渡强度
        )
        
        # 创建完整画布
        full_gradient = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        full_gradient.paste(gradient_img, (padding, padding))
        full_gradient = full_gradient.convert('RGBA')
        
        # 创建文字遮罩（支持字体粗细）
        text_mask = Image.new('L', (canvas_width, canvas_height), 0)
        mask_draw = ImageDraw.Draw(text_mask)
        
        if 排版方向 == "竖排":
            y_offset = padding
            for char, char_width, char_height in char_info:
                x_offset = (canvas_width - char_width) // 2
                
                # 支持字体粗细
                if 字体粗细 == "常规":
                    mask_draw.text((x_offset, y_offset), char, font=font, fill=255)
                else:
                    self._draw_bold_char(mask_draw, (x_offset, y_offset), char, 
                                       font, 255, 字体粗细)
                
                y_offset += char_height + max(0, 字间距)
        else:
            # 横排支持字体粗细+字间距
            if 字间距 != 0:
                # 有字间距，逐字符绘制
                chars = list(text.replace('\n', ''))
                temp_img = Image.new('L', (1, 1))
                temp_draw = ImageDraw.Draw(temp_img)
                char_widths = []
                for char in chars:
                    bbox = temp_draw.textbbox((0, 0), char, font=font)
                    char_widths.append(bbox[2] - bbox[0])
                total_width = sum(char_widths) + (len(chars) - 1) * max(0, 字间距)
                x_offset = (canvas_width - total_width) // 2
                
                for char, char_width in zip(chars, char_widths):
                    char_x = x_offset + char_width // 2
                    if 字体粗细 == "常规":
                        mask_draw.text((char_x, canvas_height // 2), char, 
                                     font=font, fill=255, anchor='mm')
                    else:
                        self.create_bold_text(mask_draw, (char_x, canvas_height // 2), 
                                            char, font, 255, 字体粗细)
                    x_offset += char_width + max(0, 字间距)
            else:
                # 无字间距，整体绘制
                if 字体粗细 == "常规":
                    mask_draw.text((canvas_width // 2, canvas_height // 2), text, 
                                  font=font, fill=255, anchor='mm')
                else:
                    self.create_bold_text(mask_draw, (canvas_width // 2, canvas_height // 2), 
                                        text, font, 255, 字体粗细)
        
        # 应用遮罩
        result = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        result.paste(full_gradient, mask=text_mask)
        
        return result
    
    def create_vertical_text(self, text: str, font: ImageFont.FreeTypeFont, 
                           color: Tuple[int, int, int], 字间距: int = 0, 
                           bold_level: str = "常规") -> Image.Image:
        """创建竖排文字（支持字体粗细）"""
        chars = list(text.replace('\n', ''))
        
        # 计算尺寸
        temp_img = Image.new('RGBA', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        
        char_info = []
        max_width = 0
        total_height = 0
        
        for char in chars:
            bbox = temp_draw.textbbox((0, 0), char, font=font)
            char_width = bbox[2] - bbox[0]
            char_height = bbox[3] - bbox[1]
            char_info.append((char, char_width, char_height))
            max_width = max(max_width, char_width)
            total_height += char_height
        
        total_height += (len(chars) - 1) * max(0, 字间距)
        
        # 根据粗细级别添加额外边距
        padding_map = {"常规": 20, "粗体": 25, "特粗": 30, "超粗": 35}
        padding = padding_map.get(bold_level, 20)
        
        # 创建竖排文字图像
        vert_img = Image.new('RGBA', (max_width + padding, total_height + padding), (0, 0, 0, 0))
        vert_draw = ImageDraw.Draw(vert_img)
        
        y_offset = padding // 2
        for char, char_width, char_height in char_info:
            x_offset = (max_width - char_width) // 2 + padding // 2
            
            # 使用字体粗细功能（竖排文字逐字绘制）
            if bold_level == "常规":
                vert_draw.text((x_offset, y_offset), char, font=font, fill=color + (255,))
            elif bold_level == "粗体":
                # 绘制2次，微调位置
                offsets = [(0, 0), (1, 0), (0, 1), (1, 1)]
                for dx, dy in offsets:
                    vert_draw.text((x_offset + dx, y_offset + dy), char, font=font, fill=color + (255,))
            elif bold_level == "特粗":
                # 绘制4次，更大范围
                offsets = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2)]
                for dx, dy in offsets:
                    vert_draw.text((x_offset + dx, y_offset + dy), char, font=font, fill=color + (255,))
            elif bold_level == "超粗":
                # 绘制多次，环绕方式
                offsets = [(dx, dy) for dx in range(-1, 3) for dy in range(-1, 3)]
                for dx, dy in offsets:
                    vert_draw.text((x_offset + dx, y_offset + dy), char, font=font, fill=color + (255,))
            
            y_offset += char_height + max(0, 字间距)
        
        return vert_img
    
    def apply_animation_enhanced(self, frame_idx: int, effect_type: str, 
                                effect_duration: int, intensity: float, 
                                width: int = 0) -> Dict[str, Any]:
        """增强动画效果（优化版）"""
        
        # 淡出特殊处理
        if effect_type == "淡出" and frame_idx >= effect_duration:
            return {
                "opacity": 0.0, "offset_x": 0, "offset_y": 0,
                "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        if effect_type == "无" or frame_idx >= effect_duration:
            return {
                "opacity": 1.0, "offset_x": 0, "offset_y": 0,
                "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        progress = min(frame_idx / effect_duration, 1.0)
        ease_out = 1 - (1 - progress) ** 2
        ease_in_out = (math.sin((progress - 0.5) * math.pi) + 1) / 2
        
        # 增强动效
        if effect_type == "爆炸进入（增强）":
            scale = 1.0 + (1.5 * intensity * (1 - ease_out))
            opacity = ease_out
            rotation = int(720 * (1 - ease_out) * intensity)
            scatter = int((1 - ease_out) * 30 * intensity)
            offset_x = int(math.sin(progress * 12) * scatter)
            offset_y = int(math.cos(progress * 12) * scatter)
            return {
                "opacity": opacity, "offset_x": offset_x, "offset_y": offset_y,
                "scale": scale, "char_reveal": 1.0, "rotation": rotation, "distortion": 0
            }
        
        elif effect_type == "螺旋出现（增强）":
            angle = progress * math.pi * 4 * intensity
            radius = 200 * (1 - ease_out) * intensity
            offset_x = int(math.cos(angle) * radius)
            offset_y = int(math.sin(angle) * radius)
            rotation = int(progress * 720 * intensity)
            return {
                "opacity": ease_out, "offset_x": offset_x, "offset_y": offset_y,
                "scale": ease_out, "char_reveal": 1.0, "rotation": rotation, "distortion": 0
            }
        
        elif effect_type == "粒子聚合（增强）":
            scatter = (1 - ease_out) * 300 * intensity
            offset_x = int(math.sin(progress * 10) * scatter)
            offset_y = int(math.cos(progress * 10) * scatter)
            return {
                "opacity": ease_out, "offset_x": offset_x, "offset_y": offset_y,
                "scale": 0.3 + ease_out * 0.7, "char_reveal": 1.0, "rotation": 0, 
                "distortion": int((1-ease_out) * 20 * intensity)
            }
        
        elif effect_type == "光速飞入（增强）":
            offset_x = -int((1 - progress) ** 3 * width * 2 * intensity)
            scale = 0.2 + ease_out * 0.8
            return {
                "opacity": min(progress * 2, 1.0), "offset_x": offset_x, "offset_y": 0,
                "scale": scale, "char_reveal": 1.0, "rotation": 0, 
                "distortion": int((1-ease_out) * 30 * intensity)
            }
        
        elif effect_type == "弹簧抖动（增强）":
            freq = 8 * intensity
            damp = ease_out
            shake = math.sin(progress * math.pi * freq) * (1 - damp) * 30 * intensity
            return {
                "opacity": min(progress * 1.5, 1.0), "offset_x": int(shake), 
                "offset_y": int(shake * 0.5), "scale": 1.0, "char_reveal": 1.0, 
                "rotation": int(shake), "distortion": 0
            }
        
        elif effect_type == "翻书效果（增强）":
            if progress < 0.5:
                rotation_y = progress * 180 * intensity
                scale_x = math.cos(math.radians(rotation_y))
            else:
                rotation_y = 180 - (progress - 0.5) * 180 * intensity
                scale_x = -math.cos(math.radians(rotation_y))
            return {
                "opacity": 1.0, "offset_x": 0, "offset_y": 0,
                "scale": max(abs(scale_x), 0.1), "char_reveal": 1.0, 
                "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "液体流动（增强）":
            wave = math.sin(progress * math.pi * 3) * 20 * intensity * (1 - ease_out)
            return {
                "opacity": ease_out, "offset_x": 0, "offset_y": int(wave),
                "scale": 0.8 + ease_out * 0.2, "char_reveal": 1.0, "rotation": 0,
                "distortion": int(abs(wave))
            }
        
        elif effect_type == "闪电出现（增强）":
            if progress < 0.7:
                flash_count = 5
                flash_progress = (progress / 0.7 * flash_count) % 1.0
                opacity = 1.0 if flash_progress > 0.5 else 0.0
            else:
                opacity = 1.0
            jitter = (1 - ease_out) * 15 * intensity
            offset_x = int(math.sin(progress * 50) * jitter)
            offset_y = int(math.cos(progress * 50) * jitter)
            return {
                "opacity": opacity, "offset_x": offset_x, "offset_y": offset_y,
                "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "碎片重组（增强）":
            scatter_x = int(math.sin(progress * 20) * (1 - ease_out) * 150 * intensity)
            scatter_y = int(math.cos(progress * 15) * (1 - ease_out) * 150 * intensity)
            rotation = int((1 - ease_out) * 360 * intensity)
            return {
                "opacity": ease_out, "offset_x": scatter_x, "offset_y": scatter_y,
                "scale": 0.5 + ease_out * 0.5, "char_reveal": 1.0, "rotation": rotation,
                "distortion": int((1-ease_out) * 25 * intensity)
            }
        
        # 基础动效
        elif effect_type == "淡入":
            return {
                "opacity": ease_out, "offset_x": 0, "offset_y": 0,
                "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "淡出":
            return {
                "opacity": 1.0 - ease_out, "offset_x": 0, "offset_y": 0,
                "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "滚动下降":
            offset_y = int((1 - ease_out) * 100 * intensity)
            return {
                "opacity": ease_out, "offset_x": 0, "offset_y": -offset_y,
                "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "滚动上升":
            offset_y = int((1 - ease_out) * 100 * intensity)
            return {
                "opacity": ease_out, "offset_x": 0, "offset_y": offset_y,
                "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "打字机":
            return {
                "opacity": 1.0, "offset_x": 0, "offset_y": 0,
                "scale": 1.0, "char_reveal": ease_out, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "缩放出现":
            scale = 0.3 + ease_out * 0.7
            return {
                "opacity": ease_out, "offset_x": 0, "offset_y": 0,
                "scale": scale, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "左飞入":
            offset_x = -int((1 - ease_out) * width * intensity)
            return {
                "opacity": ease_out, "offset_x": offset_x, "offset_y": 0,
                "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "右飞入":
            offset_x = int((1 - ease_out) * width * intensity)
            return {
                "opacity": ease_out, "offset_x": offset_x, "offset_y": 0,
                "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "上飞入":
            offset_y = -int((1 - ease_out) * 200 * intensity)
            return {
                "opacity": ease_out, "offset_x": 0, "offset_y": offset_y,
                "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "下飞入":
            offset_y = int((1 - ease_out) * 200 * intensity)
            return {
                "opacity": ease_out, "offset_x": 0, "offset_y": offset_y,
                "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "弹跳出现":
            bounce = abs(math.sin(progress * math.pi * 3)) * (1 - ease_out) * 50 * intensity
            return {
                "opacity": ease_out, "offset_x": 0, "offset_y": -int(bounce),
                "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "旋转淡入":
            rotation = int((1 - ease_out) * 360 * intensity)
            return {
                "opacity": ease_out, "offset_x": 0, "offset_y": 0,
                "scale": ease_out, "char_reveal": 1.0, "rotation": rotation, "distortion": 0
            }
        
        elif effect_type == "波浪效果":
            wave = math.sin(progress * math.pi * 4) * 30 * intensity
            return {
                "opacity": 1.0, "offset_x": 0, "offset_y": int(wave),
                "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "闪烁":
            flash = 1.0 if (int(progress * 10) % 2 == 0) else 0.3
            return {
                "opacity": flash, "offset_x": 0, "offset_y": 0,
                "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "抖动出现":
            jitter = (1 - ease_out) * 10 * intensity
            offset_x = int(math.sin(progress * 50) * jitter)
            offset_y = int(math.cos(progress * 50) * jitter)
            return {
                "opacity": ease_out, "offset_x": offset_x, "offset_y": offset_y,
                "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "渐进放大":
            scale = 0.1 + ease_out * 0.9
            return {
                "opacity": ease_out, "offset_x": 0, "offset_y": 0,
                "scale": scale, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "分裂合并":
            if progress < 0.5:
                spread = (0.5 - progress) * 200 * intensity
            else:
                spread = (progress - 0.5) * 200 * intensity
            offset_x = int(math.sin(progress * 10) * spread)
            return {
                "opacity": ease_out, "offset_x": offset_x, "offset_y": 0,
                "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "弹性进入":
            if progress < 0.5:
                elastic = progress * 2
            else:
                elastic = 1.0 + math.sin((progress - 0.5) * math.pi * 4) * (1 - progress) * 0.3
            scale = 0.5 + elastic * 0.5
            return {
                "opacity": min(progress * 1.5, 1.0), "offset_x": 0, "offset_y": 0,
                "scale": scale, "char_reveal": 1.0, "rotation": 0, "distortion": 0
            }
        
        elif effect_type == "3D翻转":
            rotation = int(progress * 180 * intensity)
            scale = abs(math.cos(math.radians(rotation)))
            scale = max(scale, 0.1)
            return {
                "opacity": 1.0, "offset_x": 0, "offset_y": 0,
                "scale": scale, "char_reveal": 1.0, "rotation": rotation, "distortion": 0
            }
        
        # 默认无动效
        return {
            "opacity": 1.0, "offset_x": 0, "offset_y": 0, 
            "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
        }
    
    def create_bold_text(self, draw: ImageDraw.ImageDraw, position: Tuple[int, int], 
                        text: str, font: ImageFont.FreeTypeFont, 
                        fill: Tuple[int, int, int, int], bold_level: str):
        """创建加粗文字（优化版）"""
        x, y = position
        
        if bold_level == "常规":
            draw.text((x, y), text, font=font, fill=fill, anchor='mm')
        elif bold_level == "粗体":
            offsets = [(0, 0), (1, 0), (0, 1), (1, 1)]
            for dx, dy in offsets:
                draw.text((x + dx, y + dy), text, font=font, fill=fill, anchor='mm')
        elif bold_level == "特粗":
            offsets = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2)]
            for dx, dy in offsets:
                draw.text((x + dx, y + dy), text, font=font, fill=fill, anchor='mm')
        elif bold_level == "超粗":
            offsets = [(dx, dy) for dx in range(-1, 3) for dy in range(-1, 3)]
            for dx, dy in offsets:
                draw.text((x + dx, y + dy), text, font=font, fill=fill, anchor='mm')
    
    def create_stroke_text(self, text: str, font: ImageFont.FreeTypeFont, 
                          text_color: Tuple[int, int, int], 
                          stroke_color: Tuple[int, int, int], 
                          stroke_size: int, stroke_position: str, 
                          stroke_opacity: float, width: int, height: int, 
                          字间距: int = 0, 排版方向: str = "横排", 
                          字体粗细: str = "常规") -> Image.Image:
        """创建描边文字（全功能版 - 支持横竖排+字体粗细）"""
        
        text_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        
        if stroke_size == 0:
            # 无描边，直接绘制文字（支持粗细和排版）
            return self._draw_text_with_bold(text_layer, text, font, text_color + (255,), 
                                            width, height, 字体粗细, 排版方向, 字间距)
        
        stroke_rgba = stroke_color + (int(255 * stroke_opacity),)
        
        # 创建描边层
        stroke_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        stroke_draw = ImageDraw.Draw(stroke_layer)
        
        center_x = width // 2
        center_y = height // 2
        
        # 动态采样密度
        angle_step = 10 if stroke_size <= 5 else 15
        
        if 排版方向 == "竖排":
            # 竖排描边 - 逐字符绘制
            chars = list(text.replace('\n', ''))
            temp_img = Image.new('RGBA', (1, 1))
            temp_draw = ImageDraw.Draw(temp_img)
            
            # 计算竖排尺寸
            char_heights = []
            max_width = 0
            for char in chars:
                bbox = temp_draw.textbbox((0, 0), char, font=font)
                char_width = bbox[2] - bbox[0]
                char_height = bbox[3] - bbox[1]
                char_heights.append(char_height)
                max_width = max(max_width, char_width)
            
            total_height = sum(char_heights) + (len(chars) - 1) * max(0, 字间距)
            start_y = (height - total_height) // 2
            y_offset = start_y
            
            # 绘制竖排描边
            for i, (char, char_height) in enumerate(zip(chars, char_heights)):
                for angle in range(0, 360, angle_step):
                    for distance in range(1, stroke_size + 1):
                        offset_x = int(math.cos(math.radians(angle)) * distance)
                        offset_y = int(math.sin(math.radians(angle)) * distance)
                        
                        # 绘制描边（支持粗细）
                        if 字体粗细 == "常规":
                            stroke_draw.text((center_x + offset_x, y_offset + offset_y), 
                                           char, font=font, fill=stroke_rgba)
                        else:
                            self._draw_bold_char(stroke_draw, (center_x + offset_x, y_offset + offset_y), 
                                               char, font, stroke_rgba, 字体粗细)
                
                y_offset += char_height + max(0, 字间距)
        else:
            # 横排描边
            if 字间距 != 0:
                # 有字间距，逐字符绘制
                chars = list(text.replace('\n', ''))
                temp_img = Image.new('RGBA', (1, 1))
                temp_draw = ImageDraw.Draw(temp_img)
                
                char_widths = []
                for char in chars:
                    bbox = temp_draw.textbbox((0, 0), char, font=font)
                    char_widths.append(bbox[2] - bbox[0])
                
                total_width = sum(char_widths) + (len(chars) - 1) * max(0, 字间距)
                start_x = (width - total_width) // 2
                x_offset = start_x
                
                # 绘制横排描边（逐字符）
                for char, char_width in zip(chars, char_widths):
                    char_x = x_offset + char_width // 2
                    for angle in range(0, 360, angle_step):
                        for distance in range(1, stroke_size + 1):
                            offset_x = int(math.cos(math.radians(angle)) * distance)
                            offset_y = int(math.sin(math.radians(angle)) * distance)
                            
                            if 字体粗细 == "常规":
                                stroke_draw.text((char_x + offset_x, center_y + offset_y),
                                               char, font=font, fill=stroke_rgba, anchor='mm')
                            else:
                                self.create_bold_text(stroke_draw, (char_x + offset_x, center_y + offset_y),
                                                    char, font, stroke_rgba, 字体粗细)
                    x_offset += char_width + max(0, 字间距)
            else:
                # 无字间距，整体绘制
                for angle in range(0, 360, angle_step):
                    for distance in range(1, stroke_size + 1):
                        offset_x = int(math.cos(math.radians(angle)) * distance)
                        offset_y = int(math.sin(math.radians(angle)) * distance)
                        
                        # 绘制描边（支持粗细）
                        if 字体粗细 == "常规":
                            stroke_draw.text((center_x + offset_x, center_y + offset_y),
                                           text, font=font, fill=stroke_rgba, anchor='mm')
                        else:
                            self.create_bold_text(stroke_draw, (center_x + offset_x, center_y + offset_y),
                                                text, font, stroke_rgba, 字体粗细)
        
        # 根据描边位置合成
        if stroke_position == "外部":
            # 外部描边：先描边，后文字
            text_layer = Image.alpha_composite(text_layer, stroke_layer)
            text_layer = self._draw_text_with_bold(text_layer, text, font, text_color + (255,), 
                                                   width, height, 字体粗细, 排版方向, 字间距)
        elif stroke_position == "居中":
            # 居中描边：描边和文字混合
            text_layer = Image.alpha_composite(text_layer, stroke_layer)
            text_layer = self._draw_text_with_bold(text_layer, text, font, text_color + (255,), 
                                                   width, height, 字体粗细, 排版方向, 字间距)
        else:  # 内部
            # 内部描边：先文字，后用文字遮罩裁剪描边
            text_mask = Image.new('L', (width, height), 0)
            text_mask = self._draw_text_with_bold(text_mask, text, font, 255, 
                                                  width, height, 字体粗细, 排版方向, 字间距)
            stroke_layer.putalpha(text_mask.split()[0] if text_mask.mode == 'L' else text_mask)
            text_layer = self._draw_text_with_bold(text_layer, text, font, text_color + (255,), 
                                                   width, height, 字体粗细, 排版方向, 字间距)
            text_layer = Image.alpha_composite(text_layer, stroke_layer)
        
        return text_layer
    
    def _draw_text_with_bold(self, layer, text: str, font: ImageFont.FreeTypeFont, 
                            fill, width: int, height: int, bold_level: str, 
                            direction: str, spacing: int):
        """辅助函数：绘制支持粗细和排版的文字"""
        draw = ImageDraw.Draw(layer)
        center_x = width // 2
        center_y = height // 2
        
        if direction == "竖排":
            # 竖排
            chars = list(text.replace('\n', ''))
            temp_img = Image.new('RGBA', (1, 1))
            temp_draw = ImageDraw.Draw(temp_img)
            
            char_heights = []
            for char in chars:
                bbox = temp_draw.textbbox((0, 0), char, font=font)
                char_heights.append(bbox[3] - bbox[1])
            
            total_height = sum(char_heights) + (len(chars) - 1) * max(0, spacing)
            y_offset = (height - total_height) // 2
            
            for char, char_height in zip(chars, char_heights):
                if bold_level == "常规":
                    draw.text((center_x, y_offset), char, font=font, fill=fill)
                else:
                    self._draw_bold_char(draw, (center_x, y_offset), char, font, fill, bold_level)
                y_offset += char_height + max(0, spacing)
        else:
            # 横排
            if spacing != 0:
                # 有字间距时，逐字符绘制
                chars = list(text.replace('\n', ''))
                temp_img = Image.new('RGBA', (1, 1))
                temp_draw = ImageDraw.Draw(temp_img)
                
                char_widths = []
                max_height = 0
                for char in chars:
                    bbox = temp_draw.textbbox((0, 0), char, font=font)
                    char_widths.append(bbox[2] - bbox[0])
                    max_height = max(max_height, bbox[3] - bbox[1])
                
                total_width = sum(char_widths) + (len(chars) - 1) * max(0, spacing)
                x_offset = (width - total_width) // 2
                
                for char, char_width in zip(chars, char_widths):
                    char_x = x_offset + char_width // 2
                    if bold_level == "常规":
                        draw.text((char_x, center_y), char, font=font, fill=fill, anchor='mm')
                    else:
                        self.create_bold_text(draw, (char_x, center_y), char, font, fill, bold_level)
                    x_offset += char_width + max(0, spacing)
            else:
                # 无字间距时，整体绘制
                if bold_level == "常规":
                    draw.text((center_x, center_y), text, font=font, fill=fill, anchor='mm')
                else:
                    self.create_bold_text(draw, (center_x, center_y), text, font, fill, bold_level)
        
        return layer
    
    def _draw_bold_char(self, draw, position: Tuple[int, int], char: str, 
                       font: ImageFont.FreeTypeFont, fill, bold_level: str):
        """辅助函数：绘制单个粗体字符"""
        x, y = position
        
        if bold_level == "粗体":
            offsets = [(0, 0), (1, 0), (0, 1), (1, 1)]
        elif bold_level == "特粗":
            offsets = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2)]
        elif bold_level == "超粗":
            offsets = [(dx, dy) for dx in range(-1, 3) for dy in range(-1, 3)]
        else:
            offsets = [(0, 0)]
        
        for dx, dy in offsets:
            draw.text((x + dx, y + dy), char, font=font, fill=fill)
    
    def create_projection(self, text_img: Image.Image, angle: int, 
                         distance: int, intensity: float, blur: int) -> Image.Image:
        """创建投影（优化版）"""
        if distance == 0 or intensity == 0:
            return Image.new('RGBA', text_img.size, (0, 0, 0, 0))
        
        angle_rad = math.radians(angle)
        offset_x = int(math.cos(angle_rad) * distance)
        offset_y = int(math.sin(angle_rad) * distance)
        
        # 提取alpha通道并调整强度
        shadow_alpha = text_img.split()[3]
        shadow_alpha = shadow_alpha.point(lambda p: int(p * intensity))
        
        # 创建黑色阴影
        black_img = Image.new('RGB', text_img.size, (0, 0, 0))
        shadow = black_img.convert('RGBA')
        shadow.putalpha(shadow_alpha)
        
        # 应用高斯模糊
        if blur > 0:
            shadow = shadow.filter(ImageFilter.GaussianBlur(radius=blur))
        
        # 创建偏移的投影
        result = Image.new('RGBA', text_img.size, (0, 0, 0, 0))
        result.paste(shadow, (offset_x, offset_y), shadow)
        
        return result
    
    def add_subtitle(self, images, 字幕文本, 字体大小, 字间距, 字体颜色,
                    渐变效果, 渐变开头颜色, 渐变中间颜色, 渐变末尾颜色, 渐变过渡强度,
                    不透明度, 排版方向, 字体角度, 位置X百分比, 位置Y百分比,
                    投影角度, 投影距离, 投影强度, 投影模糊, 字体选择, 字体粗细,
                    描边大小, 描边颜色, 描边位置, 描边不透明度,
                    动效类型, 动效强度, 动效时长, 动效速度调节, 开始时间, 结束时间, 
                    时间单位, 视频帧率):
        """添加字幕（v2.0.0-stable - 高性能、高质量）"""
        
        # 输入验证
        if not 字幕文本 or not 字幕文本.strip():
            print("警告: 字幕文本为空，跳过处理")
            return (images, round(images.shape[0] / 视频帧率, 2), images.shape[0], "", 开始时间, 结束时间)
        
        batch_size = images.shape[0]
        height = images.shape[1]
        width = images.shape[2]
        
        video_duration_seconds = round(batch_size / 视频帧率, 2)
        
        # 时间计算
        if 时间单位 == "秒数":
            start_frame = int(开始时间 * 视频帧率)
            end_frame = int(结束时间 * 视频帧率) if 结束时间 > 0 else batch_size
            动效时长帧数 = max(1, int(动效时长 * 视频帧率 / 动效速度调节))
        else:
            start_frame = int(开始时间)
            end_frame = int(结束时间) if 结束时间 > 0 else batch_size
            动效时长帧数 = max(1, int(动效时长 / 动效速度调节))
        
        end_frame = min(end_frame, batch_size)
        
        # 获取缓存字体
        font = self.get_cached_font(字体选择, 字体大小)
        if font is None:
            print("错误: 字体加载失败")
            return (images, video_duration_seconds, batch_size, 字幕文本, 开始时间, 结束时间)
        
        # 预解析颜色
        text_color = self.parse_color(字体颜色)
        stroke_color = self.parse_color(描边颜色)
        
        output_images = []
        
        # 日志输出
        if 时间单位 == "秒数":
            print(f"[增强字幕] 秒数模式: 开始={开始时间:.2f}s(帧{start_frame}), "
                  f"结束={结束时间:.2f}s(帧{end_frame}), 总帧数={batch_size}")
            print(f"[增强字幕] 动效={动效类型}, 时长={动效时长:.2f}s({动效时长帧数}帧), "
                  f"强度={动效强度:.1f}x, 速度={动效速度调节}x")
        else:
            print(f"[增强字幕] 帧数模式: 开始=第{start_frame}帧, 结束=第{end_frame}帧, "
                  f"总帧数={batch_size}")
            print(f"[增强字幕] 动效={动效类型}, 时长={动效时长:.0f}帧(实际{动效时长帧数}帧)")
        
        print(f"[增强字幕] 字体={字体选择}, 大小={字体大小}px, 粗细={字体粗细}, "
              f"描边={描边大小}px, 字间距={字间距}px")
        
        for i in range(batch_size):
            # 转换当前帧
            img_array = images[i].cpu().numpy()
            img_array = (img_array * 255).astype(np.uint8)
            img_pil = Image.fromarray(img_array)
            
            # 判断是否在显示范围
            if i < start_frame or i >= end_frame:
                result = img_pil.convert('RGB')
                result_array = np.array(result).astype(np.float32) / 255.0
                output_images.append(result_array)
                continue
            
            relative_frame = i - start_frame
            
            # 淡出特殊处理
            if 动效类型 == "淡出":
                total_display_frames = end_frame - start_frame
                fade_start_frame = max(0, total_display_frames - 动效时长帧数)
                
                if relative_frame < fade_start_frame:
                    anim_params = {
                        "opacity": 1.0, "offset_x": 0, "offset_y": 0,
                        "scale": 1.0, "char_reveal": 1.0, "rotation": 0, "distortion": 0
                    }
                else:
                    fade_relative_frame = relative_frame - fade_start_frame
                    anim_params = self.apply_animation_enhanced(
                        fade_relative_frame, 动效类型, 动效时长帧数, 动效强度, width
                    )
            else:
                anim_params = self.apply_animation_enhanced(
                    relative_frame, 动效类型, 动效时长帧数, 动效强度, width
                )
            
            # 打字机效果
            display_text = 字幕文本
            if 动效类型 == "打字机":
                char_count = int(len(字幕文本) * anim_params["char_reveal"])
                display_text = 字幕文本[:max(0, char_count)]
                if not display_text:
                    result = img_pil.convert('RGB')
                    result_array = np.array(result).astype(np.float32) / 255.0
                    output_images.append(result_array)
                    continue
            
            # 创建文字图层
            canvas_width = width * 2
            canvas_height = height * 2
            
            # 全功能渲染逻辑（支持所有组合）
            if 描边大小 > 0 and 渐变效果 != "无":
                # 描边 + 渐变组合（优先渐变）
                text_img = self.create_gradient_text(
                    display_text, font, 渐变效果,
                    渐变开头颜色, 渐变中间颜色, 渐变末尾颜色, 渐变过渡强度, 排版方向, 字间距, 字体粗细
                )
                if 不透明度 < 1.0 or anim_params["opacity"] < 1.0:
                    combined_opacity = 不透明度 * anim_params["opacity"]
                    alpha_mask = text_img.split()[3].point(lambda p: int(p * combined_opacity))
                    text_img.putalpha(alpha_mask)
                    
            elif 描边大小 > 0:
                # 描边文字（支持横竖排+字体粗细）
                text_img = self.create_stroke_text(
                    display_text, font, text_color, stroke_color, 描边大小,
                    描边位置, 描边不透明度, canvas_width, canvas_height, 
                    字间距, 排版方向, 字体粗细
                )
                if 不透明度 < 1.0 or anim_params["opacity"] < 1.0:
                    combined_opacity = 不透明度 * anim_params["opacity"]
                    alpha_mask = text_img.split()[3].point(lambda p: int(p * combined_opacity))
                    text_img.putalpha(alpha_mask)
                    
            elif 渐变效果 != "无":
                # 渐变文字（支持横竖排+字体粗细）
                text_img = self.create_gradient_text(
                    display_text, font, 渐变效果,
                    渐变开头颜色, 渐变中间颜色, 渐变末尾颜色, 渐变过渡强度, 排版方向, 字间距, 字体粗细
                )
                if 不透明度 < 1.0 or anim_params["opacity"] < 1.0:
                    combined_opacity = 不透明度 * anim_params["opacity"]
                    alpha_mask = text_img.split()[3].point(lambda p: int(p * combined_opacity))
                    text_img.putalpha(alpha_mask)
                    
            elif 排版方向 == "竖排":
                # 纯色竖排文字（支持字体粗细）
                text_img = self.create_vertical_text(display_text, font, text_color, 字间距, 字体粗细)
                if 不透明度 < 1.0 or anim_params["opacity"] < 1.0:
                    combined_opacity = 不透明度 * anim_params["opacity"]
                    alpha_mask = text_img.split()[3].point(lambda p: int(p * combined_opacity))
                    text_img.putalpha(alpha_mask)
                    
            else:
                # 纯色横排文字（支持字体粗细+字间距）
                temp_img = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
                temp_draw = ImageDraw.Draw(temp_img)
                alpha = int(255 * 不透明度 * anim_params["opacity"])
                
                if 字间距 != 0:
                    # 有字间距时，逐字符绘制
                    chars = list(display_text.replace('\n', ''))
                    measure_img = Image.new('RGBA', (1, 1))
                    measure_draw = ImageDraw.Draw(measure_img)
                    
                    char_widths = []
                    for char in chars:
                        bbox = measure_draw.textbbox((0, 0), char, font=font)
                        char_widths.append(bbox[2] - bbox[0])
                    
                    total_width = sum(char_widths) + (len(chars) - 1) * max(0, 字间距)
                    x_offset = (canvas_width - total_width) // 2
                    
                    for char, char_width in zip(chars, char_widths):
                        char_x = x_offset + char_width // 2
                        if 字体粗细 == "常规":
                            temp_draw.text((char_x, canvas_height//2), char, 
                                         font=font, fill=text_color + (alpha,), anchor='mm')
                        else:
                            self.create_bold_text(temp_draw, (char_x, canvas_height//2), 
                                                char, font, text_color + (alpha,), 字体粗细)
                        x_offset += char_width + max(0, 字间距)
                else:
                    # 无字间距时，整体绘制
                    if 字体粗细 == "常规":
                        temp_draw.text((canvas_width//2, canvas_height//2), display_text, 
                                     font=font, fill=text_color + (alpha,), anchor='mm')
                    else:
                        self.create_bold_text(temp_draw, (canvas_width//2, canvas_height//2), 
                                            display_text, font, text_color + (alpha,), 字体粗细)
                
                text_img = temp_img
            
            # 应用缩放（使用高质量LANCZOS算法）
            if anim_params["scale"] != 1.0 and anim_params["scale"] > 0:
                new_size = (
                    max(1, int(text_img.width * anim_params["scale"])), 
                    max(1, int(text_img.height * anim_params["scale"]))
                )
                text_img = text_img.resize(new_size, Image.LANCZOS)
            
            # 应用旋转
            total_rotation = 字体角度 + anim_params["rotation"]
            if total_rotation != 0:
                text_img = text_img.rotate(-total_rotation, expand=True, resample=Image.BICUBIC)
            
            # 创建最终图层
            final_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            
            # 计算位置
            text_x = int(width * 位置X百分比 / 100.0) + anim_params["offset_x"]
            text_y = int(height * 位置Y百分比 / 100.0) + anim_params["offset_y"]
            
            paste_x = text_x - text_img.width // 2
            paste_y = text_y - text_img.height // 2
            
            # 添加投影
            if 投影距离 > 0 and 投影强度 > 0:
                projection = self.create_projection(text_img, 投影角度, 投影距离, 投影强度, 投影模糊)
                try:
                    final_layer.paste(projection, (paste_x, paste_y), projection)
                except Exception as e:
                    print(f"警告: 投影粘贴失败 - {e}")
            
            # 粘贴文字
            try:
                final_layer.paste(text_img, (paste_x, paste_y), text_img)
            except Exception as e:
                print(f"警告: 文字粘贴失败 - {e}")
            
            # 合成最终图像
            img_pil = img_pil.convert('RGBA')
            result = Image.alpha_composite(img_pil, final_layer)
            result = result.convert('RGB')
            
            result_array = np.array(result).astype(np.float32) / 255.0
            output_images.append(result_array)
        
        # 转换为tensor
        output_tensor = torch.from_numpy(np.stack(output_images))
        
        print(f"[增强字幕] 完成: 处理{batch_size}帧, 字幕显示{end_frame - start_frame}帧")
        
        # 返回图像和参数（供后续节点使用）
        return (output_tensor, video_duration_seconds, batch_size, 字幕文本, 开始时间, 结束时间)


# ComfyUI节点映射
NODE_CLASS_MAPPINGS = {
    "HAIGC_VideoSubtitleEnhanced": VideoSubtitleEnhancedNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "HAIGC_VideoSubtitleEnhanced": "视频字幕增强版(优化) 🎬"
}
