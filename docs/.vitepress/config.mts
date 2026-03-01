import { defineConfig } from 'vitepress'
import fs from 'node:fs'
import path from 'node:path'
import yaml from 'js-yaml'
import UnoCSS from 'unocss/vite'

// Helper function to load YAML
const loadYaml = (file: string) => {
  try {
    const filePath = path.resolve(path.dirname(new URL(import.meta.url).pathname), file)
    if (fs.existsSync(filePath)) {
      return yaml.load(fs.readFileSync(filePath, 'utf8'))
    }
  } catch (e) {
    console.error(`Error loading ${file}:`, e)
  }
  return []
}

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "0x1DEA",
  description: "Overflow of Imagination - 魔法是想像力的領域・資安也是",
  head: [
    ['link', { rel: 'icon', type: "image/svg+xml", href: '/phoenixWithText.svg' }],
    ['link', { rel: 'stylesheet', href: '/assets/fontawesome/fontawesome.min.css' }],
    ['link', { rel: 'stylesheet', href: '/assets/fontawesome/solid.min.css' }],
    ['link', { rel: 'stylesheet', href: '/assets/fontawesome/regular.min.css' }],
    ['link', { rel: 'stylesheet', href: '/assets/fontawesome/brands.min.css' }],
  ],
  themeConfig: {
    logo: "/circleImage.svg",
    nav: loadYaml('nav.yml') as any,
    sidebar: loadYaml('sidebar.yml') as any,
    
    footer: {
      message: '魔法是想像的領域 ~芙莉蓮 <葬送のフリーレン> ｜ 資安世界也是 ~CXPh03n1x',
      copyright: `Copyright © ${new Date().getFullYear()} CXPh03n1x@FHSH.isip-hs.whoam!`
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/cxphoenix/0x1dea' } // TODO: Update to user's github
    ]
  },
  vite: {
    plugins: [
      UnoCSS()
    ]
  },
  markdown: {
    math: true,
  }
})
