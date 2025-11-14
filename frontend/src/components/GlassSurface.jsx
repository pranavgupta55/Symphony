/**
 * Glass Morphism Surface Component
 */
export function GlassSurface({ children, className = '' }) {
  return (
    <div
      className={`rounded-2xl border border-gray-800/50 bg-gray-900/50 backdrop-blur-sm shadow-xl ${className}`}
    >
      {children}
    </div>
  )
}
