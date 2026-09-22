<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Product } from '@/types'
import { useCart } from '@/composables/useCart'

const props = defineProps<{ product: Product }>()
const router = useRouter()
const { addToCart } = useCart()

function openProduct() {
  router.push({ name: 'produto', params: { id: props.product.id } })
}

function quickAdd(event: MouseEvent) {
  event.stopPropagation()
  addToCart(props.product, 1)
}
</script>

<template>
  <div class="product-card" @click="openProduct">
    <div class="thumb">{{ product.image }}</div>

    <div class="info">
      <p class="name">{{ product.name }}</p>
      <p class="store">{{ product.store }}</p>
      <div class="price-row">
        <span class="price">R$ {{ product.price.toFixed(2).replace('.', ',') }}</span>
        <span v-if="product.old_price" class="original-price">
          R$ {{ product.old_price.toFixed(2).replace('.', ',') }}
        </span>
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
}

.thumb {
  width: 48px;
  height: 48px;
  border-radius: var(--cf-radius-sm);
  background: var(--cf-card-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  flex-shrink: 0;
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
</style>
