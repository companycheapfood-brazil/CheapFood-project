<script setup lang="ts">
import { ref } from 'vue'
import BottomNav from '@/components/BottomNav.vue'

const search = ref('')
const faqs = [
  'Como funciona a reserva?',
  'Como retirar meu pedido?',
  'Posso cancelar uma reserva?',
  'Como assinar o plano Pro?'
]
</script>

<template>
  <div class="screen">
    <header class="help-header">
      <h1 class="title">Central de ajuda</h1>
    </header>

    <main class="content">
      <div class="search-bar">
        <input type="text" v-model="search" placeholder="Pesquisar ajuda..." />
        <span class="search-icon">🔍</span>
      </div>

      <div class="section">
        <h2 class="section-title">PERGUNTAS FREQUENTES</h2>
        <div class="faq-list">
          <div class="faq-item" v-for="faq in faqs" :key="faq">
            {{ faq }}
          </div>
        </div>
      </div>

      <div class="section">
        <h2 class="section-title">CONTATO</h2>
        <div class="contact-card">
          <p class="contact-title">Chat com suporte</p>
          <p class="contact-subtitle">Resposta em até 2h</p>
        </div>
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

.help-header {
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

.search-bar {
  position: relative;
  width: 100%;
  margin-bottom: 2rem;
}

.search-bar input {
  width: 100%;
  padding: 1rem 1rem 1rem 1rem;
  border-radius: 12px;
  border: 1px solid #f0dfb8;
  background-color: #fdf6e9;
  font-size: 0.95rem;
  color: #333;
}

.search-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #a0845a;
}

.section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 0.75rem;
  font-weight: 800;
  color: #b0b0b0;
  margin-bottom: 1rem;
  letter-spacing: 1px;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.faq-item {
  padding: 1.2rem;
  border-radius: 12px;
  border: 1px solid #f0dfb8;
  background-color: white;
  font-size: 0.9rem;
  font-weight: 700;
  color: #333;
}

.contact-card {
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #f0dfb8;
  background-color: white;
  text-align: center;
}

.contact-title {
  font-size: 0.95rem;
  font-weight: 800;
  color: #333;
  margin: 0 0 0.3rem 0;
}

.contact-subtitle {
  font-size: 0.8rem;
  color: #a0845a;
  margin: 0;
}
</style>
