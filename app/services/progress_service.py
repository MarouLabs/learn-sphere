from datetime import datetime
from typing import Optional, Dict, Any
from app.repositories.progress_repository import ProgressRepository
from app.models.lesson_progress_model import LessonProgress


class ProgressService:
    """Service for managing course progress and lesson completion."""

    def __init__(self, course_directory: str):
        self.repository = ProgressRepository(course_directory)

    def get_progress(self) -> Dict[str, Any]:
        """Load all progress data for the course."""
        data = self.repository.load()
        if not data:
            return self._create_default_progress()
        return data

    def get_lesson_progress(self, lesson_path: str) -> Optional[LessonProgress]:
        """Get progress for a specific lesson."""
        progress_data = self.get_progress()
        lessons = progress_data.get("lessons", {})

        if lesson_path not in lessons:
            return None

        lesson_data = lessons[lesson_path]
        return LessonProgress(
            lesson_path=lesson_path,
            completed=lesson_data.get("completed", False),
            last_position_seconds=lesson_data.get("last_position_seconds", 0.0),
            last_accessed_at=lesson_data.get("last_accessed_at")
        )

    def update_lesson_progress(
        self,
        lesson_path: str,
        completed: Optional[bool] = None,
        last_position_seconds: Optional[float] = None
    ) -> bool:
        """Update progress for a specific lesson."""
        progress_data = self.get_progress()

        if "lessons" not in progress_data:
            progress_data["lessons"] = {}

        if lesson_path not in progress_data["lessons"]:
            progress_data["lessons"][lesson_path] = {
                "completed": False,
                "last_position_seconds": 0.0,
                "last_accessed_at": None
            }

        lesson_data = progress_data["lessons"][lesson_path]

        if completed is not None:
            lesson_data["completed"] = completed

        if last_position_seconds is not None:
            lesson_data["last_position_seconds"] = last_position_seconds

        lesson_data["last_accessed_at"] = datetime.now().isoformat()
        progress_data["last_updated_at"] = datetime.now().isoformat()

        return self.repository.save(progress_data)

    def mark_lesson_completed(self, lesson_path: str) -> bool:
        """Mark a lesson as completed."""
        return self.update_lesson_progress(lesson_path, completed=True)

    def mark_lesson_incomplete(self, lesson_path: str) -> bool:
        """Mark a lesson as incomplete."""
        return self.update_lesson_progress(lesson_path, completed=False)

    def update_playback_position(self, lesson_path: str, position_seconds: float) -> bool:
        """Update the playback position for a video/audio lesson."""
        return self.update_lesson_progress(lesson_path, last_position_seconds=position_seconds)

    def get_course_completion_stats(self) -> Dict[str, Any]:
        """Get overall completion statistics for the course."""
        progress_data = self.get_progress()
        lessons = progress_data.get("lessons", {})

        total_lessons = len(lessons)
        completed_lessons = sum(1 for lesson in lessons.values() if lesson.get("completed", False))

        completion_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0.0

        return {
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "completion_percentage": round(completion_percentage, 2)
        }

    def _create_default_progress(self) -> Dict[str, Any]:
        """Create default progress structure."""
        return {
            "lessons": {},
            "last_updated_at": None
        }
