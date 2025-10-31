"""Base exporter for reports."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseExporter(ABC):
    """Base class for report exporters."""

    def __init__(self):
        self.output_dir = Path("uploads/reports")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    async def export(self, data: dict[str, Any], filename: str) -> tuple[bytes, Path]:
        """
        Export report data to file.

        Args:
            data: Report data
            filename: Output filename

        Returns:
            Tuple of (file_bytes, file_path)
        """
        raise NotImplementedError

    def _ensure_directory(self, subdirectory: str) -> Path:
        """
        Ensure a subdirectory exists.

        Args:
            subdirectory: Subdirectory name

        Returns:
            Path to subdirectory
        """
        dir_path = self.output_dir / subdirectory
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

