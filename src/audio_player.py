import time  # Import time for sleep functionality
import yt_dlp  # Import yt_dlp for downloading YouTube audio
import vlc  # Import VLC for media playback
import os  # Import os for clearing the console
import re  # Import re for regular expression matching
from termcolor import colored  # Add termcolor import
from functools import lru_cache # Import lru_cache for caching


# Function to fetch the audio URL of a YouTube video
@lru_cache(maxsize=128) # Cache up to 128 most recent URLs
def get_audio_url(youtube_url):
    """
    Fetches the direct audio URL of a YouTube video.
    Uses lru_cache to store recently fetched URLs to improve performance on repeated requests.

    Args:
        youtube_url (str): The URL of the YouTube video.
    Returns:
        str: The direct audio URL, or None if fetching fails.
    """
    try:
        print(colored("\nFetching Audio...", "cyan"))
        print(colored("\nWait a second (Depend on your internet)...\n", "yellow"))
        # Options for yt_dlp to extract audio URL
        ydl_opts = {
            "format": "bestaudio/best",  # Fetch the best quality audio
            "quiet": True,  # Suppress verbose output
            "extract_flat": True,  # Extract metadata without downloading
        }
        # Extract audio stream URL
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            return info["url"]
    except yt_dlp.DownloadError as e:
        print(colored(f"Download error: {e}", "red"))
        print(colored("Check if the URL is valid and accessible.", "yellow"))
    except KeyError as e:
        print(colored(f"KeyError: Missing expected data in the response. {e}", "red"))
        print(
            colored(
                "Could not extract the audio URL. Please try again later.", "yellow"
            )
        )
    except Exception as e:
        print(colored(f"Failed to fetch audio URL. Error: {e}", "red"))
        print(colored("Wait for 2 seconds and try again...", "yellow"))
    time.sleep(2)
    return None


# Function to play a song with volume control
def play_song(song):
    """
    Plays a song from a given YouTube URL with volume control.
    Args:
        song (str): The YouTube URL of the song to play.
    """
    try:
        print(colored("\nStarting the audio...", "green"))
        url = get_audio_url(song)  # Fetch the audio URL
        if not url:
            print(colored("Could not fetch the audio URL. Aborting...", "red"))
            time.sleep(2)
            return
        player = vlc.MediaPlayer(url)  # Create a VLC media player instance
        player.play()  # Start playback

        # Set an initial volume level
        volume = 50
        player.audio_set_volume(volume)
        print(colored(f"Volume set to {volume}%.", "cyan"))

        # Infinite loop to handle user controls
        while True:
            print(
                colored("\nControls: ", "yellow")
                + colored("[P] Pause/Resume | ", "cyan")
                + colored("[R] Restart | ", "green")
                + colored("[Q] Quit | ", "red")
                + colored("[+] Increase Volume | ", "magenta")
                + colored("[-] Decrease Volume", "magenta")
            )
            command = input(colored("Enter command: ", "yellow")).strip().lower()

            if command == "p":  # Pause or resume the music
                if player.is_playing():
                    player.pause()
                    print(colored("Music paused.", "yellow"))
                else:
                    player.play()
                    print(colored("Music resumed.", "green"))
            elif command == "r":  # Restart the song
                player.stop()
                player.play()
                print(colored("Music restarted.", "green"))
            elif command == "+":  # Increase volume
                volume = min(100, volume + 10)  # Max volume is 100%
                player.audio_set_volume(volume)
                print(colored(f"Volume increased to {volume}%.", "cyan"))
            elif command == "-":  # Decrease volume
                volume = max(0, volume - 10)  # Min volume is 0%
                player.audio_set_volume(volume)
                print(colored(f"Volume decreased to {volume}%.", "cyan"))
            elif command == "q":  # Quit the player and return to the main menu
                player.stop()
                print(colored("Exiting player.", "red"))
                break
            else:
                # Handle invalid commands
                print("Invalid command. Try again.")
    except vlc.MediaPlayerError as e:
        print(colored(f"VLC MediaPlayer error: {e}", "red"))
        print(
            colored(
                "Could not initialize the media player. Please check the installation and dependencies.",
                "yellow",
            )
        )
    except Exception as e:
        print(colored(f"Some error occurred while playing the song. Error: {e}", "red"))
        print(colored("Wait for 2 seconds and try again...", "yellow"))


# Function to display a list of pre-defined songs and allow selection
def list_of_songs():
    songs = [
        "https://youtu.be/kyjg5kX4pT0?si=QKSHUocD6HVORbBW",
        "https://youtu.be/XO8wew38VM8?si=9qG5id8bC5f-Mxaq",
        "https://youtu.be/VCNLZflKQ7o?si=mCTy9U26-TU0X3lA",
    ]
    while True:
        try:
            os.system("cls")  # Clear the screen
            print("\n" + "_" * 30)
            print("\nList of songs:")
            print("\n1. Dil Tu Jaan Tu by Gurnazar Ft. Kritika Yadav")
            print("2. Millionaire by YoYo Honey Singh")
            print("3. Tere Hawaale by Arijit Singh")
            print("4. Exit")
            choice = int(input(colored("\nEnter your choice: ", "yellow")))
            if choice == 1:
                play_song(songs[0])  # Play the first song
            elif choice == 2:
                play_song(songs[1])  # Play the second song
            elif choice == 3:
                play_song(songs[2])  # Play the third song
            elif choice == 4:
                # Exit the list and return to the main menu
                print("\nThanks for using my music player!")
                break
            else:
                # Handle invalid menu choices
                print(
                    colored("\nInvalid choice... Please choose from the list.", "red")
                )
                time.sleep(2)
        except ValueError:
            print(colored("Invalid input. Please enter a number.", "red"))
            time.sleep(2)
        except Exception as e:
            print(colored(f"Unexpected error: {e}", "red"))
            time.sleep(2)


# Function to play a song
def input_url_for_audio():
    while True:
        try:
            url = input(
                colored("\nEnter the song URL (or 'exit' to go back): ", "yellow")
            ).strip()
            if url.lower() == "exit":
                break
            elif is_youtube_url(url):
                play_song(url)
            else:
                print(colored("Invalid URL. Please enter a valid YouTube URL.", "red"))
                time.sleep(1)
        except ValueError:
            print(colored("Invalid input. Please enter a valid song URL.", "red"))
            time.sleep(1)


def is_youtube_url(url):
    youtube_pattern1 = r"^https?://(?:www\.)?(?:youtube\.com|youtu\.be)/.*$"
    youtube_pattern2 = r"^https?://(www\.)?youtube\.com/playlist\?list=.*$"
    youtube_pattern = youtube_pattern1 + "|" + youtube_pattern2
    return bool(re.match(youtube_pattern, url))


# Main function to display the main menu and handle user choices
def main():
    while True:
        try:
            os.system("cls")  # Clear the screen
            print("\n" + "_" * 30)
            print("\n         Welcome to my music player!")
            print("\n1. Wanna play my list of songs?")
            print("2. Wanna play your own song?")
            print("3. Exit")
            choice = int(input(colored("\nEnter your choice: ", "yellow")))
            if choice == 1:
                list_of_songs()  # Show the list of pre-defined songs
            elif choice == 2:
                os.system("cls")  # Clear the screen
                input_url_for_audio()  # Play the user's custom song
            elif choice == 3:
                # Exit the program
                print(
                    f"\nThanks for using my music player! Have a nice day! {chr(0x1F642)}"
                )
                break
            else:
                # Handle invalid menu choices
                print(
                    colored(
                        "\nInvalid choice... Please choose from the options.", "red"
                    )
                )
                time.sleep(2)
        except ValueError:
            # Handle invalid input when the user enters something that's not a number
            print(colored("Invalid input. Please enter a valid number.", "red"))
            time.sleep(2)
        except Exception as e:
            print(colored(f"Unexpected error: {e}", "red"))
            time.sleep(2)


# Entry point of the program
if __name__ == "__main__":
    main()
