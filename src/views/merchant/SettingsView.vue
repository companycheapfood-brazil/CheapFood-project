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
    <MerchantHeader title="Configurações" :subtitle="merchantStats.storeName" />

    <main class="content">
      <div class="menu-card">
        <button v-for="item in menuItems" :key="item.label" class="menu-row">
          <span>{{ item.icon }} {{ item.label }}</span>
          <span class="chevron">›</span>
        </button>
      </div>

      <div class="menu-card">
        <button class="menu-row danger">Sair da conta</button>
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
</style>
