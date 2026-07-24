import { addPropertyControls, ControlType } from "framer"
import {
  motion,
  useMotionValueEvent,
  useScroll,
  useTransform,
  type MotionValue,
} from "framer-motion"
import { useEffect, useMemo, useRef, useState, type CSSProperties } from "react"
import { clamp, usePrefersReducedMotion } from "../shared/motion"

export type StoryMode = "Zoom" | "Curtain" | "Slice"

export interface StoryItem {
  title?: string
  caption?: string
  image?: { src?: string; srcSet?: string; alt?: string } | string
}

export interface ScrollStoryStageProps {
  mode?: StoryMode
  items?: StoryItem[]
  sectionHeightVh?: number
  stickyTop?: number
  background?: string
  textColor?: string
  captionColor?: string
  accentColor?: string
  showProgress?: boolean
  showCaptions?: boolean
  zoomStart?: number
  zoomEnd?: number
  curtainOverlap?: number
  reduceMotionOverride?: boolean
  style?: CSSProperties
}

function resolveImageSrc(image: StoryItem["image"]): string {
  if (!image) return ""
  if (typeof image === "string") return image
  return image.src ?? ""
}

function resolveImageAlt(image: StoryItem["image"], fallback: string): string {
  if (!image || typeof image === "string") return fallback
  return image.alt ?? fallback
}

const DEFAULT_ITEMS: StoryItem[] = [
  {
    title: "Launch",
    caption: "Open with intent — one frame, one message.",
    image: {
      src: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1600&q=80",
      alt: "Abstract gradient launch visual",
    },
  },
  {
    title: "Focus",
    caption: "Guide attention through scroll, not clutter.",
    image: {
      src: "https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?auto=format&fit=crop&w=1600&q=80",
      alt: "Soft abstract focus visual",
    },
  },
  {
    title: "Reveal",
    caption: "End on the product moment that converts.",
    image: {
      src: "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?auto=format&fit=crop&w=1600&q=80",
      alt: "Colorful reveal visual",
    },
  },
]

function useInViewPause(ref: React.RefObject<HTMLElement | null>) {
  const [active, setActive] = useState(true)

  useEffect(() => {
    const el = ref.current
    if (!el || typeof IntersectionObserver === "undefined") return

    const io = new IntersectionObserver(
      ([entry]) => setActive(entry.isIntersecting),
      { rootMargin: "20% 0px", threshold: 0 }
    )
    io.observe(el)
    return () => io.disconnect()
  }, [ref])

  return active
}

function useLocalProgress(
  scrollYProgress: MotionValue<number>,
  index: number,
  count: number
) {
  return useTransform(scrollYProgress, (v) => {
    const start = index / count
    const end = (index + 1) / count
    if (end === start) return 0
    return clamp((v - start) / (end - start), 0, 1)
  })
}

function StageProgress({
  progress,
  count,
  accent,
  activeIndex,
}: {
  progress: MotionValue<number>
  count: number
  accent: string
  activeIndex: number
}) {
  const width = useTransform(progress, (v) => `${clamp(v, 0, 1) * 100}%`)

  return (
    <div
      style={{
        position: "absolute",
        left: 24,
        right: 24,
        bottom: 24,
        zIndex: 20,
        display: "flex",
        flexDirection: "column",
        gap: 10,
      }}
    >
      <div
        style={{
          height: 2,
          borderRadius: 999,
          background: "rgba(255,255,255,0.2)",
          overflow: "hidden",
        }}
      >
        <motion.div
          style={{
            height: "100%",
            width,
            background: accent,
            transformOrigin: "left center",
          }}
        />
      </div>
      <div style={{ display: "flex", gap: 8, justifyContent: "center" }}>
        {Array.from({ length: count }).map((_, i) => (
          <div
            key={i}
            style={{
              width: 6,
              height: 6,
              borderRadius: "50%",
              background: i === activeIndex ? accent : "rgba(255,255,255,0.35)",
              transition: "background 200ms ease",
            }}
          />
        ))}
      </div>
    </div>
  )
}

function CopyBlock({
  title,
  caption,
  textColor,
  captionColor,
  showCaptions,
}: {
  title?: string
  caption?: string
  textColor: string
  captionColor: string
  showCaptions: boolean
}) {
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        display: "flex",
        flexDirection: "column",
        justifyContent: "flex-end",
        padding: "48px 40px 72px",
        background:
          "linear-gradient(180deg, rgba(0,0,0,0) 35%, rgba(0,0,0,0.72) 100%)",
        pointerEvents: "none",
      }}
    >
      {title ? (
        <h2
          style={{
            margin: 0,
            fontFamily: '"Instrument Sans", "Segoe UI", system-ui, sans-serif',
            fontSize: "clamp(2rem, 5vw, 3.5rem)",
            fontWeight: 600,
            letterSpacing: "-0.03em",
            color: textColor,
            lineHeight: 1.05,
          }}
        >
          {title}
        </h2>
      ) : null}
      {showCaptions && caption ? (
        <p
          style={{
            margin: "12px 0 0",
            maxWidth: 420,
            fontFamily: '"IBM Plex Sans", "Segoe UI", system-ui, sans-serif',
            fontSize: "clamp(0.95rem, 1.6vw, 1.125rem)",
            lineHeight: 1.45,
            color: captionColor,
          }}
        >
          {caption}
        </p>
      ) : null}
    </div>
  )
}

const fill: CSSProperties = {
  position: "absolute",
  inset: 0,
  overflow: "hidden",
}

const media: CSSProperties = {
  width: "100%",
  height: "100%",
  objectFit: "cover",
  display: "block",
}

function StoryLayer({
  item,
  index,
  count,
  mode,
  scrollYProgress,
  zoomStart,
  zoomEnd,
  curtainOverlap,
  textColor,
  captionColor,
  showCaptions,
  staticMode,
}: {
  item: StoryItem
  index: number
  count: number
  mode: StoryMode
  scrollYProgress: MotionValue<number>
  zoomStart: number
  zoomEnd: number
  curtainOverlap: number
  textColor: string
  captionColor: string
  showCaptions: boolean
  staticMode: boolean
}) {
  const local = useLocalProgress(scrollYProgress, index, count)
  const src = resolveImageSrc(item.image)
  const alt = resolveImageAlt(item.image, item.title ?? "Story")

  const zoomScale = useTransform(local, [0, 1], [zoomStart, zoomEnd])
  const zoomOpacity = useTransform(local, [0, 0.15, 0.85, 1], [0, 1, 1, 0])
  const zoomY = useTransform(local, [0, 1], [40, -40])

  const curtainClip = useTransform(local, [0, 1], [
    "inset(0% 0% 100% 0%)",
    `inset(0% 0% ${Math.max(0, 100 - curtainOverlap)}% 0%)`,
  ])
  const curtainOpacity = useTransform(local, [0, 0.2, 1], [0.4, 1, 1])

  const sliceX = useTransform(local, [0, 1], ["28%", "0%"])
  const sliceOpacity = useTransform(local, [0, 0.2, 0.8, 1], [0, 1, 1, 0])
  const sliceSkew = useTransform(local, [0, 0.5, 1], [8, 0, -4])

  const copy = (
    <CopyBlock
      title={item.title}
      caption={item.caption}
      textColor={textColor}
      captionColor={captionColor}
      showCaptions={showCaptions}
    />
  )

  const imageNode = src ? (
    <img src={src} alt={alt} style={media} />
  ) : (
    <div style={{ ...media, background: "#1a1a1a" }} />
  )

  if (staticMode) {
    const visible = index === 0
    return (
      <div style={{ ...fill, opacity: visible ? 1 : 0, zIndex: index + 1 }}>
        {imageNode}
        {copy}
      </div>
    )
  }

  switch (mode) {
    case "Zoom":
      return (
        <motion.div style={{ ...fill, opacity: zoomOpacity, zIndex: index + 1 }}>
          {src ? (
            <motion.img src={src} alt={alt} style={{ ...media, scale: zoomScale }} />
          ) : (
            <div style={{ ...media, background: "#1a1a1a" }} />
          )}
          <motion.div style={{ y: zoomY, width: "100%" }}>{copy}</motion.div>
        </motion.div>
      )
    case "Curtain":
      return (
        <motion.div
          style={{
            ...fill,
            zIndex: index + 1,
            clipPath: curtainClip,
            opacity: curtainOpacity,
          }}
        >
          {imageNode}
          {copy}
        </motion.div>
      )
    case "Slice":
      return (
        <motion.div
          style={{
            ...fill,
            opacity: sliceOpacity,
            x: sliceX,
            skewX: sliceSkew,
            zIndex: index + 1,
          }}
        >
          {imageNode}
          {copy}
        </motion.div>
      )
    default: {
      const _exhaustive: never = mode
      return _exhaustive
    }
  }
}

/**
 * Scroll Story Stage — cinematic scroll storytelling for SaaS & portfolios.
 * Modes: Zoom | Curtain | Slice. Sticky stage + offscreen pause + reduced motion.
 */
export default function ScrollStoryStage(props: ScrollStoryStageProps) {
  const {
    mode = "Zoom",
    items = DEFAULT_ITEMS,
    sectionHeightVh = 300,
    stickyTop = 0,
    background = "#0b0b0c",
    textColor = "#ffffff",
    captionColor = "rgba(255,255,255,0.78)",
    accentColor = "#e8ff6a",
    showProgress = true,
    showCaptions = true,
    zoomStart = 1.35,
    zoomEnd = 1,
    curtainOverlap = 8,
    reduceMotionOverride = false,
    style,
  } = props

  const sectionRef = useRef<HTMLDivElement>(null)
  const prefersReduced = usePrefersReducedMotion()
  const staticMode = reduceMotionOverride || prefersReduced
  const inView = useInViewPause(sectionRef)

  const safeItems = useMemo(() => {
    const list = items.length > 0 ? items : DEFAULT_ITEMS
    return list.slice(0, 8)
  }, [items])
  const count = safeItems.length

  const { scrollYProgress } = useScroll({
    target: sectionRef,
    offset: ["start start", "end end"],
  })

  const [activeIndex, setActiveIndex] = useState(0)

  useMotionValueEvent(scrollYProgress, "change", (v) => {
    if (!inView && !staticMode) return
    const idx = Math.min(count - 1, Math.floor(clamp(v, 0, 0.999) * count))
    setActiveIndex(idx)
  })

  const frozen = staticMode || !inView

  return (
    <section
      ref={sectionRef}
      style={{
        position: "relative",
        height: `${Math.max(150, sectionHeightVh)}vh`,
        background,
        ...style,
      }}
      aria-label="Scroll story stage"
    >
      <div
        style={{
          position: "sticky",
          top: stickyTop,
          height: "100vh",
          width: "100%",
          overflow: "hidden",
        }}
      >
        <div style={{ position: "relative", width: "100%", height: "100%" }}>
          {safeItems.map((item, index) => (
            <StoryLayer
              key={`${item.title ?? "item"}-${index}`}
              item={item}
              index={index}
              count={count}
              mode={mode}
              scrollYProgress={scrollYProgress}
              zoomStart={zoomStart}
              zoomEnd={zoomEnd}
              curtainOverlap={curtainOverlap}
              textColor={textColor}
              captionColor={captionColor}
              showCaptions={showCaptions}
              staticMode={frozen}
            />
          ))}
          {showProgress && !staticMode ? (
            <StageProgress
              progress={scrollYProgress}
              count={count}
              accent={accentColor}
              activeIndex={activeIndex}
            />
          ) : null}
        </div>
      </div>
    </section>
  )
}

ScrollStoryStage.displayName = "ScrollStoryStage"

ScrollStoryStage.defaultProps = {
  mode: "Zoom" as StoryMode,
  items: DEFAULT_ITEMS,
  sectionHeightVh: 300,
  stickyTop: 0,
  background: "#0b0b0c",
  textColor: "#ffffff",
  captionColor: "rgba(255,255,255,0.78)",
  accentColor: "#e8ff6a",
  showProgress: true,
  showCaptions: true,
  zoomStart: 1.35,
  zoomEnd: 1,
  curtainOverlap: 8,
  reduceMotionOverride: false,
}

addPropertyControls(ScrollStoryStage, {
  mode: {
    type: ControlType.Enum,
    title: "Mode",
    options: ["Zoom", "Curtain", "Slice"],
    optionTitles: ["Zoom", "Curtain", "Slice"],
    defaultValue: "Zoom",
    displaySegmentedControl: true,
  },
  items: {
    type: ControlType.Array,
    title: "Scenes",
    maxCount: 8,
    control: {
      type: ControlType.Object,
      controls: {
        title: { type: ControlType.String, title: "Title", defaultValue: "Scene" },
        caption: {
          type: ControlType.String,
          title: "Caption",
          defaultValue: "Supporting line",
          displayTextArea: true,
        },
        image: { type: ControlType.ResponsiveImage, title: "Image" },
      },
    },
  },
  sectionHeightVh: {
    type: ControlType.Number,
    title: "Height (vh)",
    min: 150,
    max: 600,
    step: 10,
    defaultValue: 300,
    description: "Taller = slower scroll storytelling.",
  },
  stickyTop: {
    type: ControlType.Number,
    title: "Sticky Top",
    min: 0,
    max: 200,
    defaultValue: 0,
  },
  background: { type: ControlType.Color, title: "Background", defaultValue: "#0b0b0c" },
  textColor: { type: ControlType.Color, title: "Title", defaultValue: "#ffffff" },
  captionColor: {
    type: ControlType.Color,
    title: "Caption",
    defaultValue: "rgba(255,255,255,0.78)",
  },
  accentColor: { type: ControlType.Color, title: "Accent", defaultValue: "#e8ff6a" },
  showProgress: {
    type: ControlType.Boolean,
    title: "Progress",
    defaultValue: true,
    enabledTitle: "Show",
    disabledTitle: "Hide",
  },
  showCaptions: {
    type: ControlType.Boolean,
    title: "Captions",
    defaultValue: true,
    enabledTitle: "Show",
    disabledTitle: "Hide",
  },
  zoomStart: {
    type: ControlType.Number,
    title: "Zoom Start",
    min: 1,
    max: 2.5,
    step: 0.05,
    defaultValue: 1.35,
    hidden: (p: ScrollStoryStageProps) => p.mode !== "Zoom",
  },
  zoomEnd: {
    type: ControlType.Number,
    title: "Zoom End",
    min: 0.6,
    max: 1.5,
    step: 0.05,
    defaultValue: 1,
    hidden: (p: ScrollStoryStageProps) => p.mode !== "Zoom",
  },
  curtainOverlap: {
    type: ControlType.Number,
    title: "Overlap %",
    min: 0,
    max: 40,
    defaultValue: 8,
    hidden: (p: ScrollStoryStageProps) => p.mode !== "Curtain",
  },
  reduceMotionOverride: {
    type: ControlType.Boolean,
    title: "Force Static",
    defaultValue: false,
    description: "Disables scroll motion (also respects prefers-reduced-motion).",
  },
})
