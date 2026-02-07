import asyncio
import json
import logging
from time import sleep
from typing import Any, Final, Optional, TypeAlias

import spotipy
from rapidfuzz import fuzz
from spotipy.oauth2 import SpotifyOAuth

from backend.apple_music_lib import get_apple_music_songs
from backend.config import settings
from backend.logger_lib import create_logger
from backend.models import SpotifyCredentials

# TODO: Add Pydantic for data validation
# TODO: Add way to save songs that failed to be added

SpotifyUser: TypeAlias = dict[str, str | Any] | Any
WAIT_TIME: Final[int] = 5
FUZZY_THRESHOLD: Final[int] = 80  # Minimum similarity score for fuzzy matching


def get_playlist_id(
    *,
    sp: spotipy.Spotify,
    current_user: SpotifyUser,
    playlist_name: str,
    public: bool,
    description: str,
) -> str:
    """Get Spotify playlist ID. If playlist doesn't exist, create it."""
    logger = create_logger(name=get_playlist_id.__name__)
    logger.debug("Getting playlist ID")

    failed_attempts: int = 0
    FAILED_LIMIT: Final[int] = 5
    offset: int = 0

    playlist_id: str = ""

    # Placeholder function to get playlist ID
    while all([playlist_id == "", failed_attempts < FAILED_LIMIT]):
        try:
            user_playlists_response: Any = sp.user_playlists(
                user=current_user["id"], limit=50, offset=offset
            )
            logger.debug(f"{user_playlists_response=}\n{failed_attempts=}\n")

            # Get playlist ID if it exists
            for playlist in user_playlists_response["items"]:
                if playlist_name == playlist["name"]:
                    playlist_id = playlist["id"]
                    logger.info(f"Found playlist: '{playlist_name}'")
                    break

            # Create playlist if it doesn't exist
            if playlist_id:
                break

            if user_playlists_response.get("next", None) is None:
                break
            offset += 50
        except Exception as e:
            logger.exception(e)
            failed_attempts += 1
        finally:
            sleep(WAIT_TIME)

    if not playlist_id:
        logger.info(f"Playlist '{playlist_name}' not found. Creating...")
        create_user_playlist_response: Any = sp.user_playlist_create(
            user=current_user["id"],
            name=playlist_name,
            public=public,
            description=description,
        )
        logger.debug(f"{create_user_playlist_response=}\n")
        playlist_id = create_user_playlist_response["id"]
        logger.info(f"Created playlist: '{playlist_name}'")

    return playlist_id


def find_song_with_fuzzy_match(
    sp: spotipy.Spotify,
    song_name: str,
    artist_name: str,
    logger: Any,
) -> Optional[str]:
    """
    Find a song on Spotify using fuzzy matching if exact match fails.

    Args:
        sp: Spotify client
        song_name: Name of the song to search for
        artist_name: Name of the artist
        logger: Logger instance

    Returns:
        Spotify track URI if found, None otherwise
    """
    # Try exact match first
    try:
        exact_search = sp.search(
            q=f"track:'{song_name}' artist:'{artist_name}'", type="track", limit=1
        )
        if exact_search["tracks"]["items"]:
            track_uri = exact_search["tracks"]["items"][0]["id"]
            logger.info(f"✓ Exact match found: '{song_name}' by '{artist_name}'")
            return track_uri
    except Exception as e:
        logger.debug(f"Exact search failed: {e}")

    # If exact match fails, try broader search with fuzzy matching
    try:
        logger.info(f"Trying fuzzy match for: '{song_name}' by '{artist_name}'")

        # Broader search without strict matching
        fuzzy_search = sp.search(
            q=f"{song_name} {artist_name}",
            type="track",
            limit=10,  # Get multiple results for fuzzy comparison
        )

        if not fuzzy_search["tracks"]["items"]:
            logger.warning(f"✗ No results found for '{song_name}' by '{artist_name}'")
            return None

        # Find best match using fuzzy matching
        best_match = None
        best_score = 0

        for track in fuzzy_search["tracks"]["items"]:
            spotify_song_name = track["name"].lower()
            spotify_artists = [artist["name"].lower() for artist in track["artists"]]
            primary_artist = spotify_artists[0] if spotify_artists else ""

            # Calculate similarity scores
            song_similarity = fuzz.ratio(song_name.lower(), spotify_song_name)

            # Check if the primary artist matches (fuzzy)
            artist_similarity = max(
                fuzz.ratio(artist_name.lower(), artist.lower())
                for artist in spotify_artists
            )

            # Weighted score: song name is more important, but artist must match
            # Artist match must be above threshold to be considered
            if artist_similarity >= FUZZY_THRESHOLD:
                combined_score = (song_similarity * 0.7) + (artist_similarity * 0.3)

                logger.debug(
                    f"Candidate: '{track['name']}' by '{primary_artist}' "
                    f"(Song: {song_similarity}%, Artist: {artist_similarity}%, "
                    f"Combined: {combined_score:.1f}%)"
                )

                if combined_score > best_score and combined_score >= FUZZY_THRESHOLD:
                    best_score = combined_score
                    best_match = track

        if best_match:
            best_artist = best_match["artists"][0]["name"]
            logger.info(
                f"✓ Fuzzy match found ({best_score:.1f}%): "
                f"'{best_match['name']}' by '{best_artist}' "
                f"for '{song_name}' by '{artist_name}'"
            )
            return best_match["id"]
        else:
            logger.warning(
                f"✗ No suitable match found for '{song_name}' by '{artist_name}' "
                f"(artist verification failed or score too low)"
            )
            return None

    except Exception as e:
        logger.error(f"Error during fuzzy search: {e}")
        return None


def add_songs_to_playlist(
    sp: spotipy.Spotify,
    playlist_id: str,
    song_list: list[dict[str, str]],
    playlist_name: str,
) -> dict[str, int]:
    """
    Add songs to playlist with improved fuzzy matching.

    Returns:
        Dictionary with success_count and failed_count
    """
    logger = create_logger(name=add_songs_to_playlist.__name__)
    logger.debug("Adding songs to playlist with fuzzy matching")

    success_count = 0
    failed_count = 0
    failed_songs = []

    # Add songs to playlist
    for idx, song_data in enumerate(song_list, 1):
        try:
            # Extract song information
            song_name = song_data["attributes"]["name"]  # type: ignore
            song_artist = song_data["attributes"]["artistName"]  # type: ignore

            logger.info(
                f"\n[{idx}/{len(song_list)}] Searching for: '{song_name}' by '{song_artist}'"
            )

            # Find song with fuzzy matching
            track_uri = find_song_with_fuzzy_match(sp, song_name, song_artist, logger)

            if track_uri:
                sleep(1.5)

                # Add song to playlist
                add_song_to_playlist_response = sp.playlist_add_items(
                    playlist_id=playlist_id, items=[track_uri]
                )
                logger.info(
                    f"✓ Added '{song_name}' by '{song_artist}' to '{playlist_name}'"
                )
                logger.debug(f"{add_song_to_playlist_response=}\n")
                success_count += 1
            else:
                failed_count += 1
                failed_songs.append(f"{song_name} - {song_artist}")
                logger.error(f"✗ Failed to find '{song_name}' by '{song_artist}'")

        except Exception as e:
            failed_count += 1
            try:
                failed_songs.append(f"{song_name} - {song_artist}")
                logger.error(f"✗ Error adding '{song_name}' by '{song_artist}': {e}")
            except Exception:
                failed_songs.append("Unknown song")
                logger.error(f"✗ Error adding unknown song: {e}")
        finally:
            sleep(WAIT_TIME)

    # Log summary
    logger.info(f"\n{'=' * 60}")
    logger.info("CONVERSION SUMMARY:")
    logger.info(f"Total songs: {len(song_list)}")
    logger.info(f"✓ Successfully added: {success_count}")
    logger.info(f"✗ Failed: {failed_count}")
    logger.info(f"{'=' * 60}\n")

    if failed_songs:
        logger.warning(f"Failed songs ({failed_count}):")
        for song in failed_songs:
            logger.warning(f"  - {song}")

    return {"success_count": success_count, "failed_count": failed_count}


def get_auth_and_current_user(
    *, spotify_creds: SpotifyCredentials, scope: str | list[str]
) -> tuple[spotipy.Spotify, SpotifyUser]:
    """Create a Spotify API Client and get the current user info."""
    logger = create_logger(name=get_auth_and_current_user.__name__)
    logger.debug("Authenticating Spotify user")

    # Authenticate user
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=spotify_creds.client_id,
            client_secret=spotify_creds.client_secret,
            redirect_uri=spotify_creds.redirect_uri,
            scope=scope,
        )
    )

    # Get current user info
    logger.debug("Getting current Spotify user")
    current_user: SpotifyUser = sp.current_user()
    logger.debug(f"{current_user=}\n")

    return (sp, current_user)


def create_spotify_playlist(
    *,
    song_list: list[dict[str, str]],
    spotify_creds: SpotifyCredentials,
    playlist_name: str,
    scope: Optional[str | list[str]] = None,
    public: bool = False,
    description: str = "Apple Music playlist converted to Spotify playlist! Automated with Python :)",
    sp: Optional[spotipy.Spotify] = None,
    current_user: Optional[SpotifyUser] = None,
) -> dict[str, int]:
    """
    Create Spotify playlist and add songs.

    IMPORTANT:
    - For FastAPI: pass in an already-authenticated `sp` and `current_user`
      so we do NOT run SpotifyOAuth here.
    - For CLI usage: you could still fall back to OAuth if sp/current_user is None.

    Returns:
        Dictionary with success_count and failed_count
    """
    # Create logger
    logger = create_logger(name=create_spotify_playlist.__name__, level=logging.DEBUG)
    logger.debug("Creating Spotify playlist")

    if not scope:
        scope = settings.SCOPE
        logger.debug(f"Using default scope: {scope=}")

    # For backend usage: sp and current_user should be provided
    # For CLI usage: authenticate if not provided
    if sp is None or current_user is None:
        logger.info("No authenticated Spotify client provided, authenticating...")
        sp, current_user = get_auth_and_current_user(
            spotify_creds=spotify_creds, scope=scope
        )

    # Check if playlist already exists. If not, create it.
    playlist_id: str = get_playlist_id(
        sp=sp,
        current_user=current_user,
        playlist_name=playlist_name,
        public=public,
        description=description,
    )

    # Add songs to playlist and return statistics
    return add_songs_to_playlist(
        sp=sp, playlist_id=playlist_id, song_list=song_list, playlist_name=playlist_name
    )


def read_json(*, filename: str) -> list[dict[str, str]]:
    # Create logger
    logger = create_logger(name=read_json.__name__)
    logger.debug(f"Reading JSON file: {filename}")

    # Read JSON file
    with open(filename, "r") as f:
        apple_song_list = json.load(f)

    return apple_song_list


async def async_main() -> None:
    # TODO: Get input dynamically (i.e., from user)
    #   - playlist url
    #   - playlist name

    url: str = "https://music.apple.com/us/playlist/gymbro/pl.u-55D6X8qU63EXGbj"
    apple_song_list = await get_apple_music_songs(url=url)
    # apple_song_list: list[dict[str, str]] = read_json(filename="apple_music_songs.json")
    spotify_creds: SpotifyCredentials = SpotifyCredentials(
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET,
        redirect_uri=settings.REDIRECT_URL,
    )

    stats = create_spotify_playlist(
        song_list=apple_song_list,
        spotify_creds=spotify_creds,
        playlist_name="GymBro",
    )

    print("\n✓ Conversion complete!")
    print(f"  Successfully added: {stats['success_count']} songs")
    print(f"  Failed: {stats['failed_count']} songs")


def main() -> None:
    if __name__ == "__main__":
        asyncio.run(async_main())


main()
