<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import MerchantHeader from "@/components/merchant/MerchantHeader.vue";
import MerchantBottomNav from "@/components/merchant/MerchantBottomNav.vue";
import { useMerchantStore } from "@/stores/useMerchantStore";
import { useToastStore } from "@/stores/useToastStore";
import { storeToRefs } from "pinia";
import SvgIcon from "@/components/ui/SvgIcon.vue";

const router = useRouter();
const merchantStore = useMerchantStore();
const toast = useToastStore();
const { storeInfo } = storeToRefs(merchantStore);

type ActiveModal =
  | null
  | "store"
  | "hours"
  | "payments"
  | "notifications"
  | "help";

const activeModal = ref<ActiveModal>(null);
const isSaving = ref(false);

const storeForm = ref({
  name: "",
  category: "",
  phone: "",
  address: "",
  cnpj: "",
});

const hoursForm = ref("Seg a Sáb: 07h às 20h · Dom: 07h às 13h");

const availablePaymentMethods = [
  "PIX",
  "Cartão de Crédito",
  "Cartão de Débito",
  "Vale-Refeição (VR / Alelo / Sodexo)",
  "Dinheiro na Retirada",
];
const selectedPayments = ref<string[]>([]);

const notificationsEnabled = ref(true);

onMounted(async () => {
  await merchantStore.fetchStoreInfo();
  syncForms();
});

function syncForms() {
  storeForm.value = {
    name: storeInfo.value.name || "Padaria Central",
    category: storeInfo.value.category || "Padaria e Confeitaria",
    phone: storeInfo.value.phone || "(17) 99999-0000",
    address: storeInfo.value.address || "Av. Bady Bassitt, 1200 - Centro",
    cnpj: storeInfo.value.cnpj || "12.345.678/0001-99",
  };
  hoursForm.value =
    storeInfo.value.openingHours || "Seg a Sáb: 07h às 20h · Dom: 07h às 13h";
  selectedPayments.value = (storeInfo.value.paymentMethods || "PIX,Cartão,Dinheiro")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
  notificationsEnabled.value = storeInfo.value.notificationsEnabled ?? true;
}

function openModal(modal: ActiveModal) {
  syncForms();
  activeModal.value = modal;
}

function togglePaymentMethod(method: string) {
  const idx = selectedPayments.value.indexOf(method);
  if (idx >= 0) {
    selectedPayments.value.splice(idx, 1);
  } else {
    selectedPayments.value.push(method);
  }
}

async function saveStoreData() {
  isSaving.value = true;
  const ok = await merchantStore.updateStoreInfo({
    name: storeForm.value.name,
    category: storeForm.value.category,
    phone: storeForm.value.phone,
    address: storeForm.value.address,
    cnpj: storeForm.value.cnpj,
  });
  isSaving.value = false;
  if (ok) {
    toast.addToast("Dados da loja salvos com sucesso!", "success");
    activeModal.value = null;
  } else {
    toast.addToast("Erro ao salvar dados da loja", "error");
  }
}

async function saveHours() {
  isSaving.value = true;
  const ok = await merchantStore.updateStoreInfo({
    openingHours: hoursForm.value,
  });
  isSaving.value = false;
  if (ok) {
    toast.addToast("Horário de funcionamento atualizado!", "success");
    activeModal.value = null;
  } else {
    toast.addToast("Erro ao salvar horário", "error");
  }
}

async function savePayments() {
  if (selectedPayments.value.length === 0) {
    toast.addToast("Selecione pelo menos uma forma de pagamento", "error");
    return;
  }
  isSaving.value = true;
  const ok = await merchantStore.updateStoreInfo({
    paymentMethods: selectedPayments.value.join(", "),
  });
  isSaving.value = false;
  if (ok) {
    toast.addToast("Formas de pagamento atualizadas!", "success");
    activeModal.value = null;
  } else {
    toast.addToast("Erro ao salvar formas de pagamento", "error");
  }
}

async function saveNotifications() {
  isSaving.value = true;
  const ok = await merchantStore.updateStoreInfo({
    notificationsEnabled: notificationsEnabled.value,
  });
  isSaving.value = false;
  if (ok) {
    toast.addToast("Preferências de notificação salvas!", "success");
    activeModal.value = null;
  } else {
    toast.addToast("Erro ao salvar notificações", "error");
  }
}

const planLabel = computed(() => {
  if (storeInfo.value.plan === "annual") return "PRO Anual VIP";
  if (storeInfo.value.plan === "free") return "Gratuito";
  return "PRO Mensal";
});

async function handleResetDemo() {
  isSaving.value = true;
  await merchantStore.resetDemoData();
  syncForms();
  isSaving.value = false;
  activeModal.value = null;
}

const logout = () => {
  localStorage.removeItem("user");
  localStorage.removeItem("cf_token");
  router.push("/start");
};
</script>

<template>
  <div class="screen">
    <MerchantHeader
      title="Configurações"
      :subtitle="storeInfo.name || 'Padaria Central'"
    />

    <main class="content">
      <!-- Resumo Rápido da Loja -->
      <div class="store-overview-card">
        <div class="store-avatar">
          <SvgIcon name="store" :size="22" />
        </div>
        <div class="store-overview-info">
          <p class="store-overview-name">{{ storeInfo.name }}</p>
          <p class="store-overview-meta">
            {{ storeInfo.category }} · {{ storeInfo.openingHours }}
          </p>
          <p class="store-overview-address">
            <SvgIcon name="map-pin" :size="12" />
            <span>{{ storeInfo.address }}</span>
          </p>
        </div>
      </div>

      <div class="menu-card">
        <button class="menu-row" @click="openModal('store')">
          <span class="menu-item-content">
            <span class="menu-icon">
              <SvgIcon name="store" :size="18" />
            </span>
            <div>
              <p class="row-title">Dados da loja</p>
              <p class="row-sub">Nome, endereço, telefone e CNPJ</p>
            </div>
          </span>
          <span class="chevron-icon">
            <SvgIcon name="chevron-right" :size="16" />
          </span>
        </button>

        <button class="menu-row" @click="openModal('hours')">
          <span class="menu-item-content">
            <span class="menu-icon">
              <SvgIcon name="clock" :size="18" />
            </span>
            <div>
              <p class="row-title">Horário de funcionamento</p>
              <p class="row-sub">{{ storeInfo.openingHours }}</p>
            </div>
          </span>
          <span class="chevron-icon">
            <SvgIcon name="chevron-right" :size="16" />
          </span>
        </button>

        <button class="menu-row" @click="openModal('payments')">
          <span class="menu-item-content">
            <span class="menu-icon">
              <SvgIcon name="wallet" :size="18" />
            </span>
            <div>
              <p class="row-title">Formas de pagamento aceitas</p>
              <p class="row-sub">{{ storeInfo.paymentMethods }}</p>
            </div>
          </span>
          <span class="chevron-icon">
            <SvgIcon name="chevron-right" :size="16" />
          </span>
        </button>

        <button class="menu-row" @click="router.push('/comerciante/planos')">
          <span class="menu-item-content">
            <span class="menu-icon pro-icon">
              <SvgIcon name="star-filled" :size="18" />
            </span>
            <div>
              <p class="row-title">Assinatura CheapFood Pro</p>
              <p class="row-sub">Plano atual: {{ planLabel }}</p>
            </div>
          </span>
          <span class="chevron-icon">
            <SvgIcon name="chevron-right" :size="16" />
          </span>
        </button>

        <button class="menu-row" @click="router.push('/comerciante/historico')">
          <span class="menu-item-content">
            <span class="menu-icon">
              <SvgIcon name="receipt" :size="18" />
            </span>
            <div>
              <p class="row-title">Histórico de Vendas</p>
              <p class="row-sub">Pedidos retirados e expirados</p>
            </div>
          </span>
          <span class="chevron-icon">
            <SvgIcon name="chevron-right" :size="16" />
          </span>
        </button>

        <button class="menu-row" @click="openModal('notifications')">
          <span class="menu-item-content">
            <span class="menu-icon">
              <SvgIcon name="sparkles" :size="18" />
            </span>
            <div>
              <p class="row-title">Notificações e Alertas</p>
              <p class="row-sub">
                {{
                  storeInfo.notificationsEnabled
                    ? "Ativadas (reservas e validade)"
                    : "Silenciadas"
                }}
              </p>
            </div>
          </span>
          <span class="chevron-icon">
            <SvgIcon name="chevron-right" :size="16" />
          </span>
        </button>

        <button class="menu-row" @click="openModal('help')">
          <span class="menu-item-content">
            <span class="menu-icon">
              <SvgIcon name="help-circle" :size="18" />
            </span>
            <div>
              <p class="row-title">Central de ajuda do parceiro</p>
              <p class="row-sub">Dúvidas sobre leilões, retiradas e repasses</p>
            </div>
          </span>
          <span class="chevron-icon">
            <SvgIcon name="chevron-right" :size="16" />
          </span>
        </button>
      </div>

      <div class="menu-card">
        <button class="menu-row" @click="handleResetDemo" :disabled="isSaving">
          <span class="menu-item-content">
            <span class="menu-icon">
              <SvgIcon name="repeat" :size="18" />
            </span>
            <div>
              <p class="row-title">Restaurar Cenário da Apresentação</p>
              <p class="row-sub">
                Recria os 12 produtos, leilões ativos e histórico inicial
              </p>
            </div>
          </span>
          <span class="chevron-icon">
            <SvgIcon name="chevron-right" :size="16" />
          </span>
        </button>

        <button class="menu-row danger" @click="logout">
          <span class="menu-item-content">
            <span class="menu-icon danger-icon">
              <SvgIcon name="log-out" :size="18" />
            </span>
            Sair da conta
          </span>
        </button>
      </div>
    </main>

    <!-- MODAL: DADOS DA LOJA -->
    <div
      v-if="activeModal === 'store'"
      class="modal-overlay"
      @click.self="activeModal = null"
    >
      <div class="modal-card">
        <h3 class="modal-title">Editar Dados da Loja</h3>
        <div class="form-fields">
          <label class="field">
            <span>Nome Fantasia</span>
            <input v-model="storeForm.name" type="text" />
          </label>
          <label class="field">
            <span>Ramo / Categoria</span>
            <input v-model="storeForm.category" type="text" />
          </label>
          <label class="field">
            <span>Endereço de Retirada</span>
            <input v-model="storeForm.address" type="text" />
          </label>
          <div class="row-2">
            <label class="field">
              <span>Telefone</span>
              <input v-model="storeForm.phone" type="text" />
            </label>
            <label class="field">
              <span>CNPJ</span>
              <input v-model="storeForm.cnpj" type="text" />
            </label>
          </div>
        </div>
        <div class="modal-actions">
          <button class="btn-cancel" @click="activeModal = null">Cancelar</button>
          <button class="btn-save" :disabled="isSaving" @click="saveStoreData">
            {{ isSaving ? "Salvando..." : "Salvar" }}
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL: HORÁRIO DE FUNCIONAMENTO -->
    <div
      v-if="activeModal === 'hours'"
      class="modal-overlay"
      @click.self="activeModal = null"
    >
      <div class="modal-card">
        <h3 class="modal-title">Horário de Funcionamento</h3>
        <p class="modal-desc">
          Defina o horário limite para os clientes retirarem seus pedidos no balcão.
        </p>
        <label class="field">
          <span>Horário exibido aos clientes</span>
          <input
            v-model="hoursForm"
            type="text"
            placeholder="Ex: Seg a Sáb: 07h às 20h"
          />
        </label>
        <div class="presets">
          <button
            type="button"
            class="preset-chip"
            @click="hoursForm = 'Seg a Sáb: 07h às 20h · Dom: 07h às 13h'"
          >
            Comercial + Domingos
          </button>
          <button
            type="button"
            class="preset-chip"
            @click="hoursForm = 'Todos os dias: 08h às 22h'"
          >
            Todos os dias (08h-22h)
          </button>
        </div>
        <div class="modal-actions">
          <button class="btn-cancel" @click="activeModal = null">Cancelar</button>
          <button class="btn-save" :disabled="isSaving" @click="saveHours">
            Salvar Horário
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL: FORMAS DE PAGAMENTO -->
    <div
      v-if="activeModal === 'payments'"
      class="modal-overlay"
      @click.self="activeModal = null"
    >
      <div class="modal-card">
        <h3 class="modal-title">Formas de Pagamento</h3>
        <p class="modal-desc">
          Selecione os métodos aceitos para reserva e retirada na sua loja:
        </p>
        <div class="check-list">
          <label
            v-for="m in availablePaymentMethods"
            :key="m"
            class="check-item"
            @click.prevent="togglePaymentMethod(m)"
          >
            <input type="checkbox" :checked="selectedPayments.includes(m)" />
            <span>{{ m }}</span>
          </label>
        </div>
        <div class="modal-actions">
          <button class="btn-cancel" @click="activeModal = null">Cancelar</button>
          <button class="btn-save" :disabled="isSaving" @click="savePayments">
            Salvar Métodos
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL: NOTIFICAÇÕES -->
    <div
      v-if="activeModal === 'notifications'"
      class="modal-overlay"
      @click.self="activeModal = null"
    >
      <div class="modal-card">
        <h3 class="modal-title">Notificações da Loja</h3>
        <p class="modal-desc">
          Receba avisos quando novos clientes reservarem produtos ou derem lances em leilões.
        </p>
        <label
          class="check-item"
          @click.prevent="notificationsEnabled = !notificationsEnabled"
        >
          <input type="checkbox" :checked="notificationsEnabled" />
          <span>Ativar alertas de reservas, lances e validade</span>
        </label>
        <div class="modal-actions" style="margin-top: 16px">
          <button class="btn-cancel" @click="activeModal = null">Cancelar</button>
          <button
            class="btn-save"
            :disabled="isSaving"
            @click="saveNotifications"
          >
            Salvar
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL: CENTRAL DE AJUDA -->
    <div
      v-if="activeModal === 'help'"
      class="modal-overlay"
      @click.self="activeModal = null"
    >
      <div class="modal-card">
        <h3 class="modal-title">Central de Ajuda do Parceiro</h3>
        <div class="faq-list">
          <div class="faq-box">
            <strong>1. Como confirmar a retirada de um pedido?</strong>
            <p>
              Peça o código PIN de 4 dígitos ao cliente e clique em "Confirmar retirada" na aba Pedidos.
            </p>
          </div>
          <div class="faq-box">
            <strong>2. Como funciona o Leilão Híbrido?</strong>
            <p>
              Você define um lance inicial menor e um preço de Compra Imediata. Clientes podem disputar lances ou arrematar na hora!
            </p>
          </div>
          <div class="faq-box">
            <strong>3. O que fazer quando um produto vence na vitrine?</strong>
            <p>
              Se o item ainda estiver próprio para consumo imediato, use o botão "+20% Desconto e Reativar" na aba Vencidos.
            </p>
          </div>
        </div>
        <div class="modal-actions" style="margin-top: 16px">
          <button class="btn-save" @click="activeModal = null">Entendi</button>
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
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.store-overview-card {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: var(--cf-radius-md);
  padding: 14px 16px;
}

.store-avatar {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  background: var(--mc-purple-soft);
  color: var(--mc-navy);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  line-height: 0;
}

.store-overview-name {
  font-size: 15px;
  font-weight: 800;
  color: var(--mc-navy);
}

.store-overview-meta {
  font-size: 11px;
  color: var(--mc-text-muted);
  margin-top: 2px;
}

.store-overview-address {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: var(--mc-navy);
  font-weight: 600;
  margin-top: 4px;
}

.menu-card {
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: var(--cf-radius-md);
  overflow: hidden;
}

.menu-row {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: transparent;
  border: none;
  color: var(--mc-text);
  font-size: 13px;
  font-weight: 500;
  padding: 14px 16px;
  border-bottom: 1px solid var(--mc-border);
  text-align: left;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.menu-row:last-child {
  border-bottom: none;
}

.menu-row:hover {
  background-color: var(--cf-bg, #fafafa);
}

.menu-item-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.row-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--mc-text);
}

.row-sub {
  font-size: 11px;
  color: var(--mc-text-muted);
  margin-top: 2px;
}

.menu-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: var(--mc-purple-soft, #f0eeff);
  color: var(--mc-navy, #1b3b5f);
  flex-shrink: 0;
  line-height: 0;
}

.pro-icon {
  background: #fff4d6;
  color: #b46900;
}

.danger-icon {
  background: #fff0f0;
  color: var(--mc-danger, #e74c3c);
}

.chevron-icon {
  color: var(--mc-text-muted);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  line-height: 0;
}

.menu-row.danger {
  color: var(--mc-danger, #e74c3c);
  font-weight: 700;
}

/* Modals */
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
  padding: 20px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
}

.modal-title {
  font-size: 17px;
  font-weight: 800;
  color: var(--mc-navy);
  margin-bottom: 8px;
}

.modal-desc {
  font-size: 12px;
  color: var(--mc-text-muted);
  margin-bottom: 14px;
  line-height: 1.4;
}

.form-fields {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 16px;
}

.row-2 {
  display: flex;
  gap: 8px;
}

.row-2 .field {
  flex: 1;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.field span {
  font-size: 11px;
  font-weight: 700;
  color: var(--mc-text-muted);
}

.field input {
  border: 1px solid var(--mc-border);
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 13px;
  outline: none;
}

.presets {
  display: flex;
  gap: 8px;
  margin: 10px 0 16px;
  flex-wrap: wrap;
}

.preset-chip {
  background: #f0f4f8;
  color: var(--mc-navy);
  border: none;
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
}

.check-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.check-item {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #f8fafc;
  border: 1px solid var(--mc-border);
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.faq-box {
  background: #f8fafc;
  border: 1px solid var(--mc-border);
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 12px;
}

.faq-box strong {
  display: block;
  color: var(--mc-navy);
  margin-bottom: 4px;
}

.faq-box p {
  color: var(--mc-text-muted);
  line-height: 1.4;
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
  padding: 11px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.btn-save {
  flex: 1;
  background: var(--mc-navy);
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 11px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}
</style>
