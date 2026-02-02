const LoadingSpinner = ({ message = "Loading..." }) => {
  return (
    <div className="flex flex-col items-center justify-center space-y-4">
      <div className="relative w-16 h-16">
        <div className="absolute top-0 left-0 w-full h-full border-4 border-primary-200 rounded-full animate-ping opacity-75"></div>
        <div className="absolute top-0 left-0 w-full h-full border-4 border-t-primary-500 border-r-transparent border-b-transparent border-l-transparent rounded-full animate-spin"></div>
      </div>
      <p className="text-gray-300 text-lg animate-pulse">{message}</p>
    </div>
  );
};

export default LoadingSpinner;
