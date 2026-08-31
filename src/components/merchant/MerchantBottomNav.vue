<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()

const tabs = [
  { name: 'merchant-dashboard', label: 'Dashboard', icon: '▦', to: '/comerciante' },
  { name: 'merchant-new', label: 'Novo', icon: '＋', to: '/comerciante/novo' },
  { name: 'merchant-products', label: 'Produtos', icon: '📦', to: '/comerciante/produtos' },
  { name: 'merchant-orders', label: 'Pedidos', icon: '🧾', to: '/comerciante/pedidos' },
  { name: 'merchant-settings', label: 'Config', icon: '⚙️', to: '/comerciante/config' },
]
</script>

<template>
  <nav class="bottom-nav">
    <RouterLink
      v-for="tab in tabs"
      :key="tab.name"
      :to="tab.to"
      class="nav-item"
      :class="{ active: route.name === tab.name }"
    >
      <span class="nav-icon">{{ tab.icon }}</span>
      <span class="nav-label">{{ tab.label }}</span>
    </RouterLink>
  </nav>
</template>

<style scoped>
.bottom-nav {
  display: flex;
  justify-content: space-around;
  align-items: center;
  background: var(--mc-surface);
  border-top: 1px solid var(--mc-border);
  padding: 8px 4px calc(env(safe-area-inset-bottom, 0px) + 8px);
  flex-shrink: 0;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 6px 10px;
  border-radius: var(--cf-radius-sm);
  color: var(--mc-text-muted);
}

.nav-icon {
  font-size: 16px;
}

.nav-label {
  font-size: 10px;
  font-weight: 600;
}

.nav-item.active {
  color: var(--cf-pink);
}
</style>
