#!/usr/bin/env node

/**
 * VitePress Helper Tool (TypeScript Version)
 * 使用方法: npx tsx scripts/vphelper.ts new post <post_name> [-d <path> | -c <category>]
 */

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

// 定義參數設定的介面
export interface HelperConfig {
    command: string[];
    options: {
        dir: string;
    };
    postName: string;
}

// 預設資料夾路徑
export const DEFAULT_DIR = 'docs/post';

// 參數解析器
export function parseArgs(args: string[]): HelperConfig {
    const config: HelperConfig = {
        command: [],
        options: {
            dir: DEFAULT_DIR // 預設資料夾
        },
        postName: ''
    };

    // 用來標記是否已經設定過路徑，用於檢測衝突
    let isCustomDirSet = false; // 是否使用了 -d
    let isCategorySet = false;  // 是否使用了 -c

    for (let i = 0; i < args.length; i++) {
        const arg = args[i];

        if (arg === '-d') {
            // 檢查衝突
            if (isCategorySet) {
                throw new Error('參數 -c 與 -d 不能同時使用。');
            }

            if (args[i + 1] && !args[i + 1].startsWith('-')) {
                config.options.dir = args[i + 1];
                isCustomDirSet = true;
                i++; // 跳過下一個參數因為它是值
            } else {
                throw new Error('參數 -d 後面需要接路徑。');
            }
        } else if (arg === '-c') {
            // 檢查衝突
            if (isCustomDirSet) {
                throw new Error('參數 -c 與 -d 不能同時使用。');
            }

            if (args[i + 1] && !args[i + 1].startsWith('-')) {
                // 將分類名稱接在預設路徑後面
                config.options.dir = path.join(DEFAULT_DIR, args[i + 1]);
                isCategorySet = true;
                i++; // 跳過下一個參數因為它是值
            } else {
                throw new Error('參數 -c 後面需要接分類名稱。');
            }
        } else if (!arg.startsWith('-')) {
            // 如果不是選項，則視為命令或名稱的一部分
            if (config.command.length < 2) {
                config.command.push(arg);
            } else {
                // new post 之後的參數視為 post_name
                config.postName = arg;
            }
        }
    }
    return config;
}

// 格式化時間：YYYY-mm-ddTHH:MM:SS+08:00 (UTC+8)
export function getFormattedDate(): string {
    const now = new Date();
    // 1. 取得 UTC 時間並加上 8 小時 (UTC+8) 的毫秒數
    const offset = 8 * 60 * 60 * 1000;
    const utc8Date = new Date(now.getTime() + offset);

    // 2. toISOString() 會回傳該時間物件的 UTC 字串表示法
    // 因為我們手動加了 8 小時，所以數值部分已經變成了 UTC+8 的時間
    // 3. 最後將結尾的 'Z' (代表 UTC) 替換為 '+08:00' 來正確標示時區
    return utc8Date.toISOString().replace(/\.\d{3}Z$/, '+08:00');
}

// 主要執行邏輯
export function main(): void {
    // 取得命令列參數 (排除 node 和 script 路徑)
    const args: string[] = process.argv.slice(2);

    try {
        const { command, options, postName } = parseArgs(args);

        // 檢查指令是否為 new post
        if (command[0] !== 'new' || command[1] !== 'post') {
            console.error('\x1b[31m%s\x1b[0m', '錯誤: 未知的指令。');
            console.log('用法: npx tsx scripts/vphelper.ts new post <post_name> [-d <path> | -c <category>]');
            process.exit(1);
        }

        if (!postName) {
            console.error('\x1b[31m%s\x1b[0m', '錯誤: 請輸入文章名稱 (post_name)。');
            process.exit(1);
        }

        // 處理檔案名稱：將空格轉為底線 (例如: "my new post" -> "my_new_post")
        const safeFileName = postName.trim().replace(/\s+/g, '_');

        // 處理標題：每個單字首字母大寫 (例如: "my new post" -> "My New Post")
        const titleName = postName.replace(/\b\w/g, (char) => char.toUpperCase());

        // 建構目標路徑
        // process.cwd() 確保路徑是相對於執行指令的專案根目錄
        const targetDir = path.resolve(process.cwd(), options.dir);
        // 使用處理過的檔案名稱，加上 .md
        const fileName = `${safeFileName}.md`; 
        const filePath = path.join(targetDir, fileName);

        // 準備檔案內容模板
        const createdTime = getFormattedDate();
        // 文章內容模板
        const fileContent = `---
title: ${titleName}
description:
createdTime: ${createdTime}
thumbnail:
---

# ${titleName}
`;

        // 1. 確保資料夾存在
        if (!fs.existsSync(targetDir)) {
            console.log(`正在建立資料夾: ${options.dir}...`);
            fs.mkdirSync(targetDir, { recursive: true });
        }

        // 2. 檢查檔案是否已存在
        if (fs.existsSync(filePath)) {
            console.error('\x1b[33m%s\x1b[0m', `警告: 檔案 "${fileName}" 已經存在於 "${options.dir}"，操作已取消。`);
            process.exit(1);
        }

        // 3. 寫入檔案
        fs.writeFileSync(filePath, fileContent, 'utf8');

        console.log('\x1b[32m%s\x1b[0m', '✅ 成功建立新文章！');
        console.log(`📁 路徑: ${filePath}`);
        console.log(`📅 時間: ${createdTime}`);

    } catch (error: any) {
        console.error('\x1b[31m%s\x1b[0m', '❌ 發生錯誤:');
        console.error(error.message);
        process.exit(1);
    }
}

// 只有當直接執行此檔案時才執行 main
// 使用 ESM 方式判斷 entry point
const isMainModule = process.argv[1] === fileURLToPath(import.meta.url);
if (isMainModule) {
    main();
}