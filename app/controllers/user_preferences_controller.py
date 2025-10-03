from flask import Blueprint, request, jsonify
from app.services.user_preferences_service import UserPreferencesService

user_preferences_blueprint = Blueprint("user_preferences", __name__, url_prefix="/api/user-preferences")


@user_preferences_blueprint.route("/theme", methods=["GET"])
def get_theme():
    """Get the current theme preference."""
    try:
        preferences_service = UserPreferencesService()
        theme = preferences_service.get_theme()
        return jsonify({"success": True, "theme": theme})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@user_preferences_blueprint.route("/theme", methods=["POST"])
def update_theme():
    """Update the theme preference."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        theme = data.get("theme", "light")

        if theme not in ["light", "dark"]:
            return jsonify({"success": False, "error": "Invalid theme. Must be 'light' or 'dark'"}), 400

        preferences_service = UserPreferencesService()
        preferences_service.update_theme(theme)

        return jsonify({"success": True, "theme": theme})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@user_preferences_blueprint.route("/playback-speed", methods=["GET"])
def get_playback_speed():
    """Get the current playback speed preferences."""
    try:
        preferences_service = UserPreferencesService()
        speeds = preferences_service.get_playback_speeds()
        return jsonify({"success": True, "speeds": speeds})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@user_preferences_blueprint.route("/playback-speed", methods=["POST"])
def update_playback_speed():
    """Update playback speed preferences."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        video_speed = data.get("video_speed")
        audio_speed = data.get("audio_speed")

        if video_speed is not None and (video_speed < 0.25 or video_speed > 4.0):
            return jsonify({"success": False, "error": "Video speed must be between 0.25 and 4.0"}), 400

        if audio_speed is not None and (audio_speed < 0.25 or audio_speed > 4.0):
            return jsonify({"success": False, "error": "Audio speed must be between 0.25 and 4.0"}), 400

        preferences_service = UserPreferencesService()
        preferences_service.update_playback_speed(video_speed, audio_speed)

        speeds = preferences_service.get_playback_speeds()
        return jsonify({"success": True, "speeds": speeds})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@user_preferences_blueprint.route("/last-accessed-course", methods=["GET"])
def get_last_accessed_course():
    """Get the last accessed course information."""
    try:
        preferences_service = UserPreferencesService()
        last_course = preferences_service.get_last_accessed_course()
        return jsonify({"success": True, "last_course": last_course})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@user_preferences_blueprint.route("/", methods=["GET"])
def get_all_preferences():
    """Get all user preferences."""
    try:
        preferences_service = UserPreferencesService()
        preferences = preferences_service.load_preferences()
        return jsonify({"success": True, "preferences": preferences})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500