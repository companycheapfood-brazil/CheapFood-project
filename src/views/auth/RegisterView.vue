<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthService from '@/services/auth.service'

const router = useRouter()

const name = ref('')
const email = ref('')
const password = ref('')
const errorMessage = ref('')
const successMessage = ref('')

const handleRegister = async () => {
  try {
    // Assuming new user defaults to consumer unless we had a role selector.
    // Since StartView has "Sou comerciante", maybe they pass role via query param?
    const role = router.currentRoute.value.query.role || 'consumer'
    
    const res = await AuthService.register({ 
      name: name.value, 
      email: email.value, 
      password: password.value,
      role: role
    })
    
    // Auto login after register
    await AuthService.login({ email: email.value, password: password.value })
    
    successMessage.value = 'Conta criada com sucesso!'
    setTimeout(() => {
      router.push('/')
    }, 1000)
  } catch (error: any) {
    errorMessage.value = error.response?.data?.message || 'Erro ao criar conta'
  }
}
</script>

<template>
  <div class="auth-layout">
    <div class="logo-container-small">
      <svg class="cart-icon-small" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M7 18C5.9 18 5.01 18.9 5.01 20C5.01 21.1 5.9 22 7 22C8.1 22 9 21.1 9 20C9 18.9 8.1 18 7 18ZM1 2V4H3L6.6 11.59L5.24 14.04C5.09 14.32 5 14.65 5 15C5 16.1 5.9 17 7 17H19V15H7.42C7.28 15 7.17 14.89 7.17 14.75L7.2 14.63L8.1 13H15.55C16.3 13 16.96 12.59 17.3 11.97L20.88 5.48C20.95 5.34 21 5.17 21 5C21 4.45 20.55 4 20 4H5.21L4.27 2H1ZM17 18C15.9 18 15.01 18.9 15.01 20C15.01 21.1 15.9 22 17 22C18.1 22 19 21.1 19 20C19 18.9 18.1 18 17 18Z" fill="#FF3B69"/>
      </svg>
      <h1 class="logo-text-small">Cheap<span class="logo-text-highlight">Food</span></h1>
      <p class="subtitle-small">Economize. Restaure e desperdício.</p>
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

        <button type="submit" class="btn btn-primary mt-4">Criar minha conta</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.success-msg {
  color: #2ecc71;
  font-weight: bold;
  font-size: 0.9rem;
}
</style>
