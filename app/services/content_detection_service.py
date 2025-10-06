import os
import re
from typing import List, Set
from app.models.course_model import NodeType
from app.models.lesson_data_model import LessonData
from app.models.module_data_model import ModuleData
from app.models.lesson_type import LessonType, get_lesson_type_from_extension, ALL_LESSON_EXTENSIONS
from app.utils.text_formatter import TextFormatter


def natural_sort_key(text: str):
    """
    Generate a key for natural sorting that handles numbers correctly.
    This ensures items are sorted as: 1, 2, 3, ..., 10, 11, ..., 100, 101
    instead of: 1, 10, 100, 11, 2, 20, 3

    Args:
        text (str): The text to generate a sort key for

    Returns:
        list: A list of mixed strings and integers for proper sorting

    Example:
        sorted(['item1', 'item10', 'item2'], key=natural_sort_key)
        # Returns: ['item1', 'item2', 'item10']
    """
    def convert(part):
        return int(part) if part.isdigit() else part.lower()

    return [convert(c) for c in re.split(r'(\d+)', text)]


class ContentDetectionService:
    """Service to detect the type of content in directories (Course, Module, Directory)."""

    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'}
    
    @staticmethod
    def detect_content_type(directory_path: str) -> NodeType:
        """
        Detect if a directory is a Course, Module, or Directory based on its structure.
        
        Args:
            directory_path (str): Path to the directory to analyze
            
        Returns:
            NodeType: The detected type of content
        """
        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            return NodeType.DIRECTORY
            
        try:
            items = os.listdir(directory_path)
            
            # Get directories and files separately
            directories = []
            files = []
            
            for item in items:
                # ignore hidden files and directories
                if item.startswith('.'):
                    continue
                    
                item_path = os.path.join(directory_path, item)
                if os.path.isdir(item_path):
                    directories.append(item_path)
                else:
                    files.append(item)
            
            # Check if it's a Module (only files, no directories)
            if not directories and files:
                # Check if files are lesson-type files
                if ContentDetectionService._has_lesson_files(files):
                    return NodeType.MODULE
                # TODO: if no supported files, return NodeType.UNKNOWN
                    
            # Check if it's a Course
            if ContentDetectionService._is_course_structure(directory_path, directories, files):
                return NodeType.COURSE
                
            # Default to Directory if it contains other directories
            return NodeType.DIRECTORY
            
        except PermissionError:
            # LOG ERROR MESSAGE
            return NodeType.DIRECTORY
    
    @staticmethod
    def _is_lesson_file(file_path: str) -> bool:
        """
        Check if a file is a lesson file.
        A lesson file must be:
        1. A file (not directory)
        2. Not hidden (doesn't start with '.')
        3. Have a supported lesson format extension
        """
        # Check if it's a file
        if not os.path.isfile(file_path):
            return False

        # Get filename
        filename = os.path.basename(file_path)

        # Check if it's hidden
        if filename.startswith('.'):
            return False

        # Check if it has a supported extension
        _, ext = os.path.splitext(filename.lower())
        return ext in ALL_LESSON_EXTENSIONS

    @staticmethod
    def _has_lesson_files(files: List[str]) -> bool:
        """Check if the files list contains lesson-type files."""
        for file in files:
            _, ext = os.path.splitext(file.lower())
            if ext in ALL_LESSON_EXTENSIONS:
                return True
        return False
    
    @staticmethod
    def _is_course_structure(directory_path: str, directories: List[str], files: List[str]) -> bool:
        """
        Check if the directory structure matches a course pattern.
        Course: A folder that has grand children files only (no folders).
        Structure: Course -> Module -> Lesson (files)
        A module cannot contain folders, only files.
        """
        # A course must have at least one subdirectory (module)
        if not directories:
            return False

        # Check that ALL subdirectories are modules (contain only files, no subdirectories)
        for subdir_path in directories:
            try:
                subdir_items = os.listdir(subdir_path)
                has_subdirectories = False
                has_lesson_files = False

                for item in subdir_items:
                    if item.startswith('.'):
                        continue

                    item_path = os.path.join(subdir_path, item)
                    if os.path.isdir(item_path):
                        # If any subdirectory contains folders, this is NOT a course
                        has_subdirectories = True
                        break
                    else:
                        # Check if it's a lesson file
                        _, ext = os.path.splitext(item.lower())
                        if ext in ALL_LESSON_EXTENSIONS:
                            has_lesson_files = True

                # If subdirectory contains other directories, this is NOT a course
                if has_subdirectories:
                    return False

                # If subdirectory has no lesson files, it's not a valid module
                if not has_lesson_files:
                    return False

            except PermissionError:
                # Skip directories we can't access
                continue

        # It's a course if all subdirectories are valid modules (contain only files)
        return True
    
    @staticmethod
    def find_course_image(directory_path: str) -> str:
        """
        Find a course image in the directory.
        
        Args:
            directory_path (str): Path to search for images
            
        Returns:
            str: Path to the image file, or empty string if none found
        """
        if not os.path.exists(directory_path):
            return ""
            
        try:
            items = os.listdir(directory_path)
            
            # Look for common image names first
            priority_names = ['cover', 'thumbnail', 'image', 'logo', 'icon']
            
            for priority_name in priority_names:
                for item in items:
                    name, ext = os.path.splitext(item.lower())
                    if name == priority_name and ext in ContentDetectionService.IMAGE_EXTENSIONS:
                        return os.path.join(directory_path, item)
            
            # If no priority image found, return the first image
            for item in items:
                _, ext = os.path.splitext(item.lower())
                if ext in ContentDetectionService.IMAGE_EXTENSIONS:
                    return os.path.join(directory_path, item)
                    
        except PermissionError:
            pass
            
        return ""
    
    @staticmethod
    def calculate_progress(directory_path: str) -> float:
        """
        Calculate progress for a course/module based on completion tracking.

        Args:
            directory_path (str): Path to calculate progress for

        Returns:
            float: Progress percentage (0.0 to 100.0)
        """
        from app.services.progress_service import ProgressService

        try:
            progress_service = ProgressService(directory_path)
            stats = progress_service.get_course_completion_stats()
            return stats.get("completion_percentage", 0.0)
        except Exception:
            return 0.0

    @staticmethod
    def scan_course_modules(course_directory: str) -> List[ModuleData]:
        """
        Scan course directory and construct modules from subdirectories.

        Args:
            course_directory (str): Path to the course directory

        Returns:
            List[ModuleData]: List of modules found in the course directory
        """
        modules = []

        try:
            # Get all subdirectories (potential modules)
            items = os.listdir(course_directory)
            module_dirs = []

            for item in items:
                item_path = os.path.join(course_directory, item)
                if os.path.isdir(item_path) and not item.startswith('.'):
                    module_dirs.append((item, item_path))

            # Sort module directories using natural sort
            module_dirs.sort(key=lambda x: natural_sort_key(x[0]))

            for module_number, (module_name, module_path) in enumerate(module_dirs, 1):
                lessons = ContentDetectionService.scan_module_lessons(module_path)

                # Calculate total duration for the module
                module_duration = sum(lesson.duration_seconds for lesson in lessons)

                #TODO: Extract this method for reusability
                # Clean up module title
                module_title = module_name
                module_title = TextFormatter.remove_numbering_prefix(module_title)

                module = ModuleData(
                    title=module_title,
                    module_number=module_number,
                    lessons=lessons,
                    total_duration_seconds=module_duration,
                    completed=False,  # TODO: Calculate based on lesson completion
                    directory_name=module_name
                )
                modules.append(module)

        except PermissionError:
            pass

        return modules

    @staticmethod
    def scan_module_lessons(module_directory: str) -> List[LessonData]:
        """
        Scan module directory and construct lessons from files.

        Args:
            module_directory (str): Path to the module directory

        Returns:
            List[LessonData]: List of lessons found in the module directory
        """
        lessons = []

        try:
            lesson_files = os.listdir(module_directory)
            lesson_files.sort(key=natural_sort_key)

            for lesson_file in lesson_files:
                if lesson_file.startswith('.'):
                    continue

                lesson_path = os.path.join(module_directory, lesson_file)
                if os.path.isfile(lesson_path):
                    # Determine lesson type based on file extension
                    ext = os.path.splitext(lesson_file)[1]
                    lesson_type = get_lesson_type_from_extension(ext)

                    # Extract lesson title (remove extension and numbering)
                    lesson_title = os.path.splitext(lesson_file)[0]
                    # Clean up common prefixes like "1. ", "01 - ", etc.
                    lesson_title = TextFormatter.remove_numbering_prefix(lesson_title)

                    lesson = LessonData(
                        title=lesson_title,
                        lesson_type=lesson_type,
                        duration_seconds=0,  # TODO: Extract actual duration for media files
                        completed=False,  # TODO: Track completion status
                        file_path=lesson_path
                    )
                    lessons.append(lesson)

        except PermissionError:
            pass

        return lessons

    @staticmethod
    def scan_course_lessons(course_directory: str) -> List[LessonData]:
        """
        Scan course directory for lessons (files directly in the course root).

        Args:
            course_directory (str): Path to the course directory

        Returns:
            List[LessonData]: List of lessons found in the course root
        """
        lessons = []

        try:
            items = os.listdir(course_directory)
            lesson_files = []

            for item in items:
                item_path = os.path.join(course_directory, item)

                if ContentDetectionService._is_lesson_file(item_path):
                    lesson_files.append(item)

            # Sort lesson files using natural sort
            lesson_files.sort(key=natural_sort_key)

            for lesson_file in lesson_files:
                lesson_path = os.path.join(course_directory, lesson_file)

                # Determine lesson type based on file extension
                ext = os.path.splitext(lesson_file)[1]
                lesson_type = get_lesson_type_from_extension(ext)

                # Extract lesson title (remove extension and numbering)
                lesson_title = os.path.splitext(lesson_file)[0]
                # Clean up common prefixes like "1. ", "01 - ", etc.
                lesson_title = TextFormatter.remove_numbering_prefix(lesson_title)

                lesson = LessonData(
                    title=lesson_title,
                    lesson_type=lesson_type,
                    duration_seconds=0,  # TODO: Extract actual duration for media files
                    completed=False,  # TODO: Track completion status
                    file_path=lesson_path
                )
                lessons.append(lesson)

        except PermissionError:
            pass

        return lessons
