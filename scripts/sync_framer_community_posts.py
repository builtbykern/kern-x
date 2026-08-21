#!/usr/bin/env python3
"""Sync docs/framer-community/posts/*.md and queue from state/framer-community-catalog.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "state" / "framer-community-catalog.json"
QUEUE = ROOT / "state" / "framer-community-queue.json"
POSTS_DIR = ROOT / "docs" / "framer-community" / "posts"

POST_BODIES: dict[str, dict[str, str]] = {
    "kinetic-line": {
        "hook": "Kinetic Line — a divider you can actually pluck",
        "intro": "Most section dividers in Framer are static strokes. Hover might fade or shift them — nothing reacts to where on the line you touched or how hard you pulled.",
        "bullets": "→ hero separators\n→ editorial section breaks\n→ vertical accent lines\n→ horizontal dividers between blocks",
        "note": "Panel controls for bend, pluck, reach, tension, damping, and orientation. Subtle defaults for editorial layouts.",
        "video": "slow pluck on horizontal divider → vertical accent line → let it settle",
        "question": "Where would you drop a physics divider — hero, between sections, or as a vertical rail?",
    },
    "inertia-grid": {
        "hook": "InertiaGrid — a media grid that reacts to cursor distance",
        "intro": "Gallery grids look premium in screenshots. On hover they usually just scale. InertiaGrid gives each tile spring-based motion from cursor proximity — drift, repel, or glitch presets.",
        "bullets": "→ Drift, Repel, Glitch interaction presets\n→ per-card spring motion, rotation, and scale\n→ responsive columns, gaps, and breakpoints\n→ reduced-motion fallback + canvas guard",
        "note": "Tune content, entrance, layout, and background from the panel. Zero external dependencies.",
        "video": "cursor across grid → repel preset → drift preset → glitch micro-scatter",
        "question": "Editorial drift or bold glitch — which preset fits your layout?",
    },
    "circlecards": {
        "hook": "CircleCards — a 3D card ring that actually moves with your cursor",
        "intro": "Circular galleries in Framer usually end up as flat carousels. CircleCards lays cards on a polar ring with real depth — pointer flip, stage tilt, and optional auto-roll on publish.",
        "bullets": "→ auto-roll pauses on card hover\n→ showcase on click centers a card\n→ 6–48 cards, image + video slots\n→ film grain, vignette, glare built in",
        "note": "Auto-roll does not run on the Framer canvas. Preview on a published URL.",
        "video": "auto-roll → hover pause + flip → click showcase → card centers",
        "question": "Portfolio ring, agency reel, or product showcase — where would you drop this?",
    },
    "letter-roll-menu": {
        "hook": "LetterRollMenu — per-letter motion on a short studio nav",
        "body": "finally got per-letter motion to sit in a 4-item nav without looking like a slot machine.\n\nRoll, Wave, or Flip — the focus rail tracks the row.\n\nBuiltByKern → Marketplace → LetterRollMenu\n\nwhich signature would you actually ship?",
        "video": "/Users/noel/Desktop/Framer/docs/projects/listings/Kern_LetterRollMenu_demo_3s.mp4",
    },
    "infinite-carousel-3d": {
        "hook": "InfiniteCarousel3D — cylindrical depth without heavy 3D libraries",
        "intro": "Standard carousels feel flat and repetitive. This one uses cylindrical perspective and hardware-accelerated transforms for a seamless infinite loop — images and video.",
        "bullets": "→ infinite loop with zero layout jumps\n→ perspective + Y-axis rotation controls\n→ native video with autoplay guards\n→ flatten, scale, or lift hover states",
        "note": "30+ property controls. Responsive width, height, and gap per breakpoint.",
        "video": "infinite scroll → hover lift → mixed image + video slides",
        "question": "Hero reel, product gallery, or logo strip — where would you use a 3D carousel?",
    },
    "scrolling-blur": {
        "hook": "Scrolling Blur — backdrop blur that follows scroll",
        "intro": "Most blur chrome in Framer is a static overlay or a CSS hack. Scrolling Blur stacks soft-masked backdrop-filter layers with peak blur at the pinned edge — intentional motion design.",
        "bullets": "→ Edge, U, or ∩ shape modes\n→ top or bottom position\n→ Always On, Follow Scroll, or Off\n→ Safari-safe, pointer-events none",
        "note": "Pin over nav or footer chrome. Follow Scroll uses visibility — preview on published URL for scroll-reactive mode.",
        "video": "fixed top blur → scroll page → blur follows → settles on idle",
        "question": "Nav chrome or footer dock — top or bottom blur on your sites?",
    },
    "wave-dot-link": {
        "hook": "Wave Dot Link — a traveling marker that waves through your label",
        "intro": "Most nav links underline on hover or scale the whole word. Wave Dot Link races a marker along the baseline while characters lift, tilt, and settle with spring travel.",
        "bullets": "→ dot, dash, or square baseline marker\n→ per-letter lift, tilt, scale, trail\n→ hover or click trigger\n→ canvas matches live rest pose",
        "note": "Set label + destination, tune marker and motion from the panel.",
        "video": "hover across label → marker travels → letters lift → click variant",
        "question": "Hero CTA, vertical nav, or inline link — where would you use a traveling marker?",
    },
    "marker-highlight": {
        "hook": "MarkerHighlight — hand-drawn marker strokes over your headline",
        "intro": "Highlighting words in Framer usually means a static background color. MarkerHighlight draws SVG paths with seeded noise — spring-animated strokes that tilt toward the cursor.",
        "bullets": "→ highlight, underline, or strike-through per word\n→ draw on mount, in-view, or hover\n→ cursor tilt within adjustable radius\n→ mix-blend multiply for ink-on-paper feel",
        "note": "Up to 10 target words. Typography and animation groups per breakpoint.",
        "video": "headline loads → marker draws in → cursor tilt on hover",
        "question": "Hero headline or manifesto block — which words would you mark?",
    },
    "flowing-menu": {
        "hook": "FlowingMenu — navigation rows with real spring physics",
        "intro": "Static nav rows with flat hovers set the wrong tone. FlowingMenu triggers directional reveal overlays with infinite marquee, magnetic text, and velocity-responsive scroll.",
        "bullets": "→ five reveal modes: Edge Slide, Clip Circle, Wipe, Blur In, Split\n→ spring presets with explicit stiffness, damping, mass\n→ magnetic text scatter from cursor\n→ optional custom cursor with mix-blend-mode",
        "note": "55+ controls across 10 groups. Pill images or full background per row.",
        "video": "hover rows → clip circle from cursor → marquee velocity → magnetic text",
        "question": "Clip Circle or Edge Slide — which reveal mode fits your menu?",
    },
    "kinetic-grid": {
        "hook": "Kinetic Grid — vertical lines you can pluck like strings",
        "intro": "Static column grids do nothing on hover. Kinetic Grid turns each vertical line into a segmented string — nearest column bends with optional bleed into neighbors.",
        "bullets": "→ hero backdrops and section dividers\n→ column count + responsive breakpoints\n→ inset left/right without breaking full-bleed\n→ entrance stagger, clip bends, stroke + background",
        "note": "Lines stay straight on canvas. Physics runs in preview and on the published site only.",
        "video": "idle grid → pluck center column → neighbor bleed → settle",
        "question": "Hero backdrop, section break, or full-page texture — where would you use a pluckable grid?",
    },
    "corner-scroller": {
        "hook": "Corner Scroller — scroll-pinned portfolio with spatial handoffs",
        "intro": "Fade slideshows are not a studio index. Corner Scroller pins a stage — each project holds full-bleed, then hands off spatially as the next image grows from the corner preview.",
        "bullets": "→ corner morph or slide left handoff styles\n→ hold time + scroll distance per project\n→ frosted caption overlay (title · year · category)\n→ optional tilt/fold entrance on incoming image",
        "note": "Scroll effects are not fully represented on canvas. Preview on published URL.",
        "video": "scroll through projects → corner morph handoff → caption overlay",
        "question": "Corner morph or slide left — which handoff reads better for your portfolio?",
    },
    "spiral-3d-gallery": {
        "hook": "Spiral 3D Gallery — images in a living 3D helix",
        "intro": "Most 3D sliders fake depth with scale and fade. This one renders cards in true 3D space — z-depth drives blur, skew, and opacity every frame.",
        "bullets": "→ Editorial, Premium, Snap motion presets\n→ film grain + color grading per card\n→ responsive ring radius and card size\n→ static in editor, animates on publish",
        "note": "Drop in images, tune intensity and speed, publish. Reduced-motion fade fallback included.",
        "video": "spiral rotates → depth blur on back cards → preset switch",
        "question": "Editorial slow spiral or Snap preset — which energy fits your gallery?",
    },
    "curvy-showcase": {
        "hook": "Curvy Showcase — portfolio as a bowl ribbon, not a horizontal stack",
        "intro": "Horizontal project stacks with hover scale feel template-default. Curvy Showcase keeps scroll inside the stage — cards sit on a concave bowl arc, snap to center, and expand into fullscreen case study view.",
        "bullets": "→ wheel anywhere, drag only on cards\n→ click or settle to expand with spring choreography\n→ character-by-character title reveal\n→ optional custom cursor (project name on hover)",
        "note": "Bind CMS to Projects or use the items array. Bowl intensity and focus depth from the panel.",
        "video": "scroll ribbon → card snaps center → expand → close chip",
        "question": "Bowl ribbon or flat row — which portfolio motion fits your studio?",
    },
    "the-scroller": {
        "hook": "TheScroller — 3D slider on a real spring scroll engine",
        "intro": "Native carousels lack velocity response. TheScroller runs spring physics over wheel, touch, and keyboard — three visual presets with optional motion blur tied to scroll speed.",
        "bullets": "→ Distortion — velocity-driven scale\n→ Carousel — orbital arc with depth falloff\n→ Cards — tilted stack with organic rotation\n→ GPU-accelerated, zero layout shift",
        "note": "Per-breakpoint controls. Full keyboard and screen-reader accessibility.",
        "video": "scroll distortion preset → carousel arc → cards stack tilt",
        "question": "Distortion, Carousel, or Cards — which 3D preset would you ship?",
    },
    "zoom-image-intro": {
        "hook": "Zoom-Image Intro — a preloader that actually hands off to your page",
        "intro": "Most preloaders freeze on the last frame or cut abruptly. Zoom-Image Intro plays a stacked zoom sequence, settles the final image, then fades out to the page below.",
        "bullets": "→ image stack + delay between frames\n→ zoom amount, direction, pace curve\n→ auto dismiss + hold after sequence\n→ six editorial stills in defaults",
        "note": "Swap default images, tune timing, publish. Real dismiss timing only on live preview.",
        "video": "stacked zoom sequence → final hold → fade to page",
        "question": "Agency launch or portfolio drop — would you use a zoom preloader?",
    },
    "quote-intake": {
        "hook": "Quote Intake — multi-step quote calculator",
        "body": "Quote Intake — multi-step estimator that updates the range as they choose.\n\nIntent → Scope → Timing → Review. Webhook optional — no fake email.\n\nhttps://framer.link/puCPcPg",
        "video": "Intent → Scope slider → range updates → Review → submit",
        "x_tweet": "quote intake — multi-step estimator that updates the range as they choose. intent → scope → timing → review. webhook optional",
        "x_alt": "live quote range as they choose — intent → scope → timing → review",
        "x_media": "10–15s Intent → Scope → range → Review",
    },
    "filling-point": {
        "hook": "Filling Point — hover that paints from where you entered",
        "intro": "Invert-on-hover CTAs feel the same everywhere. Filling Point starts a seed circle at the nearest border to your pointer, then three solid disks cascade out from that exact enter point — leave reverses the whole beat.",
        "bullets": "→ pointer-enter origin (not button-center flood)\n→ seed kisses the nearest edge before cover expands\n→ three-beat cascade in, reverse cascade out\n→ Solid disks or Soft wash (gradient, not blur)",
        "note": "Ship Cinematic for the readable paint event. Canvas stays idle — motion only on preview / publish.",
        "video": "enter corner → seed on edge → three-beat flood → leave reverse → Soft wash once",
        "question": "Would you notice if the fill started from button center instead of your pointer?",
    },
    "glyph-ink": {
        "hook": "Glyph Ink — type that inks from where you entered",
        "intro": "Headline hovers usually fade the whole word the same way. Glyph Ink seeds from your pointer: each letter fills from the nearest glyph-box edge, cascades by distance, then breathes out longer than it entered.",
        "bullets": "→ pointer-origin seed per glyph (nearest edge)\n→ distance-ordered ink cascade across the line\n→ elliptical soft-tip fill — no fat diagonal disk\n→ Cinematic / Balanced / Snappy / Custom motion",
        "note": "Hover is the product — no auto-demo. Canvas holds a mid-ink rest (~55%); full motion on preview / publish. Ghost + Ink colors, Font control, touch/keyboard/reduced-motion → full text.",
        "video": "enter left of headline → letters ink by distance → leave long breathe → enter from right once",
        "question": "Hero manifesto or section title — where would pointer-origin ink land first?",
    },
    "metric-seal": {
        "hook": "Metric Seal — ink seals the figure while it counts",
        "intro": "Most metric counters just tick digits up. Metric Seal is a sealed ink event on enter view: a directional wipe fills the figure with a soft tip that hardens as coverage completes, while a bloom halo rides the front and fades into one sealed layer.",
        "bullets": "→ directional ink wipe + soft tip → hard seal\n→ bloom halo on the front, then one sealed layer\n→ From → To count on its own ease-out (never crawls with the mask)\n→ Cinematic / Balanced / Snappy motion",
        "note": "Ship Cinematic for the readable mid-body travel. Preview on published URL — enter-view is the product.",
        "video": "scroll into view → ink wipe seals figure → digits ease To → bloom fades → Snappy once on denser row",
        "question": "Stats row, pricing proof, or case-study KPI — where would you seal a metric first?",
        "x_tweet": "most metric counters just tick up. this one seals the figure with ink on enter — soft tip hardens, bloom rides the front, digits ease on their own curve so the count never crawls with the mask",
        "x_alt": "ink seals the metric while it counts — directional wipe, bloom fade, From → To on a separate ease-out",
        "x_media": "10–15s scroll-into-view seal (same shot list as Community video)",
    },
    "drift-plane": {
        "hook": "Drift Plane — an infinite image plane you actually fly through",
        "intro": "Most Framer galleries stop at a grid or carousel. Drift Plane puts cards on a toroidal 3D plane — idle drift, mouse parallax, three depth layers — so pan never hits an edge.",
        "bullets": "→ infinite toroidal wrap (no hard edges)\n→ idle drift + mouse parallax\n→ far / mid / near depth layers\n→ optional per-card links (click vs pan)\n→ Appear intro + Group Click Exit (toggleable)",
        "note": "No Auto Demo — pan and click are the product. Reduced-motion + canvas/export safe. Zero external packages.",
        "video": "idle drift → mouse parallax → drag pan wrap → click linked card + group exit",
        "question": "Portfolio void, moodboard, or lookbook — where would you drop an infinite plane?",
    },
    "copy-field": {
        "hook": "Copy Field — reveal a masked value, then copy",
        "intro": "Most Framer copy UIs are a button glued to plain text. Copy Field masks a string (or grouped digits), reveals with one tap on the eye, then copies the real value — stroke → check success, with fine-pointer hover hints for View / Copy.",
        "bullets": "→ Masked → reveal → copy → success flow\n→ Real clipboard (writeText + execCommand fallback)\n→ Optional digit grouping (4s)\n→ Hover hints (View / Copy) on fine pointer\n→ Optional inline Copied feedback chip",
        "note": "No Auto Demo — pointer is the product. Reduced-motion + canvas-safe idle. Zero external packages.",
        "video": "masked rest → View hint → reveal → Copy hint → copy → stroke→check + Copied chip",
        "question": "Pricing page, account card, or docs snippet — where would you drop a reveal-then-copy field?",
        "x_tweet": "most copy UIs are a button next to plain text. this one masks the value, reveals on the eye, then copies for real — stroke → check, hover hints for View / Copy",
        "x_alt": "masked → reveal → copy — real clipboard, digit groups, View/Copy hints, stroke→check success",
        "x_media": "8–12s View→reveal→Copy→success (same shot list as Community video)",
    },
    "contact-dock": {
        "hook": "Contact Dock — glass orb, hello sheet",
        "body": "Contact Dock — glass orb that springs a hello sheet.\n\nAvatar, greeting, up to 3 channels (book / email / tel). Pulse rings. Escape closes it.\n\nhttps://framer.link/OLAQE0Z",
        "video": "pulse orb → open sheet → channel hover → Escape close",
        "x_tweet": "contact dock — glass orb that springs a hello sheet. avatar, greeting, book / email / tel. pulse rings, escape to close",
        "x_alt": "glass orb → hello sheet — 3 channels, pulse, escape close",
        "x_media": "10–15s orb → open → Escape",
    },
    "video-ring": {
        "hook": "Video Ring — floating play/pause with a progress ring",
        "body": "Video Ring — video fills the frame, play/pause rides a radial progress ring.\n\nCorner control. Autoplay / loop / mute. Pauses offscreen.\n\nhttps://framer.link/sGV69QU",
        "video": "idle ring progress → tap pause → tap play → ring catches up",
        "x_tweet": "video ring — full-frame video, floating play/pause with a radial progress ring. pauses offscreen",
        "x_alt": "floating play/pause + radial timeline on your hero video",
        "x_media": "10–15s progress ring → pause → play",
    },
    "morph-dropdown": {
        "hook": "Morph Dropdown — liquid morph from pill to menu",
        "body": "Morph Dropdown — pill opens with a gooey metaball morph, then settles with a clean gap.\n\nSliding hover highlight. Pick one — trigger label crossfades, menu morphs closed.\n\nCanvas-safe Preview Open. Pointer is the product — no Auto Demo.\n\nhttps://framer.link/mZkAB9F",
        "video": "closed pill → gooey open → hover slide → select + label crossfade → morph closed",
        "x_tweet": "most dropdowns just expand a list. this one morphs — gooey pill to floating menu, sliding highlight, label crossfade on pick",
        "x_alt": "morph dropdown — liquid metaball from pill to menu. sliding highlight, label crossfade on pick",
        "x_media": "10–15s open → hover → select → close",
    },
    "hold-confirm": {
        "hook": "Hold Confirm — hold to commit, release cancels",
        "body": "most confirm buttons are click and hope. this one makes you hold — ink fills under the label, let go early and it snaps back.\n\nhold-to-commit or a second dialog — which would you ship for delete / pay / send?\n\nhttps://framer.link/jCaqr0L",
        "video": "hold fill → release cancel snap → full hold seal → success label → auto-reset",
        "x_tweet": "most confirm buttons are click and hope. this one makes you hold — ink fills under the label, let go early and it snaps back",
        "x_alt": "hold confirm — hold to commit, release cancels. ink fills under the label; let go early and it snaps back",
        "x_media": "10–15s cancel once → full seal once",
    },
    "access-code": {
        "hook": "Access Code — invite / OTP, paste works",
        "body": "most OTP fields fight paste. this one wants it — segmented slots fill on paste, soft unlock, optional remember.\n\ninvite gate or one-time code — which would you ship first?\n\nhttps://framer.link/x0ekBXf",
        "video": "idle slots → focus → paste code → digit stagger → Unlocked settle",
        "x_tweet": "most OTP fields fight paste. this one wants it — segmented slots fill on paste, soft unlock, optional remember",
        "x_alt": "access code — paste-first OTP / invite slots, soft unlock, remember",
        "x_media": "4–8s paste → unlock settle",
    },
}


def build_post(component: dict, body: dict[str, str]) -> str:
    preview = component.get("preview_url")
    marketplace = component.get("in_marketplace", True)
    footer = f"BuiltByKern → Marketplace → {component['name']}"
    if not marketplace:
        footer = f"BuiltByKern → {component['name']} (preview — listing pending)"

    # Punch format: short `body` block (no Most X / bullet dump)
    if "body" in body:
        post_body = body["body"].rstrip()
        if preview and preview not in post_body:
            post_body = f"{post_body}\n\n{preview}"
        post = f"""# {component['name']} — Community post

**Component:** {component['name']}
**Preview:** {preview or "(add framer.link)"}
**Category:** {component['category']}
**Marketplace slug:** `{component['slug']}`
**In marketplace:** {"yes" if marketplace else "no — preview only"}

## Hook

`{body['hook']}`

## Body

```
{post_body}

[attach video: {body['video']}]
```
"""
    else:
        preview_line = f"\nTry it live: {preview}\n" if preview else ""
        post = f"""# {component['name']} — Community post

**Component:** {component['name']}
**Preview:** {preview or "(add framer.link)"}
**Category:** {component['category']}
**Marketplace slug:** `{component['slug']}`
**In marketplace:** {"yes" if marketplace else "no — preview only"}

## Hook

`{body['hook']}`

## Body

```
{body['intro']}

{body['bullets']}

{body['note']}
{preview_line}
[attach video: {body['video']}]

{footer}

{body['question']}
```

## Pin comment

(Add canvas vs publish caveat if motion only runs on live site.)
"""

    x_tweet = body.get("x_tweet")
    if x_tweet and preview:
        x_alt = body.get("x_alt", "")
        x_media = body.get("x_media", "10–15s clip (same shot list as Community video)")
        alt_block = (
            f"\n### Short alt\n\n```\n{x_alt}\n\n{preview}\n\n#Framer #FramerMarketplace\n```\n"
            if x_alt
            else ""
        )
        post += f"""
## X / Twitter

**Channel:** X only — do not paste Community body verbatim  
**Link:** {preview}  
**Media:** {x_media}

### Tweet

```
{x_tweet}

{preview}

#Framer #FramerMarketplace
```
{alt_block}"""

    return post


def main() -> None:
    catalog = json.loads(CATALOG.read_text())
    existing_queue = {}
    if QUEUE.exists():
        for item in json.loads(QUEUE.read_text()).get("posts", []):
            existing_queue[item["id"]] = item

    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    queue_posts = []

    for component in catalog["components"]:
        cid = component["id"]
        body = POST_BODIES[cid]
        post_path = POSTS_DIR / f"{cid}.md"
        post_path.write_text(build_post(component, body))

        prior = existing_queue.get(cid, {})
        queue_posts.append(
            {
                "id": cid,
                "component": component["name"],
                "marketplace_slug": component["slug"],
                "preview_url": component.get("preview_url"),
                "in_marketplace": component.get("in_marketplace", True),
                "status": prior.get("status", "draft"),
                "scheduled": prior.get("scheduled"),
                "published_at": prior.get("published_at"),
            }
        )

    queue = {
        "cadence_days": catalog["cadence_days"],
        "invite_url": catalog["invite_url"],
        "profile": catalog["profile"],
        "posts": queue_posts,
    }
    if QUEUE.exists():
        prior_doc = json.loads(QUEUE.read_text())
        if prior_doc.get("notes"):
            queue["notes"] = prior_doc["notes"]
    QUEUE.write_text(json.dumps(queue, indent=2) + "\n")
    print(f"Wrote {len(queue_posts)} posts to {POSTS_DIR}")
    print(f"Updated {QUEUE}")


if __name__ == "__main__":
    main()
