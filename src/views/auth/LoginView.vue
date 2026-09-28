<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AuthService from '@/services/auth.service'

const router = useRouter()
const route = useRoute()

const isMerchant = computed(() => route.query.role === 'merchant')

const email = ref('')
const password = ref('')
const errorMessage = ref('')

const handleLogin = async () => {
  try {
    const res = await AuthService.login({ email: email.value, password: password.value })
    if (res.user.role === 'merchant') {
      router.push('/comerciante')
    } else {
      router.push('/')
    }
  } catch (error: any) {
    errorMessage.value = error.response?.data?.message || 'Erro ao fazer login'
  }
}
</script>

<template>
  <div class="auth-layout" :class="{ 'merchant-theme': isMerchant }">
    <div class="logo-container-small">
      <div class="logo-row">
      <svg class="cart-icon-small" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M7 18C5.9 18 5.01 18.9 5.01 20C5.01 21.1 5.9 22 7 22C8.1 22 9 21.1 9 20C9 18.9 8.1 18 7 18ZM1 2V4H3L6.6 11.59L5.24 14.04C5.09 14.32 5 14.65 5 15C5 16.1 5.9 17 7 17H19V15H7.42C7.28 15 7.17 14.89 7.17 14.75L7.2 14.63L8.1 13H15.55C16.3 13 16.96 12.59 17.3 11.97L20.88 5.48C20.95 5.34 21 5.17 21 5C21 4.45 20.55 4 20 4H5.21L4.27 2H1ZM17 18C15.9 18 15.01 18.9 15.01 20C15.01 21.1 15.9 22 17 22C18.1 22 19 21.1 19 20C19 18.9 18.1 18 17 18Z" />
      </svg>
      <h1 class="logo-text-small">Cheap<span class="logo-text-highlight">Food</span></h1>
      </div>
      <p class="subtitle-small">Economize. Reduza o desperdício.</p>
    </div>

    <div class="auth-box">
      <div class="toggle-container">
        <button class="toggle-btn active">Entrar</button>
        <button class="toggle-btn" @click="router.push('/register' + (isMerchant ? '?role=merchant' : ''))">Cadastrar</button>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label>E-mail</label>
          <input type="email" v-model="email" placeholder="seu@email.com" required />
        </div>

        <div class="form-group">
          <label>Senha</label>
          <input type="password" v-model="password" placeholder="••••••••" required />
        </div>

        <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>

        <a href="#" @click.prevent="router.push('/forgot-password')" class="forgot-link">Esqueceu a senha?</a>

        <button type="submit" class="btn btn-primary mt-4">Entrar</button>
      </form>
    </div>
  </div>
</template>

<style>
/* Additional specific styles for forms, building on StartView styles */
.logo-container-small {
  text-align: center;
  margin-bottom: 2rem;
}

.cart-icon-small {
  width: 40px;
  height: 40px;
}

.logo-text-small {
  font-size: 2rem;
  font-weight: 800;
  color: white;
  margin: 0;
}

.subtitle-small {
  color: #c9791a;
  font-size: 0.85rem;
  margin-top: 0.2rem;
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
  margin-bottom: 2rem;
  padding: 4px;
}

.toggle-btn {
  flex: 1;
  padding: 0.8rem;
  border: none;
  background: transparent;
  border-radius: 20px;
  font-weight: 600;
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
  gap: 1.2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  color: #c9791a;
  font-weight: 600;
  font-size: 0.9rem;
}

.form-group input {
  padding: 1rem;
  border-radius: 12px;
  border: 2px solid transparent;
  background-color: #fdf6e9;
  color: #333;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #ff3b69;
  background-color: #fff;
  box-shadow: 0 0 0 4px rgba(255, 59, 105, 0.15);
}

.form-group input::placeholder {
  color: #bfa47a;
}

.forgot-link {
  color: #ff3b69;
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
}

.error-msg {
  color: #ff0000;
  font-size: 0.9rem;
  font-weight: bold;
}

.mt-4 {
  margin-top: 1.5rem;
}

/* MERCHANT THEME OVERRIDES */
.merchant-theme {
  background-color: #c4b8e8 !important; /* Lilac */
}

.merchant-theme .cart-icon-small path {
  fill: #1e1b6e !important; /* Navy */
}

.merchant-theme .logo-text-small {
  color: #1e1b6e !important;
}

.merchant-theme .logo-text-highlight {
  color: #c9791a !important; /* Orange/Brown */
}

.merchant-theme .subtitle-small {
  color: #4a4268 !important;
}

.merchant-theme .toggle-container {
  background-color: rgba(255, 255, 255, 0.5) !important;
}

.merchant-theme .toggle-btn {
  color: #4a4268 !important;
}

.merchant-theme .toggle-btn.active {
  background-color: #3b30b8 !important;
  color: white !important;
}

.merchant-theme .form-group label {
  color: #4a4268 !important;
}

.merchant-theme .form-group input {
  background-color: rgba(255, 255, 255, 0.7) !important;
}

.merchant-theme .form-group input:focus {
  border-color: #3b30b8 !important;
  box-shadow: 0 0 0 4px rgba(59, 48, 184, 0.15) !important;
}

.merchant-theme .forgot-link {
  color: #3b30b8 !important;
}

.merchant-theme .btn-primary {
  background-color: #3b30b8 !important;
  box-shadow: 0 4px 10px rgba(59, 48, 184, 0.3) !important;
}

.merchant-theme .btn-primary:hover {
  background-color: #2e2494 !important;
}

.logo-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 0.5rem;
}

</style>
