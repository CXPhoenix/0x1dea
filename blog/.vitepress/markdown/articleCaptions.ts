import type { MarkdownRenderer } from 'vitepress'

type Token = ReturnType<MarkdownRenderer['parse']>[number]
interface CaptionBlock {
  kind: 'figure' | 'table'
  id: string
  caption?: string
}

function fail(message: string): never {
  throw new Error(`[article-captions] ${message}`)
}

/** Opt-in captions are compiled once per Markdown document, with no client state. */
export function articleCaptions(md: MarkdownRenderer) {
  md.block.ruler.before('fence', 'article_caption', (state, startLine, endLine, silent) => {
    const line = (n: number) => state.src.slice(state.bMarks[n] + state.tShift[n], state.eMarks[n]).trim()
    const opening = line(startLine)
    if (!/^:::\s+(?:figure|table)(?:\s|$)/.test(opening))
      return false
    if (silent)
      return true
    const match = /^:::\s+(figure|table)\s+([a-z][a-z0-9-]*)(?:\s+(\S.*))?$/.exec(opening)
    if (!match || (match[1] === 'figure' && match[3]))
      fail(`Invalid block: ${opening}`)
    const kind = match[1] as CaptionBlock['kind']
    const id = match[2]
    let closing = startLine + 1
    while (closing < endLine && line(closing) !== ':::') {
      if (/^:::\s+(?:figure|table)(?:\s|$)/.test(line(closing)))
        fail(`Nested block in ${kind} ${id}`)
      closing++
    }
    if (closing === endLine)
      fail(`Missing closing ::: for ${kind} ${id}`)
    const open = state.push('article_caption_open', 'figure', 1)
    open.meta = { kind, id, caption: match[3] } satisfies CaptionBlock
    open.map = [startLine, closing + 1]
    md.block.parse(state.getLines(startLine + 1, closing, state.blkIndent, false), md, state.env, state.tokens)
    state.push('article_caption_close', 'figure', -1)
    state.line = closing + 1
    return true
  }, { alt: ['paragraph', 'reference', 'blockquote', 'list'] })

  md.core.ruler.after('inline', 'article_captions', (state) => {
    let figureNumber = 0
    let tableNumber = 0
    const targets = new Map<string, string>()
    for (let i = 0; i < state.tokens.length; i++) {
      const open = state.tokens[i]
      if (open.type !== 'article_caption_open')
        continue
      const block = open.meta as CaptionBlock
      const closeIndex = state.tokens.findIndex((token, index) => index > i && token.type === 'article_caption_close')
      const body = state.tokens.slice(i + 1, closeIndex)
      const image = body[1]?.children?.[0]
      let caption = block.caption
      let captionIndex = i + 2
      if (block.kind === 'figure') {
        if (body.length !== 3 || body[0].type !== 'paragraph_open' || body[1].children?.length !== 1 || image?.type !== 'image')
          fail(`Expected one standalone image in figure ${block.id}`)
        caption = image.attrGet('title') ?? undefined
        open.attrSet('id', `fig-${block.id}`)
        open.attrSet('class', 'article-figure')
        body[0].hidden = true
        body[2].hidden = true
        captionIndex = closeIndex
      }
      else {
        if (body[0]?.type !== 'table_open' || body.at(-1)?.type !== 'table_close' || body.filter(t => t.type === 'table_open').length !== 1)
          fail(`Expected one Markdown table in table ${block.id}`)
        body[0].attrSet('id', `tbl-${block.id}`)
        body[0].meta = { articleCaptionTarget: true }
        open.tag = 'div'
        open.attrSet('class', 'article-table')
        state.tokens[closeIndex].tag = 'div'
      }
      if (caption === undefined || caption.trim() === '')
        fail(`Missing caption in ${block.kind} ${block.id}`)
      const tag = block.kind === 'figure' ? 'figcaption' : 'caption'
      const number = block.kind === 'figure' ? ++figureNumber : ++tableNumber
      const label = `${block.kind === 'figure' ? '圖' : '表'} ${number}`
      const anchor = `${block.kind === 'figure' ? 'fig' : 'tbl'}-${block.id}`
      if (targets.has(anchor))
        fail(`Duplicate ${block.kind} ${block.id}`)
      targets.set(anchor, label)
      const captionOpen = new state.Token(`${tag}_open`, tag, 1)
      captionOpen.attrSet('v-pre', '')
      const text = new state.Token('text', '', 0)
      text.content = `${label}：`
      const inline = new state.Token('inline', '', 0)
      const children: Token[] = []
      md.inline.parse(caption, md, state.env, children)
      for (const child of children) {
        if (child.type === 'html_inline')
          child.type = 'text'
      }
      inline.children = [text, ...children]
      inline.meta = { caption: true }
      const captionClose = new state.Token(`${tag}_close`, tag, -1)
      state.tokens.splice(captionIndex, 0, captionOpen, inline, captionClose)
      i = closeIndex + 3
    }

    for (const token of state.tokens) {
      if (token.type !== 'inline' || !token.children || (token.meta as { caption?: boolean } | null)?.caption === true)
        continue
      let linkDepth = 0
      token.children = token.children.flatMap((child): Token[] => {
        if (child.type === 'link_open' || (child.type === 'html_inline' && /^<a(?:\s|>)/i.test(child.content)))
          linkDepth++
        if (child.type === 'link_close' || (child.type === 'html_inline' && /^<\/a\s*>/i.test(child.content)))
          linkDepth = Math.max(0, linkDepth - 1)
        if (child.type !== 'text' || linkDepth)
          return [child]
        const result: Token[] = []
        let previous = 0
        for (const match of child.content.matchAll(/(?<![\w@])@(fig|tbl):([\w-]*)/g)) {
          if (!/^[a-z][a-z0-9-]*$/.test(match[2]))
            fail(`Invalid reference ${match[0]}`)
          const before = new state.Token('text', '', 0)
          before.content = child.content.slice(previous, match.index)
          result.push(before)
          const anchor = `${match[1]}-${match[2]}`
          const label = targets.get(anchor)
          if (label === undefined)
            fail(`Unknown reference ${match[0]}`)
          const open = new state.Token('link_open', 'a', 1)
          open.attrSet('href', `#${anchor}`)
          open.attrSet('class', 'article-reference')
          const text = new state.Token('text', '', 0)
          text.content = label
          result.push(open, text, new state.Token('link_close', 'a', -1))
          previous = match.index + match[0].length
        }
        const after = new state.Token('text', '', 0)
        after.content = child.content.slice(previous)
        result.push(after)
        return result
      })
    }
  })

  // Run after VitePress has generated heading anchors, including explicit IDs.
  md.core.ruler.push('article_caption_anchors', (state) => {
    const generated = new Set<string>()
    for (const token of state.tokens) {
      if (token.type === 'article_caption_open') {
        const block = token.meta as CaptionBlock
        generated.add(`${block.kind === 'figure' ? 'fig' : 'tbl'}-${block.id}`)
      }
    }
    const check = (id: string | null) => {
      if (id !== null && generated.has(md.utils.unescapeAll(id)))
        fail(`Reserved anchor collision: ${md.utils.unescapeAll(id)}`)
    }
    const inspect = (tokens: Token[]) => {
      for (const token of tokens) {
        if (token.type !== 'article_caption_open' && (token.meta as { articleCaptionTarget?: boolean } | null)?.articleCaptionTarget !== true)
          check(token.attrGet('id'))
        if (token.type === 'html_inline' || token.type === 'html_block') {
          const html = token.content.replace(/<!--[\s\S]*?-->/g, '')
          // Consume whole attributes, so an ID mentioned inside another value is not an ID.
          for (const tag of html.matchAll(/<[a-z][\w:-]*(?:\s+[^\s"'<>/=]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s"'=<>`]+))?)*\s*\/?>/gi)) {
            for (const attr of tag[0].matchAll(/\s+([^\s"'<>/=]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?/g)) {
              if (attr[1].toLowerCase() === 'id')
                check(attr[2] ?? attr[3] ?? attr[4] ?? null)
            }
          }
        }
        if (token.children)
          inspect(token.children)
      }
    }
    inspect(state.tokens)
  })
}
