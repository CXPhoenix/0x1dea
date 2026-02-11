<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import { useData } from 'vitepress'
import Particles from './components/Particles.vue'

const { Layout } = DefaultTheme
</script>

<template>
  <Layout>
    <template #layout-top>
      <div class="visual-effects-container fixed inset-0 z-0 pointer-events-none">
        <Particles />
      </div>
    </template>
  </Layout>
</template>

<style>
/* Global overrides or utility classes if needed */
</style>
