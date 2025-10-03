import json
import os
from datetime import datetime
from typing import Dict, Optional, Any
from app.models.course_model import NodeType


class RegistryService:
    """Unified service to manage the registry for both directories and courses with their metadata and node types."""

    def __init__(self, registry_path: str = "app/data/registry.json"):
        self.registry_path = registry_path
        self._ensure_registry_exists()

    def _ensure_registry_exists(self) -> None:
        """Ensure the registry file exists with proper structure."""
        if not os.path.exists(self.registry_path):
            os.makedirs(os.path.dirname(self.registry_path), exist_ok=True)
            self._create_empty_registry()

    def _create_empty_registry(self) -> None:
        """Create an empty registry file."""
        registry_data = {
            "directories": {},
            "courses": {},
            "metadata": {
                "version": "1.0",
                "last_updated": None,
                "description": "Unified registry for directories and courses with their metadata and node types"
            }
        }
        self._save_registry(registry_data)

    def _load_registry(self) -> Dict[str, Any]:
        """Load the registry from file."""
        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._create_empty_registry()
            return self._load_registry()

    def _save_registry(self, registry_data: Dict[str, Any]) -> None:
        """Save the registry to file."""
        registry_data["metadata"]["last_updated"] = datetime.now().isoformat()
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(registry_data, f, indent=2, ensure_ascii=False)

    def _get_registry_section(self, node_type: NodeType) -> str:
        """Get the appropriate registry section based on node type."""
        if node_type == NodeType.DIRECTORY:
            return "directories"
        elif node_type in [NodeType.COURSE, NodeType.MODULE, NodeType.LESSON]:
            return "courses"
        else:
            # TODO: Better handle unknown types
            return "courses"  # Default to courses for unknown types

    def is_registered(self, title: str, path: str, node_type: NodeType) -> bool:
        """Check if an item is already registered."""
        registry_data = self._load_registry()
        section = self._get_registry_section(node_type)
        registry_key = f"{title}|{path}"
        return registry_key in registry_data[section]

    def get_registry_entry(self, title: str, path: str, node_type: NodeType) -> Optional[Dict[str, Any]]:
        """Get registry entry for an item."""
        registry_data = self._load_registry()
        section = self._get_registry_section(node_type)
        registry_key = f"{title}|{path}"
        return registry_data[section].get(registry_key)

    def register_item(self, title: str, path: str, node_type: NodeType) -> Dict[str, Any]:
        """Register a new item in the registry."""
        registry_data = self._load_registry()
        section = self._get_registry_section(node_type)
        registry_key = f"{title}|{path}"

        entry = {
            "title": title,
            "path": path,
            "node_type": node_type.value,
            "registered_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat()
        }

        registry_data[section][registry_key] = entry
        self._save_registry(registry_data)

        return entry

    def update_last_accessed(self, title: str, path: str, node_type: NodeType) -> None:
        """Update the last accessed timestamp for an item."""
        registry_data = self._load_registry()
        section = self._get_registry_section(node_type)
        registry_key = f"{title}|{path}"

        if registry_key in registry_data[section]:
            registry_data[section][registry_key]["last_accessed"] = datetime.now().isoformat()
            self._save_registry(registry_data)

    def get_all_directories(self) -> Dict[str, Any]:
        """Get all directory registry entries."""
        registry_data = self._load_registry()
        return registry_data["directories"]

    def get_all_courses(self) -> Dict[str, Any]:
        """Get all course registry entries."""
        registry_data = self._load_registry()
        return registry_data["courses"]

    def get_directory_by_id(self, directory_id: str) -> Optional[Dict[str, Any]]:
        """Get a directory entry by its ID (directory name)."""
        directories = self.get_all_directories()
        for key, entry in directories.items():
            # Extract directory name from path
            directory_name = os.path.basename(entry["path"])
            if directory_name == directory_id:
                return entry
        return None

    def get_course_by_id(self, course_id: str) -> Optional[Dict[str, Any]]:
        """Get a course entry by its ID (course name)."""
        courses = self.get_all_courses()
        for key, entry in courses.items():
            # Extract course name from path
            course_name = os.path.basename(entry["path"])
            if course_name == course_id:
                return entry
        return None

    def cleanup_old_entries(self, days_threshold: int = 30) -> int:
        """Remove entries that haven't been accessed for a specified number of days."""
        registry_data = self._load_registry()
        current_time = datetime.now()
        removed_count = 0

        # Clean both directories and courses
        for section in ["directories", "courses"]:
            entries_to_remove = []
            for key, entry in registry_data[section].items():
                last_accessed = datetime.fromisoformat(entry["last_accessed"])
                days_since_access = (current_time - last_accessed).days

                if days_since_access > days_threshold:
                    entries_to_remove.append(key)

            for key in entries_to_remove:
                del registry_data[section][key]
                removed_count += 1

        if removed_count > 0:
            self._save_registry(registry_data)

        return removed_count

    def clear_all_entries(self) -> None:
        """Clear all registry entries."""
        self._create_empty_registry()

    #TODO: Avoid having path hardcoded in multiple places
    def migrate_from_directory_registry(self, old_registry_path: str = "app/data/directory_registry.json") -> None:
        """Migrate data from the old directory registry to the unified registry."""
        if not os.path.exists(old_registry_path):
            return

        try:
            with open(old_registry_path, 'r', encoding='utf-8') as f:
                old_registry = json.load(f)

            registry_data = self._load_registry()

            # Migrate old entries
            for key, entry in old_registry.get("registry", {}).items():
                node_type = NodeType(entry["node_type"])
                section = self._get_registry_section(node_type)
                registry_data[section][key] = entry

            self._save_registry(registry_data)
            print(f"Migrated {len(old_registry.get('registry', {}))} entries from directory registry")

        except Exception as e:
            print(f"Error migrating directory registry: {e}")