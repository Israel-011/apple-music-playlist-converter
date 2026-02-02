import { useState } from "react";
import Header from "./components/Header";
import LoadingSpinner from "./components/LoadingSpinner";
import StatusDisplay from "./components/StatusDisplay";
import { playlistService } from "./services/api";
import { FaSpotify, FaLink } from "react-icons/fa";

function App() {
  const [applePlaylistUrl, setApplePlaylistUrl] = useState("");
  const [spotifyPlaylistName, setSpotifyPlaylistName] = useState("");
  const [isPublic, setIsPublic] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [conversionStatus, setConversionStatus] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleSpotifyAuth = async () => {
    try {
      setError("");
      const data = await playlistService.authenticateSpotify();
      if (data.auth_url) {
        window.location.href = data.auth_url;
      }
    } catch (err) {
      setError(err.error || "Failed to authenticate with Spotify");
    }
  };

  const handleConvert = async (e) => {
    e.preventDefault();

    if (!applePlaylistUrl.trim()) {
      setError("Please enter an Apple Music playlist URL");
      return;
    }

    if (!spotifyPlaylistName.trim()) {
      setError("Please enter a name for your Spotify playlist");
      return;
    }

    setLoading(true);
    setError("");
    setConversionStatus(null);

    try {
      const result = await playlistService.convertPlaylist(
        applePlaylistUrl,
        spotifyPlaylistName,
        isPublic,
      );

      setConversionStatus({
        status: "completed",
        successCount: result.success_count || 0,
        failedCount: result.failed_count || 0,
        totalCount: result.total_count || 0,
      });

      // Clear form
      setApplePlaylistUrl("");
      setSpotifyPlaylistName("");
    } catch (err) {
      setError(err.error || "Failed to convert playlist. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <Header />

        <main className="space-y-6">
          {/* Authentication Section */}
          {!isAuthenticated && (
            <div className="card text-center space-y-4">
              <h2 className="text-2xl font-semibold text-white">
                Connect Your Spotify Account
              </h2>
              <p className="text-gray-400">
                First, you need to authenticate with Spotify to create playlists
              </p>
              <button
                onClick={handleSpotifyAuth}
                className="btn-primary inline-flex items-center gap-2"
              >
                <FaSpotify className="text-xl" />
                Connect Spotify
              </button>
            </div>
          )}

          {/* Conversion Form */}
          <div className="card">
            <h2 className="text-2xl font-semibold text-white mb-6">
              Convert Playlist
            </h2>

            <form onSubmit={handleConvert} className="space-y-6">
              {/* Apple Music URL Input */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  <FaLink className="inline mr-2" />
                  Apple Music Playlist URL
                </label>
                <input
                  type="url"
                  value={applePlaylistUrl}
                  onChange={(e) => setApplePlaylistUrl(e.target.value)}
                  placeholder="https://music.apple.com/us/playlist/..."
                  className="input-field"
                  required
                />
                <p className="text-gray-500 text-sm mt-2">
                  Example:
                  https://music.apple.com/us/playlist/your-playlist/pl.xxxxx
                </p>
              </div>

              {/* Spotify Playlist Name Input */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Spotify Playlist Name
                </label>
                <input
                  type="text"
                  value={spotifyPlaylistName}
                  onChange={(e) => setSpotifyPlaylistName(e.target.value)}
                  placeholder="My Awesome Playlist"
                  className="input-field"
                  required
                />
              </div>

              {/* Public/Private Toggle */}
              <div className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  id="isPublic"
                  checked={isPublic}
                  onChange={(e) => setIsPublic(e.target.checked)}
                  className="w-5 h-5 text-primary-500 bg-gray-700 border-gray-600 rounded focus:ring-primary-500 focus:ring-2"
                />
                <label htmlFor="isPublic" className="text-gray-300">
                  Make playlist public
                </label>
              </div>

              {/* Error Message */}
              {error && (
                <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-4">
                  <p className="text-red-400 text-sm">{error}</p>
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? "Converting..." : "Convert Playlist"}
              </button>
            </form>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="card">
              <LoadingSpinner message="Converting your playlist..." />
              <p className="text-center text-gray-400 mt-4 text-sm">
                This may take a few minutes depending on the playlist size
              </p>
            </div>
          )}

          {/* Conversion Status */}
          {conversionStatus && !loading && (
            <StatusDisplay
              status={conversionStatus.status}
              successCount={conversionStatus.successCount}
              failedCount={conversionStatus.failedCount}
              totalCount={conversionStatus.totalCount}
            />
          )}

          {/* Info Section */}
          <div className="card bg-primary-900/20 border-primary-500/30">
            <h3 className="text-lg font-semibold text-white mb-3">
              How it works
            </h3>
            <ol className="space-y-2 text-gray-300 text-sm list-decimal list-inside">
              <li>Copy the URL of your Apple Music playlist</li>
              <li>Paste it above and give your new Spotify playlist a name</li>
              <li>Click "Convert Playlist" and wait for the magic to happen</li>
              <li>Find your new playlist in your Spotify account</li>
            </ol>
          </div>
        </main>

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-500 text-sm">
          <p>Made with ❤️ by Israel Pratt</p>
          <p className="mt-2">
            Note: Some songs may not be available on Spotify
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
