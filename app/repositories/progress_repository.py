import os
from .base_json_repository import BaseJsonRepository


class ProgressRepository(BaseJsonRepository):
    """Repository for course progress stored in .learn_sphere_progress.json files."""

    PROGRESS_FILENAME = ".learn_sphere_progress.json"

    def __init__(self, course_directory: str):
        progress_path = os.path.join(course_directory, self.PROGRESS_FILENAME)
        super().__init__(progress_path)
        self.course_directory = course_directory

    @staticmethod
    def get_progress_path(course_directory: str) -> str:
        """Get the full path to the progress file for a course directory."""
        return os.path.join(course_directory, ProgressRepository.PROGRESS_FILENAME)

    @staticmethod
    def progress_exists(course_directory: str) -> bool:
        """Check if progress file exists for a course directory."""
        progress_path = ProgressRepository.get_progress_path(course_directory)
        return os.path.exists(progress_path)
