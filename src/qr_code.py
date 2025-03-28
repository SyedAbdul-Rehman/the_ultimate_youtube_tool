import time
import qrcode  # Import the qrcode library for generating QR codes
import os  # Import os for file and directory operations
import requests  # Import requests for making HTTP requests
from audio_player import is_youtube_url
  # Import the is_youtube_url function from audio_player.py
from termcolor import colored  # Import the colored function from termcolor for colored text output


def terminal_color(color, is_background=False):
    # Map color names to ANSI escape codes for terminal output
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
    # Return the ANSI escape code for the specified color
    return f"\033[{color_map.get(color.lower(), 0)}m"


def fetch_random_joke():
    try:
        # Set headers to accept JSON response
        headers = {"Accept": "application/json"}
        # Make a GET request to fetch a random joke
        response = requests.get("https://icanhazdadjoke.com/", headers=headers)
        # Raise an error if the response status is not OK
        response.raise_for_status()
        # Parse the JSON response
        data = response.json()
        # Return the joke from the response data
        return data.get("joke", "No joke found.")
    except requests.RequestException as e:
        # Print an error message if the request fails
        print(f"An error occurred while fetching the joke: {e}")
        # Return a default joke in case of an error
        return "Why don't scientists trust atoms? Because they make up everything!"


def generate_qr_terminal(
    data, box_size=1, border=1, fill_color="black", back_color="white"
):
    # Clear the terminal screen
    os.system("cls" if os.name == "nt" else "clear")
    try:
        # Create a QRCode object with specified settings
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )
        # Add data to the QR code
        qr.add_data(data)
        # Optimize the QR code size
        qr.make(fit=True)
        # Get terminal color codes for fill and background
        fill_color_code = terminal_color(fill_color)
        back_color_code = terminal_color(back_color, is_background=True)
        print(f"{fill_color_code}")
        print(f"{back_color_code}")
        # Iterate over the QR code matrix to print it in the terminal
        for row in qr.get_matrix():
            for col in row:
                if col:
                    # Print filled cells with the specified fill color
                    print(f"{fill_color_code}██{terminal_color('reset')}", end="")
                else:
                    # Print empty cells with the specified background color
                    print(f"{back_color_code}  {terminal_color('reset')}", end="")
            print()  # New line after each row

        # Indicate successful QR code generation
        print(
            colored(
                "\nQR Code successfully displayed in the terminal. (If terminal QR is not working try after saving)",
                "green",
            )
        )
        return qr  # Return the QRCode object
    except Exception as e:
        # Print an error message if QR code generation fails
        print(colored(f"An error occurred while generating the QR code: {e}", "red"))
        return None


def save_qr_code(qr, data, fill_color="black", back_color="white"):
    try:
        # Define the folder name for saving QR codes
        folder_name = "qr_codes"
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Create a valid filename by replacing spaces and slashes
        filename = f"{folder_name}/{data.replace(' ', '_').replace('/', '_')[:50]}.png"
        # Generate an image from the QRCode object
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        # Save the image to the specified filename
        img.save(filename)

        # Indicate successful saving of the QR code
        print(colored(f"QR Code saved as {filename}", "green"))
    except Exception as e:
        print(colored(f"An error occurred while saving the QR code: {e}", "red"))


def input_qr_url():
    url = input(colored("\nEnter the url for the QR Code: ", "cyan")).strip()
    if not url:
        raise ValueError("Input cannot be empty.")
    if __name__ == "__main__":
        return url
    elif is_youtube_url(url):
        return url
    else:
        print(colored("Invalid URL. Please enter a valid YouTube URL.", "red"))
        time.sleep(1)


def default_qr(data):
    try:
        os.system("cls" if os.name == "nt" else "clear")
        # Prompt the user for data to encode in the QR code
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
    try:
        # Prompt the user for data to encode in the QR code
        os.system("cls" if os.name == "nt" else "clear")
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
        os.system("cls" if os.name == "nt" else "clear")
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
    try:
        os.system("cls" if os.name == "nt" else "clear")
        # Fetch a random joke and generate a QR code for it
        random_joke = fetch_random_joke()
        qr = generate_qr_terminal(random_joke)

        if qr:
            # Ask the user if they want to save the QR code
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
        # Print an error message if an exception occurs
        print(colored(f"An error occurred: {e}", "red"))


def qr_menu():
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
            # Exit the program
            break

        else:
            # Print an error message for invalid menu choices
            print(colored("Invalid choice... Try again", "red"))
            time.sleep(1)


def main():
    print(
        colored(
            "Welcome to the Terminal QR Code Generator! (Suggestion: Open terminal in full screen)",
            "green",
        )
    )
    print(colored("\n" + "_" * 30, "cyan"))
    qr_menu()


if __name__ == "__main__":
    # Run the main function if the script is executed directly
    main()
