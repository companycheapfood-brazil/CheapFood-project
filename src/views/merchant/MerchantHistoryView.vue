<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import MerchantHeader from "@/components/merchant/MerchantHeader.vue";
import MerchantBottomNav from "@/components/merchant/MerchantBottomNav.vue";
import { useMerchantStore } from "@/stores/useMerchantStore";
import SvgIcon from "@/components/ui/SvgIcon.vue";

const merchantStore = useMerchantStore();
const activeTab = ref<"todos" | "retirados" | "expirados">("todos");

onMounted(() => {
  merchantStore.fetchOrders();
});

const historyOrders = computed(() => {
  return merchantStore.orders
    .filter((o) => o.status === "retirado" || o.status === "expirado")
    .map((o) => ({
      id: o.id,
      customerName: o.customerName || "Cliente",
      productName: o.productName,
      quantity: o.quantity || 1,
      date: o.createdAt || "Hoje",
      code: o.code,
      status: o.status as "retirado" | "expirado",
      value: (o.price || 0) * (o.quantity || 1),
    }));
});

const filteredOrders = computed(() => {
  if (activeTab.value === "todos") return historyOrders.value;
  const target = activeTab.value === "retirados" ? "retirado" : "expirado";
  return historyOrders.value.filter((o) => o.status === target);
});

const totalCount = computed(() => historyOrders.value.length);

const totalRecovered = computed(() =>
  historyOrders.value
    .filter((o) => o.status === "retirado")
    .reduce((acc, o) => acc + o.value, 0),
);

function money(v: number) {
  return `R$ ${v.toFixed(2).replace(".", ",")}`;
}
</script>

<template>
  <div class="screen">
    <MerchantHeader
      title="Histórico de Vendas"
      :subtitle="`Total: ${totalCount} pedido(s) finalizados`"
      backTo="/comerciante/pedidos"
    />

    <main class="content">
      <div class="summary-banner">
        <div>
          <p class="summary-label">Total recuperado em retiradas</p>
          <p class="summary-value">{{ money(totalRecovered) }}</p>
        </div>
        <div class="summary-pill">
          {{ historyOrders.filter((o) => o.status === "retirado").length }} entregas
        </div>
      </div>

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
          Retirados ({{
            historyOrders.filter((o) => o.status === "retirado").length
          }})
        </button>
        <button
          class="tab"
          :class="{ active: activeTab === 'expirados' }"
          @click="activeTab = 'expirados'"
        >
          Expirados ({{
            historyOrders.filter((o) => o.status === "expirado").length
          }})
        </button>
      </div>

      <div class="order-list">
        <div
          v-for="order in filteredOrders"
          :key="order.id"
          class="order-card"
          @click="$router.push(`/comerciante/pedidos/${order.id}`)"
        >
          <div class="order-top">
            <p class="customer-name">{{ order.customerName }}</p>
            <span class="status-badge" :class="order.status">
              {{ order.status === "retirado" ? "Retirado" : "Expirado" }}
            </span>
          </div>
          <p class="order-product">
            <SvgIcon name="shopping-bag" :size="14" />
            <span>{{ order.productName }} (x{{ order.quantity }}) · {{ order.date }}</span>
          </p>
          <div class="order-bottom">
            <span class="order-code">Código PIN: <strong>{{ order.code }}</strong></span>
            <span class="order-value">{{ money(order.value) }}</span>
          </div>
        </div>
      </div>

      <p v-if="filteredOrders.length === 0" class="empty">
        Nenhum pedido encontrado nesta aba.
      </p>
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
  padding-bottom: 100px;
  overflow-y: auto;
}

.summary-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: 14px;
  padding: 14px 16px;
  margin-bottom: 14px;
}

.summary-label {
  font-size: 11px;
  color: var(--mc-text-muted);
  font-weight: 600;
}

.summary-value {
  font-size: 20px;
  font-weight: 900;
  color: var(--mc-green, #2a9d8f);
  margin-top: 2px;
}

.summary-pill {
  background: #e6f6ec;
  color: #1f8a4c;
  font-size: 11px;
  font-weight: 800;
  padding: 6px 12px;
  border-radius: 999px;
}

.tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
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
  cursor: pointer;
}

.tab.active {
  background: var(--mc-navy);
  border-color: var(--mc-navy);
  color: #fff;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.order-card {
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: 16px;
  padding: 14px;
  cursor: pointer;
  transition: transform 0.15s ease;
}

.order-card:hover {
  transform: translateY(-1px);
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
  color: var(--mc-danger);
  background: var(--mc-danger-soft);
}

.order-product {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--mc-text-muted);
  margin-top: 6px;
}

.order-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
  font-size: 12px;
}

.order-code {
  color: var(--mc-text-muted);
}

.order-code strong {
  color: var(--mc-navy);
}

.order-value {
  color: var(--mc-green, #2a9d8f);
  font-weight: 800;
}

.empty {
  text-align: center;
  color: var(--mc-text-muted);
  font-size: 13px;
  padding: 24px 0;
}
</style>
