<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useData } from 'vitepress'

const { isDark } = useData()
const isGlitchActive = ref(false)

const triggerGlitch = () => {
  isGlitchActive.value = true
  setTimeout(() => {
    isGlitchActive.value = false
  }, 300)
}

const glitchColor = computed(() => isDark.value ? 'white' : 'black')

onMounted(() => {
  // Randomly trigger glitch every few seconds
  setInterval(() => {
    if (Math.random() > 0.9) {
      triggerGlitch()
    }
  }, 5000)
})
</script>

<template>
  <div v-if="isGlitchActive" class="electricity-overlay fixed inset-0 z-50 pointer-events-none mix-blend-overlay opacity-30">
    <div class="glitch-line" v-for="n in 5" :key="n" :style="{ top: Math.random() * 100 + '%', height: Math.random() * 5 + 'px', background: glitchColor }"></div>
  </div>
</template>

<style scoped>
.electricity-overlay {
  background: rgba(0, 255, 255, 0.05);
}

.glitch-line {
  position: absolute;
  left: 0;
  width: 100%;
  opacity: 0.8;
  box-shadow: 0 0 10px cyan;
}
</style>
