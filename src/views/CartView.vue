<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useCart } from '@/composables/useCart'
import BottomNav from '@/components/BottomNav.vue'

const router = useRouter()
const { items, totalItems, subtotal, totalSavings, updateQuantity, generateReservationCode } =
  useCart()

function money(v: number) {
  return `R$ ${v.toFixed(2).replace('.', ',')}`
}

function confirmReservation() {
  generateReservationCode()
  router.push('/comprovante')
}
</script>

<template>
  <div class="screen">
    <header class="header">
      <h1 class="title">Meu carrinho</h1>
      <span class="count-badge">{{ totalItems }} itens</span>
    </header>

    <main class="content">
      <div v-if="items.length === 0" class="empty-state">
        <p class="empty-icon">🛒</p>
        <p>Seu carrinho está vazio.</p>
        <RouterLink to="/" class="empty-link">Ver produtos</RouterLink>
      </div>

      <template v-else>
        <div class="cart-list">
          <div v-for="item in items" :key="item.product.id" class="cart-item">
            <div class="thumb">{{ item.product.icon }}</div>
            <div class="info">
              <p class="name">{{ item.product.name }}</p>
              <p class="store">{{ item.product.store }}</p>
              <p class="price">{{ money(item.product.price) }}</p>
            </div>
            <div class="qty-control">
              <button @click="updateQuantity(item.product.id, -1)">−</button>
              <span>{{ item.quantity }}</span>
              <button @click="updateQuantity(item.product.id, 1)">+</button>
            </div>
          </div>
        </div>

        <section class="summary-card">
          <div class="summary-row">
            <span>Subtotal</span>
            <span>{{ money(subtotal) }}</span>
          </div>
          <div class="summary-row savings">
            <span>Economia total</span>
            <span>- {{ money(totalSavings) }}</span>
          </div>
          <div class="summary-row total">
            <span>Total</span>
            <span>{{ money(subtotal) }}</span>
          </div>
          <div class="savings-pill">Economizou {{ money(totalSavings) }}!</div>
        </section>
      </template>
    </main>

    <div v-if="items.length > 0" class="footer">
      <button class="confirm-btn" @click="confirmReservation">Confirmar reserva</button>
      <p class="footer-note">Itens reservados por 2h para retirada</p>
    </div>

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
  padding: 18px 16px;
  border-radius: 0 0 var(--cf-radius-lg) var(--cf-radius-lg);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

.title {
  font-size: 17px;
  font-weight: 800;
  color: #1a1a1a;
}

.count-badge {
  background: var(--cf-pink);
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 999px;
}

.content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 60px 0;
  color: var(--cf-text-muted);
}

.empty-icon {
  font-size: 40px;
}

.empty-link {
  color: var(--cf-orange-soft);
  font-weight: 600;
  margin-top: 4px;
}

.cart-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 16px;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--cf-card);
  border-radius: var(--cf-radius-md);
  padding: 12px;
}

.thumb {
  width: 42px;
  height: 42px;
  border-radius: var(--cf-radius-sm);
  background: var(--cf-card-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.info {
  flex: 1;
  min-width: 0;
}

.name {
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.store {
  font-size: 11px;
  color: var(--cf-text-muted);
  margin-top: 2px;
}

.price {
  font-size: 13px;
  font-weight: 700;
  color: var(--cf-orange-soft);
  margin-top: 4px;
}

.qty-control {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--cf-card-soft);
  border-radius: 999px;
  padding: 4px 8px;
}

.qty-control button {
  width: 22px;
  height: 22px;
  border-radius: 999px;
  border: none;
  background: var(--cf-orange);
  color: #1a1a1a;
  font-weight: 700;
  font-size: 14px;
  line-height: 1;
}

.qty-control span {
  font-size: 13px;
  font-weight: 600;
  min-width: 12px;
  text-align: center;
}

.summary-card {
  background: var(--cf-card);
  border-radius: var(--cf-radius-md);
  padding: 16px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: var(--cf-text-muted);
  padding: 6px 0;
}

.summary-row.savings {
  color: var(--cf-pink-soft);
}

.summary-row.total {
  color: var(--cf-text);
  font-size: 16px;
  font-weight: 800;
  border-top: 1px solid var(--cf-border);
  margin-top: 6px;
  padding-top: 12px;
}

.savings-pill {
  margin-top: 12px;
  background: var(--cf-pink);
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  text-align: center;
  padding: 8px;
  border-radius: 999px;
}

.footer {
  padding: 8px 16px 16px;
  flex-shrink: 0;
}

.confirm-btn {
  width: 100%;
  background: var(--cf-orange);
  color: #1a1a1a;
  border: none;
  border-radius: var(--cf-radius-sm);
  padding: 15px;
  font-size: 14px;
  font-weight: 700;
}

.footer-note {
  text-align: center;
  font-size: 11px;
  color: var(--cf-text-faint);
  margin-top: 8px;
}
</style>
