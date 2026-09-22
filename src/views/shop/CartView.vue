<script setup lang="ts">
import { useRouter } from 'vue-router'
import BottomNav from '@/components/BottomNav.vue'
import ShopService from '@/services/shop.service'
import { useCart } from '@/composables/useCart'

const router = useRouter()
const { items: cartItems, updateQuantity, subtotal, totalSavings: savings, checkout: generateCode, clearCart } = useCart()

const checkout = async () => {
  try {
    const res = await ShopService.checkout(cartItems as any)
    const code = generateCode()
    router.push({ path: '/comprovante', query: { code: (res as any).code || code, subtotal: subtotal.value, savings: savings.value } })
    clearCart()
  } catch (error) {
    console.error(error)
  }
}
</script>

<template>
  <div class="screen">
    <header class="cart-header">
      <h1 class="header-title">Meu carrinho</h1>
      <span class="header-badge">{{ cartItems.length }} itens</span>
    </header>

    <main class="content">
      <div v-if="cartItems.length === 0" class="empty-cart">
        Seu carrinho está vazio.
      </div>
      <div v-else class="cart-items">
        <div class="cart-item" v-for="item in cartItems" :key="item.product.id">
          <div class="item-img">
            <span class="emoji-img">{{ item.product.image }}</span>
          </div>
          <div class="item-details">
            <h3 class="item-name">{{ item.product.name }}</h3>
            <p class="item-store">{{ item.product.store }}</p>
            <p class="item-price">R${{ item.product.price.toFixed(2).replace('.', ',') }}</p>
          </div>
          <div class="quantity-selector">
            <button class="q-btn" @click="updateQuantity(item.product.id, -1)">-</button>
            <span class="q-val">{{ item.quantity }}</span>
            <button class="q-btn" @click="updateQuantity(item.product.id, 1)">+</button>
          </div>
        </div>
      </div>

      <div class="summary-card" v-if="cartItems.length > 0">
        <div class="summary-row">
          <span class="label">Subtotal</span>
          <span class="value">R${{ subtotal.toFixed(2).replace('.', ',') }}</span>
        </div>
        <div class="summary-row">
          <span class="label">Economia total</span>
          <span class="value pink">- R${{ savings.toFixed(2).replace('.', ',') }}</span>
        </div>
        <hr class="divider" />
        <div class="summary-row total-row">
          <span class="label">Total</span>
          <span class="value">R${{ subtotal.toFixed(2).replace('.', ',') }}</span>
        </div>
        
        <div class="savings-badge">
          🎉 Economizou R${{ savings.toFixed(2).replace('.', ',') }}!
        </div>
      </div>

      <button v-if="cartItems.length > 0" class="checkout-btn" @click="checkout">Confirmar reserva</button>
      <p v-if="cartItems.length > 0" class="checkout-hint">Itens reservados por 2h para retirada</p>
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

.cart-header {
  background-color: #f6b55d;
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  font-size: 1.4rem;
  font-weight: 800;
  color: #333;
  margin: 0;
}

.header-badge {
  background-color: #ff3b69;
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 800;
}

.content {
  padding: 1.5rem;
  flex: 1;
  overflow-y: auto;
  padding-bottom: 100px;
}

.empty-cart {
  text-align: center;
  color: #888;
  margin-top: 3rem;
}

.cart-items {
  display: flex;
  flex-direction: column;
}

.cart-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #f0f0f0;
  gap: 1rem;
  transition: background-color 0.2s ease, border-radius 0.2s ease;
}

.cart-item:hover {
  background-color: #fdfaf5;
  border-radius: 12px;
}

.item-img {
  width: 50px;
  height: 50px;
  background-color: #fdf6e9;
  border: 1px solid #f0dfb8;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.item-details {
  flex: 1;
}

.item-name {
  font-size: 0.9rem;
  font-weight: 700;
  color: #333;
  margin: 0 0 0.2rem 0;
}

.item-store {
  font-size: 0.75rem;
  color: #888;
  margin: 0 0 0.4rem 0;
}

.item-price {
  font-size: 1rem;
  font-weight: 800;
  color: #333;
  margin: 0;
}

.quantity-selector {
  display: flex;
  align-items: center;
  border: 1px solid #f0dfb8;
  border-radius: 20px;
  background-color: #fdf6e9;
  overflow: hidden;
}

.q-btn {
  background: transparent;
  border: none;
  width: 30px;
  height: 30px;
  font-size: 1.2rem;
  color: #8c5b16;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.q-btn:hover {
  background-color: #f5e4c6;
}

.q-val {
  width: 20px;
  text-align: center;
  font-weight: 700;
  color: #333;
  font-size: 0.9rem;
}

.summary-card {
  background-color: #fdf6e9;
  border: 1px solid #f0dfb8;
  border-radius: 16px;
  padding: 1.5rem;
  margin-top: 2rem;
  box-shadow: 0 4px 15px rgba(240, 223, 184, 0.4);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.8rem;
  font-size: 0.9rem;
}

.summary-row .label {
  color: #888;
}

.summary-row .value {
  font-weight: 700;
  color: #333;
}

.summary-row .value.pink {
  color: #ff3b69;
}

.divider {
  border: none;
  border-top: 1px dashed #dcb985;
  margin: 1rem 0;
}

.total-row {
  font-size: 1.1rem;
}

.total-row .label {
  font-weight: 800;
  color: #333;
}

.savings-badge {
  background-color: #ff3b69;
  color: white;
  text-align: center;
  padding: 0.6rem;
  border-radius: 20px;
  font-weight: 800;
  font-size: 0.85rem;
  margin-top: 1.5rem;
  box-shadow: 0 4px 12px rgba(255, 59, 105, 0.3);
}

.checkout-btn {
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

.checkout-btn:hover {
  background-color: #e6a245;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(247, 183, 94, 0.5);
}

.checkout-btn:active {
  transform: translateY(0) scale(0.98);
}

.checkout-hint {
  text-align: center;
  color: #a0845a;
  font-size: 0.75rem;
  margin-top: 0.8rem;
}
</style>
