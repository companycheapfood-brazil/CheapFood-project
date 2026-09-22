<script setup lang="ts">
import { ref } from 'vue'
import BottomNav from '@/components/BottomNav.vue'

const activeTab = ref('Termos de uso')

const terms = [
  { title: '1. Aceitação dos Termos', desc: 'Ao usar o CheapFood, você concorda com estes Termos de Uso. Leia com atenção antes de continuar.' },
  { title: '2. Uso do Serviço', desc: 'O CheapFood é uma plataforma de conexão entre consumidores e comerciantes para produtos próximos ao vencimento.' },
  { title: '3. Responsabilidades', desc: 'Os comerciantes são responsáveis pelas informações de validade e qualidade dos produtos cadastrados.' },
  { title: '4. Cancelamentos', desc: 'Reservas não retiradas dentro do prazo são automaticamente canceladas e o produto volta ao estoque.' },
]
</script>

<template>
  <div class="screen">
    <header class="terms-header">
      <h1 class="title">Termos e privacidade</h1>
    </header>

    <main class="content">
      <div class="toggle-container">
        <button 
          class="toggle-btn" 
          :class="{ active: activeTab === 'Termos de uso' }"
          @click="activeTab = 'Termos de uso'"
        >
          Termos de uso
        </button>
        <button 
          class="toggle-btn" 
          :class="{ active: activeTab === 'Privacidade' }"
          @click="activeTab = 'Privacidade'"
        >
          Privacidade
        </button>
      </div>

      <div class="terms-list" v-if="activeTab === 'Termos de uso'">
        <div class="term-item" v-for="term in terms" :key="term.title">
          <h3 class="term-title">{{ term.title }}</h3>
          <p class="term-desc">{{ term.desc }}</p>
        </div>
      </div>
      <div class="terms-list" v-else>
        <div class="term-item">
          <h3 class="term-title">Política de Privacidade</h3>
          <p class="term-desc">Seus dados estão seguros conosco e não serão compartilhados com terceiros.</p>
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

.terms-header {
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

.toggle-container {
  display: flex;
  background-color: #f5f5f5;
  border-radius: 12px;
  padding: 0.3rem;
  margin-bottom: 2rem;
}

.toggle-btn {
  flex: 1;
  padding: 0.8rem;
  border-radius: 10px;
  border: none;
  background: transparent;
  font-size: 0.85rem;
  font-weight: 700;
  color: #888;
  cursor: pointer;
}

.toggle-btn.active {
  background-color: white;
  color: #333;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.terms-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.term-item {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.term-title {
  font-size: 0.9rem;
  font-weight: 800;
  color: #333;
  margin: 0;
}

.term-desc {
  font-size: 0.85rem;
  color: #a0a0a0;
  line-height: 1.5;
  margin: 0;
}
</style>
