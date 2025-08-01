import os
import sys
import pyfiglet
from socket import create_connection
from termcolor import colored
from song_save import music_library 
from audio_player import input_url_for_audio
from video_downloader import input_url_for_video
from qr_code import qr_menu as qr
from yt_access_control import yt_access_menu as yt_access
from colorama import init
init()
os.system('color')

def check_internet_connection():
    """
    Checks for an active internet connection by attempting to connect to Google's DNS server.
    Returns:
        bool: True if connected, False otherwise.
    """
    try:
        # Attempt to create a connection to a known reliable host (Google's DNS server)
        create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        # If connection fails, an OSError is raised
        return False

def song_menu():
    """
    Displays the song player menu and handles user choices for playing saved songs
    or a new song from YouTube.
    """
    try:
        while True:
            print(colored("\n--------------------------------\n", "yellow"))
            print(colored("1. Saved Songs", "green"))
            print(colored("2. Play a Song from YouTube", "green"))
            print(colored("3. Exit", "green"))
            song_choice = input(colored("Enter your choice: ", "yellow"))
            if song_choice == "1":
                # Navigate to the music library to manage and play saved songs
                music_library()
            elif song_choice == "2":
                # Prompt user for a YouTube URL to play audio
                try:
                    input_url_for_audio()
                except Exception as e:
                    print(colored(e, "red"))
            elif song_choice == "3":
                # Exit the song menu
                break
            else:
                print(colored("Invalid choice", "red"))
    except Exception as e:
        print(colored(e, "red"))


def main():
    """
    Main function of the application. Displays the welcome banner, checks internet
    connection, and presents the main menu for various YouTube-related tools.
    """
    # Display application title using pyfiglet
    text = "The Ultimate Youtube Tool"
    ascii_art = pyfiglet.figlet_format(text, font="standard")
    print(colored(ascii_art, "red"))
    print(colored("By: @SyedAbdul-Rehman", "cyan"), end="              ")
    
    # Check and display internet connection status
    status = "● Online" if check_internet_connection() else "● Offline"
    status_color = "green" if check_internet_connection() else "red"
    print(colored(f"Status: {status}", status_color))
    print(colored("Version: 1.0.0", "green"))
    
    # Exit if no internet connection is detected
    if not check_internet_connection():
        print(
            colored(
                "No internet connection. Make sure you're conected with internet and then try again...",
                "red",
            )
        )
        os.system("pause")
        sys.exit()

    try:
        # Main application loop
        while True:
            print(colored("--------------------------------\n", "yellow"))
            print(colored("Select an option:", "yellow"))
            print(colored("1. Song/Audio Player", "green"))
            print(colored("2. Video/Audio Downloader", "green"))
            print(colored("3. YouTube QR Code Generator", "green"))
            print(colored("4. Block or Unblock YouTube", "green"))
            print(colored("5. Exit", "green"))
            choice = input(colored("Enter your choice: ", "yellow"))
            if choice == "1":
                # Open the song/audio player menu
                song_menu()
            elif choice == "2":
                # Open the video/audio downloader
                input_url_for_video()
            elif choice == "3":
                # Open the YouTube QR Code Generator
                qr()
            elif choice == "4":
                # Open the YouTube access control menu
                yt_access()
            elif choice == "5":
                # Exit the application
                print(colored("Thank you for using The Ultimate Youtube Tool.", "blue"))
                os.system("pause")
                sys.exit()
            else:
                print(colored("Invalid choice. Please choose again.", "red"))
    except KeyboardInterrupt:
        print(colored("\nProgram stopped by user.", "yellow"))
        os.system("pause")
    except Exception as e:
        print(colored(e, "red"))


if __name__ == "__main__":
    main()
