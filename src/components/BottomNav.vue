<script setup lang="ts">
import { useRoute } from "vue-router";
import { useCartStore } from "@/stores/useCartStore";
import { useSidebarStore } from "@/stores/useSidebarStore";
import { storeToRefs } from "pinia";

const route = useRoute();
const cartStore = useCartStore();
const sidebarStore = useSidebarStore();
const { totalItems } = storeToRefs(cartStore);

const tabs = [
  {
    name: "home",
    label: "Início",
    svg: '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    to: "/",
  },
  {
    name: "buscar",
    label: "Buscar",
    svg: '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    to: "/buscar",
  },
  {
    name: "carrinho",
    label: "Carrinho",
    svg: '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg>',
    to: "/carrinho",
  },
  {
    name: "perfil",
    label: "Perfil",
    svg: '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    to: "/perfil",
  },
];
</script>

<template>
  <nav class="bottom-nav">
    <RouterLink
      v-for="tab in tabs"
      :key="tab.name"
      :to="tab.to"
      :aria-label="tab.label"
      class="nav-item"
      :class="{
        active:
          route.name === tab.name ||
          (tab.name === 'home' && route.name === 'produto') ||
          (tab.name === 'carrinho' && route.name === 'comprovante'),
      }"
    >
      <span class="nav-icon-wrap">
        <span class="nav-icon" v-html="tab.svg"></span>
        <span
          v-if="tab.name === 'carrinho' && totalItems > 0"
          class="nav-badge"
        >
          {{ totalItems }}
        </span>
      </span>
      <span class="nav-label">{{ tab.label }}</span>
    </RouterLink>

    <button
      type="button"
      class="nav-item menu-trigger"
      aria-label="Abrir Menu Lateral"
      @click="sidebarStore.open()"
    >
      <span class="nav-icon-wrap">
        <span class="nav-icon">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="22"
            height="22"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <line x1="4" y1="6" x2="20" y2="6" />
            <line x1="4" y1="12" x2="20" y2="12" />
            <line x1="4" y1="18" x2="15" y2="18" />
          </svg>
        </span>
      </span>
      <span class="nav-label">Menu</span>
    </button>
  </nav>
</template>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  width: 100%;
  max-width: 480px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-sizing: border-box;
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-top: 1px solid rgba(240, 223, 184, 0.85);
  box-shadow: 0 -4px 20px rgba(92, 56, 9, 0.08);
  padding: 5px 2px calc(env(safe-area-inset-bottom, 0px) + 5px);
  z-index: 1000;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  padding: 3px 1px;
  border-radius: 12px;
  color: #8a8a96;
  background: transparent;
  border: none;
  transition: all 0.2s ease;
  flex: 1 1 0;
  min-width: 0;
  max-width: 20%;
  box-sizing: border-box;
}

.nav-icon-wrap {
  position: relative;
  display: inline-flex;
  padding: 2px 6px;
  border-radius: 999px;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  opacity: 0.75;
  transition: opacity 0.2s ease;
}

.nav-badge {
  position: absolute;
  top: -4px;
  right: -2px;
  background: linear-gradient(135deg, #ff3b69 0%, #e02854 100%);
  color: #fff;
  font-size: 9px;
  font-weight: 800;
  line-height: 1;
  padding: 2px 4px;
  border-radius: 999px;
  min-width: 15px;
  text-align: center;
  box-shadow: 0 2px 6px rgba(255, 59, 105, 0.35);
}

.nav-label {
  font-size: 10px;
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: center;
  width: 100%;
  line-height: 1.15;
}

.nav-item.active {
  color: var(--cf-pink);
}

.nav-item.active .nav-icon-wrap {
  background: #fff0f4;
  transform: translateY(-1px);
}

.nav-item.active .nav-icon {
  opacity: 1;
}
</style>
