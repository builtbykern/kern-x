# Content calendar template — @builtbykern

Fill each **Sunday** before running `python3 scripts/accio_build_week.py`.  
Script auto-assigns components from listings; use overrides below when launching a specific SKU.

## Week: __________ (ISO e.g. 2026-W20)

| Day | Type | Component override | Link override | Notes |
|-----|------|-------------------|---------------|-------|
| Mon | clip | | | media: canvas clip |
| Tue | insight | | | thread ok |
| Wed | spotlight | | | listing link day |
| Thu | take | | | no link |
| Fri | before_after | | | media |
| Sat | ecosystem | | | no sell |
| Sun | recap | | | optional CTA |

## Launch override (if applicable)

| Field | Value |
|-------|--------|
| Launch component | |
| Listing URL | |
| Launch price | $ |
| Giveaway | follow + RT, N licenses |
| D0 post time | |

Set `today.type` to `launch` in `Accio/state/week-current.json` on launch day (manual edit after script run).

## Example week (2026-W20 — auto-generated)

| Day | Type | Component | Link |
|-----|------|-----------|------|
| Mon | clip | Kern_InertiaGrid | no |
| Tue | insight | — | no |
| Wed | spotlight | Kern_CustomCursor | from listing |
| Thu | take | — | no |
| Fri | before_after | FlowingMenu | no |
| Sat | ecosystem | — | no |
| Sun | recap | — | no |

See live state: `Accio/state/week-current.json`.
