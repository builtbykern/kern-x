import { addPropertyControls, ControlType } from "framer"
import {
  motion,
  useInView,
  useScroll,
  useTransform,
  type MotionValue,
} from "framer-motion"
import {
  useEffect,
  useId,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
} from "react"

function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value))
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

export type PathPreset = "Arc" | "Wave" | "Line" | "Custom"
export type KineticMode = "Path" | "ColorReveal" | "Blur" | "Scramble"

export interface PathTypeKineticProps {
  text?: string
  mode?: KineticMode
  pathPreset?: PathPreset
  customPath?: string
  granularity?: "Letter" | "Word"
  fontSize?: number
  fontWeight?: number
  fontFamily?: string
  letterSpacing?: number
  color?: string
  colorStart?: string
  colorEnd?: string
  blurAmount?: number
  scrambleCharset?: string
  scrambleSpeed?: number
  pathDuration?: number
  autoPlay?: boolean
  style?: CSSProperties
}

const PATHS: Record<Exclude<PathPreset, "Custom">, string> = {
  Arc: "M 20 140 Q 300 20 580 140",
  Wave: "M 10 100 C 120 20, 200 180, 300 100 S 480 20, 590 100",
  Line: "M 20 100 L 580 100",
}

const SCRAMBLE_CHARS =
  "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

function splitUnits(text: string, granularity: "Letter" | "Word"): string[] {
  if (granularity === "Word") {
    return text.split(/(\s+)/).filter((s) => s.length > 0)
  }
  return Array.from(text)
}

function PathText({
  text,
  pathD,
  color,
  fontSize,
  fontWeight,
  fontFamily,
  letterSpacing,
  progress,
  staticMode,
}: {
  text: string
  pathD: string
  color: string
  fontSize: number
  fontWeight: number
  fontFamily: string
  letterSpacing: number
  progress: MotionValue<number>
  staticMode: boolean
}) {
  const id = useId().replace(/:/g, "")
  const pathId = `pathtype-${id}`
  const startOffset = useTransform(progress, [0, 1], ["0%", "100%"])

  return (
    <svg
      viewBox="0 0 600 200"
      width="100%"
      height="100%"
      style={{ overflow: "visible", display: "block" }}
      aria-label={text}
    >
      <defs>
        <path id={pathId} d={pathD} fill="none" />
      </defs>
      <text
        fill={color}
        style={{
          fontSize,
          fontWeight,
          fontFamily,
          letterSpacing,
        }}
      >
        {staticMode ? (
          <textPath href={`#${pathId}`} startOffset="0%">
            {text}
          </textPath>
        ) : (
          <motion.textPath href={`#${pathId}`} startOffset={startOffset}>
            {text}
          </motion.textPath>
        )}
      </text>
    </svg>
  )
}

function UnitSpan({
  unit,
  index,
  total,
  mode,
  progress,
  color,
  colorStart,
  colorEnd,
  blurAmount,
  fontSize,
  fontWeight,
  fontFamily,
  letterSpacing,
  staticMode,
  scrambleCharset,
  scrambleSpeed,
  inView,
}: {
  unit: string
  index: number
  total: number
  mode: Exclude<KineticMode, "Path">
  progress: MotionValue<number>
  color: string
  colorStart: string
  colorEnd: string
  blurAmount: number
  fontSize: number
  fontWeight: number
  fontFamily: string
  letterSpacing: number
  staticMode: boolean
  scrambleCharset: string
  scrambleSpeed: number
  inView: boolean
}) {
  const start = index / Math.max(total, 1)
  const end = (index + 1) / Math.max(total, 1)

  const local = useTransform(progress, (v) => {
    if (end === start) return 1
    return clamp((v - start) / (end - start), 0, 1)
  })

  const colorMv = useTransform(local, [0, 1], [colorStart, colorEnd])
  const blurMv = useTransform(local, [0, 1], [blurAmount, 0])
  const filterMv = useTransform(blurMv, (b) => `blur(${b}px)`)
  const opacityMv = useTransform(local, [0, 1], [0.25, 1])

  const [scrambled, setScrambled] = useState(unit)
  const [localProgress, setLocalProgress] = useState(0)

  useEffect(() => {
    if (mode !== "Scramble") return
    return local.on("change", (v) => setLocalProgress(v))
  }, [local, mode])

  useEffect(() => {
    if (mode !== "Scramble" || staticMode || !inView || unit.trim() === "") {
      setScrambled(unit)
      return
    }

    let frame = 0
    let raf = 0
    const chars = scrambleCharset || SCRAMBLE_CHARS

    const tick = () => {
      frame += 1
      if (localProgress >= 1) {
        setScrambled(unit)
        return
      }
      if (frame % Math.max(1, Math.round(4 / scrambleSpeed)) === 0) {
        setScrambled(
          Array.from(unit)
            .map((ch) =>
              ch === " " ? " " : chars[Math.floor(Math.random() * chars.length)]
            )
            .join("")
        )
      }
      raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [
    mode,
    staticMode,
    inView,
    unit,
    scrambleCharset,
    scrambleSpeed,
    localProgress,
  ])

  if (unit === " " || unit === "\n") {
    return <span style={{ whiteSpace: "pre" }}>{unit}</span>
  }

  const base: CSSProperties = {
    fontSize,
    fontWeight,
    fontFamily,
    letterSpacing,
    display: "inline-block",
  }

  if (staticMode) {
    return (
      <span
        style={{
          ...base,
          color: mode === "ColorReveal" ? colorEnd : color,
        }}
      >
        {unit}
      </span>
    )
  }

  switch (mode) {
    case "ColorReveal":
      return (
        <motion.span style={{ ...base, color: colorMv }}>{unit}</motion.span>
      )
    case "Blur":
      return (
        <motion.span
          style={{ ...base, color, opacity: opacityMv, filter: filterMv }}
        >
          {unit}
        </motion.span>
      )
    case "Scramble":
      return (
        <motion.span
          style={{
            ...base,
            color,
            opacity: opacityMv,
            fontVariantNumeric: "tabular-nums",
          }}
        >
          {localProgress >= 1 ? unit : scrambled}
        </motion.span>
      )
    default: {
      const _exhaustive: never = mode
      return _exhaustive
    }
  }
}

/**
 * PathType Kinetic — path + scroll typography for hero headlines.
 * Modes: Path | ColorReveal | Blur | Scramble.
 */
export default function PathTypeKinetic(props: PathTypeKineticProps) {
  const {
    text = "Design that moves with you",
    mode = "Path",
    pathPreset = "Wave",
    customPath = "",
    granularity = "Letter",
    fontSize = 42,
    fontWeight = 600,
    fontFamily = '"Fraunces", "Georgia", serif',
    letterSpacing = 0,
    color = "#111111",
    colorStart = "rgba(17,17,17,0.25)",
    colorEnd = "#111111",
    blurAmount = 12,
    scrambleCharset = SCRAMBLE_CHARS,
    scrambleSpeed = 1,
    pathDuration = 8,
    autoPlay = true,
    style,
  } = props

  const rootRef = useRef<HTMLDivElement>(null)
  const prefersReduced = usePrefersReducedMotion()
  const inView = useInView(rootRef, { once: false, amount: 0.35 })
  const staticMode = prefersReduced

  const pathD =
    pathPreset === "Custom" && customPath.trim()
      ? customPath
      : PATHS[pathPreset === "Custom" ? "Wave" : pathPreset]

  const { scrollYProgress } = useScroll({
    target: rootRef,
    offset: ["start 80%", "end 20%"],
  })

  const [loop, setLoop] = useState(0)
  useEffect(() => {
    if (mode !== "Path" || !autoPlay || staticMode || !inView) return
    let raf = 0
    const start = performance.now()
    const tick = (now: number) => {
      const t = ((now - start) / (pathDuration * 1000)) % 1
      setLoop(t)
      raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [mode, autoPlay, staticMode, inView, pathDuration])

  const pathProgress = useTransform(scrollYProgress, [0, 1], [0, 1])
  const autoProgress = useTransform(() => loop)

  const activeProgress: MotionValue<number> =
    mode === "Path" && autoPlay ? autoProgress : pathProgress

  const units = useMemo(
    () => splitUnits(text, granularity),
    [text, granularity]
  )

  const contentUnits = units.filter((u) => u.trim() !== "").length || units.length

  return (
    <div
      ref={rootRef}
      style={{
        width: "100%",
        minHeight: mode === "Path" ? 220 : undefined,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        ...style,
      }}
      aria-label={text}
    >
      {mode === "Path" ? (
        <PathText
          text={text}
          pathD={pathD}
          color={color}
          fontSize={fontSize}
          fontWeight={fontWeight}
          fontFamily={fontFamily}
          letterSpacing={letterSpacing}
          progress={activeProgress}
          staticMode={staticMode}
        />
      ) : (
        <p
          style={{
            margin: 0,
            maxWidth: 900,
            textAlign: "center",
            lineHeight: 1.2,
          }}
        >
          {units.map((unit, index) => {
            const contentIndex = units
              .slice(0, index)
              .filter((u) => u.trim() !== "").length
            return (
              <UnitSpan
                key={`${index}-${unit}`}
                unit={unit}
                index={contentIndex}
                total={contentUnits}
                mode={mode}
                progress={pathProgress}
                color={color}
                colorStart={colorStart}
                colorEnd={colorEnd}
                blurAmount={blurAmount}
                fontSize={fontSize}
                fontWeight={fontWeight}
                fontFamily={fontFamily}
                letterSpacing={letterSpacing}
                staticMode={staticMode}
                scrambleCharset={scrambleCharset}
                scrambleSpeed={scrambleSpeed}
                inView={inView}
              />
            )
          })}
        </p>
      )}
    </div>
  )
}

PathTypeKinetic.displayName = "PathTypeKinetic"

PathTypeKinetic.defaultProps = {
  text: "Design that moves with you",
  mode: "Path" as KineticMode,
  pathPreset: "Wave" as PathPreset,
  customPath: "",
  granularity: "Letter" as const,
  fontSize: 42,
  fontWeight: 600,
  fontFamily: '"Fraunces", "Georgia", serif',
  letterSpacing: 0,
  color: "#111111",
  colorStart: "rgba(17,17,17,0.25)",
  colorEnd: "#111111",
  blurAmount: 12,
  scrambleCharset: SCRAMBLE_CHARS,
  scrambleSpeed: 1,
  pathDuration: 8,
  autoPlay: true,
}

addPropertyControls(PathTypeKinetic, {
  text: {
    type: ControlType.String,
    title: "Text",
    defaultValue: "Design that moves with you",
    displayTextArea: true,
  },
  mode: {
    type: ControlType.Enum,
    title: "Mode",
    options: ["Path", "ColorReveal", "Blur", "Scramble"],
    optionTitles: ["Path", "Color Reveal", "Blur", "Scramble"],
    defaultValue: "Path",
    displaySegmentedControl: true,
  },
  pathPreset: {
    type: ControlType.Enum,
    title: "Path",
    options: ["Arc", "Wave", "Line", "Custom"],
    optionTitles: ["Arc", "Wave", "Line", "Custom"],
    defaultValue: "Wave",
    hidden: (p: PathTypeKineticProps) => p.mode !== "Path",
  },
  customPath: {
    type: ControlType.String,
    title: "SVG Path",
    defaultValue: "",
    displayTextArea: true,
    hidden: (p: PathTypeKineticProps) =>
      p.mode !== "Path" || p.pathPreset !== "Custom",
  },
  granularity: {
    type: ControlType.Enum,
    title: "Units",
    options: ["Letter", "Word"],
    optionTitles: ["Letter", "Word"],
    defaultValue: "Letter",
    displaySegmentedControl: true,
    hidden: (p: PathTypeKineticProps) => p.mode === "Path",
  },
  fontFamily: {
    type: ControlType.String,
    title: "Font",
    defaultValue: '"Fraunces", "Georgia", serif',
  },
  fontSize: {
    type: ControlType.Number,
    title: "Size",
    min: 16,
    max: 120,
    defaultValue: 42,
  },
  fontWeight: {
    type: ControlType.Number,
    title: "Weight",
    min: 300,
    max: 900,
    step: 100,
    defaultValue: 600,
  },
  letterSpacing: {
    type: ControlType.Number,
    title: "Tracking",
    min: -4,
    max: 20,
    step: 0.5,
    defaultValue: 0,
  },
  color: {
    type: ControlType.Color,
    title: "Color",
    defaultValue: "#111111",
  },
  colorStart: {
    type: ControlType.Color,
    title: "From",
    defaultValue: "rgba(17,17,17,0.25)",
    hidden: (p: PathTypeKineticProps) => p.mode !== "ColorReveal",
  },
  colorEnd: {
    type: ControlType.Color,
    title: "To",
    defaultValue: "#111111",
    hidden: (p: PathTypeKineticProps) => p.mode !== "ColorReveal",
  },
  blurAmount: {
    type: ControlType.Number,
    title: "Blur",
    min: 0,
    max: 30,
    defaultValue: 12,
    hidden: (p: PathTypeKineticProps) => p.mode !== "Blur",
  },
  scrambleCharset: {
    type: ControlType.String,
    title: "Charset",
    defaultValue: SCRAMBLE_CHARS,
    hidden: (p: PathTypeKineticProps) => p.mode !== "Scramble",
  },
  scrambleSpeed: {
    type: ControlType.Number,
    title: "Speed",
    min: 0.25,
    max: 3,
    step: 0.25,
    defaultValue: 1,
    hidden: (p: PathTypeKineticProps) => p.mode !== "Scramble",
  },
  autoPlay: {
    type: ControlType.Boolean,
    title: "Auto Path",
    defaultValue: true,
    hidden: (p: PathTypeKineticProps) => p.mode !== "Path",
  },
  pathDuration: {
    type: ControlType.Number,
    title: "Loop (s)",
    min: 2,
    max: 20,
    defaultValue: 8,
    hidden: (p: PathTypeKineticProps) => p.mode !== "Path" || !p.autoPlay,
  },
})
