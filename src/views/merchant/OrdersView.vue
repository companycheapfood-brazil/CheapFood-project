<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import MerchantHeader from "@/components/merchant/MerchantHeader.vue";
import MerchantBottomNav from "@/components/merchant/MerchantBottomNav.vue";
import { useMerchantStore } from "@/stores/useMerchantStore";
import { useToastStore } from "@/stores/useToastStore";
import { storeToRefs } from "pinia";
import SvgIcon from "@/components/ui/SvgIcon.vue";

const merchantStore = useMerchantStore();
const toast = useToastStore();
const { pendingOrders, pickedUpOrders, expiredOrders } =
  storeToRefs(merchantStore);
const { confirmPickup, cancelOrder } = merchantStore;

const searchCode = ref("");

onMounted(() => {
  merchantStore.fetchOrders();
});

const activeTab = ref<"pendentes" | "retirados" | "expirados">("pendentes");

const tabs = computed(() => [
  {
    key: "pendentes" as const,
    label: `Pendentes (${pendingOrders.value.length})`,
  },
  {
    key: "retirados" as const,
    label: `Retirados (${pickedUpOrders.value.length})`,
  },
  {
    key: "expirados" as const,
    label: `Expirados (${expiredOrders.value.length})`,
  },
]);

const visibleOrders = computed(() => {
  let list = pendingOrders.value;
  if (activeTab.value === "retirados") list = pickedUpOrders.value;
  else if (activeTab.value === "expirados") list = expiredOrders.value;

  const q = searchCode.value.trim().toUpperCase();
  if (!q) return list;
  return list.filter(
    (o) =>
      o.code.toUpperCase().includes(q) ||
      o.customerName.toUpperCase().includes(q) ||
      o.productName.toUpperCase().includes(q),
  );
});

async function handleConfirmPickup(orderId: string) {
  await confirmPickup(orderId);
  toast.addToast("Retirada confirmada com sucesso!", "success");
}

async function handleCancelOrder(orderId: string) {
  await cancelOrder(orderId);
  toast.addToast("Pedido cancelado e estoque devolvido.", "info");
}
</script>

<template>
  <div class="screen">
    <MerchantHeader
      title="Pedidos e Reservas"
      :subtitle="`${pendingOrders.length} aguardando retirada`"
    />

    <main class="content">
      <div class="top-tools">
        <div class="search-code-box">
          <span class="search-icon">
            <SvgIcon name="search" :size="15" />
          </span>
          <input
            v-model="searchCode"
            type="text"
            placeholder="Buscar por código PIN ou cliente..."
          />
          <button
            v-if="searchCode"
            class="clear-btn"
            @click="searchCode = ''"
            aria-label="Limpar busca"
          >
            <SvgIcon name="x" :size="14" />
          </button>
        </div>
        <button
          class="history-btn"
          @click="$router.push('/comerciante/historico')"
          title="Ver Histórico Completo"
        >
          <SvgIcon name="receipt" :size="15" />
          Histórico
        </button>
      </div>

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
        <div
          v-for="order in visibleOrders"
          :key="order.id"
          class="order-card"
          @click="$router.push(`/comerciante/pedidos/${order.id}`)"
          style="cursor: pointer"
        >
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
                order.status === "pendente"
                  ? "Aguardando"
                  : order.status === "retirado"
                    ? "Retirado"
                    : "Expirado"
              }}
            </span>
          </div>

          <p class="order-line">
            <SvgIcon name="shopping-bag" :size="14" />
            <span>{{ order.productName }} · Qtd: {{ order.quantity }}</span>
            <span v-if="order.price" class="order-total">
              · R$ {{ (order.price * order.quantity).toFixed(2).replace(".", ",") }}
            </span>
          </p>

          <div class="order-meta">
            <span class="code"
              >Código PIN: <strong>{{ order.code }}</strong></span
            >
            <span v-if="order.status === 'pendente'" class="deadline">
              Retira até {{ order.pickupDeadline }}
            </span>
            <span v-else class="date-label">
              {{ order.createdAt || "Hoje" }}
            </span>
          </div>

          <div v-if="order.status === 'pendente'" class="order-actions">
            <button
              class="confirm-btn"
              @click.stop="handleConfirmPickup(order.id)"
            >
              <SvgIcon name="check-circle" :size="15" />
              Confirmar retirada
            </button>
            <button
              class="cancel-btn"
              @click.stop="handleCancelOrder(order.id)"
            >
              Cancelar
            </button>
          </div>
        </div>

        <p v-if="visibleOrders.length === 0" class="empty">
          Nenhum pedido encontrado nesta categoria.
        </p>
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
  padding-bottom: 100px;
  overflow-y: auto;
}

.top-tools {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.search-code-box {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: var(--cf-radius-sm);
  padding: 8px 12px;
}

.search-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--mc-text-muted);
  line-height: 0;
}

.search-code-box input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-size: 12px;
  color: var(--mc-text);
}

.clear-btn {
  background: transparent;
  border: none;
  color: var(--mc-text-muted);
  cursor: pointer;
  padding: 2px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 0;
}

.history-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: var(--mc-navy);
  color: #fff;
  border: none;
  border-radius: var(--cf-radius-sm);
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
}

.tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  touch-action: pan-x;
  overscroll-behavior-x: contain;
  scrollbar-width: none;
}

.tabs::-webkit-scrollbar {
  display: none;
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
  gap: 12px;
}

.order-card {
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: var(--cf-radius-md);
  padding: 14px;
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
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--mc-text-muted);
  margin-top: 6px;
}

.order-total {
  font-weight: 700;
  color: var(--mc-navy);
}

.order-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
  font-size: 11px;
}

.code {
  color: var(--mc-text-muted);
}

.code strong {
  color: var(--mc-navy);
  letter-spacing: 0.08em;
  background: #f0f4f8;
  padding: 2px 6px;
  border-radius: 4px;
}

.deadline {
  color: var(--cf-pink);
  font-weight: 600;
}

.date-label {
  color: var(--mc-text-muted);
}

.order-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.confirm-btn {
  flex: 1 1 140px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: var(--mc-navy);
  color: #fff;
  border: none;
  border-radius: var(--cf-radius-sm);
  padding: 11px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}

.cancel-btn {
  flex: 1 1 100px;
  background: transparent;
  border: 1px solid var(--mc-danger);
  color: var(--mc-danger);
  border-radius: var(--cf-radius-sm);
  padding: 11px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}

.empty {
  text-align: center;
  color: var(--mc-text-muted);
  font-size: 13px;
  padding: 24px 0;
}
</style>
