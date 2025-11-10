import json
import audio_player as ap
from termcolor import colored
from constants import SONGS_FILE, PLAYLISTS_FILE, SUCCESS_SONG_SAVED, SUCCESS_SONG_UPDATED, SUCCESS_SONG_REMOVED


def get_songs():
    try:
        with open(SONGS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_song():
    user_data = []
    try:
        with open(SONGS_FILE, "r") as f:
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
        with open(SONGS_FILE, "w") as f:
            json.dump(user_data, f, indent=4)
            print(colored(SUCCESS_SONG_SAVED, "blue"))
    else:
        print(colored("Enter a Valid Youtube URL..", "red"))


def view_songs():
    try:
        with open(SONGS_FILE, "r") as file:
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
            with open(SONGS_FILE, "w") as f:
                json.dump(songs, f, indent=4)
            print(colored(SUCCESS_SONG_REMOVED, "blue"))
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
                with open(SONGS_FILE, "w") as f:
                    json.dump(songs, f, indent=4)
                print(colored(SUCCESS_SONG_UPDATED, "blue"))
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


def create_playlist():
    """
    Creates a new playlist by selecting songs from the saved songs list.
    """
    songs = get_songs()
    if not songs:
        print(colored("No songs saved yet to create a playlist.", "yellow"))
        return

    playlist_name = input(colored("Enter playlist name: ", "green")).strip()
    if not playlist_name:
        print(colored("Playlist name cannot be empty.", "red"))
        return

    print(colored("Select songs for the playlist (enter numbers separated by commas):", "cyan"))
    for i, song in enumerate(songs, start=1):
        print(colored(f"{i}. {song['name']}", "cyan"))

    try:
        selections = input(colored("Enter song numbers: ", "green")).strip()
        if not selections:
            print(colored("No songs selected.", "red"))
            return

        song_indices = [int(x.strip()) - 1 for x in selections.split(",")]
        playlist_songs = []

        for idx in song_indices:
            if 0 <= idx < len(songs):
                playlist_songs.append(songs[idx])
            else:
                print(colored(f"Invalid song number: {idx + 1}", "red"))
                return

        # Save playlist to a separate file
        playlists = get_playlists()
        playlists[playlist_name] = playlist_songs

        with open(PLAYLISTS_FILE, "w") as f:
            json.dump(playlists, f, indent=4)

        print(colored(f"Playlist '{playlist_name}' created successfully!", "blue"))

    except ValueError:
        print(colored("Invalid input. Please enter numbers separated by commas.", "red"))


def get_playlists():
    """
    Loads playlists from the playlists.json file.
    """
    try:
        with open(PLAYLISTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def view_playlists():
    """
    Displays all saved playlists.
    """
    playlists = get_playlists()
    if not playlists:
        print(colored("No playlists created yet.", "yellow"))
        return

    print(colored("Saved Playlists:", "red"))
    for i, playlist_name in enumerate(playlists.keys(), start=1):
        song_count = len(playlists[playlist_name])
        print(colored(f"{i}. {playlist_name} ({song_count} songs)", "cyan"))


def play_saved_playlist_enhanced(playlist_name, songs):
    """
    Enhanced playlist player with automatic progression and next/previous controls.
    
    Args:
        playlist_name (str): The name of the playlist.
        songs (list): List of song dictionaries with 'name' and 'url' keys.
    """
    if not songs:
        print(colored("This playlist is empty.", "red"))
        return
    
    print(colored(f"\n=== PLAYING PLAYLIST: {playlist_name} ===", "green"))
    print(colored(f"Total songs: {len(songs)}", "yellow"))
    
    current_index = 0
    volume = 50
    auto_next = True  # Automatically play next song when current ends
    
    while current_index < len(songs):
        current_song = songs[current_index]
        
        print(colored(f"\n--- Playing {current_index + 1}/{len(songs)}: {current_song['name']} ---", "green"))
        
        try:
            # Import VLC here to avoid issues if not available
            try:
                import vlc
                import time
            except ImportError:
                print(colored("VLC media player is not available. Cannot play audio.", "red"))
                print(colored("Please install VLC media player and ensure python-vlc package is properly configured.", "yellow"))
                time.sleep(3)
                return
            
            # Get audio URL using the existing function
            audio_url = ap.get_audio_url(current_song['url'])
            if not audio_url:
                print(colored(f"Skipping {current_song['name']} - could not fetch audio", "red"))
                current_index += 1
                continue
            
            player = vlc.MediaPlayer(audio_url)
            player.audio_set_volume(volume)
            player.play()
            
            print(colored(f"Volume: {volume}%", "cyan"))
            time.sleep(2)  # Give time for the song to start loading
            
            # Track if we need to continue to next song
            playlist_ended = False
            
            # Main playlist control loop
            while not playlist_ended:
                # Check if song has ended (if auto_next is enabled)
                if auto_next and player.get_length() > 0:
                    current_time = player.get_time() / 1000.0  # Convert to seconds
                    duration = player.get_length() / 1000.0  # Convert to seconds
                    
                    # If we're within 5 seconds of the end, prepare next song
                    if current_time >= (duration - 5) and current_time < duration:
                        print(colored("Song almost finished, preparing next song...", "yellow"))
                        time.sleep(3)
                        current_index += 1
                        playlist_ended = True
                        break
                
                # Display playlist-specific controls
                auto_status = "ON" if auto_next else "OFF"
                auto_color = "green" if auto_next else "red"
                print(
                    colored("\nPlaylist Controls: ", "yellow")
                    + colored("[N] Next Song | ", "green")
                    + colored("[P] Previous Song | ", "blue")
                    + colored("[C] Pause/Resume | ", "cyan")
                    + colored("[R] Restart Song | ", "magenta")
                    + colored(f"[A] Auto Next: {auto_status} | ", auto_color)
                    + colored("[V] Volume +/- | ", "cyan")
                    + colored("[Q] Exit Playlist", "red")
                )
                
                command = input(colored("Enter command: ", "yellow")).strip().lower()
                
                if command == "n":  # Next song
                    current_index += 1
                    playlist_ended = True
                    player.stop()
                    print(colored("Moving to next song.", "green"))
                    break
                    
                elif command == "p":  # Previous song
                    if current_index > 0:
                        current_index -= 1
                        playlist_ended = True
                        player.stop()
                        print(colored("Moving to previous song.", "blue"))
                        break
                    else:
                        print(colored("Already at the first song.", "yellow"))
                        
                elif command == "c":  # Pause/Resume
                    if player.is_playing():
                        player.pause()
                        print(colored("Music paused.", "yellow"))
                    else:
                        player.play()
                        print(colored("Music resumed.", "green"))
                        
                elif command == "r":  # Restart current song
                    player.stop()
                    player.play()
                    print(colored("Song restarted.", "magenta"))
                    
                elif command == "a":  # Toggle auto next
                    auto_next = not auto_next
                    if auto_next:
                        print(colored("Auto next enabled. Will play next song automatically.", "green"))
                    else:
                        print(colored("Auto next disabled. You'll need to press N for next song.", "red"))
                    
                elif command == "v":  # Volume control
                    print(colored(f"Current volume: {volume}%", "cyan"))
                    vol_cmd = input(colored("Enter new volume (0-100) or press Enter to cancel: ", "yellow")).strip()
                    if vol_cmd.isdigit():
                        new_vol = int(vol_cmd)
                        if 0 <= new_vol <= 100:
                            volume = new_vol
                            player.audio_set_volume(volume)
                            print(colored(f"Volume set to {volume}%.", "cyan"))
                        else:
                            print(colored("Invalid volume level. Please enter a number between 0 and 100.", "red"))
                    
                elif command == "q":  # Exit playlist
                    player.stop()
                    print(colored("Exiting playlist.", "red"))
                    return
                    
                else:
                    print("Invalid command. Try again.")
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.5)
                
        except Exception as e:
            print(colored(f"Error playing {current_song['name']}: {e}", "red"))
            current_index += 1
            continue
    
    # Playlist finished
    if current_index >= len(songs):
        print(colored("\n=== Playlist completed! ===", "green"))
        play_again = input(colored("Do you want to play the playlist again? (y/n): ", "yellow")).strip().lower()
        if play_again == "y":
            play_saved_playlist_enhanced(playlist_name, songs)  # Restart from beginning
        else:
            print(colored("Thank you for listening to the playlist!", "blue"))


def play_playlist():
    """
    Allows user to select and play a playlist with enhanced controls.
    """
    playlists = get_playlists()
    if not playlists:
        print(colored("No playlists available.", "yellow"))
        return

    view_playlists()

    try:
        choice = int(input(colored("Enter playlist number to play: ", "green")))
        playlist_names = list(playlists.keys())

        if 1 <= choice <= len(playlist_names):
            selected_playlist = playlist_names[choice - 1]
            songs = playlists[selected_playlist]
            print(colored(f"\nPlaying playlist: {selected_playlist}", "green"))
            
            # Ask user if they want enhanced playlist mode
            mode_choice = input(colored("Play with auto-progression? (y/n, default y): ", "cyan")).strip().lower()
            
            if mode_choice == "n":
                # Use the original song selection mode
                song_player_menu(songs)
            else:
                # Use enhanced playlist mode with auto-progression
                play_saved_playlist_enhanced(selected_playlist, songs)
        else:
            print(colored("Invalid playlist number.", "red"))

    except ValueError:
        print(colored("Invalid input. Please enter a number.", "red"))


def play_all_saved_songs_playlist():
    """
    Creates and plays a playlist of all saved songs with auto-progression.
    """
    all_songs = get_songs()
    if not all_songs:
        print(colored("No songs saved yet.", "yellow"))
        return
    
    print(colored(f"\n=== ALL SAVED SONGS PLAYLIST ===", "green"))
    print(colored(f"Total songs: {len(all_songs)}", "yellow"))
    print(colored("This will play all your saved songs in sequence with auto-progression.", "cyan"))
    
    confirm = input(colored("Do you want to play all saved songs? (y/n): ", "green")).strip().lower()
    if confirm == "y":
        play_saved_playlist_enhanced("All Saved Songs", all_songs)


def music_library():
    """
    Displays the main music library menu and handles user interactions
    for saving, viewing, playing, removing, editing, searching songs, and managing playlists.
    """
    menu_options = {
        "1": ("List of songs to play", lambda: song_player_menu(get_songs()) if get_songs() else print(colored("No songs saved yet.", "yellow"))),
        "2": ("Want to save a song", save_song),
        "3": ("View Saved Songs", view_songs),
        "4": ("Remove Song", remove_song),
        "5": ("Edit Song Details", edit_song),
        "6": ("Search Songs", search_songs),
        "7": ("Create Playlist", create_playlist),
        "8": ("View Playlists", view_playlists),
        "9": ("Play Playlist", play_playlist),
        "10": ("Play All Saved Songs (Auto-Progression)", play_all_saved_songs_playlist),
        "11": ("Exit", lambda: "exit")
    }

    while True:
        print(colored("\nMusic Library Menu:\n", "blue"))
        for key, (description, _) in menu_options.items():
            print(colored(f"{key}. {description}", "cyan"))

        choice = input(colored("Choose an option: ", "green")).strip()

        if choice in menu_options:
            action = menu_options[choice][1]
            if choice == "11":  # Exit option
                break
            elif callable(action):
                action()
        else:
            print(colored("Invalid option. Please choose again.", "red"))
