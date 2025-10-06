from flask import Blueprint, render_template, abort
from app.services.registry_service import RegistryService
from app.services.user_preferences_service import UserPreferencesService
from app.services.course_metadata_service import CourseMetadataService
from app.services.content_detection_service import ContentDetectionService
from app.services.directory_service import DirectoryService
from app.services.progress_service import ProgressService
from app.models.course_model import NodeType
from app.models.course_structure_model import CourseStructure

bp = Blueprint("course", __name__)


@bp.route("/course/<path:course_id>")
def details(course_id):
    """View course details including modules and lessons."""
    registry_service = RegistryService()

    course_entry = registry_service.get_course_by_id(course_id)
    if not course_entry:
        abort(404)

    course_path = course_entry["path"]

    if not DirectoryService.validate_directory_exists(course_path):
        abort(404)

    # Update last accessed
    course_node_type = NodeType(course_entry["node_type"])
    registry_service.update_last_accessed(course_entry["title"], course_path, course_node_type)

    # Get course metadata and structure
    metadata = CourseMetadataService.get_or_create_metadata(course_path, course_entry["title"])
    modules = ContentDetectionService.scan_course_modules(course_path)
    lessons = ContentDetectionService.scan_course_lessons(course_path)

    # Load progress data and apply to lessons
    progress_service = ProgressService(course_path)
    progress_data = progress_service.get_progress()
    progress_lessons = progress_data.get("lessons", {})

    # Apply progress to root-level lessons
    for lesson in lessons:
        if lesson.file_path:
            lesson_filename = lesson.file_path.split('/')[-1]
            if lesson_filename in progress_lessons:
                lesson.completed = progress_lessons[lesson_filename].get("completed", False)

    # Apply progress to module lessons
    for module in modules:
        for lesson in module.lessons:
            if lesson.file_path:
                lesson_filename = lesson.file_path.split('/')[-1]
                lesson_relative_path = f"{module.directory_name}/{lesson_filename}" if module.directory_name else lesson_filename
                if lesson_relative_path in progress_lessons:
                    lesson.completed = progress_lessons[lesson_relative_path].get("completed", False)

    # Update metadata with current counts
    metadata.total_modules = len(modules)
    metadata.total_lessons = sum(len(module.lessons) for module in modules) + len(lessons)
    metadata.total_media_duration_seconds = sum(module.total_duration_seconds for module in modules) + sum(lesson.duration_seconds for lesson in lessons)

    # Save updated metadata
    CourseMetadataService.save_course_metadata(course_path, metadata)

    course_structure = CourseStructure(metadata=metadata, modules=modules, lessons=lessons)

    breadcrumbs = registry_service.build_breadcrumbs_for_current_page(course_path, course_entry["title"])

    # Get user theme
    preferences_service = UserPreferencesService()
    user_theme = preferences_service.get_theme()

    return render_template("course_details.html", course_structure=course_structure, course_id=course_id, breadcrumbs=breadcrumbs, user_theme=user_theme)
