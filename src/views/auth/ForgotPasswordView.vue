<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthService from '@/services/auth.service'

const router = useRouter()
const email = ref('')
const message = ref('')

const handleForgot = async () => {
  try {
    await AuthService.forgotPassword(email.value)
    message.value = 'Link de redefinição enviado! Verifique seu e-mail.'
  } catch (error) {
    message.value = 'Ocorreu um erro. Tente novamente.'
  }
}
</script>

<template>
  <div class="auth-layout reset-layout">
    <div class="reset-header">
      <button class="back-link" @click="router.back()">Voltar</button>
    </div>

    <div class="reset-content">
      <div class="icon-circle">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="lock-icon">
          <path d="M18 8H17V6C17 3.24 14.76 1 12 1C9.24 1 7 3.24 7 6V8H6C4.9 8 4 8.9 4 10V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V10C20 8.9 19.1 8 18 8ZM9 6C9 4.34 10.34 3 12 3C13.66 3 15 4.34 15 6V8H9V6ZM12 17C10.9 17 10 16.1 10 15C10 13.9 10.9 13 12 13C13.1 13 14 13.9 14 15C14 16.1 13.1 17 12 17Z" fill="white"/>
        </svg>
      </div>

      <h2 class="reset-title">Recuperar senha</h2>
      <p class="reset-subtitle">Informe seu e-mail e enviaremos um link de redefinição.</p>

      <form @submit.prevent="handleForgot" class="auth-form mt-4">
        <div class="form-group">
          <label>E-mail cadastrado</label>
          <input type="email" v-model="email" placeholder="seu@email.com" required />
        </div>

        <button type="submit" class="btn btn-primary">Enviar link de recuperação</button>
      </form>

      <p v-if="message" class="info-msg">{{ message }}</p>

      <div class="info-box">
        <h4>Como funciona?</h4>
        <p>Enviaremos um e-mail com um link seguro. Verifique também sua caixa de spam.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.reset-layout {
  justify-content: flex-start;
  padding-top: 3rem;
}

.reset-header {
  width: 100%;
  max-width: 400px;
  display: flex;
  justify-content: flex-start;
  margin-bottom: 3rem;
}

.back-link {
  background: none;
  border: none;
  color: #ff3b69;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  padding: 0;
}

.reset-content {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
}

.icon-circle {
  width: 80px;
  height: 80px;
  background-color: #ff3b69;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 2rem auto;
}

.lock-icon {
  width: 36px;
  height: 36px;
}

.reset-title {
  color: #5c3809;
  font-size: 1.6rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.reset-subtitle {
  color: #8c5b16;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
  line-height: 1.4;
}

.info-box {
  background-color: #f7d299;
  border-radius: 12px;
  padding: 1rem;
  margin-top: 2rem;
  color: #8c5b16;
}

.info-box h4 {
  color: #5c3809;
  font-size: 0.95rem;
  font-weight: 700;
  margin-bottom: 0.4rem;
}

.info-box p {
  font-size: 0.85rem;
  line-height: 1.4;
}

.info-msg {
  margin-top: 1rem;
  font-weight: bold;
  color: #2ecc71;
  text-align: center;
}

.logo-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 0.5rem;
}

</style>
