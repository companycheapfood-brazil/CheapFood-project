<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import MerchantHeader from "@/components/merchant/MerchantHeader.vue";
import MerchantBottomNav from "@/components/merchant/MerchantBottomNav.vue";
import SvgIcon from "@/components/ui/SvgIcon.vue";
import { useMerchantStore } from "@/stores/useMerchantStore";
import { useToastStore } from "@/stores/useToastStore";
import { formatBRL } from "@/composables/useAuctionClock";
import { storeToRefs } from "pinia";

const route = useRoute();
const router = useRouter();
const showEmptyState = computed(() => route.query.new === "1");

const merchantStore = useMerchantStore();
const toast = useToastStore();
const { stats, storeInfo } = storeToRefs(merchantStore);

const activePeriod = ref("7days");

const periodLabels: Record<string, string> = {
  today: "Hoje",
  "7days": "Últimos 7 dias",
  month: "Este Mês",
  year: "Este Ano",
};

const subtitleText = computed(() => periodLabels[activePeriod.value]);

const isLoading = ref(true);

// Modal Validar PIN
const showPinModal = ref(false);
const pinInput = ref("");
const pinOrderResult = ref<any | null>(null);
const isValidatingPin = ref(false);

// Modal Exportar Relatório
const showReportModal = ref(false);

// Resposta às avaliações
const replyingReviewId = ref<number | null>(null);
const replyText = ref("");
const isSavingReply = ref(false);

function startReply(rev: any) {
  replyingReviewId.value = rev.id;
  replyText.value = rev.merchantReply || "";
}

async function saveReply(revId: number) {
  if (isSavingReply.value) return;
  if (!replyText.value.trim()) {
    toast.addToast("Digite uma resposta antes de enviar.", "error");
    return;
  }
  isSavingReply.value = true;
  const ok = await merchantStore.replyToReview(revId, replyText.value.trim());
  isSavingReply.value = false;
  if (ok) {
    replyingReviewId.value = null;
    replyText.value = "";
  }
}

watch(activePeriod, async (newPeriod) => {
  isLoading.value = true;
  await merchantStore.fetchDashboardStats(newPeriod);
  isLoading.value = false;
});

onMounted(async () => {
  isLoading.value = true;
  await Promise.all([
    merchantStore.fetchDashboardStats(activePeriod.value),
    merchantStore.fetchStoreInfo(),
  ]);
  isLoading.value = false;
});

const maxSales = computed(() =>
  Math.max(1, ...stats.value.dailySales.map((d) => Number(d.value) || 0)),
);

const averageTicket = computed(() => {
  const count = Number(stats.value.completedOrdersCount || 0);
  if (count <= 0) return 0;
  return Number(stats.value.revenueRecovered || 0) / count;
});

const isNegativeGrowth = computed(() =>
  String(stats.value.growth ?? "").trim().startsWith("-"),
);

const isProPlan = computed(() => {
  const p = storeInfo.value.plan || stats.value.plan;
  return p === "monthly" || p === "annual";
});

function openPinModal() {
  pinInput.value = "";
  pinOrderResult.value = null;
  showPinModal.value = true;
}

async function handleLookupPin() {
  if (pinInput.value.trim().length < 3 || isValidatingPin.value) return;
  isValidatingPin.value = true;
  pinOrderResult.value = await merchantStore.validateOrderPin(
    pinInput.value.trim(),
    false,
  );
  isValidatingPin.value = false;
}

async function handleConfirmPinPickup() {
  if (!pinOrderResult.value || isValidatingPin.value) return;
  isValidatingPin.value = true;
  const updated = await merchantStore.validateOrderPin(
    pinOrderResult.value.code,
    true,
    activePeriod.value,
  );
  isValidatingPin.value = false;
  if (updated) {
    pinOrderResult.value = updated;
  }
}

function printReport() {
  window.print();
}
</script>

<template>
  <div class="screen">
    <MerchantHeader
      :title="`Dashboard - ${storeInfo.name || stats.storeName || 'Padaria Central'}`"
      :subtitle="subtitleText"
    />

    <main class="content" v-if="!showEmptyState">
      <!-- Barra de Ações Rápidas do Balcão -->
      <div class="quick-actions-bar">
        <button class="quick-btn primary" @click="openPinModal">
          <SvgIcon name="key" size="18" />
          <span>Validar PIN de Retirada</span>
        </button>
        <button class="quick-btn secondary" @click="showReportModal = true">
          <SvgIcon name="file-text" size="18" />
          <span>Exportar Relatório</span>
        </button>
      </div>

      <div class="filter-tabs">
        <button
          :class="{ active: activePeriod === 'today' }"
          @click="activePeriod = 'today'"
        >
          Hoje
        </button>
        <button
          :class="{ active: activePeriod === '7days' }"
          @click="activePeriod = '7days'"
        >
          7 Dias
        </button>
        <button
          :class="{ active: activePeriod === 'month' }"
          @click="activePeriod = 'month'"
        >
          Este Mês
        </button>
        <button
          :class="{ active: activePeriod === 'year' }"
          @click="activePeriod = 'year'"
        >
          Este Ano
        </button>
      </div>

      <div class="stats-row">
        <div class="stat-card" :class="{ skeleton: isLoading }">
          <p class="stat-value" v-if="!isLoading">{{ stats.activeProducts }}</p>
          <p class="stat-label" v-if="!isLoading">Produtos ativos</p>
        </div>
        <div class="stat-card highlight" :class="{ skeleton: isLoading }">
          <p class="stat-value" v-if="!isLoading">
            {{ formatBRL(stats.revenueRecovered) }}
          </p>
          <p class="stat-label" v-if="!isLoading">Receita recuperada</p>
        </div>
        <div class="stat-card" :class="{ skeleton: isLoading }">
          <p class="stat-value" v-if="!isLoading">{{ stats.reservations }}</p>
          <p class="stat-label" v-if="!isLoading">Reservas pendentes</p>
        </div>
      </div>

      <!-- Métricas Adicionais Superiores -->
      <div class="stats-row extra-stats-three">
        <div class="stat-card" :class="{ skeleton: isLoading }">
          <p class="stat-value" v-if="!isLoading">
            {{ formatBRL(averageTicket) }}
          </p>
          <p class="stat-label" v-if="!isLoading">Ticket Médio</p>
        </div>
        <div class="stat-card" :class="{ skeleton: isLoading }">
          <p
            class="stat-value"
            :class="isNegativeGrowth ? 'growth-negative' : 'growth-positive'"
            v-if="!isLoading"
          >
            {{ stats.growth || "0%" }}
          </p>
          <p class="stat-label" v-if="!isLoading">Crescimento</p>
        </div>
        <div class="stat-card" :class="{ skeleton: isLoading }">
          <p class="stat-value rating-gold" v-if="!isLoading" style="display: inline-flex; align-items: center; gap: 4px;">
            <SvgIcon name="star-filled" :size="15" />
            <span>{{
              stats.ratingCount > 0
                ? Number(stats.ratingAverage).toFixed(1).replace(".", ",")
                : "--"
            }}</span>
          </p>
          <p class="stat-label" v-if="!isLoading">
            Avaliação ({{ stats.ratingCount || 0 }})
          </p>
        </div>
      </div>

      <!-- Card de Impacto Ambiental & Sustentabilidade (ESG) -->
      <section class="esg-card">
        <div class="esg-header">
          <span class="esg-badge" style="display: inline-flex; align-items: center; gap: 5px;">
            <SvgIcon name="leaf" :size="14" />
            <span>Impacto Sustentável (ODS 12 ONU)</span>
          </span>
          <span class="esg-period">{{ subtitleText }}</span>
        </div>
        <div class="esg-grid">
          <div class="esg-metric">
            <strong class="esg-val">{{ stats.foodSavedKg || 0 }} kg</strong>
            <span class="esg-lbl">Alimentos salvos</span>
          </div>
          <div class="esg-divider"></div>
          <div class="esg-metric">
            <strong class="esg-val">{{ stats.co2AvoidedKg || 0 }} kg</strong>
            <span class="esg-lbl">CO₂ evitado</span>
          </div>
          <div class="esg-divider"></div>
          <div class="esg-metric">
            <strong class="esg-val">{{ stats.itemsSaved || 0 }} un.</strong>
            <span class="esg-lbl">Itens entregues</span>
          </div>
        </div>
      </section>

      <section class="chart-card">
        <div class="chart-header">
          <div>
            <p class="chart-title">Faturamento Recuperado</p>
            <span class="chart-subtitle">{{ subtitleText }}</span>
          </div>
          <div class="chart-total">
            Total:
            <strong
              >R$
              {{ stats.revenueRecovered.toFixed(2).replace(".", ",") }}</strong
            >
          </div>
        </div>

        <div class="chart-area">
          <!-- Background Grid Lines -->
          <div class="chart-grid">
            <div class="grid-line"></div>
            <div class="grid-line"></div>
            <div class="grid-line"></div>
            <div class="grid-line"></div>
          </div>

          <div class="chart-bars">
            <div
              v-for="(d, i) in stats.dailySales"
              :key="d.label"
              class="bar-col group"
            >
              <!-- Hover Tooltip -->
              <div class="tooltip">
                <span class="tooltip-label">{{ d.label }}</span>
                <span class="tooltip-val">R$ {{ d.value.toFixed(2).replace(".", ",") }}</span>
              </div>
              
              <span class="bar-value" v-if="d.value > 0">{{
                d.value >= 1000
                  ? (d.value / 1000).toFixed(1) + "k"
                  : Math.round(d.value)
              }}</span>
              <span class="bar-value zero" v-else>-</span>
              <div class="bar-track">
                <div
                  class="bar"
                  :class="{ peak: d.value === maxSales && d.value > 0 }"
                  :style="{
                    height: `${Math.min(100, (d.value / maxSales) * 100)}%`,
                    minHeight: d.value > 0 ? '14px' : '6px',
                  }"
                ></div>
              </div>
              <span
                class="bar-label"
                :class="{ today: i === stats.dailySales.length - 1 }"
                >{{ d.label }}</span
              >
            </div>
          </div>
        </div>

        <div class="chart-footer">
          <div class="indicator">
            <span class="dot peak-dot"></span> Maior Faturamento
          </div>
          <div class="indicator"><span class="dot"></span> Período Regular</div>
        </div>
      </section>

      <!-- Seção de Avaliações Reais dos Clientes -->
      <section class="merchant-reviews-card" v-if="stats.recentReviews && stats.recentReviews.length > 0">
        <div class="m-reviews-header">
          <div>
            <p class="m-reviews-title" style="display: inline-flex; align-items: center; gap: 6px;">
              <SvgIcon name="star-filled" :size="16" style="color: #f5a623" />
              <span>Avaliações dos Clientes</span>
            </p>
            <span class="m-reviews-sub" style="display: block">
              Média {{ Number(stats.ratingAverage || 5).toFixed(1).replace(".", ",") }} de 5,0 ({{ stats.ratingCount }} avaliações)
            </span>
          </div>
        </div>

        <div class="m-reviews-list">
          <div
            v-for="rev in stats.recentReviews.slice(0, 4)"
            :key="rev.id"
            class="m-review-item"
          >
            <div class="m-rev-top">
              <div class="m-rev-avatar">{{ rev.initials || "CF" }}</div>
              <div class="m-rev-info">
                <strong>{{ rev.author }}</strong>
                <span>{{ rev.productName }} • {{ rev.dateFormatted }}</span>
              </div>
              <span class="m-rev-stars" style="display: inline-flex; align-items: center; gap: 2px; color: #f5a623;">
                <SvgIcon
                  v-for="s in (rev.rating || 5)"
                  :key="s"
                  name="star-filled"
                  :size="12"
                />
              </span>
            </div>

            <p class="m-rev-comment">“{{ rev.comment }}”</p>

            <div v-if="rev.merchantReply && replyingReviewId !== rev.id" class="m-rev-reply-box">
              <div class="m-rev-reply-head">
                <strong>Sua resposta:</strong>
                <button class="m-rev-link-btn" @click="startReply(rev)">Editar</button>
              </div>
              <p>{{ rev.merchantReply }}</p>
            </div>

            <div v-else-if="replyingReviewId === rev.id" class="m-rev-editor">
              <textarea
                v-model="replyText"
                rows="2"
                placeholder="Escreva uma resposta para o cliente..."
              ></textarea>
              <div class="m-rev-editor-btns">
                <button class="m-rev-cancel" @click="replyingReviewId = null">Cancelar</button>
                <button class="m-rev-save" :disabled="isSavingReply" @click="saveReply(rev.id)">
                  {{ isSavingReply ? "Salvando..." : "Salvar Resposta" }}
                </button>
              </div>
            </div>

            <button
              v-else
              class="m-rev-reply-trigger"
              style="display: inline-flex; align-items: center; gap: 5px;"
              @click="startReply(rev)"
            >
              <SvgIcon name="message-square" :size="13" />
              <span>Responder avaliação</span>
            </button>
          </div>
        </div>
      </section>

      <div
        v-if="stats.expiringSoon > 0"
        class="alert-banner"
        @click="router.push('/comerciante/produtos')"
        style="cursor: pointer"
      >
        <svg
          style="margin-right: 4px; vertical-align: middle"
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path
            d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"
          />
          <line x1="12" y1="9" x2="12" y2="13" />
          <line x1="12" y1="17" x2="12.01" y2="17" />
        </svg>
        {{ stats.expiringSoon }} produto(s) vencem nos próximos dias — clique para gerenciar ofertas!
      </div>
    </main>

    <main class="content empty-content" v-if="showEmptyState">
      <div class="empty-state">
        <div class="empty-icon" style="display: flex; align-items: center; justify-content: center; color: #1e1b6e;">
          <SvgIcon name="store" :size="44" />
        </div>
        <h2 class="empty-title">Bem-vindo ao CheapFood!</h2>
        <p class="empty-desc">
          Cadastre seu primeiro produto com desconto e comece a recuperar
          receita ainda hoje.
        </p>

        <div class="how-it-works">
          <h4 class="how-title">Como funciona:</h4>
          <div class="step">
            <span class="step-num">1</span>
            <p>Cadastre produtos próximos ao vencimento</p>
          </div>
          <div class="step">
            <span class="step-num">2</span>
            <p>Clientes da região reservam com desconto</p>
          </div>
          <div class="step">
            <span class="step-num">3</span>
            <p>Confirme a retirada e recupere receita</p>
          </div>
        </div>

        <button class="cta-btn" @click="router.push('/comerciante/novo')">
          Cadastrar primeiro produto
        </button>
      </div>
    </main>

    <!-- MODAL: VALIDAR PIN DE RETIRADA -->
    <div
      v-if="showPinModal"
      class="modal-overlay"
      @click.self="showPinModal = false"
    >
      <div class="modal-card">
        <h3 class="modal-title" style="display: flex; align-items: center; gap: 7px;">
          <SvgIcon name="key" :size="18" />
          <span>Validar Código PIN</span>
        </h3>
        <p class="modal-desc">
          Digite o código de 4 caracteres apresentado pelo cliente no comprovante (ex.: <strong>CF26</strong> ou <strong>B9K4</strong>):
        </p>

        <div class="pin-search-row">
          <input
            v-model="pinInput"
            type="text"
            maxlength="6"
            placeholder="Ex: CF26"
            class="pin-input"
            @keyup.enter="handleLookupPin"
          />
          <button
            class="pin-lookup-btn"
            :disabled="isValidatingPin || pinInput.trim().length < 3"
            @click="handleLookupPin"
          >
            {{ isValidatingPin ? "..." : "Buscar" }}
          </button>
        </div>

        <div v-if="pinOrderResult" class="pin-result-box">
          <div class="pin-result-top">
            <div>
              <p class="pin-customer">{{ pinOrderResult.customerName }}</p>
              <p class="pin-date">Reserva: {{ pinOrderResult.createdAt }}</p>
            </div>
            <span class="pin-status" :class="pinOrderResult.status" style="display: inline-flex; align-items: center; gap: 4px;">
              <SvgIcon v-if="pinOrderResult.status === 'retirado'" name="check-circle" :size="12" />
              <SvgIcon v-else-if="pinOrderResult.status === 'expirado'" name="x" :size="12" />
              <span>{{
                pinOrderResult.status === "pendente"
                  ? "Aguardando Retirada"
                  : pinOrderResult.status === "retirado"
                    ? "Já Retirado"
                    : "Cancelado / Expirado"
              }}</span>
            </span>
          </div>

          <div class="pin-items">
            <div
              v-for="item in pinOrderResult.items"
              :key="item.orderId"
              class="pin-item-line"
            >
              <span>{{ item.quantity }}x {{ item.productName }}</span>
              <strong>{{ formatBRL(item.total) }}</strong>
            </div>
          </div>

          <div class="pin-total-row">
            <span>Total a receber / validar</span>
            <strong>{{ formatBRL(pinOrderResult.total) }}</strong>
          </div>

          <button
            v-if="pinOrderResult.status === 'pendente'"
            class="pin-confirm-btn"
            style="display: inline-flex; align-items: center; justify-content: center; gap: 6px;"
            :disabled="isValidatingPin"
            @click="handleConfirmPinPickup"
          >
            <SvgIcon name="check-circle" :size="15" />
            <span>Confirmar Entrega ao Cliente</span>
          </button>
        </div>

        <div class="modal-footer-btns">
          <button class="btn-close-modal" @click="showPinModal = false">
            Fechar
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL: RELATÓRIO EXECUTIVO & ESG -->
    <div
      v-if="showReportModal"
      class="modal-overlay"
      @click.self="showReportModal = false"
    >
      <div class="modal-card report-modal">
        <div class="report-badge">
          {{ isProPlan ? "RELATÓRIO GERENCIAL CHEAPFOOD PRO" : "RELATÓRIO GERENCIAL CHEAPFOOD" }}
        </div>
        <h3 class="modal-title">{{ storeInfo.name || stats.storeName || "Estabelecimento" }}</h3>
        <p class="modal-desc">
          Período analisado: <strong>{{ subtitleText }}</strong>
          <template v-if="storeInfo.cnpj"> · CNPJ: {{ storeInfo.cnpj }}</template>
        </p>

        <div class="report-table">
          <div class="report-row">
            <span>Receita Recuperada no Período</span>
            <strong class="green"
              >R$ {{ stats.revenueRecovered.toFixed(2).replace(".", ",") }}</strong
            >
          </div>
          <div class="report-row">
            <span>Crescimento vs. Período Anterior</span>
            <strong>{{ stats.growth }}</strong>
          </div>
          <div class="report-row">
            <span>Unidades Resgatadas por Clientes</span>
            <strong>{{ stats.itemsSaved }} unidades</strong>
          </div>
          <div class="report-row">
            <span>Alimentos Salvos do Desperdício</span>
            <strong class="green">{{ stats.foodSavedKg }} kg</strong>
          </div>
          <div class="report-row">
            <span>Emissões de CO₂ Evitadas (Estimativa FAO)</span>
            <strong class="green">{{ stats.co2AvoidedKg }} kg CO₂e</strong>
          </div>
          <div class="report-row">
            <span>Produtos Ativos na Vitrine Hoje</span>
            <strong>{{ stats.activeProducts }} ofertas</strong>
          </div>
        </div>

        <div class="modal-footer-btns two-cols">
          <button class="btn-close-modal" @click="showReportModal = false">
            Fechar
          </button>
          <button
            class="btn-print"
            style="display: inline-flex; align-items: center; justify-content: center; gap: 6px;"
            @click="printReport"
          >
            <SvgIcon name="printer" :size="15" />
            <span>Imprimir / Salvar PDF</span>
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

.quick-actions-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 14px;
}

.quick-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  border-radius: 12px;
  padding: 11px 12px;
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
  transition: transform 0.15s ease;
}

.quick-btn:hover {
  transform: translateY(-1px);
}

.quick-btn.primary {
  background: var(--mc-navy);
  color: #fff;
  box-shadow: 0 4px 10px rgba(27, 59, 95, 0.2);
}

.quick-btn.secondary {
  background: var(--mc-surface);
  color: var(--mc-navy);
  border: 1px solid var(--mc-border);
}

.stats-row {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
}

.stat-card {
  flex: 1;
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: var(--cf-radius-md);
  padding: 14px 10px;
  text-align: center;
}

.stat-card.highlight .stat-value {
  color: var(--mc-navy);
}

.stat-value {
  font-size: 18px;
  font-weight: 800;
}

.stat-value.growth-positive {
  color: var(--mc-green, #2a9d8f);
}

.stat-value.growth-negative {
  color: var(--mc-danger, #d92d3f);
}

.stat-label {
  font-size: 10px;
  color: var(--mc-text-muted);
  margin-top: 4px;
}

.esg-card {
  background: linear-gradient(135deg, #e8f8f5 0%, #f4fbf9 100%);
  border: 1px solid #b8e6dc;
  border-radius: var(--cf-radius-md);
  padding: 14px 16px;
  margin-bottom: 16px;
}

.esg-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.esg-badge {
  font-size: 11px;
  font-weight: 800;
  color: #146c54;
}

.esg-period {
  font-size: 10px;
  font-weight: 700;
  color: #2a9d8f;
}

.esg-grid {
  display: flex;
  align-items: center;
  justify-content: space-around;
}

.esg-metric {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.esg-val {
  font-size: 16px;
  font-weight: 900;
  color: #146c54;
}

.esg-lbl {
  font-size: 10px;
  color: #4a7c6f;
  margin-top: 2px;
  font-weight: 600;
}

.esg-divider {
  width: 1px;
  height: 28px;
  background: #b8e6dc;
}

.chart-card {
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: var(--cf-radius-md);
  padding: 16px;
  margin-bottom: 16px;
}

.extra-stats {
  margin-bottom: 14px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
}

.chart-title {
  font-size: 15px;
  font-weight: 800;
  color: var(--mc-navy);
  margin: 0 0 4px 0;
}

.chart-subtitle {
  font-size: 11px;
  color: var(--mc-text-muted);
  font-weight: 600;
  background: var(--cf-bg);
  padding: 4px 8px;
  border-radius: 12px;
}

.chart-total {
  font-size: 12px;
  color: var(--mc-text-muted);
  background-color: var(--cf-card-soft);
  padding: 6px 12px;
  border-radius: 20px;
  border: 1px solid var(--mc-cream-border);
}

.chart-total strong {
  color: var(--cf-primary);
  font-weight: 800;
  font-size: 14px;
}

.chart-area {
  position: relative;
  height: 220px;
  margin-top: 20px;
}

.chart-grid {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 30px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  z-index: 0;
}

.grid-line {
  border-top: 1px dashed rgba(0, 0, 0, 0.06);
  width: 100%;
}

.chart-bars {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 8px;
  padding: 0 10px;
  z-index: 1;
}

.bar-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  height: 100%;
  position: relative;
  cursor: pointer;
}

.tooltip {
  position: absolute;
  top: -40px;
  background: #333;
  color: #fff;
  padding: 6px 10px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 11px;
  opacity: 0;
  transform: translateY(10px) scale(0.9);
  pointer-events: none;
  transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  white-space: nowrap;
  z-index: 10;
}

.tooltip::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 50%;
  transform: translateX(-50%);
  border-width: 4px 4px 0;
  border-style: solid;
  border-color: #333 transparent transparent transparent;
}

.bar-col:hover .tooltip {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.tooltip-label {
  color: #aaa;
  font-size: 9px;
  text-transform: uppercase;
  margin-bottom: 2px;
}

.tooltip-val {
  font-weight: 700;
  font-size: 12px;
}

.bar-value {
  font-size: 12px;
  font-weight: 800;
  color: var(--mc-navy);
  margin-bottom: 8px;
  transition: opacity 0.2s ease;
}

.bar-col:hover .bar-value {
  opacity: 0;
}

.bar-value.zero {
  color: #ccc;
  font-weight: 500;
}

.bar-track {
  flex: 1;
  width: 100%;
  min-height: 0;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.bar {
  width: 100%;
  max-width: 36px;
  background: linear-gradient(180deg, #dce4ec 0%, #eef2f6 100%);
  border-radius: 8px 8px 3px 3px;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.bar.peak {
  background: linear-gradient(180deg, var(--cf-primary) 0%, #ff7a45 100%);
  box-shadow: 0 6px 14px rgba(255, 107, 107, 0.25);
}

.bar-col:hover .bar {
  filter: brightness(1.05);
  transform: translateY(-4px) scaleX(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.bar-col:hover .bar.peak {
  box-shadow: 0 8px 18px rgba(255, 107, 107, 0.4);
}

.bar-label {
  font-size: 12px;
  color: var(--mc-text-muted);
  margin-top: 12px;
  font-weight: 600;
}

.bar-label.today {
  color: var(--mc-navy);
  font-weight: 800;
  background: #f0f0f0;
  padding: 4px 8px;
  border-radius: 8px;
}

.chart-footer {
  display: flex;
  gap: 20px;
  margin-top: 30px;
  padding-top: 16px;
  border-top: 1px dashed var(--mc-border);
  justify-content: center;
}

.indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  font-weight: 600;
  color: var(--mc-text-muted);
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--mc-cream-border);
}

.dot.peak-dot {
  background: var(--cf-primary);
  box-shadow: 0 2px 6px rgba(255, 107, 107, 0.3);
}

.alert-banner {
  background: var(--mc-warning-bg);
  color: var(--mc-warning-text);
  font-size: 12px;
  font-weight: 600;
  padding: 12px 14px;
  border-radius: var(--cf-radius-sm);
  transition: transform 0.15s ease;
}

.alert-banner:hover {
  transform: translateY(-1px);
}

.filter-tabs {
  display: flex;
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: var(--cf-radius-md);
  padding: 4px;
  margin-bottom: 14px;
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  touch-action: pan-x;
  scrollbar-width: none;
}

.filter-tabs::-webkit-scrollbar {
  display: none;
}

.filter-tabs button {
  flex: 1 0 auto;
  min-width: 58px;
  background: transparent;
  border: none;
  padding: 8px 10px;
  font-size: 12px;
  font-weight: 700;
  color: var(--mc-text-muted);
  border-radius: 8px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.filter-tabs button.active {
  background: var(--mc-navy);
  color: #fff;
  box-shadow: 0 2px 6px rgba(27, 59, 95, 0.25);
}

/* Modals */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 16px;
}

.modal-card {
  background: #fff;
  border-radius: 18px;
  padding: 20px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
}

.modal-title {
  font-size: 17px;
  font-weight: 800;
  color: var(--mc-navy);
  margin-bottom: 6px;
}

.modal-desc {
  font-size: 12px;
  color: var(--mc-text-muted);
  line-height: 1.4;
  margin-bottom: 14px;
}

.pin-search-row {
  display: flex;
  gap: 8px;
  margin-bottom: 14px;
}

.pin-input {
  flex: 1;
  border: 2px solid var(--mc-border);
  border-radius: 10px;
  padding: 10px 14px;
  font-size: 18px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  text-align: center;
  color: var(--mc-navy);
  outline: none;
}

.pin-input:focus {
  border-color: var(--mc-navy);
}

.pin-lookup-btn {
  background: var(--mc-navy);
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 0 18px;
  font-size: 13px;
  font-weight: 800;
  cursor: pointer;
}

.pin-result-box {
  background: #f8fafc;
  border: 1px solid var(--mc-border);
  border-radius: 12px;
  padding: 14px;
  margin-bottom: 14px;
}

.pin-result-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.pin-customer {
  font-size: 14px;
  font-weight: 800;
  color: var(--mc-navy);
}

.pin-date {
  font-size: 11px;
  color: var(--mc-text-muted);
}

.pin-status {
  font-size: 10px;
  font-weight: 800;
  padding: 4px 8px;
  border-radius: 999px;
  background: #fff3cd;
  color: #8a5300;
}

.pin-status.retirado {
  background: #e6f6ec;
  color: #1f8a4c;
}

.pin-status.expirado {
  background: var(--mc-danger-soft);
  color: var(--mc-danger);
}

.pin-items {
  border-top: 1px dashed var(--mc-border);
  border-bottom: 1px dashed var(--mc-border);
  padding: 8px 0;
  margin-bottom: 8px;
}

.pin-item-line {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  padding: 3px 0;
}

.pin-total-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  font-weight: 800;
  color: var(--mc-navy);
  margin-bottom: 12px;
}

.pin-confirm-btn {
  width: 100%;
  background: #1f8a4c;
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 12px;
  font-size: 13px;
  font-weight: 800;
  cursor: pointer;
}

.report-badge {
  display: inline-block;
  font-size: 10px;
  font-weight: 800;
  background: #e8f0fe;
  color: var(--mc-navy);
  padding: 4px 10px;
  border-radius: 999px;
  margin-bottom: 8px;
}

.report-table {
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: #f8fafc;
  border: 1px solid var(--mc-border);
  border-radius: 12px;
  padding: 12px 14px;
  margin-bottom: 16px;
}

.report-row {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  padding: 4px 0;
  border-bottom: 1px solid #eef2f6;
}

.report-row:last-child {
  border-bottom: none;
}

.report-row strong.green {
  color: #1f8a4c;
}

.modal-footer-btns {
  display: flex;
  gap: 10px;
}

.btn-close-modal {
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

.btn-print {
  flex: 1;
  background: var(--mc-navy);
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 11px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.extra-stats-three {
  grid-template-columns: repeat(3, 1fr);
}

.rating-gold {
  color: #d97706 !important;
}

.merchant-reviews-card {
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: var(--mc-radius-md);
  padding: 16px;
}

.m-reviews-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.m-reviews-title {
  font-size: 15px;
  font-weight: 800;
  color: var(--mc-text);
  margin: 0;
}

.m-reviews-sub {
  font-size: 11px;
  color: var(--mc-text-muted);
}

.m-reviews-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.m-review-item {
  background: #fdf9f2;
  border: 1px solid var(--mc-cream-border);
  border-radius: 10px;
  padding: 12px;
}

.m-rev-top {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}

.m-rev-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--mc-coral);
  color: #fff;
  font-size: 11px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.m-rev-info {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.m-rev-info strong {
  font-size: 12.5px;
  color: var(--mc-text);
}

.m-rev-info span {
  font-size: 10.5px;
  color: var(--mc-text-muted);
}

.m-rev-stars {
  font-size: 11px;
  flex-shrink: 0;
}

.m-rev-comment {
  margin: 0 0 8px 0;
  font-size: 12px;
  color: var(--mc-text);
  line-height: 1.4;
}

.m-rev-reply-box {
  background: #fff;
  border-left: 3px solid var(--mc-amber);
  border-radius: 6px;
  padding: 8px 10px;
}

.m-rev-reply-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2px;
}

.m-rev-reply-head strong {
  font-size: 11px;
  color: #8c5b16;
}

.m-rev-link-btn {
  background: none;
  border: none;
  color: var(--mc-coral);
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
}

.m-rev-reply-box p {
  margin: 0;
  font-size: 11.5px;
  color: var(--mc-text-muted);
}

.m-rev-reply-trigger {
  background: #fff;
  border: 1px solid var(--mc-cream-border);
  border-radius: 8px;
  padding: 5px 10px;
  font-size: 11px;
  font-weight: 700;
  color: var(--mc-navy);
  cursor: pointer;
}

.m-rev-editor textarea {
  width: 100%;
  border: 1px solid var(--mc-border);
  border-radius: 8px;
  padding: 8px;
  font-size: 12px;
  font-family: inherit;
  resize: none;
  margin-bottom: 6px;
}

.m-rev-editor-btns {
  display: flex;
  justify-content: flex-end;
  gap: 6px;
}

.m-rev-cancel {
  background: #f0ece1;
  border: none;
  border-radius: 6px;
  padding: 5px 10px;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
}

.m-rev-save {
  background: var(--mc-green);
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 5px 12px;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--mc-surface) 25%,
    var(--mc-cream-border) 50%,
    var(--mc-surface) 75%
  );
  background-size: 200% 100%;
  animation: pulse 1.5s infinite;
  border: 1px solid transparent;
  min-height: 60px;
}

@keyframes pulse {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

@media (max-width: 420px) {
  .quick-actions-bar {
    flex-wrap: wrap;
  }

  .quick-btn {
    flex: 1 1 140px;
  }

  .stats-row {
    flex-wrap: wrap;
  }

  .stat-card {
    flex: 1 1 100px;
    min-width: 0;
  }

  .esg-header {
    flex-wrap: wrap;
    gap: 6px;
  }

  .chart-header {
    flex-wrap: wrap;
    gap: 10px;
  }

  .chart-area {
    overflow-x: auto;
  }

  .chart-bars {
    min-width: 280px;
  }

  .pin-search-row {
    flex-wrap: wrap;
  }

  .pin-lookup-btn {
    padding: 12px 18px;
  }

  .modal-footer-btns.two-cols {
    flex-wrap: wrap;
  }
}

@media print {
  .screen > :not(.modal-overlay),
  .modal-footer-btns {
    display: none !important;
  }

  .modal-overlay {
    position: static !important;
    background: #ffffff !important;
    backdrop-filter: none !important;
    padding: 0 !important;
  }

  .modal-card {
    box-shadow: none !important;
    max-width: 100% !important;
    border: 1px solid #e2e8f0 !important;
  }
}
</style>

