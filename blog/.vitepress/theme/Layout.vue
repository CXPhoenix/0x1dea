<script setup lang="ts">
import { useData } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import { computed } from 'vue'
import Particles from './components/Particles.vue'

const { Layout } = DefaultTheme
const { frontmatter } = useData()

const showParticleBg = computed(() => frontmatter.value.layout === 'home' || frontmatter.value.showParticle)
</script>

<template>
  <Layout>
    <template #layout-top>
      <div class="visual-effects-container pointer-events-none fixed inset-0 z-0">
        <Particles v-if="showParticleBg" />
      </div>
    </template>
  </Layout>
</template>

<style>
/* Global overrides or utility classes if needed */
</style>
