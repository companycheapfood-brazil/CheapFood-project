<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import BottomNav from '@/components/BottomNav.vue'

const router = useRouter()
const route = useRoute()

const code = ref('')
const subtotal = ref(0)
const savings = ref(0)
const items = ref<any[]>([])

onMounted(() => {
  code.value = (route.query.code as string) || 'A7K3'
  subtotal.value = parseFloat((route.query.subtotal as string) || '17.98')
  savings.value = parseFloat((route.query.savings as string) || '21.52')
  
  if (route.query.items) {
    items.value = JSON.parse(route.query.items as string)
  } else {
    // fallback mockup items
    items.value = [
      { name: 'Leite Integral 1L', cart_quantity: 3 },
      { name: 'Queijo mussarela 300g', cart_quantity: 1 },
      { name: 'Pão integral 500g', cart_quantity: 1 }
    ]
  }
})
</script>

<template>
  <div class="screen">
    <header class="receipt-header">
      <h1 class="header-title">Comprovante</h1>
      <span class="header-badge">{{ items.reduce((acc, i) => acc + i.cart_quantity, 0) }} itens</span>
    </header>

    <main class="content">
      <div class="success-icon-container">
        <div class="success-circle">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#2ecc71" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        </div>
      </div>
      
      <h2 class="title">Reserva confirmada!</h2>
      <p class="subtitle">Você tem até 19:00 para retirar</p>

      <div class="summary-card">
        <div class="item-list">
          <div class="item-row" v-for="item in items" :key="item.name">
            <span class="item-label">Item</span>
            <span class="item-value">{{ item.name }} ({{ item.cart_quantity }}uni)</span>
          </div>
        </div>
        
        <div class="summary-row mt">
          <span class="label">Subtotal</span>
          <span class="value">R${{ subtotal.toFixed(2).replace('.', ',') }}</span>
        </div>
        <div class="summary-row">
          <span class="label">Economia total</span>
          <span class="value pink">- R${{ savings.toFixed(2).replace('.', ',') }}</span>
        </div>
        
        <hr class="divider" />
        
        <div class="summary-row total-row">
          <span class="label">Total</span>
          <span class="value">R${{ subtotal.toFixed(2).replace('.', ',') }}</span>
        </div>
        
        <div class="savings-badge">
          🎉 Economizou R${{ savings.toFixed(2).replace('.', ',') }}!
        </div>
      </div>

      <div class="code-card">
        <span class="code-label">CÓDIGO DA RESERVA</span>
        <h1 class="code-value">{{ code }}</h1>
      </div>

      <button class="back-btn" @click="router.push('/')">Voltar ao início</button>
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

.receipt-header {
  background-color: #f6b55d;
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  font-size: 1.4rem;
  font-weight: 800;
  color: #333;
  margin: 0;
}

.header-badge {
  background-color: #ff3b69;
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 800;
}

.content {
  padding: 1.5rem;
  flex: 1;
  overflow-y: auto;
  padding-bottom: 100px;
}

.success-icon-container {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
  margin-bottom: 1.5rem;
}

.success-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: #eafbe4;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(46, 204, 113, 0.2);
}

.title {
  text-align: center;
  font-size: 1.4rem;
  font-weight: 800;
  color: #333;
  margin: 0 0 0.5rem 0;
}

.subtitle {
  text-align: center;
  font-size: 0.9rem;
  color: #a0845a;
  margin: 0 0 2rem 0;
}

.summary-card {
  background-color: #fdf6e9;
  border: 1px solid #f0dfb8;
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 15px rgba(240, 223, 184, 0.4);
}

.item-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.item-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
}

.item-label {
  color: #a0845a;
}

.item-value {
  font-weight: 700;
  color: #333;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.summary-row.mt {
  margin-top: 1.5rem;
}

.summary-row .label {
  color: #a0845a;
}

.summary-row .value {
  font-weight: 700;
  color: #333;
}

.summary-row .value.pink {
  color: #ff3b69;
}

.divider {
  border: none;
  border-top: 1px dashed #dcb985;
  margin: 1rem 0;
}

.total-row {
  font-size: 1.1rem;
}

.total-row .label {
  font-weight: 800;
  color: #333;
}

.savings-badge {
  background-color: #ff3b69;
  color: white;
  text-align: center;
  padding: 0.6rem;
  border-radius: 20px;
  font-weight: 800;
  font-size: 0.85rem;
  margin-top: 1.5rem;
  box-shadow: 0 4px 12px rgba(255, 59, 105, 0.3);
}

.code-card {
  border: 2px dashed #ff3b69;
  border-radius: 16px;
  padding: 1.5rem;
  text-align: center;
  margin-bottom: 2rem;
  background-color: #fff0f3;
}

.code-label {
  color: #ff3b69;
  font-size: 0.85rem;
  font-weight: 800;
  letter-spacing: 1px;
}

.code-value {
  color: #ff3b69;
  font-size: 2.5rem;
  font-weight: 800;
  letter-spacing: 5px;
  margin: 0.5rem 0 0 0;
}

.back-btn {
  width: 100%;
  background-color: transparent;
  color: #ff3b69;
  padding: 1.2rem;
  border: 2px solid #ff3b69;
  border-radius: 20px;
  font-size: 1.1rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.back-btn:hover {
  background-color: rgba(255, 59, 105, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.08);
}

.back-btn:active {
  transform: translateY(0) scale(0.98);
}
</style>
