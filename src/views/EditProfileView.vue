<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import BottomNav from '@/components/BottomNav.vue'

const router = useRouter()

const form = reactive({
  name: 'João Silva',
  email: 'joao@email.com',
  phone: '(14) 99888-0000',
  cpf: '***.***.***-**',
})

function saveProfile() {
  alert('Alterações salvas com sucesso!')
}
</script>

<template>
  <div class="screen">

    <header class="header">
      <button class="back" @click="router.back()">‹</button>
      <h1>Editar perfil</h1>
    </header>

    <main class="content">

      <button class="avatar-button" type="button">
        <div class="avatar">
          👤
        </div>

        <span class="camera">📷</span>

        <span class="change-photo">
          Alterar foto
        </span>
      </button>

      <form class="form" @submit.prevent="saveProfile">

        <label>
          Nome completo
          <input v-model="form.name" type="text" />
        </label>

        <label>
          E-mail
          <input v-model="form.email" type="email" />
        </label>

        <label>
          Telefone
          <input v-model="form.phone" type="tel" />
        </label>

        <label>
          CPF
          <input v-model="form.cpf" type="text" />
        </label>

        <button class="save" type="submit">
          Salvar alterações
        </button>

      </form>

    </main>

    <BottomNav />

  </div>
</template>

<style scoped>

.screen {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--cf-bg);
}

.header {
  position: relative;
  min-height: 54px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--cf-orange);
  border-radius: 0 0 var(--cf-radius-lg) var(--cf-radius-lg);
}

.header h1 {
  font-size: 16px;
  font-weight: 800;
}

.back {
  position: absolute;
  left: 16px;
  border: none;
  background: transparent;
  font-size: 30px;
  cursor: pointer;
}

.content {
  flex: 1;
  padding: 24px 16px;
}

.avatar-button {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;

  margin: 0 auto 22px;

  border: none;
  background: transparent;
  cursor: pointer;
}

.avatar {
  width: 58px;
  height: 58px;

  border-radius: 50%;

  background: #f3f0ed;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 24px;
}

.camera {
  position: absolute;

  right: 2px;
  top: 39px;

  width: 21px;
  height: 21px;

  border-radius: 50%;

  background: var(--cf-orange);

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 11px;
}

.change-photo {
  color: var(--cf-orange-dark);
  font-size: 10px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 11px;
}

label {
  color: var(--cf-text-muted);
  font-size: 9px;
}

input {
  width: 100%;

  margin-top: 4px;

  padding: 10px 12px;

  border: 1px solid #f0dfb8;
  border-radius: 8px;

  background: #fffaf0;

  color: var(--cf-text);

  font-size: 11px;

  outline: none;
}

input:focus {
  border-color: var(--cf-orange);
}

.save {
  margin-top: 3px;

  padding: 12px;

  border: none;
  border-radius: 10px;

  background: var(--cf-orange);

  color: #1a1a1a;

  font-size: 11px;
  font-weight: 800;

  cursor: pointer;
}

</style>