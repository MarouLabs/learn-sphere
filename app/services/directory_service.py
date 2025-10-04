import os
from typing import List, Optional
from app.models.course_model import Course, NodeType
from app.services.content_detection_service import ContentDetectionService
from app.services.registry_service import RegistryService
from app.utils.text_formatter import TextFormatter


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
        registry_service = RegistryService()
        
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
                    
                    # Detect content type first to determine registry section
                    content_type = ContentDetectionService.detect_content_type(item_path) if force_analysis else None

                    # If not forcing analysis, try to get from registry first
                    if not force_analysis:
                        # We need to try both sections since we don't know the type yet
                        registry_entry = None
                        for node_type in [NodeType.DIRECTORY, NodeType.COURSE]:
                            entry = registry_service.get_registry_entry(formatted_title, item_path, node_type)
                            if entry:
                                registry_entry = entry
                                content_type = NodeType(entry["node_type"])
                                break
                    else:
                        registry_entry = None
                    
                    if registry_entry and not force_analysis:
                        print(f"Found in registry: {formatted_title} - skipping deep analysis")

                        registry_service.update_last_accessed(formatted_title, item_path, content_type)

                        node_type = content_type

                        image_absolute_path = ContentDetectionService.find_course_image(item_path)
                        image_url = DirectoryService._convert_image_path_to_url(image_absolute_path, item, node_type)
                        progress_percent = ContentDetectionService.calculate_progress(item_path)

                        course = Course(
                            id=item,
                            title=formatted_title,
                            node_type=node_type,
                            path=item_path,
                            image_path=image_url
                        )
                        course.progress.progress_percent = progress_percent
                        
                    else:
                        print(f"Not in registry: {formatted_title} - performing deep analysis")

                        if content_type is None:
                            content_type = ContentDetectionService.detect_content_type(item_path)

                        image_absolute_path = ContentDetectionService.find_course_image(item_path)
                        image_url = DirectoryService._convert_image_path_to_url(image_absolute_path, item, content_type)
                        progress_percent = ContentDetectionService.calculate_progress(item_path)

                        course = Course(
                            id=item,
                            title=formatted_title,
                            node_type=content_type,
                            path=item_path,
                            image_path=image_url
                        )
                        course.progress.progress_percent = progress_percent

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
        return TextFormatter.format_directory_title(directory_name)
    
    @staticmethod
    def _convert_image_path_to_url(absolute_image_path: str, item_id: str, node_type: NodeType) -> Optional[str]:
        """
        Convert absolute filesystem image path to web-accessible URL.

        Args:
            absolute_image_path: Absolute path to the image file
            item_id: The course or directory ID
            node_type: Type of the node (course or directory)

        Returns:
            Web-accessible URL or None if no image
        """
        if not absolute_image_path:
            return None

        filename = os.path.basename(absolute_image_path)

        if node_type == NodeType.DIRECTORY:
            return f"/media/directory/{item_id}/{filename}"
        else:
            return f"/media/course/{item_id}/{filename}"

    @staticmethod
    def validate_directory_exists(directory_path: str) -> bool:
        """
        Validate that a directory exists.

        Args:
            directory_path (str): The absolute path to the directory

        Returns:
            bool: True if directory exists, False otherwise
        """
        return os.path.exists(directory_path) and os.path.isdir(directory_path)

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
