import os
from typing import Optional, Dict, Any
from .base_json_repository import BaseJsonRepository


class CourseMetadataRepository(BaseJsonRepository):
    """Repository for course metadata stored in .learn_sphere_metadata.json files."""

    METADATA_FILENAME = ".learn_sphere_metadata.json"

    def __init__(self, course_directory: str):
        metadata_path = os.path.join(course_directory, self.METADATA_FILENAME)
        super().__init__(metadata_path)
        self.course_directory = course_directory

    @staticmethod
    def get_metadata_path(course_directory: str) -> str:
        """Get the full path to the metadata file for a course directory."""
        return os.path.join(course_directory, CourseMetadataRepository.METADATA_FILENAME)

    @staticmethod
    def metadata_exists(course_directory: str) -> bool:
        """Check if metadata file exists for a course directory."""
        metadata_path = CourseMetadataRepository.get_metadata_path(course_directory)
        return os.path.exists(metadata_path)
