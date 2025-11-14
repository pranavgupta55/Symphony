/**
 * Confidence Timeline Chart using Recharts
 */
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart,
} from 'recharts';

const ConfidenceTimeline = ({ timeline }) => {
  if (!timeline || timeline.length === 0) {
    return <p className="text-gray-500">No confidence data available</p>;
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.7) return '#10b981'; // green
    if (confidence >= 0.4) return '#f59e0b'; // yellow
    return '#ef4444'; // red
  };

  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={timeline}>
          <defs>
            <linearGradient id="confidenceGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.1} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="time"
            label={{ value: 'Time (seconds)', position: 'insideBottom', offset: -5 }}
            stroke="#6b7280"
          />
          <YAxis
            domain={[0, 1]}
            label={{ value: 'Confidence', angle: -90, position: 'insideLeft' }}
            stroke="#6b7280"
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#ffffff',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
            }}
            formatter={(value) => [`${(value * 100).toFixed(0)}%`, 'Confidence']}
          />
          <Legend />
          <Area
            type="monotone"
            dataKey="confidence"
            stroke="#3b82f6"
            fill="url(#confidenceGradient)"
            strokeWidth={2}
            name="Vocal Confidence"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ConfidenceTimeline;
