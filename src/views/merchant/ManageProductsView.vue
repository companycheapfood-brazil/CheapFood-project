<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import MerchantHeader from "@/components/merchant/MerchantHeader.vue";
import MerchantBottomNav from "@/components/merchant/MerchantBottomNav.vue";
import AuctionBadge from "@/components/AuctionBadge.vue";
import { useMerchantStore } from "@/stores/useMerchantStore";
import { useToastStore } from "@/stores/useToastStore";
import { storeToRefs } from "pinia";
import { API_URL, isImageUrl, resolveImageUrl } from "@/config/api";
import { authHeaders } from "@/utils/auth";
import SvgIcon from "@/components/ui/SvgIcon.vue";

const merchantStore = useMerchantStore();
const toast = useToastStore();
const { activeProducts, expiredProducts, soldProducts } =
  storeToRefs(merchantStore);
const { togglePause, applyExtraDiscount } = merchantStore;

onMounted(() => {
  merchantStore.fetchProducts();
});

const tabs = [
  { key: "ativos", label: "Ativos" },
  { key: "vencidos", label: "Vencidos" },
  { key: "vendidos", label: "Vendidos" },
] as const;

const activeTab = ref<(typeof tabs)[number]["key"]>("ativos");

const visibleProducts = computed(() => {
  if (activeTab.value === "ativos") return activeProducts.value;
  if (activeTab.value === "vencidos") return expiredProducts.value;
  return soldProducts.value;
});

function money(v: number) {
  return `R$ ${v.toFixed(2).replace(".", ",")}`;
}

const showStopModal = ref(false);
const productToStopId = ref<string | null>(null);

function handleStopAuction(productId: string) {
  productToStopId.value = productId;
  showStopModal.value = true;
}

async function confirmStopAuction() {
  if (!productToStopId.value) return;
  try {
    const res = await fetch(
      `${API_URL}/merchant/products/${productToStopId.value}/auction/stop`,
      {
        method: "POST",
        headers: {
          ...authHeaders(),
        },
      },
    );
    if (!res.ok) throw new Error("Falha ao parar leilão");
    toast.addToast("Leilão encerrado com sucesso! Preço congelado.", "success");
    await merchantStore.fetchProducts();
    showStopModal.value = false;
    productToStopId.value = null;
  } catch (err) {
    toast.addToast("Erro ao parar leilão", "error");
  }
}

async function handleExtraDiscount(productId: string) {
  const ok = await applyExtraDiscount(productId);
  if (ok) {
    toast.addToast(
      "Desconto extra de 20% aplicado e validade renovada por +2 dias!",
      "success",
    );
    activeTab.value = "ativos";
  } else {
    toast.addToast("Não foi possível aplicar desconto extra", "error");
  }
}
</script>

<template>
  <div class="screen">
    <MerchantHeader
      title="Meus produtos"
      :subtitle="`${activeProducts.length} ativos · ${expiredProducts.length} vencidos`"
    />

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
          <span class="tab-count">
            ({{
              t.key === "ativos"
                ? activeProducts.length
                : t.key === "vencidos"
                  ? expiredProducts.length
                  : soldProducts.length
            }})
          </span>
        </button>
      </div>

      <div class="product-list">
        <div v-for="p in visibleProducts" :key="p.id" class="product-card">
          <div class="product-content">
            <div class="thumb">
              <img
                v-if="isImageUrl(p.image)"
                :src="resolveImageUrl(p.image)"
                :alt="p.name"
                class="real-image"
              /><span v-else v-html="p.image || p.icon" class="emoji-img"></span>
            </div>

            <div class="info">
              <div class="info-top">
                <p class="name">{{ p.name }}</p>
                <div class="price-pill">
                  <span class="old-price">{{ money(p.originalPrice) }}</span>
                  <strong class="promo-price">{{ money(p.promoPrice) }}</strong>
                </div>
              </div>

              <div class="badges-row">
                <span
                  class="expires-badge"
                  :class="{
                    vencido: p.status === 'vencido',
                    vendido: p.status === 'vendido',
                  }"
                >
                  {{ p.expiresLabel }}
                </span>
                <span v-if="!p.auction" class="discount-badge">
                  -{{
                    Math.round(
                      ((p.originalPrice - p.promoPrice) / p.originalPrice) * 100,
                    )
                  }}%
                </span>
                <span v-if="p.paused && p.status === 'ativo'" class="paused-badge">
                  Pausado
                </span>
              </div>

              <div v-if="p.auction" style="margin-top: 6px">
                <AuctionBadge :auction="p.auction" variant="compact" />
              </div>

              <div class="progress-track">
                <div
                  class="progress-fill"
                  :style="{
                    width: `${Math.min(100, (p.reservedCount / Math.max(1, p.quantityAvailable)) * 100)}%`,
                  }"
                ></div>
              </div>
              <p class="progress-label">
                {{ p.reservedCount }} reservadas · {{ p.quantityAvailable }} em estoque
              </p>
            </div>
          </div>

          <div class="card-actions">
            <button
              class="action-btn outline"
              @click="$router.push('/comerciante/editar/' + p.id)"
            >
              Editar
            </button>
            <button
              v-if="p.status === 'ativo'"
              class="action-btn"
              :class="{ paused: p.paused }"
              @click="togglePause(p.id)"
            >
              {{ p.paused ? "Ativar" : "Pausar" }}
            </button>
            <button
              v-if="p.status === 'ativo' && p.auction && !p.auction.ended"
              class="action-btn stop-auction"
              @click="handleStopAuction(p.id)"
            >
              Parar Leilão
            </button>
            <button
              v-else-if="p.status === 'vencido'"
              class="action-btn discount"
              @click="handleExtraDiscount(p.id)"
            >
              +20% Desconto e Reativar
            </button>
          </div>
        </div>

        <div v-if="visibleProducts.length === 0" class="empty-state">
          <div class="empty-icon">
            <SvgIcon name="shopping-bag" :size="36" />
          </div>
          <h3 class="empty-title">Nenhum produto por aqui</h3>
          <p class="empty-desc">Você ainda não tem itens nesta aba.</p>
          <button
            v-if="activeTab === 'ativos'"
            class="cta-btn"
            @click="$router.push('/comerciante/novo')"
          >
            Cadastrar primeiro produto
          </button>
        </div>
      </div>
    </main>

    <!-- Modal -->
    <div v-if="showStopModal" class="modal-overlay" @click.self="showStopModal = false">
      <div class="modal-content">
        <h3>Deseja encerrar este leilão imediatamente? O preço atual será mantido para venda direta.</h3>
        <div class="modal-actions">
          <button class="btn-cancel" @click="showStopModal = false">Cancelar</button>
          <button class="btn-confirm" @click="confirmStopAuction">Confirmar Encerramento</button>
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

.tabs {
  display: flex;
  background: var(--mc-purple-soft);
  border-radius: 999px;
  padding: 4px;
  margin-bottom: 16px;
}

.tab {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--mc-text-muted);
  font-size: 12px;
  font-weight: 700;
  padding: 10px 4px;
  border-radius: 999px;
  cursor: pointer;
}

.tab-count {
  font-size: 11px;
  opacity: 0.8;
}

.tab.active {
  background: var(--mc-surface);
  color: var(--mc-text);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.product-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.product-card {
  display: flex;
  flex-direction: column;
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: var(--cf-radius-md);
  padding: 16px;
}

.product-content {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.thumb {
  overflow: hidden;
  width: 58px;
  min-width: 58px;
  height: 58px;
  flex-shrink: 0;
  border-radius: var(--cf-radius-sm);
  background: var(--mc-purple-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.info {
  flex: 1;
  min-width: 0;
}

.info-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.name {
  font-size: 14px;
  font-weight: 800;
  color: var(--mc-navy);
}

.price-pill {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  flex-shrink: 0;
}

.old-price {
  font-size: 10px;
  color: var(--mc-text-muted);
  text-decoration: line-through;
}

.promo-price {
  font-size: 13px;
  font-weight: 800;
  color: var(--mc-green, #2a9d8f);
}

.badges-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 6px;
}

.expires-badge {
  font-size: 10px;
  font-weight: 700;
  color: #fff;
  background: var(--cf-pink);
  padding: 3px 8px;
  border-radius: 999px;
}

.expires-badge.vencido {
  background: var(--mc-danger);
}

.expires-badge.vendido {
  background: var(--mc-text-muted);
}

.discount-badge {
  font-size: 10px;
  font-weight: 700;
  color: var(--mc-navy);
  background: var(--mc-purple-soft);
  padding: 3px 8px;
  border-radius: 999px;
}

.paused-badge {
  font-size: 10px;
  font-weight: 700;
  color: #8a5300;
  background: #fff3cd;
  padding: 3px 8px;
  border-radius: 999px;
}

.progress-track {
  height: 6px;
  background: var(--mc-border);
  border-radius: 999px;
  margin-top: 12px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--cf-primary);
  border-radius: 999px;
}

.progress-label {
  font-size: 11px;
  color: var(--mc-text-muted);
  margin-top: 6px;
  font-weight: 600;
}

.card-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding-top: 16px;
  border-top: 1px dashed var(--mc-border);
}

.action-btn {
  flex: 1 1 110px;
  background: var(--mc-danger);
  color: #fff;
  border: none;
  border-radius: var(--cf-radius-sm);
  padding: 10px 8px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.action-btn.outline {
  background: transparent;
  color: var(--mc-navy);
  border: 1px solid var(--mc-border);
}

.action-btn.paused {
  background: var(--mc-navy);
}

.action-btn.stop-auction {
  background: #f6b55d;
  color: #1a1a1a;
}

.action-btn.discount {
  background: var(--cf-orange);
  color: #1a1a1a;
}

.empty-state {
  text-align: center;
  padding: 40px 12px;
  background: var(--mc-cream);
  border-radius: var(--cf-radius-md);
  border: 1px dashed var(--mc-cream-border);
  margin-top: 16px;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.empty-title {
  font-size: 16px;
  font-weight: 800;
  color: var(--mc-navy);
  margin-bottom: 6px;
}

.empty-desc {
  font-size: 13px;
  color: var(--mc-text-muted);
  margin-bottom: 24px;
}

.cta-btn {
  background: var(--mc-navy);
  color: #fff;
  border: none;
  border-radius: var(--cf-radius-sm);
  padding: 14px 20px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  width: 100%;
}

.real-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #fff;
  padding: 2px;
}
.emoji-img {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  font-size: 1.5rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: var(--mc-surface, #fff);
  padding: 24px;
  border-radius: var(--cf-radius-md, 16px);
  width: 90%;
  max-width: 400px;
  text-align: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  animation: slideUp 0.2s ease-out;
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.modal-content h3 {
  font-size: 15px;
  font-weight: 700;
  color: var(--mc-navy, #1a1a1a);
  margin-bottom: 24px;
  line-height: 1.4;
}

.modal-actions {
  display: flex;
  gap: 12px;
}

.modal-actions button {
  flex: 1;
  padding: 12px;
  border-radius: var(--cf-radius-sm, 8px);
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-cancel {
  background: transparent;
  color: var(--mc-text-muted, #666);
  border: 1px solid var(--mc-border, #eee) !important;
}

.btn-confirm {
  background: var(--mc-danger, #e74c3c);
  color: #fff;
}
</style>
