"""Generates the official project icons (PNG and multi-size ICO).

Follows SOLID & DRY principles:
- Single Responsibility: Responsible solely for synthesizing and saving project branding icons.
- Encapsulation: Mathematical geometry and color palettes cleanly defined.
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFilter


class ProjectIconGenerator:
    """Generates official floral/RGB icons for OpenRGB Flowers Blooming."""

    DEFAULT_SIZES: List[Tuple[int, int]] = [
        (16, 16),
        (32, 32),
        (48, 48),
        (64, 64),
        (128, 128),
        (256, 256),
    ]

    PETAL_COLORS = [
        (255, 42, 109, 250),   # 0: Radiant Pink/Crimson
        (255, 115, 0, 250),    # 1: Tangerine Orange
        (255, 210, 0, 250),    # 2: Amber Yellow
        (16, 215, 90, 250),    # 3: Spring Neon Green
        (0, 225, 255, 250),    # 4: Cyan Blue
        (59, 130, 246, 250),   # 5: Azure
        (147, 51, 234, 250),   # 6: Violet Purple
        (236, 72, 153, 250),   # 7: Orchid Fuchsia
    ]

    @classmethod
    def generate_master_image(cls, canvas_size: int = 1024) -> Image.Image:
        """Renders high-resolution master image with anti-aliasing and soft ambient glow."""
        img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
        cx, cy = canvas_size / 2.0, canvas_size / 2.0
        num_petals = len(cls.PETAL_COLORS)
        petal_len = canvas_size * 0.36
        petal_width = canvas_size * 0.18
        dist = canvas_size * 0.18

        # 1. Soft RGB ambient glow behind petals
        glow = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
        draw_glow = ImageDraw.Draw(glow)
        for i in range(num_petals):
            angle = i * (2.0 * math.pi / num_petals) - (math.pi / 2.0)
            px = cx + dist * math.cos(angle)
            py = cy + dist * math.sin(angle)
            draw_glow.ellipse(
                [px - petal_width * 1.1, py - petal_len * 0.7, px + petal_width * 1.1, py + petal_len * 0.7],
                fill=(cls.PETAL_COLORS[i][0], cls.PETAL_COLORS[i][1], cls.PETAL_COLORS[i][2], 80),
            )
        glow = glow.filter(ImageFilter.GaussianBlur(radius=25))
        img.paste(glow, (0, 0), glow)

        # 2. Main Outer Petals with smooth highlights
        for i in range(num_petals):
            angle_deg = i * (360.0 / num_petals)
            petal = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
            pdraw = ImageDraw.Draw(petal)

            pcx = cx
            pcy = cy - dist - (petal_len * 0.45)
            bbox = [pcx - petal_width * 0.85, pcy - petal_len * 0.55, pcx + petal_width * 0.85, pcy + petal_len * 0.55]
            pdraw.ellipse(bbox, fill=cls.PETAL_COLORS[i])

            inner_bbox = [pcx - petal_width * 0.5, pcy - petal_len * 0.35, pcx + petal_width * 0.5, pcy + petal_len * 0.35]
            highlight_color = (
                min(255, cls.PETAL_COLORS[i][0] + 60),
                min(255, cls.PETAL_COLORS[i][1] + 60),
                min(255, cls.PETAL_COLORS[i][2] + 60),
                220,
            )
            pdraw.ellipse(inner_bbox, fill=highlight_color)

            rotated = petal.rotate(-angle_deg, resample=Image.Resampling.BICUBIC, center=(cx, cy))
            img.alpha_composite(rotated)

        # 3. Inner Petals for depth & vibrancy
        for i in range(num_petals):
            angle_deg = i * (360.0 / num_petals) + (180.0 / num_petals)
            petal = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
            pdraw = ImageDraw.Draw(petal)
            pcx = cx
            pcy = cy - dist * 0.7 - (petal_len * 0.25)
            bbox = [pcx - petal_width * 0.55, pcy - petal_len * 0.35, pcx + petal_width * 0.55, pcy + petal_len * 0.35]
            color = cls.PETAL_COLORS[(i + 4) % num_petals]
            pdraw.ellipse(bbox, fill=(color[0], color[1], color[2], 210))
            rotated = petal.rotate(-angle_deg, resample=Image.Resampling.BICUBIC, center=(cx, cy))
            img.alpha_composite(rotated)

        # 4. Radiant pistil core
        draw = ImageDraw.Draw(img)
        r_core_outer = canvas_size * 0.14
        draw.ellipse([cx - r_core_outer, cy - r_core_outer, cx + r_core_outer, cy + r_core_outer], fill=(255, 230, 100, 255))
        r_core_inner = canvas_size * 0.09
        draw.ellipse([cx - r_core_inner, cy - r_core_inner, cx + r_core_inner, cy + r_core_inner], fill=(255, 255, 255, 255))

        return img

    @classmethod
    def generate_all(cls, output_dir: Path) -> Tuple[Path, Path]:
        """Generates both icon.png (256x256) and icon.ico (16, 32, 48, 64, 128, 256)."""
        output_dir.mkdir(parents=True, exist_ok=True)
        master = cls.generate_master_image(canvas_size=1024)

        # 256x256 PNG
        png_img = master.resize((256, 256), Image.Resampling.LANCZOS)
        png_path = output_dir / "icon.png"
        png_img.save(png_path, format="PNG")

        # Multi-resolution ICO
        ico_frames = [master.resize(size, Image.Resampling.LANCZOS) for size in cls.DEFAULT_SIZES]
        ico_path = output_dir / "icon.ico"
        ico_frames[-1].save(ico_path, format="ICO", sizes=cls.DEFAULT_SIZES, append_images=ico_frames[:-1])

        return png_path, ico_path


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets"
    png, ico = ProjectIconGenerator.generate_all(out)
    print(f"Generated icons in {out}: {png.name}, {ico.name}")
