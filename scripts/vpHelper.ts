#!/usr/bin/env node

/**
 * VitePress Helper Tool (TypeScript Version)
 * 使用方法: npx tsx scripts/vphelper.ts new post <post_name> [-d <path> | -c <category>]
 */

import fs from 'node:fs'
import path from 'node:path'
import process from 'node:process'
import { fileURLToPath } from 'node:url'

// 定義參數設定的介面
export interface HelperConfig {
  command: string[]
  options: {
    dir: string
  }
  postName: string
}

// 預設資料夾路徑
export const DEFAULT_DIR = 'blog/post'
// 更新 Assets 根目錄路徑
export const ASSETS_ROOT = 'blog/public/assets'

// 參數解析器
export function parseArgs(args: string[]): HelperConfig {
  const config: HelperConfig = {
    command: [],
    options: {
      dir: DEFAULT_DIR, // 預設資料夾
    },
    postName: '',
  }

  // 用來標記是否已經設定過路徑，用於檢測衝突
  let isCustomDirSet = false // 是否使用了 -d
  let isCategorySet = false // 是否使用了 -c

  for (let i = 0; i < args.length; i++) {
    const arg = args[i]

    if (arg === '-d') {
      // 檢查衝突
      if (isCategorySet) {
        throw new Error('參數 -c 與 -d 不能同時使用。')
      }

      if (args[i + 1] && !args[i + 1].startsWith('-')) {
        config.options.dir = args[i + 1]
        isCustomDirSet = true
        i++ // 跳過下一個參數因為它是值
      }
      else {
        throw new Error('參數 -d 後面需要接路徑。')
      }
    }
    else if (arg === '-c') {
      // 檢查衝突
      if (isCustomDirSet) {
        throw new Error('參數 -c 與 -d 不能同時使用。')
      }

      if (args[i + 1] && !args[i + 1].startsWith('-')) {
        // 將分類名稱接在預設路徑後面
        config.options.dir = path.join(DEFAULT_DIR, args[i + 1])
        isCategorySet = true
        i++ // 跳過下一個參數因為它是值
      }
      else {
        throw new Error('參數 -c 後面需要接分類名稱。')
      }
    }
    else if (!arg.startsWith('-')) {
      // 如果不是選項，則視為命令或名稱的一部分
      if (config.command.length < 2) {
        config.command.push(arg)
      }
      else {
        // new post 之後的參數視為 post_name
        config.postName = arg
      }
    }
  }
  return config
}

// 格式化時間：YYYY-mm-ddTHH:MM:SS+08:00 (UTC+8)
export function getFormattedDate(): string {
  const now = new Date()
  // 1. 取得 UTC 時間並加上 8 小時 (UTC+8) 的毫秒數
  const offset = 8 * 60 * 60 * 1000
  const utc8Date = new Date(now.getTime() + offset)

  // 2. toISOString() 會回傳該時間物件的 UTC 字串表示法
  // 因為我們手動加了 8 小時，所以數值部分已經變成了 UTC+8 的時間
  // 3. 最後將結尾的 'Z' (代表 UTC) 替換為 '+08:00' 來正確標示時區
  return utc8Date.toISOString().replace(/\.\d{3}Z$/, '+08:00')
}

// 取得靜態資源資料夾名稱
// 新邏輯: 移除 blog 前綴後的完整路徑 + "_" + 安全的文章名稱
export function getAssetFolderName(targetDir: string, safeFileName: string): string {
  const cwd = process.cwd()
  // 確保 targetDir 轉為相對於專案根目錄的路徑
  // 如果傳入的是絕對路徑，轉為相對；如果是相對路徑，resolve 後再轉相對 (normalize)
  const absoluteTarget = path.isAbsolute(targetDir) ? targetDir : path.resolve(cwd, targetDir)
  const relativePath = path.relative(cwd, absoluteTarget)

  // 分割路徑並過濾掉第一個路徑
  // split 會把 'blog/post/hello' 拆成 ['blog', 'post', 'hello']
  const pathSegments = relativePath.split(path.sep).slice(1)

  // 組合前綴：post_hello
  const prefix = pathSegments.join('_')

  // 如果前綴是空的 (代表檔案直接在 blog 下)，回傳檔名 `root_{檔名}`
  if (!prefix) {
    return `root_${safeFileName}`
  }

  // 回傳：post_hello_world
  return `${prefix}_${safeFileName}`
}

// 主要執行邏輯
export function main(): void {
  // 取得命令列參數 (排除 node 和 script 路徑)
  const args: string[] = process.argv.slice(2)

  try {
    const { command, options, postName } = parseArgs(args)

    // 檢查指令是否為 new post
    if (command[0] !== 'new' || command[1] !== 'post') {
      console.error('\x1B[31m%s\x1B[0m', '錯誤: 未知的指令。')
      console.log('用法: npx tsx scripts/vphelper.ts new post <post_name> [-d <path> | -c <category>]')
      process.exit(1)
    }

    if (!postName) {
      console.error('\x1B[31m%s\x1B[0m', '錯誤: 請輸入文章名稱 (post_name)。')
      process.exit(1)
    }

    // 處理檔案名稱：將空格轉為底線 (例如: "my new post" -> "my_new_post")
    const safeFileName = postName.trim().replace(/\s+/g, '_')

    // 處理標題：每個單字首字母大寫 (例如: "my new post" -> "My New Post")
    const titleName = postName.replace(/\b\w/g, char => char.toUpperCase())

    // 建構目標路徑
    const rootDir = process.cwd()
    const targetDir = path.resolve(rootDir, options.dir)

    // 1. 處理文章檔案路徑
    const fileName = `${safeFileName}.md`
    const filePath = path.join(targetDir, fileName)

    // 2. 處理 Assets 資料夾路徑
    const assetFolderName = getAssetFolderName(targetDir, safeFileName)
    const assetDirPath = path.resolve(rootDir, ASSETS_ROOT, assetFolderName)

    // 準備檔案內容模板
    const createdTime = getFormattedDate()
    // 文章內容模板
    const fileContent = `---
title: ${titleName}
description:
createdTime: ${createdTime}
thumbnail:
---

# ${titleName}
`

    // --- 開始執行檔案系統操作 ---

    // A. 建立文章資料夾
    if (!fs.existsSync(targetDir)) {
      console.log(`正在建立資料夾: ${options.dir}...`)
      fs.mkdirSync(targetDir, { recursive: true })
    }

    // B. 檢查文章是否已存在
    if (fs.existsSync(filePath)) {
      console.error('\x1B[33m%s\x1B[0m', `警告: 檔案 "${fileName}" 已經存在於 "${options.dir}"，操作已取消。`)
      process.exit(1)
    }

    // C. 寫入文章檔案
    fs.writeFileSync(filePath, fileContent, 'utf8')

    // D. 建立 Assets 資料夾
    fs.mkdirSync(assetDirPath, { recursive: true })

    console.log('\x1B[32m%s\x1B[0m', '✅ 成功建立新文章！')
    console.log(`📄 文章: ${filePath}`)
    console.log(`🖼️  資源: ${assetDirPath}`)
    console.log(`📅 時間: ${createdTime}`)
  }
  catch (error) {
    console.error('\x1B[31m%s\x1B[0m', '❌ 發生錯誤:')
    console.error((error as { message: unknown }).message)
    process.exit(1)
  }
}

// 只有當直接執行此檔案時才執行 main
const isMainModule = process.argv[1] === fileURLToPath(import.meta.url)
if (isMainModule) {
  main()
}
