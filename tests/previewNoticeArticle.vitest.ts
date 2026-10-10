import { readFileSync } from 'node:fs'
import { fileURLToPath, URL as NodeURL } from 'node:url'
import { createMarkdownRenderer } from 'vitepress'
import { expect, it } from 'vitest'

it('compiles the selected article with a shared notice and keeps following prose outside', async () => {
  const md = await createMarkdownRenderer(fileURLToPath(new NodeURL('../blog/', import.meta.url)))
  const source = readFileSync(fileURLToPath(new NodeURL('../blog/post/course/security-awareness/electricity-privacy.md', import.meta.url)), 'utf8')
  const html = md.render(source)
  expect(html).toContain('<PreviewNotice')
  expect(html).not.toContain('class="info custom-block"')
  expect(html).toMatch(/<PreviewNotice[\s\S]*?\/>\s*<(?:ArticleSummary\b|p>假設兩個家庭)/)
})
