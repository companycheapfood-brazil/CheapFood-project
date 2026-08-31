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
    <div class="thumb">{{ product.icon }}</div>

    <div class="info">
      <p class="name">{{ product.name }}</p>
      <p class="store">{{ product.store }}</p>
      <div class="price-row">
        <span class="price">R$ {{ product.price.toFixed(2).replace('.', ',') }}</span>
        <span v-if="product.originalPrice" class="original-price">
          R$ {{ product.originalPrice.toFixed(2).replace('.', ',') }}
        </span>
      </div>
      <span v-if="product.expiresLabel" class="expires-badge">{{ product.expiresLabel }}</span>
    </div>

    <button class="add-btn" @click="quickAdd">+</button>
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
  width: 30px;
  height: 30px;
  border-radius: 999px;
  border: none;
  background: var(--cf-orange);
  color: #1a1a1a;
  font-size: 18px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
</style>
