import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import tailwindcss from '@tailwindcss/vite'

// https://vitejs.dev/config/
export default defineConfig({
  base: process.env.DEV_ENV == 'true' ? '/' : './',
  build: {
    outDir: 'electron/build'
  },
  server: {
    port: 5174,
    strictPort: true
  },
  plugins: [svelte(), tailwindcss()],
})
