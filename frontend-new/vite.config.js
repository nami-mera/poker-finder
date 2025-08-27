import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: '/poker-finder/', // 方便后续部署到 GitHub Pages 或子目录
})
