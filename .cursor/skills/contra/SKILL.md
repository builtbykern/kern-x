---
name: contra
description: Operate BuiltByKern Contra storefront (human): product fields, Component URL After purchase (not remix), still-first thumbs, tags, checkout text, feed timing. Use when Noel asks to list, fix, or paste a Contra product, After purchase, or Contra feed post. Not for cron. Framer Buy stays on LemonSqueezy — Contra is parallel.
disable-model-invocation: true
---

# Contra — parallel storefront

Profile: [contra.com/kern_mjgpb61c](https://contra.com/kern_mjgpb61c)

Framer **Buy** stays on LemonSqueezy. Contra is a second storefront. Price must match the Framer listing (`LISTING.md` / launch kit). Digital product sales on Contra **do** count toward Amount earned badges ($1k / $5k / …).

Paste catalog: `docs/contra/products-top10.md` (Arbour template at top, then components). Launch sequence paste: `docs/arbour-launch.md` + `state/positioning.json` → `contra.next`.

Agent drafts paste. Noel OKs and publishes. Do not post the Contra feed from the browser.

Arbour listing is **live** ($59, stills on the product page). Remaining Contra beat = **feed post** after Community, not a second listing.

## This week's feed

Read `state/positioning.json` → `contra.next` before inventing a feed post. After Community, not the same hour as X.

`VERIFY` After purchase URLs still open: LetterRollMenu, Corner Scroller, Copy Field, Filling Point, CircleCards, Wave Dot Link. Fix in Assets → Copy URL when Noel is in Framer — do not guess.

## Delivery (components)

After purchase must be the **Component URL** (`framer.com/m/...`), not a remix.

| Type | Use |
|------|-----|
| **Component URL** | Assets → Copy URL → paste into any project. **Canonical for components.** |
| Live preview | `framer.link` / `*.framer.app` — Description only |
| Remix (`?duplicate=…`) | Templates / optional demo project — **not** default for components |
| Project URL (`framer.com/projects/…`) | Editor only — **buyers cannot open**. Never put in After purchase. |

If Marketplace listing **Component URL** is empty/disabled, copy from Framer Assets (right-click component → Copy URL).

## Visuals (grid thumb bug)

Contra product **cards use `featuredMedia[0]`**. If the first asset is an MP4 with no poster, the grid looks empty/white.

**Always:** still **first**, MP4 second. Thumb `Kern_*_thumbnail.png` (4:3). Max 6 media.

Quiet thumb fix is allowed **before** a launch tweet. Do **not** post to the Contra **feed** until after X + Community (see hub launch sequence).

## Shared listing fields

**Name:** `{Component} - Framer Component` (templates: editorial name, not “Framer Component”).

**Tags:** `Framer` · `Framer Designer` · `Framer Developer` · `UI Designer` · `Component libraries`

**Checkout page text** (paste as-is):

```
Refund Policy
Digital component purchases are non-refundable. Preview the live demo before buying.

License
Single-use: one Framer project / one website (personal, commercial, or client).
No resale, redistribution, or claiming as your own — even if modified.

Support
Message BuiltByKern on Contra, or reply on the Framer Community listing.
```

## Feed vs listing

| Surface | When |
|---------|------|
| Product page visuals | Anytime; still-first before social launch |
| Contra **feed** post | After X original + Community; never same hour as X |
| Description | World + named move + live preview URL. Not a feature wall. |

WIP templates: no live URL in social; listing can exist with stills. Confirm with Noel before calling a product live.

## Workflow

1. Open `docs/contra/products-top10.md` (or the launch kit for a template).
2. Verify Component URL in Framer Assets if the doc says `VERIFY`.
3. Upload still first, then demo MP4.
4. Fill tags + checkout text + After purchase.
5. Price = Framer listing. Do not restyle ($59 stays $59).
6. Feed post last in the launch sequence.

## Do not

- Put Project URLs in After purchase
- Lead the gallery with video
- Dump Contra links on X originals (X self-reply = `framer.link`)
- Treat Contra as the primary Buy button on Framer
