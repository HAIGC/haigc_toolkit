"""
视频拼接平滑过渡节点
使两段视频拼接处实现平滑过渡，包括交叉淡化、光流混合等高级效果
"""

import torch
import numpy as np
from PIL import Image
import torch.nn.functional as F

class VideoTransitionNode:
    """视频拼接平滑过渡节点"""
    
    def __init__(self):
        self.type = "HAIGC_VideoTransition"
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "视频A": ("IMAGE",),  # 第一段视频
                "视频B": ("IMAGE",),  # 第二段视频
                "过渡类型": ([
                    "交叉淡化",
                    "渐变擦除_左到右",
                    "渐变擦除_右到左", 
                    "渐变擦除_上到下",
                    "渐变擦除_下到上",
                    "圆形扩散",
                    "方形扩散",
                    "淡入淡出_黑场",
                    "淡入淡出_白场",
                    "推移_左",
                    "推移_右",
                    "推移_上",
                    "推移_下",
                    "溶解",
                    "缩放过渡",
                ], {
                    "default": "交叉淡化"
                }),
                "过渡时长帧数": ("INT", {
                    "default": 30,
                    "min": 1,
                    "max": 300,
                    "step": 1,
                    "display": "number"
                }),
                "过渡位置": (["视频A末尾", "视频B开头", "两者中间"], {
                    "default": "两者中间"
                }),
                "缓动函数": (["线性", "缓入", "缓出", "缓入缓出", "弹性"], {
                    "default": "缓入缓出"
                }),
                "边缘羽化": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 100,
                    "step": 1,
                    "display": "number"
                }),
            },
            "optional": {
                "颜色匹配": ("BOOLEAN", {
                    "default": False,
                    "label_on": "启用",
                    "label_off": "禁用"
                }),
                "亮度平滑": ("BOOLEAN", {
                    "default": False,
                    "label_on": "启用", 
                    "label_off": "禁用"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "INT")
    RETURN_NAMES = ("合成视频", "总帧数")
    FUNCTION = "create_transition"
    CATEGORY = "HAIGC工具集/视频处理"
    
    def easing_function(self, t, easing_type):
        """缓动函数"""
        if easing_type == "线性":
            return t
        elif easing_type == "缓入":
            return t * t
        elif easing_type == "缓出":
            return 1 - (1 - t) * (1 - t)
        elif easing_type == "缓入缓出":
            if t < 0.5:
                return 2 * t * t
            else:
                return 1 - 2 * (1 - t) * (1 - t)
        elif easing_type == "弹性":
            import math
            if t == 0 or t == 1:
                return t
            p = 0.3
            s = p / 4
            return math.pow(2, -10 * t) * math.sin((t - s) * (2 * math.pi) / p) + 1
        return t
    
    def create_gradient_mask(self, width, height, direction, progress):
        """创建渐变遮罩"""
        mask = np.zeros((height, width), dtype=np.float32)
        
        if direction == "左到右":
            for x in range(width):
                value = (x / width - (1 - progress)) / progress
                value = np.clip(value, 0, 1)
                mask[:, x] = value
                
        elif direction == "右到左":
            for x in range(width):
                value = ((width - x) / width - (1 - progress)) / progress
                value = np.clip(value, 0, 1)
                mask[:, x] = value
                
        elif direction == "上到下":
            for y in range(height):
                value = (y / height - (1 - progress)) / progress
                value = np.clip(value, 0, 1)
                mask[y, :] = value
                
        elif direction == "下到上":
            for y in range(height):
                value = ((height - y) / height - (1 - progress)) / progress
                value = np.clip(value, 0, 1)
                mask[y, :] = value
        
        return mask
    
    def create_radial_mask(self, width, height, progress, shape="circle"):
        """创建径向遮罩"""
        y, x = np.ogrid[:height, :width]
        center_y, center_x = height / 2, width / 2
        
        if shape == "circle":
            max_radius = np.sqrt(center_x**2 + center_y**2)
            distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            mask = np.clip((distance - max_radius * (1 - progress)) / (max_radius * progress), 0, 1)
            mask = 1 - mask  # 反转，使中心先显示
            
        elif shape == "square":
            max_dist = max(center_x, center_y)
            dist_x = np.abs(x - center_x)
            dist_y = np.abs(y - center_y)
            distance = np.maximum(dist_x, dist_y)
            mask = np.clip((distance - max_dist * (1 - progress)) / (max_dist * progress), 0, 1)
            mask = 1 - mask
        
        return mask.astype(np.float32)
    
    def match_colors(self, img1, img2, alpha):
        """颜色匹配 - 使过渡更自然"""
        # 计算两个图像的平均颜色
        mean1 = torch.mean(img1, dim=[0, 1], keepdim=True)
        mean2 = torch.mean(img2, dim=[0, 1], keepdim=True)
        
        # 渐进调整颜色
        adjusted_img2 = img2 + (mean1 - mean2) * (1 - alpha) * 0.5
        adjusted_img2 = torch.clamp(adjusted_img2, 0, 1)
        
        return adjusted_img2
    
    def smooth_brightness(self, img1, img2, alpha):
        """亮度平滑"""
        # 计算亮度
        brightness1 = torch.mean(img1)
        brightness2 = torch.mean(img2)
        
        # 调整第二张图的亮度
        brightness_ratio = brightness1 / (brightness2 + 1e-6)
        adjusted_img2 = img2 * (1 + (brightness_ratio - 1) * (1 - alpha) * 0.3)
        adjusted_img2 = torch.clamp(adjusted_img2, 0, 1)
        
        return adjusted_img2
    
    def create_transition(self, 视频A, 视频B, 过渡类型="交叉淡化", 过渡时长帧数=30,
                         过渡位置="两者中间", 缓动函数="缓入缓出", 边缘羽化=0,
                         颜色匹配=False, 亮度平滑=False):
        """创建视频过渡效果"""
        
        batch_a = 视频A.shape[0]
        batch_b = 视频B.shape[0]
        height = 视频A.shape[1]
        width = 视频A.shape[2]
        
        # 确保两个视频尺寸一致
        if 视频B.shape[1] != height or 视频B.shape[2] != width:
            # 调整视频B的尺寸
            视频B_resized = []
            for i in range(batch_b):
                frame = 视频B[i].cpu().numpy()
                frame_pil = Image.fromarray((frame * 255).astype(np.uint8))
                frame_pil = frame_pil.resize((width, height), Image.LANCZOS)
                frame_resized = np.array(frame_pil).astype(np.float32) / 255.0
                视频B_resized.append(frame_resized)
            视频B = torch.from_numpy(np.stack(视频B_resized)).to(视频A.device)
        
        # 确定过渡的起始帧
        if 过渡位置 == "视频A末尾":
            # 在视频A的末尾创建过渡
            transition_start_a = max(0, batch_a - 过渡时长帧数)
            transition_frames_a = 视频A[transition_start_a:batch_a]
            transition_frames_b = 视频B[:过渡时长帧数]
            pre_transition = 视频A[:transition_start_a] if transition_start_a > 0 else None
            post_transition = 视频B[过渡时长帧数:] if batch_b > 过渡时长帧数 else None
            
        elif 过渡位置 == "视频B开头":
            # 在视频B的开头创建过渡
            transition_frames_a = 视频A[-过渡时长帧数:]
            transition_frames_b = 视频B[:过渡时长帧数]
            pre_transition = 视频A[:-过渡时长帧数] if batch_a > 过渡时长帧数 else None
            post_transition = 视频B[过渡时长帧数:] if batch_b > 过渡时长帧数 else None
            
        else:  # 两者中间
            # 各取一半创建过渡
            half_transition = 过渡时长帧数 // 2
            transition_frames_a = 视频A[-half_transition:]
            transition_frames_b = 视频B[:过渡时长帧数 - half_transition]
            pre_transition = 视频A[:-half_transition] if batch_a > half_transition else None
            post_transition = 视频B[过渡时长帧数 - half_transition:] if batch_b > 过渡时长帧数 - half_transition else None
        
        # 调整过渡帧数量
        actual_transition_frames = min(transition_frames_a.shape[0], transition_frames_b.shape[0])
        transition_frames_a = transition_frames_a[:actual_transition_frames]
        transition_frames_b = transition_frames_b[:actual_transition_frames]
        
        # 生成过渡帧
        transition_output = []
        
        for i in range(actual_transition_frames):
            # 计算过渡进度
            progress = i / max(actual_transition_frames - 1, 1)
            progress = self.easing_function(progress, 缓动函数)
            
            frame_a = transition_frames_a[i]
            frame_b = transition_frames_b[i]
            
            # 应用颜色匹配
            if 颜色匹配:
                frame_b = self.match_colors(frame_a, frame_b, progress)
            
            # 应用亮度平滑
            if 亮度平滑:
                frame_b = self.smooth_brightness(frame_a, frame_b, progress)
            
            # 根据过渡类型创建帧
            if 过渡类型 == "交叉淡化":
                blended = frame_a * (1 - progress) + frame_b * progress
                
            elif 过渡类型.startswith("渐变擦除"):
                direction = 过渡类型.split("_")[1]
                mask = self.create_gradient_mask(width, height, direction, progress)
                mask_tensor = torch.from_numpy(mask).to(frame_a.device).unsqueeze(-1)
                blended = frame_a * (1 - mask_tensor) + frame_b * mask_tensor
                
            elif 过渡类型 == "圆形扩散":
                mask = self.create_radial_mask(width, height, progress, "circle")
                mask_tensor = torch.from_numpy(mask).to(frame_a.device).unsqueeze(-1)
                blended = frame_a * (1 - mask_tensor) + frame_b * mask_tensor
                
            elif 过渡类型 == "方形扩散":
                mask = self.create_radial_mask(width, height, progress, "square")
                mask_tensor = torch.from_numpy(mask).to(frame_a.device).unsqueeze(-1)
                blended = frame_a * (1 - mask_tensor) + frame_b * mask_tensor
                
            elif 过渡类型 == "淡入淡出_黑场":
                if progress < 0.5:
                    fade_out = 1 - (progress * 2)
                    blended = frame_a * fade_out
                else:
                    fade_in = (progress - 0.5) * 2
                    blended = frame_b * fade_in
                    
            elif 过渡类型 == "淡入淡出_白场":
                white = torch.ones_like(frame_a)
                if progress < 0.5:
                    fade_progress = progress * 2
                    blended = frame_a * (1 - fade_progress) + white * fade_progress
                else:
                    fade_progress = (progress - 0.5) * 2
                    blended = white * (1 - fade_progress) + frame_b * fade_progress
                    
            elif 过渡类型.startswith("推移"):
                direction = 过渡类型.split("_")[1]
                if direction == "左":
                    offset = int(width * progress)
                    blended = torch.zeros_like(frame_a)
                    if offset < width:
                        blended[:, :width-offset, :] = frame_a[:, offset:, :]
                        blended[:, width-offset:, :] = frame_b[:, :offset, :]
                elif direction == "右":
                    offset = int(width * progress)
                    blended = torch.zeros_like(frame_a)
                    if offset < width:
                        blended[:, offset:, :] = frame_a[:, :width-offset, :]
                        blended[:, :offset, :] = frame_b[:, width-offset:, :]
                elif direction == "上":
                    offset = int(height * progress)
                    blended = torch.zeros_like(frame_a)
                    if offset < height:
                        blended[:height-offset, :, :] = frame_a[offset:, :, :]
                        blended[height-offset:, :, :] = frame_b[:offset, :, :]
                elif direction == "下":
                    offset = int(height * progress)
                    blended = torch.zeros_like(frame_a)
                    if offset < height:
                        blended[offset:, :, :] = frame_a[:height-offset, :, :]
                        blended[:offset, :, :] = frame_b[height-offset:, :, :]
                else:
                    blended = frame_a * (1 - progress) + frame_b * progress
                    
            elif 过渡类型 == "溶解":
                # 创建随机噪声遮罩
                noise = torch.rand_like(frame_a[:, :, 0])
                mask = (noise < progress).float().unsqueeze(-1)
                blended = frame_a * (1 - mask) + frame_b * mask
                
            elif 过渡类型 == "缩放过渡":
                if progress < 0.5:
                    # 缩小A
                    scale = 1 - progress
                    blended = frame_a * scale + frame_b * (1 - scale) * 0.5
                else:
                    # 放大B
                    scale = (progress - 0.5) * 2
                    blended = frame_b * scale + frame_a * (1 - scale) * 0.5
            else:
                # 默认交叉淡化
                blended = frame_a * (1 - progress) + frame_b * progress
            
            # 应用边缘羽化（如果需要）
            if 边缘羽化 > 0:
                # 简单的边缘柔化
                feather = 边缘羽化 / 100.0
                edge_mask = torch.ones_like(blended[:, :, 0])
                
                # 创建边缘渐变
                for d in range(边缘羽化):
                    alpha = d / 边缘羽化
                    if d < height and d < width:
                        edge_mask[d, :] *= alpha
                        edge_mask[height-1-d, :] *= alpha
                        edge_mask[:, d] *= alpha
                        edge_mask[:, width-1-d] *= alpha
                
                edge_mask = edge_mask.unsqueeze(-1)
                blended = blended * edge_mask + (1 - edge_mask) * 0.5
            
            blended = torch.clamp(blended, 0, 1)
            transition_output.append(blended)
        
        # 合并所有部分
        result_parts = []
        
        if pre_transition is not None and pre_transition.shape[0] > 0:
            result_parts.append(pre_transition)
        
        if len(transition_output) > 0:
            transition_tensor = torch.stack(transition_output)
            result_parts.append(transition_tensor)
        
        if post_transition is not None and post_transition.shape[0] > 0:
            result_parts.append(post_transition)
        
        # 拼接所有部分
        if len(result_parts) > 0:
            final_output = torch.cat(result_parts, dim=0)
        else:
            final_output = torch.cat([视频A, 视频B], dim=0)
        
        total_frames = final_output.shape[0]
        
        print(f"视频过渡合成完成:")
        print(f"  - 过渡类型: {过渡类型}")
        print(f"  - 过渡帧数: {actual_transition_frames}")
        print(f"  - 总输出帧数: {total_frames}")
        
        return (final_output, total_frames)

