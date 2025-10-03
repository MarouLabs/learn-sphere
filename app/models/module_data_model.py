from dataclasses import dataclass
from typing import List, Optional
from .lesson_data_model import LessonData


@dataclass
class ModuleData:
    title: str
    module_number: int
    lessons: List[LessonData]
    total_duration_seconds: int = 0
    completed: bool = False
    directory_name: Optional[str] = None