import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Particles from '../Particles.vue'

describe('Particles.vue', () => {
  const VueParticlesMock = {
    name: 'vue-particles',
    template: '<div class="vue-particles-stub"></div>',
    props: ['options']
  }

  it('renders vue-particles component', () => {
    const wrapper = mount(Particles, {
      global: {
        components: {
          'vue-particles': VueParticlesMock
        },
        stubs: {
          'ClientOnly': {
            template: '<slot />'
          }
        }
      }
    })
    
    expect(wrapper.findComponent({ name: 'vue-particles' }).exists()).toBe(true)
    expect(wrapper.find('.vue-particles-stub').exists()).toBe(true)
  })

  it('passes options to vue-particles', () => {
    const wrapper = mount(Particles, {
      global: {
        components: {
          'vue-particles': VueParticlesMock
        },
        stubs: {
          'ClientOnly': {
            template: '<slot />'
          }
        }
      }
    })
    
    const particlesComponent = wrapper.findComponent({ name: 'vue-particles' })
    expect(particlesComponent.exists()).toBe(true)
    
    const options = particlesComponent.props('options')
    expect(options).toBeDefined()
    // Verify specific option structure to match what's in the component
    expect(options.particles.move.enable).toBe(true)
  })
})
