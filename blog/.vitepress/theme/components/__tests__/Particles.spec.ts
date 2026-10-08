import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'
import Particles from '../Particles.vue'

// Mock vitepress useData
vi.mock('vitepress', () => ({
  useData: () => ({
    isDark: { value: false },
  }),
}))

describe('particles.vue', () => {
  const VueParticlesMock = {
    name: 'vue-particles',
    template: '<div class="vue-particles-stub"></div>',
    props: ['options'],
  }

  it('renders vue-particles component', () => {
    const wrapper = mount(Particles, {
      global: {
        components: {
          'vue-particles': VueParticlesMock,
        },
        stubs: {
          ClientOnly: {
            template: '<slot />',
          },
        },
      },
    })

    expect(wrapper.findComponent({ name: 'vue-particles' }).exists()).toBe(true)
    expect(wrapper.find('.vue-particles-stub').exists()).toBe(true)
  })

  it('passes options to vue-particles', () => {
    const wrapper = mount(Particles, {
      global: {
        components: {
          'vue-particles': VueParticlesMock,
        },
        stubs: {
          ClientOnly: {
            template: '<slot />',
          },
        },
      },
    })

    const particlesComponent = wrapper.findComponent({ name: 'vue-particles' })
    expect(particlesComponent.exists()).toBe(true)

    const options = particlesComponent.props('options') as { particles: { move: { enable: boolean } } }
    expect(options).toBeDefined()
    // Verify specific option structure to match what's in the component
    expect(options.particles.move.enable).toBe(true)
  })
})
