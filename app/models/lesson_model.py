from dataclasses import dataclass
from typing import Optional
from enum import Enum
import datetime


class LessonType(Enum):
    VIDEO = "video"
    AUDIO = "audio"
    TEXT = "text"

@dataclass
class Lesson:
    title: str
    lesson_type: LessonType
    file_path: str 
    
    # for video/audio
    duration_seconds: Optional[int] = None
    progress_seconds: int = 0
    completed: bool = False
    
    # For text lessons: optionally store parsed content
    text_content: Optional[str] = None

    last_accessed_at: Optional[str] = None  # ISO timestamp
    order_index: int = 0  # position in module

    def mark_accessed(self):
        self.last_accessed_at = datetime.datetime.now(datetime.timezone.utc)

    def mark_completed(self):
        self.completed = True
        self.progress_seconds = self.duration_seconds or self.progress_seconds
