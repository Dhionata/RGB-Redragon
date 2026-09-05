"""Interface for hardware frame transmission."""
from abc import ABC, abstractmethod
from openrgb_flowers.core.models.render_frame import RenderFrame


class IFrameTransmitter(ABC):
    """Contract for transmitting rendered lighting frames to hardware or mock target."""

    @abstractmethod
    def connect(self) -> bool:
        """Establishes connection to the target device/SDK. Returns True if successful."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Closes connection gracefully."""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Checks if connection is actively established."""
        pass

    @abstractmethod
    def send_frame(self, frame: RenderFrame) -> bool:
        """Transmits a rendered frame to the device. Returns True if sent successfully."""
        pass
