<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import BottomNav from '@/components/BottomNav.vue'
import ShopService from '@/services/shop.service'
import { useCartStore } from '@/stores/useCartStore'
import { useFavoritesStore } from '@/stores/useFavoritesStore'

const router = useRouter()
const cartStore = useCartStore()
const favoritesStore = useFavoritesStore()
const { addToCart: addCartAction } = cartStore

const search = ref('')
const activeFilter = ref('Todos')
const filters = [
  { name: 'Todos', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>' },
  { name: 'Laticínios', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2v20"/><path d="M18 2v20"/><path d="M6 12h12"/><path d="M6 6h12"/><path d="M6 18h12"/></svg>' },
  { name: 'Padaria', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m4.6 13.4-.6 1.5c-.7 1.9.1 3.9 1.8 5.1l.3.2c1.7 1.1 4 .8 5.4-.8l.8-.9c.7-.8 1.9-.8 2.6 0l.8.9c1.4 1.6 3.7 1.9 5.4.8l.3-.2c1.7-1.2 2.5-3.2 1.8-5.1l-.6-1.5"/><path d="M10.5 8.5 9 12"/><path d="M13.5 8.5 15 12"/><path d="m14.5 3.5 1.5 5"/><path d="m9.5 3.5-1.5 5"/><path d="m4.5 5.5 1.5 4"/><path d="m19.5 5.5-1.5 4"/></svg>' },
  { name: 'Hortifruti', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>' },
  { name: 'Bebidas', svg: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 8 1.75 12.2A2 2 0 0 0 9.71 22h4.58a2 2 0 0 0 1.96-1.8L18 8"/><path d="M5 8h14"/><path d="M7 15a6.47 6.47 0 0 1 5 0 6.47 6.47 0 0 0 5 0"/><path d="m12 8 1-6h2"/></svg>' }
]

const products = ref<any[]>([])

onMounted(async () => {
  products.value = await ShopService.getProducts()
})

const filteredProducts = computed(() => {
  return products.value.filter(p => {
    const matchesSearch = p.name.toLowerCase().includes(search.value.toLowerCase()) || p.store.toLowerCase().includes(search.value.toLowerCase())
    const matchesFilter = activeFilter.value === 'Todos' || p.category === activeFilter.value
    return matchesSearch && matchesFilter
  })
})

const goToProduct = (id: string) => {
  router.push('/produto/' + id)
}

const addToCart = (product: any) => {
  addCartAction(product, 1)
}
</script>

<template>
  <div class="screen">
    <header class="home-header">
      <div class="logo-container">
        <svg class="cart-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M7 18C5.9 18 5.01 18.9 5.01 20C5.01 21.1 5.9 22 7 22C8.1 22 9 21.1 9 20C9 18.9 8.1 18 7 18ZM1 2V4H3L6.6 11.59L5.24 14.04C5.09 14.32 5 14.65 5 15C5 16.1 5.9 17 7 17H19V15H7.42C7.28 15 7.17 14.89 7.17 14.75L7.2 14.63L8.1 13H15.55C16.3 13 16.96 12.59 17.3 11.97L20.88 5.48C20.95 5.34 21 5.17 21 5C21 4.45 20.55 4 20 4H5.21L4.27 2H1ZM17 18C15.9 18 15.01 18.9 15.01 20C15.01 21.1 15.9 22 17 22C18.1 22 19 21.1 19 20C19 18.9 18.1 18 17 18Z" fill="#FF3B69"/>
        </svg>
        <h1 class="logo-text">Cheap<span class="logo-text-highlight">Food</span></h1>
      </div>

      <div class="search-bar">
        <input type="text" v-model="search" placeholder="Buscar produtos, lojas..." />
        <span class="search-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        </span>
      </div>
    </header>

    <main class="content">
      <div class="promo-card">
        <div class="promo-info">
          <div class="promo-badge">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" color="#d92d3f"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg>
          </div>
          <h2 class="promo-title">Até 70% OFF</h2>
          <h3 class="promo-subtitle">em laticínios</h3>
          <p class="promo-desc">Vence amanhã · Supermercado Bom Preço</p>
        </div>
        <div class="promo-img">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4"/><path d="M2 7h20"/><path d="M22 7v3a2 2 0 0 1-2 2v0a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 16 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 12 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 8 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 4 12v0a2 2 0 0 1-2-2V7"/></svg>
        </div>
      </div>

      <div class="categories">
        <button 
          v-for="filter in filters" 
          :key="filter.name" 
          class="category-btn"
          :class="{ active: activeFilter === filter.name }"
          @click="activeFilter = filter.name"
        >
          <span v-if="filter.svg" class="cat-icon" v-html="filter.svg"></span> {{ filter.name }}
        </button>
      </div>

      <div class="section-header">
        <h2>Perto de vencer 🏷️</h2>
        <a href="#" class="see-all" @click.prevent="router.push('/buscar')">Ver todos</a>
      </div>

      <div class="product-list">
        <div class="product-card" v-for="product in filteredProducts" :key="product.id" @click="goToProduct(product.id)">
          <div class="product-image">
            <img v-if="product.image && (product.image.startsWith('/') || product.image.startsWith('http'))" :src="product.image.startsWith('http') ? product.image : `http://localhost:5000${product.image}`" class="real-image" />
            <span v-else class="emoji-img" v-html="product.image"></span>
          </div>
          <div class="product-details">
            <h3 class="product-name">{{ product.name }}</h3>
            <p class="product-store">{{ product.store }}</p>
            <div class="product-price-row">
              <span class="price">R${{ product.price.toFixed(2).replace('.', ',') }}</span>
              <span class="old-price">R${{ product.old_price.toFixed(2).replace('.', ',') }}</span>
            </div>
            <div class="tag-row">
              <span class="tag" :class="{'danger': product.expires_in.includes('hoje')}">{{ product.expires_in }}</span>
            </div>
          </div>
          <button class="add-btn" aria-label="Adicionar ao carrinho" @click.stop="addToCart(product)">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
          </button>
        </div>
      </div>
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

.home-header {
  background-color: #f6b55d;
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.cart-icon {
  width: 24px;
  height: 24px;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 800;
  color: white;
  margin: 0;
}

.logo-text-highlight {
  color: #ff3b69;
}

.search-bar {
  position: relative;
  width: 100%;
}

.search-bar input {
  width: 100%;
  padding: 0.8rem 2.8rem 0.8rem 1rem; /* Added right padding so text doesn't overlap icon */
  border-radius: 12px;
  border: none;
  background-color: white;
  font-size: 0.95rem;
  color: #333;
}

.search-icon {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 2.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  line-height: 1;
}

.content {
  padding: 1.5rem;
  flex: 1;
  overflow-y: auto;
  padding-bottom: 80px;
}

.promo-card {
  background-color: #f7b75e;
  border-radius: 16px;
  padding: 1.2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #5c3809;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 15px rgba(247, 183, 94, 0.3);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.promo-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(247, 183, 94, 0.5);
}

.promo-badge {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.promo-title {
  font-size: 1.2rem;
  font-weight: 800;
  margin: 0;
}

.promo-subtitle {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
}

.promo-desc {
  font-size: 0.75rem;
  opacity: 0.9;
  margin: 0;
}

.promo-img {
  font-size: 3rem;
  background-color: rgba(255,255,255,0.3);
  border-radius: 50%;
  width: 60px;
  min-width: 60px;
  height: 60px;
  flex-shrink: 0;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.categories {
  display: flex;
  gap: 0.8rem;
  overflow-x: auto;
  padding: 4px 4px 0.5rem 4px;
  margin: 0 -4px 1.5rem -4px;
}

.categories::-webkit-scrollbar {
  display: none;
}

.category-btn {
  padding: 0.6rem 1rem;
  border-radius: 20px;
  border: 1px solid #e0e0e0;
  background: white;
  font-weight: 600;
  font-size: 0.85rem;
  color: #555;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.category-btn:hover {
  background-color: #fff0f3;
  border-color: #ffb3c6;
  transform: translateY(-1px);
}

.category-btn.active {
  background-color: #ff3b69;
  color: white;
  border-color: #ff3b69;
}

.category-btn.active:hover {
  background-color: #e0335c;
  border-color: #e0335c;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h2 {
  font-size: 1.1rem;
  font-weight: 800;
  color: #333;
  margin: 0;
}

.see-all {
  color: #ff3b69;
  font-size: 0.85rem;
  font-weight: 600;
  text-decoration: none;
}

.product-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.product-card {
  border: 1px solid #f0f0f0;
  border-radius: 16px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
  cursor: pointer;
  background-color: white;
  transition: all 0.2s ease;
}

.product-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  border-color: transparent;
}

.product-image {
  width: 60px;
  min-width: 60px;
  height: 60px;
  flex-shrink: 0;
  overflow: hidden;
  background-color: #fdf6e9;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #f0dfb8;
  overflow: hidden;
}

.real-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.emoji-img {
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-details {
  flex: 1;
}

.product-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: #333;
  margin: 0 0 0.2rem 0;
}

.product-store {
  font-size: 0.75rem;
  color: #888;
  margin: 0 0 0.5rem 0;
}

.product-price-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.4rem;
}

.price {
  font-size: 1.1rem;
  font-weight: 800;
  color: #333;
}

.old-price {
  font-size: 0.85rem;
  color: #aaa;
  text-decoration: line-through;
}

.tag-row {
  display: flex;
}

.tag {
  background-color: #fdf6e9;
  color: #c9791a;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 700;
  border: 1px solid #f7d299;
}

.tag.danger {
  background-color: #ff3b69;
  color: white;
  border: none;
}

.add-btn {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background-color: #ff3b69;
  color: white;
  border: none;
  font-size: 1.5rem;
  font-weight: 500;
  line-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 4px 10px rgba(255, 59, 105, 0.3);
}

.add-btn:hover {
  background-color: #e0335c;
  transform: translateY(-50%) scale(1.05);
  box-shadow: 0 6px 15px rgba(255, 59, 105, 0.45);
}

.add-btn:active {
  transform: translateY(-50%) scale(0.95);
  box-shadow: 0 2px 5px rgba(255, 59, 105, 0.3);
}

</style>

