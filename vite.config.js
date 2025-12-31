import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [
    svelte({
      compilerOptions: {
        dev: process.env.NODE_ENV !== 'production'
      }
    })
  ],
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    sourcemap: true
  },
  server: {
    port: 5000
  },
  publicDir: 'public',
  define: {
    'import.meta.env.VITE_FILES_BASE_URL': JSON.stringify(process.env.VITE_FILES_BASE_URL || 'https://files.99boundaries.com'),
    'import.meta.env.VITE_OSM_BASE_URL': JSON.stringify(process.env.VITE_OSM_BASE_URL || 'https://www.openstreetmap.org')
  }
});
