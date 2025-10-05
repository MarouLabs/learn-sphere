import os
from typing import Optional, Tuple, Dict, Any
from app.utils.path_validator import PathValidator
from app.models.lesson_type import get_lesson_type_from_extension, LessonType, DOCUMENT_EXTENSIONS
import markdown


class LessonService:
    """Service for handling lesson-related operations."""

    @staticmethod
    def build_lesson_path(course_path: str, lesson_path: str) -> str:
        """
        Build the full lesson path from course path and relative lesson path.
        Validates that the lesson path doesn't escape the course directory.

        Args:
            course_path (str): The absolute path to the course
            lesson_path (str): The relative path to the lesson within the course

        Returns:
            str: The full absolute path to the lesson

        Raises:
            ValueError: If the lesson path attempts to escape the course directory
        """
        return PathValidator.validate_safe_path(lesson_path, course_path)

    @staticmethod
    def validate_lesson_exists(lesson_path: str) -> bool:
        """
        Validate that a lesson file exists.

        Args:
            lesson_path (str): The absolute path to the lesson file

        Returns:
            bool: True if lesson file exists, False otherwise
        """
        return os.path.exists(lesson_path) and os.path.isfile(lesson_path)

    @staticmethod
    def extract_lesson_title(lesson_path: str) -> str:
        """
        Extract lesson title from the filename.

        Args:
            lesson_path (str): The path to the lesson file

        Returns:
            str: The lesson title without extension
        """
        return os.path.splitext(os.path.basename(lesson_path))[0]

    @staticmethod
    def get_module_info(lesson_path: str) -> Optional[Tuple[bool, str]]:
        """
        Get module information from lesson path.

        Args:
            lesson_path (str): The relative lesson path

        Returns:
            Optional[Tuple[bool, str]]: (has_module, module_name) or None
        """
        module_dir = os.path.dirname(lesson_path)
        if module_dir:
            return (True, module_dir)
        return (False, None)

    @staticmethod
    def prepare_lesson_content(file_path: str) -> Dict[str, Any]:
        """
        Prepare lesson content based on file type.

        Args:
            file_path (str): Absolute path to the lesson file

        Returns:
            Dict[str, Any]: Dictionary containing:
                - lesson_type: LessonType enum
                - text_content: Rendered content for text files (None for media)
                - is_markdown: Boolean indicating if content is markdown
                - is_pdf: Boolean indicating if file is PDF
                - is_html: Boolean indicating if file is HTML
        """
        file_extension = os.path.splitext(file_path)[1]
        lesson_type = get_lesson_type_from_extension(file_extension)

        is_pdf = file_extension.lower() in DOCUMENT_EXTENSIONS
        is_html = file_extension.lower() in ['.html', '.htm']
        text_content = None
        is_markdown = False

        if lesson_type == LessonType.TEXT and not is_pdf:
            text_content = LessonService._read_text_file(file_path)

            if file_extension.lower() in ['.md', '.markdown']:
                is_markdown = True
                text_content = LessonService._render_markdown(text_content)

        return {
            'lesson_type': lesson_type,
            'text_content': text_content,
            'is_markdown': is_markdown,
            'is_pdf': is_pdf,
            'is_html': is_html
        }

    @staticmethod
    def _read_text_file(file_path: str) -> str:
        """
        Read text file content.

        Args:
            file_path (str): Path to the text file

        Returns:
            str: File content or error message
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception:
                return "Error reading file content. File encoding not supported."
        except Exception as e:
            return f"Error reading file content: {str(e)}"

    @staticmethod
    def _render_markdown(content: str) -> str:
        """
        Render markdown content to HTML.

        Args:
            content (str): Raw markdown content

        Returns:
            str: Rendered HTML
        """
        try:
            return markdown.markdown(
                content,
                extensions=['fenced_code', 'tables', 'nl2br', 'codehilite']
            )
        except Exception:
            return content

    @staticmethod
    def get_file_metadata(file_path: str, lesson_type: LessonType) -> Dict[str, Any]:
        """
        Get file metadata (size, format, duration for media files, etc.).

        Args:
            file_path (str): Absolute path to the file
            lesson_type (LessonType): Type of lesson (video, audio, text)

        Returns:
            Dict[str, Any]: Dictionary containing:
                - file_size: Human-readable file size
                - file_size_bytes: Raw file size in bytes
                - file_format: File extension (e.g., .mp4, .pdf)
                - duration: Duration for media files (None for non-media)
                - duration_seconds: Raw duration in seconds
        """
        try:
            file_stats = os.stat(file_path)
            file_size_bytes = file_stats.st_size
            file_extension = os.path.splitext(file_path)[1].upper()

            def format_file_size(size_bytes: int) -> str:
                """Convert bytes to human-readable format."""
                for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                    if size_bytes < 1024.0:
                        return f"{size_bytes:.2f} {unit}"
                    size_bytes /= 1024.0
                return f"{size_bytes:.2f} PB"

            def format_duration(seconds: int) -> str:
                """Convert seconds to HH:MM:SS or MM:SS format."""
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                secs = seconds % 60

                if hours > 0:
                    return f"{hours:02d}:{minutes:02d}:{secs:02d}"
                else:
                    return f"{minutes:02d}:{secs:02d}"

            # TODO: Extract actual duration from media files
            # For now, generate random placeholder duration for media files
            duration = None
            duration_seconds = 0

            if lesson_type in [LessonType.VIDEO, LessonType.AUDIO]:
                import random
                # Generate random duration between 1 minute and 2 hours
                duration_seconds = random.randint(60, 7200)
                duration = format_duration(duration_seconds)

            return {
                'file_size': format_file_size(file_size_bytes),
                'file_size_bytes': file_stats.st_size,
                'file_format': file_extension.lstrip('.'),
                'duration': duration,
                'duration_seconds': duration_seconds
            }
        except Exception:
            return {
                'file_size': 'Unknown',
                'file_size_bytes': 0,
                'file_format': 'Unknown',
                'duration': None,
                'duration_seconds': 0
            }

    @staticmethod
    def prepare_lesson_view(course_id: str, lesson_path: str, registry_service) -> Optional[Dict[str, Any]]:
        """
        Prepare all data needed for lesson view template.

        Args:
            course_id (str): Course ID
            lesson_path (str): Relative lesson path
            registry_service: RegistryService instance

        Returns:
            Optional[Dict[str, Any]]: Lesson view data or None if invalid
        """
        course_entry = registry_service.get_course_by_id(course_id)
        if not course_entry:
            return None

        course_path = course_entry["path"]

        try:
            full_lesson_path = LessonService.build_lesson_path(course_path, lesson_path)
        except ValueError:
            return None

        if not LessonService.validate_lesson_exists(full_lesson_path):
            return None

        lesson_title = LessonService.extract_lesson_title(lesson_path)
        lesson_content = LessonService.prepare_lesson_content(full_lesson_path)
        file_metadata = LessonService.get_file_metadata(full_lesson_path, lesson_content['lesson_type'])

        breadcrumbs = registry_service.build_breadcrumbs_from_path(course_path, course_entry["title"])

        has_module, module_name = LessonService.get_module_info(lesson_path)
        if has_module:
            module_anchor = module_name.replace(' ', '-').replace('/', '-').lower()
            module_url = f'/course/{course_id}#module-{module_anchor}'
            breadcrumbs.append({"title": module_name, "url": module_url})

        breadcrumbs.append({"title": lesson_title, "url": None})

        return {
            'lesson_title': lesson_title,
            'course_title': course_entry["title"],
            'lesson_type': lesson_content['lesson_type'].value,
            'media_url': f'/media/course/{course_id}/{lesson_path}',
            'download_url': f'/lesson/{course_id}/{lesson_path}/download',
            'text_content': lesson_content['text_content'],
            'is_markdown': lesson_content['is_markdown'],
            'is_pdf': lesson_content['is_pdf'],
            'is_html': lesson_content['is_html'],
            'file_size': file_metadata['file_size'],
            'file_format': file_metadata['file_format'],
            'duration': file_metadata['duration'],
            'breadcrumbs': breadcrumbs
        }

    @staticmethod
    def prepare_lesson_download(course_id: str, lesson_path: str, registry_service) -> Optional[Dict[str, Any]]:
        """
        Prepare data for lesson file download.

        Args:
            course_id (str): Course ID
            lesson_path (str): Relative lesson path
            registry_service: RegistryService instance

        Returns:
            Optional[Dict[str, Any]]: Download data or None if invalid
        """
        course_entry = registry_service.get_course_by_id(course_id)
        if not course_entry:
            return None

        course_path = course_entry["path"]

        try:
            full_lesson_path = LessonService.build_lesson_path(course_path, lesson_path)
        except ValueError:
            return None

        if not LessonService.validate_lesson_exists(full_lesson_path):
            return None

        filename = os.path.basename(full_lesson_path)

        return {
            'file_path': full_lesson_path,
            'filename': filename
        }
