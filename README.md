# Ultimate YouTube Tool 🎵 📺

A versatile Python-based command-line tool that combines multiple YouTube functionalities in one place.

## Features 🚀

### 1. Song/Audio Player 🎵
- Play saved songs from your local library
- Stream songs directly from YouTube URLs
- Create and manage custom playlists
- Manage your music collection with advanced features:
  - Edit song details (name and URL)
  - Search songs by name
  - Add/remove songs from your library
  - Create custom playlists from saved songs
  - Play entire playlists

### 2. Video/Audio Downloader 💽
- Download videos from YouTube
- Extract audio from YouTube videos
- Save content for offline playback
- Improved error handling and user feedback

### 3. YouTube QR Code Generator 📱
- Generate QR codes for YouTube videos
- Customizable QR code styles (colors, bold, underline)
- Easy sharing of YouTube content
- Quick mobile access to videos
- Generate QR codes for jokes and fun content

### 4. YouTube Access Control 🔒
- Block or unblock YouTube access on your system
- Administrator privileges required
- DNS cache flushing for immediate effect

## ⚠️ **CRITICAL REQUIREMENT: VLC Media Player**
**🚨 This tool REQUIRES VLC Media Player 64-bit to be installed and configured for audio playback functionality!**

**Before proceeding with installation, you MUST:**

1. **Download and Install VLC Media Player 64-bit:**
   - Official Download: [https://www.videolan.org/vlc/download-windows.html](https://www.videolan.org/vlc/download-windows.html)
   - Direct 64-bit Download: [https://get.videolan.org/vlc/3.0.18/win64/vlc-3.0.18-win64.exe](https://get.videolan.org/vlc/3.0.18/win64/vlc-3.0.18-win64.exe)

2. **Configure VLC Environment Variable Path:**
   - **Windows 10/11:** 
     - Open Control Panel → System → Advanced System Settings → Environment Variables
     - Add VLC installation directory to PATH variable
     - Default path: `C:\Program Files\VideoLAN\VLC\`
   - **Windows 7/8:**
     - Right-click "Computer" → Properties → Advanced System Settings → Environment Variables
     - Add VLC path to system PATH variable

3. **Verify VLC Installation:**
   - Open Command Prompt
   - Type `vlc --version` to verify it's accessible from command line
   - If command not found, restart your terminal/command prompt

**🎵 Without VLC Media Player, the audio player and song streaming features will NOT work!**
## Installation 💻

### 1. Clone the repository
```bash
git clone https://github.com/SyedAbdul-Rehman/the_ultimate_youtube_tool.git
cd the_ultimate_youtube_tool
```

### 2. Install required dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Configure environment variables
Copy the example environment file and customize it:
```bash
cp .env.example .env
```

Edit `.env` to configure API settings:
```bash
# Joke API Configuration
JOKE_API_URL=https://icanhazdadjoke.com/
JOKE_API_TIMEOUT=5
```

## Usage 🔧
Run the main script:
```bash
python main.py
```

Follow the interactive menu to:
- Play or download music
- Download videos
- Generate QR codes
- Manage your music library

## Features in Detail 📋
### Song/Audio Player
- Browse and play your saved music collection
- Stream YouTube audio without downloading
- Create and manage custom playlists
- Advanced music library management with search and edit capabilities
- User-friendly menu interface with improved navigation

### Video/Audio Downloader
- High-quality video downloads with format selection
- Audio extraction capability
- Input validation for YouTube URLs
- Multiple format support with error handling

### QR Code Generator
- Convert YouTube URLs to QR codes
- Optimized performance with caching
- Customizable colors and styles
- Generate QR codes for jokes and fun content
- Easy sharing functionality and mobile-friendly access

### YouTube Access Control
- Block or unblock YouTube access system-wide
- Administrator privileges with clear instructions
- DNS cache flushing for immediate effect

## Requirements 📝
### System Requirements
- **VLC Media Player 64-bit** (🔴 **ESSENTIAL** - Required for audio playback functionality)
- Python 3.x
- Internet connection
- Administrator privileges (for YouTube access control features)

### Python Packages
- pyfiglet
- termcolor
- yt-dlp
- python-vlc (Python binding for VLC)
- qrcode
- requests

## Author ✍️
**@SyedAbdul-Rehman**

## Version
**Current Version: 1.0.0**

## License 📝
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing 🤝
Contributions, issues, and feature requests are welcome!

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

## Support 💪
If you like this project, please give it a ⭐️!
