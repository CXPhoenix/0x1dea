import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import Electricity from '../Electricity.vue'

describe('Electricity.vue', () => {
  it('does not render overlay initially', () => {
    const wrapper = mount(Electricity)
    expect(wrapper.find('.electricity-overlay').exists()).toBe(false)
  })

  it('renders overlay when glitch is triggered', async () => {
    vi.useFakeTimers()
    const wrapper = mount(Electricity)
    
    // Default isDark is false, so color should be black
    // We can't easily trigger the random interval without mocking Math.random
    // Let's mock Math.random to return > 0.9 to trigger the glitch
    const randomSpy = vi.spyOn(Math, 'random').mockReturnValue(0.95)
    
    // Advance time by 5000ms to trigger interval
    vi.advanceTimersByTime(5000)
    await wrapper.vm.$nextTick()
    
    expect(wrapper.find('.electricity-overlay').exists()).toBe(true)
    
    // Advance time by 300ms to end glitch
    vi.advanceTimersByTime(300)
    await wrapper.vm.$nextTick()
    
    expect(wrapper.find('.electricity-overlay').exists()).toBe(false)
    
    randomSpy.mockRestore()
    vi.useRealTimers()
  })
})
