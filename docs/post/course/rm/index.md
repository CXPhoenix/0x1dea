---
title: '研究方法教學備課系列'
isIndex: true
count: -1
category: '研究方法教學'
---

<script setup>
    import { filterPostsKey } from '../../../.vitepress/theme/composables/usePostFilter'
    import { provide } from 'vue'
    import { useData } from 'vitepress'

    const { frontmatter } = useData()
    provide(filterPostsKey, (post) => post.category === (frontmatter.value.category || '綜合'))
</script>

# {{ frontmatter.title }}

<NewPost class="mt-8" />