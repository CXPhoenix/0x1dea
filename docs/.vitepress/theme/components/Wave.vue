<script setup lang="ts">
import { useData } from 'vitepress'

const { isDark } = useData()
</script>

<template>
  <div class="wave-container fixed bottom-0 left-0 w-full z-0 pointer-events-none overflow-hidden">
    <svg class="waves" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
    viewBox="0 24 150 28" preserveAspectRatio="none" shape-rendering="auto">
    <defs>
    <path id="gentle-wave" d="M-160 44c30 0 58-18 88-18s 58 18 88 18 58-18 88-18 58 18 88 18 v44h-352z" />
    </defs>
    <g class="parallax">
    <use xlink:href="#gentle-wave" x="48" y="0" :fill="isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)'" />
    <use xlink:href="#gentle-wave" x="48" y="3" :fill="isDark ? 'rgba(255,255,255,0.03)' : 'rgba(0,0,0,0.03)'" />
    <use xlink:href="#gentle-wave" x="48" y="5" :fill="isDark ? 'rgba(255,255,255,0.01)' : 'rgba(0,0,0,0.01)'" />
    </g>
    </svg>
  </div>
</template>

<style scoped>
.waves {
  width: 100%;
  height: 100px;
  min-height: 100px;
}

.parallax > use {
  animation: move-forever 25s cubic-bezier(.55,.5,.45,.5) infinite;
}
.parallax > use:nth-child(1) {
  animation-delay: -2s;
  animation-duration: 7s;
}
.parallax > use:nth-child(2) {
  animation-delay: -3s;
  animation-duration: 10s;
}
.parallax > use:nth-child(3) {
  animation-delay: -4s;
  animation-duration: 13s;
}
@keyframes move-forever {
  0% {
   transform: translate3d(-90px,0,0);
  }
  100% { 
    transform: translate3d(85px,0,0);
  }
}
</style>
