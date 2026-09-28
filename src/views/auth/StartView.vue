<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goToConsumer = () => {
  router.push('/login?role=consumer')
}

const goToMerchant = () => {
  router.push('/login?role=merchant')
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<template>
  <div class="auth-layout">
    <div class="logo-container">
      <div class="logo-row">
      <svg class="cart-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M7 18C5.9 18 5.01 18.9 5.01 20C5.01 21.1 5.9 22 7 22C8.1 22 9 21.1 9 20C9 18.9 8.1 18 7 18ZM1 2V4H3L6.6 11.59L5.24 14.04C5.09 14.32 5 14.65 5 15C5 16.1 5.9 17 7 17H19V15H7.42C7.28 15 7.17 14.89 7.17 14.75L7.2 14.63L8.1 13H15.55C16.3 13 16.96 12.59 17.3 11.97L20.88 5.48C20.95 5.34 21 5.17 21 5C21 4.45 20.55 4 20 4H5.21L4.27 2H1ZM17 18C15.9 18 15.01 18.9 15.01 20C15.01 21.1 15.9 22 17 22C18.1 22 19 21.1 19 20C19 18.9 18.1 18 17 18Z" fill="#FF3B69"/>
      </svg>
      <h1 class="logo-text">Cheap<span class="logo-text-highlight">Food</span></h1>
      </div>
      <p class="subtitle">Economize. Reduza o desperdício.</p>
    </div>

    <div class="actions">
      <button class="btn btn-primary" @click="goToConsumer">Entrar como consumidor</button>
      <button class="btn btn-outline" @click="goToMerchant">Sou comerciante</button>
      
      <button class="btn-text" @click="goToRegister">
        <span class="muted">Novo aqui?</span> Cadastre-se grátis
      </button>
    </div>
  </div>
</template>

<style>
/* Shared Auth Styles */
.auth-layout {
  min-height: 100vh;
  background-color: #f6b55d;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  font-family: 'Inter', sans-serif;
}

.logo-container {
  text-align: center;
  margin-bottom: 4rem;
}

.cart-icon {
  width: 50px;
  height: 50px;
}

.logo-text {
  font-size: 2.5rem;
  font-weight: 800;
  color: white;
  margin: 0;
}

.logo-text-highlight {
  color: #ff3b69;
}

.subtitle {
  color: #fff9ea;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.actions {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn {
  width: 100%;
  padding: 1rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.btn-primary {
  background-color: #ff3b69;
  color: white;
  box-shadow: 0 4px 10px rgba(255, 59, 105, 0.3);
}

.btn-primary:hover {
  background-color: #e0335c;
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(255, 59, 105, 0.45);
}

.btn-primary:active {
  transform: translateY(0) scale(0.98);
  box-shadow: 0 2px 5px rgba(255, 59, 105, 0.3);
}

.btn-outline {
  background-color: transparent;
  color: #ff3b69;
  border: 2px solid #ff3b69;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.btn-outline:hover {
  background-color: rgba(255, 59, 105, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.08);
}

.btn-outline:active {
  transform: translateY(0) scale(0.98);
}

.btn-text {
  background: none;
  border: none;
  color: white;
  font-weight: 600;
  margin-top: 1rem;
  cursor: pointer;
}

.btn-text .muted {
  color: #ff3b69;
}

.logo-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 0.5rem;
}

</style>
