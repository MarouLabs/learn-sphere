import re


class TextFormatter:
    """Utility class for text formatting operations."""

    @staticmethod
    def remove_numbering_prefix(text: str) -> str:
        """
        Remove numbering prefix from text (e.g., '1. ', '01 - ', '001_').

        Args:
            text (str): The text to process

        Returns:
            str: The text without numbering prefix
        """
        return re.sub(r'^\d+[\.\-\s_]*', '', text).strip()

    @staticmethod
    def format_directory_title(directory_name: str) -> str:
        """
        Format directory name into a readable title.

        Args:
            directory_name (str): The directory name

        Returns:
            str: Formatted title
        """
        title = directory_name.replace('_', ' ').replace('-', ' ')
        title = ' '.join(word.capitalize() for word in title.split())
        return title
