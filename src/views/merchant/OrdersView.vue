<script setup lang="ts">
import { computed, ref } from 'vue'
import MerchantHeader from '@/components/merchant/MerchantHeader.vue'
import MerchantBottomNav from '@/components/merchant/MerchantBottomNav.vue'
import { useMerchant } from '@/composables/useMerchant'

const { pendingOrders, pickedUpOrders, expiredOrders, confirmPickup, cancelOrder } = useMerchant()

const activeTab = ref<'pendentes' | 'retirados' | 'expirados'>('pendentes')

const tabs = computed(() => [
  { key: 'pendentes' as const, label: `Pendentes (${pendingOrders.value.length})` },
  { key: 'retirados' as const, label: 'Retirados' },
  { key: 'expirados' as const, label: 'Expirados' },
])

const visibleOrders = computed(() => {
  if (activeTab.value === 'pendentes') return pendingOrders.value
  if (activeTab.value === 'retirados') return pickedUpOrders.value
  return expiredOrders.value
})
</script>

<template>
  <div class="screen">
    <MerchantHeader title="Pedidos" :subtitle="`${pendingOrders.length} aguardando retirada`" />

    <main class="content">
      <div class="tabs">
        <button
          v-for="t in tabs"
          :key="t.key"
          class="tab"
          :class="{ active: activeTab === t.key }"
          @click="activeTab = t.key"
        >
          {{ t.label }}
        </button>
      </div>

      <div class="order-list">
        <div v-for="order in visibleOrders" :key="order.id" class="order-card">
          <div class="order-top">
            <p class="customer-name">{{ order.customerName }}</p>
            <span
              class="status-badge"
              :class="{
                retirado: order.status === 'retirado',
                expirado: order.status === 'expirado',
              }"
            >
              {{
                order.status === 'pendente'
                  ? 'Aguardando'
                  : order.status === 'retirado'
                    ? 'Retirado'
                    : 'Expirado'
              }}
            </span>
          </div>

          <p class="order-line">🛍️ {{ order.productName }} · Qtd: {{ order.quantity }}</p>

          <div class="order-meta">
            <span class="code">Código: <strong>{{ order.code }}</strong></span>
            <span v-if="order.status === 'pendente'" class="deadline">
              Retira até {{ order.pickupDeadline }}
            </span>
          </div>

          <div v-if="order.status === 'pendente'" class="order-actions">
            <button class="confirm-btn" @click="confirmPickup(order.id)">Confirmar retirada</button>
            <button class="cancel-btn" @click="cancelOrder(order.id)">Cancelar</button>
          </div>
        </div>

        <p v-if="visibleOrders.length === 0" class="empty">Nenhum pedido nesta categoria.</p>
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
  background: var(--mc-bg);
  color: var(--mc-text);
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
  overflow-x: auto;
}

.tab {
  flex-shrink: 0;
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  color: var(--mc-text-muted);
  font-size: 11px;
  font-weight: 600;
  padding: 8px 14px;
  border-radius: 999px;
  white-space: nowrap;
}

.tab.active {
  background: var(--mc-navy);
  border-color: var(--mc-navy);
  color: #fff;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-card {
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: var(--cf-radius-md);
  padding: 14px;
}

.order-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.customer-name {
  font-size: 13px;
  font-weight: 700;
}

.status-badge {
  font-size: 10px;
  font-weight: 700;
  color: var(--mc-warning-text);
  background: var(--mc-warning-bg);
  padding: 3px 9px;
  border-radius: 999px;
}

.status-badge.retirado {
  color: var(--mc-success);
  background: #e6f6ec;
}

.status-badge.expirado {
  color: var(--mc-danger);
  background: var(--mc-danger-soft);
}

.order-line {
  font-size: 12px;
  color: var(--mc-text-muted);
  margin-top: 6px;
}

.order-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
  font-size: 11px;
}

.code {
  color: var(--mc-text-muted);
}

.code strong {
  color: var(--mc-text);
  letter-spacing: 0.05em;
}

.deadline {
  color: var(--cf-pink);
  font-weight: 600;
}

.order-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.confirm-btn {
  flex: 1;
  background: var(--mc-navy);
  color: #fff;
  border: none;
  border-radius: var(--cf-radius-sm);
  padding: 11px;
  font-size: 12px;
  font-weight: 700;
}

.cancel-btn {
  flex: 1;
  background: transparent;
  border: 1px solid var(--cf-orange);
  color: var(--cf-orange-soft);
  border-radius: var(--cf-radius-sm);
  padding: 11px;
  font-size: 12px;
  font-weight: 700;
}

.empty {
  text-align: center;
  color: var(--mc-text-muted);
  font-size: 13px;
  padding: 24px 0;
}
</style>
