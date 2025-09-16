import time
import qrcode
import os
import requests
from functools import lru_cache
from audio_player import is_youtube_url
from termcolor import colored
from utils import clear_screen


@lru_cache(maxsize=128)
def terminal_color(color, is_background=False, style=None):
    """
    Maps color names and styles to ANSI escape codes for terminal output.

    This function provides a comprehensive color mapping system for terminal
    text styling, supporting both foreground and background colors with optional
    text styles. Results are cached for improved performance in QR code generation.

    Args:
        color (str): The name of the color. Supported colors:
            - Basic: "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"
            - Special: "reset" (resets all formatting)
        is_background (bool, optional): If True, applies color to background.
            Defaults to False (foreground).
        style (str, optional): Text style modifier. Supported styles:
            - "bold": Makes text bold
            - "underline": Underlines text

    Returns:
        str: ANSI escape code sequence for the specified color and style.

    Examples:
        >>> terminal_color("red")
        '\\x1b[31m'
        >>> terminal_color("blue", is_background=True)
        '\\x1b[44m'
        >>> terminal_color("green", style="bold")
        '\\x1b[1;32m'
    """
    codes = []

    # Add style codes
    if style == "bold":
        codes.append("1")
    elif style == "underline":
        codes.append("4")

    # Add color code
    color_map = {
        "black": 40 if is_background else 30,
        "red": 41 if is_background else 31,
        "green": 42 if is_background else 32,
        "yellow": 43 if is_background else 33,
        "blue": 44 if is_background else 34,
        "magenta": 45 if is_background else 35,
        "cyan": 46 if is_background else 36,
        "white": 47 if is_background else 37,
        "reset": 0,
    }
    codes.append(str(color_map.get(color.lower(), 0)))

    return f"\033[{';'.join(codes)}m"


@lru_cache(maxsize=32)
def fetch_random_joke():
    """
    Fetches a random joke from the icanhazdadjoke.com API.
    Results are cached to avoid repeated API calls.

    Returns:
        str: A random joke, or a default joke if fetching fails.
    """
    try:
        headers = {"Accept": "application/json"}
        response = requests.get("https://icanhazdadjoke.com/", headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("joke", "No joke found.")
    except requests.RequestException as e:
        print(f"An error occurred while fetching the joke: {e}")
        return "Why don't scientists trust atoms? Because they make up everything!"


def generate_qr_terminal(
    data, box_size=1, border=1, fill_color="black", back_color="white"
):
    """
    Generates and displays a QR code in the terminal.

    Args:
        data (str): The data to encode in the QR code.
        box_size (int): The size of each box (pixel) in the QR code.
        border (int): The thickness of the border around the QR code.
        fill_color (str): The fill color for the QR code (e.g., "black", "blue").
        back_color (str): The background color for the QR code (e.g., "white", "yellow").

    Returns:
        qrcode.QRCode: The QRCode object if successful, None otherwise.
    """
    clear_screen()
    try:
        qr = qrcode.QRCode(
            version=None,  # Auto-select optimal version
            error_correction=qrcode.constants.ERROR_CORRECT_M,  # Better balance of size/speed
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Pre-compute color codes for better performance
        fill_color_code = terminal_color(fill_color)
        back_color_code = terminal_color(back_color, is_background=True)
        reset_code = terminal_color("reset")

        print(f"{fill_color_code}")
        print(f"{back_color_code}")

        # Build the QR matrix display more efficiently
        matrix = qr.get_matrix()
        for row in matrix:
            for col in row:
                if col:
                    print(f"{fill_color_code}██{reset_code}", end="")
                else:
                    print(f"{back_color_code}  {reset_code}", end="")
            print()

        print(
            colored(
                "\nQR Code successfully displayed in the terminal. (If terminal QR is not working try after saving)",
                "green",
            )
        )
        return qr
    except Exception as e:
        print(colored(f"An error occurred while generating the QR code: {e}", "red"))
        return None


def save_qr_code(qr, data, fill_color="black", back_color="white"):
    """
    Saves the generated QR code as a PNG image file.

    Args:
        qr (qrcode.QRCode): The QRCode object to save.
        data (str): The data encoded in the QR code, used for filename generation.
        fill_color (str): The fill color of the QR code image.
        back_color (str): The background color of the QR code image.
    """
    try:
        folder_name = "qr_codes"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        filename = f"{folder_name}/{data.replace(' ', '_').replace('/', '_')[:50]}.png"
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(filename)

        print(colored(f"QR Code saved as {filename}", "green"))
    except Exception as e:
        print(colored(f"An error occurred while saving the QR code: {e}", "red"))


def input_qr_url():
    """
    Prompts the user to enter a URL for QR code generation and validates it.

    Returns:
        str: The validated URL, or None if the URL is invalid or empty.
    """
    url = input(colored("\nEnter the url for the QR Code: ", "cyan")).strip()
    if not url:
        print(colored("Input cannot be empty.", "red"))
        time.sleep(1)
        return None
    if is_youtube_url(url):
        return url
    else:
        print(colored("Invalid URL. Please enter a valid YouTube URL.", "red"))
        time.sleep(1)
        return None


def default_qr(data):
    """
    Generates and optionally saves a QR code with default settings.

    Args:
        data (str): The data to encode in the QR code.
    """
    try:
        clear_screen()
        print(colored("\n--------------------------------\n", "yellow"))
        print(colored("Generating QR code with default settings...", "cyan"))
        qr = generate_qr_terminal(data)

        if qr:
            save_option = (
                input(
                    colored(
                        "Do you want to save this QR code as an image file? (yes/no): ",
                        "yellow",
                    )
                )
                .strip()
                .lower()
            )
            if save_option == "yes":
                save_qr_code(qr, data)
            else:
                print(colored("QR code not saved.", "red"))
    except Exception as e:
        print(colored(f"An error occurred: {e}", "red"))


def custom_qr(data):
    """
    Generates and optionally saves a QR code with custom fill and background colors.

    Args:
        data (str): The data to encode in the QR code.
    """
    try:
        clear_screen()
        print(colored("\n--------------------------------\n", "yellow"))
        print(colored("Custom QR Code Settings:", "cyan"))
        print("Available colors:")
        print(
            colored("black", "black"),
            colored("red", "red"),
            colored("green", "green"),
            colored("yellow", "yellow"),
            colored("blue", "blue"),
            colored("magenta", "magenta"),
            colored("cyan", "cyan"),
            colored("white", "white"),
        )
        fill_color = (
            input(colored("Enter fill color (default is black): ", "cyan")).strip()
            or "black"
        )
        back_color = (
            input(
                colored("Enter background color (default is white): ", "cyan")
            ).strip()
            or "white"
        )
        clear_screen()
        print(colored("\nGenerating QR code with custom settings...", "cyan"))
        qr = generate_qr_terminal(
            data, box_size=1, border=1, fill_color=fill_color, back_color=back_color
        )

        if qr:
            save_option = (
                input(
                    colored(
                        "Do you want to save this QR code as an image file? (yes/no): ",
                        "yellow",
                    )
                )
                .strip()
                .lower()
            )
            if save_option == "yes":
                save_qr_code(qr, data, fill_color, back_color)
            else:
                print(colored("QR code not saved.", "red"))
    except ValueError as ve:
        print(colored(f"Error: {ve}", "red"))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def joke_qr():
    """
    Fetches a random joke, generates a QR code for it, and optionally saves it.
    """
    try:
        clear_screen()
        random_joke = fetch_random_joke()
        qr = generate_qr_terminal(random_joke)

        if qr:
            save_option = (
                input(
                    colored(
                        "Do you want to save this QR code as an image file? (yes/no): ",
                        "yellow",
                    )
                )
                .strip()
                .lower()
            )
            if save_option == "yes":
                save_qr_code(qr, random_joke)
            else:
                print(colored("QR code not saved.", "red"))
    except Exception as e:
        print(colored(f"An error occurred: {e}", "red"))


def qr_menu():
    """
    Displays the QR code generation menu and handles user choices.
    """
    while True:
        print(colored("\n--------------------------------\n", "yellow"))
        print(colored("QR Menu:", "cyan"))
        print(colored("1. Generate QR Code with Default Settings", "cyan"))
        print(colored("2. Generate QR Code with Custom Settings", "cyan"))
        print(colored("3. Tell me a joke...", "cyan"))
        print(colored("4. Exit", "yellow"))

        choice = input(colored("Please select an option: ", "green")).strip()

        if choice == "1":
            data = input_qr_url()
            if data is not None:
                default_qr(data)

        elif choice == "2":
            data = input_qr_url()
            if data is not None:
                custom_qr(data)

        elif choice == "3":
            joke_qr()

        elif choice == "4":
            break

        else:
            print(colored("Invalid choice... Try again", "red"))
            time.sleep(1)
