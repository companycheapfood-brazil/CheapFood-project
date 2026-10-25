<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import MerchantHeader from "@/components/merchant/MerchantHeader.vue";
import MerchantBottomNav from "@/components/merchant/MerchantBottomNav.vue";
import { useMerchantStore } from "@/stores/useMerchantStore";
import { useToastStore } from "@/stores/useToastStore";
import { storeToRefs } from "pinia";
import SvgIcon from "@/components/ui/SvgIcon.vue";

const route = useRoute();
const router = useRouter();
const merchantStore = useMerchantStore();
const toast = useToastStore();
const { orders } = storeToRefs(merchantStore);
const { confirmPickup, cancelOrder } = merchantStore;

onMounted(() => {
  if (orders.value.length === 0) merchantStore.fetchOrders();
});

const order = computed(() => {
  const id = route.params.orderId as string;
  return orders.value.find((o: any) => String(o.id) === id);
});

const spacedCode = computed(() => {
  if (!order.value) return "";
  return order.value.code.split("").join(" ");
});

const statusLabel = computed(() => {
  if (!order.value) return "";
  switch (order.value.status) {
    case "pendente":
      return "Aguardando retirada";
    case "retirado":
      return "Retirado";
    case "expirado":
      return "Expirado";
    default:
      return "";
  }
});

async function handleConfirm() {
  if (order.value) {
    await confirmPickup(order.value.id);
    toast.addToast("Retirada confirmada com sucesso!", "success");
    router.push("/comerciante/pedidos");
  }
}

async function handleCancel() {
  if (order.value) {
    await cancelOrder(order.value.id);
    toast.addToast("Pedido cancelado e estoque devolvido.", "info");
    router.push("/comerciante/pedidos");
  }
}
</script>

<template>
  <div class="screen">
    <MerchantHeader
      title="Detalhe do Pedido"
      subtitle="Conferência de código e retirada"
      backTo="/comerciante/pedidos"
    />

    <main class="content" v-if="order">
      <div class="code-card">
        <p class="code-label">CÓDIGO DE RETIRADA (PIN)</p>
        <p class="code-value">{{ spacedCode }}</p>
        <span class="status-badge" :class="order.status">{{
          statusLabel
        }}</span>
      </div>

      <section class="section">
        <p class="section-label">CLIENTE</p>
        <div class="client-card">
          <div class="client-avatar">
            <SvgIcon name="user" :size="20" />
          </div>
          <div class="client-info">
            <p class="client-name">{{ order.customerName }}</p>
            <p class="client-meta">
              Consumidor verificado CheapFood · 4.9
              <SvgIcon name="star-filled" :size="12" style="color: #f59e0b" />
            </p>
          </div>
        </div>
      </section>

      <section class="section">
        <p class="section-label">DETALHES DA RESERVA</p>
        <div class="detail-table">
          <div class="detail-row">
            <span class="detail-key">Produto</span>
            <span class="detail-val">{{ order.productName }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-key">Quantidade</span>
            <span class="detail-val"
              >{{ order.quantity }} unidade{{
                order.quantity > 1 ? "s" : ""
              }}</span
            >
          </div>
          <div class="detail-row">
            <span class="detail-key">Valor Unitário</span>
            <span class="detail-val"
              >R$
              {{
                order.price ? order.price.toFixed(2).replace(".", ",") : "--"
              }}</span
            >
          </div>
          <div class="detail-row">
            <span class="detail-key">Total da Reserva</span>
            <span class="detail-val price"
              >R$
              {{
                order.price
                  ? (order.price * order.quantity).toFixed(2).replace(".", ",")
                  : "--"
              }}</span
            >
          </div>
          <div class="detail-row">
            <span class="detail-key">Reservado em</span>
            <span class="detail-val">{{ order.createdAt || "Hoje" }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-key">Retira até</span>
            <span class="detail-val deadline"
              >Hoje até {{ order.pickupDeadline }}</span
            >
          </div>
        </div>
      </section>

      <div class="actions" v-if="order.status === 'pendente'">
        <button class="btn-confirm" @click="handleConfirm">
          <SvgIcon name="check-circle" :size="17" />
          Confirmar retirada no balcão
        </button>
        <button class="btn-cancel" @click="handleCancel">
          Cancelar pedido
        </button>
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

.code-card {
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  margin-bottom: 20px;
}

.code-label {
  font-size: 10px;
  font-weight: 700;
  color: var(--mc-text-muted);
  letter-spacing: 0.1em;
  margin-bottom: 8px;
}

.code-value {
  font-size: 36px;
  font-weight: 900;
  color: var(--mc-navy);
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
  font-weight: 700;
  color: var(--mc-text-muted);
  letter-spacing: 0.08em;
  margin-bottom: 10px;
}

.client-card {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: 16px;
  padding: 14px;
}

.client-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--mc-purple-soft);
  color: var(--mc-navy);
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
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--mc-text-muted);
  margin-top: 2px;
}

.detail-table {
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: 16px;
  padding: 14px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid var(--mc-border);
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-key {
  font-size: 13px;
  color: var(--mc-text-muted);
}

.detail-val {
  font-size: 13px;
  font-weight: 700;
  color: var(--mc-text);
}

.detail-val.price {
  color: var(--mc-green, #2a9d8f);
  font-size: 15px;
}

.detail-val.deadline {
  color: var(--cf-pink);
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
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: var(--mc-navy);
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
  border: 1px solid var(--mc-danger);
  color: var(--mc-danger);
  border-radius: 12px;
  padding: 15px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}
</style>
