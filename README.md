# kern-x — Framer Code Components

Framer-ready code files live in [`code/`](code/):

| Code file | Category | Price target |
|---|---|---|
| [`code/ScrollStoryStage.tsx`](code/ScrollStoryStage.tsx) | Interactions | $19 |
| [`code/PathTypeKinetic.tsx`](code/PathTypeKinetic.tsx) | Typography | $12 |
| [`code/CMSSpotlightGallery.tsx`](code/CMSSpotlightGallery.tsx) | Carousels | Free / $9 |

Marketplace copy: [`listings/`](listings/).

## Add to a Framer project (Code files)

Each file is a self-contained Framer Code Component (`export default` + `addPropertyControls` + layout annotations).

1. Open your Framer project
2. **Assets → Code → + → New Component**
3. Name it to match the file (`ScrollStoryStage`, `PathTypeKinetic`, `CMSSpotlightGallery`)
4. Paste the full contents of the matching `.tsx` from `/code`
5. Save — the component appears in Assets and can be dropped on the canvas

Repeat for all three files.

Optional sync: use [Framer Code Link](https://www.npmjs.com/package/framer-code-link) or a Code Sync plugin to push the `/code` folder into the project instead of pasting.

## Local preview

```bash
npm install
npm run dev
```

Outside Framer, `shared/framer-shim.ts` stubs `addPropertyControls` / `ControlType`.

## Scripts

- `npm run dev` — preview playground
- `npm run typecheck` — TypeScript check
- `npm run build` — typecheck + Vite production build of the preview
