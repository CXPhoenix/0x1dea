import { defineConfig, presetWind3 } from 'unocss'

// Match the preset already supplied by unocss/vite, now shared with ESLint.
export default defineConfig({
  presets: [presetWind3()],
})
