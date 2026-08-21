---
name: instagram-explore
description: Explore Instagram for BuiltByKern (human playbook only): audience, Reels vs carousels, cadence, shot lists, captions, CTAs to Framer Community or Contra. Use when Noel asks to plan Instagram, draft IG captions, or map stills/clips to Reels/carousels. Do not publish, do not automate, do not open Instagram unless Noel is posting by hand.
disable-model-invocation: true
---

# Instagram — explore playbook

**Status:** research + first-batch playbook. Noel publishes by hand. This skill does not post, schedule, or drive a browser to Instagram.

Job: let strangers discover the **studio world** (templates + components + Lummi stills). Authority first. Sales via link in bio — not caption URL spam.

## Audience

Primary: Framer designers and template buyers who already watch motion on X / Community.

Secondary: stills people (Lummi / editorial photography) who do not live on X.

Do not chase generic “entrepreneur” or Webflow-bait hashtag sets. One world per post (same rule as Lummi collections).

## Format jobs (2026)

| Format | Job | BuiltByKern use |
|--------|-----|-----------------|
| **Reels** | Discovery / non-followers | Demo clips already shot for X/Community. Hook in 3s. 15–45s if you have it; 7s launch clips are ok if the move is obvious. Captions on-screen (sound off). |
| **Carousels** | Saves / authority | One Lummi collection, 6–10 stills. Hook slide → world → named craft beat → CTA slide. Mixed stills + a short in-carousel clip when the motion *is* the product. |
| **Single still** | Rhythm only | Rare. Prefer carousel if you have a collection. |
| **Stories** | Trust, not reach | Skip until the feed playbook is running. |

For a launch-sized beat: Reel first (same clip as X), carousel within 24h (stills of the same world). Never the same hour as the X tweet.

## Cadence (explore, not growth-hack)

Start **3 posts / week**, not daily:

| Slot | Format | Source |
|------|--------|--------|
| 1 | Reel | Existing demo MP4 (component or template) |
| 2 | Carousel | One Lummi collection (`docs/lummi/collections.md`) |
| 3 | Reel **or** ship-story stills | Community video, recut; no Marketplace URL on screen |

Offset ≥4h from that day’s X original. Do not clone the X caption.

Pause and review after 12 posts: saves on carousels, follows from Reels, DMs. No like-count vanity.

## Shot list — Reel

1. **0–3s** — the named move already happening (rail, veil, pan, type). No logo card.
2. **Mid** — one more beat in the same world (no extra products).
3. **End** — hold on the still that could be the Contra thumb. No “link in bio” burn-in.
4. Export 9:16 if you recut; 1:1/16:9 demos can run letterboxed if the move stays readable.

Reuse X/Community files. Do not invent a parallel shoot until the first 12 posts exist.

## Shot list — Carousel (Lummi world)

Cover = collection cover still. 6–10 slides:

1. Hook: world name + one sensory line (`Quiet London facades. No stock HDR.`)
2–N. Stills in collection order. One photo per slide. No mix of Almada + London.
Last. Soft CTA: Framer Community or “stills for a template in progress” — not a price.

## Captions

English. Short. World first. Not X-reply lowercase, not a feature list.

**Reel**

```
[named move] in [world].

one studio — templates, components, stills.

#Framer
```

**Carousel**

```
[world one-liner from docs/lummi/collections.md]

stills for a Framer template in progress. not mixed stock.
```

CTA: **one** of (a) link in bio → Community profile / Contra, (b) “more of this world on Framer Community”, (c) Lummi creator https://www.lummi.ai/creator/builtbykern. Never stack Marketplace + Contra + Lummi URLs in one caption.

Hashtags: 1–3 max (`#Framer` plus one world or `#FramerTemplate` if true). No hashtag walls.

## Link in bio (when Noel sets it)

Single destination, rotate by phase:

- Warmup / explore: Framer Community profile
- Launch week: `framer.link` for the live template
- Always-on catalog: Contra profile **or** Community Marketplace tab — pick one, don’t split

## First batch (playbook, not files)

Named in `state/positioning.json` → `instagram.first_batch`. Do **not** generate a new asset folder. Reuse those paths. Noel publishes by hand, not the same hour as X or Community.

## Do not

- Auto-post, schedule, or scrape Instagram
- Duplicate X copy
- Mix Lummi worlds
- Put `framer.com/community/marketplace/…` on-screen or in caption
- Use this skill during cron
- Claim follower/sales targets; this lane is explore
