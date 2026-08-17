# Arbour — Framer Community calendar (WIP)

Human-run. **Not** for cron. Offset from X daily originals (Community ≈ every **2–3 days**).

Live site (internal only — **do not post** while WIP).  
Media: `/Users/noel/Desktop/Framer/docs/projects/arbour/media/`  
Copy source: `COPY.md` Community blocks  
X parallel: [`docs/arbour-warmup.md`](../arbour-warmup.md) · `state/arbour-warmup-queue.json`

## Rules

| Do | Don't |
|----|-------|
| Post type that fits WIP (Showcase / Design / Update — **not** Component card unless listing exists) | Paste marketplace **or** live preview URLs |
| 2–4 **stills** per post (carousel) | Text-only |
| WIP language — process, not launch | “Shipping / remix / buy” |
| Motion/craft talk only | Soft peek / `arbour.framer.website` in body |
| Light tags: `#Framer` + `#FramerTemplate` (WIP) | Tag spam / marketplace URL paste |
| Reply to comments in 2–4h | Stack same day as X original |

## Calendar (staggered vs X)

X runs daily 30 jul → 7 ago. Community picks **4 posts** in the same window (every ~2–3 days), stills-first.

| # | Date | After X slot | Pill | Stills (2–4) | Community body |
|---|------|--------------|------|--------------|----------------|
| 1 | **Fri 31 jul** | After X TerritoryRail (fri) | 1+2 | `d-home-hero` · `d-home-territory-rail` · `m-home-hero` | Home open + TerritoryRail (pill 1+2 merge) |
| 2 | **Mon 3 ago** | After X filmstrip sun + props mon | 3+4 | `d-home-editorial-rail` · `d-props-grid` · `m-props-grid` | Editorial rail + properties grid |
| 3 | **Wed 5 ago** | Same day as X neighbourhoods (offset evening) | 5+6 | `d-props-filters` · `d-neighbourhoods-grid` · `m-neighbourhoods` | Filters + neighbourhoods dossiers |
| 4 | **Fri 7 ago** | After X detail thu + journal fri | 7+8 | `d-detail-hero` · `d-home-journal` · `d-home-process` · `d-contact-hero` | Detail + journal/process (close warmup) |

Optional spare (if a date slips): `d-about-offices` · `m-contact` with spare copy from COPY.

## Paste-ready bodies

### 1 — Fri 31 jul (home + territory)

**Stills:** `stills/d-home-hero.png` · `stills/d-home-territory-rail.png` · `stills/m-home-hero.png`

```
Arbour WIP — home open + TerritoryRail

Sketching the first viewport: parchment, ink, a mark that doesn’t compete with the photography.

Neighbourhoods as an editorial stage: image, coords, quiet index. Desktop + a phone still.

Not a finished template. Just the entrance and the map of place.

#Framer #FramerTemplate
```

### 2 — Mon 3 ago (rail + properties)

**Stills:** `stills/d-home-editorial-rail.png` · `stills/d-props-grid.png` · `stills/m-props-grid.png`

```
Arbour WIP — editorial rail → /properties

Home portfolio strip before the full portfolio page. Motion on hover only.

Owned PropertyCards on a filtered CMS list. Desktop grid + phone crop.
Still wiring polish. Structure first.

#Framer #FramerTemplate
```

### 3 — Wed 5 ago (filters + neighbourhoods)

**Stills:** `stills/d-props-filters.png` · `stills/d-neighbourhoods-grid.png` · `stills/m-neighbourhoods.png`

```
Arbour WIP — filters + /neighbourhoods

Form controls → page variables → collection list. Quiet UI, estate pacing.

Territory checkerboard + hero. Place before property. Still in progress.

#Framer #FramerTemplate
```

### 4 — Fri 7 ago (detail + journal)

**Stills:** `stills/d-detail-hero.png` · `stills/d-home-journal.png` · `stills/d-home-process.png` · optional `stills/d-contact-hero.png`

```
Arbour WIP — detail + journal on home

Cheyne Walk as the sample residence. Detail template still getting weight and rhythm.

Article cards + viewing process as a quiet index. Full /notes route still cooking.

#Framer #FramerTemplate
```

## Workflow

1. Pick next `status: pending` in [`state/arbour-community-queue.json`](../../state/arbour-community-queue.json)
2. Attach stills listed (no Component marketplace card until Arbour is listed)
3. Paste body → publish on Framer Community
4. Mark: set `status: published`, `published_at`, `post_url` in the queue JSON

## Sync with X

| X date | X focus | Community |
|--------|---------|-----------|
| Thu 30 | Home video | — (X only) |
| Fri 31 | Territory video | **Post 1** stills |
| Sat 1 | Mobile home | — |
| Sun 2 | Filmstrip | — |
| Mon 3 | Props grid | **Post 2** stills |
| Tue 4 | Filters | — |
| Wed 5 | Neighbourhoods | **Post 3** stills (evening) |
| Thu 6 | Detail | — |
| Fri 7 | Journal stills | **Post 4** stills |
