"""High-performance floral blooming simulation engine."""
from __future__ import annotations
import math
import random
from typing import List, Optional
import numpy as np

from openrgb_flowers.core.interfaces.i_effect_engine import IEffectEngine
from openrgb_flowers.core.interfaces.i_layout_provider import ILayoutProvider
from openrgb_flowers.core.interfaces.i_blend_strategy import IBlendStrategy
from openrgb_flowers.core.interfaces.i_color_palette import IColorPalette
from openrgb_flowers.core.models.effect_config import EffectConfig
from openrgb_flowers.core.models.render_frame import RenderFrame
from openrgb_flowers.effects.flower_instance import FlowerInstance
from openrgb_flowers.effects.palettes.palette_registry import PaletteRegistry
from openrgb_flowers.effects.blending.organic_weighted_blend import OrganicWeightedBlend
from openrgb_flowers.effects.blending.screen_blend import ScreenBlend
from openrgb_flowers.effects.blending.additive_blend import AdditiveBlend
from openrgb_flowers.math.fast_color import FastColorMath
from openrgb_flowers.math.spatial_grid import SpatialGrid


class BloomingEngine(IEffectEngine):
    """Vectorized floral engine orchestrating concurrent blooming flowers."""

    def __init__(
        self,
        config: EffectConfig,
        layout_provider: ILayoutProvider,
        blend_strategy: Optional[IBlendStrategy] = None,
        palette: Optional[IColorPalette] = None,
        spatial_grid: Optional[SpatialGrid] = None,
    ) -> None:
        self._config = config
        self._layout = layout_provider
        self._palette = palette or PaletteRegistry.get(config.palette_name)
        self._blend_strategy = blend_strategy or self._resolve_blend_strategy(config.blend_mode)
        self._spatial_grid = spatial_grid or SpatialGrid()

        # Cache layout coordinates as float arrays
        self._x_coords, self._y_coords = self._layout.get_coordinate_arrays()
        self._led_count = self._layout.get_key_count()

        # Simulation state
        self._flowers: List[FlowerInstance] = []
        self._frame_count = 0
        self._sim_time = 0.0
        self._spawn_accumulator = 0.0

        # Precompute background base array
        self._bg_base = np.tile(
            np.array(self._config.background_color.to_tuple(), dtype=np.float32),
            (self._led_count, 1),
        )

    @staticmethod
    def _resolve_blend_strategy(mode_name: str) -> IBlendStrategy:
        name = mode_name.lower().strip()
        if name == "screen":
            return ScreenBlend()
        elif name == "additive":
            return AdditiveBlend()
        return OrganicWeightedBlend()

    def get_config(self) -> EffectConfig:
        return self._config

    def get_active_flower_count(self) -> int:
        return len(self._flowers)

    def update_layout(self, layout_provider: ILayoutProvider) -> None:
        """Updates the physical layout provider and recomputes coordinate buffers."""
        self._layout = layout_provider
        self._x_coords, self._y_coords = self._layout.get_coordinate_arrays()
        self._led_count = self._layout.get_key_count()
        self._bg_base = np.tile(
            np.array(self._config.background_color.to_tuple(), dtype=np.float32),
            (self._led_count, 1),
        )

    def reset(self) -> None:
        self._flowers.clear()
        self._frame_count = 0
        self._sim_time = 0.0
        self._spawn_accumulator = 0.0

    def _should_spawn_flower(self, dt: float) -> bool:
        """Determines if a new flower blossom should spawn."""
        if len(self._flowers) >= self._config.max_flowers:
            return False

        # If field is completely empty, spawn immediately
        if not self._flowers:
            return True

        self._spawn_accumulator += dt * self._config.spawn_rate * self._config.speed
        if self._spawn_accumulator >= 1.0:
            self._spawn_accumulator -= 1.0
            return True
        return False

    def _generate_flower_position(self) -> tuple[float, float]:
        """Generates organic coordinates with natural spacing."""
        best_x = random.uniform(0.08, 0.92)
        best_y = random.uniform(0.12, 0.88)

        # Attempt to avoid tight clustering if active blooms exist
        if self._flowers:
            max_min_dist = -1.0
            for _ in range(5):
                cand_x = random.uniform(0.08, 0.92)
                cand_y = random.uniform(0.12, 0.88)
                min_d = min(
                    math.hypot(cand_x - f.get_center()[0], cand_y - f.get_center()[1])
                    for f in self._flowers
                )
                if min_d > max_min_dist:
                    max_min_dist = min_d
                    best_x, best_y = cand_x, cand_y

        return best_x, best_y

    def _spawn_flower(self) -> None:
        """Spawns a new organic blooming flower instance."""
        cx, cy = self._generate_flower_position()
        petal_count = random.choice(self._config.petal_options)
        rotation = random.uniform(0.0, 2.0 * math.pi)
        lifespan = random.uniform(2.8, 4.4) / self._config.speed
        max_radius = random.uniform(0.35, 0.52)
        petal_depth = random.uniform(0.18, 0.28)

        # For rainbow palette, generate a fresh randomized harmonious chromatic offset
        if self._config.palette_name.lower() == "rainbow":
            from openrgb_flowers.effects.palettes.rainbow_palette import RainbowPalette
            flower_palette = RainbowPalette(base_hue=random.uniform(0.0, 360.0))
        else:
            flower_palette = self._palette

        flower = FlowerInstance(
            center_x=cx,
            center_y=cy,
            palette=flower_palette,
            petal_count=petal_count,
            max_radius=max_radius,
            lifespan=lifespan,
            rotation=rotation,
            petal_depth=petal_depth,
            spatial_grid=self._spatial_grid,
        )
        self._flowers.append(flower)

    def _compute_ambient_background(self) -> np.ndarray:
        """Calculates subtle gentle meadow ambient wave under keys."""
        if not self._config.ambient_pulse:
            return self._bg_base.copy()

        # Slow breathing botanical breeze across keys
        phase = self._sim_time * 0.8
        wave = (np.sin(self._x_coords * 3.0 + phase) * 0.5 + 0.5)[:, np.newaxis]
        breeze_tint = np.array([6.0, 14.0, 10.0], dtype=np.float32)
        return self._bg_base + breeze_tint * (wave * 0.5)

    def tick(self, dt: float) -> RenderFrame:
        """Advances simulation by dt seconds and renders the next frame."""
        self._sim_time += dt
        self._frame_count += 1

        # 1. Update existing blooms & remove expired
        self._flowers = [f for f in self._flowers if f.update(dt * self._config.speed)]

        # 2. Spawn new blooms if needed
        if self._should_spawn_flower(dt):
            self._spawn_flower()

        # 3. Ambient background
        base_colors = self._compute_ambient_background()

        # 4. Evaluate each flower layer
        layer_colors: List[np.ndarray] = []
        layer_intensities: List[np.ndarray] = []

        for flower in self._flowers:
            intensities, colors = flower.evaluate(self._x_coords, self._y_coords)
            layer_colors.append(colors)
            layer_intensities.append(intensities)

        # 5. Blend layers
        blended = self._blend_strategy.blend_layers(base_colors, layer_colors, layer_intensities)

        # 6. Apply brightness and gamma correction
        final_uint8 = FastColorMath.apply_brightness_gamma(
            blended.astype(np.float32),
            brightness=self._config.brightness,
            gamma=self._config.gamma,
        )

        return RenderFrame(
            timestamp=self._sim_time,
            frame_index=self._frame_count,
            colors=final_uint8,
            led_count=self._led_count,
        )
