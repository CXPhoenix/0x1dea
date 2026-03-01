import { inject } from 'vue'
import type { InjectionKey } from 'vue'
import type { Post } from '../../../shared/posts.data.ts'

export type PostSortFn = (a: Post, b: Post) => number

/**
 * Injection key for providing a custom post sort comparator.
 *
 * Usage in a parent component or page:
 *   import { sortPostsKey } from './.vitepress/theme/composables/usePostSort'
 *   provide(sortPostsKey, (a, b) => new Date(a.createdTime).getTime() - new Date(b.createdTime).getTime())
 */
export const sortPostsKey: InjectionKey<PostSortFn> = Symbol('sortPosts')

// createdTime is declared as Date but arrives as a string after JSON serialization
const defaultSort: PostSortFn = (a, b) =>
  new Date(b.createdTime).getTime() - new Date(a.createdTime).getTime() // newest first

export function usePostSort(): PostSortFn {
  return inject(sortPostsKey, defaultSort)
}
