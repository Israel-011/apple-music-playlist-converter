import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const playlistService = {
  // Convert Apple Music playlist to Spotify
  convertPlaylist: async (
    applePlaylistUrl,
    spotifyPlaylistName,
    isPublic = false,
  ) => {
    try {
      const response = await api.post("/api/convert", {
        apple_playlist_url: applePlaylistUrl,
        spotify_playlist_name: spotifyPlaylistName,
        is_public: isPublic,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: "Failed to convert playlist" };
    }
  },

  // Get conversion status
  getConversionStatus: async (conversionId) => {
    try {
      const response = await api.get(`/api/conversion/${conversionId}`);
      return response.data;
    } catch (error) {
      throw (
        error.response?.data || { error: "Failed to get conversion status" }
      );
    }
  },

  // Authenticate with Spotify
  authenticateSpotify: async () => {
    try {
      const response = await api.get("/api/auth/spotify");
      return response.data;
    } catch (error) {
      throw (
        error.response?.data || { error: "Failed to authenticate with Spotify" }
      );
    }
  },

  // Check Spotify authentication status
  checkSpotifyAuth: async () => {
    try {
      const response = await api.get("/api/auth/spotify/status");
      return response.data;
    } catch (error) {
      return { authenticated: false };
    }
  },
};

export default api;
