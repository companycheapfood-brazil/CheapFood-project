<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import BottomNav from '@/components/BottomNav.vue'
import AuthService from '@/services/auth.service'

const router = useRouter()
const password = ref('')

const deleteAccount = async () => {
  // Mock delete account
  await AuthService.logout()
  router.push('/start')
}
</script>

<template>
  <div class="screen">
    <header class="delete-header">
      <h1 class="title">Excluir conta</h1>
    </header>

    <main class="content">
      <div class="warning-section">
        <div class="warning-icon"></div>
        <h2 class="warning-title">Tem certeza?</h2>
        <p class="warning-desc">Esta ação é permanente e não pode ser desfeita. Você perderá todo o histórico de pedidos e reservas.</p>
      </div>

      <div class="info-card">
        <h3 class="info-title">O que será excluído:</h3>
        <ul class="info-list">
          <li><span class="cross">✕</span> Perfil e dados pessoais</li>
          <li><span class="cross">✕</span> Histórico de pedidos</li>
          <li><span class="cross">✕</span> Favoritos e avaliações</li>
        </ul>
      </div>

      <div class="form-group">
        <label>Digite sua senha para confirmar</label>
        <input type="password" v-model="password" placeholder="••••••••" />
      </div>

      <div class="actions">
        <button class="btn-delete" @click="deleteAccount">Excluir minha conta</button>
        <button class="btn-cancel" @click="router.back()">Cancelar</button>
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

.delete-header {
  background-color: #f6b55d;
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  text-align: center;
}

.title {
  font-size: 1.2rem;
  font-weight: 800;
  color: #333;
  margin: 0;
}

.content {
  padding: 1.5rem;
  flex: 1;
  overflow-y: auto;
  padding-bottom: 100px;
}

.warning-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-top: 1rem;
  margin-bottom: 2rem;
}

.warning-icon {
  width: 70px;
  height: 70px;
  background-color: #f9f9f9;
  border-radius: 50%;
  margin-bottom: 1rem;
}

.warning-title {
  font-size: 1.2rem;
  font-weight: 800;
  color: #333;
  margin: 0 0 0.5rem 0;
}

.warning-desc {
  font-size: 0.85rem;
  color: #a0a0a0;
  line-height: 1.5;
  margin: 0;
}

.info-card {
  border: 1px solid #f0dfb8;
  border-radius: 12px;
  padding: 1.2rem;
  margin-bottom: 2rem;
}

.info-title {
  font-size: 0.85rem;
  font-weight: 800;
  color: #ff3b69;
  margin: 0 0 1rem 0;
}

.info-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.info-list li {
  font-size: 0.85rem;
  color: #555;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cross {
  color: #ff3b69;
  font-weight: bold;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.form-group label {
  font-size: 0.8rem;
  font-weight: 700;
  color: #888;
}

.form-group input {
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid #f0dfb8;
  background-color: #fdf6e9;
  font-size: 0.95rem;
  color: #333;
  letter-spacing: 2px;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn-delete {
  width: 100%;
  background-color: #e6103e;
  color: white;
  padding: 1.2rem;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 800;
  cursor: pointer;
}

.btn-cancel {
  width: 100%;
  background-color: transparent;
  color: #f6b55d;
  padding: 1.2rem;
  border: 1px solid #f6b55d;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 800;
  cursor: pointer;
}
</style>
