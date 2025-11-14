/**
 * Upload Form Component for Audio and Charts
 */
import { useState } from 'react';
import useAnalysisStore from '../store/useAnalysisStore';
import { analyzeEarningsCall, pollJobStatus } from '../api/client';

const UploadForm = () => {
  const [audioFile, setAudioFile] = useState(null);
  const [chartFiles, setChartFiles] = useState([]);
  const [companyName, setCompanyName] = useState('');
  const [companyContext, setCompanyContext] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const {
    setCurrentJob,
    setAnalysisStatus,
    setAnalysisResults,
    setError,
    setLoading,
    clearError,
    isLoading,
  } = useAnalysisStore();

  const handleAudioChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setAudioFile(file);
      clearError();
    }
  };

  const handleChartChange = (e) => {
    const files = Array.from(e.target.files);
    setChartFiles((prev) => [...prev, ...files]);
    clearError();
  };

  const removeChart = (index) => {
    setChartFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = Array.from(e.dataTransfer.files);
    const audioFiles = files.filter((f) =>
      ['audio/mpeg', 'audio/wav', 'audio/m4a', 'audio/x-m4a'].includes(f.type)
    );
    const imageFiles = files.filter((f) => f.type.startsWith('image/'));

    if (audioFiles.length > 0) {
      setAudioFile(audioFiles[0]);
    }

    if (imageFiles.length > 0) {
      setChartFiles((prev) => [...prev, ...imageFiles]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!audioFile) {
      setError('Please select an audio file');
      return;
    }

    try {
      setLoading(true);
      clearError();

      // Upload and start analysis
      const job = await analyzeEarningsCall(
        audioFile,
        chartFiles,
        companyName,
        companyContext
      );

      setCurrentJob(job.id);

      // Poll for results
      const results = await pollJobStatus(job.id, (status) => {
        setAnalysisStatus(status);
      });

      setAnalysisResults(results);
    } catch (error) {
      setError(error.message || 'Failed to analyze earnings call');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Upload Earnings Call</h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Audio Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Audio File *
          </label>
          <div
            className={`border-2 border-dashed rounded-lg p-6 text-center ${
              dragActive
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-300 hover:border-gray-400'
            } transition-colors`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            {audioFile ? (
              <div className="text-green-600">
                <p className="font-medium">{audioFile.name}</p>
                <p className="text-sm text-gray-500">
                  {(audioFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
                <button
                  type="button"
                  onClick={() => setAudioFile(null)}
                  className="mt-2 text-red-600 hover:text-red-700 text-sm"
                >
                  Remove
                </button>
              </div>
            ) : (
              <>
                <p className="text-gray-600 mb-2">
                  Drag and drop an audio file, or click to browse
                </p>
                <input
                  type="file"
                  accept="audio/mpeg,audio/wav,audio/m4a,audio/x-m4a"
                  onChange={handleAudioChange}
                  className="hidden"
                  id="audio-upload"
                />
                <label
                  htmlFor="audio-upload"
                  className="inline-block bg-blue-600 text-white px-4 py-2 rounded-md cursor-pointer hover:bg-blue-700 transition"
                >
                  Select Audio File
                </label>
                <p className="text-xs text-gray-500 mt-2">
                  Supported formats: MP3, WAV, M4A
                </p>
              </>
            )}
          </div>
        </div>

        {/* Chart Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Financial Charts (Optional)
          </label>
          <input
            type="file"
            accept="image/png,image/jpeg,image/jpg"
            multiple
            onChange={handleChartChange}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-gray-100 file:text-gray-700 hover:file:bg-gray-200"
          />
          {chartFiles.length > 0 && (
            <div className="mt-3 space-y-2">
              {chartFiles.map((file, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between bg-gray-50 p-2 rounded"
                >
                  <span className="text-sm text-gray-700">{file.name}</span>
                  <button
                    type="button"
                    onClick={() => removeChart(index)}
                    className="text-red-600 hover:text-red-700 text-sm"
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Company Name */}
        <div>
          <label
            htmlFor="company-name"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Company Name (Optional)
          </label>
          <input
            type="text"
            id="company-name"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            placeholder="e.g., Tesla Inc."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Company Context */}
        <div>
          <label
            htmlFor="company-context"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Company Context (Optional)
          </label>
          <textarea
            id="company-context"
            value={companyContext}
            onChange={(e) => setCompanyContext(e.target.value)}
            placeholder="Provide additional context about the company, industry, or specific concerns..."
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={!audioFile || isLoading}
          className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium transition"
        >
          {isLoading ? 'Analyzing...' : 'Analyze Earnings Call'}
        </button>
      </form>
    </div>
  );
};

export default UploadForm;
