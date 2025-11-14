/**
 * Transcript Viewer with Sentiment Highlighting
 */
const TranscriptViewer = ({ segments }) => {
  if (!segments || segments.length === 0) {
    return <p className="text-gray-500">No transcript available</p>;
  }

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'positive':
        return 'bg-green-100 border-green-300 text-green-800';
      case 'negative':
        return 'bg-red-100 border-red-300 text-red-800';
      case 'neutral':
      default:
        return 'bg-gray-100 border-gray-300 text-gray-800';
    }
  };

  const getSpeakerColor = (speaker) => {
    if (speaker?.includes('CEO')) return 'text-blue-700 font-semibold';
    if (speaker?.includes('CFO')) return 'text-purple-700 font-semibold';
    if (speaker?.includes('Analyst')) return 'text-orange-700';
    return 'text-gray-700';
  };

  return (
    <div className="space-y-3 max-h-96 overflow-y-auto">
      {segments.map((segment, index) => (
        <div
          key={index}
          className={`p-3 border-l-4 rounded-r ${getSentimentColor(
            segment.sentiment
          )}`}
        >
          <div className="flex items-center justify-between mb-1">
            <span className={`text-sm font-medium ${getSpeakerColor(segment.speaker)}`}>
              {segment.speaker || 'Speaker'}
            </span>
            <span className="text-xs text-gray-500">
              {segment.start_time?.toFixed(1)}s - {segment.end_time?.toFixed(1)}s
            </span>
          </div>
          <p className="text-sm leading-relaxed">{segment.text}</p>
          {segment.sentiment_score && (
            <div className="mt-2 text-xs text-gray-600">
              Sentiment: {segment.sentiment} ({(segment.sentiment_score * 100).toFixed(0)}%)
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default TranscriptViewer;
