# Framer Community — @builtbykern

Human-run promotion for [Framer Community](https://www.framer.com/community/). **Not** loaded by cron agents.

## Cadence

- **1 post every 2–3 days** (offset from X daily originals)
- Reply to comments within **2–4 hours** of publish

## Source of truth

| File | Purpose |
|------|---------|
| `state/framer-community-catalog.json` | All marketplace components + metadata |
| `state/framer-community-queue.json` | Publish status per component |
| `docs/framer-community/posts/*.md` | Copy + video notes per component |

Regenerate posts after catalog edits:

```bash
python3 scripts/sync_framer_community_posts.py
```

## Publish rules

| Do | Don't |
|----|-------|
| Post type **Component** + attach card | Paste `framer.com/community/marketplace/...` in body |
| Use `framer.link` preview URLs | Marketplace links in text (blocked) |
| Attach **video** (10–25s) | Text-only posts (ineligible for Hype) |
| Point to profile: `BuiltByKern → Marketplace → [name]` | Duplicate X copy verbatim |
| **Punch copy** — 2–4 lines, name the move | Feature dumps, "Most X… This one…", bullet walls |

What already works (ranked from live posts, Aug 2026):

**Your posts**
1. **Ship story + named move** (Corner ~31♥/9💬) — personal “finally shipped” + one sensory beat + video
2. **Social roll call** (Sunday desk ~25♥/5💬) — ask city + what you’re building, go first, no pitch
3. **Contrast one-liner** (Copy Field ~22♥/4💬) — `most X… this one…` + sensory chain + framer.link
4. Avoid sterile punch (Morph / Contact Dock / Video Ring ~7–10♥, ~0💬)
5. Avoid long feature dumps for comments (Wave Dot ~17♥/1💬)

**Peer Hype (what the feed actually boosts)**
1. **Video first** — almost every Hype card is motion; text is a caption (≈8–35 words)
2. **Human > brochure** — lifestyle beat, craft joy (“couldn’t help myself”), humor, BIP micro-win
3. **Reply hooks** — “drop yours below”, “do you agree…?”, “curious for feedback”, “should I…?”
4. **Soft product** — name the move + link; let the clip sell. Hard feature lists rarely hit Hype
5. **Opinion / feedback asks** punch above product drops on comments (often 6–10💬)

## Workflow

1. Pick next `status: draft` in `state/framer-community-queue.json`
2. Open `docs/framer-community/posts/[id].md`
3. Record video per shot list
4. Community → **Post** → **Component** → select component
5. Paste body, attach video, publish
6. Set `status: published`, `published_at: YYYY-MM-DD`

## Marketplace inventory (26)

| ID | Component | Preview | Live |
|----|-----------|---------|------|
| `kinetic-line` | Kinetic Line | framer.link/9FKl60Z | yes |
| `inertia-grid` | InertiaGrid | — | yes |
| `circlecards` | CircleCards | — | yes |
| `letter-roll-menu` | LetterRollMenu | — | yes |
| `infinite-carousel-3d` | InfiniteCarousel3D | — | yes |
| `scrolling-blur` | Scrolling Blur | — | yes |
| `wave-dot-link` | Wave Dot Link | framer.link/ufE5Qk4 | yes |
| `marker-highlight` | MarkerHighlight | — | yes |
| `flowing-menu` | FlowingMenu | — | yes |
| `kinetic-grid` | Kinetic Grid | framer.link/UlKKQnq | yes |
| `corner-scroller` | Corner Scroller | — | yes |
| `spiral-3d-gallery` | Spiral 3D Gallery | — | yes |
| `curvy-showcase` | Curvy Showcase | — | yes |
| `the-scroller` | TheScroller | — | yes |
| `zoom-image-intro` | Zoom-Image Intro | framer.link/PG4L7WV | yes |
| `quote-intake` | Quote Intake | framer.link/puCPcPg | yes |
| `filling-point` | Filling Point | framer.link/BPI56ka | yes |
| `glyph-ink` | Glyph Ink | framer.link/spaxn6C | yes |
| `metric-seal` | Metric Seal | framer.link/h5lRzNs | yes |
| `drift-plane` | Drift Plane | framer.link/DV7ph9v | yes |
| `copy-field` | Copy Field | framer.link/kf8ROzJ | yes |
| `contact-dock` | Contact Dock | framer.link/OLAQE0Z | yes |
| `video-ring` | Video Ring | framer.link/sGV69QU | yes |
| `morph-dropdown` | Morph Dropdown | framer.link/mZkAB9F | yes |
| `hold-confirm` | Hold Confirm | framer.link/jCaqr0L | yes |
| `access-code` | Access Code | framer.link/x0ekBXf | yes |

**26 live** on [@builtbykern marketplace](https://www.framer.com/@builtbykern/?tab=marketplace).

## Arbour template warmup (WIP)

Staggered stills calendar (offset from X): [`arbour-warmup.md`](arbour-warmup.md) · queue `state/arbour-community-queue.json`.

## Invite link (X growth)

```
https://www.framer.com/community/join?invite=y0MfazGKzAWL
```

## Assets

- `assets/social/framer-community-hype-feed.png`
- `assets/social/framer-community-marketplace-tab.png`
- `posts/community-invite-x.md` — X invite copy (not Community)
