import { createHash } from 'node:crypto'
import { readFileSync } from 'node:fs'
import { fileURLToPath, URL as NodeURL } from 'node:url'
import { createMarkdownRenderer } from 'vitepress'
import { describe, expect, it } from 'vitest'
import { articleCaptions } from '../blog/.vitepress/markdown/articleCaptions'
import baseline from './fixtures/article-caption-baseline.json'
import provenance from './fixtures/article-caption-provenance.json'

const root = fileURLToPath(new NodeURL('../blog/', import.meta.url))
const renderer = async () => createMarkdownRenderer(root, { config: articleCaptions })
const figure = (id: string, caption = '模擬總功率') => `::: figure ${id}\n![電鍋加熱與保溫的功率曲線](/chart.svg "${caption}")\n:::\n`
const plainTable = '| 設備 | 功率 |\n| --- | ---: |\n| 電鍋 | 600 W |\n'
const table = (id: string) => `::: table ${id} 設備功率比較\n${plainTable}:::\n`
const parse = (html: string) => new DOMParser().parseFromString(html, 'text/html')

describe('article captions through VitePress Markdown', () => {
  it('numbers opted-in figures and preserves independent alternative text while excluding memes', async () => {
    const md = await renderer()
    const doc = parse(md.render(`${figure('ems')}\n![貓說只是來吃宵夜](/meme.png)\n\n<img src="/banner.png" alt="橫幅">\n\n${figure('nilm', '設備用電估計')}`))

    expect(Array.from(doc.querySelectorAll('figcaption')).map(el => el.textContent)).toEqual(['圖 1：模擬總功率', '圖 2：設備用電估計'])
    expect(doc.querySelector('#fig-ems > img')?.getAttribute('alt')).toBe('電鍋加熱與保溫的功率曲線')
    expect(doc.querySelector('#fig-ems > img')?.getAttribute('src')).toBe('/chart.svg')
    expect(doc.querySelectorAll('figure')).toHaveLength(2)
    expect(doc.querySelector('img[src="/meme.png"]')?.closest('figure')).toBeNull()
    expect(doc.querySelector('img[src="/banner.png"]')?.closest('figure')).toBeNull()
  })

  it('numbers tables separately with native first-child captions and resets each document', async () => {
    const md = await renderer()
    const source = `${figure('ems')}\n${table('power')}\n${plainTable}\n${table('energy')}`
    const doc = parse(md.render(source))
    expect(Array.from(doc.querySelectorAll('caption')).map(el => el.textContent)).toEqual(['表 1：設備功率比較', '表 2：設備功率比較'])
    expect(doc.querySelector('#tbl-power')?.firstElementChild?.tagName).toBe('CAPTION')
    expect(doc.querySelectorAll('table')).toHaveLength(3)
    expect(doc.querySelectorAll('figcaption')).toHaveLength(1)
    const second = parse(md.render(`${table('power')}\n${figure('ems')}`))
    expect(second.querySelector('caption')?.textContent).toBe('表 1：設備功率比較')
    expect(second.querySelector('figcaption')?.textContent).toBe('圖 1：模擬總功率')
  })

  it('resolves forward and source-note references and updates every link after insertion or reordering', async () => {
    const md = await renderer()
    const refs = '看 @fig:ems就知道，另見 @tbl:power。\n\n<small>圖源：@fig:ems 與 @fig:nilm。</small>\n\n'
    const source = `${refs}${figure('ems')}\n${table('power')}\n${figure('nilm')}`
    const links = (source: string) => Array.from(parse(md.render(source)).querySelectorAll('a.article-reference')).map(el => [el.textContent, el.getAttribute('href')])
    expect(links(source)).toEqual([['圖 1', '#fig-ems'], ['表 1', '#tbl-power'], ['圖 1', '#fig-ems'], ['圖 2', '#fig-nilm']])
    expect(links(`${figure('new')}\n${source}`)).toEqual([['圖 2', '#fig-ems'], ['表 1', '#tbl-power'], ['圖 2', '#fig-ems'], ['圖 3', '#fig-nilm']])
    expect(links(`${refs}${figure('nilm')}\n${figure('ems')}\n${table('power')}`)).toEqual([['圖 2', '#fig-ems'], ['表 1', '#tbl-power'], ['圖 2', '#fig-ems'], ['圖 1', '#fig-nilm']])
    expect(parse(md.render(source)).querySelector('p')?.textContent).toBe('看 圖 1就知道，另見 表 1。')
  })

  it.each([
    ['duplicate figure', `${figure('ems')}\n${figure('ems')}`, 'ems'],
    ['duplicate table', `${table('power')}\n${table('power')}`, 'power'],
    ['unknown reference', '@fig:missing', '@fig:missing'],
    ['wrong kind', `@tbl:ems\n\n${figure('ems')}`, '@tbl:ems'],
    ['invalid reference ID', '@fig:Bad', '@fig:Bad'],
    ['invalid block ID', '::: figure Bad\n![alt](/x.svg "caption")\n:::', 'Bad'],
    ['missing figure caption', '::: figure ems\n![alt](/x.svg)\n:::', 'ems'],
    ['missing table caption', `::: table power\n${plainTable}:::`, 'power'],
    ['missing closing fence', '::: figure ems\n![alt](/x.svg "caption")', 'ems'],
    ['extra figure content', '::: figure ems\n![alt](/x.svg "caption")\n\nextra\n:::', 'ems'],
    ['non-table body', '::: table power Caption\nnot a table\n:::', 'power'],
    ['nested block', `::: figure ems\n${figure('inner')}:::`, 'ems'],
  ])('rejects %s with an actionable diagnostic', async (_name, source, diagnostic) => {
    const md = await renderer()
    expect(() => md.render(source)).toThrow(diagnostic)
  })

  it('allows the same ID in the separately namespaced figure and table', async () => {
    const md = await renderer()
    const doc = parse(md.render(`@fig:shared 與 @tbl:shared\n\n${figure('shared')}\n${table('shared')}`))
    expect(Array.from(doc.querySelectorAll('a.article-reference')).map(el => el.getAttribute('href'))).toEqual(['#fig-shared', '#tbl-shared'])
  })

  it('keeps references literal in code, escaped text, images, HTML attributes and existing links', async () => {
    const md = await renderer()
    const source = [
      '`@fig:missing`',
      '```md\n@fig:missing\n```',
      '\\@fig:missing',
      '![alt @fig:missing](/x.svg "title @fig:missing")',
      '<span title="@fig:missing">文字</span>',
      '[見 @fig:missing](#fig:missing)',
      '<a href="#dest">見 @fig:missing</a>',
    ].join('\n\n')
    const doc = parse(md.render(source))
    expect(doc.querySelectorAll('a.article-reference')).toHaveLength(0)
    expect(doc.querySelector('code')?.textContent).toBe('@fig:missing')
    expect(doc.querySelector('img')?.getAttribute('alt')).toBe('alt @fig:missing')
    expect(doc.querySelector('span[title]')?.getAttribute('title')).toBe('@fig:missing')
    expect(doc.querySelectorAll('a')).toHaveLength(2)
    expect(doc.body.textContent).toContain('@fig:missing')
  })

  it('renders source links and emphasis in captions while leaving HTML, Vue and reference text literal', async () => {
    const md = await renderer()
    const caption = '**重繪** [[1]](#ref-1) <b>原文</b> {{ value }} @fig:literal [禁止](javascript:alert(1))'
    const doc = parse(md.render(`${figure('ems', caption)}\n\n::: table power **設備** [[1]](#ref-1)\n${plainTable}:::\n`))
    const figcaption = doc.querySelector('figcaption')!
    expect(figcaption.querySelector('strong')?.textContent).toBe('重繪')
    expect(figcaption.querySelector('a')?.getAttribute('href')).toBe('#ref-1')
    expect(figcaption.textContent).toContain('<b>原文</b> {{ value }} @fig:literal')
    expect(figcaption.querySelector('b')).toBeNull()
    expect(figcaption.querySelector('[href^="javascript:"]')).toBeNull()
    expect(figcaption.hasAttribute('v-pre')).toBe(true)
    expect(doc.querySelector('caption strong')?.textContent).toBe('設備')
    expect(doc.querySelector('caption a')?.getAttribute('href')).toBe('#ref-1')
  })

  it.each([
    '<div id="fig-ems"></div>',
    '<span ID=fig-ems>來源</span>',
    '<div title="x > y" id="fig&#45;ems"></div>',
    '# 標題 {#fig-ems}',
  ])('rejects static anchor collisions: %s', async (collision) => {
    const md = await renderer()
    expect(() => md.render(`${collision}\n\n${figure('ems')}`)).toThrow('fig-ems')
  })

  it('does not mistake quoted attribute text or HTML comments for conflicting IDs', async () => {
    const md = await renderer()
    expect(() => md.render(`<span data-note='id="fig-ems"'>文字</span>\n\n<!-- <div id="fig-ems"> -->\n\n${figure('ems')}`)).not.toThrow()
  })

  it('preserves the frozen task-entry migration and its independent inverse hash', async () => {
    const source = readFileSync(fileURLToPath(new NodeURL('./fixtures/article-caption-migrated.md', import.meta.url)), 'utf8')
    const entry = readFileSync(fileURLToPath(new NodeURL('./fixtures/article-caption-entry.md', import.meta.url)), 'utf8')
    expect(createHash('sha256').update(entry).digest('hex')).toBe(baseline.sourceSha256)
    expect(createHash('sha256').update(source).digest('hex')).toBe(provenance.migrated_sha256)
    const md = await renderer()
    const doc = parse(md.render(source))
    expect(doc.querySelectorAll('figure.article-figure')).toHaveLength(3)
    expect(doc.querySelectorAll('a.article-reference')).toHaveLength(6)
    expect(Array.from(doc.querySelectorAll('img')).map(el => ({ src: el.getAttribute('src'), alt: el.getAttribute('alt') }))).toEqual(baseline.images)
    expect(source.split('---', 3)[1]).toBe(baseline.frontmatter)
    expect(source).not.toMatch(/圖 [123]/)
    let original = source
    for (const [index, item] of baseline.figures.entries()) {
      const block = `::: figure ${item.id}\n![${item.alt}](${item.src} "${item.caption}")\n:::`
      expect(source).toContain(block)
      original = original.replace(block, item.original).replaceAll(`@fig:${item.id}`, `圖 ${index + 1}`)
    }
    expect(original).toBe(entry)
    expect(createHash('sha256').update(original).digest('hex')).toBe(baseline.sourceSha256)
    expect(doc.querySelector('#fig-nilm-process figcaption a')?.getAttribute('href')).toBe('#ref-1')
    expect(doc.querySelector('#fig-occupancy-process figcaption a')?.getAttribute('href')).toBe('#ref-4')
  })

  it('renders the production article with preserved media and source-note citations', async () => {
    const source = readFileSync(`${root}/post/course/security-awareness/electricity-privacy.md`, 'utf8')
    const md = await renderer()
    const doc = parse(md.render(source))
    expect(createHash('sha256').update(source).digest('hex')).toBe('8e6cc7a954ceaf4248ea8aa0f6d24ee343b8b5da4466f858b5440df95a0f68db')
    expect(doc.querySelectorAll('figure.article-figure')).toHaveLength(3)
    expect(doc.querySelectorAll('a.article-reference')).toHaveLength(6)
    expect(Array.from(doc.querySelectorAll('img')).map(el => ({ src: el.getAttribute('src'), alt: el.getAttribute('alt') }))).toEqual(baseline.images)
    expect(source.split('---', 3)[1]).toBe(baseline.frontmatter.replace('draft: true\n', '').replace('previewOnly: true\n', ''))
    expect(source).not.toMatch(/圖 [123]/)
    expect(source).toContain('@fig:nilm-process 是依 NILMTK 重新繪製的流程示意 [[1]](#ref-1)')
    expect(source).toContain('@fig:occupancy-process 依 Liang 與 Wang 的方法重繪 [[4]](#ref-4)')
    expect(doc.querySelector('a[href="#ref-1"]')).not.toBeNull()
    expect(doc.querySelector('a[href="#ref-4"]')).not.toBeNull()
  })

  it('compiles the copyable author-guide examples through the public renderer', async () => {
    const guide = readFileSync(fileURLToPath(new NodeURL('../docs/authoring/article-captions.md', import.meta.url)), 'utf8')
    const examples = [...guide.matchAll(/```md\n([\s\S]*?)```/g)].map(match => match[1])
    expect(examples.length).toBeGreaterThan(0)
    const md = await renderer()
    const doc = parse(md.render(examples.join('\n\n')))
    expect(doc.querySelectorAll('figure')).toHaveLength(1)
    expect(doc.querySelectorAll('table')).toHaveLength(2)
    expect(doc.querySelectorAll('caption')).toHaveLength(1)
    expect(doc.querySelectorAll('a.article-reference')).toHaveLength(3)
    expect(doc.querySelector('figure img')?.getAttribute('alt')).toBe('電鍋先以 600 W 加熱，再以 50 W 保溫。')
    expect(doc.querySelector('figcaption a')?.getAttribute('href')).toBe('#ref-1')
    expect(doc.querySelector('img[src$="p-cat-event.png"]')?.closest('figure')).toBeNull()
  })
})
