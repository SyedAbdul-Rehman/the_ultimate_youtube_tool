# Contributing to The Ultimate YouTube Tool

Thank you for your interest in contributing to The Ultimate YouTube Tool! This document provides guidelines and information for contributors.

## How to Contribute

### Reporting Bugs
- Use the GitHub Issues tab to report bugs
- Include detailed steps to reproduce the issue
- Provide your operating system and Python version
- Include any error messages or screenshots

### Suggesting Features
- Open a GitHub Issue with the "enhancement" label
- Describe the feature and its use case
- Explain why it would be beneficial to the project

### Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/SyedAbdul-Rehman/the_ultimate_youtube_tool.git
   cd the_ultimate_youtube_tool
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python src/main.py
   ```

## Code Style Guidelines

### Python Style
- Follow PEP 8 guidelines
- Use 4 spaces for indentation
- Use snake_case for variable and function names
- Use PascalCase for class names
- Keep line length under 88 characters

### Documentation
- Add docstrings to all functions and classes
- Use Google-style docstrings
- Keep comments clear and concise

### Commit Messages
- Use conventional commit format:
  ```
  type(scope): description

  [optional body]
  ```
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Keep the description concise but descriptive

### Testing
- Test your changes thoroughly
- Ensure existing functionality still works
- Add tests for new features when possible

## Project Structure
```
the_ultimate_youtube_tool/
├── src/
│   ├── main.py              # Main application entry point
│   ├── audio_player.py      # Audio playback functionality
│   ├── video_downloader.py  # Video/audio downloading
│   ├── qr_code.py          # QR code generation
│   ├── song_save.py        # Song library management
│   └── yt_access_control.py # YouTube access control
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
└── CONTRIBUTING.md         # This file
```

## Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Help create a positive community

## License
By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Questions?
If you have any questions about contributing, feel free to open an issue or contact the maintainers.
