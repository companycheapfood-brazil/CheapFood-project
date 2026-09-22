<script setup lang="ts">
import { ref } from 'vue'
import BottomNav from '@/components/BottomNav.vue'

const name = ref('João Silva')
const email = ref('joao@email.com')
const phone = ref('(14) 99999-0000')
const cpf = ref('•••.•••.•••-••')
</script>

<template>
  <div class="screen">
    <header class="edit-header">
      <h1 class="title">Editar perfil</h1>
    </header>

    <main class="content">
      <div class="avatar-section">
        <div class="avatar-circle">
          <span class="avatar-emoji">🙋‍♂️</span>
          <div class="edit-badge"></div>
        </div>
        <button class="change-photo-btn">Alterar foto</button>
      </div>

      <form class="edit-form" @submit.prevent>
        <div class="form-group">
          <label>Nome completo</label>
          <input type="text" v-model="name" />
        </div>
        <div class="form-group">
          <label>E-mail</label>
          <input type="email" v-model="email" />
        </div>
        <div class="form-group">
          <label>Telefone</label>
          <input type="text" v-model="phone" />
        </div>
        <div class="form-group">
          <label>CPF</label>
          <input type="text" v-model="cpf" disabled />
        </div>

        <button class="save-btn">Salvar alterações</button>
      </form>
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

.edit-header {
  background-color: #f6b55d;
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
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

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
}

.avatar-circle {
  width: 70px;
  height: 70px;
  background-color: #fdf6e9;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  font-size: 2rem;
}

.edit-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 20px;
  height: 20px;
  background-color: #f6b55d;
  border-radius: 50%;
  border: 2px solid white;
}

.change-photo-btn {
  background: none;
  border: none;
  color: #f6b55d;
  font-weight: 700;
  font-size: 0.85rem;
  margin-top: 0.5rem;
  cursor: pointer;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
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
  font-weight: 500;
}

.form-group input:disabled {
  color: #aaa;
  background-color: #f9f9f9;
  border-color: #eee;
}

.save-btn {
  width: 100%;
  background-color: #f7b75e;
  color: #5c3809;
  padding: 1.2rem;
  border: none;
  border-radius: 20px;
  font-size: 1.1rem;
  font-weight: 800;
  margin-top: 1rem;
  cursor: pointer;
}
</style>