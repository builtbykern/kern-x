---
name: framer-community
description: Draft and queue Framer Community posts for @builtbykern (human). Punch copy, video-first Hype, ship stories, Creators habits, unfollow playbook, catalog/queue. Use when Noel asks for Community copy, Hype, Creators, Arbour Community warmup, or unfollow. Not for cron. Not for X originals (use x-originals).
disable-model-invocation: true
---

# Framer Community — human lane

Site: [framer.com/community](https://www.framer.com/community/). **Not** Circle (`framer.community` is archive). Not loaded by cron.

Agent drafts paste. Noel OKs and publishes. Do not drive Community in the browser.

## Cadence

- **1 post every 2–3 days**, offset from the X original that day
- Reply to comments within **2–4 hours** of publish
- Sunday social roll call is a keeper (city + what you’re building, go first, no pitch)

## Source of truth

| File | Role |
|------|------|
| `state/positioning.json` → `community.next` | **Next post.** Wins over queues. |
| `state/arbour-community-queue.json` | Template/WIP/launch slots |
| `state/framer-community-catalog.json` | Components + metadata |
| `state/framer-community-queue.json` | Component publish status — **may be stale**; do not use the first `draft` row |
| `docs/framer-community/posts/*.md` | Copy + video notes |

Regenerate component posts after catalog edits (`POST_BODIES` in the script is the source — update that before sync or punch copy is overwritten):

```bash
python3 scripts/sync_framer_community_posts.py
```

The sync keeps `notes` on the queue JSON. It does **not** own Arbour launch copy (`state/arbour-community-queue.json` / `state/positioning.json`).

## Publish rules

| Do | Don't |
|----|-------|
| Post type **Component** + attach card | Paste `framer.com/community/marketplace/...` in body |
| `framer.link` preview URLs | Marketplace links in text (blocked) |
| Attach **video** 10–25s | Text-only (ineligible for Hype) |
| Point to profile: `BuiltByKern → Marketplace → [name]` | Duplicate X copy verbatim |
| Punch 2–4 lines, name the move | Feature dumps, bullet walls, sterile “Most X… This one…” |

WIP templates: stills/video only — no live preview URL until launch.

Lummi stills: Share your work, 2–4 stills, no Marketplace URL, title like `Lummi [set] stills for a Framer template in progress`. One world, not mixed stock. Creator: https://www.lummi.ai/creator/builtbykern

## What ranks (from live posts)

**Your shapes that work**

1. Ship story + named move (Corner ~31♥/9💬)
2. Sunday roll call (~25♥/5💬)
3. Contrast one-liner only when it stays sensory (Copy Field ~22♥/4💬)

**Avoid:** sterile punches (Morph / Contact Dock / Video Ring). Long feature dumps starve comments.

**Peer Hype:** video first; human > brochure; reply hooks (“drop yours”, “curious for feedback”); soft product — clip sells.

Creators rank cares about useful posts **and** ongoing participation (replies, not only drops). Prefer craft that can earn discussion over spotlighting every listing.

## Workflow

1. Read `state/positioning.json` → `community.next`. If pending, that is the post.
2. Else next `pending` (not `skipped`) in `state/arbour-community-queue.json`.
3. Else a ship-story component with strong video (prefer LetterRollMenu). Never Kinetic Line / Morph / Contact Dock / Video Ring just because they sit first in the component queue.
4. Open the copy doc / paste `body` from the board. Record or attach the named video.
5. Community → **Post** → **Template** or **Component** as the board says → paste body → attach media → publish
6. Set `status: published` on the board + matching queue row, `published_at: YYYY-MM-DD`
7. Stay for comments 2–4h (launch: 16:00–18:00 CEST)

Invite (X growth, not a Community body link dump):

```
https://www.framer.com/community/join?invite=y0MfazGKzAWL
```

## Unfollow (Creators hygiene)

Playbook: `docs/framer-community/UNFOLLOW-PLAYBOOK.md` + `state/framer-community-unfollow.json`.

- Target following down (~304 → ~100) without dropping useful signals
- Keep: Framer staff, Pro Expert, high interaction, anyone who sells on Marketplace, allowlist
- 10–20 unfollows/day, not a dump
- Ambiguous → skip (keep)

## Do not

- Blast Community in the same hour as the X launch tweet
- Cron-publish
- Recycle sterile component punches
- Mix two Lummi worlds in one post
