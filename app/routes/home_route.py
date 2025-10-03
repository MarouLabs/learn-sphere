from flask import Blueprint, render_template
from config import Config
from app.services.directory_service import DirectoryService
from app.services.user_preferences_service import UserPreferencesService

bp = Blueprint("home", __name__)


@bp.route("/")
def index():
    """Root/home page showing courses and directories in the root directory."""
    # Get courses from the configured directory
    courses = DirectoryService.scan_directory(Config.COURSES_ROOT_DIRECTORY_ABS_PATH)

    # Get user theme
    preferences_service = UserPreferencesService()
    user_theme = preferences_service.get_theme()

    return render_template("home.html", courses=courses, user_theme=user_theme)
