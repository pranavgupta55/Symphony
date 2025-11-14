/**
 * Progress Indicator Component
 */
import useAnalysisStore from '../store/useAnalysisStore';

const ProgressIndicator = () => {
  const { isLoading, analysisStatus, error } = useAnalysisStore();

  if (!isLoading && !error) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full mx-4">
        {error ? (
          <div>
            <div className="text-red-600 text-center mb-4">
              <svg
                className="w-16 h-16 mx-auto mb-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <h3 className="text-xl font-bold">Analysis Failed</h3>
            </div>
            <p className="text-gray-700 text-center mb-4">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition"
            >
              Try Again
            </button>
          </div>
        ) : (
          <div>
            <div className="text-center mb-6">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
              <h3 className="text-xl font-bold text-gray-800">
                Analyzing Earnings Call...
              </h3>
              <p className="text-gray-600 mt-2">
                {analysisStatus?.status === 'processing'
                  ? 'Processing your audio file'
                  : 'Starting analysis...'}
              </p>
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-gray-200 rounded-full h-2.5 mb-4">
              <div
                className="bg-blue-600 h-2.5 rounded-full transition-all duration-500"
                style={{ width: `${analysisStatus?.progress || 0}%` }}
              ></div>
            </div>

            <div className="text-center text-sm text-gray-600">
              {analysisStatus?.progress || 0}% complete
            </div>

            {/* Status Steps */}
            <div className="mt-6 space-y-2 text-sm">
              <div
                className={`flex items-center ${
                  (analysisStatus?.progress || 0) >= 20
                    ? 'text-green-600'
                    : 'text-gray-400'
                }`}
              >
                <span className="mr-2">
                  {(analysisStatus?.progress || 0) >= 20 ? '✓' : '○'}
                </span>
                Audio Transcription
              </div>
              <div
                className={`flex items-center ${
                  (analysisStatus?.progress || 0) >= 35
                    ? 'text-green-600'
                    : 'text-gray-400'
                }`}
              >
                <span className="mr-2">
                  {(analysisStatus?.progress || 0) >= 35 ? '✓' : '○'}
                </span>
                Vocal Feature Extraction
              </div>
              <div
                className={`flex items-center ${
                  (analysisStatus?.progress || 0) >= 50
                    ? 'text-green-600'
                    : 'text-gray-400'
                }`}
              >
                <span className="mr-2">
                  {(analysisStatus?.progress || 0) >= 50 ? '✓' : '○'}
                </span>
                Sentiment Analysis
              </div>
              <div
                className={`flex items-center ${
                  (analysisStatus?.progress || 0) >= 65
                    ? 'text-green-600'
                    : 'text-gray-400'
                }`}
              >
                <span className="mr-2">
                  {(analysisStatus?.progress || 0) >= 65 ? '✓' : '○'}
                </span>
                Chart Analysis
              </div>
              <div
                className={`flex items-center ${
                  (analysisStatus?.progress || 0) >= 75
                    ? 'text-green-600'
                    : 'text-gray-400'
                }`}
              >
                <span className="mr-2">
                  {(analysisStatus?.progress || 0) >= 75 ? '✓' : '○'}
                </span>
                Multi-Modal Fusion
              </div>
              <div
                className={`flex items-center ${
                  (analysisStatus?.progress || 0) >= 90
                    ? 'text-green-600'
                    : 'text-gray-400'
                }`}
              >
                <span className="mr-2">
                  {(analysisStatus?.progress || 0) >= 90 ? '✓' : '○'}
                </span>
                AI Analysis Generation
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProgressIndicator;
