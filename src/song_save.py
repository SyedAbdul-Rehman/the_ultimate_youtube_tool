import json
import audio_player as ap
from termcolor import colored


def get_songs():
    try:
        with open("songs.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_song():
    user_data = []
    try:
        with open("songs.json", "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        pass

    name = input(colored("Enter name of song: ", "green"))
    url = input(colored("Enter url of song: ", "green"))
    if name == "" or url == "":
        print(colored("Enter a Valid Name and URL..", "red"))
        return
    if ap.is_youtube_url(url):
        song = {"name": name, "url": url}
        user_data.append(song)
        with open("songs.json", "w") as f:
            json.dump(user_data, f, indent=4)
            print(colored("Song saved successfully!", "blue"))
    else:
        print(colored("Enter a Valid Youtube URL..", "red"))


def view_songs():
    try:
        with open("songs.json", "r") as file:
            songs = json.load(file)
            print(colored("Saved Songs:", "red"))
            for i, song in enumerate(songs, start=1):
                print(colored(f"{i}. {song['name']}", "cyan"))
    except FileNotFoundError:
        print(colored("No songs saved yet.", "yellow"))


def remove_song():
    """
    Removes a selected song from the saved songs list in 'songs.json'.
    """
    try:
        songs = get_songs()
        if not songs:
            print(colored("No songs saved yet to remove.", "yellow"))
            return

        print(colored("Saved Songs:", "red"))
        for i, song in enumerate(songs, start=1):
            print(colored(f"{i}. {song['name']}", "cyan"))

        song_number = int(
            input(colored("Enter the number of the song to remove: ", "green"))
        )
        if 1 <= song_number <= len(songs):
            del songs[song_number - 1]
            with open("songs.json", "w") as f:
                json.dump(songs, f, indent=4)
            print(colored("Song removed successfully!", "blue"))
        else:
            print(colored("Invalid song number", "red"))
    except ValueError:
        print(colored("Invalid input. Please enter a number.", "red"))
    except FileNotFoundError:
        print(colored("No songs saved yet.", "yellow"))
    except Exception as e:
        print(colored(f"An unexpected error occurred: {e}", "red"))


def edit_song():
    """
    Edits the details (name and URL) of a selected song in 'songs.json'.
    """
    try:
        songs = get_songs()
        if not songs:
            print(colored("No songs saved yet to edit.", "yellow"))
            return

        print(colored("Saved Songs:", "red"))
        for i, song in enumerate(songs, start=1):
            print(colored(f"{i}. {song['name']}", "cyan"))

        song_number = int(
            input(colored("Enter the number of the song to edit: ", "green"))
        )
        if 1 <= song_number <= len(songs):
            current_song = songs[song_number - 1]
            print(colored(f"\nEditing: {current_song['name']} ({current_song['url']})", "yellow"))

            new_name = input(colored(f"Enter new name (current: {current_song['name']}): ", "green")).strip()
            new_url = input(colored(f"Enter new URL (current: {current_song['url']}): ", "green")).strip()

            if not new_name:
                new_name = current_song['name']
            if not new_url:
                new_url = current_song['url']

            if ap.is_youtube_url(new_url):
                songs[song_number - 1] = {"name": new_name, "url": new_url}
                with open("songs.json", "w") as f:
                    json.dump(songs, f, indent=4)
                print(colored("Song updated successfully!", "blue"))
            else:
                print(colored("Invalid YouTube URL. Song not updated.", "red"))
        else:
            print(colored("Invalid song number", "red"))
    except ValueError:
        print(colored("Invalid input. Please enter a number.", "red"))
    except FileNotFoundError:
        print(colored("No songs saved yet.", "yellow"))
    except Exception as e:
        print(colored(f"An unexpected error occurred: {e}", "red"))


def song_player_menu(songs):
    """
    Displays a menu of songs and allows the user to select and play a song.

    Args:
        songs (list): A list of song dictionaries (each with 'name' and 'url').
    """
    while True:
        print(colored("\nChoose a song to play:", "green"))
        for i, song in enumerate(songs, start=1):
            print(colored(f"{i}. {song['name']}", "cyan"))
        song_choice = input(
            colored(
                "Enter the number of the song (or type 'exit' to go back): ", "green"
            )
        )
        if song_choice.lower() == "exit":
            break
        try:
            song_choice = int(song_choice)
            if 1 <= song_choice <= len(songs):
                url = songs[song_choice - 1]["url"]
                ap.play_song(url)
            else:
                print(colored("Invalid song number", "red"))
        except ValueError:
            print(colored("Invalid input. Please enter a number.", "red"))


def search_songs():
    """
    Searches for songs by name and displays matching results.
    """
    try:
        songs = get_songs()
        if not songs:
            print(colored("No songs saved yet to search.", "yellow"))
            return

        search_term = input(colored("Enter song name to search: ", "green")).strip().lower()
        if not search_term:
            print(colored("Search term cannot be empty.", "red"))
            return

        matching_songs = [song for song in songs if search_term in song['name'].lower()]

        if matching_songs:
            print(colored(f"\nFound {len(matching_songs)} matching song(s):", "green"))
            for i, song in enumerate(matching_songs, start=1):
                print(colored(f"{i}. {song['name']} - {song['url']}", "cyan"))
        else:
            print(colored("No songs found matching your search.", "yellow"))
    except Exception as e:
        print(colored(f"An unexpected error occurred: {e}", "red"))


def music_library():
    """
    Displays the main music library menu and handles user interactions
    for saving, viewing, playing, removing, editing, and searching songs.
    """
    menu_options = {
        "1": ("List of songs to play", lambda: song_player_menu(get_songs()) if get_songs() else print(colored("No songs saved yet.", "yellow"))),
        "2": ("Want to save a song", save_song),
        "3": ("View Saved Songs", view_songs),
        "4": ("Remove Song", remove_song),
        "5": ("Edit Song Details", edit_song),
        "6": ("Search Songs", search_songs),
        "7": ("Exit", lambda: "exit")
    }

    while True:
        print(colored("\nMusic Library Menu:\n", "blue"))
        for key, (description, _) in menu_options.items():
            print(colored(f"{key}. {description}", "cyan"))

        choice = input(colored("Choose an option: ", "green")).strip()

        if choice in menu_options:
            action = menu_options[choice][1]
            if choice == "7":  # Exit option
                break
            elif callable(action):
                action()
        else:
            print(colored("Invalid option. Please choose again.", "red"))
