"""
User Preferences Service

Handles loading and saving user preferences including last accessed course
and playback speed settings.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from app.repositories.user_preferences_repository import UserPreferencesRepository


class UserPreferencesService:
    """Service for managing user preferences stored in JSON format."""

    def __init__(self, preferences_file: Path | None = None):
        self.repository = UserPreferencesRepository(preferences_file)

    def _ensure_preferences_file(self):
        """Ensure the preferences file exists with default values."""
        if not self.repository.exists():
            self._create_default_preferences()

    def _create_default_preferences(self):
        """Create the preferences file with default values."""
        default_prefs = {
            "last_accessed_course": {
                "course_id": None,
                "name": None,
                "last_accessed_at": None,
            },
            "video_playback_speed": 1.0,
            "audio_playback_speed": 1.0,
            "theme": "light",
        }

        self.repository.save(default_prefs)

    def load_preferences(self) -> Dict[str, Any]:
        """Load user preferences from the JSON file."""
        self._ensure_preferences_file()

        try:
            preferences = self.repository.load()

            if not preferences or not isinstance(preferences, dict):
                preferences = {}

            preferences.setdefault(
                "last_accessed_course",
                {"course_id": None, "name": None, "last_accessed_at": None},
            )
            preferences.setdefault("video_playback_speed", 1.0)
            preferences.setdefault("audio_playback_speed", 1.0)
            preferences.setdefault("theme", "light")

            return preferences

        except IOError as e:
            print(f"Error loading preferences: {e}. Using defaults.")
            self._create_default_preferences()
            return self.load_preferences()

    def save_preferences(self, preferences: Dict[str, Any]):
        """Save user preferences to the JSON file."""
        try:
            self._ensure_preferences_file()
            self.repository.save(preferences)
        except Exception as e:
            print(f"Error saving preferences: {e}")

    def update_last_accessed_course(self, course_id: str, course_name: str):
        """Update the last accessed course in preferences."""
        preferences = self.load_preferences()
        preferences["last_accessed_course"] = {
            "course_id": course_id,
            "name": course_name,
            "last_accessed_at": datetime.now().isoformat(),
        }
        self.save_preferences(preferences)

    def get_last_accessed_course(self) -> Optional[Dict[str, str]]:
        """Get the last accessed course information."""
        preferences = self.load_preferences()
        last_course = preferences.get("last_accessed_course")

        if (
            last_course
            and last_course.get("course_id")
            and last_course.get("name")
        ):
            return last_course

        # Fallback: old format with path
        if (
            last_course
            and last_course.get("path")
            and last_course.get("name")
            and os.path.exists(last_course["path"])
        ):
            return last_course

        return None

    def update_playback_speed(
        self, video_speed: Optional[float] = None, audio_speed: Optional[float] = None
    ):
        """Update playback speed preferences."""
        preferences = self.load_preferences()

        if video_speed is not None:
            preferences["video_playback_speed"] = video_speed

        if audio_speed is not None:
            preferences["audio_playback_speed"] = audio_speed

        self.save_preferences(preferences)

    def get_playback_speeds(self) -> Dict[str, float]:
        """Get the current playback speed preferences."""
        preferences = self.load_preferences()
        return {
            "video": preferences.get("video_playback_speed", 1.0),
            "audio": preferences.get("audio_playback_speed", 1.0),
        }

    def update_theme(self, theme: str):
        """Update the theme preference."""
        preferences = self.load_preferences()
        preferences["theme"] = theme
        self.save_preferences(preferences)

    def get_theme(self) -> str:
        """Get the current theme preference."""
        preferences = self.load_preferences()
        return preferences.get("theme", "light")