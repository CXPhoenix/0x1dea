<script setup lang="ts">
import { computed } from 'vue'
import { useData } from 'vitepress'

const { isDark } = useData()

const color = computed(() => isDark.value ? '#ffffff' : '#000000')
const linksColor = computed(() => isDark.value ? '#ffffff' : '#000000')

const options = computed(() => ({
  fullScreen: {
    enable: true,
    zIndex: 0
  },
  background: {
    color: {
      value: 'transparent'
    }
  },
  fpsLimit: 120,
  interactivity: {
    events: {
      onClick: {
        enable: false,
        mode: 'push'
      },
      onHover: {
        enable: false,
        mode: 'repulse'
      },
      resize: {
        enable: true
      }
    },
    modes: {
      push: {
        quantity: 4
      },
      repulse: {
        distance: 200,
        duration: 0.4
      }
    }
  },
  particles: {
    color: {
      value: color.value
    },
    links: {
      color: linksColor.value,
      distance: 150,
      enable: true,
      opacity: 0.1,
      width: 1
    },
    move: {
      direction: 'none',
      enable: true,
      outModes: 'bounce',
      random: false,
      speed: 1,
      straight: false
    },
    number: {
      density: {
        enable: true,
        height: 800,
        width: 800
      },
      value: 80
    },
    opacity: {
      value: 0.2
    },
    shape: {
      type: 'circle'
    },
    size: {
      value: { min: 1, max: 5 }
    }
  },
  detectRetina: true
}))
</script>

<template>
  <ClientOnly>
    <vue-particles
      id="tsparticles"
      :options="options"
      class="fixed inset-0 z-0 pointer-events-none opacity-60"
    />
  </ClientOnly>
</template>

<style scoped>
/* No specific styles needed as vue-particles handles canvas */
</style>
