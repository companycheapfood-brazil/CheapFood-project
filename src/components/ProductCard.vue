<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Product } from '@/types'
import { useCartStore } from '@/stores/useCartStore'

const props = defineProps<{ product: Product }>()
const router = useRouter()
const cartStore = useCartStore()
const { addToCart } = cartStore

function openProduct() {
  router.push({ name: 'produto', params: { id: props.product.id } })
}

function quickAdd(event: MouseEvent) {
  event.stopPropagation()
  addToCart(props.product, 1)
}

import { useFavoritesStore } from '@/stores/useFavoritesStore'
const favoritesStore = useFavoritesStore()
</script>

<template>
  <div class="product-card" @click="openProduct">
    <div class="thumb">
      <img v-if="product.image && (product.image.startsWith('/') || product.image.startsWith('http'))" :src="product.image.startsWith('http') ? product.image : `http://localhost:5000${product.image}`" class="real-image" />
      <span v-else v-html="product.image"></span>
    </div>

    <div class="info">
      <p class="name">{{ product.name }}</p>
      <p class="store">{{ product.store }}</p>
      <div class="price-row" style="display:flex; justify-content:space-between; align-items:center; width: 100%">
        <div>
          <span class="price">R$ {{ product.price.toFixed(2).replace('.', ',') }}</span>
          <span v-if="product.old_price" class="original-price">
            R$ {{ product.old_price.toFixed(2).replace('.', ',') }}
          </span>
        </div>
        <button class="fav-btn" @click.stop="favoritesStore.toggleFavorite(product.id)">
          <svg v-if="favoritesStore.isFavorite(product.id)" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="#FF3B69" stroke="#FF3B69" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#bfa47a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
        </button>
      </div>
      <span v-if="product.expires_in" class="expires-badge">{{ product.expires_in }}</span>
    </div>

    <button class="add-btn" @click="quickAdd">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="12" y1="5" x2="12" y2="19"></line>
        <line x1="5" y1="12" x2="19" y2="12"></line>
      </svg>
    </button>
  </div>
</template>

<style scoped>
.product-card {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--cf-card);
  border-radius: var(--cf-radius-md);
  padding: 12px;
  position: relative;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.product-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.thumb {
  width: 48px;
  min-width: 48px;
  height: 48px;
  flex-shrink: 0;
  overflow: hidden;
  border-radius: var(--cf-radius-sm);
  background: var(--cf-card-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  flex-shrink: 0;
  overflow: hidden;
  overflow: hidden;
}

.real-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.info {
  flex: 1;
  min-width: 0;
}

.name {
  font-size: 14px;
  font-weight: 600;
  color: var(--cf-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.store {
  font-size: 11px;
  color: var(--cf-text-muted);
  margin-top: 2px;
}

.price-row {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin-top: 4px;
}

.price {
  font-size: 15px;
  font-weight: 700;
  color: var(--cf-orange-soft);
}

.original-price {
  font-size: 11px;
  color: var(--cf-text-faint);
  text-decoration: line-through;
}

.expires-badge {
  display: inline-block;
  margin-top: 6px;
  font-size: 10px;
  font-weight: 600;
  color: #fff;
  background: var(--cf-pink);
  padding: 2px 8px;
  border-radius: 999px;
}

.add-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background-color: #ff3b69;
  color: white;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 4px 10px rgba(255, 59, 105, 0.3);
}

.add-btn:hover {
  background-color: #e0335c;
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 6px 15px rgba(255, 59, 105, 0.45);
}

.add-btn:active {
  transform: translateY(0) scale(0.95);
  box-shadow: 0 2px 5px rgba(255, 59, 105, 0.3);
}

.price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.fav-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s;
}
.fav-btn:active {
  transform: scale(0.8);
}

</style>

