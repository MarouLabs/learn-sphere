from flask import Blueprint, render_template, abort, request, jsonify
import os
from config import Config
from app.services.directory_service import DirectoryService
from app.services.registry_service import RegistryService
from app.services.user_preferences_service import UserPreferencesService
from app.services.course_metadata_service import CourseMetadataService
from app.services.content_detection_service import ContentDetectionService
from app.models.course_model import NodeType
from app.models.course_structure_model import CourseStructure

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    # Get courses from the configured directory
    courses = DirectoryService.scan_directory(Config.COURSES_ROOT_DIRECTORY_ABS_PATH)

    # Get user theme
    preferences_service = UserPreferencesService()
    user_theme = preferences_service.get_theme()

    return render_template("home.html", courses=courses, user_theme=user_theme)

@bp.route("/directory/<path:directory_id>")
def directory_view(directory_id):
    registry_service = RegistryService()

    # Check if directory is registered
    directory_entry = registry_service.get_directory_by_id(directory_id)
    if not directory_entry:
        abort(404)

    directory_path = directory_entry["path"]

    # Check if directory still exists
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        abort(404)

    # Update last accessed
    registry_service.update_last_accessed(directory_entry["title"], directory_path, NodeType.DIRECTORY)

    # Get directory contents
    courses = DirectoryService.scan_directory(directory_path)

    # Get user theme
    preferences_service = UserPreferencesService()
    user_theme = preferences_service.get_theme()

    return render_template("directory.html", courses=courses, directory_title=directory_entry["title"], directory_id=directory_id, user_theme=user_theme)

@bp.route("/course/<path:course_id>")
def course_details(course_id):
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

    # Get user theme
    preferences_service = UserPreferencesService()
    user_theme = preferences_service.get_theme()

    return render_template("course_details.html", course_structure=course_structure, course_id=course_id, user_theme=user_theme)

@bp.route("/lesson/<path:course_id>/<path:lesson_path>")
def lesson_view(course_id, lesson_path):
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

    # Get user theme
    preferences_service = UserPreferencesService()
    user_theme = preferences_service.get_theme()

    return render_template("lesson_view.html",
                         lesson_title=lesson_title,
                         course_title=course_entry["title"],
                         course_id=course_id,
                         lesson_path=full_lesson_path,
                         user_theme=user_theme)
