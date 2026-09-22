<script setup lang="ts">
import { ref } from 'vue'
import BottomNav from '@/components/BottomNav.vue'

const tabs = ['Todos (18)', 'Retirados', 'Expirados']
const activeTab = ref('Todos (18)')

const orders = [
  { name: 'João Silva', details: '🥛 Leite Integral 1L - 26/05 16:42', code: 'Código A7K3', status: 'Retirado', price: 'R$2,49' },
  { name: 'Maria Oliveira', details: '🧀 Queijo Mussarela - 25/05 18:10', code: 'Código B2M9', status: 'Retirado', price: 'R$15,80' },
  { name: 'Pedro Costa', details: '🥚 Ovos Caipira - 24/05 19:00', code: 'Código C9X1', status: 'Expirado', price: 'R$4,90' },
]
</script>

<template>
  <div class="screen">
    <header class="history-header">
      <h1 class="title">Histórico de pedidos</h1>
    </header>

    <main class="content">
      <div class="filters">
        <button 
          v-for="tab in tabs" 
          :key="tab"
          class="filter-btn"
          :class="{ active: activeTab === tab }"
          @click="activeTab = tab"
        >
          {{ tab }}
        </button>
      </div>

      <div class="order-list">
        <div class="order-card" v-for="(order, idx) in orders" :key="idx">
          <div class="card-top">
            <h3 class="order-name">{{ order.name }}</h3>
            <span class="status-badge" :class="order.status === 'Expirado' ? 'expired' : 'success'">
              {{ order.status }}
            </span>
          </div>
          <p class="order-details">{{ order.details }}</p>
          <div class="card-bottom">
            <span class="order-code">{{ order.code }}</span>
            <span class="order-price" :class="order.status === 'Expirado' ? 'expired-price' : ''">
              {{ order.price }}
            </span>
          </div>
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

.history-header {
  background-color: #f6b55d;
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
  text-align: center;
}

.title {
  font-size: 1.2rem;
  font-weight: 800;
  color: #333;
  margin: 0;
}

.content {
  padding: 1.5rem;
  flex: 1;
  overflow-y: auto;
  padding-bottom: 100px;
}

.filters {
  display: flex;
  gap: 0.8rem;
  margin-bottom: 1.5rem;
}

.filter-btn {
  background-color: #fdf6e9;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  color: #a0845a;
  cursor: pointer;
}

.filter-btn.active {
  background-color: #f6b55d;
  color: white;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.order-card {
  border: 1px solid #f0dfb8;
  border-radius: 12px;
  padding: 1rem;
  background-color: white;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.order-name {
  font-size: 0.95rem;
  font-weight: 800;
  color: #333;
  margin: 0;
}

.status-badge {
  background-color: #eafbe4;
  color: #2ecc71;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 800;
}

.status-badge.expired {
  background-color: #f5f5f5;
  color: #888;
}

.order-details {
  font-size: 0.85rem;
  color: #888;
  margin: 0 0 1rem 0;
}

.card-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-code {
  font-size: 0.85rem;
  color: #b0b0b0;
}

.order-price {
  font-size: 1rem;
  font-weight: 800;
  color: #f6b55d;
}

.order-price.expired-price {
  color: #b0b0b0;
}
</style>
