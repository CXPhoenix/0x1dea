import antfu from '@antfu/eslint-config'

export default antfu({
  // Enable Vue support
  vue: true,

  // Enable UnoCSS support
  unocss: true,

  // Enable Markdown support
  markdown: true,

  // explicit tsconfig
  typescript: {
    tsconfigPath: 'tsconfig.json',
  },

  // Custom rules if needed
  rules: {
    // 'no-console': 'warn',
  },
})
