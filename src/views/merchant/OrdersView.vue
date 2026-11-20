<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import MerchantHeader from "@/components/merchant/MerchantHeader.vue";
import MerchantBottomNav from "@/components/merchant/MerchantBottomNav.vue";
import { useMerchantStore } from "@/stores/useMerchantStore";
import { useToastStore } from "@/stores/useToastStore";
import { formatBRL } from "@/composables/useAuctionClock";
import { storeToRefs } from "pinia";
import SvgIcon from "@/components/ui/SvgIcon.vue";

const merchantStore = useMerchantStore();
const toast = useToastStore();
const { pendingOrders, pickedUpOrders, expiredOrders } =
  storeToRefs(merchantStore);
const { confirmPickup, cancelOrder } = merchantStore;

const searchCode = ref("");
const isLoading = ref(true);
const busyOrderIds = ref<Record<string, boolean>>({});
const orderIdToCancel = ref<string | null>(null);

onMounted(async () => {
  isLoading.value = true;
  await merchantStore.fetchOrders();
  isLoading.value = false;
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
      String(o.code || "").toUpperCase().includes(q) ||
      String(o.customerName || "").toUpperCase().includes(q) ||
      String(o.productName || "").toUpperCase().includes(q),
  );
});

async function handleConfirmPickup(orderId: string) {
  if (busyOrderIds.value[orderId]) return;
  busyOrderIds.value[orderId] = true;
  try {
    const ok = await confirmPickup(orderId);
    if (ok) {
      toast.addToast("Retirada confirmada com sucesso!", "success");
    }
  } finally {
    busyOrderIds.value[orderId] = false;
  }
}

function requestCancelOrder(orderId: string) {
  orderIdToCancel.value = orderId;
}

async function confirmCancelOrder() {
  const orderId = orderIdToCancel.value;
  if (!orderId || busyOrderIds.value[orderId]) return;
  busyOrderIds.value[orderId] = true;
  try {
    const ok = await cancelOrder(orderId);
    if (ok) {
      toast.addToast("Pedido cancelado e estoque devolvido.", "info");
    }
    orderIdToCancel.value = null;
  } finally {
    busyOrderIds.value[orderId] = false;
  }
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
        <p v-if="isLoading" class="empty">Carregando pedidos...</p>
        <template v-else>
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
              · {{ formatBRL(order.price * order.quantity) }}
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
              :disabled="busyOrderIds[order.id]"
              @click.stop="handleConfirmPickup(order.id)"
            >
              <SvgIcon name="check-circle" :size="15" />
              {{ busyOrderIds[order.id] ? "Processando..." : "Confirmar retirada" }}
            </button>
            <button
              class="cancel-btn"
              :disabled="busyOrderIds[order.id]"
              @click.stop="requestCancelOrder(order.id)"
            >
              Cancelar
            </button>
          </div>
        </div>

        <p v-if="visibleOrders.length === 0" class="empty">
          Nenhum pedido encontrado nesta categoria.
        </p>
        </template>
      </div>
    </main>

    <!-- Modal de Confirmação de Cancelamento -->
    <div
      v-if="orderIdToCancel"
      class="modal-overlay"
      @click.self="!busyOrderIds[orderIdToCancel] && (orderIdToCancel = null)"
    >
      <div class="modal-card">
        <h3 class="modal-title">Cancelar reserva?</h3>
        <p class="modal-desc">
          O pedido será marcado como expirado e as unidades retornarão automaticamente ao estoque.
        </p>
        <div class="modal-actions">
          <button
            type="button"
            class="modal-btn-back"
            :disabled="busyOrderIds[orderIdToCancel]"
            @click="orderIdToCancel = null"
          >
            Voltar
          </button>
          <button
            type="button"
            class="modal-btn-danger"
            :disabled="busyOrderIds[orderIdToCancel]"
            @click="confirmCancelOrder"
          >
            {{ busyOrderIds[orderIdToCancel] ? "Cancelando..." : "Confirmar cancelamento" }}
          </button>
        </div>
      </div>
    </div>

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

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 16px;
}

.modal-card {
  width: 100%;
  max-width: 360px;
  background: #ffffff;
  border-radius: 18px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
}

.modal-title {
  font-size: 16px;
  font-weight: 800;
  color: var(--mc-navy);
  margin-bottom: 8px;
}

.modal-desc {
  font-size: 12px;
  color: var(--mc-text-muted);
  line-height: 1.4;
  margin-bottom: 18px;
}

.modal-actions {
  display: flex;
  gap: 10px;
}

.modal-btn-back {
  flex: 1;
  background: transparent;
  border: 1px solid var(--mc-border);
  color: var(--mc-text-muted);
  border-radius: 10px;
  padding: 11px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.modal-btn-danger {
  flex: 1.2;
  background: var(--mc-danger);
  border: none;
  color: #fff;
  border-radius: 10px;
  padding: 11px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}
</style>
