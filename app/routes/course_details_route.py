from flask import Blueprint, render_template, abort
import os
from app.services.registry_service import RegistryService
from app.services.user_preferences_service import UserPreferencesService
from app.services.course_metadata_service import CourseMetadataService
from app.services.content_detection_service import ContentDetectionService
from app.models.course_model import NodeType
from app.models.course_structure_model import CourseStructure

bp = Blueprint("course", __name__)


@bp.route("/course/<path:course_id>")
def details(course_id):
    """View course details including modules and lessons."""
    registry_service = RegistryService()

    # Check if course is registered
    course_entry = registry_service.get_course_by_id(course_id)
    if not course_entry:
        abort(404)

    course_path = course_entry["path"]

    # Check if course still exists
    if not os.path.exists(course_path) or not os.path.isdir(course_path):
        abort(404)

    # Update last accessed
    course_node_type = NodeType(course_entry["node_type"])
    registry_service.update_last_accessed(course_entry["title"], course_path, course_node_type)

    # Get course metadata and structure
    metadata = CourseMetadataService.get_or_create_metadata(course_path, course_entry["title"])
    modules = ContentDetectionService.scan_course_modules(course_path)
    lessons = ContentDetectionService.scan_course_lessons(course_path)

    # Update metadata with current counts
    metadata.total_modules = len(modules)
    metadata.total_lessons = sum(len(module.lessons) for module in modules) + len(lessons)
    metadata.total_media_duration_seconds = sum(module.total_duration_seconds for module in modules) + sum(lesson.duration_seconds for lesson in lessons)

    # Save updated metadata
    CourseMetadataService.save_course_metadata(course_path, metadata)

    # Create course structure
    course_structure = CourseStructure(metadata=metadata, modules=modules, lessons=lessons)

    # Build breadcrumbs
    breadcrumbs = registry_service.build_breadcrumbs_from_path(course_path, course_entry["title"])
    # Remove URL from last breadcrumb (current page)
    if breadcrumbs:
        breadcrumbs[-1]["url"] = None

    # Get user theme
    preferences_service = UserPreferencesService()
    user_theme = preferences_service.get_theme()

    return render_template("course_details.html", course_structure=course_structure, course_id=course_id, breadcrumbs=breadcrumbs, user_theme=user_theme)
