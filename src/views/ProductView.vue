<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { getProductById } from '@/data/products'
import { useCart } from '@/composables/useCart'
import BottomNav from '@/components/BottomNav.vue'

const props = defineProps<{ id: string }>()
const router = useRouter()
const { addToCart } = useCart()

const product = computed(() => getProductById(props.id))

function handleAdd() {
  if (!product.value) return
  addToCart(product.value, 1)
  router.push('/carrinho')
}

function stars(rating: number) {
  return '★'.repeat(rating) + '☆'.repeat(5 - rating)
}
</script>

<template>
  <div v-if="product" class="screen">
    <header class="header">
      <button class="back-btn" @click="router.back()">←</button>
    </header>

    <main class="content">
      <div class="hero">
        <span class="hero-icon">{{ product.icon }}</span>
      </div>

      <div class="title-row">
        <div>
          <h1 class="name">{{ product.name }}</h1>
          <div class="price-row">
            <span class="price">R$ {{ product.price.toFixed(2).replace('.', ',') }}</span>
            <span v-if="product.originalPrice" class="original-price">
              R$ {{ product.originalPrice.toFixed(2).replace('.', ',') }}
            </span>
          </div>
        </div>
        <div class="badges">
          <span v-if="product.discountLabel" class="discount-badge">{{
            product.discountLabel
          }}</span>
          <span v-if="product.expiresLabel" class="expires-badge">{{
            product.expiresLabel
          }}</span>
        </div>
      </div>

      <section class="details-card">
        <div class="detail-row">
          <span class="detail-label">Validade</span>
          <span class="detail-value">{{ product.validity }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Categoria</span>
          <span class="detail-value">🏷️ {{ product.category }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Quantidade</span>
          <span class="detail-value">{{ product.quantityLabel }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Loja</span>
          <span class="detail-value">{{ product.store }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Distância</span>
          <span class="detail-value">{{ product.distance }}</span>
        </div>
      </section>

      <section class="reviews">
        <p class="section-title">Avaliações</p>
        <div v-for="(review, i) in product.reviews" :key="i" class="review-card">
          <div class="avatar">{{ review.authorInitials }}</div>
          <div class="review-body">
            <div class="review-head">
              <span class="review-name">{{ review.authorName }}</span>
              <span class="review-stars">{{ stars(review.rating) }}</span>
            </div>
            <p class="review-comment">{{ review.comment }}</p>
          </div>
        </div>
      </section>
    </main>

    <div class="footer">
      <button class="add-btn" @click="handleAdd">Adicionar</button>
    </div>

    <BottomNav />
  </div>

  <div v-else class="screen not-found">
    <p>Produto não encontrado.</p>
    <RouterLink to="/">Voltar para a home</RouterLink>
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
  padding: 16px;
  border-radius: 0 0 var(--cf-radius-lg) var(--cf-radius-lg);
  flex-shrink: 0;
}

.back-btn {
  width: 32px;
  height: 32px;
  border-radius: 999px;
  border: none;
  background: rgba(0, 0, 0, 0.15);
  color: #1a1a1a;
  font-size: 16px;
}

.content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.hero {
  background: var(--cf-card);
  border-radius: var(--cf-radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 0;
  margin-bottom: 16px;
}

.hero-icon {
  font-size: 56px;
}

.title-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 18px;
  gap: 12px;
}

.name {
  font-size: 18px;
  font-weight: 700;
}

.price-row {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-top: 6px;
}

.price {
  font-size: 20px;
  font-weight: 800;
  color: var(--cf-orange-soft);
}

.original-price {
  font-size: 13px;
  color: var(--cf-text-faint);
  text-decoration: line-through;
}

.badges {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
}

.discount-badge {
  font-size: 10px;
  font-weight: 700;
  color: #fff;
  background: var(--cf-pink);
  padding: 3px 8px;
  border-radius: 999px;
  white-space: nowrap;
}

.expires-badge {
  font-size: 10px;
  font-weight: 600;
  color: var(--cf-text-muted);
}

.details-card {
  background: var(--cf-card);
  border-radius: var(--cf-radius-md);
  padding: 6px 16px;
  margin-bottom: 20px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid var(--cf-border);
  font-size: 13px;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  color: var(--cf-text-muted);
}

.detail-value {
  font-weight: 600;
}

.section-title {
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 10px;
}

.review-card {
  display: flex;
  gap: 10px;
  background: var(--cf-card);
  border-radius: var(--cf-radius-md);
  padding: 12px;
}

.avatar {
  width: 34px;
  height: 34px;
  border-radius: 999px;
  background: var(--cf-orange);
  color: #1a1a1a;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.review-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.review-name {
  font-size: 13px;
  font-weight: 600;
}

.review-stars {
  font-size: 11px;
  color: var(--cf-orange-soft);
}

.review-comment {
  font-size: 12px;
  color: var(--cf-text-muted);
  margin-top: 4px;
}

.footer {
  padding: 12px 16px 16px;
  flex-shrink: 0;
}

.add-btn {
  width: 100%;
  background: var(--cf-orange);
  color: #1a1a1a;
  border: none;
  border-radius: var(--cf-radius-sm);
  padding: 15px;
  font-size: 14px;
  font-weight: 700;
}

.not-found {
  align-items: center;
  justify-content: center;
  gap: 12px;
  text-align: center;
}
</style>
