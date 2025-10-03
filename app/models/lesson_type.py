from enum import Enum


class LessonType(Enum):
    TEXT = "text"
    VIDEO = "video"
    AUDIO = "audio"
    UNKNOWN = "unknown"


# File extension constants
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.m4v', '.flv', '.wmv'}
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac', '.wma'}
TEXT_EXTENSIONS = {'.txt', '.md', '.rst', '.doc', '.docx'}
DOCUMENT_EXTENSIONS = {'.pdf', '.epub', '.mobi'}

# Extension to lesson type mapping
EXTENSION_TO_LESSON_TYPE = {}

# Populate the mapping
for ext in VIDEO_EXTENSIONS:
    EXTENSION_TO_LESSON_TYPE[ext] = LessonType.VIDEO

for ext in AUDIO_EXTENSIONS:
    EXTENSION_TO_LESSON_TYPE[ext] = LessonType.AUDIO

for ext in TEXT_EXTENSIONS:
    EXTENSION_TO_LESSON_TYPE[ext] = LessonType.TEXT


def get_lesson_type_from_extension(file_extension: str) -> LessonType:
    """Get lesson type from file extension."""
    ext_lower = file_extension.lower()
    return EXTENSION_TO_LESSON_TYPE.get(ext_lower, LessonType.UNKNOWN)