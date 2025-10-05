from flask import Blueprint, render_template, abort, send_file
from app.services.lesson_service import LessonService
from app.services.registry_service import RegistryService
from app.services.user_preferences_service import UserPreferencesService

bp = Blueprint("lesson", __name__)


@bp.route("/lesson/<path:course_id>/<path:lesson_path>")
def view(course_id, lesson_path):
    """View a lesson within a course."""
    registry_service = RegistryService()
    preferences_service = UserPreferencesService()

    lesson_view_data = LessonService.prepare_lesson_view(course_id, lesson_path, registry_service)

    if not lesson_view_data:
        abort(404)

    user_theme = preferences_service.get_theme()
    playback_speeds = preferences_service.get_playback_speeds()

    return render_template("lesson_view.html",
                         lesson_title=lesson_view_data['lesson_title'],
                         course_title=lesson_view_data['course_title'],
                         course_id=course_id,
                         lesson_path=lesson_path,
                         lesson_type=lesson_view_data['lesson_type'],
                         media_url=lesson_view_data['media_url'],
                         download_url=lesson_view_data['download_url'],
                         text_content=lesson_view_data['text_content'],
                         is_markdown=lesson_view_data['is_markdown'],
                         is_pdf=lesson_view_data['is_pdf'],
                         is_html=lesson_view_data['is_html'],
                         file_size=lesson_view_data['file_size'],
                         file_format=lesson_view_data['file_format'],
                         duration=lesson_view_data['duration'],
                         breadcrumbs=lesson_view_data['breadcrumbs'],
                         next_lesson=lesson_view_data['next_lesson'],
                         previous_lesson=lesson_view_data['previous_lesson'],
                         back_to_course_url=lesson_view_data['back_to_course_url'],
                         user_theme=user_theme,
                         video_speed=playback_speeds.get('video', 1.0),
                         audio_speed=playback_speeds.get('audio', 1.0))


@bp.route("/lesson/<path:course_id>/<path:lesson_path>/download")
def download(course_id, lesson_path):
    """Download a lesson file."""
    registry_service = RegistryService()

    download_data = LessonService.prepare_lesson_download(course_id, lesson_path, registry_service)

    if not download_data:
        abort(404)

    return send_file(download_data['file_path'],
                    as_attachment=True,
                    download_name=download_data['filename'])
