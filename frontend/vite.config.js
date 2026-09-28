import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const backend = "http://localhost:8000"

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/documents": backend,
      "/search": backend,
      "/metrics": backend,
      "/export": backend,
    },
  },
});
