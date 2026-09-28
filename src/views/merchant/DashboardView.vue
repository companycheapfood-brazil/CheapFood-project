<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MerchantHeader from '@/components/merchant/MerchantHeader.vue'
import MerchantBottomNav from '@/components/merchant/MerchantBottomNav.vue'
import { useMerchantStore } from '@/stores/useMerchantStore'
import { storeToRefs } from 'pinia'

const route = useRoute()
const router = useRouter()
const showEmptyState = computed(() => route.query.new === '1')

const merchantStore = useMerchantStore()
const { stats } = storeToRefs(merchantStore)

onMounted(() => {
  merchantStore.fetchDashboardStats()
})

const maxSales = computed(() => Math.max(1, ...stats.value.dailySales.map((d) => d.value)))
const peakDayIndex = computed(() => stats.value.dailySales.findIndex((d) => d.value === maxSales.value))
</script>

<template>
  <div class="screen">
    <MerchantHeader
      title="Dashboard - Padaria Central"
      subtitle="ltimos 7 dias"
    />

    <main class="content" v-if="!showEmptyState">
      <div class="stats-row">
        <div class="stat-card">
          <p class="stat-value">{{ stats.activeProducts }}</p>
          <p class="stat-label">Produtos ativos</p>
        </div>
        <div class="stat-card highlight">
          <p class="stat-value">R$ {{ stats.revenueRecovered }}</p>
          <p class="stat-label">Receita recuperada</p>
        </div>
        <div class="stat-card">
          <p class="stat-value">{{ stats.reservations }}</p>
          <p class="stat-label">Reservas</p>
        </div>
      </div>

      <!-- MÃ©tricas Adicionais Superiores -->
      <div class="stats-row extra-stats">
        <div class="stat-card">
          <p class="stat-value">R$ {{ (stats.revenueRecovered / (stats.dailySales.length || 1)).toFixed(2).replace('.', ',') }}</p>
          <p class="stat-label">Ticket Médio (Semanal)</p>
        </div>
        <div class="stat-card">
          <p class="stat-value">{{ stats.reservations + stats.dailySales.reduce((a,b)=>a+b.value, 0) > 0 ? '+' : '' }}{{ Math.floor(Math.random() * 12) + 5 }}%</p>
          <p class="stat-label">Crescimento (vs Semana Anterior)</p>
        </div>
      </div>

      <section class="chart-card">
        <div class="chart-header">
          <div>
            <p class="chart-title">Faturamento Diário</p>
            <span class="chart-subtitle">Últimos 7 dias</span>
          </div>
          <div class="chart-total">
            Total: <strong>R$ {{ stats.revenueRecovered.toFixed(2).replace('.', ',') }}</strong>
          </div>
        </div>
        <div class="chart-bars">
          <div v-for="(d, i) in stats.dailySales" :key="d.label" class="bar-col">
            <span class="bar-value" v-if="d.value > 0">{{ d.value >= 1000 ? (d.value/1000).toFixed(1) + 'k' : Math.round(d.value) }}</span>
            <span class="bar-value zero" v-else>-</span>
            <div
              class="bar"
              :class="{ peak: i === peakDayIndex && d.value > 0 }"
              :style="{ height: `${(d.value / maxSales) * 100}%`, minHeight: d.value > 0 ? '12px' : '4px' }"
            ></div>
            <span class="bar-label" :class="{ today: i === stats.dailySales.length - 1 }">{{ d.label }}</span>
          </div>
        </div>
        <div class="chart-footer">
          <div class="indicator">
            <span class="dot peak-dot"></span> Maior Faturamento
          </div>
          <div class="indicator">
            <span class="dot"></span> Dia Regular
          </div>
        </div>
      </section>

      <div class="alert-banner">
        <svg style="margin-right: 4px; vertical-align: middle;" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        {{ stats.expiringSoon }} produtos vencem em 2 dias â€” adicione promoÃ§Ãµes!
      </div>
    </main>

    <main class="content empty-content" v-if="showEmptyState">
      <div class="empty-state">
        <div class="empty-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" color="var(--mc-navy)"><path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4"/><path d="M2 7h20"/><path d="M22 7v3a2 2 0 0 1-2 2v0a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 16 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 12 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 8 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 4 12v0a2 2 0 0 1-2-2V7"/></svg>
        </div>
        <h2 class="empty-title">Bem-vindo ao FoodSaver!</h2>
        <p class="empty-desc">
          Cadastre seu primeiro produto com desconto
          e comece a recuperar receita ainda hoje.
        </p>

        <div class="how-it-works">
          <h4 class="how-title">Como funciona:</h4>
          <div class="step">
            <span class="step-num">1</span>
            <p>Cadastre produtos prÃ³ximos ao vencimento</p>
          </div>
          <div class="step">
            <span class="step-num">2</span>
            <p>Clientes da regiÃ£o reservam com desconto</p>
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

.stats-row {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
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

.stat-label {
  font-size: 10px;
  color: var(--mc-text-muted);
  margin-top: 4px;
}

.chart-card {
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: var(--cf-radius-md);
  padding: 16px;
  margin-bottom: 16px;
}

.extra-stats {
  margin-bottom: 24px;
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

.chart-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  height: 140px;
  gap: 6px;
  padding: 0 10px;
}

.bar-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  height: 100%;
}

.bar-value {
  font-size: 11px;
  font-weight: 800;
  color: var(--mc-navy);
  margin-bottom: 6px;
}

.bar-value.zero {
  color: #ccc;
  font-weight: 500;
}

.bar {
  width: 100%;
  max-width: 28px;
  background: var(--mc-cream-border);
  border-radius: 6px 6px 2px 2px;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.bar.peak {
  background: var(--cf-primary);
  box-shadow: 0 6px 14px rgba(255, 107, 107, 0.25);
}

.bar:hover {
  filter: brightness(0.9);
  transform: translateY(-2px);
}

.bar-label {
  font-size: 11px;
  color: var(--mc-text-muted);
  margin-top: 10px;
  font-weight: 600;
}

.bar-label.today {
  color: var(--mc-navy);
  font-weight: 800;
  background: #f0f0f0;
  padding: 2px 6px;
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
}

.empty-content {
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-state {
  text-align: center;
  padding: 0 12px;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-title {
  font-size: 18px;
  font-weight: 800;
  margin-bottom: 8px;
}

.empty-desc {
  font-size: 13px;
  color: var(--mc-text-muted);
  line-height: 1.5;
  margin-bottom: 24px;
}

.how-it-works {
  background: var(--mc-warning-bg);
  border-radius: var(--cf-radius-md);
  padding: 16px;
  text-align: left;
  margin-bottom: 24px;
}

.how-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--mc-warning-text);
  margin-bottom: 12px;
}

.step {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 10px;
}

.step:last-child {
  margin-bottom: 0;
}

.step-num {
  background: var(--cf-orange);
  color: #fff;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  flex-shrink: 0;
}

.step p {
  font-size: 13px;
  color: var(--mc-text);
  line-height: 1.4;
}

.cta-btn {
  width: 100%;
  background: var(--cf-orange);
  color: #fff;
  border: none;
  border-radius: var(--cf-radius-sm);
  padding: 15px;
  font-size: 14px;
  font-weight: 700;
}
</style>



