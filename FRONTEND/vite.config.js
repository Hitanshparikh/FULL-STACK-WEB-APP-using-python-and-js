import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
  },
  // Optional: Add this section if you want to explicitly define external dependencies
  // build: {
  //   rollupOptions: {
  //     external: ['react-icons/io5'] // Uncomment if you want to externalize this package
  //   }
  // }
});
