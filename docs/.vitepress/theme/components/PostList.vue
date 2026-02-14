<script setup lang="ts">
import { computed } from 'vue'
import PostCard from './PostCard.vue'

interface Post {
  title: string
  url: string
  createdTime: {
    seconds: number
    nanoseconds: number
  } | string | Date
  abstract?: string
  thumbnil?: string
  category?: string
}

const props = defineProps<{
  posts: Post[]
}>()

const groupedPosts = computed(() => {
  const groups: Record<string, Post[]> = {}
  
  props.posts.forEach(post => {
    const category = post.category || '綜合'
    if (!groups[category]) {
      groups[category] = []
    }
    groups[category].push(post)
  })
  
  return groups
})

// Sort categories if needed, or just iterate keys
const sortedCategories = computed(() => {
  return Object.keys(groupedPosts.value).sort((a, b) => {
    if (a === '綜合') return 1 // '綜合' at the end
    if (b === '綜合') return -1
    return a.localeCompare(b)
  })
})
</script>

<template>
  <div class="post-list-container">
    <div v-for="category in sortedCategories" :key="category" class="category-section">
      <h2 class="category-title">{{ category }}</h2>
      <div class="post-grid">
        <PostCard v-for="post in groupedPosts[category]" :key="post.url" :post="post" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.post-list-container {
  display: flex;
  flex-direction: column;
  gap: 3rem;
  padding: 2rem 0;
}

.category-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--vp-c-brand-1, #646cff);
  display: inline-block;
  color: var(--vp-c-text-1);
}

.post-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

@media (max-width: 639px) {
  .post-grid {
    grid-template-columns: 1fr;
  }
}
</style>