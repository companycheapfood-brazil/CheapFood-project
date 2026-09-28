<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AuthService from '@/services/auth.service'

const router = useRouter()
const route = useRoute()

const isMerchant = computed(() => route.query.role === 'merchant')

const name = ref('')
const email = ref('')
const password = ref('')
const errorMessage = ref('')
const successMessage = ref('')

const handleRegister = async () => {
  try {
    const role = route.query.role || 'consumer'
    
    const res = await AuthService.register({ 
      name: name.value, 
      email: email.value, 
      password: password.value,
      role: role
    })
    
    await AuthService.login({ email: email.value, password: password.value })
    
    successMessage.value = 'Conta criada com sucesso!'
    setTimeout(() => {
      router.push(role === 'merchant' ? '/comerciante' : '/')
    }, 1000)
  } catch (error: any) {
    errorMessage.value = error.response?.data?.message || 'Erro ao criar conta'
  }
}
</script>

<template>
  <div class="register-layout" :class="{ 'merchant-theme': isMerchant }">
    <div class="logo-container">
      <svg class="cart-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M7 18C5.9 18 5.01 18.9 5.01 20C5.01 21.1 5.9 22 7 22C8.1 22 9 21.1 9 20C9 18.9 8.1 18 7 18ZM1 2V4H3L6.6 11.59L5.24 14.04C5.09 14.32 5 14.65 5 15C5 16.1 5.9 17 7 17H19V15H7.42C7.28 15 7.17 14.89 7.17 14.75L7.2 14.63L8.1 13H15.55C16.3 13 16.96 12.59 17.3 11.97L20.88 5.48C20.95 5.34 21 5.17 21 5C21 4.45 20.55 4 20 4H5.21L4.27 2H1ZM17 18C15.9 18 15.01 18.9 15.01 20C15.01 21.1 15.9 22 17 22C18.1 22 19 21.1 19 20C19 18.9 18.1 18 17 18Z" :fill="isMerchant ? '#1e1b6e' : '#FF3B69'"/>
      </svg>
      <h1 class="logo-text">Cheap<span class="logo-highlight">Food</span></h1>
      <p class="subtitle">Economize. Restaure e desperdício.</p>
    </div>

    <div class="auth-box">
      <div class="toggle-container">
        <button class="toggle-btn" @click="router.push('/login')">Entrar</button>
        <button class="toggle-btn active">Cadastrar</button>
      </div>

      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label>Nome completo</label>
          <input type="text" v-model="name" placeholder="Seu nome" required />
        </div>

        <div class="form-group">
          <label>E-mail</label>
          <input type="email" v-model="email" placeholder="seu@email.com" required />
        </div>

        <div class="form-group">
          <label>Senha</label>
          <input type="password" v-model="password" placeholder="Mín. 8 caracteres" required minlength="8" />
        </div>

        <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success-msg">{{ successMessage }}</p>

        <button type="submit" class="btn-register">Criar minha conta</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.register-layout {
  min-height: 100vh;
  background-color: #f6b55d;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  font-family: 'Inter', sans-serif;
  transition: background-color 0.3s;
}

.logo-container {
  text-align: center;
  margin-top: 2rem;
  margin-bottom: 2rem;
}

.cart-icon {
  width: 60px;
  height: 60px;
  margin-bottom: 0.5rem;
}

.logo-text {
  font-size: 2rem;
  font-weight: 800;
  color: white;
  margin: 0;
}

.logo-highlight {
  color: #ff3b69;
}

.subtitle {
  color: #c9791a;
  font-size: 0.85rem;
  margin-top: 0.3rem;
  font-weight: 500;
}

.auth-box {
  width: 100%;
  max-width: 400px;
}

.toggle-container {
  display: flex;
  background-color: #f7d299;
  border-radius: 25px;
  margin-bottom: 1.5rem;
  padding: 4px;
}

.toggle-btn {
  flex: 1;
  padding: 0.8rem;
  border: none;
  background: transparent;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.95rem;
  color: #c9791a;
  cursor: pointer;
  transition: all 0.2s;
}

.toggle-btn.active {
  background-color: #ff3b69;
  color: white;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  color: #c9791a;
  font-weight: 600;
  font-size: 0.85rem;
}

.form-group input {
  padding: 1rem;
  border-radius: 20px;
  border: none;
  background-color: #fdf6e9;
  color: #333;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.form-group input:focus {
  outline: none;
  background-color: #fff;
  box-shadow: 0 0 0 3px rgba(255, 59, 105, 0.2);
}

.form-group input::placeholder {
  color: #bfa47a;
}

.btn-register {
  width: 100%;
  padding: 1rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  background-color: #ff3b69;
  color: white;
  margin-top: 0.5rem;
  box-shadow: 0 4px 12px rgba(255, 59, 105, 0.3);
  transition: all 0.2s ease;
}

.btn-register:hover {
  background-color: #e0335c;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 59, 105, 0.4);
}

.btn-register:active {
  transform: translateY(0) scale(0.98);
}

.error-msg {
  color: #ff0000;
  font-weight: bold;
  font-size: 0.9rem;
}

.success-msg {
  color: #2ecc71;
  font-weight: bold;
  font-size: 0.9rem;
}

/* MERCHANT THEME OVERRIDES */
.merchant-theme {
  background-color: #c4b8e8;
}

.merchant-theme .logo-text {
  color: #1e1b6e;
}

.merchant-theme .logo-highlight {
  color: #c9791a;
}

.merchant-theme .subtitle {
  color: #4a4268;
}

.merchant-theme .toggle-container {
  background-color: rgba(255, 255, 255, 0.5);
}

.merchant-theme .toggle-btn {
  color: #4a4268;
}

.merchant-theme .toggle-btn.active {
  background-color: #3b30b8;
  color: white;
}

.merchant-theme .form-group label {
  color: #4a4268;
}

.merchant-theme .form-group input {
  background-color: rgba(255, 255, 255, 0.7);
}

.merchant-theme .form-group input:focus {
  box-shadow: 0 0 0 3px rgba(59, 48, 184, 0.2);
}

.merchant-theme .form-group input::placeholder {
  color: #9a8ec0;
}

.merchant-theme .btn-register {
  background-color: #3b30b8;
  box-shadow: 0 4px 12px rgba(59, 48, 184, 0.3);
}

.merchant-theme .btn-register:hover {
  background-color: #2e2494;
}
</style>
