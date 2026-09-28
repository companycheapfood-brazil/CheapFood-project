<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import MerchantHeader from '@/components/merchant/MerchantHeader.vue'
import MerchantBottomNav from '@/components/merchant/MerchantBottomNav.vue'
import { useMerchantStore } from '@/stores/useMerchantStore'
import { storeToRefs } from 'pinia'

const merchantStore = useMerchantStore()
const { activeProducts, expiredProducts, soldProducts } = storeToRefs(merchantStore)
const { togglePause } = merchantStore

onMounted(() => {
  merchantStore.fetchProducts()
})

const tabs = [
  { key: 'ativos', label: 'Ativos' },
  { key: 'vencidos', label: 'Vencidos' },
  { key: 'vendidos', label: 'Vendidos' },
] as const

const activeTab = ref<(typeof tabs)[number]['key']>('ativos')

const visibleProducts = computed(() => {
  if (activeTab.value === 'ativos') return activeProducts.value
  if (activeTab.value === 'vencidos') return expiredProducts.value
  return soldProducts.value
})

function money(v: number) {
  return `R$ ${v.toFixed(2).replace('.', ',')}`
}
</script>

<template>
  <div class="screen">
    <MerchantHeader title="Meus produtos" />

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
        </button>
      </div>

      <div class="product-list">
        <div v-for="p in visibleProducts" :key="p.id" class="product-card">
          <div class="thumb"><img v-if="p.image && p.image.startsWith('http')" :src="p.image" class="real-image" /><span v-else v-html="p.image || p.icon" class="emoji-img"></span></div>

          <div class="info">
            <div class="info-top">
              <p class="name">{{ p.name }}</p>
              <button class="edit-btn">Editar</button>
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
              <span class="discount-badge">
                -{{ Math.round(((p.originalPrice - p.promoPrice) / p.originalPrice) * 100) }}%
              </span>
            </div>

            <div class="progress-track">
              <div
                class="progress-fill"
                :style="{
                  width: `${Math.min(100, (p.reservedCount / p.quantityAvailable) * 100)}%`,
                }"
              ></div>
            </div>
            <p class="progress-label">
              {{ p.reservedCount }} de {{ p.quantityAvailable }} reservadas
            </p>
          </div>

          <button
            v-if="p.status === 'ativo'"
            class="action-btn"
            :class="{ paused: p.paused }"
            @click="togglePause(p.id)"
          >
            {{ p.paused ? 'Ativar' : 'Pausar' }}
          </button>
          <button v-else-if="p.status === 'vencido'" class="action-btn discount">+Desc.</button>
        </div>

        <p v-if="visibleProducts.length === 0" class="empty">Nenhum produto nesta categoria.</p>
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
  font-weight: 600;
  padding: 8px 0;
  border-radius: 999px;
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
  gap: 12px;
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: var(--cf-radius-md);
  padding: 14px;
}

.thumb { overflow: hidden; 
  width: 40px;
  min-width: 40px;
  height: 40px;
  flex-shrink: 0;
  border-radius: var(--cf-radius-sm);
  background: var(--mc-purple-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.info {
  flex: 1;
  min-width: 0;
}

.info-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.name {
  font-size: 13px;
  font-weight: 700;
}

.edit-btn {
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  color: var(--mc-text);
  font-size: 11px;
  font-weight: 600;
  padding: 5px 10px;
  border-radius: var(--cf-radius-sm);
}

.badges-row {
  display: flex;
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

.progress-track {
  height: 5px;
  background: var(--mc-border);
  border-radius: 999px;
  margin-top: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--mc-navy);
  border-radius: 999px;
}

.progress-label {
  font-size: 10px;
  color: var(--mc-text-muted);
  margin-top: 4px;
}

.action-btn {
  align-self: flex-start;
  background: var(--mc-danger);
  color: #fff;
  border: none;
  border-radius: var(--cf-radius-sm);
  padding: 8px 12px;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}

.action-btn.paused {
  background: var(--mc-navy);
}

.action-btn.discount {
  background: var(--cf-orange);
  color: #1a1a1a;
}

.empty {
  text-align: center;
  color: var(--mc-text-muted);
  font-size: 13px;
  padding: 24px 0;
}
.real-image { width: 100%; height: 100%; object-fit: cover; }
.emoji-img { display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; font-size: 1.5rem; }
</style>


