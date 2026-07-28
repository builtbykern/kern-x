# Page Progress

**Category:** Interactions  
**Price:** Free  
**Byline:** Fixed reading progress for long pages

## Description

Page Progress is a fixed top or bottom bar that tracks document scroll. Drop it on blogs, case studies, and docs so readers see how far they are.

### Features
- Position: Top or Bottom
- Fill + track colors
- Height and z-index
- Canvas/editor shows ~35% placeholder so the bar is visible
- `pointer-events: none` — never blocks clicks
- Respects `prefers-reduced-motion`

### Not included (by design)
Chapter markers, circular progress, multi-section tracking.

## Setup
1. Paste `PageProgress.tsx` into Framer → Assets → Code
2. Place once on the page (fixed overlay)
3. Pick position and colors

## Acceptance
- Fill width = scroll progress of the document
- Does not intercept pointer events
- Single self-contained `.tsx`

## Thumbnail
Thin top bar growing over an article mock.
