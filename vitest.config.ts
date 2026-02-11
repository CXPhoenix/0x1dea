import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'happy-dom',
    globals: true,
    include: ['**/*.spec.ts'],
    alias: {
      'vitepress': path.resolve(path.dirname(new URL(import.meta.url).pathname), './docs/.vitepress/tests/mocks/vitepress.ts')
    }
  }
})
