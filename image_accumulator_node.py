"""
图片批次累积节点
可对输入的图片进行累积，并在合适时机批量输出
"""

import torch
import numpy as np

class ImageAccumulatorNode:
    """图片批次累积节点"""
    
    def __init__(self):
        self.type = "HAIGC_ImageAccumulator"
        self.accumulated_images = []
        self.is_accumulating = True
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "批次重复次数": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "display": "number"
                }),
                "最大累积数量": ("INT", {
                    "default": 100,
                    "min": 1,
                    "max": 10000,
                    "step": 1,
                    "display": "number"
                }),
                "触发输出": ("BOOLEAN", {
                    "default": False,
                    "label_on": "立即输出",
                    "label_off": "继续累积"
                }),
                "清空缓存": ("BOOLEAN", {
                    "default": False,
                    "label_on": "清空",
                    "label_off": "保留"
                }),
            },
            "optional": {
                "images": ("IMAGE",),  # 可选输入
            }
        }
    
    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("图像批次", "累积数量", "总帧数")
    FUNCTION = "accumulate_images"
    CATEGORY = "HAIGC工具集/图片处理"
    OUTPUT_NODE = False
    
    def accumulate_images(self, 批次重复次数=1, 最大累积数量=100, 
                         触发输出=False, 清空缓存=False, images=None):
        """累积图片并在适当时机输出"""
        
        # 清空缓存
        if 清空缓存:
            self.accumulated_images = []
            self.is_accumulating = True
            print("图片累积器：缓存已清空")
            # 返回空批次
            empty_image = torch.zeros((1, 64, 64, 3))
            return (empty_image, 0, 0)
        
        # 如果有新图片输入，添加到累积列表
        if images is not None:
            batch_size = images.shape[0]
            
            # 将批次中的每张图片分别添加
            for i in range(batch_size):
                if len(self.accumulated_images) < 最大累积数量:
                    self.accumulated_images.append(images[i:i+1])
                else:
                    print(f"图片累积器：已达到最大累积数量 {最大累积数量}")
                    break
            
            print(f"图片累积器：累积中... 当前数量: {len(self.accumulated_images)}")
        
        # 判断是否需要输出
        should_output = False
        
        # 手动触发输出
        if 触发输出:
            should_output = True
            print("图片累积器：手动触发输出")
        
        # 达到最大累积数量
        elif len(self.accumulated_images) >= 最大累积数量:
            should_output = True
            print(f"图片累积器：达到最大累积数量，自动输出")
        
        # 如果需要输出
        if should_output and len(self.accumulated_images) > 0:
            # 合并所有累积的图片
            output_batch = torch.cat(self.accumulated_images, dim=0)
            accumulated_count = len(self.accumulated_images)
            
            # 应用批次重复
            if 批次重复次数 > 1:
                repeated_batches = [output_batch] * 批次重复次数
                output_batch = torch.cat(repeated_batches, dim=0)
                print(f"图片累积器：批次重复 {批次重复次数} 次")
            
            total_frames = output_batch.shape[0]
            
            print(f"图片累积器：输出批次 - 累积数量: {accumulated_count}, 重复后总帧数: {total_frames}")
            
            # 清空累积列表以备下次使用
            self.accumulated_images = []
            self.is_accumulating = True
            
            return (output_batch, accumulated_count, total_frames)
        
        # 如果还在累积中，返回当前状态
        else:
            # 如果还没有累积任何图片，返回空批次
            if len(self.accumulated_images) == 0:
                empty_image = torch.zeros((1, 64, 64, 3))
                return (empty_image, 0, 0)
            
            # 返回当前累积的图片（用于预览）
            preview_batch = torch.cat(self.accumulated_images, dim=0)
            accumulated_count = len(self.accumulated_images)
            
            return (preview_batch, accumulated_count, accumulated_count)
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # 每次都标记为变化，确保节点能够持续累积
        return float("nan")

