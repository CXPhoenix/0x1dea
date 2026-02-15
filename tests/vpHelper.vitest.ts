import { describe, it, expect } from 'vitest';
import path from 'node:path';
import { parseArgs, getFormattedDate, DEFAULT_DIR } from '../scripts/vphelper';

describe('vphelper', () => {
    
    describe('parseArgs', () => {
        it('應該正確解析基本的 new post 指令', () => {
            const args = ['new', 'post', 'MyArticle'];
            const config = parseArgs(args);
            
            expect(config.command).toEqual(['new', 'post']);
            expect(config.postName).toBe('MyArticle');
            expect(config.options.dir).toBe(DEFAULT_DIR);
        });

        it('應該支援含有空白的文章名稱', () => {
            const args = ['new', 'post', 'My', 'Awesome', 'Article'];
            const config = parseArgs(args);
            
            // "My" 被視為 command 的一部分? 不，根據邏輯：
            // 0: new (command)
            // 1: post (command)
            // 2: My (postName)
            // 3: Awesome (被覆蓋到 postName 或被忽略？)
            
            // 讓我們回顧 parseArgs 的邏輯：
            // 如果不是選項，且 command 長度 >= 2，則設為 postName。
            // 迴圈會繼續，後面的字串會不斷覆蓋 postName。
            // 這是一個簡單實作的特性，我們可以用它來測試最後一個參數是否被捕獲，
            // 但實務上使用者應該用引號包起來 "My Awesome Article" 當作一個參數傳入。
            
            const quotedArgs = ['new', 'post', 'My Awesome Article'];
            const quotedConfig = parseArgs(quotedArgs);
            expect(quotedConfig.postName).toBe('My Awesome Article');
        });

        it('應該正確解析 -d 參數', () => {
            const args = ['new', 'post', 'MyArticle', '-d', 'custom/path'];
            const config = parseArgs(args);
            
            expect(config.options.dir).toBe('custom/path');
        });

        it('應該正確解析 -c 參數 (接在預設路徑後)', () => {
            const args = ['new', 'post', 'MyArticle', '-c', 'tech'];
            const config = parseArgs(args);
            
            const expectedPath = path.join(DEFAULT_DIR, 'tech');
            expect(config.options.dir).toBe(expectedPath);
        });

        it('當 -d 和 -c 同時使用時應拋出錯誤', () => {
            const args = ['new', 'post', 'MyArticle', '-d', 'path', '-c', 'cat'];
            
            expect(() => parseArgs(args)).toThrow('參數 -c 與 -d 不能同時使用');
        });

        it('當 -c 和 -d 同時使用時應拋出錯誤 (順序相反)', () => {
            const args = ['new', 'post', 'MyArticle', '-c', 'cat', '-d', 'path'];
            
            expect(() => parseArgs(args)).toThrow('參數 -c 與 -d 不能同時使用');
        });

        it('當 -d 後面沒有接路徑時應拋出錯誤', () => {
            const args = ['new', 'post', 'MyArticle', '-d'];
            expect(() => parseArgs(args)).toThrow('參數 -d 後面需要接路徑');
        });

        it('當 -c 後面沒有接分類時應拋出錯誤', () => {
            const args = ['new', 'post', 'MyArticle', '-c'];
            expect(() => parseArgs(args)).toThrow('參數 -c 後面需要接分類名稱');
        });
        
        it('當 -d 後面接的是另一個 flag 時應拋出錯誤', () => {
            const args = ['new', 'post', 'MyArticle', '-d', '-c'];
            // 根據邏輯，下一個參數如果是 -c，startsWith('-') 會為真，進入 else 區塊
            expect(() => parseArgs(args)).toThrow('參數 -d 後面需要接路徑');
        });
    });

    describe('getFormattedDate', () => {
        it('應該回傳符合 ISO 8601 且時區為 +08:00 的字串', () => {
            const dateStr = getFormattedDate();
            
            // 驗證格式: YYYY-MM-DDTHH:mm:ss+08:00
            const regex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+08:00$/;
            expect(dateStr).toMatch(regex);
        });

        it('產生的時間應該可以被 Date 物件正確解析', () => {
            const dateStr = getFormattedDate();
            const date = new Date(dateStr);
            
            expect(date.toString()).not.toBe('Invalid Date');
            expect(isNaN(date.getTime())).toBe(false);
        });
    });
});