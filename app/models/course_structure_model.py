from dataclasses import dataclass
from typing import List
from .course_metadata_model import CourseMetadata
from .module_data_model import ModuleData
from .lesson_data_model import LessonData


@dataclass
class CourseStructure:
    metadata: CourseMetadata
    modules: List[ModuleData]
    lessons: List[LessonData]