import { describe, it, expect } from 'vitest';
import path from 'node:path';
import { parseArgs, getFormattedDate, getAssetFolderName, DEFAULT_DIR, ASSETS_ROOT } from '../scripts/vphelper';

describe('vphelper', () => {
    
    // ... parseArgs 和 getFormattedDate 的測試保持不變，省略以節省篇幅 ...
    // (您可以保留原本這兩個 describe block)
    
    describe('parseArgs', () => {
        it('應該正確解析基本的 new post 指令', () => {
            const args = ['new', 'post', 'MyArticle'];
            const config = parseArgs(args);
            expect(config.command).toEqual(['new', 'post']);
            expect(config.postName).toBe('MyArticle');
            expect(config.options.dir).toBe(DEFAULT_DIR);
        });
        // ... 其他 parseArgs 測試 ...
         it('當 -d 和 -c 同時使用時應拋出錯誤', () => {
            const args = ['new', 'post', 'MyArticle', '-d', 'path', '-c', 'cat'];
            expect(() => parseArgs(args)).toThrow('參數 -c 與 -d 不能同時使用');
        });
    });

    describe('getFormattedDate', () => {
        it('應該回傳符合 ISO 8601 且時區為 +08:00 的字串', () => {
            const dateStr = getFormattedDate();
            const regex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+08:00$/;
            expect(dateStr).toMatch(regex);
        });
    });

    describe('Assets Configuration', () => {
        it('ASSETS_ROOT 應該是 docs/public/assets', () => {
             expect(ASSETS_ROOT).toBe('docs/public/assets');
        });
    });

    describe('getAssetFolderName', () => {
        // 邏輯: 移除 docs, 連接剩餘路徑與檔名
        
        it('範例1: 預設資料夾 docs/post', () => {
            // docs/post -> post -> post_hello
            const targetDir = 'docs/post';
            const safeName = 'hello';
            const expected = 'post_hello';
            expect(getAssetFolderName(targetDir, safeName)).toBe(expected);
        });

        it('範例2: 使用 -c 指定分類 (docs/post/hello)', () => {
            // docs/post/hello -> post/hello -> post_hello_world
            const targetDir = 'docs/post/hello';
            const safeName = 'world';
            const expected = 'post_hello_world';
            expect(getAssetFolderName(targetDir, safeName)).toBe(expected);
        });

        it('範例3: 使用 -d 指定多層資料夾 (docs/new-posts)', () => {
            // docs/new-posts -> new-posts -> new-posts_hello_world
            const targetDir = 'docs/new-posts';
            const safeName = 'hello_world';
            const expected = 'new-posts_hello_world';
            expect(getAssetFolderName(targetDir, safeName)).toBe(expected);
        });

        it('範例4: 使用 -d 指定根層資料夾 (docs)', () => {
            // docs -> (empty) -> hi_vitepress
            // 因為沒有 docs 之後的路徑，所以只剩檔名
            const targetDir = 'docs';
            const safeName = 'hi_vitepress';
            const expected = 'root_hi_vitepress';
            expect(getAssetFolderName(targetDir, safeName)).toBe(expected);
        });

        it('應該能處理絕對路徑', () => {
            // 模擬絕對路徑: /Users/me/project/docs/guide
            // 相對路徑轉換後為: docs/guide
            // 結果: guide_setup
            const cwd = process.cwd();
            const targetDir = path.resolve(cwd, 'docs/guide');
            const safeName = 'setup';
            const expected = 'guide_setup';
            expect(getAssetFolderName(targetDir, safeName)).toBe(expected);
        });
    });
});