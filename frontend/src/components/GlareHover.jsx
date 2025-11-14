/**
 * Glare Hover Effect Component
 */
import { motion } from 'framer-motion'

export function GlareHover({ children, className = '' }) {
  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      transition={{ type: 'spring', stiffness: 300 }}
      className={className}
    >
      {children}
    </motion.div>
  )
}
