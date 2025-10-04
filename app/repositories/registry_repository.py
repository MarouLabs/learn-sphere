from pathlib import Path
from .base_json_repository import BaseJsonRepository


class RegistryRepository(BaseJsonRepository):
    """Repository for the directory registry stored in registry.json."""

    DEFAULT_REGISTRY_PATH = "app/data/registry.json"

    def __init__(self, registry_path: str = None):
        if registry_path is None:
            registry_path = self.DEFAULT_REGISTRY_PATH
        super().__init__(registry_path)
