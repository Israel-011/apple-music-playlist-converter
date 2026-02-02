import { SiApplemusic, SiSpotify } from "react-icons/si";
import { FaExchangeAlt } from "react-icons/fa";

const Header = () => {
  return (
    <header className="w-full py-8 px-4">
      <div className="max-w-4xl mx-auto text-center">
        <div className="flex items-center justify-center gap-4 mb-4">
          <SiApplemusic className="text-5xl text-apple-red animate-pulse" />
          <FaExchangeAlt className="text-3xl text-primary-400" />
          <SiSpotify className="text-5xl text-spotify-green animate-pulse" />
        </div>
        <h1 className="text-5xl font-bold bg-gradient-to-r from-apple-red via-primary-400 to-spotify-green bg-clip-text text-transparent mb-3">
          Playlist Converter
        </h1>
        <p className="text-gray-400 text-lg">
          Convert your Apple Music playlists to Spotify with ease
        </p>
      </div>
    </header>
  );
};

export default Header;
