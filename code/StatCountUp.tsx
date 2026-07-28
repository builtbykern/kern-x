/**
 * Stat CountUp
 * Clean metric counter for SaaS & portfolio stats.
 *
 * @framerSupportedLayoutWidth any
 * @framerSupportedLayoutHeight any
 * @framerIntrinsicWidth 200
 * @framerIntrinsicHeight 64
 */

import { addPropertyControls, ControlType } from "framer"
import { useEffect, useRef, useState, type CSSProperties } from "react"

export interface StatCountUpProps {
  from?: number
  to?: number
  duration?: number
  prefix?: string
  suffix?: string
  decimals?: number
  useCommas?: boolean
  fontFamily?: string
  fontSize?: number
  fontWeight?: number
  color?: string
  textAlign?: "left" | "center" | "right"
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

function formatValue(
  value: number,
  decimals: number,
  useCommas: boolean
): string {
  const fixed = value.toFixed(decimals)
  if (!useCommas) return fixed
  const [intPart, decPart] = fixed.split(".")
  const withCommas = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, ",")
  return decimals > 0 ? `${withCommas}.${decPart}` : withCommas
}

function easeOutCubic(t: number): number {
  return 1 - Math.pow(1 - t, 3)
}

/**
 * Stat CountUp — animates from → to once when entering the viewport.
 */
export default function StatCountUp(props: StatCountUpProps) {
  const {
    from = 0,
    to = 12000,
    duration = 1.6,
    prefix = "",
    suffix = "+",
    decimals = 0,
    useCommas = true,
    fontFamily = '"Instrument Sans", "Segoe UI", system-ui, sans-serif',
    fontSize = 48,
    fontWeight = 600,
    color = "#111111",
    textAlign = "left",
    style,
  } = props

  const ref = useRef<HTMLDivElement>(null)
  const prefersReduced = usePrefersReducedMotion()
  const [value, setValue] = useState(prefersReduced ? to : from)
  const [started, setStarted] = useState(false)

  useEffect(() => {
    if (prefersReduced) {
      setValue(to)
      return
    }

    const el = ref.current
    if (!el || typeof IntersectionObserver === "undefined") {
      setValue(to)
      return
    }

    const io = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && entry.intersectionRatio >= 0.4) {
          setStarted(true)
          io.disconnect()
        }
      },
      { threshold: [0, 0.4, 1] }
    )
    io.observe(el)
    return () => io.disconnect()
  }, [prefersReduced, to])

  useEffect(() => {
    if (!started || prefersReduced) return

    let raf = 0
    const start = performance.now()
    const fromVal = from
    const toVal = to
    const durMs = Math.max(0.1, duration) * 1000

    const tick = (now: number) => {
      const t = Math.min(1, (now - start) / durMs)
      const eased = easeOutCubic(t)
      const current = fromVal + (toVal - fromVal) * eased
      setValue(t >= 1 ? toVal : current)
      if (t < 1) raf = requestAnimationFrame(tick)
    }

    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [started, prefersReduced, from, to, duration])

  const display = `${prefix}${formatValue(value, decimals, useCommas)}${suffix}`

  return (
    <div
      ref={ref}
      style={{
        fontFamily,
        fontSize,
        fontWeight,
        color,
        textAlign,
        lineHeight: 1.1,
        letterSpacing: "-0.03em",
        whiteSpace: "nowrap",
        ...style,
      }}
      aria-label={display}
    >
      {display}
    </div>
  )
}

StatCountUp.displayName = "StatCountUp"

StatCountUp.defaultProps = {
  from: 0,
  to: 12000,
  duration: 1.6,
  prefix: "",
  suffix: "+",
  decimals: 0,
  useCommas: true,
  fontFamily: '"Instrument Sans", "Segoe UI", system-ui, sans-serif',
  fontSize: 48,
  fontWeight: 600,
  color: "#111111",
  textAlign: "left" as const,
}

addPropertyControls(StatCountUp, {
  from: {
    type: ControlType.Number,
    title: "From",
    defaultValue: 0,
  },
  to: {
    type: ControlType.Number,
    title: "To",
    defaultValue: 12000,
  },
  duration: {
    type: ControlType.Number,
    title: "Duration",
    min: 0.2,
    max: 6,
    step: 0.1,
    unit: "s",
    defaultValue: 1.6,
  },
  prefix: {
    type: ControlType.String,
    title: "Prefix",
    defaultValue: "",
  },
  suffix: {
    type: ControlType.String,
    title: "Suffix",
    defaultValue: "+",
  },
  decimals: {
    type: ControlType.Number,
    title: "Decimals",
    min: 0,
    max: 4,
    step: 1,
    defaultValue: 0,
  },
  useCommas: {
    type: ControlType.Boolean,
    title: "Commas",
    defaultValue: true,
    enabledTitle: "On",
    disabledTitle: "Off",
  },
  fontFamily: {
    type: ControlType.String,
    title: "Font",
    defaultValue: '"Instrument Sans", "Segoe UI", system-ui, sans-serif',
  },
  fontSize: {
    type: ControlType.Number,
    title: "Size",
    min: 12,
    max: 120,
    defaultValue: 48,
  },
  fontWeight: {
    type: ControlType.Number,
    title: "Weight",
    min: 300,
    max: 900,
    step: 100,
    defaultValue: 600,
  },
  color: {
    type: ControlType.Color,
    title: "Color",
    defaultValue: "#111111",
  },
  textAlign: {
    type: ControlType.Enum,
    title: "Align",
    options: ["left", "center", "right"],
    optionTitles: ["Left", "Center", "Right"],
    defaultValue: "left",
    displaySegmentedControl: true,
  },
})
