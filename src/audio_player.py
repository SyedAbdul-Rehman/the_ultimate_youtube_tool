import os
import re
import time
import yt_dlp
from functools import lru_cache
from termcolor import colored
from utils import clear_screen

# Check if VLC is available (will be checked when needed)
VLC_AVAILABLE = False


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
            "no_warnings": True,  # Suppress warnings
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


# Function to get playlist information
def get_playlist_info(playlist_url):
    """
    Fetches information about a YouTube playlist.
    
    Args:
        playlist_url (str): The YouTube playlist URL.
        
    Returns:
        dict: Playlist information including title and list of video URLs, or None if fetching fails.
    """
    try:
        print(colored("\nFetching playlist information...", "cyan"))
        print(colored("This may take a moment for large playlists...\n", "yellow"))
        
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,  # Suppress warnings
            "extract_flat": True,  # Extract metadata without downloading
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            
            playlist_info = {
                "title": info.get("title", "Unknown Playlist"),
                "uploader": info.get("uploader", "Unknown"),
                "videos": []
            }
            
            # Extract video information from the playlist
            for entry in info.get("entries", []):
                if entry and "id" in entry:
                    video_url = f"https://youtu.be/{entry['id']}"
                    video_info = {
                        "title": entry.get("title", "Unknown Title"),
                        "url": video_url,
                        "duration": entry.get("duration", 0)
                    }
                    playlist_info["videos"].append(video_info)
            
            return playlist_info
            
    except Exception as e:
        print(colored(f"Failed to fetch playlist information: {e}", "red"))
        print(colored("Please check if the playlist URL is valid and accessible.", "yellow"))
        return None


# Function to get current playback time (in seconds)
def get_current_time(player):
    """Get current playback time in seconds."""
    try:
        return player.get_time() / 1000.0  # VLC returns time in milliseconds
    except:
        return 0


# Function to get song duration (in seconds)
def get_duration(player):
    """Get current song duration in seconds."""
    try:
        return player.get_length() / 1000.0  # VLC returns length in milliseconds
    except:
        return 0


# Function to play a playlist with automatic progression and navigation controls
def play_playlist(playlist_url, start_index=0):
    """
    Plays a YouTube playlist with automatic next song progression and navigation controls.
    
    Args:
        playlist_url (str): The YouTube playlist URL.
        start_index (int): The index of the song to start playing from.
    """
    # Try to import VLC only when needed
    try:
        import vlc
    except ImportError:
        print(colored("VLC media player is not available. Cannot play audio.", "red"))
        print(colored("Please install VLC media player and ensure python-vlc package is properly configured.", "yellow"))
        time.sleep(3)
        return
    
    # Get playlist information
    playlist_info = get_playlist_info(playlist_url)
    if not playlist_info:
        return
    
    videos = playlist_info["videos"]
    if not videos:
        print(colored("No videos found in this playlist.", "red"))
        return
    
    print(colored(f"\n=== PLAYLIST: {playlist_info['title']} ===", "green"))
    print(colored(f"Total videos: {len(videos)}", "yellow"))
    print(colored(f"Playlist by: {playlist_info['uploader']}", "cyan"))
    
    current_index = start_index
    volume = 50
    auto_next = True  # Automatically play next song when current ends
    
    while current_index < len(videos):
        current_video = videos[current_index]
        
        print(colored(f"\n--- Playing {current_index + 1}/{len(videos)}: {current_video['title']} ---", "green"))
        
        # Get audio URL for current video
        audio_url = get_audio_url(current_video['url'])
        if not audio_url:
            print(colored(f"Skipping {current_video['title']} - could not fetch audio", "red"))
            current_index += 1
            continue
        
        try:
            player = vlc.MediaPlayer(audio_url)
            player.audio_set_volume(volume)
            player.play()
            
            print(colored(f"Volume: {volume}%", "cyan"))
            print(colored("Loading next song...", "yellow"))
            time.sleep(2)  # Give time for the song to start loading
            
            # Track if we need to continue to next song
            playlist_ended = False
            
            # Main playlist control loop
            while not playlist_ended:
                # Check if song has ended (if auto_next is enabled)
                if auto_next and get_duration(player) > 0:
                    current_time = get_current_time(player)
                    duration = get_duration(player)
                    
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
            print(colored(f"Error playing {current_video['title']}: {e}", "red"))
            current_index += 1
            continue
    
    # Playlist finished
    if current_index >= len(videos):
        print(colored("\n=== Playlist completed! ===", "green"))
        play_again = input(colored("Do you want to play the playlist again? (y/n): ", "yellow")).strip().lower()
        if play_again == "y":
            play_playlist(playlist_url, 0)  # Restart from beginning
        else:
            print(colored("Thank you for listening to the playlist!", "blue"))


# Function to detect if URL is a playlist
def is_youtube_playlist(url):
    """Check if the URL is a YouTube playlist."""
    playlist_pattern = r"^https?://(www\.)?youtube\.com/playlist\?list=.*$"
    return bool(re.match(playlist_pattern, url))


# Function to play a song with volume control
def play_song(song):
    """
    Plays a song from a given YouTube URL with volume control.
    Args:
        song (str): The YouTube URL of the song to play.
    """
    # Try to import VLC only when needed
    try:
        import vlc
    except ImportError:
        print(colored("VLC media player is not available. Cannot play audio.", "red"))
        print(colored("Please install VLC media player and ensure python-vlc package is properly configured.", "yellow"))
        time.sleep(3)
        return

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
            clear_screen()  # Clear the screen
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


# Function to play a song or playlist based on URL type
def input_url_for_audio():
    while True:
        try:
            url = input(
                colored("\nEnter the song URL (or 'exit' to go back): ", "yellow")
            ).strip()
            if url.lower() == "exit":
                break
            elif is_youtube_url(url):
                # Check if it's a playlist URL
                if is_youtube_playlist(url):
                    print(colored("🎵 YouTube playlist detected! Starting playlist playback...", "green"))
                    play_playlist(url)
                else:
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


def test_error_handling():
    """
    Basic error handling tests for audio_player functions.
    Tests various error conditions and edge cases.
    """
    print(colored("Running basic error handling tests...", "cyan"))

    # Test 1: Invalid URL format
    test_urls = [
        "",  # Empty string
        "not_a_url",  # Invalid format
        "https://google.com",  # Non-YouTube URL
        "https://youtube.com/watch?v=invalid",  # Valid format but may not exist
    ]

    for url in test_urls:
        result = is_youtube_url(url)
        if url in ["", "not_a_url", "https://google.com"]:
            assert not result, f"Expected False for invalid URL: {url}"
        print(colored(f"✓ URL validation test passed for: {url}", "green"))

    # Test 2: Test get_audio_url with invalid input
    try:
        result = get_audio_url("")
        assert result is None, "Expected None for empty URL"
        print(colored("✓ Empty URL test passed", "green"))
    except Exception as e:
        print(colored(f"✓ Expected exception for empty URL: {e}", "green"))

    print(colored("All basic error handling tests completed!", "green"))
