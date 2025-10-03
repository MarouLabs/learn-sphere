from flask import Blueprint, render_template, abort
import os
from app.services.registry_service import RegistryService
from app.services.user_preferences_service import UserPreferencesService

bp = Blueprint("lesson", __name__)


@bp.route("/lesson/<path:course_id>/<path:lesson_path>")
def view(course_id, lesson_path):
    """View a lesson within a course."""
    registry_service = RegistryService()

    # Check if course is registered
    course_entry = registry_service.get_course_by_id(course_id)
    if not course_entry:
        abort(404)

    course_path = course_entry["path"]

    # Construct full lesson path
    full_lesson_path = os.path.join(course_path, lesson_path)

    # Check if lesson file exists
    if not os.path.exists(full_lesson_path) or not os.path.isfile(full_lesson_path):
        abort(404)

    # Extract lesson title from filename
    lesson_title = os.path.splitext(os.path.basename(lesson_path))[0]

    # Build breadcrumbs for course first
    breadcrumbs = registry_service.build_breadcrumbs_from_path(course_path, course_entry["title"])

    # Add module to breadcrumb if lesson is in a subdirectory
    if os.path.dirname(lesson_path):
        module_name = os.path.dirname(lesson_path)
        breadcrumbs.append({"title": module_name, "url": None})

    # Add lesson as final breadcrumb
    breadcrumbs.append({"title": lesson_title, "url": None})

    # Get user theme
    preferences_service = UserPreferencesService()
    user_theme = preferences_service.get_theme()

    return render_template("lesson_view.html",
                         lesson_title=lesson_title,
                         course_title=course_entry["title"],
                         course_id=course_id,
                         lesson_path=full_lesson_path,
                         breadcrumbs=breadcrumbs,
                         user_theme=user_theme)
