"""Immutable 24-bit RGB Color Model with fast conversion and packing."""
from __future__ import annotations
from dataclasses import dataclass
import struct
from typing import Tuple


@dataclass(frozen=True, slots=True)
class ColorRGB:
    """Represents a 24-bit RGB color with values in [0, 255]."""

    r: int
    g: int
    b: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "r", max(0, min(255, int(self.r))))
        object.__setattr__(self, "g", max(0, min(255, int(self.g))))
        object.__setattr__(self, "b", max(0, min(255, int(self.b))))

    def to_tuple(self) -> Tuple[int, int, int]:
        """Returns integer tuple (r, g, b)."""
        return (self.r, self.g, self.b)

    def to_normalized(self) -> Tuple[float, float, float]:
        """Returns normalized float tuple in [0.0, 1.0]."""
        return (self.r / 255.0, self.g / 255.0, self.b / 255.0)

    def to_hex(self) -> str:
        """Returns hex color code '#RRGGBB'."""
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"

    def pack(self) -> bytes:
        """Packs into 3 bytes little-endian for fast network transmission."""
        return struct.pack("BBB", self.r, self.g, self.b)

    @classmethod
    def from_normalized(cls, r: float, g: float, b: float) -> ColorRGB:
        """Constructs ColorRGB from normalized floats in [0.0, 1.0]."""
        return cls(
            r=int(round(max(0.0, min(1.0, r)) * 255.0)),
            g=int(round(max(0.0, min(1.0, g)) * 255.0)),
            b=int(round(max(0.0, min(1.0, b)) * 255.0)),
        )

    @classmethod
    def from_hex(cls, hex_str: str) -> ColorRGB:
        """Constructs ColorRGB from hex string '#RRGGBB' or 'RRGGBB'."""
        clean = hex_str.lstrip("#")
        if len(clean) != 6:
            raise ValueError(f"Invalid hex color string: {hex_str}")
        r = int(clean[0:2], 16)
        g = int(clean[2:4], 16)
        b = int(clean[4:6], 16)
        return cls(r, g, b)

    def to_openrgb(self):
        """Converts to openrgb.utils.RGBColor if openrgb is installed."""
        try:
            from openrgb.utils import RGBColor
            return RGBColor(self.r, self.g, self.b)
        except ImportError:
            return (self.r, self.g, self.b)
