import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import { fileURLToPath, URL } from "node:url"

export default defineConfig({
  plugins: [react()],
  root: "preview",
  resolve: {
    alias: {
      framer: fileURLToPath(new URL("./shared/framer-shim.ts", import.meta.url)),
      "@components": fileURLToPath(new URL("./components", import.meta.url)),
      "@shared": fileURLToPath(new URL("./shared", import.meta.url)),
    },
  },
  server: {
    port: 5173,
  },
})
