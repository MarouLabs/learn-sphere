from flask import Blueprint, render_template, abort
from app.services.registry_service import RegistryService
from app.services.user_preferences_service import UserPreferencesService
from app.services.lesson_service import LessonService

bp = Blueprint("lesson", __name__)


@bp.route("/lesson/<path:course_id>/<path:lesson_path>")
def view(course_id, lesson_path):
    """View a lesson within a course."""
    registry_service = RegistryService()

    course_entry = registry_service.get_course_by_id(course_id)
    if not course_entry:
        abort(404)

    course_path = course_entry["path"]

    try:
        full_lesson_path = LessonService.build_lesson_path(course_path, lesson_path)
    except ValueError:
        abort(404)

    if not LessonService.validate_lesson_exists(full_lesson_path):
        abort(404)

    lesson_title = LessonService.extract_lesson_title(lesson_path)

    breadcrumbs = registry_service.build_breadcrumbs_from_path(course_path, course_entry["title"])

    has_module, module_name = LessonService.get_module_info(lesson_path)
    if has_module:
        breadcrumbs.append({"title": module_name, "url": None})

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
