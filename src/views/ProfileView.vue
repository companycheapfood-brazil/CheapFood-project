<script setup lang="ts">
import { ref } from 'vue'
import BottomNav from '@/components/BottomNav.vue'

const tabs = ['Economizados', 'Reservas', 'Comida salva']
const activeTab = ref('Economizados')

const menuItems = [
  { label: 'Histórico de pedidos', icon: '📦' },
  { label: 'Editar dados', icon: '✏️' },
  { label: 'Central de ajuda', icon: '❓' },
  { label: 'Termos e privacidade', icon: '📄' },
]

const user = {
  name: 'João Silva',
  role: 'Consumidor · Marília, SP',
  initials: 'JS',
}
</script>

<template>
  <div class="screen">
    <header class="header">
      <h1 class="title">Perfil</h1>
      <div class="avatar-block">
        <div class="avatar">{{ user.initials }}</div>
        <p class="user-name">{{ user.name }}</p>
        <p class="user-role">{{ user.role }}</p>
      </div>

      <div class="tabs">
        <button
          v-for="t in tabs"
          :key="t"
          class="tab"
          :class="{ active: activeTab === t }"
          @click="activeTab = t"
        >
          {{ t }}
        </button>
      </div>
    </header>

    <main class="content">
      <div class="menu-card">
        <button v-for="item in menuItems" :key="item.label" class="menu-row">
          <span>{{ item.icon }} {{ item.label }}</span>
          <span class="chevron">›</span>
        </button>
      </div>

      <div class="menu-card">
        <button class="menu-row danger">Excluir conta</button>
        <button class="menu-row danger">Sair</button>
      </div>
    </main>

    <BottomNav />
  </div>
</template>

<style scoped>
.screen {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--cf-bg);
}

.header {
  background: var(--cf-orange);
  padding: 18px 16px 0;
  border-radius: 0 0 var(--cf-radius-lg) var(--cf-radius-lg);
  flex-shrink: 0;
}

.title {
  font-size: 17px;
  font-weight: 800;
  color: #1a1a1a;
  text-align: center;
  margin-bottom: 8px;
}

.avatar-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-bottom: 16px;
}

.avatar {
  width: 64px;
  height: 64px;
  border-radius: 999px;
  background: rgba(0, 0, 0, 0.15);
  color: #1a1a1a;
  font-size: 22px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}

.user-name {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a1a;
}

.user-role {
  font-size: 11px;
  color: rgba(26, 26, 26, 0.65);
  margin-top: 2px;
}

.tabs {
  display: flex;
  gap: 4px;
}

.tab {
  flex: 1;
  background: transparent;
  border: none;
  color: rgba(26, 26, 26, 0.65);
  font-size: 12px;
  font-weight: 600;
  padding: 10px 0;
  border-bottom: 2px solid transparent;
}

.tab.active {
  color: #1a1a1a;
  border-bottom-color: var(--cf-pink);
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
  background: var(--cf-card);
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
  color: var(--cf-text);
  font-size: 13px;
  font-weight: 500;
  padding: 15px 16px;
  border-bottom: 1px solid var(--cf-border);
  text-align: left;
}

.menu-row:last-child {
  border-bottom: none;
}

.chevron {
  color: var(--cf-text-faint);
}

.menu-row.danger {
  color: var(--cf-pink);
  font-weight: 600;
}
</style>
