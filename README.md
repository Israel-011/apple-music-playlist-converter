[![Python Versions](https://github.com/primetimetank21/apple-music-playlist-converter/actions/workflows/python-versions.yml/badge.svg)](https://github.com/primetimetank21/apple-music-playlist-converter/actions/workflows/python-versions.yml)

# 🎵 Apple Music Playlist Converter

Convert your Apple Music playlists to Spotify playlists with ease! This automated tool fetches songs from an Apple Music playlist and recreates it in your Spotify account.

## ✨ Features

- 🔄 **Automatic Conversion**: Seamlessly transfer playlists from Apple Music to Spotify
- 🎯 **Smart Matching**: Intelligent song search and matching algorithm
- 📝 **Logging**: Comprehensive logging system for tracking conversion progress
- 🔒 **Secure**: Uses environment variables for API credentials
- 🎨 **Modern**: Built with Python 3.12+ and modern async capabilities
- ⚡ **Efficient**: Asynchronous processing for faster conversions

## 🚀 Prerequisites

Before you begin, ensure you have the following:

- **Python 3.12+** installed on your system
- **Spotify Developer Account** - [Sign up here](https://developer.spotify.com/)
  - Client ID
  - Client Secret
  - Redirect URI configured in your Spotify app settings
- **Apple Music Playlist URL** - The public URL of the playlist you want to convert

## 📦 Installation

### Option 1: Using UV (Recommended)

```bash
# Clone the repository
git clone git@github.com:Israel-011/apple-music-playlist-converter.git
cd apple-music-playlist-converter

# Install dependencies using uv
make install
```

### Option 2: Using pip

```bash
# Clone the repository
git clone git@github.com:Israel-011/apple-music-playlist-converter.git
cd apple-music-playlist-converter

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

## ⚙️ Configuration

1. **Copy the environment template:**

   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file with your credentials:**

   ```env
   # Spotify API Credentials
   CLIENT_ID="your_spotify_client_id_here"
   CLIENT_SECRET="your_spotify_client_secret_here"
   REDIRECT_URL="http://localhost:8888/callback"

   # Spotify Scopes (comma-separated)
   SCOPE="playlist-modify-public,playlist-modify-private,user-library-read"

   # Logging Level
   LOG_LEVEL="INFO"
   ```

3. **Get Spotify API Credentials:**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new app or use an existing one
   - Copy your Client ID and Client Secret
   - Add `http://localhost:8888/callback` to your Redirect URIs

## 🎮 Usage

### Running the Converter

**Using Make:**

```bash
make run
```

**Using Python directly:**

```bash
python src/main.py
```

**Using UV:**

```bash
uv run src/main.py
```

### Example Workflow

1. Find an Apple Music playlist URL (e.g., `https://music.apple.com/us/playlist/your-playlist/pl.xxxxx`)
2. Update the URL in `src/main.py` (or modify to accept command-line arguments)
3. Run the converter
4. The script will:
   - Fetch all songs from the Apple Music playlist
   - Search for matching songs on Spotify
   - Create a new Spotify playlist
   - Add all found songs to your Spotify playlist

## 📁 Project Structure

```
apple-music-playlist-converter/
├── src/
│   ├── main.py                 # Main application entry point
│   ├── config.py               # Configuration and settings management
│   ├── models.py               # Pydantic data models
│   ├── apple_music_lib/        # Apple Music integration
│   │   ├── __init__.py
│   │   └── get_apple_music.py  # Fetch songs from Apple Music
│   └── logger_lib/             # Logging utilities
│       ├── __init__.py
│       └── create_logger.py    # Logger configuration
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── .pre-commit-config.yaml     # Pre-commit hooks configuration
├── Makefile                    # Build and run commands
├── pyproject.toml              # Project dependencies and metadata
├── requirements.txt            # Python dependencies (pip format)
├── uv.lock                     # UV dependency lock file
└── README.md                   # This file
```

## 🛠️ Development

### Code Quality

**Format code:**

```bash
make format
```

**Lint code:**

```bash
make lint
```

**Run tests:**

```bash
make test
```

**Clean build artifacts:**

```bash
make clean
```

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. They are automatically installed when you run `make install`.

To manually run pre-commit hooks:

```bash
pre-commit run --all-files
```

## 📊 Logging

The application uses a comprehensive logging system. You can adjust the log level in your `.env` file:

- `DEBUG`: Detailed information for debugging
- `INFO`: General informational messages (default)
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical issues

Logs will show:

- Songs successfully added to playlist
- Songs that couldn't be found on Spotify
- API errors and exceptions

## ⚠️ Known Limitations

- Not all songs from Apple Music may be available on Spotify
- Song matching is based on track name and artist, which may occasionally result in incorrect matches
- Rate limiting may apply based on Spotify API usage

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 To-Do

- [ ] Add command-line argument support for playlist URLs
- [ ] Implement progress bar for conversion status
- [ ] Add support for saving failed song matches
- [ ] Create GUI interface
- [ ] Add support for batch conversion (multiple playlists)
- [ ] Implement reverse conversion (Spotify to Apple Music)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Spotipy](https://spotipy.readthedocs.io/) - Spotify API wrapper
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [Playwright](https://playwright.dev/python/) - Browser automation

## 📧 Contact

Israel Pratt - [@Israel-011](https://github.com/Israel-011)

Project Link: [https://github.com/Israel-011/apple-music-playlist-converter](https://github.com/Israel-011/apple-music-playlist-converter)

---

⭐ If you find this project helpful, please consider giving it a star!
