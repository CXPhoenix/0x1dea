import { createContentLoader, type ContentData } from 'vitepress'

/**
 * 定義 Post 的資料結構
 * 匯出此介面，方便在 Vue 元件中 import 使用
 */
export interface Post {
  title: string
  url: string
  description: string
  createdTime: Date
  thumbnail: string
  category: string
  categoryFromPath: string
  categoryRootPath: string
}

declare const data: Post[]
export { data }

/**
 * 輔助函式：從 URL 解析分類
 * 將邏輯抽離，保持 transform 乾淨
 */
function getCategoryFromUrl(url: string): string {
  // 移除開頭的 /post/ 以及結尾的 .md, .html 或 /
  const relativePath = url
    .replace(/^\/post\//, '')
    .replace(/\.(md|html)$/, '')
    .replace(/\/$/, '')

  const segments = relativePath.split('/')

  // 如果路徑包含子目錄 (e.g., tech/js/intro)，取檔案名稱前的部分作為分類
  if (segments.length > 1) {
    return segments.slice(0, -1).join('/')
  }
  
  // 如果只有一層或無法判斷，回傳第一個片段或預設值
  return '綜合'
}

function getCategoryRootPath(url: string): string {
  return url.split('/').slice(0, -1).join('/')
}

export default createContentLoader('post/**/*.md', {
  includeSrc: true, // 如果不需要全文搜尋，建議設為 false 以減少 bundle size
  render: false,
  excerpt: false,
  
  /**
   * 轉換原始資料
   * @param rawData VitePress 載入的原始資料
   */
  transform(rawData: ContentData[]): Post[] {
    const categories: Map<string, string> = new Map()
    rawData.filter((post) => post.frontmatter.isIndex).forEach((post) => {
      const categoryRootPath = getCategoryRootPath(post.url)
      if (!categories.has(categoryRootPath)) {
        categories.set(categoryRootPath, post.frontmatter.category)
      }
    })
    const posts = rawData
      .filter((post) => !post.frontmatter.isIndex)
      .map((post, idx) => {
        // 使用 Date.now() 確保每次 build 的預設時間基準一致，或固定一個種子
        // 這裡為了演示保留您的邏輯，但建議在 frontmatter 必填 date
        const fallbackDate = new Date(Date.now() - idx * 1000 * 60 * 60 * 24)

        return {
          title: post.frontmatter.title || '無標題',
          url: post.url,
          description: post.frontmatter.description ?? '閱讀更多...',
          createdTime: post.frontmatter.createdTime 
            ? new Date(post.frontmatter.createdTime) 
            : fallbackDate,
          thumbnail: post.frontmatter.thumbnail || `https://picsum.photos/seed/${idx + 1}/400/300`,
          category: post.frontmatter.category || (categories.get(getCategoryRootPath(post.url)) ?? getCategoryFromUrl(post.url)),
          categoryFromPath: getCategoryFromUrl(post.url),
          categoryRootPath: getCategoryRootPath(post.url),
        }
      })

    return posts
  }
})