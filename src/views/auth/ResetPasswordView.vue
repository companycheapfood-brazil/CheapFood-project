<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthService from '@/services/auth.service'

const router = useRouter()
const password = ref('')
const confirmPassword = ref('')
const message = ref('')

const handleReset = async () => {
  if (password.value !== confirmPassword.value) {
    message.value = 'As senhas não coincidem.'
    return
  }

  try {
    // We would normally get a token from the URL, but for the mock:
    await AuthService.resetPassword({ email: 'test@example.com', password: password.value })
    message.value = 'Senha redefinida com sucesso!'
    setTimeout(() => {
      router.push('/login')
    }, 2000)
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

      <h2 class="reset-title">Nova senha</h2>
      <p class="reset-subtitle">Crie sua nova senha abaixo.</p>

      <form @submit.prevent="handleReset" class="auth-form mt-4">
        <div class="form-group">
          <label>Nova senha</label>
          <input type="password" v-model="password" placeholder="••••••••" required />
        </div>

        <div class="form-group">
          <label>Confirmar nova senha</label>
          <input type="password" v-model="confirmPassword" placeholder="••••••••" required />
        </div>

        <div class="password-rules">
          <div class="rule valid">
            <span class="icon">✓</span> Mínimo 8 caracteres
          </div>
          <div class="rule valid">
            <span class="icon">✓</span> Uma letra maiúscula
          </div>
          <div class="rule">
            <span class="icon">○</span> Um número ou símbolo
          </div>
        </div>

        <button type="submit" class="btn btn-primary mt-4">Redefinir senha</button>
      </form>

      <p v-if="message" class="info-msg" :class="{ 'error-msg': message.includes('não') || message.includes('erro') }">{{ message }}</p>

      <div class="bottom-link">
        Lembrou a senha? <a href="#" @click.prevent="router.push('/login')">Entrar agora</a>
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
}

.password-rules {
  margin-top: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.rule {
  font-size: 0.85rem;
  color: #8c5b16;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.rule.valid {
  color: white;
}

.rule .icon {
  font-size: 1rem;
}

.bottom-link {
  margin-top: 2rem;
  text-align: center;
  color: #8c5b16;
  font-size: 0.9rem;
}

.bottom-link a {
  color: #ff3b69;
  font-weight: bold;
  text-decoration: none;
}

.info-msg {
  margin-top: 1rem;
  font-weight: bold;
  color: #2ecc71;
  text-align: center;
}
.error-msg {
  color: #ff0000;
}

.logo-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 0.5rem;
}

</style>
