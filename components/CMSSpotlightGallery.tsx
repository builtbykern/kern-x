import { addPropertyControls, ControlType } from "framer"
import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
  type KeyboardEvent,
  type PointerEvent as ReactPointerEvent,
} from "react"
import { clamp, usePrefersReducedMotion } from "../shared/motion"

export interface GalleryItem {
  title?: string
  caption?: string
  tag?: string
  link?: string
  image?: { src?: string; srcSet?: string; alt?: string } | string
}

export interface CMSSpotlightGalleryProps {
  items?: GalleryItem[]
  itemWidth?: number
  itemGap?: number
  height?: number
  background?: string
  textColor?: string
  mutedColor?: string
  accentColor?: string
  showProgress?: boolean
  showTags?: boolean
  snap?: boolean
  borderRadius?: number
  style?: CSSProperties
}

function resolveImageSrc(image: GalleryItem["image"]): string {
  if (!image) return ""
  if (typeof image === "string") return image
  return image.src ?? ""
}

function resolveImageAlt(image: GalleryItem["image"], fallback: string): string {
  if (!image || typeof image === "string") return fallback
  return image.alt ?? fallback
}

const DEFAULT_ITEMS: GalleryItem[] = [
  {
    title: "Northline Studio",
    caption: "Brand system for a climate-tech launch.",
    tag: "Branding",
    link: "#",
    image: {
      src: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80",
      alt: "Northline case study",
    },
  },
  {
    title: "Harbor CMS",
    caption: "Editorial layout rebuilt for weekly publishing.",
    tag: "Product",
    link: "#",
    image: {
      src: "https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?auto=format&fit=crop&w=1200&q=80",
      alt: "Harbor CMS case study",
    },
  },
  {
    title: "Atlas Gallery",
    caption: "Scroll-safe media wall for a photography archive.",
    tag: "Web",
    link: "#",
    image: {
      src: "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?auto=format&fit=crop&w=1200&q=80",
      alt: "Atlas Gallery case study",
    },
  },
  {
    title: "Pulse Metrics",
    caption: "Dashboard storytelling for SaaS onboarding.",
    tag: "SaaS",
    link: "#",
    image: {
      src: "https://images.unsplash.com/photo-1557672172-298e090bd0f1?auto=format&fit=crop&w=1200&q=80",
      alt: "Pulse Metrics case study",
    },
  },
]

/**
 * CMS Spotlight Gallery — horizontal snap gallery with sticky active title.
 * Bind `items` to a Framer CMS collection (image, title, tag, link, caption).
 */
export default function CMSSpotlightGallery(props: CMSSpotlightGalleryProps) {
  const {
    items = DEFAULT_ITEMS,
    itemWidth = 320,
    itemGap = 20,
    height = 520,
    background = "#eef2ef",
    textColor = "#12201c",
    mutedColor = "rgba(18,32,28,0.62)",
    accentColor = "#0f6b5c",
    showProgress = true,
    showTags = true,
    snap = true,
    borderRadius = 18,
    style,
  } = props

  const scrollerRef = useRef<HTMLDivElement>(null)
  const prefersReduced = usePrefersReducedMotion()
  const safeItems = useMemo(
    () => (items.length > 0 ? items : DEFAULT_ITEMS),
    [items]
  )

  const [activeIndex, setActiveIndex] = useState(0)
  const [dragging, setDragging] = useState(false)
  const dragState = useRef({
    active: false,
    startX: 0,
    scrollLeft: 0,
    moved: false,
  })

  const updateActive = useCallback(() => {
    const el = scrollerRef.current
    if (!el) return
    const stride = itemWidth + itemGap
    const idx = Math.round(el.scrollLeft / stride)
    setActiveIndex(clamp(idx, 0, safeItems.length - 1))
  }, [itemGap, itemWidth, safeItems.length])

  useEffect(() => {
    const el = scrollerRef.current
    if (!el) return
    updateActive()
    const onScroll = () => updateActive()
    el.addEventListener("scroll", onScroll, { passive: true })
    return () => el.removeEventListener("scroll", onScroll)
  }, [updateActive])

  const scrollToIndex = useCallback(
    (index: number) => {
      const el = scrollerRef.current
      if (!el) return
      const next = clamp(index, 0, safeItems.length - 1)
      const stride = itemWidth + itemGap
      el.scrollTo({
        left: next * stride,
        behavior: prefersReduced ? "auto" : "smooth",
      })
      setActiveIndex(next)
    },
    [itemGap, itemWidth, prefersReduced, safeItems.length]
  )

  const onKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "ArrowRight") {
      e.preventDefault()
      scrollToIndex(activeIndex + 1)
    } else if (e.key === "ArrowLeft") {
      e.preventDefault()
      scrollToIndex(activeIndex - 1)
    } else if (e.key === "Home") {
      e.preventDefault()
      scrollToIndex(0)
    } else if (e.key === "End") {
      e.preventDefault()
      scrollToIndex(safeItems.length - 1)
    }
  }

  const onPointerDown = (e: ReactPointerEvent<HTMLDivElement>) => {
    const el = scrollerRef.current
    if (!el) return
    dragState.current = {
      active: true,
      startX: e.clientX,
      scrollLeft: el.scrollLeft,
      moved: false,
    }
    setDragging(true)
    el.setPointerCapture(e.pointerId)
  }

  const onPointerMove = (e: ReactPointerEvent<HTMLDivElement>) => {
    const el = scrollerRef.current
    if (!el || !dragState.current.active) return
    const dx = e.clientX - dragState.current.startX
    if (Math.abs(dx) > 4) dragState.current.moved = true
    el.scrollLeft = dragState.current.scrollLeft - dx
  }

  const endDrag = (e: ReactPointerEvent<HTMLDivElement>) => {
    const el = scrollerRef.current
    if (!el || !dragState.current.active) return
    dragState.current.active = false
    setDragging(false)
    try {
      el.releasePointerCapture(e.pointerId)
    } catch {
      // already released
    }
    if (snap) {
      const stride = itemWidth + itemGap
      const idx = Math.round(el.scrollLeft / stride)
      scrollToIndex(idx)
    } else {
      updateActive()
    }
  }

  const active = safeItems[activeIndex] ?? safeItems[0]
  const progress = safeItems.length <= 1 ? 1 : activeIndex / (safeItems.length - 1)

  return (
    <section
      style={{
        position: "relative",
        width: "100%",
        background,
        color: textColor,
        padding: "32px 0 40px",
        overflow: "hidden",
        ...style,
      }}
      aria-roledescription="carousel"
      aria-label="CMS spotlight gallery"
    >
      <div
        style={{
          position: "sticky",
          top: 0,
          zIndex: 2,
          padding: "0 28px 20px",
          display: "grid",
          gap: 8,
          background: `linear-gradient(180deg, ${background} 70%, transparent)`,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "baseline",
            justifyContent: "space-between",
            gap: 16,
            flexWrap: "wrap",
          }}
        >
          <div style={{ minWidth: 0 }}>
            {showTags && active?.tag ? (
              <div
                style={{
                  fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
                  fontSize: 12,
                  letterSpacing: "0.08em",
                  textTransform: "uppercase",
                  color: accentColor,
                  marginBottom: 6,
                }}
              >
                {active.tag}
              </div>
            ) : null}
            <h3
              style={{
                margin: 0,
                fontFamily: '"Instrument Sans", system-ui, sans-serif',
                fontSize: "clamp(1.5rem, 3vw, 2.25rem)",
                fontWeight: 600,
                letterSpacing: "-0.03em",
                lineHeight: 1.1,
              }}
            >
              {active?.title ?? "Untitled"}
            </h3>
            {active?.caption ? (
              <p
                style={{
                  margin: "8px 0 0",
                  maxWidth: 480,
                  fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
                  fontSize: 15,
                  lineHeight: 1.45,
                  color: mutedColor,
                }}
              >
                {active.caption}
              </p>
            ) : null}
          </div>
          <div
            style={{
              display: "flex",
              gap: 8,
              alignItems: "center",
            }}
          >
            <NavButton
              label="Previous"
              onClick={() => scrollToIndex(activeIndex - 1)}
              disabled={activeIndex <= 0}
              color={textColor}
            />
            <NavButton
              label="Next"
              onClick={() => scrollToIndex(activeIndex + 1)}
              disabled={activeIndex >= safeItems.length - 1}
              color={textColor}
            />
          </div>
        </div>
        {showProgress ? (
          <div
            style={{
              height: 2,
              borderRadius: 999,
              background: "rgba(20,18,16,0.12)",
              overflow: "hidden",
            }}
          >
            <div
              style={{
                height: "100%",
                width: `${progress * 100}%`,
                background: accentColor,
                transition: prefersReduced ? undefined : "width 200ms ease",
              }}
            />
          </div>
        ) : null}
      </div>

      <div
        ref={scrollerRef}
        role="list"
        tabIndex={0}
        onKeyDown={onKeyDown}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={endDrag}
        onPointerCancel={endDrag}
        style={{
          display: "flex",
          gap: itemGap,
          overflowX: "auto",
          overflowY: "hidden",
          padding: "8px 28px 12px",
          scrollSnapType: snap ? "x mandatory" : undefined,
          cursor: dragging ? "grabbing" : "grab",
          touchAction: "pan-y",
          WebkitOverflowScrolling: "touch",
          scrollbarWidth: "none",
          msOverflowStyle: "none",
          outline: "none",
        }}
        aria-live="polite"
      >
        {safeItems.map((item, index) => {
          const src = resolveImageSrc(item.image)
          const href = item.link?.trim()
          const isActive = index === activeIndex
          const card = (
            <article
              role="listitem"
              aria-current={isActive ? "true" : undefined}
              style={{
                flex: `0 0 ${itemWidth}px`,
                width: itemWidth,
                height,
                scrollSnapAlign: snap ? "start" : undefined,
                borderRadius,
                overflow: "hidden",
                position: "relative",
                background: "#1a1a1a",
                transform: isActive ? "scale(1)" : "scale(0.97)",
                opacity: isActive ? 1 : 0.78,
                transition: prefersReduced
                  ? undefined
                  : "transform 220ms ease, opacity 220ms ease",
                boxShadow: isActive
                  ? "0 18px 40px rgba(20,18,16,0.18)"
                  : "none",
              }}
            >
              {src ? (
                <img
                  src={src}
                  alt={resolveImageAlt(item.image, item.title ?? "Gallery item")}
                  draggable={false}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                    display: "block",
                    pointerEvents: "none",
                    userSelect: "none",
                  }}
                />
              ) : null}
              <div
                style={{
                  position: "absolute",
                  left: 16,
                  right: 16,
                  bottom: 16,
                  color: "#fff",
                  fontFamily: '"Instrument Sans", system-ui, sans-serif',
                  fontSize: 14,
                  fontWeight: 500,
                  textShadow: "0 1px 8px rgba(0,0,0,0.45)",
                }}
              >
                {item.title}
              </div>
            </article>
          )

          if (href) {
            return (
              <a
                key={`${item.title ?? "item"}-${index}`}
                href={href}
                onClick={(e) => {
                  if (dragState.current.moved) {
                    e.preventDefault()
                  }
                }}
                style={{ textDecoration: "none", color: "inherit" }}
              >
                {card}
              </a>
            )
          }

          return (
            <div key={`${item.title ?? "item"}-${index}`} onClick={() => scrollToIndex(index)}>
              {card}
            </div>
          )
        })}
      </div>

      <style>{`
        [aria-label="CMS spotlight gallery"] [role="list"]::-webkit-scrollbar {
          display: none;
        }
      `}</style>
    </section>
  )
}

function NavButton({
  label,
  onClick,
  disabled,
  color,
}: {
  label: string
  onClick: () => void
  disabled: boolean
  color: string
}) {
  return (
    <button
      type="button"
      aria-label={label}
      onClick={onClick}
      disabled={disabled}
      style={{
        width: 40,
        height: 40,
        borderRadius: 999,
        border: `1px solid ${color}`,
        background: "transparent",
        color,
        opacity: disabled ? 0.35 : 1,
        cursor: disabled ? "not-allowed" : "pointer",
        fontSize: 16,
        lineHeight: 1,
      }}
    >
      {label === "Previous" ? "←" : "→"}
    </button>
  )
}

CMSSpotlightGallery.displayName = "CMSSpotlightGallery"

CMSSpotlightGallery.defaultProps = {
  items: DEFAULT_ITEMS,
  itemWidth: 320,
  itemGap: 20,
  height: 520,
  background: "#eef2ef",
  textColor: "#12201c",
  mutedColor: "rgba(18,32,28,0.62)",
  accentColor: "#0f6b5c",
  showProgress: true,
  showTags: true,
  snap: true,
  borderRadius: 18,
}

addPropertyControls(CMSSpotlightGallery, {
  items: {
    type: ControlType.Array,
    title: "Items (CMS)",
    description:
      "Map from a Framer CMS collection: image, title, caption, tag, link.",
    control: {
      type: ControlType.Object,
      controls: {
        title: { type: ControlType.String, title: "Title", defaultValue: "Project" },
        caption: {
          type: ControlType.String,
          title: "Caption",
          defaultValue: "Short description",
          displayTextArea: true,
        },
        tag: { type: ControlType.String, title: "Tag", defaultValue: "Work" },
        link: { type: ControlType.Link, title: "Link" },
        image: { type: ControlType.ResponsiveImage, title: "Image" },
      },
    },
  },
  itemWidth: {
    type: ControlType.Number,
    title: "Card Width",
    min: 200,
    max: 640,
    defaultValue: 320,
  },
  itemGap: {
    type: ControlType.Number,
    title: "Gap",
    min: 8,
    max: 48,
    defaultValue: 20,
  },
  height: {
    type: ControlType.Number,
    title: "Height",
    min: 280,
    max: 800,
    defaultValue: 520,
  },
  borderRadius: {
    type: ControlType.Number,
    title: "Radius",
    min: 0,
    max: 40,
    defaultValue: 18,
  },
  background: {
    type: ControlType.Color,
    title: "Background",
    defaultValue: "#eef2ef",
  },
  textColor: {
    type: ControlType.Color,
    title: "Text",
    defaultValue: "#12201c",
  },
  mutedColor: {
    type: ControlType.Color,
    title: "Muted",
    defaultValue: "rgba(18,32,28,0.62)",
  },
  accentColor: {
    type: ControlType.Color,
    title: "Accent",
    defaultValue: "#0f6b5c",
  },
  showProgress: {
    type: ControlType.Boolean,
    title: "Progress",
    defaultValue: true,
  },
  showTags: {
    type: ControlType.Boolean,
    title: "Tags",
    defaultValue: true,
  },
  snap: {
    type: ControlType.Boolean,
    title: "Snap",
    defaultValue: true,
  },
})
