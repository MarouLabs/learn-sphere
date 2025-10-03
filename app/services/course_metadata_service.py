import json
import os
from typing import Optional
from dataclasses import asdict
from datetime import datetime

from app.models.course_metadata_model import CourseMetadata


class CourseMetadataService:
    """Service to manage course metadata stored in .learn_sphere_metadata.json files."""

    METADATA_FILENAME = ".learn_sphere_metadata.json"

    @staticmethod
    def get_metadata_path(course_directory: str) -> str:
        """Get the full path to the metadata file for a course directory."""
        return os.path.join(course_directory, CourseMetadataService.METADATA_FILENAME)

    @staticmethod
    def metadata_exists(course_directory: str) -> bool:
        """Check if metadata file exists for a course directory."""
        metadata_path = CourseMetadataService.get_metadata_path(course_directory)
        return os.path.exists(metadata_path)

    @staticmethod
    def load_course_metadata(course_directory: str) -> Optional[CourseMetadata]:
        """Load course metadata from the .learn_sphere_metadata.json file."""
        metadata_path = CourseMetadataService.get_metadata_path(course_directory)

        if not os.path.exists(metadata_path):
            return None

        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extract the metadata part
            metadata_dict = data.get('metadata', data)  # Support both nested and flat structure
            return CourseMetadata(**metadata_dict)

        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Error loading course metadata from {metadata_path}: {e}")
            return None

    @staticmethod
    def save_course_metadata(course_directory: str, metadata: CourseMetadata) -> bool:
        """Save course metadata to the .learn_sphere_metadata.json file."""
        metadata_path = CourseMetadataService.get_metadata_path(course_directory)

        try:
            # Update timestamps
            now = datetime.now().isoformat()
            if not metadata.created_at:
                metadata.created_at = now
            metadata.updated_at = now

            # Convert to dictionary
            data = {
                'metadata': asdict(metadata)
            }

            # Ensure directory exists
            os.makedirs(course_directory, exist_ok=True)

            # Write to file
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"Error saving course metadata to {metadata_path}: {e}")
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