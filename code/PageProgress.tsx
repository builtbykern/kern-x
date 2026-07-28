/**
 * Page Progress
 * Fixed reading progress for long pages.
 *
 * @framerSupportedLayoutWidth any
 * @framerSupportedLayoutHeight any
 * @framerIntrinsicWidth 400
 * @framerIntrinsicHeight 4
 */

import { addPropertyControls, ControlType } from "framer"
import { useEffect, useState, type CSSProperties } from "react"

export interface PageProgressProps {
  position?: "Top" | "Bottom"
  height?: number
  color?: string
  trackColor?: string
  zIndex?: number
  style?: CSSProperties
}

function usePrefersReducedMotion(): boolean {
  const [reduced, setReduced] = useState(false)
  useEffect(() => {
    if (typeof window === "undefined" || !window.matchMedia) return
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)")
    const update = () => setReduced(mq.matches)
    update()
    mq.addEventListener("change", update)
    return () => mq.removeEventListener("change", update)
  }, [])
  return reduced
}

function getScrollProgress(): number {
  if (typeof window === "undefined" || typeof document === "undefined") return 0
  const doc = document.documentElement
  const scrollTop = window.scrollY || doc.scrollTop
  const max = doc.scrollHeight - window.innerHeight
  if (max <= 0) return 0
  return Math.min(1, Math.max(0, scrollTop / max))
}

/**
 * Page Progress — fixed top/bottom bar tied to document scroll.
 */
export default function PageProgress(props: PageProgressProps) {
  const {
    position = "Top",
    height = 3,
    color = "#0f6b5c",
    trackColor = "rgba(0,0,0,0.08)",
    zIndex = 9999,
    style,
  } = props

  const prefersReduced = usePrefersReducedMotion()
  const [progress, setProgress] = useState(0.35)
  const [isCanvas, setIsCanvas] = useState(true)

  useEffect(() => {
    // Detect published / preview vs static canvas-ish first paint
    setIsCanvas(false)
    const update = () => setProgress(getScrollProgress())
    update()
    window.addEventListener("scroll", update, { passive: true })
    window.addEventListener("resize", update)
    return () => {
      window.removeEventListener("scroll", update)
      window.removeEventListener("resize", update)
    }
  }, [])

  const widthPct = `${(isCanvas ? 0.35 : progress) * 100}%`

  return (
    <div
      style={{
        position: "fixed",
        left: 0,
        right: 0,
        top: position === "Top" ? 0 : undefined,
        bottom: position === "Bottom" ? 0 : undefined,
        height,
        background: trackColor,
        zIndex,
        pointerEvents: "none",
        ...style,
      }}
      role="progressbar"
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={Math.round((isCanvas ? 0.35 : progress) * 100)}
      aria-label="Reading progress"
    >
      <div
        style={{
          height: "100%",
          width: widthPct,
          background: color,
          transition: prefersReduced ? undefined : "width 80ms linear",
        }}
      />
    </div>
  )
}

PageProgress.displayName = "PageProgress"

PageProgress.defaultProps = {
  position: "Top" as const,
  height: 3,
  color: "#0f6b5c",
  trackColor: "rgba(0,0,0,0.08)",
  zIndex: 9999,
}

addPropertyControls(PageProgress, {
  position: {
    type: ControlType.Enum,
    title: "Position",
    options: ["Top", "Bottom"],
    optionTitles: ["Top", "Bottom"],
    defaultValue: "Top",
    displaySegmentedControl: true,
  },
  height: {
    type: ControlType.Number,
    title: "Height",
    min: 1,
    max: 12,
    defaultValue: 3,
  },
  color: {
    type: ControlType.Color,
    title: "Fill",
    defaultValue: "#0f6b5c",
  },
  trackColor: {
    type: ControlType.Color,
    title: "Track",
    defaultValue: "rgba(0,0,0,0.08)",
  },
  zIndex: {
    type: ControlType.Number,
    title: "Z Index",
    min: 1,
    max: 99999,
    defaultValue: 9999,
  },
})
