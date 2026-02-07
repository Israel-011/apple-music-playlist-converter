"""
FastAPI backend for the Playlist Converter frontend.
This provides REST API endpoints for the React frontend.
"""

from typing import Optional
from urllib.parse import urlencode

import requests
import spotipy
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from backend.apple_music_lib import get_apple_music_songs
from backend.config import settings
from backend.logger_lib import create_logger
from backend.main import create_spotify_playlist
from backend.models import SpotifyCredentials

# ===== In-memory token store (single-user for now) =====
spotify_token: dict | None = None

FRONTEND_URL = "http://localhost:5173"
BACKEND_REDIRECT_URI = (
    settings.REDIRECT_URL or "http://localhost:8000/api/auth/spotify/callback"
)

# Create FastAPI app
app = FastAPI(
    title="Playlist Converter API",
    description="Convert Apple Music playlists to Spotify",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = create_logger(name="api")


# Request/Response Models
class ConvertPlaylistRequest(BaseModel):
    apple_playlist_url: str
    spotify_playlist_name: str
    is_public: bool = False


class ConvertPlaylistResponse(BaseModel):
    status: str
    message: str
    success_count: int
    failed_count: int
    total_count: int


class AuthResponse(BaseModel):
    authenticated: bool
    auth_url: Optional[str] = None


# ===== Helpers =====
def get_spotify_auth_url() -> str:
    """
    Generate Spotify authorization URL without using SpotifyOAuth.
    This avoids the port binding issue.
    """
    # Spotify authorization endpoint
    auth_url = "https://accounts.spotify.com/authorize"

    # Convert scope to space-separated string if it's a list
    scope = settings.SCOPE
    if isinstance(scope, list):
        scope = " ".join(scope)

    # Build query parameters
    params = {
        "client_id": settings.CLIENT_ID,
        "response_type": "code",
        "redirect_uri": BACKEND_REDIRECT_URI,
        "scope": scope,
        # "show_dialog": "false",
    }

    return f"{auth_url}?{urlencode(params)}"


def exchange_code_for_token(code: str) -> dict:
    """
    Exchange authorization code for access token using direct HTTP request.
    This is the correct server-side approach that doesn't start a local server.
    """
    token_url = "https://accounts.spotify.com/api/token"

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": BACKEND_REDIRECT_URI,
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code != 200:
        logger.error(f"Token exchange failed: {response.text}")
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to exchange code for token: {response.text}",
        )

    return response.json()


# API Endpoints
@app.get("/")
async def root():
    return {"message": "Playlist Converter API", "version": "1.0.0", "docs": "/docs"}


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}


# ===== OAuth: start login =====
@app.get("/connect", response_model=AuthResponse)
async def spotify_auth():
    """
    Step 1: Generate Spotify authorization URL and return it to frontend.
    Frontend will redirect user to this URL.
    """
    logger.info("Starting Spotify OAuth flow")
    auth_url = get_spotify_auth_url()
    logger.info(f"Generated Spotify auth URL: {auth_url}")
    return RedirectResponse(auth_url)


# ===== OAuth: callback from Spotify =====
@app.get("/callback")
async def spotify_callback(request: Request):
    """
    Step 2: Spotify redirects here with authorization code.
    Exchange code for access token using direct HTTP request (no local server).
    """
    global spotify_token

    logger.info("Received Spotify OAuth callback")
    code = request.query_params.get("code")
    error = request.query_params.get("error")

    if error:
        logger.error(f"Spotify OAuth error: {error}")
        return RedirectResponse(f"{FRONTEND_URL}?spotify=error")

    if not code:
        logger.error("No code provided in Spotify callback")
        return RedirectResponse(f"{FRONTEND_URL}?spotify=error")

    try:
        # Exchange code for token using direct HTTP request
        # This avoids SpotifyOAuth's port binding issue
        token_info = exchange_code_for_token(code)
        spotify_token = token_info

        logger.info("Spotify token stored successfully")
        logger.debug(f"Token info: {token_info.keys()}")

        return RedirectResponse(f"{FRONTEND_URL}?spotify=success")

    except Exception as e:
        logger.error(f"Failed to exchange code for token: {e}")
        return RedirectResponse(f"{FRONTEND_URL}?spotify=error")


# ===== OAuth: status =====
@app.get("/api/auth/spotify/status")
async def spotify_auth_status():
    global spotify_token

    if not spotify_token or "access_token" not in spotify_token:
        return {"authenticated": False}

    # (Optional) you could check expiry here
    return {"authenticated": True}


# ===== Conversion endpoint =====
@app.post("/api/convert", response_model=ConvertPlaylistResponse)
async def convert_playlist(request: ConvertPlaylistRequest):
    global spotify_token

    try:
        logger.info(f"Starting playlist conversion: {request.spotify_playlist_name}")

        if not spotify_token or "access_token" not in spotify_token:
            raise HTTPException(
                status_code=401, detail="User is not authenticated with Spotify"
            )

        # Get Apple Music songs
        apple_song_list = await get_apple_music_songs(url=request.apple_playlist_url)

        if not apple_song_list:
            raise HTTPException(
                status_code=400,
                detail="Could not fetch songs from Apple Music playlist",
            )

        # Build Spotify client from stored token
        access_token = spotify_token["access_token"]
        sp = spotipy.Spotify(auth=access_token)
        current_user = sp.current_user()
        logger.info(f"Using Spotify user: {current_user.get('id')}")

        # Create Spotify credentials (kept for compatibility, not used for OAuth now)
        spotify_creds = SpotifyCredentials(
            client_id=settings.CLIENT_ID,
            client_secret=settings.CLIENT_SECRET,
            redirect_uri=BACKEND_REDIRECT_URI,
        )

        # Convert to Spotify (now using existing client)
        result = create_spotify_playlist(
            song_list=apple_song_list,
            spotify_creds=spotify_creds,
            playlist_name=request.spotify_playlist_name,
            public=request.is_public,
            sp=sp,
            current_user=current_user,
        )

        total_count = len(apple_song_list)
        success_count = result.get("success_count", total_count)
        failed_count = result.get("failed_count", 0)

        logger.info(f"Conversion completed: {success_count}/{total_count} songs")

        return ConvertPlaylistResponse(
            status="completed",
            message="Playlist converted successfully",
            success_count=success_count,
            failed_count=failed_count,
            total_count=total_count,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Conversion error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to convert playlist: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
