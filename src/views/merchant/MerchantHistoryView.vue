<script setup lang="ts">
import { computed, ref } from 'vue'
import MerchantBottomNav from '@/components/merchant/MerchantBottomNav.vue'
import { merchantStats } from '@/data/merchant'

interface HistoryOrder {
  id: string
  customerName: string
  productIcon: string
  productName: string
  date: string
  code: string
  status: 'retirado' | 'expirado'
  value: number
}

const historyOrders: HistoryOrder[] = [
  {
    id: 'h1',
    customerName: 'João Silva',
    productIcon: '🥛',
    productName: 'Leite Integral 1L',
    date: '26/05 16:42',
    code: 'A7K3',
    status: 'retirado',
    value: 2.49,
  },
  {
    id: 'h2',
    customerName: 'Maria Oliveira',
    productIcon: '🧀',
    productName: 'Queijo Mussarela',
    date: '25/05 18:10',
    code: 'B2M9',
    status: 'retirado',
    value: 15.80,
  },
  {
    id: 'h3',
    customerName: 'Pedro Costa',
    productIcon: '🥚',
    productName: 'Ovos Caipira',
    date: '24/05 19:00',
    code: 'C9X1',
    status: 'expirado',
    value: 4.90,
  },
]

const activeTab = ref<'todos' | 'retirados' | 'expirados'>('todos')

const filteredOrders = computed(() => {
  if (activeTab.value === 'todos') return historyOrders
  return historyOrders.filter(o => o.status === activeTab.value)
})

const totalCount = historyOrders.length

function money(v: number) {
  return `R$${v.toFixed(2).replace('.', ',')}`
}
</script>

<template>
  <div class="screen">
    <header class="history-header">
      <h1 class="header-title">Histórico de pedidos</h1>
      <p class="header-subtitle">{{ merchantStats.period }}</p>
    </header>

    <main class="content">
      <div class="tabs">
        <button
          class="tab"
          :class="{ active: activeTab === 'todos' }"
          @click="activeTab = 'todos'"
        >
          Todos ({{ totalCount }})
        </button>
        <button
          class="tab"
          :class="{ active: activeTab === 'retirados' }"
          @click="activeTab = 'retirados'"
        >
          Retirados
        </button>
        <button
          class="tab"
          :class="{ active: activeTab === 'expirados' }"
          @click="activeTab = 'expirados'"
        >
          Expirados
        </button>
      </div>

      <div class="order-list">
        <div v-for="order in filteredOrders" :key="order.id" class="order-card">
          <div class="order-top">
            <p class="customer-name">{{ order.customerName }}</p>
            <span
              class="status-badge"
              :class="order.status"
            >
              {{ order.status === 'retirado' ? 'Retirado' : 'Expirado' }}
            </span>
          </div>
          <p class="order-product">
            {{ order.productIcon }} {{ order.productName }} · {{ order.date }}
          </p>
          <div class="order-bottom">
            <span class="order-code">Código {{ order.code }}</span>
            <span class="order-value">{{ money(order.value) }}</span>
          </div>
        </div>
      </div>

      <p v-if="filteredOrders.length === 0" class="empty">Nenhum pedido encontrado.</p>
    </main>

    <MerchantBottomNav />
  </div>
</template>

<style scoped>
.screen {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #fff;
  color: #1a1a2e;
}

.history-header {
  background: #f5a623;
  padding: 20px 18px;
  border-radius: 0 0 22px 22px;
  flex-shrink: 0;
}

.header-title {
  font-size: 17px;
  font-weight: 800;
  color: #fff;
}

.header-subtitle {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.85);
  margin-top: 2px;
}

.content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.tab {
  flex-shrink: 0;
  background: #fff;
  border: 1px solid #eceaf4;
  color: #7a7a8c;
  font-size: 11px;
  font-weight: 600;
  padding: 8px 14px;
  border-radius: 999px;
  white-space: nowrap;
  cursor: pointer;
}

.tab.active {
  background: #f5a623;
  border-color: #f5a623;
  color: #fff;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.order-card {
  background: #fff;
  border: 1px solid #eceaf4;
  border-radius: 16px;
  padding: 14px;
}

.order-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.customer-name {
  font-size: 14px;
  font-weight: 700;
}

.status-badge {
  font-size: 10px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 999px;
}

.status-badge.retirado {
  color: #1f8a4c;
  background: #e6f6ec;
}

.status-badge.expirado {
  color: #7a7a8c;
  background: #f2f2f5;
}

.order-product {
  font-size: 12px;
  color: #7a7a8c;
  margin-top: 6px;
}

.order-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 6px;
  font-size: 12px;
}

.order-code {
  color: #7a7a8c;
}

.order-value {
  color: #f5a623;
  font-weight: 700;
}

.empty {
  text-align: center;
  color: #7a7a8c;
  font-size: 13px;
  padding: 24px 0;
}
</style>
