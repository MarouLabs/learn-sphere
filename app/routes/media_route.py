from flask import Blueprint, send_file, abort
from app.services.registry_service import RegistryService
from app.services.media_service import MediaService

bp = Blueprint("media", __name__)


@bp.route("/media/course/<path:course_id>/<path:file_path>")
def serve_course_file(course_id, file_path):
    """Serve media files (images, videos, etc.) from course directories."""
    registry_service = RegistryService()

    course_entry = registry_service.get_course_by_id(course_id)
    if not course_entry:
        abort(404)

    course_path = course_entry["path"]

    is_valid, full_file_path = MediaService.get_course_file_path(course_path, file_path)
    if not is_valid:
        abort(404)

    return send_file(full_file_path)


@bp.route("/media/directory/<path:directory_id>/<path:file_path>")
def serve_directory_file(directory_id, file_path):
    """Serve media files (images) from directory paths."""
    registry_service = RegistryService()

    directory_entry = registry_service.get_directory_by_id(directory_id)
    if not directory_entry:
        abort(404)

    directory_path = directory_entry["path"]

    is_valid, full_file_path = MediaService.get_directory_file_path(directory_path, file_path)
    if not is_valid:
        abort(404)

    return send_file(full_file_path)
