
import { vi } from 'vitest'
import { ref } from 'vue'

export function useData() {
  return {
    isDark: ref(false),
    page: ref({
      title: 'Mock Title',
      frontmatter: {}
    }),
    theme: ref({}),
    frontmatter: ref({})
  }
}
