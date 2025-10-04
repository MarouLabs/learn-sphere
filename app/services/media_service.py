import os
from typing import Optional, Tuple
from app.utils.path_validator import PathValidator


class MediaService:
    """Service for handling media file operations."""

    @staticmethod
    def get_course_file_path(course_path: str, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Get and validate the full path to a course file.

        Args:
            course_path: Absolute path to the course directory
            file_path: Relative path to the file within the course

        Returns:
            Tuple of (is_valid, full_path) where is_valid indicates if the file exists
        """
        try:
            full_file_path = PathValidator.validate_safe_path(file_path, course_path)
        except ValueError:
            return (False, None)

        if not os.path.exists(full_file_path) or not os.path.isfile(full_file_path):
            return (False, None)

        return (True, full_file_path)

    @staticmethod
    def get_directory_file_path(directory_path: str, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Get and validate the full path to a directory file.

        Args:
            directory_path: Absolute path to the directory
            file_path: Relative path to the file within the directory

        Returns:
            Tuple of (is_valid, full_path) where is_valid indicates if the file exists
        """
        try:
            full_file_path = PathValidator.validate_safe_path(file_path, directory_path)
        except ValueError:
            return (False, None)

        if not os.path.exists(full_file_path) or not os.path.isfile(full_file_path):
            return (False, None)

        return (True, full_file_path)
