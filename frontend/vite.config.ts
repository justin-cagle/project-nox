import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    open: true,
    proxy: {
      '/api': {
        target: 'http://host.docker.internal:8000', // or your Pi's IP if needed
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
