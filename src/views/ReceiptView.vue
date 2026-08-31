<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCart } from '@/composables/useCart'
import BottomNav from '@/components/BottomNav.vue'

const router = useRouter()
const { items, totalItems, subtotal, totalSavings, lastReservationCode, clearCart } = useCart()

// Se o usuário cair direto nessa tela sem ter reservado nada, manda pra home.
onMounted(() => {
  if (items.length === 0 && !lastReservationCode.value) {
    router.replace('/')
  }
})

function money(v: number) {
  return `R$ ${v.toFixed(2).replace('.', ',')}`
}

function backToHome() {
  clearCart()
  router.push('/')
}

const withdrawalDeadline = computed(() => {
  const d = new Date()
  d.setHours(19, 0, 0, 0)
  return d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
})
</script>

<template>
  <div class="screen">
    <header class="header">
      <h1 class="title">Comprovante</h1>
      <span class="count-badge">{{ totalItems }} itens</span>
    </header>

    <main class="content">
      <div class="success-block">
        <div class="check-circle">✓</div>
        <p class="success-title">Reserva confirmada!</p>
        <p class="success-subtitle">Você tem até {{ withdrawalDeadline }} para retirar</p>
      </div>

      <section class="summary-card">
        <div v-for="item in items" :key="item.product.id" class="summary-item-row">
          <span class="item-label">Item</span>
          <span class="item-value"
            >{{ item.product.name }} ({{ item.quantity }}un)</span
          >
        </div>

        <div class="summary-row">
          <span>Subtotal</span>
          <span>{{ money(subtotal) }}</span>
        </div>
        <div class="summary-row savings">
          <span>Economia total</span>
          <span>- {{ money(totalSavings) }}</span>
        </div>
        <div class="summary-row total">
          <span>Total</span>
          <span>{{ money(subtotal) }}</span>
        </div>

        <div class="savings-pill">Economizou {{ money(totalSavings) }}!</div>
      </section>

      <section class="code-card">
        <p class="code-label">CÓDIGO DA RESERVA</p>
        <p class="code-value">{{ lastReservationCode.value.split('').join(' ') }}</p>
      </section>
    </main>

    <div class="footer">
      <button class="home-btn" @click="backToHome">Voltar ao início</button>
    </div>

    <BottomNav />
  </div>
</template>

<style scoped>
.screen {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--cf-bg);
}

.header {
  background: var(--cf-orange);
  padding: 18px 16px;
  border-radius: 0 0 var(--cf-radius-lg) var(--cf-radius-lg);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

.title {
  font-size: 17px;
  font-weight: 800;
  color: #1a1a1a;
}

.count-badge {
  background: var(--cf-pink);
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 999px;
}

.content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.success-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 24px 0 20px;
}

.check-circle {
  width: 64px;
  height: 64px;
  border-radius: 999px;
  background: rgba(46, 204, 113, 0.18);
  color: var(--cf-green);
  font-size: 28px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 6px;
}

.success-title {
  font-size: 16px;
  font-weight: 800;
}

.success-subtitle {
  font-size: 12px;
  color: var(--cf-text-muted);
}

.summary-card {
  background: var(--cf-card);
  border-radius: var(--cf-radius-md);
  padding: 16px;
  margin-bottom: 14px;
}

.summary-item-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  font-size: 12px;
  padding: 4px 0;
  color: var(--cf-text-muted);
}

.item-value {
  color: var(--cf-text);
  text-align: right;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: var(--cf-text-muted);
  padding: 6px 0;
}

.summary-row.savings {
  color: var(--cf-pink-soft);
}

.summary-row.total {
  color: var(--cf-text);
  font-size: 16px;
  font-weight: 800;
  border-top: 1px solid var(--cf-border);
  margin-top: 6px;
  padding-top: 12px;
}

.savings-pill {
  margin-top: 12px;
  background: var(--cf-pink);
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  text-align: center;
  padding: 8px;
  border-radius: 999px;
}

.code-card {
  background: var(--cf-card-soft);
  border: 1px dashed var(--cf-orange);
  border-radius: var(--cf-radius-md);
  padding: 16px;
  text-align: center;
}

.code-label {
  font-size: 10px;
  letter-spacing: 0.08em;
  color: var(--cf-text-muted);
  margin-bottom: 6px;
}

.code-value {
  font-size: 26px;
  font-weight: 800;
  color: var(--cf-orange-soft);
  letter-spacing: 0.12em;
}

.footer {
  padding: 8px 16px 16px;
  flex-shrink: 0;
}

.home-btn {
  width: 100%;
  background: transparent;
  border: 1px solid var(--cf-border);
  color: var(--cf-text);
  border-radius: var(--cf-radius-sm);
  padding: 14px;
  font-size: 14px;
  font-weight: 700;
}
</style>
