/**
 * Processing Checklist Component
 * Visualizes the backend processing flow
 */
import { motion } from 'framer-motion'
import { FadeIn } from './FadeIn'
import { GlassSurface } from './GlassSurface'
import clsx from 'clsx'

export function ProcessingChecklist({
  steps,
  currentStepName,
  sentimentText = 'Analyzing Financials',
}) {
  const currentStepIndex = steps.findIndex((s) => s.name === currentStepName)

  return (
    <GlassSurface className="p-8">
      <h2 className="mb-6 text-3xl font-bold text-white">
        <motion.span
          key={currentStepName}
          initial={{ scale: 0.9, opacity: 0.5 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="inline-block text-blue-400"
        >
          Processing Pipeline
        </motion.span>
      </h2>
      <div className="space-y-4">
        {steps.map((step, index) => {
          const isActive = step.name === currentStepName
          const isComplete = step.status === 'completed'
          const isRunning = step.status === 'running'

          return (
            <FadeIn key={step.name} delay={index * 0.1}>
              <motion.div
                layout
                className={clsx(
                  'flex items-center gap-4 rounded-xl p-4 transition-all duration-300',
                  isComplete && 'bg-green-900/30',
                  isRunning && 'bg-blue-900/30 border border-blue-500/50',
                  !isComplete && !isRunning && 'bg-gray-900'
                )}
              >
                <span
                  className={clsx(
                    'text-2xl',
                    isComplete && 'text-green-400',
                    isRunning && 'text-blue-400 animate-spin-slow',
                    step.status === 'failed' && 'text-red-400'
                  )}
                >
                  {isComplete ? '✅' : isRunning ? '⚙️' : '⏳'}
                </span>
                <div className="flex-1">
                  <h3
                    className={clsx(
                      'text-lg font-bold',
                      isComplete ? 'text-green-300' : 'text-white',
                      isActive && 'text-2xl text-blue-300 font-extrabold italic'
                    )}
                  >
                    {step.name}
                  </h3>
                  <p className="text-sm text-gray-500">
                    {isActive
                      ? sentimentText
                      : isComplete
                        ? 'Completed Successfully'
                        : 'Waiting'}
                  </p>
                </div>
              </motion.div>
            </FadeIn>
          )
        })}
      </div>
    </GlassSurface>
  )
}
