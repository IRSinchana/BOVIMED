import { useMemo, useState } from 'react'
import AnalysisImage from './AnalysisImage'
import { formatConfidence } from '../utils/analysis'

const BOX_COLORS = ['#2d6a4f', '#40916c', '#1b4332', '#d4a373', '#bc4749', '#6a994e', '#386641']

export default function DetectionImageOverlay({
  src,
  detections = [],
  alt = '',
  fallbackLabel,
  className = 'max-h-80 w-full object-contain bg-stone-100',
  maxHeightClass = 'max-h-80',
}) {
  const [dims, setDims] = useState({ w: 0, h: 0 })

  const boxes = useMemo(
    () =>
      (detections || []).filter(
        (d) => Array.isArray(d.bbox) && d.bbox.length === 4 && d.bbox.every((v) => v != null),
      ),
    [detections],
  )

  return (
    <AnalysisImage
      src={src}
      alt={alt}
      fallbackLabel={fallbackLabel}
      className={`${maxHeightClass} w-full object-contain bg-stone-100 ${className}`.trim()}
      onLoad={(e) => {
        setDims({
          w: e.currentTarget.naturalWidth || 1,
          h: e.currentTarget.naturalHeight || 1,
        })
      }}
    >
      {dims.w > 0 && boxes.length > 0 ? (
        <svg
          className="pointer-events-none absolute inset-0 h-full w-full"
          viewBox={`0 0 ${dims.w} ${dims.h}`}
          preserveAspectRatio="xMidYMid meet"
        >
          {boxes.map((det, i) => {
            const [x1, y1, x2, y2] = det.bbox.map(Number)
            const color = BOX_COLORS[i % BOX_COLORS.length]
            const label = `${det.class_name} ${formatConfidence(det.confidence)}`
            return (
              <g key={`${det.class_name}-${i}`}>
                <rect
                  x={x1}
                  y={y1}
                  width={Math.max(0, x2 - x1)}
                  height={Math.max(0, y2 - y1)}
                  fill="none"
                  stroke={color}
                  strokeWidth={Math.max(2, dims.w / 300)}
                />
                <text
                  x={x1}
                  y={Math.max(16, y1 - 4)}
                  fill={color}
                  fontSize={Math.max(12, dims.w / 45)}
                  fontWeight="700"
                >
                  {label}
                </text>
              </g>
            )
          })}
        </svg>
      ) : null}
    </AnalysisImage>
  )
}
