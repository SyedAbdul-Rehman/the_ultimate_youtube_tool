# from pytube import YouTube      # for downloading YouTube videos
import yt_dlp
import os  # for managing file paths
from termcolor import colored


def download_directory():
    """
    Ensures a 'downloads' directory exists in the current working directory
    and returns its path.
    """
    path = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_url(url):
    """
    Fetches YouTube video information using yt-dlp.

    Args:
        url (str): The YouTube video URL.

    Returns:
        dict: Video information dictionary, or None if fetching fails.
    """
    try:
        ydl_opts = {"quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            yt = ydl.extract_info(url, download=False)
            print(colored(f"\nTitle: {yt['title']}", "cyan"))
            print(colored(f"Uploader: {yt['uploader']}", "yellow"))
            duration = yt.get("duration", 0)
            print(
                colored(
                    f"Length: {duration // 60} minutes and {duration % 60} seconds",
                    "green",
                )
            )
        return yt
    except Exception as e:
        print(colored(f"Error fetching video information: {e}", "red"))
        print(colored("Please check if the URL is valid and accessible.", "yellow"))
        return None


def display_streams(url):
    """
    Displays available video/audio formats for the given YouTube URL.

    Args:
        url (str): The YouTube video URL.

    Returns:
        dict: Dictionary of format IDs to descriptions, or None if fetching fails.
    """
    try:
        print(colored("\nFetching available formats...\n", "cyan"))
        options = {
            "listformats": False,  # Disable format listing
            "quiet": True,
            "no_warnings": True,  # Suppress unnecessary output
        }

        formats = {}

        # Use yt-dlp to extract formats
        with yt_dlp.YoutubeDL(options) as ydl:
            yt = ydl.extract_info(url, download=False)
            for fmt in yt["formats"]:
                if fmt.get("ext") and fmt.get("format_note"):
                    formats[fmt["format_id"]] = f"{fmt['format_note']} ({fmt['ext']})"

        # Display formats
        print(colored("Available formats:", "yellow"))
        for fmt_id, description in formats.items():
            print(colored(f"{fmt_id}: ", "green") + colored(description, "cyan"))

        return formats
    except KeyboardInterrupt:
        print(colored("\nFormat selection canceled by the user.", "red"))
        return None
    except Exception as e:
        print(colored(f"Error fetching available formats: {e}", "red"))
        print(colored("Please check the video URL or try again later.", "yellow"))
        return None


def download_stream(url, format_id, path):
    """
    Downloads the selected video/audio stream to the specified path.

    Args:
        url (str): The YouTube video URL.
        format_id (str): The format ID to download.
        path (str): The directory path to save the file.
    """
    print(colored("\nDownloading...", "yellow"))
    try:
        ydl_opts = {
            "outtmpl": os.path.join(path, "%(title)s.%(ext)s"),
            "format": format_id,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(colored("Download complete!", "green"))
    except KeyboardInterrupt:
        print(colored("\nDownload canceled by the user.", "red"))
    except Exception as e:
        print(colored(f"Download failed: {e}", "red"))
        print(colored("Please check the selected format ID or your network connection.", "yellow"))


def input_url_for_video():
    """
    Handles user input for YouTube video URLs and format selection for downloading.
    Supports multiple URLs separated by commas.
    """
    download_path = download_directory()
    print(colored(f"Files will be saved in: {download_path}", "cyan"))
    while True:
        urls = (
            input(colored("Enter YouTube video URL(s) separated by commas: ", "yellow"))
            .strip()
            .split(",")
        )
        urls = [url.strip() for url in urls if url.strip()]

        if not urls:
            print(colored("No valid URLs provided. Please try again.", "red"))
            continue

        for url in urls:
            print(colored(f"\nProcessing URL: {url}", "cyan"))

            # Fetch video information
            yt = get_url(url)
            if not yt:
                print(colored("Skipping invalid or inaccessible URL. It might be private, deleted, or region-restricted.", "red"))
                continue

            streams = display_streams(url)
            if not streams:
                print(
                    colored(
                        "No available formats found for this video. Skipping...", "red"
                    )
                )
                continue

            while True:
                format_id = input(
                    colored(
                        "\nEnter the number of your preferred format (or type 'cancel' to skip): ",
                        "yellow",
                    )
                ).strip()
                if format_id.lower() == "cancel":
                    print(colored("Skipping this video.", "yellow"))
                    break
                elif format_id not in streams:
                    print(
                        colored(
                            "Invalid choice. Please try again or type 'cancel' to skip.",
                            "red",
                        )
                    )
                else:
                    download_stream(url, format_id, download_path)
                    break

        retry = (
            input(
                colored("\nDo you want to download more videos? (yes/no): ", "yellow")
            )
            .strip()
            .lower()
        )
        if retry != "yes":
            print(
                colored(
                    "Thank you for using the YouTube Video Downloader. Goodbye!",
                    "green",
                )
            )
            break
