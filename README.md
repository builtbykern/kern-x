# kern-x — Framer Marketplace Components

Three Framer code components aimed at **Featured** placement and high views:

| Component | Category | Price target | File |
|---|---|---|---|
| **Scroll Story Stage** | Interactions | $19 | [`components/ScrollStoryStage.tsx`](components/ScrollStoryStage.tsx) |
| **PathType Kinetic** | Typography | $12 | [`components/PathTypeKinetic.tsx`](components/PathTypeKinetic.tsx) |
| **CMS Spotlight Gallery** | Carousels | Free / $9 | [`components/CMSSpotlightGallery.tsx`](components/CMSSpotlightGallery.tsx) |

Marketplace copy lives in [`listings/`](listings/).

## Local preview

```bash
npm install
npm run dev
```

Open the Vite preview, then scroll through all three demos.

## Publish into Framer

1. Create/open a Framer project
2. Assets → Code → New Component
3. Paste the contents of each `.tsx` file (Framer provides `framer` + `framer-motion`)
4. Build a live preview page with **one** component instance (per listing best practices)
5. Publish via Community → Post → Component using the matching listing markdown

Outside Framer, `shared/framer-shim.ts` stubs `addPropertyControls` / `ControlType` for local typecheck and preview.

## Scripts

- `npm run dev` — preview playground
- `npm run typecheck` — TypeScript check
- `npm run build` — typecheck + Vite production build of the preview
