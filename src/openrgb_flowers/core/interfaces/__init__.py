"""Core interfaces adhering to Interface Segregation Principle."""
from openrgb_flowers.core.interfaces.i_color_palette import IColorPalette
from openrgb_flowers.core.interfaces.i_flower_model import IFlowerModel
from openrgb_flowers.core.interfaces.i_blend_strategy import IBlendStrategy
from openrgb_flowers.core.interfaces.i_layout_provider import ILayoutProvider
from openrgb_flowers.core.interfaces.i_frame_transmitter import IFrameTransmitter
from openrgb_flowers.core.interfaces.i_effect_engine import IEffectEngine
from openrgb_flowers.core.interfaces.i_visualizer import IVisualizer

__all__ = [
    "IColorPalette",
    "IFlowerModel",
    "IBlendStrategy",
    "ILayoutProvider",
    "IFrameTransmitter",
    "IEffectEngine",
    "IVisualizer",
]
