/**
 * Report Input Page - Data Ingestion
 * Handles audio, text, and image inputs for analysis
 */
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { FadeIn } from '../components/FadeIn'
import { GradientText } from '../components/GradientText'
import { GlareHover } from '../components/GlareHover'
import { TiltCard } from '../components/TiltCard'
import clsx from 'clsx'

export function ReportInputPage() {
  const [inputType, setInputType] = useState('audio')
  const [file, setFile] = useState(null)
  const [textInput, setTextInput] = useState('')
  const [title, setTitle] = useState('')
  const navigate = useNavigate()

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const handleStartAnalysis = async () => {
    if (!title.trim()) {
      alert('Please enter a Report Title.')
      return
    }

    if (inputType === 'audio' && !file) {
      alert('Please select an audio file.')
      return
    }
    if (inputType === 'image' && !file) {
      alert('Please select an image file.')
      return
    }
    if (inputType === 'text' && !textInput.trim()) {
      alert('Please enter transcript text.')
      return
    }

    // Navigate to the analysis route with state
    navigate(`/analysis/new-run`, {
      state: {
        inputType,
        title,
        file: file ? file.name : null,
        text: textInput,
      },
    })
  }

  const isFormValid = title.trim() && (
    (inputType === 'audio' && file) ||
    (inputType === 'image' && file) ||
    (inputType === 'text' && textInput.trim())
  )

  return (
    <div className="min-h-screen bg-gray-950 p-8">
      <FadeIn>
        <div className="mb-8">
          <h1 className="mb-2 text-4xl font-bold text-white">
            <GradientText>Data Ingestion</GradientText>
          </h1>
          <p className="text-gray-400">
            Select an input type to begin the Whisper/Claude analysis pipeline.
          </p>
        </div>
      </FadeIn>

      <div className="mx-auto max-w-3xl space-y-6">
        {/* Report Title */}
        <FadeIn delay={0.1}>
          <GlareHover>
            <TiltCard>
              <div className="rounded-2xl border border-gray-800 bg-gray-900 p-6">
                <label htmlFor="report-title" className="mb-2 block text-sm font-medium text-gray-300">
                  Report Title
                </label>
                <input
                  id="report-title"
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g., Q4 2025 Earnings Call - Apple Inc."
                  className="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 text-white placeholder-gray-500 focus:border-blue-500 focus:ring-blue-500/20"
                />
              </div>
            </TiltCard>
          </GlareHover>
        </FadeIn>

        {/* Input Type Selector (Dock Inspired) */}
        <FadeIn delay={0.2}>
          <div className="flex justify-center rounded-2xl border border-gray-800 bg-gray-900 p-2 shadow-inner">
            {[
              { type: 'audio', label: '🎧 Audio File' },
              { type: 'text', label: '📄 Raw Transcript' },
              { type: 'image', label: '🖼️ Image/PDF' },
            ].map((item) => (
              <button
                key={item.type}
                onClick={() => setInputType(item.type)}
                className={clsx(
                  'flex-1 rounded-xl px-6 py-3 font-semibold transition-all',
                  inputType === item.type
                    ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/30'
                    : 'text-gray-400 hover:bg-gray-800'
                )}
              >
                {item.label}
              </button>
            ))}
          </div>
        </FadeIn>

        {/* Dynamic Input Area */}
        <FadeIn delay={0.3}>
          <GlareHover>
            <TiltCard>
              <div className="rounded-2xl border-2 border-blue-500/20 bg-gray-900 p-8">
                {inputType === 'audio' && (
                  <div>
                    <label htmlFor="audio-upload" className="mb-2 block text-lg font-bold text-white">
                      Upload Earnings Call Audio (.mp3, .m4a, .wav)
                    </label>
                    <input
                      id="audio-upload"
                      type="file"
                      accept="audio/*"
                      onChange={handleFileChange}
                      className="mt-1 w-full text-sm text-gray-400 file:mr-4 file:rounded-full file:border-0 file:bg-blue-500/20 file:px-4 file:py-2 file:text-blue-400 hover:file:bg-blue-500/30"
                    />
                    {file && <p className="mt-3 text-sm text-green-400">Selected: {file.name}</p>}
                  </div>
                )}
                {inputType === 'text' && (
                  <div>
                    <label htmlFor="text-upload" className="mb-2 block text-lg font-bold text-white">
                      Paste Full Transcript
                    </label>
                    <textarea
                      id="text-upload"
                      rows={10}
                      value={textInput}
                      onChange={(e) => setTextInput(e.target.value)}
                      placeholder="Paste the quarterly earnings call transcript here..."
                      className="w-full rounded-xl border border-gray-700 bg-gray-950 px-4 py-3 font-mono text-sm text-white placeholder-gray-500 focus:border-blue-500 focus:ring-blue-500/20"
                    />
                  </div>
                )}
                {inputType === 'image' && (
                  <div>
                    <label htmlFor="image-upload" className="mb-2 block text-lg font-bold text-white">
                      Upload Screenshot/PDF of Report Text
                    </label>
                    <input
                      id="image-upload"
                      type="file"
                      accept="image/*,application/pdf"
                      onChange={handleFileChange}
                      className="mt-1 w-full text-sm text-gray-400 file:mr-4 file:rounded-full file:border-0 file:bg-yellow-500/20 file:px-4 file:py-2 file:text-yellow-400 hover:file:bg-yellow-500/30"
                    />
                    {file && <p className="mt-3 text-sm text-green-400">Selected: {file.name}</p>}
                    <p className="mt-4 text-xs text-gray-500">
                      (Note: This will use vision models for OCR/Analysis - higher latency/cost)
                    </p>
                  </div>
                )}
              </div>
            </TiltCard>
          </GlareHover>
        </FadeIn>

        {/* Start Button */}
        <FadeIn delay={0.4}>
          <GlareHover>
            <button
              onClick={handleStartAnalysis}
              disabled={!isFormValid}
              className={clsx(
                'w-full rounded-xl bg-gradient-to-r from-blue-500 to-pink-500 px-6 py-4 text-lg font-bold text-white transition-all hover:scale-[1.02] shadow-2xl',
                !isFormValid && 'opacity-50 cursor-not-allowed'
              )}
            >
              Start AI Pipeline
            </button>
          </GlareHover>
        </FadeIn>
      </div>
    </div>
  )
}
