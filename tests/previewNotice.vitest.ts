import { mount } from '@vue/test-utils'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { createSSRApp, h } from 'vue'
import { renderToString } from 'vue/server-renderer'
import PreviewNotice from '../blog/.vitepress/theme/components/PreviewNotice.vue'

const homepageCopy = { title: '六篇 staging 試稿預覽', text: '這六篇供 staging 預覽與審稿，尚未發佈到正式站。' }

describe('build-time preview notice with author props', () => {
  beforeEach(() => {
    vi.stubEnv('VITE_SITE_NOTICE_ENABLED', undefined)
    vi.stubEnv('CF_PAGES_BRANCH', undefined)
  })
  afterEach(() => vi.unstubAllEnvs())

  it('shows a named note with explicitly enabled author text', () => {
    vi.stubEnv('VITE_SITE_NOTICE_ENABLED', 'true')
    const wrapper = mount(PreviewNotice, { props: { title: '預覽標題', text: '預覽內容' } })
    expect(wrapper.find('[role="note"]').exists()).toBe(true)
    expect(wrapper.attributes('aria-label')).toBe('預覽標題')
    expect(wrapper.find('h2').text()).toBe('預覽標題')
    expect(wrapper.find('p').text()).toBe('預覽內容')
    wrapper.unmount()
  })

  it('uses staging fallback with the copy supplied by the homepage', () => {
    vi.stubEnv('CF_PAGES_BRANCH', 'staging')
    const wrapper = mount(PreviewNotice, { props: homepageCopy })
    expect(wrapper.find('[role="note"]').exists()).toBe(true)
    expect(wrapper.find('h2').text()).toBe(homepageCopy.title)
    expect(wrapper.find('p').text()).toBe(homepageCopy.text)
    wrapper.unmount()
  })

  it('trims whitespace and preserves embedded text newlines in a message-only note', () => {
    vi.stubEnv('VITE_SITE_NOTICE_ENABLED', 'true')
    const wrapper = mount(PreviewNotice, { props: { title: '   ', text: '  第一行\n第二行  ' } })
    expect(wrapper.find('h2').exists()).toBe(false)
    expect(wrapper.find('p').element.textContent).toBe('第一行\n第二行')
    expect(wrapper.attributes('aria-label')).toBe('預覽說明')
    wrapper.unmount()
  })

  it('omits an empty paragraph and preserves title newlines', () => {
    vi.stubEnv('VITE_SITE_NOTICE_ENABLED', 'true')
    const wrapper = mount(PreviewNotice, { props: { title: '  第一行\n第二行  ', text: '' } })
    expect(wrapper.find('p').exists()).toBe(false)
    expect(wrapper.find('h2').element.textContent).toBe('第一行\n第二行')
    wrapper.unmount()
  })

  it('renders no note when both fields are blank', () => {
    vi.stubEnv('VITE_SITE_NOTICE_ENABLED', 'true')
    const wrapper = mount(PreviewNotice, { props: { title: '', text: ' \n ' } })
    expect(wrapper.find('[role="note"]').exists()).toBe(false)
    wrapper.unmount()
  })

  it.each([
    [undefined, undefined, false],
    [undefined, 'main', false],
    [undefined, 'feature', false],
    [undefined, 'Staging', false],
    ['false', 'staging', false],
    ['', 'staging', false],
    [' ', 'staging', false],
    ['TRUE', 'staging', false],
    [' true ', 'staging', false],
    ['1', 'staging', false],
    ['true', 'main', true],
    ['true', undefined, true],
  ])('flag %s with branch %s renders %s', (flag, branch, visible) => {
    vi.stubEnv('VITE_SITE_NOTICE_ENABLED', flag)
    vi.stubEnv('CF_PAGES_BRANCH', branch)
    const wrapper = mount(PreviewNotice, { props: homepageCopy })
    expect(wrapper.find('[role="note"]').exists()).toBe(visible)
    wrapper.unmount()
  })

  it('renders hostile author strings literally without executable elements', () => {
    vi.stubEnv('VITE_SITE_NOTICE_ENABLED', 'true')
    const title = '<img src=x onerror="window.__noticeExecuted=1">'
    const text = '<script>window.__noticeExecuted=1</script>\n<strong>純文字</strong>'
    const wrapper = mount(PreviewNotice, { props: { title, text } })
    expect(wrapper.find('h2').element.textContent).toBe(title)
    expect(wrapper.find('p').element.textContent).toBe(text)
    expect(wrapper.findAll('img, script, strong')).toHaveLength(0)
    expect(wrapper.attributes('aria-label')).toBe(title)
    wrapper.unmount()
  })

  it.each([
    [{}, false, false],
    [{ title: '標題' }, true, false],
    [{ text: '內容' }, false, true],
  ])('treats omitted props as empty: %j', (props, heading, paragraph) => {
    vi.stubEnv('VITE_SITE_NOTICE_ENABLED', 'true')
    const wrapper = mount(PreviewNotice, { props })
    expect(wrapper.find('h2').exists()).toBe(heading)
    expect(wrapper.find('p').exists()).toBe(paragraph)
    wrapper.unmount()
  })

  it('reactively updates author copy, field omission and the whole note visibility', async () => {
    vi.stubEnv('VITE_SITE_NOTICE_ENABLED', 'true')
    const wrapper = mount(PreviewNotice, { props: homepageCopy })
    await wrapper.setProps({ title: '更新', text: '新文案' })
    expect(wrapper.find('h2').text()).toBe('更新')
    expect(wrapper.find('p').text()).toBe('新文案')
    await wrapper.setProps({ title: ' ', text: '內容' })
    expect(wrapper.find('h2').exists()).toBe(false)
    expect(wrapper.attributes('aria-label')).toBe('預覽說明')
    await wrapper.setProps({ title: '', text: '' })
    expect(wrapper.find('[role="note"]').exists()).toBe(false)
    await wrapper.setProps({ title: '再顯示' })
    expect(wrapper.find('h2').text()).toBe('再顯示')
    wrapper.unmount()
  })
})

describe('preview notice server-rendered environment matrix', () => {
  afterEach(() => vi.unstubAllEnvs())
  it.each([
    ['true', 'staging', true],
    ['true', 'main', true],
    ['false', 'staging', false],
    ['false', 'main', false],
    [undefined, 'staging', true],
    [undefined, 'main', false],
    [undefined, undefined, false],
    ['', 'staging', false],
    ['TRUE', 'staging', false],
    [' true ', 'staging', false],
  ])('SSR flag %s and branch %s yields visible=%s', async (flag, branch, visible) => {
    vi.stubEnv('VITE_SITE_NOTICE_ENABLED', flag)
    vi.stubEnv('CF_PAGES_BRANCH', branch)
    const html = await renderToString(createSSRApp({ render: () => h(PreviewNotice, { title: '審閱', text: '<script>literal</script>' }) }))
    expect(html.includes('<aside')).toBe(visible)
    if (visible) {
      expect(html).toContain('&lt;script&gt;literal&lt;/script&gt;')
      expect(html).not.toContain('<script>')
    }
  })
})
