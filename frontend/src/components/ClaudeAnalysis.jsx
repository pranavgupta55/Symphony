/**
 * Claude AI Analysis Panel with Collapsible Sections
 */
import { useState } from 'react';

const CollapsibleSection = ({ title, children, defaultOpen = false }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="border border-gray-200 rounded-lg mb-3">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-4 py-3 flex items-center justify-between bg-gray-50 hover:bg-gray-100 transition rounded-lg"
      >
        <span className="font-semibold text-gray-800">{title}</span>
        <svg
          className={`w-5 h-5 text-gray-600 transition-transform ${
            isOpen ? 'rotate-180' : ''
          }`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>
      {isOpen && <div className="p-4">{children}</div>}
    </div>
  );
};

const ClaudeAnalysis = ({ analysis }) => {
  if (!analysis) {
    return <p className="text-gray-500">No AI analysis available</p>;
  }

  return (
    <div className="space-y-4">
      {/* Executive Summary - Always Open */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="font-bold text-lg text-blue-900 mb-2">Executive Summary</h3>
        <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">
          {analysis.executive_summary || 'No summary available'}
        </p>
      </div>

      {/* Risk Indicators */}
      <CollapsibleSection title="Risk Indicators" defaultOpen={true}>
        {analysis.risk_indicators && analysis.risk_indicators.length > 0 ? (
          <ul className="space-y-2">
            {analysis.risk_indicators.map((risk, index) => (
              <li key={index} className="flex items-start">
                <span className="text-red-600 mr-2">⚠️</span>
                <span className="text-gray-700">{risk}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-500">No significant risks identified</p>
        )}
      </CollapsibleSection>

      {/* Opportunities */}
      <CollapsibleSection title="Opportunities" defaultOpen={true}>
        {analysis.opportunities && analysis.opportunities.length > 0 ? (
          <ul className="space-y-2">
            {analysis.opportunities.map((opportunity, index) => (
              <li key={index} className="flex items-start">
                <span className="text-green-600 mr-2">✓</span>
                <span className="text-gray-700">{opportunity}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-500">No specific opportunities highlighted</p>
        )}
      </CollapsibleSection>

      {/* Red Flags */}
      {analysis.red_flags && analysis.red_flags.length > 0 && (
        <CollapsibleSection title="Red Flags" defaultOpen={true}>
          <div className="bg-red-50 border-l-4 border-red-500 p-3 rounded">
            <ul className="space-y-2">
              {analysis.red_flags.map((flag, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-red-700 mr-2">🚩</span>
                  <span className="text-red-800 font-medium">{flag}</span>
                </li>
              ))}
            </ul>
          </div>
        </CollapsibleSection>
      )}

      {/* Confidence Assessment */}
      <CollapsibleSection title="Confidence Assessment">
        <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">
          {analysis.confidence_assessment || 'No confidence assessment available'}
        </p>
      </CollapsibleSection>

      {/* Overall Recommendation */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-lg p-4">
        <h3 className="font-bold text-lg text-purple-900 mb-2">
          Overall Recommendation
        </h3>
        <p className="text-gray-700 whitespace-pre-wrap leading-relaxed font-medium">
          {analysis.overall_recommendation || 'No recommendation available'}
        </p>
      </div>
    </div>
  );
};

export default ClaudeAnalysis;
