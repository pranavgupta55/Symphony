/**
 * Report Hub - Central Dashboard
 * Shows history of reports and option to start new analysis
 */
import { Link, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { FadeIn } from '../components/FadeIn'
import { GradientText } from '../components/GradientText'
import { TiltCard } from '../components/TiltCard'
import { GlassSurface } from '../components/GlassSurface'
import clsx from 'clsx'

export function ReportHub() {
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    fetchReports()
  }, [])

  const fetchReports = async () => {
    setLoading(true)
    const { data: userData } = await supabase.auth.getUser()

    // For development - skip auth check and show demo/mock data
    // In production, uncomment the auth check below
    /*
    if (!userData?.user) {
      navigate('/login')
      return
    }
    */

    const { data, error } = await supabase
      .from('report_analyses')
      .select('*')
      .order('created_at', { ascending: false })

    if (error) {
      console.error('Error fetching reports:', error)
      setReports([])
    } else {
      setReports(data || [])
    }

    setLoading(false)
  }

  const handleNewRunClick = () => {
    navigate('/new-report')
  }

  return (
    <div className="min-h-screen bg-gray-950 p-8">
      <FadeIn>
        <div className="mb-8">
          <h1 className="mb-2 text-6xl font-extrabold text-white">
            <GradientText>Investment AI Hub</GradientText>
          </h1>
          <p className="text-xl text-gray-400">
            Start a new analysis or review your historical reports.
          </p>
        </div>
      </FadeIn>

      <div className="grid gap-8 lg:grid-cols-3">
        {/* Left Pane: New Run */}
        <div className="lg:col-span-1">
          <FadeIn delay={0.2}>
            <GlassSurface className="p-8">
              <h2 className="mb-4 text-3xl font-bold text-blue-400">
                Start New Analysis
              </h2>
              <p className="mb-6 text-gray-300">
                Upload your earnings call audio, image, or raw transcript.
              </p>
              <button
                onClick={handleNewRunClick}
                className="w-full rounded-xl bg-gradient-to-r from-blue-500 to-purple-500 px-6 py-4 text-lg font-bold text-white transition-all hover:scale-[1.02]"
              >
                🚀 New Report Run
              </button>
            </GlassSurface>
          </FadeIn>
        </div>

        {/* Right Pane: Past Runs (Scrollable Window) */}
        <div className="lg:col-span-2">
          <FadeIn delay={0.4}>
            <GlassSurface className="p-8">
              <h2 className="mb-4 text-3xl font-bold text-pink-400">
                Historical Reports ({reports.length})
              </h2>
              <div className="space-y-4 max-h-[70vh] overflow-y-auto pr-2">
                {loading ? (
                  <p className="text-center text-gray-500">Loading history...</p>
                ) : reports.length === 0 ? (
                  <p className="text-center text-gray-500">No reports found. Start a new analysis!</p>
                ) : (
                  reports.map((report) => (
                    <TiltCard key={report.id}>
                      <Link
                        to={`/analysis/${report.id}`}
                        className="block rounded-xl border border-gray-800 bg-gray-900 p-4 transition-all hover:border-blue-500/50 hover:bg-gray-800/80"
                      >
                        <h3 className="text-xl font-semibold text-white">{report.title}</h3>
                        <div className="mt-1 flex justify-between text-sm text-gray-400">
                          <span>
                            Input:
                            <span
                              className={clsx(
                                'ml-2 rounded-full px-2 py-0.5 text-xs font-medium',
                                report.input_type === 'audio' && 'bg-blue-500/20 text-blue-400',
                                report.input_type === 'text' && 'bg-green-500/20 text-green-400',
                                report.input_type === 'image' && 'bg-yellow-500/20 text-yellow-400'
                              )}
                            >
                              {report.input_type.toUpperCase()}
                            </span>
                          </span>
                          <span>
                            Date: {new Date(report.created_at).toLocaleDateString()}
                          </span>
                        </div>
                      </Link>
                    </TiltCard>
                  ))
                )}
              </div>
            </GlassSurface>
          </FadeIn>
        </div>
      </div>
    </div>
  )
}
