from dataclasses import dataclass
from typing import Optional


@dataclass
class CourseMetadata:
    title: str
    description: str = ""
    total_modules: int = 0
    total_lessons: int = 0
    total_media_duration_seconds: int = 0
    image_path: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None