<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BottomNav from '@/components/BottomNav.vue'
import ShopService from '@/services/shop.service'
import { useCartStore } from '@/stores/useCartStore'

const props = defineProps({
  id: {
    type: String,
    required: true
  }
})

const router = useRouter()
const product = ref<any>(null)
const cartStore = useCartStore()
const { addToCart: addCartAction } = cartStore

onMounted(async () => {
  product.value = await ShopService.getProduct(props.id)
})

const addToCart = () => {
  addCartAction(product.value, 1)
  router.push('/carrinho')
}
</script>

<template>
  <div class="screen" v-if="product">
    <header class="product-header">
      <div class="product-image-large">
        <img v-if="product.image && (product.image.startsWith('/') || product.image.startsWith('http'))" :src="product.image.startsWith('http') ? product.image : `http://localhost:5000${product.image}`" class="real-image-large" />
        <span v-else class="emoji-img" v-html="product.image"></span>
      </div>
      <h1 class="product-title">{{ product.name }}</h1>
      <p class="product-store">{{ product.store }}</p>
      
      <div class="price-row">
        <span class="price">R${{ product.price.toFixed(2).replace('.', ',') }}</span>
        <span class="old-price">R${{ product.old_price.toFixed(2).replace('.', ',') }}</span>
      </div>

      <div class="tag-row">
        <span class="discount-tag">-50% OFF</span>
        <span class="expire-tag">{{ product.expires_in }}</span>
      </div>
    </header>

    <main class="content">
      <div class="details-table">
        <div class="detail-row">
          <span class="label">Validade</span>
          <span class="value pink">Confira na embalagem</span>
        </div>
        <div class="detail-row">
          <span class="label">Categoria</span>
          <span class="value">• {{ product.category }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Quantidade</span>
          <span class="value">{{ product.quantity }} unidades</span>
        </div>
        <div class="detail-row">
          <span class="label">Loja</span>
          <span class="value">{{ product.store }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Distância</span>
          <span class="value orange">{{ product.distance }}</span>
        </div>
      </div>

      <div class="reviews-section">
        <h3 class="section-title">Avaliações</h3>
        <div class="review-card">
          <div class="review-header">
            <div class="reviewer-avatar">MC</div>
            <span class="reviewer-name">Maria C.</span>
            <div class="stars">⭐⭐⭐⭐⭐</div>
          </div>
          <p class="review-text">Produto fresco, embalagem perfeita.<br/>Ótima economia!</p>
        </div>
      </div>

      <button class="add-button" @click="addToCart">Adicionar</button>
    </main>
    <BottomNav />
  </div>
</template>

<style scoped>
.screen {
  background-color: #ffffff;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.product-header {
  background: linear-gradient(to bottom, #f9b657, #f7d299);
  padding: 3rem 1.5rem 2rem 1.5rem;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
  text-align: center;
}

.product-image-large { font-size: 5rem; margin-bottom: 1rem; overflow: hidden; display: flex; align-items: center; justify-content: center; width: 140px; height: 140px; margin: 0 auto 1.5rem auto; border-radius: 20px; background: white; box-shadow: 0 8px 24px rgba(0,0,0,0.1); }
.real-image-large { width: 100%; height: 100%; object-fit: cover; border-radius: 20px; }

.product-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #333;
  margin: 0 0 0.3rem 0;
}

.product-store {
  font-size: 0.85rem;
  color: #5c3809;
  margin: 0 0 1rem 0;
}

.price-row {
  display: flex;
  justify-content: center;
  align-items: baseline;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.price {
  font-size: 2rem;
  font-weight: 800;
  color: #333;
}

.old-price {
  font-size: 1rem;
  color: #8c5b16;
  text-decoration: line-through;
}

.tag-row {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.discount-tag {
  background-color: #ff3b69;
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 800;
}

.expire-tag {
  background-color: white;
  color: #8c5b16;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 700;
}

.content {
  padding: 1.5rem;
  flex: 1;
  overflow-y: auto;
  padding-bottom: 100px;
}

.details-table {
  display: flex;
  flex-direction: column;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 1rem 0;
  border-bottom: 1px solid #f0f0f0;
  font-size: 0.9rem;
}

.detail-row:last-child {
  border-bottom: none;
}

.label {
  color: #888;
}

.value {
  font-weight: 700;
  color: #333;
}

.value.pink {
  color: #ff3b69;
}

.value.orange {
  color: #f5a623;
}

.reviews-section {
  margin-top: 2rem;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #333;
}

.review-card {
  border: 1px solid #f0dfb8;
  background-color: #fdf6e9;
  border-radius: 12px;
  padding: 1.2rem;
}

.review-header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 0.8rem;
}

.reviewer-avatar {
  background-color: #ff3b69;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.8rem;
}

.reviewer-name {
  font-weight: 700;
  font-size: 0.9rem;
  color: #333;
  flex: 1;
}

.stars {
  font-size: 0.7rem;
}

.review-text {
  font-size: 0.85rem;
  color: #666;
  line-height: 1.4;
  margin: 0;
}

.add-button {
  width: 100%;
  background-color: #f7b75e;
  color: #5c3809;
  padding: 1.2rem;
  border: none;
  border-radius: 20px;
  font-size: 1.1rem;
  font-weight: 800;
  margin-top: 2rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 15px rgba(247, 183, 94, 0.4);
}

.add-button:hover {
  background-color: #e6a245;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(247, 183, 94, 0.5);
}

.add-button:active {
  transform: translateY(0) scale(0.98);
}
</style>



