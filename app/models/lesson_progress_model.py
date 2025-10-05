from dataclasses import dataclass
from typing import Optional


@dataclass
class LessonProgress:
    lesson_path: str
    completed: bool = False
    last_position_seconds: float = 0.0
    last_accessed_at: Optional[str] = None
