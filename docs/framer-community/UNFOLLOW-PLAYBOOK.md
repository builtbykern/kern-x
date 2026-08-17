# Framer Community — Unfollow playbook

**Goal:** bajar following (~304 → hacia ~100 estilo Matt) sin cortar señales útiles.  
**Cuenta:** @builtbykern · **nueva** Community (`framer.com/community`) — Circle (`framer.community`) es archive read-only.  
**Estado:** `state/framer-community-unfollow.json`

## Keep (nunca unfollow)

1. **Framer team / staff** — bio con “@Framer”, Engineering/Product/Education at Framer, badge Team/Admin/Staff. Ejemplos ya vistos: `@meli` (Eng Lead), `@jatodaro` (Product Education). En duda → keep.
2. **Pro Expert / Expert** — keep por defecto (suelen vender + engagement).
3. **Alta interacción** — posts recientes con engagement fuerte (♥ / comentarios altos en Feed/Hype), o gente que responde a menudo en tus hilos. Umbral práctico: media ≥ ~20♥ en posts recientes **o** comentarios activos en tus threads.
4. **Vende en Marketplace** — tiene components/templates/plugins live (aunque posteé poco).
5. **Allowlist manual** — ver `keep` en el state JSON.

## Unfollow (candidato)

Cumple **todo** lo siguiente:

1. **No vende** — sin components ni templates en Marketplace (ni creator page con listings live).
2. **Inactivo o ruido** — **una** de estas:
   - **No posta** — “No Posts” / perfil vacío / solo follows
   - **Posta pero no vende** — posts de opinión / follow-for-follow / hello / WIP sin listing, **y** engagement bajo (típicamente &lt; ~5♥ y &lt; ~3 comments en posts recientes)
3. **No es keep** — no team, no Expert/Pro Expert, no alta interacción, no allowlist.

**No** unfollow solo por “posta poco” si vende o si pega Hype/comments fuertes.

## Ritmo

- **10–20 unfollows / día**, no dump de 100.
- Anotar cada handle + motivo en el state.
- Si el perfil es ambiguo → **skip** (keep).

## Flujo (manual / asistido)

1. Abrir tu perfil Community → **Following**.
2. Abrir cada perfil: posts recientes + bio/links Marketplace.
3. Si es unfollow → Unfollow + log en state.
4. No tocar Staff / Experts con hype / gente que te contesta.

## Notas

- Community requiere **login Framer** (sesión Circle). Playwright de kern-x es solo X.
- “Vende” = Marketplace listing live; WIP / solo portfolio ≠ vende.
- Alguien que **posta mucho** pero **no vende** → keep solo si tiene **alta interacción**; si no, unfollow (prioridad: feed limpio de creators).
