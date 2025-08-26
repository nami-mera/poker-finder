import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000', // 后端接口地址，根据你的实际端口改
        changeOrigin: true,
      },
    },
  },
})