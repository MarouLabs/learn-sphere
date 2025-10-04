import os
from pathlib import Path


class PathValidator:
    """Utility class for validating and sanitizing file paths."""

    @staticmethod
    def validate_safe_path(user_input: str, base_path: str) -> str:
        """
        Validate that a user-provided path is safe and within the base directory.
        Prevents path traversal attacks.

        Args:
            user_input (str): The user-provided path component
            base_path (str): The base directory that the path must be within

        Returns:
            str: The validated absolute path

        Raises:
            ValueError: If the path attempts to escape the base directory
        """
        real_base = os.path.realpath(base_path)

        combined_path = os.path.join(base_path, user_input)
        real_path = os.path.realpath(combined_path)

        if not real_path.startswith(real_base):
            raise ValueError(f"Invalid path: attempting to access outside base directory")

        return real_path

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize a filename by removing potentially dangerous characters.

        Args:
            filename (str): The filename to sanitize

        Returns:
            str: Sanitized filename
        """
        dangerous_chars = ['..', '/', '\\', '\0']
        sanitized = filename
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        return sanitized
