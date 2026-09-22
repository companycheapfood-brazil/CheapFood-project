<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import BottomNav from '@/components/BottomNav.vue'
import AuthService from '@/services/auth.service'

const router = useRouter()

const handleLogout = async () => {
  try {
    await AuthService.logout()
  } catch (e) {
    console.error('Logout error:', e)
  }
  router.push('/start')
}

const tabs = ['Economizados', 'Reservas', 'Comida salva']
const activeTab = ref('Economizados')

const menuItems = [
  { label: 'Histórico de pedidos', to: '/perfil/historico' },
  { label: 'Editar dados', to: '/perfil/editar' },
  { label: 'Central de ajuda', to: '/perfil/ajuda' },
  { label: 'Termos e privacidade', to: '/perfil/termos' },
  { label: 'Excluir conta', to: '/perfil/excluir' },
]

const user = {
  name: 'João Silva',
  role: 'Consumidor · Marília, SP',
  initials: 'JS',
}
</script>

<template>
  <div class="screen">
    <header class="profile-header">
      <h1 class="title">Perfil</h1>
      <div class="avatar-block">
        <div class="avatar"></div>
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
      <div class="menu-list">
        <RouterLink
          v-for="item in menuItems"
          :key="item.label"
          :to="item.to"
          class="menu-row"
        >
          {{ item.label }}
        </RouterLink>
        <button class="menu-row danger" @click="handleLogout">Sair</button>
      </div>
    </main>

    <BottomNav />
  </div>
</template>

<style scoped>
.screen {
  background-color: #ffffff;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.profile-header {
  background-color: #f6b55d;
  padding: 2rem 1.5rem 0 1.5rem;
  text-align: center;
}

.title {
  font-size: 1.2rem;
  font-weight: 800;
  color: #333;
  margin: 0 0 1.5rem 0;
}

.avatar-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1.5rem;
}

.avatar {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.3);
  margin-bottom: 0.8rem;
}

.user-name {
  font-size: 1.3rem;
  font-weight: 800;
  color: #000;
  margin: 0 0 0.3rem 0;
}

.user-role {
  font-size: 0.85rem;
  color: #333;
  margin: 0;
}

.tabs {
  display: flex;
  justify-content: space-around;
  border-top: 1px solid rgba(0,0,0,0.05);
  padding-top: 0.5rem;
}

.tab {
  flex: 1;
  background: transparent;
  border: none;
  color: #333;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 1rem 0;
  cursor: pointer;
  border-right: 1px solid rgba(0,0,0,0.05);
}

.tab:last-child {
  border-right: none;
}

.content {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 80px;
}

.menu-list {
  display: flex;
  flex-direction: column;
}

.menu-row {
  width: 100%;
  padding: 1.2rem 1.5rem;
  background: white;
  border: none;
  border-bottom: 1px solid #f0f0f0;
  text-align: left;
  font-size: 1rem;
  font-weight: 700;
  color: #333;
  text-decoration: none;
  cursor: pointer;
}

.menu-row.danger {
  color: #ff3b69;
}
</style>
