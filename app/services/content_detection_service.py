import os
from typing import List, Set
from app.models.course_model import NodeType


class ContentDetectionService:
    """Service to detect the type of content in directories (Course, Module, Directory)."""
    
    # Common image file extensions
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'}
    
    # Common lesson file extensions
    LESSON_EXTENSIONS = {
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', # Video
        '.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a',         # Audio
        '.pdf', '.doc', '.docx', '.txt', '.md', '.html', '.htm', # Documents
    }
    
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
    def _has_lesson_files(files: List[str]) -> bool:
        """Check if the files list contains lesson-type files."""
        for file in files:
            _, ext = os.path.splitext(file.lower())
            if ext in ContentDetectionService.LESSON_EXTENSIONS:
                return True
        return False
    
    @staticmethod
    def _is_course_structure(directory_path: str, directories: List[str], files: List[str]) -> bool:
        """
        Check if the directory structure matches a course pattern.
        Course: Contains modules (directories with only files) and/or lesson files.
        """
        has_modules = False
        has_lesson_files = ContentDetectionService._has_lesson_files(files)
        
        # Check if subdirectories are modules (contain only files, no subdirectories)
        for subdir_path in directories:
            try:
                subdir_items = os.listdir(subdir_path)
                subdir_directories = []
                subdir_files = []
                
                for item in subdir_items:
                    if item.startswith('.'):
                        continue
                        
                    item_path = os.path.join(subdir_path, item)
                    if os.path.isdir(item_path):
                        subdir_directories.append(item)
                    else:
                        subdir_files.append(item)
                
                # If subdirectory has no directories and has lesson files, it's a module
                if not subdir_directories and ContentDetectionService._has_lesson_files(subdir_files):
                    has_modules = True
                elif subdir_directories:
                    # If subdirectory has other directories, this is likely a directory of courses
                    return False
                    
            except PermissionError:
                continue
        
        # It's a course if it has modules or lesson files at the root
        return has_modules or has_lesson_files
    
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
        Calculate progress for a course/module (placeholder implementation).
        
        Args:
            directory_path (str): Path to calculate progress for
            
        Returns:
            float: Progress percentage (0.0 to 100.0)
        """
        # TODO: Implement actual progress calculation based on completion tracking
        # For now, return a random-ish value based on directory name
        import hashlib
        hash_value = int(hashlib.md5(directory_path.encode()).hexdigest()[:8], 16)
        return (hash_value % 101)  # 0-100
