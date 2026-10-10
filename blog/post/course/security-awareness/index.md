---
title: "資安認知推廣備課系列"
isIndex: true
count: -1
category: "資安認知推廣備課系列"
---

<script setup>
    import { filterPostsKey } from '../../../.vitepress/theme/composables/usePostFilter'
    import { provide } from 'vue'
    import { useData } from 'vitepress'

    const { frontmatter } = useData()
    provide(filterPostsKey, (post) => post.category === (frontmatter.value.category || '綜合'))
</script>

# {{ frontmatter.title }}

從生活中的資料與使用情境，討論資安風險及判斷的依據。

<NewPost class="mt-8" />
