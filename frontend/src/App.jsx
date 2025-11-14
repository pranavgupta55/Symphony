/**
 * Symphony AI - Main Application Component
 */
import { useState } from 'react';
import useAnalysisStore from './store/useAnalysisStore';
import UploadForm from './components/UploadForm';
import ResultsDashboard from './components/ResultsDashboard';
import ProgressIndicator from './components/ProgressIndicator';

function App() {
  const { analysisResults, resetAnalysis } = useAnalysisStore();

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="text-3xl mr-3">🎵</div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Symphony AI</h1>
                <p className="text-sm text-gray-600">
                  Multi-Modal Financial Analysis Platform
                </p>
              </div>
            </div>
            {analysisResults && (
              <button
                onClick={resetAnalysis}
                className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition"
              >
                New Analysis
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {!analysisResults ? (
          <div>
            {/* Hero Section */}
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Decode Earnings Calls with AI
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Analyze vocal biomarkers, sentiment, and financial charts to uncover hidden
                insights and detect deception in executive communications
              </p>
            </div>

            {/* Features */}
            <div className="grid md:grid-cols-3 gap-6 mb-12">
              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="text-4xl mb-3">🎤</div>
                <h3 className="text-lg font-semibold mb-2">Vocal Biomarkers</h3>
                <p className="text-gray-600 text-sm">
                  Extract MFCCs, pitch, jitter, and shimmer to detect confidence and stress
                </p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="text-4xl mb-3">📊</div>
                <h3 className="text-lg font-semibold mb-2">FinBERT Sentiment</h3>
                <p className="text-gray-600 text-sm">
                  Financial-tuned NLP model analyzes tone and sentiment across the call
                </p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="text-4xl mb-3">🤖</div>
                <h3 className="text-lg font-semibold mb-2">Claude AI Insights</h3>
                <p className="text-gray-600 text-sm">
                  Advanced AI synthesis identifies risks, opportunities, and red flags
                </p>
              </div>
            </div>

            {/* Upload Form */}
            <UploadForm />
          </div>
        ) : (
          <ResultsDashboard />
        )}
      </main>

      {/* Progress Indicator */}
      <ProgressIndicator />

      {/* Footer */}
      <footer className="mt-16 pb-8 text-center text-gray-500 text-sm">
        <p>Symphony AI © 2025 | Multi-Modal Financial Analysis</p>
      </footer>
    </div>
  );
}

export default App;
