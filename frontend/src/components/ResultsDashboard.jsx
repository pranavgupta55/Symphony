/**
 * Main Results Dashboard Component
 */
import { useState } from 'react';
import useAnalysisStore from '../store/useAnalysisStore';
import TranscriptViewer from './TranscriptViewer';
import ConfidenceTimeline from './ConfidenceTimeline';
import ClaudeAnalysis from './ClaudeAnalysis';

const ResultsDashboard = () => {
  const { analysisResults, currentJobId } = useAnalysisStore();
  const [activeTab, setActiveTab] = useState('overview');

  if (!analysisResults) {
    return null;
  }

  const downloadJSON = () => {
    const dataStr = JSON.stringify(analysisResults, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `symphony-analysis-${currentJobId}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'transcript', label: 'Transcript', icon: '📝' },
    { id: 'confidence', label: 'Confidence Analysis', icon: '📈' },
    { id: 'ai-analysis', label: 'AI Analysis', icon: '🤖' },
  ];

  return (
    <div className="bg-white rounded-lg shadow-md p-6 max-w-6xl mx-auto mt-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Analysis Results</h2>
          {analysisResults.company_name && (
            <p className="text-gray-600 mt-1">{analysisResults.company_name}</p>
          )}
        </div>
        <button
          onClick={downloadJSON}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition flex items-center gap-2"
        >
          <span>💾</span>
          Download JSON
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg border border-blue-200">
          <div className="text-sm text-blue-700 font-medium mb-1">Overall Confidence</div>
          <div className="text-2xl font-bold text-blue-900">
            {analysisResults.overall_confidence
              ? `${(analysisResults.overall_confidence * 100).toFixed(0)}%`
              : 'N/A'}
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg border border-green-200">
          <div className="text-sm text-green-700 font-medium mb-1">Sentiment</div>
          <div className="text-2xl font-bold text-green-900 capitalize">
            {analysisResults.overall_sentiment || 'N/A'}
          </div>
        </div>

        <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg border border-purple-200">
          <div className="text-sm text-purple-700 font-medium mb-1">Risk Level</div>
          <div className="text-2xl font-bold text-purple-900 capitalize">
            {analysisResults.risk_level || 'N/A'}
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <div className="flex gap-1 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-3 font-medium transition whitespace-nowrap ${
                activeTab === tab.id
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      <div className="min-h-96">
        {activeTab === 'overview' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-3">Confidence Timeline</h3>
              {analysisResults.audio_features?.confidence_timeline && (
                <ConfidenceTimeline
                  timeline={analysisResults.audio_features.confidence_timeline}
                />
              )}
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-3">Key Insights</h3>
              {analysisResults.fusion_results?.fusion_insights && (
                <ul className="space-y-2">
                  {analysisResults.fusion_results.fusion_insights.map((insight, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-blue-600 mr-2">•</span>
                      <span className="text-gray-700">{insight}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>

            {analysisResults.fusion_results?.discrepancies &&
              analysisResults.fusion_results.discrepancies.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold mb-3 text-red-700">
                    Detected Discrepancies
                  </h3>
                  <div className="space-y-2">
                    {analysisResults.fusion_results.discrepancies.map((disc, index) => (
                      <div
                        key={index}
                        className="bg-red-50 border-l-4 border-red-500 p-3 rounded"
                      >
                        <div className="font-medium text-red-800">{disc.type}</div>
                        <div className="text-sm text-red-700">{disc.description}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
          </div>
        )}

        {activeTab === 'transcript' && (
          <div>
            <h3 className="text-lg font-semibold mb-3">Full Transcript</h3>
            {analysisResults.sentiment_analysis?.segments && (
              <TranscriptViewer segments={analysisResults.sentiment_analysis.segments} />
            )}
          </div>
        )}

        {activeTab === 'confidence' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-3">Vocal Confidence Over Time</h3>
              {analysisResults.audio_features?.confidence_timeline && (
                <ConfidenceTimeline
                  timeline={analysisResults.audio_features.confidence_timeline}
                />
              )}
            </div>

            {analysisResults.audio_features?.stress_indicators &&
              analysisResults.audio_features.stress_indicators.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold mb-3">Stress Indicators</h3>
                  <div className="space-y-2">
                    {analysisResults.audio_features.stress_indicators.map((indicator, index) => (
                      <div
                        key={index}
                        className="bg-yellow-50 border-l-4 border-yellow-500 p-3 rounded"
                      >
                        <div className="font-medium text-yellow-800 capitalize">
                          {indicator.type.replace(/_/g, ' ')}
                        </div>
                        <div className="text-sm text-yellow-700">{indicator.description}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
          </div>
        )}

        {activeTab === 'ai-analysis' && (
          <div>
            <h3 className="text-lg font-semibold mb-4">Claude AI Analysis</h3>
            {analysisResults.claude_analysis && (
              <ClaudeAnalysis analysis={analysisResults.claude_analysis} />
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsDashboard;
