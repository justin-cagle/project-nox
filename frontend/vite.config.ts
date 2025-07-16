import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    open: true,
    proxy: {
      '/api': {
        target: 'http://192.168.0.149:8000', // or your Pi's IP if needed
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
