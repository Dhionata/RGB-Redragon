"""HSV Color representation for smooth floral color transitions."""
from __future__ import annotations
from dataclasses import dataclass
import colorsys
from typing import Tuple
from openrgb_flowers.core.models.color_rgb import ColorRGB


@dataclass(frozen=True, slots=True)
class ColorHSV:
    """Represents a color in HSV space (Hue: 0-360, Saturation: 0-1, Value: 0-1)."""

    h: float
    s: float
    v: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "h", float(self.h) % 360.0)
        object.__setattr__(self, "s", max(0.0, min(1.0, float(self.s))))
        object.__setattr__(self, "v", max(0.0, min(1.0, float(self.v))))

    def to_rgb(self) -> ColorRGB:
        """Converts HSV to RGB model."""
        r_f, g_f, b_f = colorsys.hsv_to_rgb(self.h / 360.0, self.s, self.v)
        return ColorRGB.from_normalized(r_f, g_f, b_f)

    @classmethod
    def from_rgb(cls, rgb: ColorRGB) -> ColorHSV:
        """Constructs ColorHSV from ColorRGB."""
        r_f, g_f, b_f = rgb.to_normalized()
        h_f, s_f, v_f = colorsys.rgb_to_hsv(r_f, g_f, b_f)
        return cls(h=h_f * 360.0, s=s_f, v=v_f)

    def to_tuple(self) -> Tuple[float, float, float]:
        """Returns tuple (h, s, v)."""
        return (self.h, self.s, self.v)
