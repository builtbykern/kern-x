---
name: builtbykern
description: Routes BuiltByKern studio positioning across X, Contra, Framer Community, and Instagram. Studio = Framer templates + code components + Lummi stills; the visual world is the brand. Authority first, sales follow. Use in human chats when drafting originals, launches, Community posts, Contra listings, Instagram playbooks, paste kits, or multi-channel positioning. Never use during KERN-Post or KERN-Reply cron, and never when the user message is prompts/cron-post.txt or prompts/cron-reply.txt.
---

# BuiltByKern — positioning hub

Human chats only. Cron stays on `runtime/*.RUN.md` + `voice/voice-compact.txt`.

## Paste contract

1. Agent reads `state/positioning.json`, loads the channel skill, drafts the full paste (copy + where + media path).
2. Stop and wait for Noel’s **OK**.
3. Noel pastes in the channel. Agent does **not** post, compose in the browser, or run `x_post_original.py` / Community / Contra / IG publish.
4. After Noel says it is live: mark `next.status` published, add URL, point `next` at the following beat.

Reminders: ping Noel when a pending window opens (this chat, or a daily Cursor agent if they ask). Never treat a reminder as permission to publish.

Replies to other people on X may still use `reply-cycle.RUN.md` only if Noel asks. Positioning posts are always this paste loop.

## This week's board (read first)

`state/positioning.json` is the operational source of truth: next beat per channel, paste copy, windows, what not to do.

If a queue (Community drafts, `week-current.json`) disagrees with this board, **the board wins**. Do not `build_week.py` during an active launch week — it overwrites overlay copy.

KERN-Post: `runtime/post.RUN.md` must `status: stale_week` when `week-current.json` is not today's ISO week. That is the pause. Do not rely on a human remembering to disable the automation.

After a beat ships: set that channel's `next.status` to `published`, add URL/date, then point `next` at the following beat.

Verify the board against the tree (does not post):

```bash
python3 scripts/positioning_status.py
```

## Thesis

**BuiltByKern is a studio**, not a single product. Repeat this in every channel:

- Framer **templates** (worlds: Arbour / paper+ink, etc.)
- Framer **code components** (Marketplace craft, named moves)
- **Lummi stills** (one collection = one world; never mix London with Almada)

Authority (craft, ship stories, pasteable takes) comes first. Sales (Marketplace, Contra) are a consequence — never the opening beat.

Handle: `@builtbykern`. English on every public channel unless the user explicitly asks otherwise.

## Load the channel skill

Read the matching file **before** drafting. Do not improvise a channel you have not loaded.

| Task | Skill |
|------|--------|
| X original, thread, launch, stay-on-thread, Arbour warmup overlay | `.cursor/skills/x-originals/SKILL.md` |
| Framer Community post, Hype, Creators, unfollow, queue | `.cursor/skills/framer-community/SKILL.md` |
| Contra product, After purchase, thumbs, feed post | `.cursor/skills/contra/SKILL.md` |
| Instagram explore, Reels/carousel playbook, captions, shot list | `.cursor/skills/instagram-explore/SKILL.md` |
| X reply cycle / cron | Do **not** use this hub. Use `runtime/reply-cycle.RUN.md` only. |

## Voice split

| Surface | Voice | Source |
|---------|--------|--------|
| X **replies** (cron) | 1 sentence, lowercase, react not lecture | `voice/voice-compact.txt` |
| X **originals** (human) | Punch + named move; pasteable lists; 1–2 discovery tags | `x-originals` skill + voice-compact originals section |
| Community | Punch 2–4 lines; ship story; video is the post | `framer-community` skill |
| Contra | Listing fields, still-first thumb, Component URL | `contra` skill |
| Instagram | World first (stills/clip); short caption; CTA to Community or link-in-bio | `instagram-explore` skill |

Do not paste X-reply voice onto Community, Contra, or Instagram.

## Channel jobs

| Channel | Job | Cadence (human) | Sell |
|---------|-----|-----------------|------|
| X originals | Authority + copy-link; video is the product | 1/day, human-written. Cron may ship only if `today.copy` is already set. | Listing URL = self-reply only |
| X replies | Mutual-reply loop (For You weight 20) | Cron, 14–20 cycles/day, cap in `state/daily-caps.json` | Almost never |
| Framer Community | Hype / Creators; ship stories | 1 post / 2–3 days, offset from X | Component card + `framer.link`; no Marketplace URL in body |
| Contra | Parallel storefront (LemonSqueezy stays on Framer Buy) | Listing live; feed after X+Community, never same hour | Price matches listing |
| Instagram | Explore / discovery of the studio world | Playbook only until Noel publishes by hand | Link in bio → Community or Contra; no dump of listing URLs |

## Launch sync (all channels)

Do **not** blast X + Community + Contra + IG in the same hour.

Default sequence (see `docs/arbour-launch.md` when it is a template launch):

1. Contra visuals quiet (still **first**, video second) — no feed post yet
2. **X** original (video, no URL) → self-reply with `framer.link` → stay 45–60 min
3. **Community** next day, 12:00–14:00 CEST window when possible
4. **Contra feed** after Community
5. **Instagram** last (explore): same clip/stills, different caption, ≥4h after X

WIP templates: video/stills only. Never post live preview / template URL until launch.

## Lummi worlds

One brief = one collection. Cover = first still. Source: `docs/lummi/collections.md`.

Community/Contra paste for WIP stills: Share your work, 2–4 stills, no Marketplace URL, title like `Lummi [set] stills for a Framer template in progress`.

## Hard rules

- English only on public output
- One X tab only (reuse `com.builtbykern.kern-reply` / `get_work_page`)
- Cron allowlists still win during KERN-Post / KERN-Reply — this hub must not load
- Do not duplicate `voice/voice-compact.txt` or RUN files; point to them
- Ask Noel before inventing a new product price, URL, or “live” claim
