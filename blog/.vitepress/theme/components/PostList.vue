<script setup lang="ts">
import { computed, ref } from 'vue'
import PostBlock from './PostBlock.vue'
import PostCard from './PostCard.vue'

interface Post {
  title: string
  url: string
  createdTime: {
    seconds: number
    nanoseconds: number
  } | string | Date
  categoryRootPath: string
  description?: string
  thumbnail?: string
  category?: string
}

interface Group {
  name: string
  categoryRootPath: string
  posts: Post[]
}

const props = defineProps<{
  posts: Post[]
}>()

// State
const searchQuery = ref('')
const sortBy = ref<'time' | 'category'>('time')
const sortOrder = ref<'asc' | 'desc'>('desc')
const viewMode = ref<'card' | 'block'>('block')

// Helper: Normalize date for comparison
function getTime(post: Post) {
  const time = post.createdTime
  if (typeof time === 'object' && time !== null && 'seconds' in time) {
    return time.seconds * 1000
  }
  return new Date(time as any).getTime()
}

// Filtered and Sorted Data
const processedPosts = computed(() => {
  // 1. Filter
  const filtered = props.posts.filter((post) => {
    const q = searchQuery.value.toLowerCase().trim()
    if (!q)
      return true

    const titleMatch = post.title?.toLowerCase().includes(q)
    if (sortBy.value === 'time') {
      return titleMatch
    }
    else {
      const categoryMatch = (post.category || '綜合').toLowerCase().includes(q)
      return titleMatch || categoryMatch
    }
  })

  // 2. Sort
  return filtered.sort((a, b) => {
    let result = 0
    if (sortBy.value === 'time') {
      result = getTime(a) - getTime(b)
    }
    else {
      const catA = a.category || '綜合'
      const catB = b.category || '綜合'
      result = catA.localeCompare(catB)
      if (result === 0) {
        result = getTime(b) - getTime(a)
        return result
      }
    }
    return sortOrder.value === 'asc' ? result : -result
  })
})

// Grouped data if in category mode
const groupedData = computed(() => {
  if (sortBy.value !== 'category')
    return null

  const groups: Map<string, Group> = new Map()

  processedPosts.value.forEach((post) => {
    const category = post.category || '綜合'
    if (!groups.has(category)) {
      groups.set(category, {
        name: category,
        categoryRootPath: post.categoryRootPath,
        posts: [],
      })
    }
    groups.get(category)!.posts.push(post)
  })

  return Array.from(groups.entries()).map(([, group]) => ({ name: group.name, categoryRootPath: group.categoryRootPath, posts: group.posts }))
})

const transitionKey = computed(() => {
  return `${sortBy.value}-${sortOrder.value}-${viewMode.value}`
})

function toggleSortMode() {
  sortBy.value = sortBy.value === 'time' ? 'category' : 'time'
}

function toggleSortOrder() {
  sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
}

function toggleViewMode() {
  viewMode.value = viewMode.value === 'card' ? 'block' : 'card'
}
</script>

<template>
  <div class="post-list-container">
    <!-- Controls Section -->
    <div v-if="processedPosts.length > 0" class="controls-wrapper">
      <div class="search-bar">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <input
          v-model="searchQuery" type="text" :placeholder="sortBy === 'time' ? '搜尋文章標題...' : '搜尋標題或類型...'"
          class="search-input"
        >
      </div>

      <div class="actions">
        <button class="control-btn" :title="viewMode === 'card' ? '切換至列表模式' : '切換至卡片模式'" @click="toggleViewMode">
          <svg
            v-if="viewMode === 'card'" class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
            stroke-width="2"
          >
            <line x1="8" y1="6" x2="21" y2="6" />
            <line x1="8" y1="12" x2="21" y2="12" />
            <line x1="8" y1="18" x2="21" y2="18" />
            <line x1="3" y1="6" x2="3.01" y2="6" />
            <line x1="3" y1="12" x2="3.01" y2="12" />
            <line x1="3" y1="18" x2="3.01" y2="18" />
          </svg>
          <svg v-else class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7" />
            <rect x="14" y="3" width="7" height="7" />
            <rect x="14" y="14" width="7" height="7" />
            <rect x="3" y="14" width="7" height="7" />
          </svg>
        </button>

        <button class="control-btn" title="切換排序方式" @click="toggleSortMode">
          <span class="btn-text">{{ sortBy === 'time' ? '時間排序' : '類型排序' }}</span>
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="16 3 21 3 21 8" />
            <line x1="4" y1="20" x2="21" y2="3" />
            <polyline points="21 16 21 21 16 21" />
            <line x1="15" y1="15" x2="21" y2="21" />
            <line x1="4" y1="4" x2="9" y2="9" />
          </svg>
        </button>

        <button class="control-btn" title="切換升降冪" @click="toggleSortOrder">
          <span class="btn-text">{{ sortOrder === 'asc' ? '升冪' : '降冪' }}</span>
          <svg
            v-if="sortOrder === 'asc'" class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
            stroke-width="2"
          >
            <line x1="12" y1="19" x2="12" y2="5" />
            <polyline points="5 12 12 5 19 12" />
          </svg>
          <svg v-else class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19" />
            <polyline points="19 12 12 19 5 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Content Section -->
    <Transition mode="out-in" name="fade">
      <div :key="transitionKey" class="content-view" :class="viewMode">
        <!-- Grouped View -->
        <template v-if="sortBy === 'category'">
          <div v-for="group in groupedData" :key="group.name" class="category-block">
            <h2 class="category-header">
              <span class="category-indicator" />
              <a :href="group.categoryRootPath" target="_top" style="text-underline-offset: 0.3rem;">{{ group.name }}</a>
            </h2>
            <div class="post-grid" :class="viewMode">
              <component
                :is="viewMode === 'card' ? PostCard : PostBlock" v-for="post in group.posts" :key="post.url"
                :post="post" :show-category="false"
              />
            </div>
          </div>
        </template>

        <!-- Flat View -->
        <template v-else>
          <div class="post-grid" :class="viewMode">
            <component
              :is="viewMode === 'card' ? PostCard : PostBlock" v-for="post in processedPosts" :key="post.url"
              :post="post" :show-category="true"
            />
          </div>
        </template>
      </div>
    </Transition>

    <!-- Empty State -->
    <div v-if="processedPosts.length === 0" class="empty-state">
      <div class="empty-visual">
        📭
      </div>
      <p class="pt-4">
        沒有任何文章，努力產生中！<br>((└(:3」┌)┘))
      </p>
    </div>
  </div>
</template>

<style scoped>
.post-list-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

/* Controls - Liquid Glass */
.controls-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 3rem;
  align-items: center;
  justify-content: space-between;
}

.search-bar {
  flex: 1;
  min-width: 280px;
  position: relative;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 0 1rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.dark .search-bar {
  background: rgba(0, 0, 0, 0.2);
  border-color: rgba(255, 255, 255, 0.05);
}

.search-bar:focus-within {
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 0 0 2px var(--vp-c-brand-soft);
  transform: translateY(-1px);
}

.search-icon {
  width: 18px;
  height: 18px;
  color: var(--vp-c-text-3);
  margin-right: 0.75rem;
}

.search-input {
  width: 100%;
  height: 48px;
  background: transparent;
  border: none;
  outline: none;
  color: var(--vp-c-text-1);
  font-size: 1rem;
}

.actions {
  display: flex;
  gap: 0.75rem;
}

.control-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0 1.25rem;
  height: 48px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: var(--vp-c-text-1);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dark .control-btn {
  background: rgba(0, 0, 0, 0.2);
}

.control-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

.control-btn:active {
  transform: translateY(0);
}

.btn-icon {
  width: 20px;
  height: 20px;
  opacity: 0.8;
}

/* Content Layout */
.post-grid {
  display: grid;
  gap: 2rem;
  /* Remove internal transition to avoid conflict with parent transition */
}

.post-grid.card {
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
}

.post-grid.block {
  grid-template-columns: 1fr;
  gap: 1rem;
}

.category-block {
  margin-bottom: 4rem;
}

.category-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.75rem;
  font-weight: 800;
  margin-bottom: 2rem;
  color: var(--vp-c-text-1);
  position: relative;
}

.category-indicator {
  width: 8px;
  height: 32px;
  background: var(--vp-c-brand-1);
  border-radius: 4px;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 5rem 0;
  color: var(--vp-c-text-2);
}

.empty-visual {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

/* Animations - Fade Out-In */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 640px) {
  .controls-wrapper {
    flex-direction: column;
    align-items: stretch;
  }

  .actions {
    justify-content: center;
  }

  .control-btn {
    flex: 1;
    padding: 0 1rem;
  }

  .btn-text {
    display: none;
  }

  .category-header {
    font-size: 1.5rem;
  }
}
</style>
