from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


class NodeType(Enum):
    DIRECTORY = "directory"
    COURSE = "course"
    MODULE = "module"
    LESSON = "lesson"
    UNKNOWN = "unknown"

@dataclass
class CourseProgress:
    progress_percent: float = 0.0
    last_accessed_item_timestamp: Optional[int] = None
    last_accessed_item_title: Optional[str] = None
    last_accessed_item_path: Optional[str] = None

@dataclass
class Course:
    id: Optional[str] = None
    title: str = ""
    node_type: NodeType = NodeType.COURSE
    path: Optional[str] = None

    progress: CourseProgress = field(default_factory=CourseProgress)
    image_path: Optional[str] = None
    description: Optional[str] = None
    
    def get_initials(self) -> str:
        """Get initials from the course title for display."""
        words = self.title.split()
        if len(words) >= 2:
            return (words[0][0] + words[1][0]).upper()
        elif len(words) == 1 and len(words[0]) >= 2:
            return words[0][:2].upper()
        elif len(words) == 1:
            return words[0][0].upper()
        return "CO"
