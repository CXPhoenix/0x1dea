<script setup lang="ts">
import { computed } from 'vue'
import { data as posts } from '../../../shared/posts.data'
import PostBlock from './PostBlock.vue'
import { usePostSort } from '../composables/usePostSort'
import { usePostFilter } from '../composables/usePostFilter'

const props = withDefaults(defineProps<{
  count?: number
}>(), {
  count: 5
})

const filterFn = usePostFilter()
const sortFn = usePostSort()

const newestPosts = computed(() =>
  [...posts].filter(filterFn).sort(sortFn).slice(0, props.count)
)
</script>

<template>
  <div class="new-post-list">
    <PostBlock
      v-for="post in newestPosts"
      :key="post.url"
      :post="post"
    />
  </div>
</template>

<style scoped>
.new-post-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
</style>
