import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import NewPost from './components/NewPost.vue'
import PostBlock from './components/PostBlock.vue'
import PostCard from './components/PostCard.vue'
import PostList from './components/PostList.vue'
import PreviewNotice from './components/PreviewNotice.vue'
import Layout from './Layout.vue'
import './style.css'
import 'virtual:uno.css'

export default {
  extends: DefaultTheme,
  Layout: Layout as Theme['Layout'],
  async enhanceApp({ app }) {
    app.component('PostCard', PostCard)
    app.component('PostBlock', PostBlock)
    app.component('PostList', PostList)
    app.component('NewPost', NewPost)
    app.component('PreviewNotice', PreviewNotice)

    if (!import.meta.env.SSR) {
      const Particles = (await import('@tsparticles/vue3')).default
      const { loadSlim } = await import('@tsparticles/slim')

      app.use(Particles, {
        init: async (engine) => {
          await loadSlim(engine)
        },
      })
    }
  },
} satisfies Theme
