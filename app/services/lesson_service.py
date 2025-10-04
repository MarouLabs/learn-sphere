import os
from typing import Optional, Tuple
from app.utils.path_validator import PathValidator


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
