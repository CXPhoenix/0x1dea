import type { DefaultTheme } from 'vitepress'
import fs from 'node:fs'
import path from 'node:path'
import process from 'node:process'
import { fileURLToPath } from 'node:url'
import yaml from 'js-yaml'
import UnoCSS from 'unocss/vite'
import { defineConfig } from 'vitepress'

// Helper function to load YAML
function loadYaml(file: string): unknown {
  try {
    const filePath = path.resolve(path.dirname(new URL(import.meta.url).pathname), file)
    if (fs.existsSync(filePath)) {
      return yaml.load(fs.readFileSync(filePath, 'utf8'))
    }
  }
  catch (e) {
    console.error(`Error loading ${file}:`, e)
  }
  return []
}

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: '0x1DEA',
  description: 'Overflow of Imagination - 魔法是想像力的領域・資安也是',
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/phoenixWithText.svg' }],
    ['link', { rel: 'stylesheet', href: '/assets/fontawesome/fontawesome.min.css' }],
    ['link', { rel: 'stylesheet', href: '/assets/fontawesome/solid.min.css' }],
    ['link', { rel: 'stylesheet', href: '/assets/fontawesome/regular.min.css' }],
    ['link', { rel: 'stylesheet', href: '/assets/fontawesome/brands.min.css' }],
  ],
  themeConfig: {
    logo: '/circleImage.svg',
    nav: loadYaml('nav.yml') as DefaultTheme.NavItem[],
    sidebar: loadYaml('sidebar.yml') as DefaultTheme.Sidebar,

    footer: {
      message: '魔法是想像的領域 ~芙莉蓮 <葬送のフリーレン> ｜ 資安世界也是 ~CXPh03n1x',
      copyright: `Copyright © ${new Date().getFullYear()} CXPh03n1x@FHSH.isip-hs.whoam!`,
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/cxphoenix/0x1dea' }, // TODO: Update to user's github
    ],
  },
  vite: {
    envDir: fileURLToPath(new URL('../../', import.meta.url)),
    define: {
      'import.meta.env.CF_PAGES_BRANCH': JSON.stringify(process.env.CF_PAGES_BRANCH ?? ''),
    },
    plugins: [
      UnoCSS(),
    ],
  },
  markdown: {
    math: true,
  },
  transformPageData(pageData) {
    if (pageData.relativePath.endsWith('index.md') && pageData.relativePath !== 'index.md') {
      // 使用 ??= (邏輯空值賦值) 的好處是：
      // 如果您在某個特定的 index.md 裡手動寫了 sidebar: true，它會以您手寫的為主；
      // 如果沒寫，就會自動補上這裡的預設值 false。
      pageData.frontmatter.sidebar ??= false
      pageData.frontmatter.aside ??= false
      pageData.frontmatter.footer ??= true
      pageData.frontmatter.showParticle ??= true
      pageData.frontmatter.next ??= false
    }
  },
})
