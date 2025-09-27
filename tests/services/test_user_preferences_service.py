import json
import os
from datetime import datetime
import pytest
from app.services.user_preferences_service import UserPreferencesService


@pytest.fixture
def prefs_service(tmp_path):
    """Provide a fresh service instance with a temp file for testing."""
    test_file = tmp_path / "prefs.json"
    return UserPreferencesService(preferences_file=test_file)


def test_creates_default_file(prefs_service):
    prefs = prefs_service.load_preferences()
    assert "last_accessed_course" in prefs
    assert "video_playback_speed" in prefs
    assert "audio_playback_speed" in prefs
    assert prefs_service.preferences_file.exists()


def test_load_and_save_preferences(prefs_service):
    prefs = prefs_service.load_preferences()
    prefs["video_playback_speed"] = 1.5
    prefs_service.save_preferences(prefs)

    with open(prefs_service.preferences_file) as f:
        reloaded = json.load(f)

    assert reloaded["video_playback_speed"] == 1.5


def test_load_preferences_with_invalid_json(prefs_service):
    # Create a corrupted file
    with open(prefs_service.preferences_file, "w") as f:
        f.write("{ invalid json ")

    prefs = prefs_service.load_preferences()
    assert "last_accessed_course" in prefs
    assert prefs["video_playback_speed"] == 1.0


def test_update_last_accessed_course_and_get(prefs_service):
    prefs_service.update_last_accessed_course("course123", "Python Basics")
    last_course = prefs_service.get_last_accessed_course()

    assert last_course is not None
    assert last_course["course_id"] == "course123"
    assert last_course["name"] == "Python Basics"
    # Check that last_accessed_at is a valid ISO string
    datetime.fromisoformat(last_course["last_accessed_at"])


def test_update_playback_speeds_and_get(prefs_service):
    prefs_service.update_playback_speed(video_speed=1.25, audio_speed=1.75)
    speeds = prefs_service.get_playback_speeds()

    assert speeds["video"] == 1.25
    assert speeds["audio"] == 1.75


def test_get_last_accessed_course_with_old_format(prefs_service, tmp_path):
    # Write old format with "path"
    fake_path = tmp_path / "dummy_course"
    fake_path.mkdir()
    (fake_path / "lesson.txt").write_text("dummy")

    old_format = {
        "last_accessed_course": {
            "path": str(fake_path),
            "name": "Legacy Course",
            "last_accessed_at": "2024-01-01T00:00:00"
        },
        "video_playback_speed": 1.0,
        "audio_playback_speed": 1.0
    }
    with open(prefs_service.preferences_file, "w") as f:
        json.dump(old_format, f)

    course = prefs_service.get_last_accessed_course()
    assert course["name"] == "Legacy Course"
    assert os.path.exists(course["path"])
