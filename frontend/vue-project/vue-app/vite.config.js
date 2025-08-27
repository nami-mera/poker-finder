import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  base: '/poker-finder/',  // 👈 填你的 GitHub 仓库名
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://13.231.184.250:5000', // 后端接口地址，根据你的实际端口改
        changeOrigin: true,
      },
    },
  },
})