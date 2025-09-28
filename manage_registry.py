#!/usr/bin/env python3
"""
Directory Registry Management Script

This script provides utilities to manage the directory registry.
"""

import sys
import json
from config import Config
from app.services.directory_registry_service import DirectoryRegistryService
from app.services.directory_service import DirectoryService


def show_registry():
    """Display all entries in the registry."""
    registry_service = DirectoryRegistryService()
    entries = registry_service.get_all_entries()
    
    if not entries:
        print("Registry is empty.")
        return
    
    print(f"Registry contains {len(entries)} entries:")
    print("-" * 80)
    
    for key, entry in entries.items():
        print(f"Title: {entry['title']}")
        print(f"Path: {entry['path']}")
        print(f"Type: {entry['node_type']}")
        print(f"Color: {entry['color']}")
        print(f"Registered: {entry['registered_at']}")
        print(f"Last Accessed: {entry['last_accessed']}")
        print("-" * 80)


def cleanup_registry(days=30):
    """Clean up old registry entries."""
    registry_service = DirectoryRegistryService()
    removed_count = registry_service.cleanup_old_entries(days)
    
    if removed_count > 0:
        print(f"Removed {removed_count} entries older than {days} days.")
    else:
        print(f"No entries older than {days} days found.")


def clear_registry():
    """Clear all entries from the registry."""
    registry_service = DirectoryRegistryService()
    registry_service.clear_all_entries()
    print("Registry cleared successfully.")


def force_analyze():
    """Force analysis of the root directory, ignoring registry cache."""
    print(f"Force analyzing root directory: {Config.COURSES_ROOT_DIRECTORY_ABS_PATH}")
    courses = DirectoryService.force_analyze_directory(Config.COURSES_ROOT_DIRECTORY_ABS_PATH)
    print(f"Analysis complete. Found {len(courses)} courses/directories.")
    
    for course in courses:
        print(f"  - {course.title} ({course.node_type.value})")


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manage_registry.py show          - Show all registry entries")
        print("  python manage_registry.py cleanup [days] - Remove entries older than N days (default: 30)")
        print("  python manage_registry.py clear         - Clear all registry entries")
        print("  python manage_registry.py force-analyze - Force analysis of root directory (ignore cache)")
        return
    
    command = sys.argv[1].lower()
    
    if command == "show":
        show_registry()
    elif command == "cleanup":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        cleanup_registry(days)
    elif command == "clear":
        confirm = input("Are you sure you want to clear all registry entries? (y/N): ")
        if confirm.lower() == 'y':
            clear_registry()
        else:
            print("Operation cancelled.")
    elif command == "force-analyze":
        force_analyze()
    else:
        print(f"Unknown command: {command}")
        print("Use 'show', 'cleanup', 'clear', or 'force-analyze'")


if __name__ == "__main__":
    main()
