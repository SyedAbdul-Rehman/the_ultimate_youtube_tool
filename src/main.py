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
import authentication as auth
from colorama import init
init()
os.system('color')

def check_internet_connection():
    try:
        create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def handle_authentication():
    while True:
        print(colored("\n--------------------------------\n", "yellow"))
        print(colored("1. Login", "green"))
        print(colored("2. Sign-up", "green"))
        print(colored("3. Stop Automatic Logic", "green"))
        print(colored("4. Exit", "green"))
        choice = input(colored("Enter your choice: ", "yellow"))

        if choice == "1":
            result = auth.login()
            if result:
                break
        elif choice == "2":
            auth.signup()
        elif choice == "3":
            auth.logout()
        elif choice == "4":
            print(colored("Thank you for using The Ultimate Youtube Tool.", "blue"))
            os.system("pause")
            sys.exit()
        else:
            print(colored("Invalid choice. Please choose again.", "red"))
            
def song_menu():
    try:
        while True:
            print(colored("\n--------------------------------\n", "yellow"))
            print(colored("1. Sved Songs", "green"))
            print(colored("2. Play a Song from YouTube", "green"))
            print(colored("3. Exit", "green"))
            song_choice = input(colored("Enter your choice: ", "yellow"))
            if song_choice == "1":
                music_library()
            elif song_choice == "2":
                try:
                    input_url_for_audio()
                except Exception as e:
                    print(colored(e, "red"))
            elif song_choice == "3":
                break
            else:
                print(colored("Invalid choice", "red"))
    except Exception as e:
        print(colored(e, "red"))


def main():
    text = "The Ultimate Youtube Tool"
    ascii_art = pyfiglet.figlet_format(text, font="standard")
    print(colored(ascii_art, "red"))
    print(colored("By: @SyedAbdul-Rehman", "cyan"), end="              ")
    status = "● Online" if check_internet_connection() else "● Offline"
    status_color = "green" if check_internet_connection() else "red"
    print(colored(f"Status: {status}", status_color))
    print(colored("Version: 1.0.0", "green"))
    
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
        while True:
            print(colored("--------------------------------\n", "yellow"))
            print(colored("Select an option:", "yellow"))
            print(colored("1. Song/Audio Player", "green"))
            print(colored("2. Video/Audio Downloader", "green"))
            print(colored("3. Youtuebe QR Code Generator", "green"))
            print(colored("4. Block or Unblock YouTube", "green"))
            print(colored("5. Exit", "green"))
            choice = input(colored("Enter your choice: ", "yellow"))
            if choice == "1":
                song_menu()
            elif choice == "2":
                input_url_for_video()
            elif choice == "3":
                qr()
            elif choice == "4":
                yt_access()
            elif choice == "5":
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
