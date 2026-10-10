<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{ variant?: string, title?: string }>(), {
  variant: 'note',
  title: 'TL;DR',
})

const variant = computed(() => ['note', 'cards', 'terminal'].includes(props.variant) ? props.variant : 'note')
const title = computed(() => props.title.trim() || 'TL;DR')
</script>

<template>
  <aside :class="[$style.summary, $style[variant]]" role="note" :aria-label="title">
    <header v-if="variant === 'terminal'" :class="[$style.title, $style.windowTitle]">
      {{ title }}
    </header>
    <p v-else :class="$style.title">
      {{ title }}
    </p>
    <div :class="$style.body">
      <slot />
    </div>
  </aside>
</template>

<style module>
.summary {
  --summary-bg: #f0f8f4;
  --summary-text: #243e36;
  --summary-border: #b4d4c4;
  --summary-accent: #386f58;
  --summary-code: #dfece4;
  margin: 1.5rem 0;
  border: 1px solid var(--summary-border);
  border-radius: 12px;
  padding: 1.1rem 1.25rem;
  background: var(--summary-bg);
  color: var(--summary-text);
  overflow-wrap: anywhere;
}

.note {
  border-inline-start: 4px solid var(--summary-accent);
}

.summary .title {
  margin: 0 0 0.75rem;
  color: inherit;
  font-size: 0.9rem;
  font-weight: 700;
  line-height: 1.5;
  letter-spacing: 0.04em;
}

.body,
.summary .body :global(p:not(.custom-block *)),
.summary .body :global(ul:not(.custom-block *)),
.summary .body :global(ol:not(.custom-block *)),
.summary .body :global(li:not(.custom-block *)) {
  color: inherit;
  font-size: 1rem;
  line-height: 1.75;
}

.summary .body :global(p:not(.custom-block *)),
.summary .body :global(ul:not(.custom-block *)),
.summary .body :global(ol:not(.custom-block *)) {
  margin: 0.6rem 0;
}

.body > :first-child {
  margin-top: 0;
}

.body > :last-child {
  margin-bottom: 0;
}

.body :global(ul:not(.custom-block *)),
.body :global(ol:not(.custom-block *)) {
  padding-inline-start: 1.2rem;
}

.body :global(li:not(.custom-block *)) + :global(li:not(.custom-block *)) {
  margin-top: 0.45rem;
}

.body :global(a:not(.custom-block *)) {
  color: inherit;
  text-decoration: underline;
  text-underline-offset: 0.15em;
  overflow-wrap: anywhere;
}

.summary .body :global(:not(pre) > code:not(.custom-block *)) {
  border-radius: 4px;
  padding: 0.1em 0.25em;
  background: var(--summary-code);
  color: inherit;
  font-size: 0.92em;
  white-space: break-spaces;
  overflow-wrap: anywhere;
}

.body :global(strong:not(.custom-block *)) {
  font-size: inherit;
}

.cards {
  --summary-bg: #f4f8fc;
  --summary-text: #243d50;
  --summary-border: #bdd0df;
  --summary-accent: #3b6787;
  --summary-code: #e4edf4;
}

.cards .body > :global(ul:not(.custom-block *)),
.cards .body > :global(ol:not(.custom-block *)) {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.75rem;
  padding: 0;
}

.cards .body > :global(ul:not(.custom-block *)) > :global(li:not(.custom-block *)),
.cards .body > :global(ol:not(.custom-block *)) > :global(li:not(.custom-block *)) {
  min-width: 0;
  margin: 0;
  border: 1px solid var(--summary-border);
  border-radius: 8px;
  padding: 0.8rem 0.9rem;
  background: var(--vp-c-bg, #fff);
}

.cards .body > :global(ul:not(.custom-block *)) > :global(li:not(.custom-block *))::marker {
  color: transparent;
}

.cards .body > :global(ol:not(.custom-block *)) {
  padding-inline-start: 1.2rem;
}

.cards .body > :global(ul:not(.custom-block *)) > :global(li:not(.custom-block *))::before {
  display: block;
  width: 24px;
  height: 24px;
  margin-bottom: 0.6rem;
  background: var(--summary-accent);
  content: '';
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='9' fill='none' stroke='black' stroke-width='1.6'/%3E%3Cpath d='M12 6v6l4 2' fill='none' stroke='black' stroke-width='1.6'/%3E%3C/svg%3E") center / contain no-repeat;
}

.cards .body > :global(ul:not(.custom-block *)) > :global(li:not(.custom-block *)):nth-child(2)::before {
  mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M3 17h4l3-10 4 12 3-7 4 1' fill='none' stroke='black' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
}

.cards .body > :global(ul:not(.custom-block *)) > :global(li:not(.custom-block *)):nth-child(3)::before {
  mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='m3 8 9-5 9 5-9 5-9-5Zm0 5 9 5 9-5M3 18l9 5 9-5' fill='none' stroke='black' stroke-width='1.6' stroke-linejoin='round'/%3E%3C/svg%3E");
}

.terminal {
  --summary-bg: #101c2a;
  --summary-text: #e8eff5;
  --summary-border: #405266;
  --summary-accent: #8edbc6;
  --summary-code: #233344;
}

.terminal {
  padding: 0;
}

.terminal .windowTitle {
  margin: 0;
  border-bottom: 1px solid var(--summary-border);
  border-radius: 11px 11px 0 0;
  padding: 0.65rem 1.25rem;
  background: var(--summary-code);
}

.terminal .body {
  padding: 1.1rem 1.25rem;
}

.terminal .body > :global(ul:not(.custom-block *)) {
  list-style: none;
  padding-inline-start: 0;
}

.terminal .body > :global(ul:not(.custom-block *)) > :global(li:not(.custom-block *)) {
  position: relative;
  padding-inline-start: 1.5rem;
}

.terminal .body > :global(ul:not(.custom-block *)) > :global(li:not(.custom-block *))::before {
  position: absolute;
  inset-inline-start: 0;
  top: 0.3em;
  width: 1em;
  height: 1.2em;
  background: var(--summary-accent);
  content: '';
  mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 20'%3E%3Ctext x='1' y='16' font-family='monospace' font-size='19' fill='black'%3E%24%3C/text%3E%3C/svg%3E") center / contain no-repeat;
}

.terminal .title {
  color: var(--summary-accent);
  font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
}

:global(.dark) .note {
  --summary-bg: #192f28;
  --summary-text: #e3eee7;
  --summary-border: #49695b;
  --summary-accent: #9bcbb6;
  --summary-code: #2a4336;
}

:global(.dark) .cards {
  --summary-bg: #1a2b37;
  --summary-text: #e0eaf2;
  --summary-border: #4b6579;
  --summary-accent: #a1c7e3;
  --summary-code: #2d4252;
}

@media (max-width: 700px) {
  .summary,
  :global(.dark) .summary {
    padding: 1rem;
  }

  .cards .body > :global(ul:not(.custom-block *)),
  .cards .body > :global(ol:not(.custom-block *)) {
    grid-template-columns: 1fr;
  }

  .terminal,
  :global(.dark) .terminal {
    padding: 0;
  }

  .terminal .body {
    padding: 1rem;
  }
}

@media print {
  .summary,
  :global(.dark) .summary {
    --summary-bg: #fff;
    --summary-text: #111;
    --summary-border: #777;
    --summary-accent: #333;
    --summary-code: #eee;
    break-inside: avoid;
  }

  .cards .body > :global(ul:not(.custom-block *)),
  .cards .body > :global(ol:not(.custom-block *)) {
    grid-template-columns: 1fr;
  }

  .terminal .windowTitle,
  .cards .body > :global(ul:not(.custom-block *)) > :global(li:not(.custom-block *)),
  .cards .body > :global(ol:not(.custom-block *)) > :global(li:not(.custom-block *)) {
    background: #fff;
  }
}
</style>
