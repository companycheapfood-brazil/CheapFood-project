<script setup lang="ts">
import { ref, computed } from 'vue'
import { products } from '@/data/products'
import ProductCard from '@/components/ProductCard.vue'
import BottomNav from '@/components/BottomNav.vue'

const search = ref('')

const results = computed(() =>
  products.filter((p) => p.name.toLowerCase().includes(search.value.toLowerCase())),
)
</script>

<template>
  <div class="screen">
    <header class="header">
      <h1 class="title">Buscar</h1>
      <div class="search-bar">
        <input v-model="search" type="text" placeholder="Buscar produtos, lojas..." autofocus />
        <span class="search-icon">🔍</span>
      </div>
    </header>

    <main class="content">
      <div class="product-list">
        <ProductCard v-for="p in results" :key="p.id" :product="p" />
        <p v-if="results.length === 0" class="empty">Nenhum produto encontrado.</p>
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

.title {
  font-size: 17px;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 12px;
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
