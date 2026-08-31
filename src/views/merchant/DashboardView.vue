<script setup lang="ts">
import { computed } from 'vue'
import MerchantHeader from '@/components/merchant/MerchantHeader.vue'
import MerchantBottomNav from '@/components/merchant/MerchantBottomNav.vue'
import { merchantStats, dailySales } from '@/data/merchant'

const maxSales = computed(() => Math.max(...dailySales.map((d) => d.value)))
const peakDayIndex = computed(() => dailySales.findIndex((d) => d.value === maxSales.value))
</script>

<template>
  <div class="screen">
    <MerchantHeader
      :title="`Dashboard — ${merchantStats.storeName}`"
      :subtitle="merchantStats.period"
    />

    <main class="content">
      <div class="stats-row">
        <div class="stat-card">
          <p class="stat-value">{{ merchantStats.activeProducts }}</p>
          <p class="stat-label">Produtos ativos</p>
        </div>
        <div class="stat-card highlight">
          <p class="stat-value">R$ {{ merchantStats.revenueRecovered }}</p>
          <p class="stat-label">Receita recuperada</p>
        </div>
        <div class="stat-card">
          <p class="stat-value">{{ merchantStats.reservations }}</p>
          <p class="stat-label">Reservas</p>
        </div>
      </div>

      <section class="chart-card">
        <p class="chart-title">Vendas por dia</p>
        <div class="chart-bars">
          <div v-for="(d, i) in dailySales" :key="d.label" class="bar-col">
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
        ⚠️ {{ merchantStats.expiringSoonCount }} produtos vencem em 2 dias — adicione promoções!
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
</style>
