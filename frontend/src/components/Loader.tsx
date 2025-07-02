import { motion } from 'framer-motion'
import clsx from 'clsx'

export const Loader: React.FC<{ className?: string }> = ({ className }) => {
  return (
    <div
      className={clsx(
        'w-16 h-16',
        'flex items-center justify-center',
        className
      )}
      role="status"
      aria-label="Loading"
    >
      <svg
        viewBox="0 0 100 100"
        className="w-full h-full"
        fill="none"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        {/* Filters */}
        <defs>
          <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="1.5" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>

          <filter id="aberration">
            <feTurbulence
              type="fractalNoise"
              baseFrequency="0.03"
              numOctaves="2"
              result="noise"
            />
            <feDisplacementMap
              in="SourceGraphic"
              in2="noise"
              scale="1.8"
              xChannelSelector="R"
              yChannelSelector="G"
            />
          </filter>
        </defs>

        {/* Outer ring */}
        <motion.circle
          cx="50"
          cy="50"
          r="42"
          className="text-cryocore dark:text-cryocore-dark"
          stroke="currentColor"
          strokeWidth="1.6"
          strokeDasharray="4 3"
          animate={{ rotate: 360 }}
          transition={{ repeat: Infinity, duration: 12, ease: 'linear' }}
          style={{ originX: '50%', originY: '50%' }}
          filter="url(#glow)"
        />

        {/* Core hex */}
        <motion.polygon
          points="50,15 80,35 80,65 50,85 20,65 20,35"
          className="text-shadowmint dark:text-shadowmint-dark"
          stroke="currentColor"
          strokeWidth="2.25"
          animate={{ rotate: 360 }}
          transition={{ repeat: Infinity, duration: 8, ease: 'linear' }}
          style={{ originX: '50%', originY: '50%' }}
          filter="url(#glow)"
        />

        {/* Inner ring hex */}
        <motion.polygon
          points="45,20 75,40 75,60 45,80 15,60 15,40"
          className="text-shadowmint dark:text-shadowmint-dark"
          stroke="currentColor"
          strokeWidth="1.75"
          animate={{ rotate: -360 }}
          transition={{ repeat: Infinity, duration: 10, ease: 'linear' }}
          style={{ originX: '50%', originY: '50%' }}
          filter="url(#glow)"
        />

        {/* Internal rotating lines */}
        {[
          [25, 50, 75, 50],
          [30, 30, 70, 70],
          [70, 30, 30, 70],
          [20, 20, 80, 80],
          [80, 20, 20, 80],
        ].map(([x1, y1, x2, y2], i) => (
          <motion.line
            key={i}
            x1={x1}
            y1={y1}
            x2={x2}
            y2={y2}
            className="text-cryocore dark:text-cryocore-dark"
            stroke="currentColor"
            strokeWidth="0.6"
            animate={{ rotate: i % 2 === 0 ? 360 : -360 }}
            transition={{
              repeat: Infinity,
              duration: 5 + i * 1.2,
              ease: 'linear',
            }}
            style={{ originX: '50%', originY: '50%' }}
          />
        ))}

        {/* Aberration flicker (overlay polygon) */}
        <motion.g
          filter="url(#aberration)"
          animate={{ opacity: [0.3, 0.1, 0.4, 0.15, 0.05] }}
          transition={{
            repeat: Infinity,
            duration: 3,
            ease: 'easeInOut',
          }}
        >
          <polygon
            points="50,15 80,35 80,65 50,85 20,65 20,35"
            className="text-cryocore dark:text-cryocore-dark"
            stroke="currentColor"
            strokeWidth="0.8"
          />
        </motion.g>
      </svg>
    </div>
  )
}
