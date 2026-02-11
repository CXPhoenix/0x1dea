<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import { useData } from 'vitepress'
import Particles from './components/Particles.vue'
import Wave from './components/Wave.vue'
import Electricity from './components/Electricity.vue'

const { Layout } = DefaultTheme
const { isDark } = useData()
</script>

<template>
  <Layout>
    <template #layout-top>
      <div class="visual-effects-container fixed inset-0 z-0 pointer-events-none">
        <Particles />
        <Wave />
        <!-- <Electricity /> -->
      </div>
    </template>
  </Layout>
</template>

<style>
/* Global overrides or utility classes if needed */
</style>
