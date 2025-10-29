"""
获取视频尾帧节点
从视频序列中提取最后一帧或指定的末尾帧
"""

import torch
import numpy as np

class VideoLastFrameNode:
    """获取视频尾帧节点"""
    
    def __init__(self):
        self.type = "HAIGC_VideoLastFrame"
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),  # 输入图片序列/视频帧
                "提取模式": (["最后一帧", "最后N帧", "倒数第N帧"], {
                    "default": "最后一帧"
                }),
                "帧数N": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 1000,
                    "step": 1,
                    "display": "number"
                }),
                "重复输出次数": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 1000,
                    "step": 1,
                    "display": "number"
                }),
            },
            "optional": {
                "输出帧信息": ("BOOLEAN", {
                    "default": True
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "INT", "INT", "INT")
    RETURN_NAMES = ("尾帧图像", "总帧数", "提取帧数", "输出帧数")
    FUNCTION = "get_last_frame"
    CATEGORY = "HAIGC工具集/视频处理"
    
    def get_last_frame(self, images, 提取模式="最后一帧", 帧数N=1, 
                      重复输出次数=1, 输出帧信息=True):
        """提取视频尾帧"""
        
        batch_size = images.shape[0]
        
        if batch_size == 0:
            raise ValueError("输入图像序列为空")
        
        # 根据模式提取帧
        if 提取模式 == "最后一帧":
            # 提取最后一帧
            output_frames = images[-1:, :, :, :]
            extracted_count = 1
            
        elif 提取模式 == "最后N帧":
            # 提取最后N帧
            n = min(帧数N, batch_size)
            output_frames = images[-n:, :, :, :]
            extracted_count = n
            
        elif 提取模式 == "倒数第N帧":
            # 提取倒数第N帧（单帧）
            index = min(帧数N, batch_size)
            output_frames = images[-index:-index+1, :, :, :]
            if output_frames.shape[0] == 0:  # 边界情况处理
                output_frames = images[-1:, :, :, :]
            extracted_count = 1
        
        else:
            # 默认返回最后一帧
            output_frames = images[-1:, :, :, :]
            extracted_count = 1
        
        # 应用重复输出
        if 重复输出次数 > 1:
            repeated_frames = output_frames.repeat(重复输出次数, 1, 1, 1)
            output_frames = repeated_frames
        
        output_count = output_frames.shape[0]
        
        # 输出信息
        if 输出帧信息:
            print(f"视频尾帧提取:")
            print(f"  - 总帧数: {batch_size}")
            print(f"  - 提取模式: {提取模式}")
            print(f"  - 提取帧数: {extracted_count}")
            print(f"  - 重复次数: {重复输出次数}")
            print(f"  - 输出帧数: {output_count}")
        
        return (output_frames, batch_size, extracted_count, output_count)

