from pathlib import Path
from .base_json_repository import BaseJsonRepository


class UserPreferencesRepository(BaseJsonRepository):
    """Repository for user preferences stored in user_preferences.json."""

    DEFAULT_PREFERENCES_PATH = Path(__file__).parent.parent / "data" / "user_preferences.json"

    def __init__(self, preferences_file: Path = None):
        if preferences_file is None:
            preferences_file = self.DEFAULT_PREFERENCES_PATH
        super().__init__(str(preferences_file))
