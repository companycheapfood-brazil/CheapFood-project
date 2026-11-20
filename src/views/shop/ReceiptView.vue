<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import BottomNav from "@/components/BottomNav.vue";
import SvgIcon from "@/components/ui/SvgIcon.vue";
import { useCartStore } from "@/stores/useCartStore";
import { useToastStore } from "@/stores/useToastStore";
import { formatBRL } from "@/composables/useAuctionClock";
import { API_URL } from "@/config/api";
import { authHeaders, handleUnauthorized } from "@/utils/auth";

const router = useRouter();
const route = useRoute();
const cartStore = useCartStore();
const toastStore = useToastStore();

const code = ref("");
const status = ref("pendente");
const subtotal = ref(0);
const savings = ref(0);
const storeName = ref("Padaria & Empório Central");
const storeAddress = ref("Rua São Paulo, 100 - Centro, Marília/SP");
const pickupDeadline = ref("Hoje em até 3 horas");
const isLoading = ref(true);
const notFound = ref(false);
const items = ref<{ name: string; quantity: number; price?: number; total?: number }[]>([]);

const paymentLabel = computed(() => {
  if (route.query.pay === "pix") return "PIX Instantâneo";
  if (cartStore.lastReceipt?.code === code.value && cartStore.lastReceipt?.paymentMethod === "pix") {
    return "PIX Instantâneo";
  }
  if (code.value && cartStore.getOrderPaymentMethod(code.value) === "pix") {
    return "PIX Instantâneo";
  }
  return "Pagamento na Retirada";
});

const totalUnits = computed(() =>
  items.value.reduce((acc, i) => acc + (Number(i.quantity) || 1), 0),
);

onMounted(async () => {
  const queryCode = String((route.query.code as string) || cartStore.lastReservationCode || "").trim();
  if (!queryCode) {
    notFound.value = true;
    isLoading.value = false;
    return;
  }
  code.value = queryCode;
  let loadedFromMemory = false;

  // 1. Tenta carregar do último recibo em memória imediatamente
  if (cartStore.lastReceipt && cartStore.lastReceipt.code === queryCode) {
    loadedFromMemory = true;
    subtotal.value = Number(cartStore.lastReceipt.total || 0);
    savings.value = Number(cartStore.lastReceipt.savings || 0);
    storeName.value = cartStore.lastReceipt.store;
    storeAddress.value = cartStore.lastReceipt.storeAddress;
    items.value = cartStore.lastReceipt.items.map((i) => ({
      name: i.name,
      quantity: i.quantity,
      price: i.price,
      total: i.total,
    }));
  }

  // 2. Busca dados reais da reserva pelo código no backend (funciona inclusive ao vir do Histórico!)
  try {
    const res = await fetch(`${API_URL}/orders/code/${encodeURIComponent(queryCode)}`, {
      headers: authHeaders(),
    });
    if (handleUnauthorized(res.status)) return;
    if (res.ok) {
      const data = await res.json().catch(() => null);
      if (data) {
        code.value = data.code || queryCode;
        status.value = data.status || "pendente";
        subtotal.value = Number(data.total ?? 0) || 0;
        savings.value = Number(data.savings ?? 0) || 0;
        storeName.value = data.store || storeName.value;
        storeAddress.value = data.storeAddress || storeAddress.value;
        pickupDeadline.value = data.pickupDeadline || pickupDeadline.value;
        if (Array.isArray(data.items) && data.items.length > 0) {
          items.value = data.items;
        }
      }
    } else if (!loadedFromMemory) {
      notFound.value = true;
    }
  } catch (e) {
    console.error(e);
    if (!loadedFromMemory) {
      notFound.value = true;
    }
  } finally {
    isLoading.value = false;
  }
});

async function copyCode() {
  if (!code.value) return;
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(code.value);
      toastStore.addToast(`Código ${code.value} copiado!`, "success");
      return;
    }
    const ta = document.createElement("textarea");
    ta.value = code.value;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
    toastStore.addToast(`Código ${code.value} copiado!`, "success");
  } catch {
    toastStore.addToast("Não foi possível copiar o código automaticamente.", "error");
  }
}

function shareOnWhatsApp() {
  const itemList = items.value.map((i) => `• ${i.quantity}x ${i.name}`).join("\n");
  const msg =
`🌱 *Comprovante de Reserva - CheapFood*
📌 *Código de Retirada:* ${code.value}
🏬 *Local:* ${storeName.value}
📍 *Endereço:* ${storeAddress.value}
⏰ *Prazo:* ${pickupDeadline.value}

🛒 *Itens do Pedido:*
${itemList || "1x Cesta de Produtos"}

💰 *Total a pagar:* ${formatBRL(subtotal.value)}
✨ *Economia gerada:* ${formatBRL(savings.value)}

Apresente este código no balcão da loja para retirar seus produtos frescos com desconto!`;

  const url = `https://api.whatsapp.com/send?text=${encodeURIComponent(msg)}`;
  window.open(url, "_blank");
}

function printReceipt() {
  window.print();
}
</script>

<template>
  <div class="screen">
    <header class="receipt-header">
      <button class="header-back" @click="router.back()" aria-label="Voltar">
        <SvgIcon name="arrow-left" :size="18" />
      </button>
      <h1 class="header-title">Comprovante</h1>
      <span class="header-badge">{{ totalUnits }} {{ totalUnits === 1 ? "item" : "itens" }}</span>
    </header>

    <main class="content">
      <div v-if="isLoading" class="summary-card" style="text-align: center; padding: 2rem;">
        <p class="subtitle" style="margin: 0;">Carregando comprovante...</p>
      </div>

      <div v-else-if="notFound" class="summary-card" style="text-align: center; padding: 2rem;">
        <h2 class="title" style="margin-bottom: 0.5rem;">Comprovante não encontrado</h2>
        <p class="subtitle">Não encontramos uma reserva ativa com este código.</p>
        <div class="actions-stack">
          <button class="primary-btn" @click="router.push('/perfil/historico')">
            Ver em Meus Pedidos
          </button>
          <button class="back-btn" @click="router.push('/')">
            Voltar ao início
          </button>
        </div>
      </div>

      <template v-else>
      <div class="success-icon-container">
        <div class="success-circle">
          <svg
            width="40"
            height="40"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#2ecc71"
            stroke-width="3"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        </div>
      </div>

      <h2 class="title">
        {{
          status === "retirado"
            ? "Pedido Retirado!"
            : status === "expirado"
              ? "Reserva Cancelada / Expirada"
              : "Reserva confirmada!"
        }}
      </h2>
      <p class="subtitle">{{ pickupDeadline }}</p>

      <div class="summary-card">
        <div class="store-pickup-box">
          <p class="store-title">
            <SvgIcon name="map-pin" :size="13" />
            <span>Local de Retirada</span>
          </p>
          <p class="store-name">{{ storeName }}</p>
          <p class="store-addr">{{ storeAddress }}</p>
        </div>

        <hr class="divider" />

        <div class="item-list">
          <div class="item-row" v-for="(item, idx) in items" :key="idx">
            <span class="item-value">{{ item.quantity }}x {{ item.name }}</span>
            <span v-if="item.total !== undefined" class="item-price">
              {{ formatBRL(item.total) }}
            </span>
          </div>
        </div>

        <div class="summary-row mt">
          <span class="label">Forma de pagamento</span>
          <span class="value">{{ paymentLabel }}</span>
        </div>
        <div class="summary-row">
          <span class="label">Subtotal</span>
          <span class="value">{{ formatBRL(subtotal) }}</span>
        </div>
        <div class="summary-row">
          <span class="label">Economia total</span>
          <span class="value pink">- {{ formatBRL(savings) }}</span>
        </div>

        <hr class="divider" />

        <div class="summary-row total-row">
          <span class="label">Total a pagar</span>
          <span class="value">{{ formatBRL(subtotal) }}</span>
        </div>

        <div v-if="savings > 0" class="savings-badge">
          <SvgIcon name="leaf" :size="15" />
          <span>Economizou {{ formatBRL(savings) }} evitando desperdício!</span>
        </div>
      </div>

      <div class="code-card" @click="copyCode" title="Toque para copiar">
        <span class="code-label">APRESENTE ESTE CÓDIGO NO BALCÃO</span>
        <h1 class="code-value">{{ code }}</h1>
        <div class="qr-box">
          <svg
            width="92"
            height="92"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#1a1a1a"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect x="3" y="3" width="7" height="7" />
            <rect x="14" y="3" width="7" height="7" />
            <rect x="14" y="14" width="7" height="7" />
            <rect x="3" y="14" width="7" height="7" />
            <path d="M7 7h.01" />
            <path d="M17 7h.01" />
            <path d="M7 17h.01" />
            <path d="M17 17h.01" />
            <path d="M12 3v4" />
            <path d="M12 12h2" />
            <path d="M12 16v5" />
            <path d="M3 12h4" />
          </svg>
        </div>
        <span class="copy-hint">Toque para copiar o código</span>
      </div>

      <div class="actions-stack">
        <div class="quick-share-grid">
          <button class="share-btn whatsapp" @click="shareOnWhatsApp">
            <SvgIcon name="smartphone" :size="16" />
            <span>Compartilhar WhatsApp</span>
          </button>
          <button class="share-btn print" @click="printReceipt">
            <SvgIcon name="file-text" :size="16" />
            <span>Imprimir / PDF</span>
          </button>
        </div>

        <button class="primary-btn" @click="router.push('/perfil/historico')">
          Ver em Meus Pedidos
        </button>
        <button class="back-btn" @click="router.push('/')">
          Voltar ao início
        </button>
      </div>
      </template>
    </main>

    <BottomNav />
  </div>
</template>

<style scoped>
.screen {
  background-color: #fbfaf8;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.receipt-header {
  background: linear-gradient(135deg, #f6b55d 0%, #f5a623 100%);
  padding: 1.8rem 1.5rem 1.4rem 1.5rem;
  border-bottom-left-radius: 24px;
  border-bottom-right-radius: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  box-shadow: 0 8px 24px rgba(245, 166, 35, 0.22);
}

.header-back {
  width: 36px;
  height: 36px;
  padding: 0;
  line-height: 0;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.88);
  color: #333;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.header-title {
  font-size: 1.3rem;
  font-weight: 900;
  color: #1f160a;
  margin: 0;
  flex: 1;
}

.header-badge {
  background: linear-gradient(135deg, #ff3b69 0%, #e02854 100%);
  color: white;
  padding: 0.35rem 0.85rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 800;
  box-shadow: 0 4px 10px rgba(255, 59, 105, 0.3);
}

.content {
  padding: 1.4rem 1.25rem;
  flex: 1;
  overflow-y: auto;
  padding-bottom: 100px;
}

.success-icon-container {
  display: flex;
  justify-content: center;
  margin-top: 0.3rem;
  margin-bottom: 0.8rem;
}

.success-circle {
  width: 74px;
  height: 74px;
  border-radius: 50%;
  background: linear-gradient(135deg, #eafbe4 0%, #d4f8c8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 20px rgba(46, 204, 113, 0.25);
  border: 2px solid #ffffff;
}

.title {
  text-align: center;
  font-size: 1.4rem;
  font-weight: 900;
  color: #1f160a;
  margin: 0 0 0.25rem 0;
}

.subtitle {
  text-align: center;
  font-size: 0.88rem;
  color: #a0845a;
  margin: 0 0 1.2rem 0;
  font-weight: 700;
}

.summary-card {
  background: linear-gradient(135deg, #fffdf8 0%, #fdf6e9 100%);
  border: 1px solid #f0dfb8;
  border-radius: 20px;
  padding: 1.3rem;
  margin-bottom: 1.3rem;
  box-shadow: 0 8px 22px rgba(160, 132, 90, 0.14);
}

.store-pickup-box {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.store-title {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  color: #a0845a;
}
.store-name {
  font-size: 0.96rem;
  font-weight: 900;
  color: #2b2111;
}
.store-addr {
  font-size: 0.8rem;
  color: #6b5a3e;
}

.item-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-bottom: 1rem;
}

.item-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.88rem;
}

.item-value {
  font-weight: 700;
  color: #2b2111;
}

.item-price {
  font-weight: 800;
  color: #5c3809;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.summary-row.mt {
  margin-top: 1.2rem;
}

.summary-row .label {
  color: #8c7148;
  font-weight: 600;
}

.summary-row .value {
  font-weight: 800;
  color: #2b2111;
}

.summary-row .value.pink {
  color: #ff3b69;
}

.divider {
  border: none;
  border-top: 1px dashed #dcb985;
  margin: 0.9rem 0;
}

.total-row {
  font-size: 1.12rem;
}

.total-row .label {
  font-weight: 900;
  color: #1f160a;
}

.savings-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: linear-gradient(135deg, #ff3b69 0%, #e02854 100%);
  color: white;
  text-align: center;
  padding: 0.65rem 0.9rem;
  border-radius: 999px;
  font-weight: 800;
  font-size: 0.82rem;
  margin-top: 1.1rem;
  box-shadow: 0 4px 12px rgba(255, 59, 105, 0.3);
}

.code-card {
  border: 2px dashed #ff3b69;
  border-radius: 20px;
  padding: 1.35rem;
  text-align: center;
  margin-bottom: 1.4rem;
  background: linear-gradient(180deg, #fff5f7 0%, #ffeef2 100%);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 6px 18px rgba(255, 59, 105, 0.1);
  transition: transform 0.15s ease;
}

.code-card:active {
  transform: scale(0.98);
}

.code-label {
  color: #ff3b69;
  font-size: 0.76rem;
  font-weight: 900;
  letter-spacing: 0.8px;
}

.code-value {
  color: #ff3b69;
  font-size: 2.5rem;
  font-weight: 900;
  letter-spacing: 5px;
  margin: 0.35rem 0 0.6rem 0;
}

.qr-box {
  background: #ffffff;
  padding: 12px;
  border-radius: 14px;
  border: 1px solid #ffd0dc;
  margin-bottom: 8px;
  box-shadow: 0 4px 10px rgba(255, 59, 105, 0.08);
}

.copy-hint {
  font-size: 0.76rem;
  color: #a33b56;
  font-weight: 700;
}

.actions-stack {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.primary-btn {
  width: 100%;
  background: linear-gradient(135deg, #f7b75e 0%, #f5a623 100%);
  color: #4a2c05;
  padding: 1.05rem;
  border: none;
  border-radius: 16px;
  font-size: 0.98rem;
  font-weight: 900;
  cursor: pointer;
  box-shadow: 0 6px 16px rgba(245, 166, 35, 0.28);
}

.back-btn {
  width: 100%;
  background-color: #ffffff;
  color: #ff3b69;
  padding: 1rem;
  border: 2px solid #ff3b69;
  border-radius: 16px;
  font-size: 0.98rem;
  font-weight: 800;
  cursor: pointer;
}

.quick-share-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 4px;
}

.share-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 0.85rem 0.75rem;
  border-radius: 14px;
  font-size: 0.82rem;
  font-weight: 800;
  cursor: pointer;
  border: 1px solid transparent;
  transition: transform 0.15s ease;
}

.share-btn:hover {
  transform: translateY(-1px);
}

.share-btn.whatsapp {
  background: #25d366;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(37, 211, 102, 0.25);
}

.share-btn.print {
  background: #ffffff;
  color: #374151;
  border-color: #d1d5db;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

@media print {
  .receipt-header,
  .actions-stack,
  .bottom-nav,
  .copy-hint {
    display: none !important;
  }

  .screen {
    background: #ffffff !important;
  }

  .summary-card,
  .code-card {
    border: 1px solid #ccc !important;
    box-shadow: none !important;
  }
}
</style>
