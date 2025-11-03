"""
视频拼接平滑过渡节点
使两段视频拼接处实现平滑过渡，包括交叉淡化、光流混合等高级效果
"""

import torch
import numpy as np
from PIL import Image
import torch.nn.functional as F
import math

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
                    "直接拼接",
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
        """创建渐变遮罩（优化版 - 向量化计算，方向已修正）"""
        # 避免除以0
        progress = max(0.001, min(0.999, progress))
        
        if direction == "左到右":
            # 从左到右擦除：视频B从左边开始逐渐覆盖视频A
            # 左边mask值应该先达到1，所以坐标从1到0递减
            x_coords = np.linspace(1, 0, width, dtype=np.float32)
            mask = np.clip((x_coords - (1 - progress)) / progress, 0, 1)
            mask = np.broadcast_to(mask, (height, width)).copy()
                
        elif direction == "右到左":
            # 从右到左擦除：视频B从右边开始逐渐覆盖视频A
            # 右边mask值应该先达到1，所以坐标从0到1递增
            x_coords = np.linspace(0, 1, width, dtype=np.float32)
            mask = np.clip((x_coords - (1 - progress)) / progress, 0, 1)
            mask = np.broadcast_to(mask, (height, width)).copy()
                
        elif direction == "上到下":
            # 从上到下擦除：视频B从上方开始逐渐覆盖视频A
            # 上边mask值应该先达到1，所以坐标从1到0递减
            y_coords = np.linspace(1, 0, height, dtype=np.float32).reshape(-1, 1)
            mask = np.clip((y_coords - (1 - progress)) / progress, 0, 1)
            mask = np.broadcast_to(mask, (height, width)).copy()
                
        elif direction == "下到上":
            # 从下到上擦除：视频B从下方开始逐渐覆盖视频A
            # 下边mask值应该先达到1，所以坐标从0到1递增
            y_coords = np.linspace(0, 1, height, dtype=np.float32).reshape(-1, 1)
            mask = np.clip((y_coords - (1 - progress)) / progress, 0, 1)
            mask = np.broadcast_to(mask, (height, width)).copy()
        else:
            mask = np.ones((height, width), dtype=np.float32) * progress
        
        return mask
    
    def create_radial_mask(self, width, height, progress, shape="circle"):
        """创建径向遮罩（从中心向外扩散）"""
        # 避免除以0
        progress = max(0.001, min(0.999, progress))
        
        y, x = np.ogrid[:height, :width]
        center_y, center_x = height / 2, width / 2
        
        if shape == "circle":
            # 圆形扩散：从中心向外
            max_radius = np.sqrt(center_x**2 + center_y**2)
            distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            # 计算归一化距离
            normalized_distance = distance / max_radius
            # 从中心向外扩散：中心先显示(mask=1)，边缘后显示(mask=0)
            # progress=0时，中心很小范围为1；progress=1时，全部为1
            mask = np.clip(1 - (normalized_distance - progress) / (1 - progress + 0.001), 0, 1)
            
        elif shape == "square":
            # 方形扩散：从中心向外
            max_dist = max(center_x, center_y)
            dist_x = np.abs(x - center_x)
            dist_y = np.abs(y - center_y)
            distance = np.maximum(dist_x, dist_y)
            # 计算归一化距离
            normalized_distance = distance / max_dist
            # 从中心向外扩散
            mask = np.clip(1 - (normalized_distance - progress) / (1 - progress + 0.001), 0, 1)
        
        return mask.astype(np.float32)
    
    def create_transition(self, 视频A, 视频B, 过渡类型="交叉淡化",
                         过渡时长帧数=30,
                         过渡位置="两者中间", 缓动函数="缓入缓出", 边缘羽化=0):
        """创建视频过渡效果 - 纯粹的视频拼接和过渡，无色彩调整"""
        
        print(f"[视频拼接节点] 纯粹拼接模式（已移除所有色彩调整）")
        
        batch_a = 视频A.shape[0]
        batch_b = 视频B.shape[0]
        height = 视频A.shape[1]
        width = 视频A.shape[2]
        
        # 如果是直接拼接，不应用任何色彩调整，保持视频原色
        if 过渡类型 == "直接拼接":
            # 确保两个视频尺寸一致
            if 视频B.shape[1] != height or 视频B.shape[2] != width:
                视频B_resized = []
                for i in range(batch_b):
                    frame = 视频B[i].cpu().numpy()
                    frame_pil = Image.fromarray((frame * 255).astype(np.uint8))
                    frame_pil = frame_pil.resize((width, height), Image.LANCZOS)
                    frame_resized = np.array(frame_pil).astype(np.float32) / 255.0
                    视频B_resized.append(frame_resized)
                视频B = torch.from_numpy(np.stack(视频B_resized)).to(视频A.device)
            
            # 直接拼接，无色彩调整，保持视频原色
            
            # 直接拼接两个视频
            final_output = torch.cat([视频A, 视频B], dim=0)
            total_frames = final_output.shape[0]
            
            print(f"视频直接拼接完成:")
            print(f"  - 视频A帧数: {batch_a}")
            print(f"  - 视频B帧数: {batch_b}")
            print(f"  - 总输出帧数: {total_frames}")
            
            return (final_output, total_frames)
        
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
        
        # 生成过渡帧（无色彩调整）
        transition_output = []
        
        for i in range(actual_transition_frames):
            # 计算过渡进度
            progress = i / max(actual_transition_frames - 1, 1)
            progress = self.easing_function(progress, 缓动函数)
            
            frame_a = transition_frames_a[i]
            frame_b = transition_frames_b[i]
            
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
                    # 向左推移：A向左移出，B从右侧进入
                    offset = int(width * progress)
                    offset = min(offset, width)  # 防止越界
                    blended = torch.zeros_like(frame_a)
                    if offset < width:
                        # A的剩余部分
                        blended[:, :width-offset, :] = frame_a[:, offset:, :]
                        # B进入的部分
                        blended[:, width-offset:, :] = frame_b[:, :offset, :]
                    else:
                        # offset >= width，完全显示B
                        blended = frame_b.clone()
                        
                elif direction == "右":
                    # 向右推移：A向右移出，B从左侧进入
                    offset = int(width * progress)
                    offset = min(offset, width)
                    blended = torch.zeros_like(frame_a)
                    if offset < width:
                        # A的剩余部分
                        blended[:, offset:, :] = frame_a[:, :width-offset, :]
                        # B进入的部分
                        blended[:, :offset, :] = frame_b[:, width-offset:, :]
                    else:
                        # offset >= width，完全显示B
                        blended = frame_b.clone()
                        
                elif direction == "上":
                    # 向上推移：A向上移出，B从下方进入
                    offset = int(height * progress)
                    offset = min(offset, height)
                    blended = torch.zeros_like(frame_a)
                    if offset < height:
                        # A的剩余部分
                        blended[:height-offset, :, :] = frame_a[offset:, :, :]
                        # B进入的部分
                        blended[height-offset:, :, :] = frame_b[:offset, :, :]
                    else:
                        # offset >= height，完全显示B
                        blended = frame_b.clone()
                        
                elif direction == "下":
                    # 向下推移：A向下移出，B从上方进入
                    offset = int(height * progress)
                    offset = min(offset, height)
                    blended = torch.zeros_like(frame_a)
                    if offset < height:
                        # A的剩余部分
                        blended[offset:, :, :] = frame_a[:height-offset, :, :]
                        # B进入的部分
                        blended[:offset, :, :] = frame_b[height-offset:, :, :]
                    else:
                        # offset >= height，完全显示B
                        blended = frame_b.clone()
                else:
                    blended = frame_a * (1 - progress) + frame_b * progress
                    
            elif 过渡类型 == "溶解":
                # 创建随机噪声遮罩
                noise = torch.rand_like(frame_a[:, :, 0])
                mask = (noise < progress).float().unsqueeze(-1)
                blended = frame_a * (1 - mask) + frame_b * mask
                
            elif 过渡类型 == "缩放过渡":
                # 真正的缩放效果：A缩小消失，B放大出现
                if progress < 0.5:
                    # 前半段：A缩小到中心
                    scale_factor = 1.0 - progress  # 1.0 -> 0.5
                    if scale_factor > 0.01:
                        # 计算缩放后的尺寸
                        new_h = max(1, int(height * scale_factor))
                        new_w = max(1, int(width * scale_factor))
                        
                        # 缩放A（HWC -> CHW -> NCHW -> 缩放 -> NCHW -> CHW -> HWC）
                        frame_a_resized = F.interpolate(
                            frame_a.permute(2, 0, 1).unsqueeze(0),  # HWC -> NCHW
                            size=(new_h, new_w),
                            mode='bilinear',
                            align_corners=False
                        ).squeeze(0).permute(1, 2, 0)  # NCHW -> HWC
                        
                        # 居中放置缩放后的A，其余用B填充（淡入）
                        blended = frame_b.clone()
                        y_offset = (height - new_h) // 2
                        x_offset = (width - new_w) // 2
                        
                        # 混合系数：随着进度增加，A的不透明度降低
                        alpha = 1.0 - (progress * 2)  # 1.0 -> 0.0
                        blended[y_offset:y_offset+new_h, x_offset:x_offset+new_w, :] = \
                            frame_a_resized * alpha + blended[y_offset:y_offset+new_h, x_offset:x_offset+new_w, :] * (1 - alpha)
                    else:
                        # 缩得太小了，直接显示B
                        blended = frame_b.clone()
                        
                else:
                    # 后半段：B从中心放大
                    scale_factor = (progress - 0.5) * 2  # 0.0 -> 1.0
                    if scale_factor < 0.99:
                        # B从小放大
                        initial_scale = 0.1 + scale_factor * 0.9  # 0.1 -> 1.0
                        new_h = max(1, int(height * initial_scale))
                        new_w = max(1, int(width * initial_scale))
                        
                        # 缩放B
                        frame_b_resized = F.interpolate(
                            frame_b.permute(2, 0, 1).unsqueeze(0),
                            size=(new_h, new_w),
                            mode='bilinear',
                            align_corners=False
                        ).squeeze(0).permute(1, 2, 0)
                        
                        # 居中放置，背景用B的模糊版本
                        blended = frame_b.clone()
                        y_offset = (height - new_h) // 2
                        x_offset = (width - new_w) // 2
                        blended[y_offset:y_offset+new_h, x_offset:x_offset+new_w, :] = frame_b_resized
                    else:
                        # 已经放大到全尺寸
                        blended = frame_b.clone()
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

