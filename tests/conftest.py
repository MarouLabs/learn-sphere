import pytest
from app.services.user_preferences_service import UserPreferencesService


@pytest.fixture
def prefs_service(tmp_path):
    """
    Provides a UserPreferencesService instance with a temporary preferences file.
    Prevents tests from modifying the real preferences in /data.
    """
    test_file = tmp_path / "prefs.json"
    return UserPreferencesService(preferences_file=test_file)
