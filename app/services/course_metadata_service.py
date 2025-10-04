from typing import Optional
from dataclasses import asdict
from datetime import datetime

from app.models.course_metadata_model import CourseMetadata
from app.repositories.course_metadata_repository import CourseMetadataRepository


class CourseMetadataService:
    """Service to manage course metadata stored in .learn_sphere_metadata.json files."""

    @staticmethod
    def get_metadata_path(course_directory: str) -> str:
        """Get the full path to the metadata file for a course directory."""
        return CourseMetadataRepository.get_metadata_path(course_directory)

    @staticmethod
    def metadata_exists(course_directory: str) -> bool:
        """Check if metadata file exists for a course directory."""
        return CourseMetadataRepository.metadata_exists(course_directory)

    @staticmethod
    def load_course_metadata(course_directory: str) -> Optional[CourseMetadata]:
        """Load course metadata from the .learn_sphere_metadata.json file."""
        repository = CourseMetadataRepository(course_directory)

        try:
            data = repository.load()
            if not data:
                return None

            metadata_dict = data.get('metadata', data)
            return CourseMetadata(**metadata_dict)

        except (IOError, KeyError, TypeError) as e:
            print(f"Error loading course metadata from {course_directory}: {e}")
            return None

    @staticmethod
    def save_course_metadata(course_directory: str, metadata: CourseMetadata) -> bool:
        """Save course metadata to the .learn_sphere_metadata.json file."""
        repository = CourseMetadataRepository(course_directory)

        try:
            now = datetime.now().isoformat()
            if not metadata.created_at:
                metadata.created_at = now
            metadata.updated_at = now

            data = {
                'metadata': asdict(metadata)
            }

            return repository.save(data)

        except Exception as e:
            print(f"Error saving course metadata to {course_directory}: {e}")
            return False

    @staticmethod
    def create_default_metadata(course_directory: str, course_title: str, description: str = "") -> CourseMetadata:
        """Create and save default metadata for a course."""
        metadata = CourseMetadata(
            title=course_title,
            description=description,
            total_modules=0,
            total_lessons=0,
            total_media_duration_seconds=0,
            image_path=None
        )

        CourseMetadataService.save_course_metadata(course_directory, metadata)
        return metadata

    @staticmethod
    def get_or_create_metadata(course_directory: str, course_title: str) -> CourseMetadata:
        """Get existing metadata or create default metadata."""
        metadata = CourseMetadataService.load_course_metadata(course_directory)

        if not metadata:
            metadata = CourseMetadataService.create_default_metadata(course_directory, course_title)

        return metadata