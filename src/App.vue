<script setup lang="ts">
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { storeToRefs } from "pinia";
import ToastContainer from "@/components/ui/ToastContainer.vue";
import MobileSidebar from "@/components/MobileSidebar.vue";
import SvgIcon from "@/components/ui/SvgIcon.vue";
import AuthService from "@/services/auth.service";
import { useToastStore } from "@/stores/useToastStore";
import { useSidebarStore } from "@/stores/useSidebarStore";
import { useCartStore } from "@/stores/useCartStore";

const router = useRouter();
const route = useRoute();
const toast = useToastStore();
const sidebarStore = useSidebarStore();
const cartStore = useCartStore();

const { mobileFrame } = storeToRefs(sidebarStore);
const demoBarOpen = ref(false);
const isSwitching = ref(false);

async function switchProfile(role: "consumer" | "merchant") {
  isSwitching.value = true;
  try {
    await AuthService.login({
      email: role === "merchant" ? "admin@cheapfood.com" : "joao@email.com",
      password: role === "merchant" ? "admin123" : "123456",
    });
    cartStore.clearCart();
    toast.addToast(
      role === "merchant"
        ? "Alternado para Painel do Lojista!"
        : "Alternado para Visão do Consumidor!",
      "success",
    );
    demoBarOpen.value = false;
    router.push(role === "merchant" ? "/comerciante" : "/");
  } catch (e) {
    toast.addToast("Erro ao alternar perfil de demonstração", "error");
  } finally {
    isSwitching.value = false;
  }
}
</script>

<template>
  <div class="app-outer" :class="{ 'mobile-frame-active': mobileFrame }">
    <div class="app-shell">
      <ToastContainer />
      <MobileSidebar />
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>

    <!-- Barra Flutuante de Modo Apresentação -->
    <div class="tcc-demo-widget">
      <button
        class="tcc-fab"
        @click="demoBarOpen = !demoBarOpen"
        title="Modo Apresentação"
      >
        <SvgIcon :name="demoBarOpen ? 'x' : 'sparkles'" :size="13" />
        <span v-if="!demoBarOpen">Apresentação</span>
      </button>

      <div v-if="demoBarOpen" class="tcc-panel">
        <p class="tcc-panel-title">Modo Apresentação</p>
        <button
          class="tcc-action-btn"
          :class="{ active: !route.path.startsWith('/comerciante') }"
          :disabled="isSwitching"
          @click="switchProfile('consumer')"
        >
          <SvgIcon name="shopping-cart" :size="14" />
          <span>Visão Consumidor (João)</span>
        </button>
        <button
          class="tcc-action-btn"
          :class="{ active: route.path.startsWith('/comerciante') }"
          :disabled="isSwitching"
          @click="switchProfile('merchant')"
        >
          <SvgIcon name="store" :size="14" />
          <span>Visão Lojista (Padaria)</span>
        </button>
        <button
          class="tcc-action-btn outline"
          @click="sidebarStore.toggleMobileFrame()"
        >
          <SvgIcon name="smartphone" :size="14" />
          <span>{{ mobileFrame ? "Expandir Tela Cheia" : "Moldura Mobile" }}</span>
        </button>
        <button
          class="tcc-action-btn"
          @click="
            demoBarOpen = false;
            sidebarStore.open();
          "
        >
          <SvgIcon name="menu" :size="14" />
          <span>Abrir Menu Lateral (Sidebar)</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style>
.app-outer {
  min-height: 100vh;
  background: var(--cf-bg);
}

.app-outer.mobile-frame-active {
  background: #1e293b;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 20px 0;
}

.app-outer.mobile-frame-active .app-shell {
  width: 100%;
  max-width: 430px;
  min-height: calc(100vh - 40px);
  border-radius: 28px;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.45);
  border: 6px solid #334155;
  overflow-x: hidden;
  position: relative;
}

.app-outer.mobile-frame-active .bottom-nav {
  max-width: 418px;
  left: 50%;
  right: auto;
  width: 100%;
  transform: translateX(-50%);
  border-bottom-left-radius: 22px;
  border-bottom-right-radius: 22px;
}

.app-shell {
  min-height: 100vh;
  background: var(--cf-bg);
  overflow-x: hidden;
}

.page-enter-active,
.page-leave-active {
  transition:
    opacity 0.25s ease,
    transform 0.25s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateX(10px);
}

.page-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

/* Widget Flutuante TCC */
.tcc-demo-widget {
  position: fixed;
  bottom: 84px;
  right: 14px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.tcc-fab {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  background: rgba(27, 59, 95, 0.92);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 999px;
  padding: 7px 13px;
  font-size: 11px;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(6px);
  transition: transform 0.15s ease;
}

.tcc-fab:hover {
  transform: scale(1.05);
}

.tcc-panel {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 12px;
  width: 230px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.22);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.tcc-panel-title {
  font-size: 10px;
  font-weight: 800;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 4px;
}

.tcc-action-btn {
  width: 100%;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  text-align: left;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #1e293b;
  border-radius: 10px;
  padding: 9px 11px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
}

.tcc-action-btn:hover {
  background: #f1f5f9;
}

.tcc-action-btn.active {
  background: #1b3b5f;
  border-color: #1b3b5f;
  color: #fff;
}

.tcc-action-btn.outline {
  background: #fff8e6;
  border-color: #f5a623;
  color: #8a5300;
}

@media print {
  .tcc-demo-widget {
    display: none !important;
  }
}
</style>
