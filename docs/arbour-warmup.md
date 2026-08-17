# Arbour X warmup — multi-day schedule

Human / Sunday plan. **Not** loaded by cron by default. Template is WIP — no launch posts.

Source media (sibling Framer repo):

- Clips / stills: `/Users/noel/Desktop/Framer/docs/projects/arbour/media/{clips,stills}`
- Copy pack: `…/media/COPY.md`
- Index: `…/media/INDEX.md`
- Live site (internal only — **do not post** the URL while WIP): `arbour.framer.website`

Queue (executable): [`state/arbour-warmup-queue.json`](../state/arbour-warmup-queue.json)

Apply into week plan after `build_week.py`:

```bash
python3 scripts/build_week.py --keep-counters   # Sunday / new week
python3 scripts/apply_arbour_warmup.py          # overlay *this ISO week only*
```

On **2026-08-03** (Mon / W32): run both again so Mon–Fri Arbour slots replace Marketplace defaults for that week.

Mark posted:

```bash
python3 scripts/apply_arbour_warmup.py --mark-posted 2026-07-30 --url 'https://x.com/…'
```

---

## Inventory ↔ COPY map

### Clips (10)

| Clip ID | File | COPY pill | Angle |
| --- | --- | --- | --- |
| `d-home-scroll-intro` | `clips/d-home-scroll-intro.mp4` | 1 | Home hero / scroll open |
| `d-home-territory-motion` | `clips/d-home-territory-motion.mp4` | 2 | TerritoryRail desktop |
| `d-home-rail-hover` | `clips/d-home-rail-hover.mp4` | 3 | Editorial property rail hover |
| `d-props-scroll-grid` | `clips/d-props-scroll-grid.mp4` | 4 | Properties grid |
| `d-props-filter-focus` | `clips/d-props-filter-focus.mp4` | 5 | Residence filters |
| `d-neighbourhoods-scroll` | `clips/d-neighbourhoods-scroll.mp4` | 6 | Neighbourhoods dossiers |
| `d-detail-scroll` | `clips/d-detail-scroll.mp4` | 7 | Property detail scroll |
| `m-home-scroll` | `clips/m-home-scroll.mp4` | 8 (mobile home) | Phone pass on home |
| `m-territory-idle` | `clips/m-territory-idle.mp4` | 2 (mobile alt) | TerritoryRail phone |
| `m-props-scroll` | `clips/m-props-scroll.mp4` | 4 (mobile alt) | Properties phone |

### Stills (18) — primary pairings

| Still ID | COPY use |
| --- | --- |
| `d-home-hero` | Pill 1 still |
| `d-home-territory-rail` | Pill 2 still |
| `d-home-editorial-rail` | Pill 3 still |
| `d-props-grid` / `m-props-grid` | Pill 4 |
| `d-props-filters` | Pill 5 |
| `d-neighbourhoods-grid` / `m-neighbourhoods` | Pill 6 |
| `d-detail-hero` | Pill 7 |
| `d-home-journal` / `d-home-process` / `d-props-market` / `d-about-offices` / `d-contact-hero` / `m-contact` | Pill 8 rotate |
| `m-home-hero` / `m-home-territory` | Mobile alts |
| `d-props-hero` | Optional props open (no dedicated pill) |

**X rule:** 1 video **or** 1–2 stills. Prefer video when the slot has a clip. End with **1–2** discovery tags: `#Framer` + `#FramerTemplate` (WIP) or `#FramerMarketplace` (when listing/live component). Soft `@framer` optional once — never a hashtag wall. **No template/preview URL** in copy until launch (avoid early copies).

**Community (optional, offset):** 2–4 stills per pill — see COPY Community blocks. Same light tags; **no live peek link** while WIP. Not in `week-current` (X lane only).

---

## Calendar (warmup ~1 week from Thu 2026-07-30)

Aligned with kern-x day types. Motion/stills + WIP craft only — never “shipping / remix / buy”, never preview URL.

| Date | Key | Type | Pill | Primary media | Hook / copy angle |
| --- | --- | --- | --- | --- | --- |
| 2026-07-30 | thu | take | 1 | `d-home-scroll-intro.mp4` | Home open — paper field, quiet type |
| 2026-07-31 | fri | before_after | 2 | `d-home-territory-motion.mp4` | Territories as stage, not pin list |
| 2026-08-01 | sat | ecosystem | 8m | `m-home-scroll.mp4` | Phone pass — same house, different frame |
| 2026-08-02 | sun | recap | 3 | `d-home-rail-hover.mp4` | Portfolio as filmstrip (no URL) |
| 2026-08-03 | mon | clip | 4 | `d-props-scroll-grid.mp4` | Portfolio page / CMS cards |
| 2026-08-04 | tue | insight | 5 | `d-props-filter-focus.mp4` | Filters ↔ CMS (thread_allowed) |
| 2026-08-05 | wed | spotlight | 6 | `d-neighbourhoods-scroll.mp4` | Neighbourhoods as dossiers |
| 2026-08-06 | thu | take | 7 | `d-detail-scroll.mp4` | One residence, full scroll |
| 2026-08-07 | fri | before_after | 8 | `d-home-journal.png` + `d-home-process.png` | Journal / process stills (no launch) |

**Spare / alts** (if a clip fails or you want a second pass later): `m-territory-idle`, `m-props-scroll`, contact/about stills, optional WIP thread in COPY.

**Not launch day.** When the template actually ships, set `today.type` to `launch` after `build_week.py` (see `docs/strategy.md`) — do not use these WIP pills for that.

---

## How execution works

1. **Manual (recommended for WIP):** open queue → attach media from Framer path → paste English `copy` → post → `--mark-posted`.
2. **With cron post agent:** after `apply_arbour_warmup.py`, `week-current.json` → `today` includes `component: "Arbour"`, `media`, `copy`. Prefer `today.copy` + attach `today.media` (see `runtime/post.RUN.md` media step).
3. **Sunday:** `build_week.py` rebuilds from Marketplace listings → **re-run** `apply_arbour_warmup.py` so remaining Arbour dates overwrite Mon–Fri (etc.) for that week.
4. **Voice:** X-facing text stays English from COPY. `voice/voice-compact.txt` still governs replies; do not rewrite Arbour originals into reply slang.
5. **Cadence (hard):** one Arbour original per scheduled day. Missed day → catch up **alone** or ≥4–6h from today’s post. Do not dump catch-up + today’s Arbour + a Marketplace component in one burst (learned 2026-08-03). Marketplace extras live in `week-current.extras` — ship another day or late offset.

---

## Status

Warmup window: **2026-07-30 → 2026-08-07**. Queue statuses: `pending` → `posted` | `skipped`.
