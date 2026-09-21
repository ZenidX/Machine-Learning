import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// base relativa: la web funciona tant servida a l'arrel com a un subdirectori
// de GitHub Pages sense haver de tocar la configuracio.
export default defineConfig({
  plugins: [react()],
  base: './',
})
