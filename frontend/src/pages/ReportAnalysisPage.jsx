/**
 * Report Analysis Page
 * Handles both loading state (new report) and display of existing report
 */
import { useState, useEffect, useMemo } from 'react'
import { useParams, useLocation, useNavigate } from 'react-router-dom'
import { supabase } from '../lib/supabase'
import { FadeIn } from '../components/FadeIn'
import { GradientText } from '../components/GradientText'
import { GlassSurface } from '../components/GlassSurface'
import { CountUpComponent } from '../components/CountUpComponent'
import { ProcessingChecklist } from '../components/ProcessingChecklist'
import clsx from 'clsx'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const initialSteps = [
  { name: 'File Upload & Validation', status: 'pending' },
  { name: 'Whisper: Transcribing Audio', status: 'pending' },
  { name: 'Claude: Extracting Key Data', status: 'pending' },
  { name: 'Claude: Generating Sentiment Analysis', status: 'pending' },
  { name: 'Saving to Supabase', status: 'pending' },
  { name: 'Finalizing Report', status: 'pending' },
]

export function ReportAnalysisPage() {
  const { id } = useParams()
  const location = useLocation()
  const navigate = useNavigate()

  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [processingSteps, setProcessingSteps] = useState(initialSteps)

  const isNewRun = id === 'new-run'
  const isProcessing = isNewRun && processingSteps.some((s) => s.status === 'running' || s.status === 'pending')

  const currentStepName = useMemo(() => {
    const runningStep = processingSteps.find((s) => s.status === 'running')
    if (runningStep) return runningStep.name
    const pendingStep = processingSteps.find((s) => s.status === 'pending')
    if (pendingStep) return pendingStep.name
    return 'Done'
  }, [processingSteps])

  useEffect(() => {
    if (isNewRun && location.state) {
      runMockBackendPipeline(location.state)
    } else if (id && id !== 'new-run') {
      fetchReport(id)
    }
  }, [id, isNewRun, location.state])

  const runMockBackendPipeline = async (input) => {
    setLoading(true)

    // Mock analysis data
    const mockAnalysis = {
      keySummary:
        'The company significantly exceeded expectations across all key metrics in Q4, driven by market expansion and operational efficiency. Management projects continued positive momentum, though acknowledging rising labor costs.',
      overallSentiment: 'Positive',
      keyMetrics: { revenue: 3500000000, netIncome: 750000000, eps: 4.25 },
      investorTakeaways: [
        'Record revenue growth of 25% year-over-year.',
        'Net income margin increased to 21%, indicating improved efficiency.',
        'New product line launch is expected to maintain growth trajectory.',
        'Strong cash position for potential acquisitions.',
      ],
      riskFactors: [
        'Rising labor costs mentioned as a potential headwind for next year.',
        'Competitive landscape intensifying in the key European market.',
      ],
      transcriptSnippets: [
        { text: 'We started the quarter slow...', sentiment: 'Negative' },
        { text: 'However, the new product line was a stellar performer...', sentiment: 'Positive' },
        { text: 'Revenue hit $3.5 billion, an all-time high.', sentiment: 'Positive' },
        { text: 'Net income reached a record $750 million.', sentiment: 'Positive' },
        { text: 'We acknowledge pressure from rising labor costs.', sentiment: 'Negative' },
      ],
      sentimentOverTime: [
        { time: 0, sentimentScore: 0.1 },
        { time: 1, sentimentScore: -0.3 },
        { time: 2, sentimentScore: 0.5 },
        { time: 3, sentimentScore: 0.9 },
        { time: 4, sentimentScore: 0.7 },
        { time: 5, sentimentScore: -0.2 },
      ],
      highlights: {
        positive: ['Revenue hit $3.5 billion, an all-time high.'],
        negative: ['We acknowledge pressure from rising labor costs.'],
      },
    }

    // Simulate step-by-step processing
    const steps = [...initialSteps]

    for (let i = 0; i < steps.length; i++) {
      await new Promise((resolve) => setTimeout(resolve, 1000 + Math.random() * 1000))
      setProcessingSteps((prev) =>
        prev.map((step, index) => {
          if (index < i) return { ...step, status: 'completed' }
          if (index === i) return { ...step, status: 'running' }
          return step
        })
      )
    }

    // Final step completed
    setProcessingSteps((prev) => prev.map((step) => ({ ...step, status: 'completed' })))

    // Mock saving to Supabase
    const { data: userData } = await supabase.auth.getUser()
    let reportId = 'mock-id-' + Date.now()

    // Try to save to Supabase (may fail if not authenticated - that's OK for demo)
    try {
      if (userData?.user) {
        const { data, error } = await supabase
          .from('report_analyses')
          .insert({
            user_id: userData.user.id,
            title: input.title,
            input_type: input.inputType,
            transcript: mockAnalysis.transcriptSnippets.map((s) => s.text).join(' '),
            analysis_data: mockAnalysis,
          })
          .select()
          .single()

        if (!error && data) {
          reportId = data.id
        }
      }
    } catch (err) {
      console.error('Supabase save error:', err)
    }

    await new Promise((resolve) => setTimeout(resolve, 500))

    setReport({
      id: reportId,
      analysis_data: mockAnalysis,
      created_at: new Date().toISOString(),
      title: input.title,
      input_type: input.inputType,
      user_id: '',
      transcript: mockAnalysis.transcriptSnippets.map((s) => s.text).join(' '),
    })
    setLoading(false)

    // Navigate to the permanent URL
    navigate(`/analysis/${reportId}`, { replace: true })
  }

  const fetchReport = async (reportId) => {
    setLoading(true)
    const { data, error } = await supabase
      .from('report_analyses')
      .select('*')
      .eq('id', reportId)
      .single()

    if (error || !data) {
      setError('Report not found or failed to load.')
    } else {
      setReport(data)
    }
    setLoading(false)
  }

  // --- Render Logic ---

  if (loading || isProcessing) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-950 p-8">
        <FadeIn>
          <div className="w-full max-w-2xl">
            <ProcessingChecklist steps={processingSteps} currentStepName={currentStepName} />
          </div>
        </FadeIn>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-950 p-8">
        <GlassSurface className="p-12 text-center text-red-400">
          <h1 className="mb-4 text-3xl font-bold">❌ Error</h1>
          <p>{error}</p>
          <button onClick={() => navigate('/hub')} className="mt-6 text-blue-500 hover:underline">
            Go to Hub
          </button>
        </GlassSurface>
      </div>
    )
  }

  const analysis = report?.analysis_data

  if (!analysis) {
    return null
  }

  return (
    <div className="min-h-screen bg-gray-950 p-8">
      {/* Header */}
      <FadeIn>
        <div className="mb-8">
          <h1 className="mb-2 text-4xl font-bold text-white">
            <GradientText>{report?.title || 'Report Analysis'}</GradientText>
          </h1>
          <p className="text-gray-400">
            {report?.created_at && `Run on: ${new Date(report.created_at).toLocaleDateString()}`}
          </p>
        </div>
      </FadeIn>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Window 1: Transcript Sentiment Breakdown (Sidebar Left) */}
        <FadeIn delay={0.1} className="lg:col-span-1">
          <GlassSurface className="p-6 max-h-[80vh] overflow-y-auto">
            <h2 className="mb-4 text-2xl font-bold text-white">Transcript Breakdown</h2>
            <div className="space-y-4">
              {analysis.transcriptSnippets.map((snippet, i) => (
                <div
                  key={i}
                  className={clsx(
                    'rounded-lg p-3 text-sm border-l-4',
                    snippet.sentiment === 'Positive' && 'border-green-500 bg-green-900/10 text-green-200',
                    snippet.sentiment === 'Negative' && 'border-red-500 bg-red-900/10 text-red-200',
                    snippet.sentiment === 'Neutral' && 'border-gray-500 bg-gray-800/50 text-gray-400'
                  )}
                >
                  <span className="font-mono text-xs text-gray-500 mr-2">[{i + 1}]</span>
                  {snippet.text}
                </div>
              ))}
            </div>
          </GlassSurface>
        </FadeIn>

        {/* Window 2: Overall Analysis and Key Metrics (Center) */}
        <div className="lg:col-span-2 space-y-6">
          <FadeIn delay={0.2}>
            <GlassSurface className="p-8">
              <h2 className="mb-4 text-3xl font-bold text-white">Overall Analysis</h2>

              <div className="mb-6 rounded-xl border border-gray-800/80 bg-gray-900/50 p-5 text-center">
                <h3 className="mb-2 text-xl font-semibold text-gray-400">Overall Sentiment:</h3>
                <p
                  className={clsx(
                    'text-6xl font-extrabold',
                    analysis.overallSentiment === 'Positive' && 'text-green-400',
                    analysis.overallSentiment === 'Negative' && 'text-red-400',
                    analysis.overallSentiment === 'Neutral' && 'text-yellow-400'
                  )}
                >
                  {analysis.overallSentiment.toUpperCase()}
                </p>
              </div>

              {/* Key Metrics - Count Up */}
              <div className="mb-8 grid grid-cols-3 gap-4">
                <div className="rounded-xl bg-gray-950 p-4 text-center">
                  <div className="text-sm text-gray-500">Revenue</div>
                  <div className="text-3xl font-bold text-blue-400">
                    <CountUpComponent
                      end={analysis.keyMetrics.revenue / 1000000000}
                      decimals={2}
                      suffix="B"
                      prefix="$"
                    />
                  </div>
                </div>
                <div className="rounded-xl bg-gray-950 p-4 text-center">
                  <div className="text-sm text-gray-500">Net Income</div>
                  <div className="text-3xl font-bold text-green-400">
                    <CountUpComponent
                      end={analysis.keyMetrics.netIncome / 1000000}
                      decimals={0}
                      suffix="M"
                      prefix="$"
                    />
                  </div>
                </div>
                <div className="rounded-xl bg-gray-950 p-4 text-center">
                  <div className="text-sm text-gray-500">EPS</div>
                  <div className="text-3xl font-bold text-blue-400">
                    <CountUpComponent end={analysis.keyMetrics.eps} decimals={2} prefix="$" />
                  </div>
                </div>
              </div>

              {/* Key Summary */}
              <div className="mb-6 rounded-xl bg-gray-900/50 p-5">
                <h3 className="mb-3 text-xl font-bold text-white">Executive Summary</h3>
                <p className="text-gray-300 leading-relaxed">{analysis.keySummary}</p>
              </div>

              {/* Investor Takeaways / Risk Factors */}
              <h3 className="mb-3 text-2xl font-bold text-white">Investor Takeaways</h3>
              <ul className="mb-6 list-disc space-y-1 pl-5 text-gray-400">
                {analysis.investorTakeaways.map((takeaway, i) => (
                  <li key={i}>{takeaway}</li>
                ))}
              </ul>

              <h3 className="mb-3 text-2xl font-bold text-red-400">⚠️ Risk Factors</h3>
              <ul className="list-disc space-y-1 pl-5 text-red-300/80">
                {analysis.riskFactors.map((risk, i) => (
                  <li key={i}>{risk}</li>
                ))}
              </ul>
            </GlassSurface>
          </FadeIn>
        </div>

        {/* Window 3: Sentiment Over Time Chart (Bottom) */}
        <FadeIn delay={0.3} className="lg:col-span-3">
          <GlassSurface className="p-6">
            <h2 className="mb-4 text-2xl font-bold text-white">Sentiment Flow Over Time</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={analysis.sentimentOverTime} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="time" stroke="#9CA3AF" tickFormatter={(value) => `${value} min`} />
                <YAxis stroke="#9CA3AF" domain={[-1, 1]} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #4B5563' }}
                  labelStyle={{ color: '#9CA3AF' }}
                />
                <Line type="monotone" dataKey="sentimentScore" stroke="#8884d8" strokeWidth={3} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </GlassSurface>
        </FadeIn>
      </div>

      {/* Back to Hub Button */}
      <FadeIn delay={0.4} className="mt-8 text-center">
        <button
          onClick={() => navigate('/hub')}
          className="rounded-xl bg-gray-800 px-6 py-3 text-white hover:bg-gray-700 transition-all"
        >
          ← Back to Hub
        </button>
      </FadeIn>
    </div>
  )
}
