<script setup lang="ts">
import { ref, computed } from 'vue'
import { products } from '@/data/products'
import ProductCard from '@/components/ProductCard.vue'
import BottomNav from '@/components/BottomNav.vue'

const filters = ['Todos', 'Laticínios', 'Padaria', 'Hortifruti', 'Bebidas']
const activeFilter = ref('Todos')
const search = ref('')

const filteredProducts = computed(() => {
  return products.filter((p) => {
    const matchesFilter = activeFilter.value === 'Todos' || p.category === activeFilter.value
    const matchesSearch = p.name.toLowerCase().includes(search.value.toLowerCase())
    return matchesFilter && matchesSearch
  })
})
</script>

<template>
  <div class="screen">
    <header class="header">
      <h1 class="logo">🛒 Cheap<span class="logo-accent">Food</span></h1>
      <div class="search-bar">
        <input v-model="search" type="text" placeholder="Buscar produtos, lojas..." />
        <span class="search-icon">🔍</span>
      </div>
    </header>

    <main class="content">
      <section class="promo-banner">
        <div>
          <p class="promo-title">Até 70% OFF</p>
          <p class="promo-subtitle">em laticínios</p>
          <p class="promo-store">Supermercado Bom Preço · Centro</p>
        </div>
        <span class="promo-icon">🥛</span>
      </section>

      <div class="filters">
        <button
          v-for="f in filters"
          :key="f"
          class="filter-chip"
          :class="{ active: activeFilter === f }"
          @click="activeFilter = f"
        >
          {{ f }}
        </button>
      </div>

      <div class="section-title-row">
        <p class="section-title">Perto de vencer ⏳</p>
        <RouterLink to="/buscar" class="see-all">Ver todos</RouterLink>
      </div>

      <div class="product-list">
        <ProductCard v-for="p in filteredProducts" :key="p.id" :product="p" />
        <p v-if="filteredProducts.length === 0" class="empty">Nenhum produto encontrado.</p>
      </div>
    </main>

    <BottomNav />
  </div>
</template>

<style scoped>
.screen {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--cf-bg);
}

.header {
  background: var(--cf-orange);
  padding: 18px 16px 16px;
  border-radius: 0 0 var(--cf-radius-lg) var(--cf-radius-lg);
  flex-shrink: 0;
}

.logo {
  font-size: 18px;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 12px;
}

.logo-accent {
  color: var(--cf-pink);
}

.search-bar {
  position: relative;
  background: rgba(0, 0, 0, 0.15);
  border-radius: var(--cf-radius-sm);
  display: flex;
  align-items: center;
}

.search-bar input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  padding: 11px 40px 11px 14px;
  font-size: 13px;
  color: #1a1a1a;
}

.search-bar input::placeholder {
  color: rgba(26, 26, 26, 0.55);
}

.search-icon {
  position: absolute;
  right: 12px;
  font-size: 14px;
}

.content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.promo-banner {
  background: var(--cf-card);
  border: 1px solid var(--cf-border);
  border-radius: var(--cf-radius-md);
  padding: 14px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.promo-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--cf-orange-soft);
}

.promo-subtitle {
  font-size: 13px;
  color: var(--cf-text);
  margin-top: 2px;
}

.promo-store {
  font-size: 11px;
  color: var(--cf-text-muted);
  margin-top: 4px;
}

.promo-icon {
  font-size: 28px;
}

.filters {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 4px;
  margin-bottom: 18px;
}

.filter-chip {
  flex-shrink: 0;
  background: var(--cf-card);
  border: 1px solid var(--cf-border);
  color: var(--cf-text-muted);
  font-size: 12px;
  font-weight: 600;
  padding: 8px 14px;
  border-radius: 999px;
  white-space: nowrap;
}

.filter-chip.active {
  background: var(--cf-orange);
  border-color: var(--cf-orange);
  color: #1a1a1a;
}

.section-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.section-title {
  font-size: 14px;
  font-weight: 700;
}

.see-all {
  font-size: 12px;
  color: var(--cf-pink);
  font-weight: 600;
}

.product-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.empty {
  color: var(--cf-text-muted);
  font-size: 13px;
  text-align: center;
  padding: 24px 0;
}
</style>
