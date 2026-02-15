#!/usr/bin/env node

/**
 * VitePress Helper Tool (TypeScript Version)
 * 使用方法: npx tsx scripts/vphelper.ts new post <post_name> [-d <directory>]
 */

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

// 定義參數設定的介面
interface HelperConfig {
    command: string[];
    options: {
        dir: string;
    };
    postName: string;
}

// 取得命令列參數 (排除 node 和 script 路徑)
const args: string[] = process.argv.slice(2);

// 預設資料夾
const DEFAULT_DIR = 'docs/post';

// 參數解析器
function parseArgs(args: string[]): HelperConfig {
    const config: HelperConfig = {
        command: [],
        options: {
            dir: DEFAULT_DIR // 預設資料夾
        },
        postName: ''
    };

    for (let i = 0; i < args.length; i++) {
        const arg = args[i];

        if (arg === '-d') {
            if (args[i + 1]) {
                config.options.dir = args[i + 1];
                i++; // 跳過下一個參數因為它是值
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

// 格式化時間：YYYY-mm-ddTHH:MM:SSZ
function getFormattedDate(): string {
    const now = new Date();
    // toISOString() 預設格式為 2023-10-05T14:48:00.000Z
    // 我們利用正則表達式移除毫秒 (.000) 部分
    return now.toISOString().replace(/\.\d{3}Z$/, 'Z');
}

// 主要執行邏輯
function main(): void {
    const { command, options, postName } = parseArgs(args);

    // 檢查指令是否為 new post
    if (command[0] !== 'new' || command[1] !== 'post') {
        console.error('\x1b[31m%s\x1b[0m', '錯誤: 未知的指令。');
        console.log('用法: npx tsx scripts/vphelper.ts new post <post_name> [-d <directory>]');
        process.exit(1);
    }

    if (!postName) {
        console.error('\x1b[31m%s\x1b[0m', '錯誤: 請輸入文章名稱 (post_name)。');
        process.exit(1);
    }

    // 建構目標路徑
    // process.cwd() 確保路徑是相對於執行指令的專案根目錄
    const targetDir = path.resolve(process.cwd(), options.dir);
    // 假設 postName 為檔案名稱，加上 .md
    const fileName = `${postName}.md`; 
    const filePath = path.join(targetDir, fileName);

    // 準備檔案內容模板
    const createdTime = getFormattedDate();
    // 注意: 這裡保留了你要求的 'thumbnil' 拼寫
    const fileContent = `---
title: ${postName}
abstract:
createdTime: ${createdTime}
thumbnil:
---

# ${postName}
`;

    try {
        // 1. 確保資料夾存在 (recursive: true 會自動建立不存在的子資料夾)
        if (!fs.existsSync(targetDir)) {
            console.log(`正在建立資料夾: ${options.dir}...`);
            fs.mkdirSync(targetDir, { recursive: true });
        }

        // 2. 檢查檔案是否已存在，避免覆蓋
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

main();