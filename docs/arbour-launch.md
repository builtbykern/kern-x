# Arbour launch kit — paste-ready

Human only. Not for cron. Listing live: https://framer.link/748Mrjh · $59  
Price matches Contra + `LISTING.md`. Do not restyle as $79/$99 in social.

**Sequence:** Contra thumb fix (quiet) → **X today 15:00 CEST** → Community **Thu 12:00–14:00** → Contra feed **Thu night / Fri**.  
Do not blast all three socials in the same hour.

Clips are ~7s (VQV min is 10s — attach anyway; video is the product, not a ranking hack).

---

## 0 — Antes de X (2 min)

1. Contra product visuals: still **first**, MP4 second.  
   First image: `/Users/noel/Desktop/Framer/docs/projects/listings/Arbour_thumbnail.png`  
   Product: [contra.com/products/eLYR4a2z](https://contra.com/products/eLYR4a2z)  
   Do **not** post to Contra feed yet.
2. Pause the X reply daemon / don’t start a foreign reply cycle. **One tab.** Stay on your tweet 45–60 min.
3. Lane B today: do not mention Arbour in replies to other people.

After X ships:

```bash
python3 scripts/record_post.py --url 'https://x.com/…' --type launch --component Arbour --had-link false --had-video true --text "$(cat <<'EOF'
PASTE_TWEET
EOF
)"
```

(`had-link false` = URL only in the self-reply, not the original.)

---

## 1 — X · hoy 15:00 CEST (9:00 ET)

**Attach:** `/Users/noel/Desktop/Framer/docs/projects/listings/Arbour_demo_3s.mp4`  
(= `arbour/media/clips/d-home-scroll-intro.mp4`, ~7s, home open)

**Tweet** (no URL):

```
most estate templates are a property grid with a map pin. this one is paper and ink — TerritoryRail as a stage, neighbourhoods as dossiers.

arbour — editorial template for independent agencies.

@framer
#Framer #FramerMarketplace
```

**Self-reply** (conversion, not algo):

```
https://framer.link/748Mrjh
```

Stay on the thread. If nobody lands in 10 min, like/reply nothing extra — don’t quote-tweet yourself.

### Replies on your own thread (english, short)

Someone likes the look:

```
paper field took a while to sit behind the photos instead of fighting them
```

Someone asks remix / Framer:

```
duplicate, retint Paper / Ink / Olive. CMS is Properties, Neighbourhoods, Journal, Agents
```

Someone asks price / where:

```
https://framer.link/748Mrjh
```

Struggle / “congrats on the launch”:

```
the quiet after listing is the part nobody sketches
```

---

## 2 — Framer Community · jue 20 ago · 12:00–14:00 CEST

**Type:** Template (listing exists) — not Showcase WIP, not Component.  
**Video:** `/Users/noel/Desktop/Framer/docs/projects/arbour/media/clips/d-home-territory-motion.mp4`  
(TerritoryRail — different clip from X.)  
Optional extra stills (max 2): `listings/Arbour_thumbnail_territory.png` · `stills/m-home-hero.png`  
**Do not** paste `framer.com/community/marketplace/…`  
**Do not** paste the X tweet.

**Body:**

```
finally shipped Arbour — a residential Framer template. parchment, TerritoryRail, neighbourhoods as dossiers.

independent agency or residential studio — who is this actually for?

https://framer.link/748Mrjh

#Framer #FramerMarketplace
```

Sweep comments **16:00–18:00**. Same reply shapes as X, english.

WIP leftover posts `#2–#4` in `state/arbour-community-queue.json`: **skip**. Listing is live; “still wiring polish” contradicts the launch.

---

## 3 — Contra feed · jue noche o vie

**After** Community presence is done.  
**Link the product**, not only the Framer listing.  
**Tags:** Framer · Web Design · Framer Designer (existing product tags also have Lummi / UI / UX)

```
Arbour is live — editorial Framer template for independent estate agencies.

Paper and Ink. TerritoryRail as a stage. Neighbourhoods as dossiers, not a pin list.

https://contra.com/products/eLYR4a2z
```

Also on Marketplace is implied by the product description — don’t dump both URLs if the card already points at the product.

---

## 4 — Qué no hacer el resto de la semana

| Día | X | Community | Contra |
|-----|---|-----------|--------|
| Mié 19 | Este launch. Un original. Presencia 60 min. | Nada | Thumb only |
| Jue 20 | 1 original del calendario **sin** “Arbour live” otra vez. Craft. | Este post 12–14h | Feed noche, opcional |
| Vie–sáb | 1/día. Sáb sin sell. | Hueco 2–3 días | Quiet |
| Dom | Recap suave si toca | No Sunday roll call hasta ~30 ago | — |

Do not post leftover Arbour WIP stills. Do not stack a second X original the same morning.

---

## Paths (absolute)

| Use | File |
|-----|------|
| X video | `/Users/noel/Desktop/Framer/docs/projects/listings/Arbour_demo_3s.mp4` |
| Community video | `/Users/noel/Desktop/Framer/docs/projects/arbour/media/clips/d-home-territory-motion.mp4` |
| Contra cover still | `/Users/noel/Desktop/Framer/docs/projects/listings/Arbour_thumbnail.png` |
| Territory still | `/Users/noel/Desktop/Framer/docs/projects/listings/Arbour_thumbnail_territory.png` |
| Canonical buy | https://framer.link/748Mrjh |
| Contra product | https://contra.com/products/eLYR4a2z |
| Live preview (listing field, not X body) | https://arbour.framer.website |
