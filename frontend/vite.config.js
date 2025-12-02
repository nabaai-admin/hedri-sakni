import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()],
    server: {
        host: '0.0.0.0',
        port: 5173,
        allowedHosts: [
            'hedri-sakni.socialaipilot.com',
            '89.117.48.162',
            'localhost',
            '.socialaipilot.com'  // Allow all subdomains
        ],
        watch: {
            usePolling: true
        },
        proxy: {
            '/api': {
                target: 'http://backend:5000',
                changeOrigin: true
            }
        }
    }
})
