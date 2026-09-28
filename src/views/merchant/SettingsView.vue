<script setup lang="ts">
import MerchantHeader from '@/components/merchant/MerchantHeader.vue'
import MerchantBottomNav from '@/components/merchant/MerchantBottomNav.vue'
import { merchantStats } from '@/data/merchant'

const menuItems = [
  { label: 'Dados da loja', icon: '🏪' },
  { label: 'Horário de funcionamento', icon: '🕒' },
  { label: 'Formas de pagamento', icon: '💳' },
  { label: 'Notificações', icon: '🔔' },
  { label: 'Central de ajuda', icon: '❓' },
]
</script>

<template>
  <div class="screen">
    <MerchantHeader title="Configurações" subtitle="Padaria Central" />

    <main class="content">
      <div class="menu-card">
        <button v-for="item in menuItems" :key="item.label" class="menu-row" style="cursor: pointer;">
          <span class="menu-item-content">
            <span class="menu-icon" v-html="item.icon"></span>
            {{ item.label }}
          </span>
          <svg class="chevron-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
        </button>
      </div>

      <div class="menu-card">
        <button class="menu-row danger" @click="logout" style="cursor: pointer;"><span class="menu-item-content"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/></svg>Sair da conta</span></button>
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
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.menu-card {
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: var(--cf-radius-md);
  overflow: hidden;
}

.menu-row {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: transparent;
  border: none;
  color: var(--mc-text);
  font-size: 13px;
  font-weight: 500;
  padding: 15px 16px;
  border-bottom: 1px solid var(--mc-border);
  text-align: left;
}

.menu-row:last-child {
  border-bottom: none;
}

.chevron {
  color: var(--mc-text-muted);
}

.menu-row.danger {
  color: var(--mc-danger);
  font-weight: 600;
}

.menu-item-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.menu-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: var(--mc-purple-soft, #f0eeff);
  color: var(--mc-purple, #7c6fea);
  flex-shrink: 0;
}

.chevron-icon {
  color: var(--mc-text-muted);
  flex-shrink: 0;
}

.menu-row:hover {
  background-color: var(--cf-bg, #fafafa);
}

.menu-row.danger .menu-item-content {
  gap: 12px;
}

.menu-row.danger svg {
  color: var(--mc-danger);
}

</style>
