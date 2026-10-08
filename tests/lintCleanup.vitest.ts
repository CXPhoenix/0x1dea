import { mount } from '@vue/test-utils'
import { afterEach, describe, expect, it, vi } from 'vitest'
import PostList from '../blog/.vitepress/theme/components/PostList.vue'

const posts = [
  { title: 'Older safety', url: '/safety.html', createdTime: '2026-02-27T00:00:00+08:00', category: 'Security', categoryRootPath: '/security' },
  { title: 'Newer research', url: '/research.html', createdTime: new Date('2026-03-01T00:00:00+08:00'), category: 'Research', categoryRootPath: '/research' },
]

describe('post list preservation', () => {
  afterEach(() => vi.unstubAllEnvs())
  it('keeps time ordering, route links and the ascending toggle', async () => {
    const wrapper = mount(PostList, { props: { posts } })
    const routes = () => wrapper.findAll('a.post-block').map(link => link.attributes('href'))
    expect(routes()).toEqual(['/research.html', '/safety.html'])
    await wrapper.find('button[title="切換升降冪"]').trigger('click')
    expect(routes()).toEqual(['/safety.html', '/research.html'])
    wrapper.unmount()
  })

  it('keeps title search, category search and category route headings', async () => {
    const wrapper = mount(PostList, { props: { posts } })
    await wrapper.find('input').setValue('safety')
    expect(wrapper.findAll('a.post-block').map(link => link.attributes('href'))).toEqual(['/safety.html'])
    await wrapper.find('input').setValue('')
    await wrapper.find('button[title="切換排序方式"]').trigger('click')
    await wrapper.find('input').setValue('Security')
    expect(wrapper.findAll('a.post-block').map(link => link.attributes('href'))).toEqual(['/safety.html'])
    expect(wrapper.find('.category-header a').attributes('href')).toBe('/security')
    wrapper.unmount()
  })

  it('keeps card switching, titles and timestamp date rendering', async () => {
    vi.stubEnv('TZ', 'UTC')
    const fixture = [{ ...posts[0], createdTime: { seconds: 1772121600, nanoseconds: 0 } }]
    const wrapper = mount(PostList, { props: { posts: fixture } })
    expect(wrapper.find('.date').text()).toBe('2026年2月26日')
    await wrapper.find('button[title="切換至卡片模式"]').trigger('click')
    expect(wrapper.findAll('a.post-card')).toHaveLength(1)
    expect(wrapper.find('a.post-card').attributes('href')).toBe('/safety.html')
    expect(wrapper.find('h2.title').text()).toBe('Older safety')
    wrapper.unmount()
  })
})
