"""Vectorized real-time random color blend engine where all keys are illuminated simultaneously."""
from __future__ import annotations
from typing import Any, Optional
import numpy as np

from openrgb_flowers.core.interfaces.i_effect_engine import IEffectEngine
from openrgb_flowers.core.interfaces.i_layout_provider import ILayoutProvider
from openrgb_flowers.core.interfaces.i_color_palette import IColorPalette
from openrgb_flowers.core.models.effect_config import EffectConfig
from openrgb_flowers.core.models.render_frame import RenderFrame
from openrgb_flowers.effects.palettes.palette_registry import PaletteRegistry
from openrgb_flowers.math.fast_color import FastColorMath


class RandomBlendEngine(IEffectEngine):
    """High-performance engine where 100% of keys remain brightly illuminated while smoothly
    and independently transitioning through randomized, organic mixed colors.

    Uses vectorized NumPy pre-allocated buffers with smoothstep (Hermite) cubic interpolation
    for silky color transitions and zero allocations per frame.
    """

    def __init__(
        self,
        config: EffectConfig,
        layout_provider: ILayoutProvider,
        palette: Optional[IColorPalette] = None,
    ) -> None:
        self._config = config
        self._layout = layout_provider
        self._palette = palette or PaletteRegistry.get(config.palette_name)

        self._led_count = self._layout.get_key_count()
        self._frame_count = 0
        self._sim_time = 0.0

        # Pre-allocate contiguous NumPy state arrays (zero memory allocations in tick)
        self._current_rgb = np.zeros((self._led_count, 3), dtype=np.float32)
        self._target_rgb = np.zeros((self._led_count, 3), dtype=np.float32)
        self._progress = np.zeros(self._led_count, dtype=np.float32)
        self._transition_speeds = np.zeros(self._led_count, dtype=np.float32)

        # Output buffer for uint8 frame
        self._output_colors = np.zeros((self._led_count, 3), dtype=np.uint8)

        # Initialize per-key random states
        self._initialize_keys()

    def _sample_palette_colors(self, count: int) -> np.ndarray:
        """Samples random colors from the active palette."""
        random_positions = np.random.uniform(0.0, 1.0, size=count)
        colors = np.zeros((count, 3), dtype=np.float32)
        for i, pos in enumerate(random_positions):
            c = self._palette.sample(float(pos))
            colors[i, 0] = c.r
            colors[i, 1] = c.g
            colors[i, 2] = c.b
        return colors

    def _initialize_keys(self) -> None:
        """Seeds initial colors, targets, and asynchronous transition phases."""
        self._current_rgb[:] = self._sample_palette_colors(self._led_count)
        self._target_rgb[:] = self._sample_palette_colors(self._led_count)

        # Stagger initial progress uniformly across [0.0, 1.0] so keys blend out of phase
        self._progress[:] = np.random.uniform(0.0, 1.0, size=self._led_count).astype(np.float32)

        # Speed variance: each key has a unique transition rate (0.6x to 2.2x base speed)
        self._transition_speeds[:] = np.random.uniform(0.6, 2.2, size=self._led_count).astype(np.float32)

    def tick(self, dt: float) -> RenderFrame:
        """Advances the color mixing simulation and renders the next frame."""
        self._sim_time += dt
        self._frame_count += 1

        # Advance progress for each key based on its individual speed and global multiplier
        speed_mult = max(0.05, float(self._config.speed))
        self._progress += dt * self._transition_speeds * speed_mult

        # Identify keys that completed their transition
        completed_mask = self._progress >= 1.0
        num_completed = int(np.count_nonzero(completed_mask))

        if num_completed > 0:
            # Set current to target for completed keys
            self._current_rgb[completed_mask] = self._target_rgb[completed_mask]
            # Wrap progress
            self._progress[completed_mask] = np.maximum(0.0, self._progress[completed_mask] - 1.0)
            # Pick new targets from palette
            self._target_rgb[completed_mask] = self._sample_palette_colors(num_completed)
            # Assign new random speed jitter
            self._transition_speeds[completed_mask] = np.random.uniform(
                0.6, 2.2, size=num_completed
            ).astype(np.float32)

        # Smoothstep interpolation: 3t^2 - 2t^3 gives zero acceleration at endpoints (silky smooth)
        t = np.clip(self._progress, 0.0, 1.0)
        smooth_t = (t * t * (3.0 - 2.0 * t))[:, np.newaxis]

        # Vectorized color interpolation
        blended = self._current_rgb + (self._target_rgb - self._current_rgb) * smooth_t

        # Apply saturation, brightness, and gamma correction
        final_uint8 = FastColorMath.apply_brightness_gamma(
            blended,
            brightness=self._config.brightness,
            gamma=self._config.gamma,
            saturation=self._config.saturation,
        )
        self._output_colors[:] = final_uint8

        return RenderFrame(
            timestamp=self._sim_time,
            frame_index=self._frame_count,
            colors=self._output_colors.copy(),
            led_count=self._led_count,
        )

    def update_config(self, config: EffectConfig) -> None:
        """Updates active runtime parameters on the fly without resetting transition states."""
        palette_changed = config.palette_name != self._config.palette_name
        self._config = config
        if palette_changed:
            self._palette = PaletteRegistry.get(config.palette_name)
            # Reseed targets so keys smoothly blend towards the new palette
            self._target_rgb[:] = self._sample_palette_colors(self._led_count)

    def reset(self) -> None:
        """Resets engine state and reseeds per-key color transitions."""
        self._sim_time = 0.0
        self._frame_count = 0
        self._initialize_keys()

    def get_config(self) -> EffectConfig:
        """Returns the active configuration."""
        return self._config

    def get_active_flower_count(self) -> int:
        """In this effect, 100% of keys are constantly active and illuminated."""
        return self._led_count

    def update_layout(self, layout_provider: ILayoutProvider) -> None:
        """Updates layout provider and reallocates buffers for new LED count."""
        self._layout = layout_provider
        self._led_count = layout_provider.get_key_count()

        self._current_rgb = np.zeros((self._led_count, 3), dtype=np.float32)
        self._target_rgb = np.zeros((self._led_count, 3), dtype=np.float32)
        self._progress = np.zeros(self._led_count, dtype=np.float32)
        self._transition_speeds = np.zeros(self._led_count, dtype=np.float32)
        self._output_colors = np.zeros((self._led_count, 3), dtype=np.uint8)

        self._initialize_keys()
