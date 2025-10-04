import json
import os
from typing import Any, Dict, Optional


class BaseJsonRepository:
    """Base repository for JSON file operations."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> Optional[Dict[str, Any]]:
        """Load data from the JSON file."""
        if not os.path.exists(self.file_path):
            return None

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
            raise IOError(f"Error loading JSON from {self.file_path}: {e}")

    def save(self, data: Dict[str, Any]) -> bool:
        """Save data to the JSON file."""
        try:
            self._ensure_directory()

            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True
        except (IOError, OSError, PermissionError) as e:
            raise IOError(f"Error saving JSON to {self.file_path}: {e}")

    def exists(self) -> bool:
        """Check if the JSON file exists."""
        return os.path.exists(self.file_path)

    def _ensure_directory(self) -> None:
        """Ensure the directory for the file path exists."""
        directory = os.path.dirname(self.file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
