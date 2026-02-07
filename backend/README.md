# Backend Directory

This directory contains all the backend Python code for the Playlist Converter application.

## Structure

```
backend/
├── __init__.py                 # Package initializer
├── api.py                      # FastAPI application and REST endpoints
├── main.py                     # Core playlist conversion logic
├── config.py                   # Configuration and settings management
├── models.py                   # Pydantic data models
├── apple_music_lib/            # Apple Music integration
│   ├── __init__.py
│   └── get_apple_music.py      # Fetch songs from Apple Music
└── logger_lib/                 # Logging utilities
    ├── __init__.py
    └── create_logger.py        # Custom logger implementation
```

## Running the Backend

### Start the FastAPI server:
```bash
make run-backend
# or
uv run uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000
```

### Run CLI conversion (standalone):
```bash
uv run python -m backend.main
```

## Key Modules

- **api.py**: FastAPI REST API with endpoints for OAuth and playlist conversion
- **main.py**: Contains all core functions for Spotify playlist creation and song matching
- **config.py**: Loads environment variables and application settings
- **models.py**: Pydantic models for data validation
- **apple_music_lib**: Handles fetching playlist data from Apple Music
- **logger_lib**: Custom logging with color formatting and file output

## Import Pattern

All imports use absolute imports from the `backend` package:
```python
from backend.config import settings
from backend.logger_lib import create_logger
from backend.apple_music_lib import get_apple_music_songs
```
