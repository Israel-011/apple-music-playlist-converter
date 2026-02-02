import { FaCheckCircle, FaTimesCircle, FaMusic } from "react-icons/fa";

const StatusDisplay = ({ status, successCount, failedCount, totalCount }) => {
  return (
    <div className="card space-y-4 animate-fade-in">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold text-white">Conversion Status</h3>
        {status === "completed" && (
          <FaCheckCircle className="text-3xl text-green-500" />
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gray-700/50 rounded-lg p-4 text-center">
          <FaMusic className="text-3xl text-primary-400 mx-auto mb-2" />
          <p className="text-gray-400 text-sm">Total Songs</p>
          <p className="text-2xl font-bold text-white">{totalCount}</p>
        </div>

        <div className="bg-gray-700/50 rounded-lg p-4 text-center">
          <FaCheckCircle className="text-3xl text-green-500 mx-auto mb-2" />
          <p className="text-gray-400 text-sm">Successful</p>
          <p className="text-2xl font-bold text-green-400">{successCount}</p>
        </div>

        <div className="bg-gray-700/50 rounded-lg p-4 text-center">
          <FaTimesCircle className="text-3xl text-red-500 mx-auto mb-2" />
          <p className="text-gray-400 text-sm">Failed</p>
          <p className="text-2xl font-bold text-red-400">{failedCount}</p>
        </div>
      </div>

      {status === "completed" && (
        <div className="bg-green-500/10 border border-green-500/50 rounded-lg p-4">
          <p className="text-green-400 text-center font-semibold">
            ✨ Conversion completed successfully! Check your Spotify account.
          </p>
        </div>
      )}

      {failedCount > 0 && (
        <div className="bg-yellow-500/10 border border-yellow-500/50 rounded-lg p-4">
          <p className="text-yellow-400 text-sm">
            ⚠️ Some songs couldn't be found on Spotify. They might not be
            available in the Spotify catalog.
          </p>
        </div>
      )}
    </div>
  );
};

export default StatusDisplay;
