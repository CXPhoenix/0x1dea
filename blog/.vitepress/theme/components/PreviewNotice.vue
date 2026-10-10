<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ title?: string, text?: string }>()
const flag = import.meta.env.VITE_SITE_NOTICE_ENABLED
const enabled = flag === undefined ? import.meta.env.CF_PAGES_BRANCH === 'staging' : flag === 'true'
const title = computed(() => (props.title ?? '').trim())
const text = computed(() => (props.text ?? '').trim())
</script>

<template>
  <aside v-if="enabled && (title || text)" class="preview-notice mt-8 rounded bg-gray-100 p-4 dark:bg-gray-800" role="note" :aria-label="title || '預覽說明'">
    <h2 v-if="title">
      {{ title }}
    </h2>
    <p v-if="text">
      {{ text }}
    </p>
  </aside>
</template>

<style scoped>
.preview-notice {
  overflow-wrap: anywhere;
}

.preview-notice h2,
.preview-notice p {
  white-space: pre-line;
}
</style>
