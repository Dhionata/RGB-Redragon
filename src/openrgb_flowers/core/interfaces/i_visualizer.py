"""Interface for real-time visualizers."""
from abc import ABC, abstractmethod
from openrgb_flowers.core.models.render_frame import RenderFrame
from openrgb_flowers.core.interfaces.i_layout_provider import ILayoutProvider


class IVisualizer(ABC):
    """Contract for displaying the rendered effect in real time."""

    @abstractmethod
    def render(self, frame: RenderFrame, layout: ILayoutProvider, active_blooms: int, fps: float) -> None:
        """Renders visual representation of current frame."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Closes visualizer and restores terminal/display."""
        pass
