import json
import os
from datetime import datetime
from typing import Dict, Optional, Any
from app.models.course_model import NodeType
from app.services.color_service import ColorService


class DirectoryRegistryService:
    """Service to manage the directory registry for courses, modules, and directories including color persistence."""
    
    def __init__(self, registry_path: str = "app/data/directory_registry.json"):
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
            "registry": {},
            "metadata": {
                "version": "1.0",
                "last_updated": None,
                "description": "Registry for course directories with their metadata, node types, and colors"
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
    
    def is_registered(self, title: str, path: str) -> bool:
        """Check if an item is already registered."""
        registry_data = self._load_registry()
        registry_key = f"{title}|{path}"
        return registry_key in registry_data["registry"]
    
    def get_registry_entry(self, title: str, path: str) -> Optional[Dict[str, Any]]:
        """Get registry entry for an item."""
        registry_data = self._load_registry()
        registry_key = f"{title}|{path}"
        return registry_data["registry"].get(registry_key)
    
    def register_item(self, title: str, path: str, node_type: NodeType) -> Dict[str, Any]:
        """Register a new item in the registry with color from ColorService."""
        registry_data = self._load_registry()
        registry_key = f"{title}|{path}"
        
        # Get color from ColorService
        color = ColorService.generate_random_color(title)
        
        entry = {
            "title": title,
            "path": path,
            "node_type": node_type.value,
            "color": color,
            "registered_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat()
        }
        
        registry_data["registry"][registry_key] = entry
        self._save_registry(registry_data)
        
        return entry
    
    def update_last_accessed(self, title: str, path: str) -> None:
        """Update the last accessed timestamp for an item."""
        registry_data = self._load_registry()
        registry_key = f"{title}|{path}"
        
        if registry_key in registry_data["registry"]:
            registry_data["registry"][registry_key]["last_accessed"] = datetime.now().isoformat()
            self._save_registry(registry_data)
    
    def get_color(self, title: str, path: str, node_type: NodeType) -> str:
        """Get color for an item, registering it if not already registered."""
        entry = self.get_registry_entry(title, path)
        
        if entry:
            # Update last accessed and return existing color
            self.update_last_accessed(title, path)
            return entry["color"]
        else:
            # Register new item (which gets color from ColorService) and return its color
            entry = self.register_item(title, path, node_type)
            return entry["color"]
    
    def get_all_entries(self) -> Dict[str, Any]:
        """Get all registry entries."""
        registry_data = self._load_registry()
        return registry_data["registry"]
    
    def cleanup_old_entries(self, days_threshold: int = 30) -> int:
        """Remove entries that haven't been accessed for a specified number of days."""
        registry_data = self._load_registry()
        current_time = datetime.now()
        removed_count = 0
        
        entries_to_remove = []
        for key, entry in registry_data["registry"].items():
            last_accessed = datetime.fromisoformat(entry["last_accessed"])
            days_since_access = (current_time - last_accessed).days
            
            if days_since_access > days_threshold:
                entries_to_remove.append(key)
        
        for key in entries_to_remove:
            del registry_data["registry"][key]
            removed_count += 1
        
        if removed_count > 0:
            self._save_registry(registry_data)
        
        return removed_count
    
    def clear_all_entries(self) -> None:
        """Clear all registry entries."""
        self._create_empty_registry()