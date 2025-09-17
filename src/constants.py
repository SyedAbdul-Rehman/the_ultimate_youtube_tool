"""
Constants used throughout the application.
"""

# Application Information
APP_NAME = "The Ultimate YouTube Tool"
APP_VERSION = "1.0.0"
AUTHOR = "@SyedAbdul-Rehman"

# File and Directory Names
SONGS_FILE = "songs.json"
PLAYLISTS_FILE = "playlists.json"
DOWNLOADS_DIR = "downloads"
QR_CODES_DIR = "qr_codes"

# YouTube URL Patterns
YOUTUBE_PATTERN1 = r"^https?://(?:www\.)?(?:youtube\.com|youtu\.be)/.*$"
YOUTUBE_PATTERN2 = r"^https?://(www\.)?youtube\.com/playlist\?list=.*$"

# Terminal Colors (supported by termcolor and terminal_color function)
SUPPORTED_COLORS = [
    "black", "red", "green", "yellow", "blue",
    "magenta", "cyan", "white"
]

# Default Settings
DEFAULT_QR_BOX_SIZE = 1
DEFAULT_QR_BORDER = 1
DEFAULT_QR_FILL_COLOR = "black"
DEFAULT_QR_BACK_COLOR = "white"

# Timeouts and Limits
API_TIMEOUT = 5  # seconds
CACHE_MAX_SIZE = 128
JOKE_CACHE_MAX_SIZE = 32

# Error Messages
ERROR_INVALID_URL = "Invalid YouTube URL format. Please enter valid YouTube URLs (youtube.com or youtu.be)."
ERROR_NO_INTERNET = "No internet connection. Make sure you're connected with internet and then try again..."
ERROR_EMPTY_INPUT = "Input cannot be empty."
ERROR_INVALID_CHOICE = "Invalid choice. Please try again."

# Success Messages
SUCCESS_DOWNLOAD_COMPLETE = "Download complete!"
SUCCESS_SONG_SAVED = "Song saved successfully!"
SUCCESS_SONG_UPDATED = "Song updated successfully!"
SUCCESS_SONG_REMOVED = "Song removed successfully!"
SUCCESS_QR_SAVED = "QR Code saved as {filename}"
SUCCESS_QR_DISPLAYED = "QR Code successfully displayed in the terminal."
