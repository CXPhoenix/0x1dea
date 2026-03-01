import { inject } from 'vue'
import type { InjectionKey } from 'vue'
import type { Post } from '../../../shared/posts.data.ts'

export type PostFilterFn = (post: Post) => boolean

/**
 * Injection key for providing a custom post filter predicate.
 *
 * Usage in a parent component or page:
 *   import { filterPostsKey } from './.vitepress/theme/composables/usePostFilter'
 *   provide(filterPostsKey, (post) => post.category === 'tech')
 */
export const filterPostsKey: InjectionKey<PostFilterFn> = Symbol('filterPosts')

const defaultFilter: PostFilterFn = () => true // accept all posts

export function usePostFilter(): PostFilterFn {
  return inject(filterPostsKey, defaultFilter)
}
