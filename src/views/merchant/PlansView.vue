<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import MerchantHeader from "@/components/merchant/MerchantHeader.vue";
import MerchantBottomNav from "@/components/merchant/MerchantBottomNav.vue";
import { useToastStore } from "@/stores/useToastStore";
import { useMerchantStore } from "@/stores/useMerchantStore";
import { storeToRefs } from "pinia";
import SvgIcon from "@/components/ui/SvgIcon.vue";

const toast = useToastStore();
const merchantStore = useMerchantStore();
const { storeInfo } = storeToRefs(merchantStore);

const selectedPlan = ref<"free" | "monthly" | "annual">("monthly");
const showCheckoutModal = ref(false);
const isActivating = ref(false);

onMounted(async () => {
  await merchantStore.fetchStoreInfo();
  if (storeInfo.value.plan) {
    selectedPlan.value = storeInfo.value.plan;
  }
});

const currentPlan = computed(() => storeInfo.value.plan || "monthly");

const planDetails = {
  free: {
    name: "Gratuito",
    price: "R$ 0",
    period: "/mês",
    summary: "Plano básico com limite de 5 ofertas por mês.",
  },
  monthly: {
    name: "Pro Mensal",
    price: "R$ 49,00",
    period: "/mês",
    summary: "Ofertas e leilões ilimitados, IA de cadastro e relatórios completos.",
  },
  annual: {
    name: "Pro Anual VIP",
    price: "R$ 399,00",
    period: "/ano",
    summary: "Economia de R$ 189/ano + destaque máximo nas buscas e suporte VIP.",
  },
};

function openSubscribeModal() {
  if (selectedPlan.value === currentPlan.value) {
    toast.addToast("Este já é o plano ativo da sua loja!", "info");
    return;
  }
  showCheckoutModal.value = true;
}

async function confirmPlanChange() {
  isActivating.value = true;
  try {
    const ok = await merchantStore.updatePlan(selectedPlan.value);
    if (ok) {
      await merchantStore.fetchDashboardStats();
      toast.addToast(
        `Plano ${planDetails[selectedPlan.value].name} ativado com sucesso!`,
        "success",
      );
      showCheckoutModal.value = false;
    } else {
      toast.addToast("Erro ao atualizar plano", "error");
    }
  } finally {
    isActivating.value = false;
  }
}
</script>

<template>
  <div class="screen">
    <MerchantHeader
      title="Planos CheapFood Pro"
      subtitle="Gerencie a assinatura do seu estabelecimento"
      backTo="/comerciante/config"
    />

    <main class="content">
      <p class="plans-subtitle">
        Aumente o alcance das suas ofertas e recupere mais receita
      </p>

      <!-- Gratuito -->
      <div
        class="plan-card"
        :class="{ selected: selectedPlan === 'free' }"
        @click="selectedPlan = 'free'"
      >
        <span v-if="currentPlan === 'free'" class="current-badge">Plano Atual</span>
        <div class="plan-top">
          <div>
            <h3 class="plan-name">Gratuito</h3>
            <p class="plan-desc">Para experimentar a plataforma</p>
          </div>
          <p class="plan-price">R$ 0</p>
        </div>
        <ul class="plan-features">
          <li><SvgIcon name="check-circle" :size="14" class="feat-ok" /> Até 5 produtos ativos/mês</li>
          <li><SvgIcon name="check-circle" :size="14" class="feat-ok" /> Perfil básico da loja</li>
          <li class="disabled"><SvgIcon name="x" :size="14" class="feat-no" /> Leilões relâmpago ilimitados</li>
          <li class="disabled"><SvgIcon name="x" :size="14" class="feat-no" /> Relatórios avançados de faturamento</li>
        </ul>
      </div>

      <!-- Pro Mensal -->
      <div
        class="plan-card highlight"
        :class="{ selected: selectedPlan === 'monthly' }"
        @click="selectedPlan = 'monthly'"
      >
        <div class="badges-line">
          <span class="popular-badge">Mais popular</span>
          <span v-if="currentPlan === 'monthly'" class="current-badge">Plano Atual</span>
        </div>
        <div class="plan-top">
          <div>
            <h3 class="plan-name">Pro Mensal</h3>
            <p class="plan-desc">Ideal para padarias, mercados e hortifrutis</p>
          </div>
          <p class="plan-price">R$ 49<span class="price-period">/mês</span></p>
        </div>
        <ul class="plan-features">
          <li><SvgIcon name="check-circle" :size="14" class="feat-ok" /> Produtos e Leilões Híbridos ilimitados</li>
          <li><SvgIcon name="check-circle" :size="14" class="feat-ok" /> Cadastro inteligente com IA (Visão Computacional)</li>
          <li><SvgIcon name="check-circle" :size="14" class="feat-ok" /> Dashboard completo de receita recuperada</li>
          <li><SvgIcon name="check-circle" :size="14" class="feat-ok" /> Destaque prioritário nas buscas da região</li>
        </ul>
      </div>

      <!-- Pro Anual -->
      <div
        class="plan-card highlight"
        :class="{ selected: selectedPlan === 'annual' }"
        @click="selectedPlan = 'annual'"
      >
        <div class="badges-line">
          <span class="vip-badge">Melhor Custo-Benefício</span>
          <span v-if="currentPlan === 'annual'" class="current-badge">Plano Atual</span>
        </div>
        <div class="plan-top">
          <div>
            <h3 class="plan-name">Pro Anual VIP</h3>
            <p class="plan-savings">Economize R$ 189 em relação ao mensal</p>
            <p class="plan-desc">Tudo do Pro + Selo Parceiro Sustentável</p>
          </div>
          <p class="plan-price">R$ 399<span class="price-period">/ano</span></p>
        </div>
        <ul class="plan-features">
          <li><SvgIcon name="check-circle" :size="14" class="feat-ok" /> Todos os recursos do Pro Mensal</li>
          <li><SvgIcon name="check-circle" :size="14" class="feat-ok" /> Taxa zero em reservas via aplicativo</li>
          <li><SvgIcon name="check-circle" :size="14" class="feat-ok" /> Relatório ESG de impacto ambiental (kg salvos)</li>
          <li><SvgIcon name="check-circle" :size="14" class="feat-ok" /> Suporte prioritário 24/7</li>
        </ul>
      </div>

      <button
        class="cta-btn"
        :disabled="selectedPlan === currentPlan"
        @click="openSubscribeModal"
      >
        <SvgIcon v-if="selectedPlan === currentPlan" name="check-circle" :size="16" />
        {{
          selectedPlan === currentPlan
            ? "Este já é seu plano atual"
            : `Ativar ${planDetails[selectedPlan].name}`
        }}
      </button>
    </main>

    <!-- Modal de Confirmação / Simulação TCC -->
    <div
      v-if="showCheckoutModal"
      class="modal-overlay"
      @click.self="showCheckoutModal = false"
    >
      <div class="modal-card">
        <div class="modal-badge">MODO APRESENTAÇÃO</div>
        <h3 class="modal-title">
          Confirmar {{ planDetails[selectedPlan].name }}
        </h3>
        <p class="modal-desc">{{ planDetails[selectedPlan].summary }}</p>

        <div class="price-summary">
          <span>Valor da assinatura</span>
          <strong
            >{{ planDetails[selectedPlan].price
            }}{{ planDetails[selectedPlan].period }}</strong
          >
        </div>

        <div class="sim-info">
          <SvgIcon name="sparkles" :size="15" />
          <span>No modo de apresentação, a ativação do plano é imediata e sem cobrança real.</span>
        </div>

        <div class="modal-actions">
          <button class="btn-cancel" @click="showCheckoutModal = false">
            Cancelar
          </button>
          <button
            class="btn-confirm"
            :disabled="isActivating"
            @click="confirmPlanChange"
          >
            {{ isActivating ? "Ativando..." : "Confirmar Assinatura" }}
          </button>
        </div>
      </div>
    </div>

    <MerchantBottomNav />
  </div>
</template>

<style scoped>
.screen {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--mc-bg);
  color: var(--mc-text);
}

.content {
  flex: 1;
  padding: 16px;
  padding-bottom: 100px;
  overflow-y: auto;
}

.plans-subtitle {
  text-align: center;
  font-size: 13px;
  color: var(--mc-text-muted);
  margin-bottom: 16px;
}

.plan-card {
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: 16px;
  padding: 18px;
  margin-bottom: 14px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.plan-card.highlight {
  border-color: rgba(27, 59, 95, 0.25);
}

.plan-card.selected {
  border-color: var(--mc-navy);
  box-shadow: 0 0 0 2px var(--mc-navy);
}

.badges-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.popular-badge {
  display: inline-block;
  background: var(--cf-orange);
  color: #1a1a1a;
  font-size: 10px;
  font-weight: 800;
  padding: 4px 12px;
  border-radius: 999px;
}

.vip-badge {
  display: inline-block;
  background: var(--mc-navy);
  color: #fff;
  font-size: 10px;
  font-weight: 800;
  padding: 4px 12px;
  border-radius: 999px;
}

.current-badge {
  display: inline-block;
  background: #e6f6ec;
  color: #1f8a4c;
  font-size: 10px;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 999px;
  margin-bottom: 6px;
}

.badges-line .current-badge {
  margin-bottom: 0;
}

.plan-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.plan-name {
  font-size: 16px;
  font-weight: 800;
  color: var(--mc-navy);
  margin: 0;
}

.plan-desc {
  font-size: 12px;
  color: var(--mc-text-muted);
  margin-top: 2px;
}

.plan-savings {
  font-size: 12px;
  color: var(--mc-green, #2a9d8f);
  font-weight: 700;
  margin-top: 2px;
}

.plan-price {
  font-size: 26px;
  font-weight: 900;
  color: var(--mc-navy);
  margin: 0;
  line-height: 1;
}

.price-period {
  font-size: 13px;
  font-weight: 500;
  color: var(--mc-text-muted);
}

.plan-features {
  list-style: none;
  padding: 0;
  margin-top: 14px;
}

.plan-features li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--mc-text);
  padding: 4px 0;
  font-weight: 500;
}

.feat-ok {
  color: #1f8a4c;
}

.feat-no {
  color: #b8c2cc;
}

.plan-features li.disabled {
  color: #b8c2cc;
}

.cta-btn {
  width: 100%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: var(--mc-navy);
  color: #fff;
  border: none;
  border-radius: 14px;
  padding: 16px;
  font-size: 15px;
  font-weight: 800;
  cursor: pointer;
  margin-top: 8px;
  transition: all 0.2s;
}

.cta-btn:disabled {
  background: #cbd5e1;
  color: #475569;
  cursor: default;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
}

.modal-card {
  background: #fff;
  border-radius: 18px;
  padding: 22px;
  width: 100%;
  max-width: 390px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
}

.modal-badge {
  display: inline-block;
  font-size: 10px;
  font-weight: 800;
  color: var(--mc-navy);
  background: #e8f0fe;
  padding: 4px 10px;
  border-radius: 999px;
  margin-bottom: 10px;
}

.modal-title {
  font-size: 18px;
  font-weight: 800;
  color: var(--mc-navy);
  margin-bottom: 6px;
}

.modal-desc {
  font-size: 13px;
  color: var(--mc-text-muted);
  line-height: 1.4;
  margin-bottom: 16px;
}

.price-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
  border: 1px solid var(--mc-border);
  padding: 12px 14px;
  border-radius: 12px;
  font-size: 13px;
  margin-bottom: 14px;
}

.price-summary strong {
  color: var(--mc-navy);
  font-size: 16px;
}

.sim-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  background: #fff8e6;
  color: #8a5300;
  padding: 10px 12px;
  border-radius: 10px;
  line-height: 1.4;
  margin-bottom: 18px;
}

.modal-actions {
  display: flex;
  gap: 10px;
}

.btn-cancel {
  flex: 1;
  background: transparent;
  border: 1px solid var(--mc-border);
  color: var(--mc-text-muted);
  border-radius: 10px;
  padding: 12px;
  font-weight: 700;
  font-size: 13px;
  cursor: pointer;
}

.btn-confirm {
  flex: 1;
  background: var(--mc-navy);
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 12px;
  font-weight: 700;
  font-size: 13px;
  cursor: pointer;
}
</style>
