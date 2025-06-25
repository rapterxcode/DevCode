// vite.config.ts
import { defineConfig } from "vite";
import checker from "vite-plugin-checker";

export default defineConfig({
plugins: [
  checker({ typescript: true }),
],
base: '/',
//root: ".",
build: {
  outDir: "dist",
},
});