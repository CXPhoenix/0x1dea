import { readFileSync } from 'node:fs'
import { fileURLToPath, URL as NodeURL } from 'node:url'
import { mount } from '@vue/test-utils'
import { createMarkdownRenderer } from 'vitepress'
import { describe, expect, it } from 'vitest'
import { createSSRApp, h } from 'vue'
import { compileTemplate } from 'vue/compiler-sfc'
import { renderToString } from 'vue/server-renderer'
import ArticleSummary from '../blog/.vitepress/theme/components/ArticleSummary.vue'

const content = '<p>第一段 <strong>重點</strong>、<em>語氣</em>、<code>inline-code</code> 與 <a href="https://vitepress.dev/guide/using-vue">連結</a>。</p><ul><li>時間線索</li><li>模型估計</li><li>資料用途</li></ul><p>第二段</p>'

describe('ArticleSummary author content and semantic boundaries', () => {
  it.each(['note', 'cards', 'terminal'])('keeps the same accessible content with %s', (variant) => {
    const wrapper = mount(ArticleSummary, { props: { variant }, slots: { default: content } })
    expect(wrapper.attributes('role')).toBe('note')
    expect(wrapper.attributes('aria-label')).toBe('TL;DR')
    expect(wrapper.findAll('li').map(item => item.text())).toEqual(['時間線索', '模型估計', '資料用途'])
    expect(wrapper.find('strong').text()).toBe('重點')
    expect(wrapper.find('em').text()).toBe('語氣')
    expect(wrapper.find('code').text()).toBe('inline-code')
    expect(wrapper.find('a').attributes('href')).toBe('https://vitepress.dev/guide/using-vue')
    expect(wrapper.findAll('div > p').map(item => item.text())).toEqual(['第一段 重點、語氣、inline-code 與 連結。', '第二段'])
    expect(wrapper.find('h2').exists()).toBe(false)
    wrapper.unmount()
  })

  it.each([undefined, '', 'UNKNOWN', '<script>alert(1)</script>'])('uses the note appearance for invalid variant %s', (variant) => {
    const expected = mount(ArticleSummary)
    const wrapper = mount(ArticleSummary, { props: { variant } })
    expect(wrapper.classes()).toEqual(expected.classes())
    expect(wrapper.find('script').exists()).toBe(false)
    wrapper.unmount()
    expected.unmount()
  })

  it('renders author title as literal text and falls back for a blank title', async () => {
    const title = '<img src=x onerror="alert(1)">'
    const wrapper = mount(ArticleSummary, { props: { title } })
    expect(wrapper.find('p').element.textContent).toBe(title)
    expect(wrapper.find('img').exists()).toBe(false)
    expect(wrapper.attributes('aria-label')).toBe(title)
    await wrapper.setProps({ title: '  ' })
    expect(wrapper.attributes('aria-label')).toBe('TL;DR')
    wrapper.unmount()
  })

  it('presents a static terminal window title without interactive controls', () => {
    const wrapper = mount(ArticleSummary, { props: { variant: 'terminal' }, slots: { default: '<ul><li>一</li><li>二</li><li>三</li></ul>' } })
    expect(wrapper.find('header').text()).toBe('TL;DR')
    expect(wrapper.findAll('button, input, textarea, [tabindex]')).toHaveLength(0)
    expect(wrapper.text()).not.toContain('$')
    wrapper.unmount()
  })

  it('renders server content without client-only APIs', async () => {
    const app = createSSRApp({
      render: () => h(ArticleSummary, { variant: 'terminal', title: '摘要' }, {
        default: () => [h('p', '段落'), h('ul', [h('li', '時間線索'), h('li', '模型估計')])],
      }),
    })
    const html = await renderToString(app)
    expect(html).toContain('aria-label="摘要"')
    expect(html).toContain('<p>段落</p>')
    expect(html).toContain('<ul><li>時間線索</li><li>模型估計</li></ul>')
  })

  it('retains the pinned compiler error for an unclosed component tag', async () => {
    const md = await createMarkdownRenderer(fileURLToPath(new NodeURL('../blog/', import.meta.url)))
    const source = md.render('<ArticleSummary>\n\nsentinel after malformed tag\n')
    const result = compileTemplate({ source, filename: 'invalid-markdown.md', id: 'invalid' })
    expect(result.errors.some(error => String(error).includes('missing end tag'))).toBe(true)
  })

  it('uses the installed VitePress Markdown parser and preserves closing/container boundaries', async () => {
    const source = readFileSync(fileURLToPath(new NodeURL('./fixtures/article-summary.md', import.meta.url)), 'utf8')
    const md = await createMarkdownRenderer(fileURLToPath(new NodeURL('../blog/', import.meta.url)))
    const html = md.render(source)
    expect(html).toContain('<ArticleSummary variant="cards">')
    const tree = document.createElement('div')
    tree.innerHTML = html
    expect(tree.querySelector('pre code')?.textContent).toContain('$ belongs to code')
    expect(tree.querySelector('li ul li')?.textContent).toBe('巢狀清單保留自己的層級。')
    expect(tree.querySelector('.info li')?.textContent).toBe('容器內清單不是摘要卡片。')
    expect(html).toContain('<strong>重點</strong>')
    expect(html).toContain('<em>語氣</em>')
    expect(html).toContain('<code>inline-code</code>')
    expect(html).toContain('href="https://vitepress.dev/guide/using-vue"')
    expect(html).toMatch(/<\/ArticleSummary>\s*<p>這段後文必須在元件外面。<\/p>/)
    for (const type of ['info', 'warning', 'tip']) {
      expect(html).toContain(`class="${type} custom-block"`)
    }
    expect(html).toMatch(/<details\s+class="details custom-block">/)
  })
})
