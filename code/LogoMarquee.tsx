/**
 * Logo Marquee
 * Infinite logo strip for trusted-by sections.
 *
 * @framerSupportedLayoutWidth any
 * @framerSupportedLayoutHeight any
 * @framerIntrinsicWidth 800
 * @framerIntrinsicHeight 80
 */

import { addPropertyControls, ControlType } from "framer"
import { useEffect, useMemo, useState, type CSSProperties } from "react"

export interface MarqueeItem {
  image?: { src?: string; srcSet?: string; alt?: string } | string
  label?: string
  link?: string
}

export interface LogoMarqueeProps {
  items?: MarqueeItem[]
  speed?: number
  direction?: "Left" | "Right"
  gap?: number
  logoHeight?: number
  pauseOnHover?: boolean
  fadeEdges?: boolean
  background?: string
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

function resolveSrc(image: MarqueeItem["image"]): string {
  if (!image) return ""
  if (typeof image === "string") return image
  return image.src ?? ""
}

function resolveAlt(image: MarqueeItem["image"], fallback: string): string {
  if (!image || typeof image === "string") return fallback
  return image.alt ?? fallback
}

const DEFAULT_ITEMS: MarqueeItem[] = [
  {
    label: "North",
    image: {
      src: "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg",
      alt: "React",
    },
  },
  {
    label: "Orbit",
    image: {
      src: "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg",
      alt: "TypeScript",
    },
  },
  {
    label: "Pulse",
    image: {
      src: "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/figma/figma-original.svg",
      alt: "Figma",
    },
  },
  {
    label: "Harbor",
    image: {
      src: "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg",
      alt: "Node",
    },
  },
  {
    label: "Atlas",
    image: {
      src: "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nextjs/nextjs-original.svg",
      alt: "Next.js",
    },
  },
  {
    label: "Vera",
    image: {
      src: "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vercel/vercel-original.svg",
      alt: "Vercel",
    },
  },
]

function Track({
  items,
  gap,
  logoHeight,
}: {
  items: MarqueeItem[]
  gap: number
  logoHeight: number
}) {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap,
        flexShrink: 0,
        paddingRight: gap,
      }}
    >
      {items.map((item, index) => {
        const src = resolveSrc(item.image)
        const label = item.label ?? `Logo ${index + 1}`
        const content = src ? (
          <img
            src={src}
            alt={resolveAlt(item.image, label)}
            height={logoHeight}
            style={{
              height: logoHeight,
              width: "auto",
              maxWidth: logoHeight * 3,
              objectFit: "contain",
              display: "block",
              opacity: 0.85,
            }}
            draggable={false}
          />
        ) : (
          <span
            style={{
              fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
              fontSize: Math.max(12, logoHeight * 0.35),
              fontWeight: 600,
              letterSpacing: "0.04em",
              textTransform: "uppercase",
              color: "rgba(0,0,0,0.55)",
              whiteSpace: "nowrap",
            }}
          >
            {label}
          </span>
        )

        const wrapStyle: CSSProperties = {
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          height: logoHeight,
          flexShrink: 0,
          textDecoration: "none",
        }

        if (item.link) {
          return (
            <a
              key={`${label}-${index}`}
              href={item.link}
              target="_blank"
              rel="noreferrer"
              style={wrapStyle}
            >
              {content}
            </a>
          )
        }

        return (
          <div key={`${label}-${index}`} style={wrapStyle}>
            {content}
          </div>
        )
      })}
    </div>
  )
}

/**
 * Logo Marquee — seamless infinite logo strip with pause-on-hover and edge fades.
 */
export default function LogoMarquee(props: LogoMarqueeProps) {
  const {
    items = DEFAULT_ITEMS,
    speed = 40,
    direction = "Left",
    gap = 48,
    logoHeight = 32,
    pauseOnHover = true,
    fadeEdges = true,
    background = "transparent",
    style,
  } = props

  const prefersReduced = usePrefersReducedMotion()
  const safeItems = useMemo(
    () => (items.length > 0 ? items : DEFAULT_ITEMS),
    [items]
  )

  // CSS duration from speed (px/s approximation via fixed track feel)
  const duration = Math.max(8, 1200 / Math.max(10, speed))
  const animName = direction === "Left" ? "logoMarqueeLeft" : "logoMarqueeRight"

  return (
    <div
      style={{
        position: "relative",
        width: "100%",
        overflow: "hidden",
        background,
        ...style,
      }}
      aria-label="Logo marquee"
    >
      <div
        className={pauseOnHover && !prefersReduced ? "logo-marquee-hover" : undefined}
        style={{
          display: "flex",
          width: "max-content",
          animation:
            prefersReduced
              ? undefined
              : `${animName} ${duration}s linear infinite`,
        }}
      >
        <Track items={safeItems} gap={gap} logoHeight={logoHeight} />
        {!prefersReduced ? (
          <Track items={safeItems} gap={gap} logoHeight={logoHeight} />
        ) : null}
      </div>

      {fadeEdges ? (
        <>
          <div
            style={{
              position: "absolute",
              left: 0,
              top: 0,
              bottom: 0,
              width: 64,
              pointerEvents: "none",
              background: `linear-gradient(90deg, ${background === "transparent" ? "#ffffff" : background}, transparent)`,
              opacity: background === "transparent" ? 0.95 : 1,
            }}
          />
          <div
            style={{
              position: "absolute",
              right: 0,
              top: 0,
              bottom: 0,
              width: 64,
              pointerEvents: "none",
              background: `linear-gradient(270deg, ${background === "transparent" ? "#ffffff" : background}, transparent)`,
              opacity: background === "transparent" ? 0.95 : 1,
            }}
          />
        </>
      ) : null}

      <style>{`
        @keyframes logoMarqueeLeft {
          from { transform: translateX(0); }
          to { transform: translateX(-50%); }
        }
        @keyframes logoMarqueeRight {
          from { transform: translateX(-50%); }
          to { transform: translateX(0); }
        }
        .logo-marquee-hover:hover {
          animation-play-state: paused !important;
        }
      `}</style>
    </div>
  )
}

LogoMarquee.displayName = "LogoMarquee"

LogoMarquee.defaultProps = {
  items: DEFAULT_ITEMS,
  speed: 40,
  direction: "Left" as const,
  gap: 48,
  logoHeight: 32,
  pauseOnHover: true,
  fadeEdges: true,
  background: "transparent",
}

addPropertyControls(LogoMarquee, {
  items: {
    type: ControlType.Array,
    title: "Logos",
    control: {
      type: ControlType.Object,
      controls: {
        image: { type: ControlType.ResponsiveImage, title: "Image" },
        label: { type: ControlType.String, title: "Label", defaultValue: "Brand" },
        link: { type: ControlType.Link, title: "Link" },
      },
    },
  },
  speed: {
    type: ControlType.Number,
    title: "Speed",
    min: 10,
    max: 120,
    defaultValue: 40,
    description: "Higher = faster.",
  },
  direction: {
    type: ControlType.Enum,
    title: "Direction",
    options: ["Left", "Right"],
    optionTitles: ["Left", "Right"],
    defaultValue: "Left",
    displaySegmentedControl: true,
  },
  gap: {
    type: ControlType.Number,
    title: "Gap",
    min: 12,
    max: 96,
    defaultValue: 48,
  },
  logoHeight: {
    type: ControlType.Number,
    title: "Logo H",
    min: 16,
    max: 96,
    defaultValue: 32,
  },
  pauseOnHover: {
    type: ControlType.Boolean,
    title: "Pause Hover",
    defaultValue: true,
  },
  fadeEdges: {
    type: ControlType.Boolean,
    title: "Fade Edges",
    defaultValue: true,
  },
  background: {
    type: ControlType.Color,
    title: "Background",
    defaultValue: "transparent",
  },
})
