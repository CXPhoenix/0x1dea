---
sidebar: false
aside: false
footer: true
showParticle: true
---

<script setup lang="ts">
    import { data as posts } from './shared/posts.data.ts';
</script>

<PostList :posts="posts" />
