<script setup lang="ts">
defineProps<{
  title: string
  href: string
  description?: string
}>()
</script>

<template>
  <a :href="href" :class="$style.ticket">
    <span :class="$style.stub">
      <span :class="$style.stubTitle">同場加映</span>
      <span :class="$style.encore" aria-hidden="true">ENCORE</span>
    </span>
    <div :class="$style.body">
      <p :class="$style.eyebrow">延伸閱讀</p>
      <p :class="$style.title">{{ title }}</p>
      <p v-if="description" :class="$style.description">{{ description }}</p>
      <span :class="$style.action">來看這一篇 <span :class="$style.arrow" aria-hidden="true">→</span></span>
    </div>
  </a>
</template>

<style module>
.ticket,
:global(.vp-doc) .ticket {
  --stub-width: 4.1rem;
  position: relative;
  display: grid;
  grid-template-columns: var(--stub-width) minmax(0, 1fr);
  max-width: 100%;
  margin: 1.6rem 0;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  font-weight: 400;
  text-decoration: none;
  overflow-wrap: anywhere;
  transition: border-color 160ms ease;
}

.ticket:hover,
:global(.vp-doc) .ticket:hover {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-text-1);
  text-decoration: none;
}

.ticket:focus-visible {
  outline: 3px solid var(--vp-c-brand-1);
  outline-offset: 5px;
}

.ticket::before,
.ticket::after {
  position: absolute;
  inset-inline-start: calc(var(--stub-width) - 8px);
  width: 16px;
  height: 16px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 50%;
  background: var(--vp-c-bg);
  content: '';
  pointer-events: none;
}

.ticket::before {
  top: -9px;
  clip-path: inset(8px 0 0);
}

.ticket::after {
  bottom: -9px;
  clip-path: inset(0 0 8px);
}

.stub {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  border-inline-end: 1px dashed var(--vp-c-divider);
  padding: 0.9rem 0.5rem;
  color: var(--vp-c-brand-1);
}

.stubTitle {
  font-size: 1.1rem;
  font-weight: 700;
  line-height: 1.25;
  letter-spacing: 0.12em;
  writing-mode: vertical-rl;
  text-orientation: upright;
}

.encore {
  font-family: var(--vp-font-family-mono);
  font-size: 0.45rem;
  line-height: 1.5;
  letter-spacing: 0.08em;
}

.body {
  min-width: 0;
  padding: 1.15rem 1.2rem;
  text-wrap: pretty;
}

.ticket .eyebrow {
  margin: 0 0 0.35rem;
  color: var(--vp-c-text-2);
  font-size: 0.6rem;
  font-weight: 600;
  line-height: 1.5;
  letter-spacing: 0.08em;
}

.ticket .title {
  margin: 0 0 0.45rem;
  color: var(--vp-c-text-1);
  font-size: 1.1rem;
  font-weight: 700;
  line-height: 1.5;
  letter-spacing: -0.025em;
}

.ticket .description {
  margin: 0 0 0.75rem;
  color: var(--vp-c-text-2);
  font-size: 0.8rem;
  line-height: 1.8;
}

.action {
  display: inline-block;
  border-radius: 4px;
  padding: 0.35rem 0.6rem;
  background: var(--vp-c-brand-3);
  color: var(--vp-c-white);
  font-size: 0.65rem;
  font-weight: 600;
  line-height: 1.6;
}

.arrow {
  display: inline-block;
  transition: transform 160ms ease;
}

.ticket:hover .arrow {
  transform: translateX(3px);
}

@media (max-width: 600px) {
  .ticket,
  :global(.vp-doc) .ticket {
    --stub-width: 2.9rem;
  }

  .stubTitle {
    font-size: 0.95rem;
  }

  .body {
    padding: 1rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .ticket,
  .arrow {
    transition: none;
  }
}
</style>
