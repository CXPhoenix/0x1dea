<script setup lang="ts">
import { computed } from 'vue'

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

const props = withDefaults(defineProps<{
  post: Post
  showCategory?: boolean
}>(), {
  showCategory: true
})

const formattedDate = computed(() => {
  let date: Date
  const rawTime = props.post.createdTime
  
  if (typeof rawTime === 'object' && rawTime !== null && 'seconds' in rawTime) {
    date = new Date(rawTime.seconds * 1000)
  } else {
    date = new Date(rawTime as string | number | Date)
  }
  
  return date.toLocaleDateString('zh-TW', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})
</script>

<template>
  <a :href="post.url" class="post-card">
    <div class="card-content">
      <div v-if="post.thumbnil" class="thumbnail-wrapper">
        <img :src="post.thumbnil" :alt="post.title" class="thumbnail" />
      </div>
      <div class="info">
        <h2 class="title">{{ post.title }}</h2>
        <div class="meta">
          <span v-if="showCategory && post.category" class="category-tag">{{ post.category }}</span>
          <span class="date">{{ formattedDate }}</span>
        </div>
        <p v-if="post.abstract" class="abstract">{{ post.abstract }}</p>
      </div>
    </div>
  </a>
</template>

<style scoped>
.post-card {
  display: block;
  text-decoration: none;
  color: inherit;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 16px;
  overflow: hidden;
  
  /* Liquid Glass Effect */
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}

.dark .post-card {
  background: rgba(30, 30, 30, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.05);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
}

.post-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  border-color: rgba(255, 255, 255, 0.4);
}

.card-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.thumbnail-wrapper {
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
}

.thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.post-card:hover .thumbnail {
  transform: scale(1.05);
}

.info {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  line-height: 1.4;
  color: var(--vp-c-text-1, #333);
}

.meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: var(--vp-c-text-2, #666);
}

.category-tag {
  font-size: 0.75rem;
  padding: 0.15rem 0.6rem;
  border-radius: 99px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-weight: 500;
}

.abstract {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--vp-c-text-2, #666);
  
  /* Line clamping for abstract */
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>