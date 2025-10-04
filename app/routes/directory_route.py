from flask import Blueprint, render_template, abort
from app.services.directory_service import DirectoryService
from app.services.registry_service import RegistryService
from app.services.user_preferences_service import UserPreferencesService
from app.models.course_model import NodeType

bp = Blueprint("directory", __name__)


@bp.route("/directory/<path:directory_id>")
def view(directory_id):
    """View a directory and its contents (courses and subdirectories)."""
    registry_service = RegistryService()

    directory_entry = registry_service.get_directory_by_id(directory_id)
    if not directory_entry:
        abort(404)

    directory_path = directory_entry["path"]

    if not DirectoryService.validate_directory_exists(directory_path):
        abort(404)

    # Update last accessed
    registry_service.update_last_accessed(directory_entry["title"], directory_path, NodeType.DIRECTORY)

    courses = DirectoryService.scan_directory(directory_path)

    breadcrumbs = registry_service.build_breadcrumbs_for_current_page(directory_path, directory_entry["title"])

    # Get user theme
    preferences_service = UserPreferencesService()
    user_theme = preferences_service.get_theme()

    return render_template("directory.html", courses=courses, directory_title=directory_entry["title"], directory_id=directory_id, breadcrumbs=breadcrumbs, user_theme=user_theme)
