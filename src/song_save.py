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
    try:
        with open("songs.json", "r") as file:
            songs = json.load(file)
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
    except FileNotFoundError:
        print(colored("No songs saved yet.", "yellow"))


def song_player_menu(songs):
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


def music_library():
    while True:
        print(colored("\nMusic Library Menu:\n", "blue"))
        print(colored("1. List of songs to play", "cyan"))
        print(colored("2. Want to save a song", "cyan"))
        print(colored("3. View Saved Songs", "cyan"))
        print(colored("4. Remove Song", "cyan"))
        print(colored("5. Exit", "cyan"))
        choice = input(colored("Choose an option: ", "green"))
        if choice == "1":
            # view_songs()
            songs = get_songs()
            if songs:
                song_player_menu(songs)
            else:
                print(colored("No songs saved yet.", "yellow"))
        elif choice == "2":
            save_song()
        elif choice == "3":
            view_songs()
        elif choice == "4":
            remove_song()
        elif choice == "5":
            break
        else:
            print(colored("Invalid option. Please choose again.", "red"))


if __name__ == "__main__":
    main()
