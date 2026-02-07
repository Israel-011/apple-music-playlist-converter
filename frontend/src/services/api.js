import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

console.log("[api.js] Loaded with API_BASE_URL:", API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 60000, // 60 second timeout
});

// Helper function to extract error details
const extractErrorDetails = (error) => {
  // Network error (no response)
  if (!error.response) {
    if (error.code === "ECONNABORTED") {
      return {
        message: "Request timeout - the server took too long to respond",
        code: "TIMEOUT",
        status: 0,
      };
    }
    if (error.message === "Network Error") {
      return {
        message: "Network error - unable to connect to the server. Please check if the backend is running.",
        code: "NETWORK_ERROR",
        status: 0,
      };
    }
    return {
      message: error.message || "Unknown error occurred",
      code: "UNKNOWN_ERROR",
      status: 0,
    };
  }

  // Server responded with error
  const response = error.response;
  const data = response.data;

  // Extract error message from various possible formats
  let message = "An error occurred";
  if (typeof data === "string") {
    message = data;
  } else if (data?.detail) {
    message = typeof data.detail === "string" ? data.detail : JSON.stringify(data.detail);
  } else if (data?.message) {
    message = data.message;
  } else if (data?.error) {
    message = data.error;
  }

  return {
    message,
    status: response.status,
    code: data?.code || `HTTP_${response.status}`,
    data: data,
  };
};

// Log every request going out
api.interceptors.request.use(
  (config) => {
    console.log(
      "[API REQUEST]",
      config.method.toUpperCase(),
      config.url,
      config.data || "",
    );
    return config;
  },
  (error) => {
    console.error("[API REQUEST ERROR]", error);
    return Promise.reject(error);
  }
);

// Log every response coming back
api.interceptors.response.use(
  (response) => {
    console.log("[API RESPONSE]", response.config.url, response.data);
    return response;
  },
  (error) => {
    const errorDetails = extractErrorDetails(error);
    console.error(
      "[API ERROR]",
      error.config?.url,
      errorDetails,
    );
    return Promise.reject(errorDetails);
  },
);

export const playlistService = {
  convertPlaylist: async (
    applePlaylistUrl,
    spotifyPlaylistName,
    isPublic = false,
  ) => {
    console.log("[convertPlaylist] Starting conversion...");
    try {
      const response = await api.post("/api/convert", {
        apple_playlist_url: applePlaylistUrl,
        spotify_playlist_name: spotifyPlaylistName,
        is_public: isPublic,
      });
      console.log("[convertPlaylist] Success:", response.data);
      return response.data;
    } catch (errorDetails) {
      console.error("[convertPlaylist] Error:", errorDetails);
      throw {
        error: errorDetails.message || "Failed to convert playlist",
        ...errorDetails,
      };
    }
  },

  getConversionStatus: async (conversionId) => {
    console.log("[getConversionStatus] Checking status for:", conversionId);
    try {
      const response = await api.get(`/api/conversion/${conversionId}`);
      console.log("[getConversionStatus] Status:", response.data);
      return response.data;
    } catch (errorDetails) {
      console.error("[getConversionStatus] Error:", errorDetails);
      throw {
        error: errorDetails.message || "Failed to get conversion status",
        ...errorDetails,
      };
    }
  },

  authenticateSpotify: async () => {
    console.log("[authenticateSpotify] Requesting Spotify login URL...");
    try {
      const response = await api.get("/api/auth/spotify");
      console.log(
        "[authenticateSpotify] Received redirect URL:",
        response.data,
      );
      return response.data;
    } catch (errorDetails) {
      console.error("[authenticateSpotify] Error:", errorDetails);
      throw {
        error: errorDetails.message || "Failed to authenticate with Spotify",
        ...errorDetails,
      };
    }
  },

  checkSpotifyAuth: async () => {
    console.log("[checkSpotifyAuth] Checking Spotify auth status...");
    try {
      const response = await api.get("/api/auth/spotify/status");
      console.log("[checkSpotifyAuth] Status:", response.data);
      return response.data;
    } catch (errorDetails) {
      console.warn("[checkSpotifyAuth] Not authenticated:", errorDetails);
      return { authenticated: false };
    }
  },
};

export default api;
