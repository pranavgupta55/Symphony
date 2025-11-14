/**
 * CountUp Animation Component
 */
import { useEffect, useState } from 'react'
import { motion, useSpring, useTransform } from 'framer-motion'

export function CountUpComponent({ end, decimals = 0, prefix = '', suffix = '' }) {
  const [displayValue, setDisplayValue] = useState(0)

  useEffect(() => {
    let startTime
    const duration = 2000 // 2 seconds

    const animate = (currentTime) => {
      if (!startTime) startTime = currentTime
      const elapsed = currentTime - startTime
      const progress = Math.min(elapsed / duration, 1)

      // Easing function (ease out)
      const easeOut = 1 - Math.pow(1 - progress, 3)
      const current = easeOut * end

      setDisplayValue(current)

      if (progress < 1) {
        requestAnimationFrame(animate)
      }
    }

    requestAnimationFrame(animate)
  }, [end])

  return (
    <span>
      {prefix}
      {displayValue.toFixed(decimals)}
      {suffix}
    </span>
  )
}
