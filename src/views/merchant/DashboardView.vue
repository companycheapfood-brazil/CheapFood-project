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
      subtitle="�ltimos 7 dias"
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

      <section class="chart-card">
        <p class="chart-title">Vendas por dia</p>
        <div class="chart-bars">
          <div v-for="(d, i) in stats.dailySales" :key="d.label" class="bar-col">
            <div
              class="bar"
              :class="{ peak: i === peakDayIndex }"
              :style="{ height: `${(d.value / maxSales) * 100}%` }"
            ></div>
            <span class="bar-label">{{ d.label }}</span>
          </div>
        </div>
      </section>

      <div class="alert-banner">
        <svg style="margin-right: 4px; vertical-align: middle;" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        {{ stats.expiringSoon }} produtos vencem em 2 dias — adicione promoções!
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

.chart-title {
  font-size: 13px;
  font-weight: 700;
  margin-bottom: 16px;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  height: 90px;
  gap: 8px;
}

.bar-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  height: 100%;
}

.bar {
  width: 100%;
  max-width: 22px;
  background: var(--mc-cream-border);
  border-radius: 6px 6px 2px 2px;
  min-height: 6px;
}

.bar.peak {
  background: var(--mc-navy);
}

.bar-label {
  font-size: 10px;
  color: var(--mc-text-muted);
  margin-top: 6px;
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


