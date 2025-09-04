"""
Utility functions used across the application.
"""
import os
from termcolor import colored


def clear_screen():
    """
    Clears the terminal screen in a cross-platform way.
    """
    os.system("cls" if os.name == "nt" else "clear")


def print_colored(text, color="white", attrs=None):
    """
    Wrapper for colored print to ensure consistent usage.

    Args:
        text (str): Text to print
        color (str): Color name
        attrs (list): List of attributes like ['bold']
    """
    print(colored(text, color, attrs=attrs))


def get_user_input(prompt, color="yellow"):
    """
    Gets user input with colored prompt.

    Args:
        prompt (str): The prompt text
        color (str): Color for the prompt

    Returns:
        str: User input
    """
    return input(colored(prompt, color))


def validate_input_not_empty(value, error_message="Input cannot be empty."):
    """
    Validates that input is not empty.

    Args:
        value (str): Input value
        error_message (str): Error message to display

    Returns:
        bool: True if valid, False otherwise
    """
    if not value.strip():
        print_colored(error_message, "red")
        return False
    return True
