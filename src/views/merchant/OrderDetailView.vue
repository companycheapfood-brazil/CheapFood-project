<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MerchantBottomNav from '@/components/merchant/MerchantBottomNav.vue'
import { useMerchantStore } from '@/stores/useMerchantStore'
import { storeToRefs } from 'pinia'

const route = useRoute()
const router = useRouter()
const merchantStore = useMerchantStore()
const { orders } = storeToRefs(merchantStore)
const { confirmPickup, cancelOrder } = merchantStore

onMounted(() => {
  if (orders.value.length === 0) merchantStore.fetchOrders()
})

const order = computed(() => {
  const id = route.params.orderId as string
  return orders.value.find((o: any) => String(o.id) === id)
})

const spacedCode = computed(() => {
  if (!order.value) return ''
  return order.value.code.split('').join(' ')
})

const statusLabel = computed(() => {
  if (!order.value) return ''
  switch (order.value.status) {
    case 'pendente': return 'Aguardando retirada'
    case 'retirado': return 'Retirado'
    case 'expirado': return 'Expirado'
    default: return ''
  }
})

function handleConfirm() {
  if (order.value) {
    confirmPickup(order.value.id)
    router.push('/comerciante/pedidos')
  }
}

function handleCancel() {
  if (order.value) {
    cancelOrder(order.value.id)
    router.push('/comerciante/pedidos')
  }
}
</script>

<template>
  <div class="screen">
    <header class="detail-header">
      <h1 class="header-title">Detalhe do pedido</h1>
    </header>

    <main class="content" v-if="order">
      <div class="code-card">
        <p class="code-label">CÓDIGO DE RETIRADA</p>
        <p class="code-value">{{ spacedCode }}</p>
        <span class="status-badge" :class="order.status">{{ statusLabel }}</span>
      </div>

      <section class="section">
        <p class="section-label">CLIENTE</p>
        <div class="client-card">
          <div class="client-avatar">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          </div>
          <div class="client-info">
            <p class="client-name">{{ order.customerName }}</p>
            <p class="client-meta">Cliente desde mai/2026 · 4.8 ★</p>
          </div>
        </div>
      </section>

      <section class="section">
        <p class="section-label">PRODUTO</p>
        <div class="detail-table">
          <div class="detail-row">
            <span class="detail-key">Produto</span>
            <span class="detail-val">{{ order.productName }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-key">Quantidade</span>
            <span class="detail-val">{{ order.quantity }} unidade{{ order.quantity > 1 ? 's' : '' }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-key">Valor</span>
            <span class="detail-val price">R$2,49</span>
          </div>
          <div class="detail-row">
            <span class="detail-key">Reservado em</span>
            <span class="detail-val">26/05 às 14:32</span>
          </div>
          <div class="detail-row">
            <span class="detail-key">Retira até</span>
            <span class="detail-val deadline">{{ order.pickupDeadline }} hoje</span>
          </div>
        </div>
      </section>

      <div class="actions" v-if="order.status === 'pendente'">
        <button class="btn-confirm" @click="handleConfirm">✓ Confirmar retirada</button>
        <button class="btn-cancel" @click="handleCancel">Cancelar pedido</button>
      </div>
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

.detail-header {
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

.content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.code-card {
  background: #fff;
  border: 1px solid #eceaf4;
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  margin-bottom: 20px;
}

.code-label {
  font-size: 10px;
  font-weight: 600;
  color: #7a7a8c;
  letter-spacing: 0.1em;
  margin-bottom: 8px;
}

.code-value {
  font-size: 36px;
  font-weight: 900;
  color: #f5a623;
  letter-spacing: 0.15em;
  margin-bottom: 12px;
}

.status-badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 14px;
  border-radius: 999px;
}

.status-badge.pendente {
  color: #a6690a;
  background: #fff4e0;
  border: 1px solid #f5a623;
}

.status-badge.retirado {
  color: #1f8a4c;
  background: #e6f6ec;
}

.status-badge.expirado {
  color: #d92d3f;
  background: #fdeceb;
}

.section {
  margin-bottom: 20px;
}

.section-label {
  font-size: 10px;
  font-weight: 600;
  color: #7a7a8c;
  letter-spacing: 0.08em;
  margin-bottom: 10px;
}

.client-card {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #fff;
  border: 1px solid #eceaf4;
  border-radius: 16px;
  padding: 14px;
}

.client-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #fdf6e9;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.client-name {
  font-size: 14px;
  font-weight: 700;
}

.client-meta {
  font-size: 12px;
  color: #7a7a8c;
  margin-top: 2px;
}

.detail-table {
  background: #fff;
  border: 1px solid #eceaf4;
  border-radius: 16px;
  padding: 14px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f5f5f5;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-key {
  font-size: 13px;
  color: #7a7a8c;
}

.detail-val {
  font-size: 13px;
  font-weight: 700;
  color: #1a1a2e;
}

.detail-val.price {
  color: #f5a623;
}

.detail-val.deadline {
  color: #f5a623;
  font-weight: 700;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.btn-confirm {
  width: 100%;
  background: #f5a623;
  color: #fff;
  border: none;
  border-radius: 12px;
  padding: 15px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.btn-cancel {
  width: 100%;
  background: transparent;
  border: 1px solid #f5a623;
  color: #f5a623;
  border-radius: 12px;
  padding: 15px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}
</style>
