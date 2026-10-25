<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { storeToRefs } from "pinia";
import { useSidebarStore } from "@/stores/useSidebarStore";
import { useCartStore } from "@/stores/useCartStore";
import { useToastStore } from "@/stores/useToastStore";
import AuthService from "@/services/auth.service";
import SvgIcon from "@/components/ui/SvgIcon.vue";

const router = useRouter();
const route = useRoute();
const sidebarStore = useSidebarStore();
const cartStore = useCartStore();
const toast = useToastStore();

const { isOpen, mobileFrame } = storeToRefs(sidebarStore);
const { totalItems } = storeToRefs(cartStore);
const isSwitching = ref(false);

const isMerchantRoute = computed(() => route.path.startsWith("/comerciante"));

const currentUser = computed(() => {
  try {
    const raw = localStorage.getItem("user");
    if (raw) return JSON.parse(raw);
  } catch {}
  return {
    name: isMerchantRoute.value ? "Padaria Central" : "João Silva",
    email: isMerchantRoute.value ? "admin@cheapfood.com" : "joao@email.com",
  };
});

watch(
  () => route.fullPath,
  () => {
    sidebarStore.close();
  },
);

function navigateTo(path: string) {
  sidebarStore.close();
  router.push(path);
}

async function switchProfile(role: "consumer" | "merchant") {
  isSwitching.value = true;
  try {
    await AuthService.login({
      email: role === "merchant" ? "admin@cheapfood.com" : "joao@email.com",
      password: role === "merchant" ? "admin123" : "123456",
    });
    toast.addToast(
      role === "merchant"
        ? "Alternado para Painel do Lojista!"
        : "Alternado para Visão do Consumidor!",
      "success",
    );
    sidebarStore.close();
    router.push(role === "merchant" ? "/comerciante" : "/");
  } catch (e) {
    toast.addToast("Erro ao alternar perfil", "error");
  } finally {
    isSwitching.value = false;
  }
}

function handleLogout() {
  localStorage.removeItem("user");
  localStorage.removeItem("cf_token");
  sidebarStore.close();
  router.push("/start");
}

const consumerLinks = [
  { to: "/", label: "Início e Para Você", icon: "home" },
  { to: "/buscar", label: "Buscar Ofertas e Leilões", icon: "search" },
  { to: "/carrinho", label: "Meu Carrinho", icon: "shopping-cart", badge: true },
  { to: "/historico", label: "Histórico e Avaliações", icon: "receipt" },
  { to: "/perfil", label: "Meu Perfil", icon: "user" },
  { to: "/perfil/editar", label: "Editar Dados", icon: "edit" },
  { to: "/ajuda", label: "Central de Ajuda", icon: "help-circle" },
  { to: "/termos", label: "Termos e Privacidade", icon: "file-text" },
];

const merchantLinks = [
  { to: "/comerciante", label: "Dashboard e Métricas", icon: "grid" },
  { to: "/comerciante/novo", label: "Cadastrar Produto (IA)", icon: "sparkles" },
  { to: "/comerciante/produtos", label: "Meus Produtos e Leilões", icon: "shopping-bag" },
  { to: "/comerciante/pedidos", label: "Pedidos e Validar PIN", icon: "check-circle" },
  { to: "/comerciante/historico", label: "Histórico de Vendas", icon: "receipt" },
  { to: "/comerciante/planos", label: "Planos CheapFood Pro", icon: "star-filled" },
  { to: "/comerciante/config", label: "Configurações da Loja", icon: "settings" },
];
</script>

<template>
  <Transition name="sidebar-fade">
    <div
      v-if="isOpen"
      class="sidebar-overlay"
      @click.self="sidebarStore.close()"
    >
      <aside class="sidebar-drawer" :class="{ 'merchant-mode': isMerchantRoute }">
        <!-- Top Brand + Close -->
        <div class="sidebar-header">
          <div class="brand-row">
            <div class="brand-logo">
              <SvgIcon name="shopping-cart" :size="20" />
            </div>
            <div class="brand-text">
              <span class="brand-title">Cheap<span>Food</span></span>
              <span class="brand-badge">
                {{ isMerchantRoute ? "Painel Lojista" : "App Consumidor" }}
              </span>
            </div>
          </div>
          <button
            type="button"
            class="close-btn"
            aria-label="Fechar menu"
            @click="sidebarStore.close()"
          >
            <SvgIcon name="x" :size="18" />
          </button>
        </div>

        <!-- User Summary Card -->
        <div class="user-card">
          <div class="user-avatar">
            <SvgIcon :name="isMerchantRoute ? 'store' : 'user'" :size="18" />
          </div>
          <div class="user-meta">
            <p class="user-name">{{ currentUser.name || "Usuário CheapFood" }}</p>
            <p class="user-email">{{ currentUser.email || "cliente@cheapfood.com" }}</p>
          </div>
        </div>

        <!-- Scrollable Content -->
        <div class="sidebar-scroll">
          <!-- Modo Apresentação Switcher -->
          <div class="switcher-box">
            <p class="section-caption">
              <SvgIcon name="sparkles" :size="12" />
              Modo Apresentação
            </p>
            <div class="role-pills">
              <button
                type="button"
                class="role-pill"
                :class="{ active: !isMerchantRoute }"
                :disabled="isSwitching"
                @click="switchProfile('consumer')"
              >
                <SvgIcon name="shopping-cart" :size="13" />
                <span>Consumidor</span>
              </button>
              <button
                type="button"
                class="role-pill"
                :class="{ active: isMerchantRoute }"
                :disabled="isSwitching"
                @click="switchProfile('merchant')"
              >
                <SvgIcon name="store" :size="13" />
                <span>Comerciante</span>
              </button>
            </div>
            <button
              type="button"
              class="frame-toggle-btn"
              @click="sidebarStore.toggleMobileFrame()"
            >
              <SvgIcon name="smartphone" :size="14" />
              <span>{{
                mobileFrame
                  ? "Desativar Moldura Mobile (Tela Cheia)"
                  : "Ativar Moldura Mobile (430px)"
              }}</span>
            </button>
          </div>

          <!-- Navegação Principal (contextual primeiro) -->
          <template v-if="!isMerchantRoute">
            <div class="nav-group">
              <p class="nav-group-title">Navegação do Consumidor</p>
              <button
                v-for="item in consumerLinks"
                :key="item.to"
                type="button"
                class="nav-link"
                :class="{ active: route.path === item.to }"
                @click="navigateTo(item.to)"
              >
                <span class="nav-link-icon">
                  <SvgIcon :name="item.icon" :size="17" />
                </span>
                <span class="nav-link-label">{{ item.label }}</span>
                <span
                  v-if="item.badge && totalItems > 0"
                  class="nav-link-badge"
                >
                  {{ totalItems }}
                </span>
              </button>
            </div>

            <div class="nav-group">
              <p class="nav-group-title">Acesso Rápido Lojista</p>
              <button
                v-for="item in merchantLinks.slice(0, 4)"
                :key="item.to"
                type="button"
                class="nav-link subtle"
                :class="{ active: route.path === item.to }"
                @click="navigateTo(item.to)"
              >
                <span class="nav-link-icon">
                  <SvgIcon :name="item.icon" :size="16" />
                </span>
                <span class="nav-link-label">{{ item.label }}</span>
              </button>
            </div>
          </template>

          <template v-else>
            <div class="nav-group">
              <p class="nav-group-title">Gestão do Comerciante</p>
              <button
                v-for="item in merchantLinks"
                :key="item.to"
                type="button"
                class="nav-link"
                :class="{ active: route.path === item.to }"
                @click="navigateTo(item.to)"
              >
                <span class="nav-link-icon">
                  <SvgIcon :name="item.icon" :size="17" />
                </span>
                <span class="nav-link-label">{{ item.label }}</span>
              </button>
            </div>

            <div class="nav-group">
              <p class="nav-group-title">Acesso Rápido Consumidor</p>
              <button
                v-for="item in consumerLinks.slice(0, 4)"
                :key="item.to"
                type="button"
                class="nav-link subtle"
                :class="{ active: route.path === item.to }"
                @click="navigateTo(item.to)"
              >
                <span class="nav-link-icon">
                  <SvgIcon :name="item.icon" :size="16" />
                </span>
                <span class="nav-link-label">{{ item.label }}</span>
              </button>
            </div>
          </template>
        </div>

        <!-- Footer -->
        <div class="sidebar-footer">
          <button type="button" class="logout-btn" @click="handleLogout">
            <SvgIcon name="log-out" :size="16" />
            <span>Sair da conta</span>
          </button>
        </div>
      </aside>
    </div>
  </Transition>
</template>

<style scoped>
.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.52);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 3000;
  display: flex;
  justify-content: flex-start;
}

.sidebar-drawer {
  width: min(310px, 86vw);
  height: 100vh;
  height: 100dvh;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  box-shadow: 12px 0 36px rgba(0, 0, 0, 0.22);
  overflow: hidden;
}

.sidebar-header {
  background: linear-gradient(135deg, #f6b55d 0%, #f5a623 100%);
  padding: 18px 16px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  flex-shrink: 0;
}

.sidebar-drawer.merchant-mode .sidebar-header {
  background: linear-gradient(135deg, #8b85f0 0%, #1e1b6e 100%);
}

.brand-row {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.brand-logo {
  width: 38px;
  height: 38px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.92);
  color: #ff3b69;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.sidebar-drawer.merchant-mode .brand-logo {
  color: #1e1b6e;
}

.brand-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.brand-title {
  font-size: 18px;
  font-weight: 900;
  color: #ffffff;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.brand-title span {
  color: #ff3b69;
}

.sidebar-drawer.merchant-mode .brand-title span {
  color: #f6b55d;
}

.brand-badge {
  font-size: 10px;
  font-weight: 800;
  color: rgba(255, 255, 255, 0.92);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-top: 2px;
}

.close-btn {
  width: 34px;
  height: 34px;
  padding: 0;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.35);
  background: rgba(255, 255, 255, 0.22);
  color: #ffffff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  line-height: 0;
  cursor: pointer;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: #fdf6e9;
  border-bottom: 1px solid #f0dfb8;
  flex-shrink: 0;
}

.sidebar-drawer.merchant-mode .user-card {
  background: #f5f3ff;
  border-bottom-color: #e4dffc;
}

.user-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #ffffff;
  color: #ff3b69;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

.sidebar-drawer.merchant-mode .user-avatar {
  color: #1e1b6e;
}

.user-meta {
  min-width: 0;
  flex: 1;
}

.user-name {
  font-size: 13px;
  font-weight: 800;
  color: #1e293b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email {
  font-size: 11px;
  color: #64748b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-scroll {
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: 14px 12px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.switcher-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.section-caption {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #475569;
}

.role-pills {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}

.role-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 8px 6px;
  border-radius: 9px;
  border: 1px solid #cbd5e1;
  background: #ffffff;
  color: #334155;
  font-size: 11px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.15s ease;
}

.role-pill.active {
  background: #ff3b69;
  border-color: #ff3b69;
  color: #ffffff;
}

.sidebar-drawer.merchant-mode .role-pill.active {
  background: #1e1b6e;
  border-color: #1e1b6e;
  color: #ffffff;
}

.frame-toggle-btn {
  width: 100%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 7px 10px;
  border-radius: 9px;
  border: 1px dashed #f5a623;
  background: #fffbeb;
  color: #92400e;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
}

.nav-group {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.nav-group-title {
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #94a3b8;
  padding: 0 8px 4px;
}

.nav-link {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 10px;
  border-radius: 11px;
  border: none;
  background: transparent;
  color: #334155;
  font-size: 13px;
  font-weight: 700;
  text-align: left;
  cursor: pointer;
  transition: all 0.15s ease;
}

.nav-link:hover {
  background: #f1f5f9;
}

.nav-link.active {
  background: #fff0f4;
  color: #ff3b69;
}

.sidebar-drawer.merchant-mode .nav-link.active {
  background: #ede9fe;
  color: #1e1b6e;
}

.nav-link.subtle {
  padding: 8px 10px;
  font-size: 12px;
  color: #64748b;
}

.nav-link-icon {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: #f8fafc;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  line-height: 0;
}

.nav-link.active .nav-link-icon {
  background: rgba(255, 59, 105, 0.12);
}

.sidebar-drawer.merchant-mode .nav-link.active .nav-link-icon {
  background: rgba(30, 27, 110, 0.12);
}

.nav-link-label {
  flex: 1;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.nav-link-badge {
  background: #ff3b69;
  color: #ffffff;
  font-size: 10px;
  font-weight: 800;
  padding: 2px 7px;
  border-radius: 999px;
  flex-shrink: 0;
}

.sidebar-footer {
  padding: 12px 16px calc(env(safe-area-inset-bottom, 0px) + 12px);
  border-top: 1px solid #e2e8f0;
  background: #ffffff;
  flex-shrink: 0;
}

.logout-btn {
  width: 100%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #fecdd3;
  background: #fff1f2;
  color: #e11d48;
  font-size: 13px;
  font-weight: 800;
  cursor: pointer;
}

.sidebar-fade-enter-active,
.sidebar-fade-leave-active {
  transition: opacity 0.22s ease;
}

.sidebar-fade-enter-active .sidebar-drawer,
.sidebar-fade-leave-active .sidebar-drawer {
  transition: transform 0.24s cubic-bezier(0.16, 1, 0.3, 1);
}

.sidebar-fade-enter-from,
.sidebar-fade-leave-to {
  opacity: 0;
}

.sidebar-fade-enter-from .sidebar-drawer,
.sidebar-fade-leave-to .sidebar-drawer {
  transform: translateX(-100%);
}
</style>
