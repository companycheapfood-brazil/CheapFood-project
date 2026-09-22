<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useCart } from '@/composables/useCart'

const route = useRoute()
const { totalItems } = useCart()

const tabs = [
  { name: 'home', label: 'Início', icon: '🏠', to: '/' },
  { name: 'buscar', label: 'Buscar', icon: '🔍', to: '/buscar' },
  { name: 'carrinho', label: 'Carrinho', icon: '🛒', to: '/carrinho' },
  { name: 'perfil', label: 'Perfil', icon: '👤', to: '/perfil' },
]
</script>

<template>
  <nav class="bottom-nav">
    <RouterLink
      v-for="tab in tabs"
      :key="tab.name"
      :to="tab.to"
      class="nav-item"
      :class="{ active: route.name === tab.name || (tab.name === 'home' && route.name === 'produto') || (tab.name === 'carrinho' && route.name === 'comprovante') }"
    >
      <span class="nav-icon-wrap">
        <span class="nav-icon">{{ tab.icon }}</span>
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
  display: flex;
  justify-content: space-around;
  align-items: center;
  background: var(--cf-bg-elevated);
  border-top: 1px solid var(--cf-border);
  padding: 8px 4px calc(env(safe-area-inset-bottom, 0px) + 8px);
  flex-shrink: 0;
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
  font-size: 18px;
  filter: grayscale(1);
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
  filter: none;
  opacity: 1;
}
</style>
