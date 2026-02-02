# 🎵 Playlist Converter - Full Stack Application

A modern, full-stack application to convert Apple Music playlists to Spotify playlists. Built with React frontend and Python FastAPI backend.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                        │
│  • Modern UI with Tailwind CSS                              │
│  • Responsive design (Mobile & Web)                         │
│  • Real-time conversion status                              │
│  • Smooth animations & dark theme                           │
└────────────────┬────────────────────────────────────────────┘
                 │ REST API
                 │ (Axios)
┌────────────────▼────────────────────────────────────────────┐
│                  Backend (FastAPI)                          │
│  • RESTful API endpoints                                    │
│  • CORS enabled                                             │
│  • Async processing                                         │
│  • Input validation (Pydantic)                              │
└────────────────┬────────────────────────────────────────────┘
                 │
        ┌────────┴─────────┐
        │                  │
┌───────▼────────┐  ┌──────▼──────────┐
│  Apple Music   │  │  Spotify API    │
│  Web Scraping  │  │  (Spotipy)      │
│  (Playwright)  │  │                 │
└────────────────┘  └─────────────────┘
```

## 📁 Project Structure

```
playlistconverter/
├── frontend/                    # React frontend application
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── Header.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   └── StatusDisplay.jsx
│   │   ├── services/           # API service layer
│   │   │   └── api.js
│   │   ├── App.jsx             # Main app component
│   │   ├── index.css           # Global styles (Tailwind)
│   │   └── main.jsx
│   ├── tailwind.config.js      # Tailwind configuration
│   ├── vite.config.js          # Vite configuration
│   ├── package.json
│   └── README.md
│
├── src/                         # Python backend
│   ├── api.py                  # FastAPI application ⭐ NEW
│   ├── main.py                 # Original CLI script
│   ├── config.py               # Configuration management
│   ├── models.py               # Pydantic models
│   ├── apple_music_lib/        # Apple Music integration
│   │   ├── __init__.py
│   │   └── get_apple_music.py
│   └── logger_lib/             # Logging utilities
│       ├── __init__.py
│       └── create_logger.py
│
├── .env.example                # Environment variables template
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Project metadata
├── README.md                   # Main documentation
└── PROJECT_OVERVIEW.md         # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- Spotify Developer Account

### 1. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or using uv
make install

# Install Playwright browsers
playwright install

# Configure environment
cp .env.example .env
# Edit .env with your Spotify credentials
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# VITE_API_URL is already set to http://localhost:8000
```

### 3. Run the Application

**Terminal 1 - Start Backend:**

```bash
# From project root
python src/api.py

# Or with uvicorn directly
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

**Terminal 2 - Start Frontend:**

```bash
cd frontend
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## 🎨 Features

### Frontend Features

- ✨ **Beautiful UI**: Modern, glassmorphic design with Tailwind CSS
- 📱 **Responsive**: Works perfectly on mobile and desktop
- 🎯 **User-Friendly**: Intuitive interface with clear instructions
- 🔄 **Real-time Updates**: Live conversion status and progress
- 🎨 **Animations**: Smooth transitions and loading states
- 🌙 **Dark Theme**: Eye-friendly dark mode
- ⚡ **Fast**: Built with Vite for lightning-fast development

### Backend Features

- 🚀 **FastAPI**: Modern, fast Python web framework
- 📡 **RESTful API**: Clean, well-documented endpoints
- 🔒 **CORS Enabled**: Secure cross-origin requests
- ✅ **Input Validation**: Pydantic models for data validation
- 📝 **Logging**: Comprehensive logging system
- 🔄 **Async Support**: Non-blocking operations
- 📚 **Auto Docs**: Interactive API documentation

## 🔌 API Endpoints

### `GET /`

Root endpoint with API information

### `GET /api/health`

Health check endpoint

### `POST /api/convert`

Convert Apple Music playlist to Spotify

**Request Body:**

```json
{
  "apple_playlist_url": "https://music.apple.com/us/playlist/...",
  "spotify_playlist_name": "My Playlist",
  "is_public": false
}
```

**Response:**

```json
{
  "status": "completed",
  "message": "Playlist converted successfully",
  "success_count": 45,
  "failed_count": 2,
  "total_count": 47
}
```

### `GET /api/auth/spotify`

Get Spotify authentication URL

### `GET /api/auth/spotify/status`

Check Spotify authentication status

## 🛠️ Tech Stack

### Frontend

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **React Icons** - Icon library

### Backend

- **Python 3.12+** - Programming language
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Spotipy** - Spotify API wrapper
- **Playwright** - Browser automation
- **Pytest** - Testing framework

## 📝 Development

### Backend Development

```bash
# Run API server with auto-reload
uvicorn src.api:app --reload

# Format code
make format

# Lint code
make lint

# Run tests
make test
```

### Frontend Development

```bash
cd frontend

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## 🌐 Usage Examples

### Using the Web Interface

1. Open `http://localhost:5173` in your browser
2. Click "Connect Spotify" to authenticate
3. Paste your Apple Music playlist URL
4. Enter a name for your Spotify playlist
5. Click "Convert Playlist"
6. Wait for the conversion to complete
7. Check your Spotify account for the new playlist

### Using the API Directly

```bash
# Convert a playlist
curl -X POST "http://localhost:8000/api/convert" \
  -H "Content-Type: application/json" \
  -d '{
    "apple_playlist_url": "https://music.apple.com/us/playlist/...",
    "spotify_playlist_name": "My Awesome Playlist",
    "is_public": false
  }'
```

## 🔐 Environment Variables

### Backend (.env)

```env
CLIENT_ID="your_spotify_client_id"
CLIENT_SECRET="your_spotify_client_secret"
REDIRECT_URL="http://localhost:8888/callback"
SCOPE="playlist-modify-public,playlist-modify-private,user-library-read"
LOG_LEVEL="INFO"
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

## 📦 Deployment

### Backend Deployment (Example with Docker)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Deployment

```bash
cd frontend
npm run build
# Deploy the 'dist' folder to your hosting service
# (Vercel, Netlify, AWS S3, etc.)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit (`git commit -m 'Add amazing feature'`)
5. Push (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- React & Vite teams for amazing tools
- FastAPI for the modern Python framework
- Tailwind CSS for the utility-first approach
- Spotipy for Spotify API integration
- Playwright for browser automation

## 📧 Contact

Israel Pratt - [@Israel-011](https://github.com/Israel-011)

---

⭐ If you find this project helpful, please give it a star!
