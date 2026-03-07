import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import Layout from './Layout.vue'
import PostCard from './components/PostCard.vue'
import PostBlock from './components/PostBlock.vue'
import PostList from './components/PostList.vue'
import NewPost from './components/NewPost.vue'
import './style.css'
import 'virtual:uno.css'

export default {
  extends: DefaultTheme,
  Layout: Layout,
  async enhanceApp({ app, router, siteData }) {
    app.component('PostCard', PostCard)
    app.component('PostBlock', PostBlock)
    app.component('PostList', PostList)
    app.component('NewPost', NewPost)

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
