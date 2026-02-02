"""
FastAPI backend for the Playlist Converter frontend.
This provides REST API endpoints for the React frontend.
"""
import asyncio
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

from apple_music_lib import get_apple_music_songs
from config import settings
from logger_lib import create_logger
from main import create_spotify_playlist
from models import SpotifyCredentials

# Create FastAPI app
app = FastAPI(
    title="Playlist Converter API",
    description="Convert Apple Music playlists to Spotify",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
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


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Playlist Converter API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/convert", response_model=ConvertPlaylistResponse)
async def convert_playlist(request: ConvertPlaylistRequest):
    """
    Convert an Apple Music playlist to Spotify.
    
    Args:
        request: Contains the Apple Music playlist URL and Spotify playlist name
        
    Returns:
        Conversion result with success/failed counts
    """
    try:
        logger.info(f"Starting playlist conversion: {request.spotify_playlist_name}")
        
        # Get Apple Music songs
        apple_song_list = await get_apple_music_songs(url=request.apple_playlist_url)
        
        if not apple_song_list:
            raise HTTPException(
                status_code=400,
                detail="Could not fetch songs from Apple Music playlist"
            )
        
        # Create Spotify credentials
        spotify_creds = SpotifyCredentials(
            client_id=settings.CLIENT_ID,
            client_secret=settings.CLIENT_SECRET,
            redirect_uri=settings.REDIRECT_URI,
        )
        
        # Convert to Spotify
        result = create_spotify_playlist(
            song_list=apple_song_list,
            spotify_creds=spotify_creds,
            playlist_name=request.spotify_playlist_name,
            public=request.is_public,
        )
        
        # Calculate statistics (simplified - adjust based on your implementation)
        total_count = len(apple_song_list)
        success_count = total_count  # Adjust this based on actual implementation
        failed_count = 0
        
        logger.info(f"Conversion completed: {success_count}/{total_count} songs")
        
        return ConvertPlaylistResponse(
            status="completed",
            message="Playlist converted successfully",
            success_count=success_count,
            failed_count=failed_count,
            total_count=total_count
        )
        
    except Exception as e:
        logger.error(f"Conversion error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to convert playlist: {str(e)}"
        )


@app.get("/api/auth/spotify", response_model=AuthResponse)
async def spotify_auth():
    """
    Get Spotify authentication URL.
    In a full implementation, this would generate an OAuth URL.
    """
    # This is a simplified version - implement proper OAuth flow
    return AuthResponse(
        authenticated=False,
        auth_url="https://accounts.spotify.com/authorize"
    )


@app.get("/api/auth/spotify/status")
async def spotify_auth_status():
    """Check if user is authenticated with Spotify"""
    # Implement proper session/token checking here
    return {"authenticated": True}  # Simplified


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
