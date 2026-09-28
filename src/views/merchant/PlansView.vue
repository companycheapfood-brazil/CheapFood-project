<script setup lang="ts">
import MerchantBottomNav from '@/components/merchant/MerchantBottomNav.vue'
import { ref } from 'vue'

const selectedPlan = ref<'free' | 'monthly' | 'annual'>('monthly')
</script>

<template>
  <div class="screen">
    <header class="plans-header">
      <h1 class="header-title">Planos FoodSaver</h1>
    </header>

    <main class="content">
      <p class="plans-subtitle">Para comerciantes — escolha seu plano</p>

      <!-- Gratuito -->
      <div
        class="plan-card"
        :class="{ selected: selectedPlan === 'free' }"
        @click="selectedPlan = 'free'"
      >
        <div class="plan-top">
          <div>
            <h3 class="plan-name">Gratuito</h3>
            <p class="plan-desc">Para experimentar</p>
          </div>
          <p class="plan-price">R$0</p>
        </div>
        <ul class="plan-features">
          <li>5 produtos/mês</li>
          <li>Perfil básico</li>
          <li class="disabled">Relatórios</li>
        </ul>
      </div>

      <!-- Pro Mensal -->
      <div
        class="plan-card highlight"
        :class="{ selected: selectedPlan === 'monthly' }"
        @click="selectedPlan = 'monthly'"
      >
        <span class="popular-badge">Mais popular</span>
        <div class="plan-top">
          <div>
            <h3 class="plan-name">Pro Mensal</h3>
          </div>
          <p class="plan-price">R$49<span class="price-period">/mês</span></p>
        </div>
        <ul class="plan-features">
          <li>Produtos ilimitados</li>
          <li>Relatórios de vendas</li>
          <li>Alertas automáticos</li>
          <li>Destaque nas buscas</li>
        </ul>
      </div>

      <!-- Pro Anual -->
      <div
        class="plan-card highlight"
        :class="{ selected: selectedPlan === 'annual' }"
        @click="selectedPlan = 'annual'"
      >
        <div class="plan-top">
          <div>
            <h3 class="plan-name">Pro Anual</h3>
            <p class="plan-savings">Economize R$189 vs mensal</p>
            <p class="plan-desc">Tudo do Pro + suporte VIP</p>
          </div>
          <p class="plan-price">R$399<span class="price-period">/ano</span></p>
        </div>
      </div>

      <button class="cta-btn">Assinar Pro agora</button>
    </main>

    <MerchantBottomNav />
  </div>
</template>

<style scoped>
.screen {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #fff;
  color: #1a1a2e;
}

.plans-header {
  background: #f5a623;
  padding: 20px 18px;
  border-radius: 0 0 22px 22px;
  flex-shrink: 0;
}

.header-title {
  font-size: 17px;
  font-weight: 800;
  color: #fff;
}

.content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.plans-subtitle {
  text-align: center;
  font-size: 13px;
  color: #7a7a8c;
  margin-bottom: 20px;
}

.plan-card {
  background: #fff;
  border: 1px solid #eceaf4;
  border-radius: 16px;
  padding: 18px;
  margin-bottom: 14px;
  cursor: pointer;
  transition: border-color 0.2s;
  position: relative;
}

.plan-card.highlight {
  border-color: #f5a623;
  border-width: 2px;
}

.plan-card.selected {
  box-shadow: 0 0 0 2px #f5a623;
}

.popular-badge {
  display: inline-block;
  background: #f5a623;
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 999px;
  margin-bottom: 10px;
}

.plan-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.plan-name {
  font-size: 16px;
  font-weight: 800;
  margin: 0;
}

.plan-desc {
  font-size: 12px;
  color: #7a7a8c;
  margin-top: 2px;
}

.plan-savings {
  font-size: 12px;
  color: #f5a623;
  font-weight: 700;
  margin-top: 2px;
}

.plan-price {
  font-size: 28px;
  font-weight: 900;
  color: #1a1a2e;
  margin: 0;
  line-height: 1;
}

.price-period {
  font-size: 14px;
  font-weight: 500;
  color: #7a7a8c;
}

.plan-features {
  list-style: none;
  padding: 0;
  margin-top: 14px;
}

.plan-features li {
  font-size: 13px;
  color: #1a1a2e;
  padding: 3px 0;
  padding-left: 8px;
}

.plan-features li.disabled {
  color: #c0c0c5;
}

.cta-btn {
  width: 100%;
  background: #f5a623;
  color: #fff;
  border: none;
  border-radius: 16px;
  padding: 16px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  margin-top: 8px;
  transition: all 0.2s;
}

.cta-btn:hover {
  background: #e09515;
  transform: translateY(-1px);
}
</style>
