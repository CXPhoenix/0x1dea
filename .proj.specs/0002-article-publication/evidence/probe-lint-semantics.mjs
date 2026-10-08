import assert from 'node:assert/strict'
import { execFileSync } from 'node:child_process'
import fs from 'node:fs'
import { createRequire } from 'node:module'
import path from 'node:path'
import process from 'node:process'
import vm from 'node:vm'
import yaml from 'js-yaml'

const root = process.cwd()
const base = '8890d5250e22ec4ee0e0493c1e72bab89d16489b'
const toolRequire = createRequire(import.meta.resolve('@antfu/eslint-config'))
const ts = toolRequire('typescript')
function source(name, before) {
  return before
    ? execFileSync('git', ['show', `${base}:${name}`], { cwd: root, encoding: 'utf8' })
    : fs.readFileSync(path.join(root, name), 'utf8')
}
function load(name, before) {
  const text = source(name, before).replaceAll('import.meta.url', JSON.stringify('file:///lint-probe-vphelper.ts'))
  const code = ts.transpileModule(text, { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022, esModuleInterop: true } }).outputText
  const exports = {}
  const require = name => name === 'vitepress'
    ? { createContentLoader: (_pattern, options) => options }
    : toolRequire(name)
  vm.runInNewContext(code, { exports, require, Date, console, process }, { timeout: 5000 })
  return exports
}
const oldLoader = load('blog/shared/posts.data.ts', true).default
const newLoader = load('blog/shared/posts.data.ts', false).default
const oldCli = load('scripts/vpHelper.ts', true)
const newCli = load('scripts/vpHelper.ts', false)
const encode = value => JSON.stringify(value)
const originalNow = Date.now
let transformCases = 0
Date.now = () => 1772323200000
try {
  const values = [undefined, null, '', false, 0, 'value', '2026-02-27T00:00:00+08:00']
  for (const value of values) {
    const input = [
      { url: '/post/security/index.html', frontmatter: { isIndex: true, category: 'Security' } },
      { url: '/post/security/a.html', frontmatter: { title: value, description: value, createdTime: value, thumbnail: value, category: value } },
      { url: '/post/b.html', frontmatter: { isIndex: value, title: 'B' } },
    ]
    assert.equal(encode(newLoader.transform(input)), encode(oldLoader.transform(input)))
    transformCases++
  }
  const articles = execFileSync('git', ['ls-files', '-z', 'blog/post'], { encoding: 'utf8' }).split('\0').filter(name => name.endsWith('.md'))
  const input = articles.map((name) => {
    const text = fs.readFileSync(name, 'utf8')
    const match = text.match(/^---\n([\s\S]*?)\n---/)
    return { url: `/${name.slice(5).replace(/\.md$/, '.html')}`, frontmatter: match ? yaml.load(match[1]) : {} }
  })
  assert.equal(encode(newLoader.transform(input)), encode(oldLoader.transform(input)))
  transformCases++
}
finally {
  Date.now = originalNow
}
const argCases = [
  ['new', 'post', 'Name'],
  ['new', 'post', 'Name', '-c', 'security'],
  ['new', 'post', 'Name', '-d', 'blog/custom'],
  ['new', 'post', 'Name', '-c'],
  ['new', 'post', 'Name', '-d'],
  ['new', 'post', 'Name', '-c', 'x', '-d', 'y'],
  ['new', 'post', 'Name', '-d', 'x', '-c', 'y'],
  [],
  ['other', 'command'],
]
function observe(fn, args) {
  try {
    return { value: fn(args) }
  }
  catch (error) { return { error: error.message } }
}
for (const args of argCases)
  assert.equal(encode(observe(newCli.parseArgs, args)), encode(observe(oldCli.parseArgs, args)))
for (const dir of ['blog/post', 'blog/post/security', 'blog', path.resolve(root, 'blog/guide')])
  assert.equal(newCli.getAssetFolderName(dir, 'hello_world'), oldCli.getAssetFolderName(dir, 'hello_world'))
for (const name of ['blog/.vitepress/nav.yml', 'blog/.vitepress/sidebar.yml'])
  assert.equal(encode(yaml.load(source(name, false))), encode(yaml.load(source(name, true))))
process.stdout.write(`${JSON.stringify({ status: 'pass', base, transform_cases: transformCases, cli_argument_cases: argCases.length, asset_path_cases: 4, yaml_files: 2, limits: 'Public-function and data equivalence; not a browser or sandbox escape audit.' }, null, 2)}\n`)
