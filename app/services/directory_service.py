import os
from typing import List
from app.models.course_model import Course, NodeType, CourseMetadata
from app.services.content_detection_service import ContentDetectionService
from app.services.directory_registry_service import DirectoryRegistryService


class DirectoryService:
    @staticmethod
    def scan_directory(directory_path: str, force_analysis: bool = False) -> List[Course]:
        """
        Scan a directory and return a list of courses/directories.
        
        Args:
            directory_path (str): The absolute path to the directory to scan
            force_analysis (bool): If True, perform deep analysis even if item is in registry
            
        Returns:
            List[Course]: List of courses and directories found
        """
        courses = []
        registry_service = DirectoryRegistryService()
        
        if not os.path.exists(directory_path):
            return courses
            
        try:
            # Get all items in the directory
            items = os.listdir(directory_path)
            
            for item in items:
                item_path = os.path.join(directory_path, item)
                
                # Skip hidden files and directories
                if item.startswith('.'):
                    continue
                    
                # Only include directories (courses/directories)
                if os.path.isdir(item_path):
                    # Format title
                    formatted_title = DirectoryService._format_title(item)
                    
                    # Check if item is already in registry (unless force_analysis is True)
                    registry_entry = registry_service.get_registry_entry(formatted_title, item_path)
                    
                    if registry_entry and not force_analysis:
                        # Item exists in registry - skip deep analysis and use cached data
                        print(f"Found in registry: {formatted_title} - skipping deep analysis")
                        
                        # Update last accessed timestamp
                        registry_service.update_last_accessed(formatted_title, item_path)
                        
                        # Create course from registry data
                        node_type = NodeType(registry_entry["node_type"])
                        
                        # Still need to check for image and calculate progress for now
                        # TODO: consider if it's worth to cache these in the registry
                        image_path = ContentDetectionService.find_course_image(item_path)
                        progress_percent = ContentDetectionService.calculate_progress(item_path)
                        
                        metadata = CourseMetadata(
                            image=image_path if image_path else None
                        )
                        
                        course = Course(
                            id=item,
                            title=formatted_title,
                            node_type=node_type,
                            path=item_path
                        )
                        course.metadata = metadata
                        course.progress.progress_percent = progress_percent
                        
                    else:
                        # Item not in registry - perform full analysis
                        print(f"Not in registry: {formatted_title} - performing deep analysis")
                        
                        # Detect content type (deep analysis)
                        content_type = ContentDetectionService.detect_content_type(item_path)
                        
                        # Find course image
                        image_path = ContentDetectionService.find_course_image(item_path)
                        
                        # Calculate progress
                        progress_percent = ContentDetectionService.calculate_progress(item_path)
                        
                        # Create metadata
                        metadata = CourseMetadata(
                            image=image_path if image_path else None
                        )
                        
                        course = Course(
                            id=item,
                            title=formatted_title,
                            node_type=content_type,
                            path=item_path
                        )
                        course.metadata = metadata
                        course.progress.progress_percent = progress_percent
                        
                        # Register the item in the registry for future use (color is automatically generated)
                        registry_service.register_item(formatted_title, item_path, content_type)
                    
                    courses.append(course)
                    
        except PermissionError:
            # Handle permission errors gracefully
            pass
            
        # Sort courses alphabetically by title
        courses.sort(key=lambda x: x.title.lower())
        
        return courses
    
    @staticmethod
    def _format_title(directory_name: str) -> str:
        """
        Format directory name into a readable title.
        
        Args:
            directory_name (str): The directory name
            
        Returns:
            str: Formatted title
        """
        # Replace underscores and hyphens with spaces
        title = directory_name.replace('_', ' ').replace('-', ' ')
        
        # Capitalize each word
        title = ' '.join(word.capitalize() for word in title.split())
        
        return title
    
    @staticmethod
    def force_analyze_directory(directory_path: str) -> List[Course]:
        """
        Force deep analysis of a directory, ignoring registry cache.
        
        Args:
            directory_path (str): The absolute path to the directory to scan
            
        Returns:
            List[Course]: List of courses and directories found with fresh analysis
        """
        print(f"Force analyzing directory: {directory_path}")
        return DirectoryService.scan_directory(directory_path, force_analysis=True)
