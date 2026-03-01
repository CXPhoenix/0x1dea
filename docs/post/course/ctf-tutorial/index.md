---
sidebar: false
aside: false
footer: true
showParticle: true
next: false
isShowInPostsList: false
count: -1
---

<script setup>
    import { filterPostsKey } from '../../../.vitepress/theme/composables/usePostFilter'
    import { provide } from 'vue'

    provide(filterPostsKey, (post) => post.category === 'course/ctf-tutorial')
</script>

<NewPost />