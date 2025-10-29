"""
HAIGC Toolkit - ComfyUI节点工具集
包含视频字幕、图片处理、视频处理等实用功能
"""

from .subtitle_node_enhanced import VideoSubtitleEnhancedNode
from .image_accumulator_node import ImageAccumulatorNode
from .video_last_frame_node import VideoLastFrameNode
from .video_transition_node import VideoTransitionNode
from .version import __version__, print_version_info

# 打印版本信息
print_version_info()

# 节点类映射
NODE_CLASS_MAPPINGS = {
    "HAIGC_VideoSubtitleEnhanced": VideoSubtitleEnhancedNode,
    "HAIGC_ImageAccumulator": ImageAccumulatorNode,
    "HAIGC_VideoLastFrame": VideoLastFrameNode,
    "HAIGC_VideoTransition": VideoTransitionNode,
}

# 节点显示名称映射（中文）
NODE_DISPLAY_NAME_MAPPINGS = {
    "HAIGC_VideoSubtitleEnhanced": "视频字幕增强版(v2.0) 🎬",
    "HAIGC_ImageAccumulator": "图片批次累积 📦",
    "HAIGC_VideoLastFrame": "获取视频尾帧 🎞️",
    "HAIGC_VideoTransition": "视频拼接过渡 🔗",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

