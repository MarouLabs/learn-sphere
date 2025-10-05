from flask import Blueprint, request, jsonify
from app.services.progress_service import ProgressService
from app.services.registry_service import RegistryService

progress_blueprint = Blueprint("progress", __name__, url_prefix="/api/progress")


@progress_blueprint.route("/<course_id>", methods=["GET"])
def get_course_progress(course_id):
    """Get all progress data for a course."""
    try:
        registry_service = RegistryService()
        course_entry = registry_service.get_course_by_id(course_id)

        if not course_entry:
            return jsonify({"success": False, "error": "Course not found"}), 404

        course_path = course_entry["path"]
        progress_service = ProgressService(course_path)
        progress_data = progress_service.get_progress()

        return jsonify({"success": True, "progress": progress_data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@progress_blueprint.route("/<course_id>/lesson", methods=["GET"])
def get_lesson_progress(course_id):
    """Get progress for a specific lesson."""
    try:
        lesson_path = request.args.get("lesson_path")
        if not lesson_path:
            return jsonify({"success": False, "error": "lesson_path parameter is required"}), 400

        registry_service = RegistryService()
        course_entry = registry_service.get_course_by_id(course_id)

        if not course_entry:
            return jsonify({"success": False, "error": "Course not found"}), 404

        course_path = course_entry["path"]
        progress_service = ProgressService(course_path)
        lesson_progress = progress_service.get_lesson_progress(lesson_path)

        if not lesson_progress:
            return jsonify({
                "success": True,
                "progress": {
                    "lesson_path": lesson_path,
                    "completed": False,
                    "last_position_seconds": 0.0,
                    "last_accessed_at": None
                }
            })

        return jsonify({
            "success": True,
            "progress": {
                "lesson_path": lesson_progress.lesson_path,
                "completed": lesson_progress.completed,
                "last_position_seconds": lesson_progress.last_position_seconds,
                "last_accessed_at": lesson_progress.last_accessed_at
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@progress_blueprint.route("/<course_id>/lesson", methods=["POST"])
def update_lesson_progress(course_id):
    """Update progress for a specific lesson."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        lesson_path = data.get("lesson_path")
        if not lesson_path:
            return jsonify({"success": False, "error": "lesson_path is required"}), 400

        registry_service = RegistryService()
        course_entry = registry_service.get_course_by_id(course_id)

        if not course_entry:
            return jsonify({"success": False, "error": "Course not found"}), 404

        course_path = course_entry["path"]
        progress_service = ProgressService(course_path)

        completed = data.get("completed")
        last_position_seconds = data.get("last_position_seconds")

        success = progress_service.update_lesson_progress(
            lesson_path=lesson_path,
            completed=completed,
            last_position_seconds=last_position_seconds
        )

        if success:
            return jsonify({"success": True, "message": "Progress updated successfully"})
        else:
            return jsonify({"success": False, "error": "Failed to update progress"}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@progress_blueprint.route("/<course_id>/lesson/complete", methods=["POST"])
def mark_lesson_complete(course_id):
    """Mark a lesson as completed."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        lesson_path = data.get("lesson_path")
        if not lesson_path:
            return jsonify({"success": False, "error": "lesson_path is required"}), 400

        registry_service = RegistryService()
        course_entry = registry_service.get_course_by_id(course_id)

        if not course_entry:
            return jsonify({"success": False, "error": "Course not found"}), 404

        course_path = course_entry["path"]
        progress_service = ProgressService(course_path)

        success = progress_service.mark_lesson_completed(lesson_path)

        if success:
            return jsonify({"success": True, "message": "Lesson marked as completed"})
        else:
            return jsonify({"success": False, "error": "Failed to mark lesson as completed"}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@progress_blueprint.route("/<course_id>/lesson/incomplete", methods=["POST"])
def mark_lesson_incomplete(course_id):
    """Mark a lesson as incomplete."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        lesson_path = data.get("lesson_path")
        if not lesson_path:
            return jsonify({"success": False, "error": "lesson_path is required"}), 400

        registry_service = RegistryService()
        course_entry = registry_service.get_course_by_id(course_id)

        if not course_entry:
            return jsonify({"success": False, "error": "Course not found"}), 404

        course_path = course_entry["path"]
        progress_service = ProgressService(course_path)

        success = progress_service.mark_lesson_incomplete(lesson_path)

        if success:
            return jsonify({"success": True, "message": "Lesson marked as incomplete"})
        else:
            return jsonify({"success": False, "error": "Failed to mark lesson as incomplete"}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@progress_blueprint.route("/<course_id>/playback-position", methods=["POST"])
def update_playback_position(course_id):
    """Update playback position for a video/audio lesson."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        lesson_path = data.get("lesson_path")
        position_seconds = data.get("position_seconds")

        if not lesson_path:
            return jsonify({"success": False, "error": "lesson_path is required"}), 400

        if position_seconds is None:
            return jsonify({"success": False, "error": "position_seconds is required"}), 400

        registry_service = RegistryService()
        course_entry = registry_service.get_course_by_id(course_id)

        if not course_entry:
            return jsonify({"success": False, "error": "Course not found"}), 404

        course_path = course_entry["path"]
        progress_service = ProgressService(course_path)

        success = progress_service.update_playback_position(lesson_path, position_seconds)

        if success:
            return jsonify({"success": True, "message": "Playback position updated"})
        else:
            return jsonify({"success": False, "error": "Failed to update playback position"}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@progress_blueprint.route("/<course_id>/stats", methods=["GET"])
def get_completion_stats(course_id):
    """Get completion statistics for a course."""
    try:
        registry_service = RegistryService()
        course_entry = registry_service.get_course_by_id(course_id)

        if not course_entry:
            return jsonify({"success": False, "error": "Course not found"}), 404

        course_path = course_entry["path"]
        progress_service = ProgressService(course_path)
        stats = progress_service.get_course_completion_stats()

        return jsonify({"success": True, "stats": stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
