import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import { h } from 'vue'
import EncoreTicket from '../blog/.vitepress/theme/components/EncoreTicket.vue'

describe('EncoreTicket related reading', () => {
  it('offers the authored recommendation as one native link', () => {
    const wrapper = mount(EncoreTicket, {
      props: {
        title: '什麼是安全？能吃嗎？',
        href: '/post/course/cybersec/what-is-safety',
        description: '如果平常怎麼運作都還不清楚，要怎麼發現哪裡出了問題呢？',
      },
    })

    expect(wrapper.attributes('href')).toBe('/post/course/cybersec/what-is-safety')
    expect(wrapper.text()).toContain('什麼是安全？能吃嗎？')
    expect(wrapper.text()).toContain('如果平常怎麼運作都還不清楚，要怎麼發現哪裡出了問題呢？')
    expect(wrapper.text()).toContain('來看這一篇')
    expect(wrapper.findAll('a')).toHaveLength(1)
    expect(wrapper.findAll('button, input')).toHaveLength(0)
    expect(wrapper.attributes('target')).toBeUndefined()
    wrapper.unmount()
  })

  it('reuses independent literal text and omits absent descriptions without an empty paragraph', () => {
    const wrapper = mount({
      render: () => h('section', [
        h(EncoreTicket, {
          title: '<img src=x onerror="alert(1)">',
          href: '/post/first',
          description: '<strong>這是文字</strong>',
        }),
        h(EncoreTicket, { title: '第二篇推薦', href: '/post/second' }),
      ]),
    })
    const links = wrapper.findAll('a')

    expect(links).toHaveLength(2)
    expect(links[0].attributes('href')).toBe('/post/first')
    expect(links[0].text()).toContain('<img src=x onerror="alert(1)">')
    expect(links[0].text()).toContain('<strong>這是文字</strong>')
    expect(links[0].findAll('img, strong')).toHaveLength(0)
    expect(links[1].attributes('href')).toBe('/post/second')
    expect(links[1].text()).toContain('第二篇推薦')
    expect(links[1].text()).toContain('來看這一篇')
    expect(links[1].findAll('p').some(paragraph => !paragraph.text().trim())).toBe(false)
    wrapper.unmount()
  })
})
