import hashlib
import random
from app.models.course_model import Course


class ColorService:
    """Service to handle color generation logic only - no persistence."""
    
    # Predefined color palette
    COLORS_PALETTE = [
        "#803fa5",  # Purple
        "#943d73",  # Pink
        "#ae2e24",  # Red
        "#9e4c00",  # Orange
        "#7f5f01",  # Yellow Mustard
        "#4c6b1f",  # Green
        "#2d7d32",  # Green Cyan
        "#206a83",  # Cyan
        "#1976d2",  # Blue
    ]
    
    @staticmethod
    def generate_random_color(title: str) -> str:
        """Generate a random color from the palette."""
        return random.choice(ColorService.COLORS_PALETTE)
    
    @staticmethod
    def get_color_for_course(course: Course) -> str:
        """Get color for a course based on its title."""
        return ColorService.generate_random_color(course.title)
    
    @staticmethod
    def get_available_colors() -> list:
        """Get the list of available colors in the palette."""
        return ColorService.COLORS_PALETTE.copy()