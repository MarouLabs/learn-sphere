from dataclasses import dataclass
from typing import Optional
from .lesson_type import LessonType


@dataclass
class LessonData:
    title: str
    lesson_type: LessonType = LessonType.TEXT
    duration_seconds: int = 0
    completed: bool = False
    file_path: Optional[str] = None