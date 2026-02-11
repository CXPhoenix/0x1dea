/// <reference types="vite/client" />
import { h } from 'vue'
import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import Layout from './Layout.vue'
import './style.css'
import 'virtual:uno.css'

export default {
  extends: DefaultTheme,
  Layout: Layout,
  async enhanceApp({ app, router, siteData }) {
    if (!import.meta.env.SSR) {
      const Particles = (await import('@tsparticles/vue3')).default
      const { loadSlim } = await import('@tsparticles/slim')
      
      app.use(Particles, {
        init: async (engine) => {
          await loadSlim(engine)
        },
      })
    }
  }
} satisfies Theme
