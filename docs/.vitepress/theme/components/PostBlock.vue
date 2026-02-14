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

const props = defineProps<{
  post: Post
}>()

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
  <a :href="post.url" class="post-block">
    <div class="block-content">
      <div class="info-main">
        <h3 class="title">{{ post.title }}</h3>
        <p v-if="post.abstract" class="abstract">{{ post.abstract }}</p>
      </div>
      <div class="meta">
        <span v-if="post.category" class="category-tag">{{ post.category }}</span>
        <span class="date">{{ formattedDate }}</span>
      </div>
    </div>
  </a>
</template>

<style scoped>
.post-block {
  display: block;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  border-radius: 12px;
  overflow: hidden;
  
  /* Liquid Glass Effect - Subtle */
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
}

.dark .post-block {
  background: rgba(30, 30, 30, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.03);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.post-block:hover {
  transform: translateX(4px);
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.dark .post-block:hover {
  background: rgba(40, 40, 40, 0.5);
  border-color: rgba(255, 255, 255, 0.1);
}

.block-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  gap: 1.5rem;
}

.info-main {
  flex: 1;
  min-width: 0;
}

.title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  line-height: 1.4;
  color: var(--vp-c-text-1, #333);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.abstract {
  margin: 0.25rem 0 0;
  font-size: 0.9rem;
  color: var(--vp-c-text-2, #666);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  opacity: 0.8;
}

.meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
}

.date {
  font-size: 0.85rem;
  color: var(--vp-c-text-3);
  font-variant-numeric: tabular-nums;
}

.category-tag {
  font-size: 0.75rem;
  padding: 0.15rem 0.6rem;
  border-radius: 99px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-weight: 500;
}

@media (max-width: 640px) {
  .block-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 1rem;
  }
  
  .meta {
    width: 100%;
    justify-content: space-between;
  }
  
  .title, .abstract {
    white-space: normal;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
  }
  
  .abstract {
    -webkit-line-clamp: 1;
    line-clamp: 1;
  }
}
</style>