<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useCartStore } from '@/stores/useCartStore'
import { storeToRefs } from 'pinia'

const route = useRoute()
const cartStore = useCartStore()
const { totalItems } = storeToRefs(cartStore)

const tabs = [
  { name: 'home', label: 'Início', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>', to: '/' },
  { name: 'buscar', label: 'Buscar', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>', to: '/buscar' },
  { name: 'carrinho', label: 'Carrinho', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg>', to: '/carrinho' },
  { name: 'perfil', label: 'Perfil', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>', to: '/perfil' },
]
</script>

<template>
  <nav class="bottom-nav">
    <RouterLink
      v-for="tab in tabs"
      :key="tab.name"
      :to="tab.to"
      :aria-label="tab.label"
      class="nav-item"
      :class="{ active: route.name === tab.name || (tab.name === 'home' && route.name === 'produto') || (tab.name === 'carrinho' && route.name === 'comprovante') }"
    >
      <span class="nav-icon-wrap">
        <span class="nav-icon" v-html="tab.svg"></span>
        <span v-if="tab.name === 'carrinho' && totalItems > 0" class="nav-badge">
          {{ totalItems }}
        </span>
      </span>
      <span class="nav-label">{{ tab.label }}</span>
    </RouterLink>
  </nav>
</template>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  align-items: center;
  background: var(--cf-bg-elevated);
  border-top: 1px solid var(--cf-border);
  padding: 8px 4px calc(env(safe-area-inset-bottom, 0px) + 8px);
  z-index: 1000;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 6px 14px;
  border-radius: var(--cf-radius-sm);
  color: var(--cf-text-faint);
  transition: color 0.15s ease;
}

.nav-icon-wrap {
  position: relative;
  display: inline-flex;
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  opacity: 0.6;
}

.nav-badge {
  position: absolute;
  top: -6px;
  right: -8px;
  background: var(--cf-pink);
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  line-height: 1;
  padding: 2px 5px;
  border-radius: 999px;
  min-width: 16px;
  text-align: center;
}

.nav-label {
  font-size: 11px;
  font-weight: 500;
}

.nav-item.active {
  color: var(--cf-pink);
}

.nav-item.active .nav-icon {
  opacity: 1;
}
</style>
