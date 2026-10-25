<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useMerchantStore } from "@/stores/useMerchantStore";
import { useSidebarStore } from "@/stores/useSidebarStore";
import SvgIcon from "@/components/ui/SvgIcon.vue";

const props = defineProps<{
  title: string;
  subtitle?: string;
  backTo?: string;
}>();

const router = useRouter();
const merchantStore = useMerchantStore();
const sidebarStore = useSidebarStore();

const planLabel = computed(() => {
  const plan = merchantStore.stats.plan || merchantStore.storeInfo.plan;
  if (plan === "annual") return "PRO Anual";
  if (plan === "monthly") return "PRO Mensal";
  return "Gratuito";
});

const isPro = computed(() => {
  const plan = merchantStore.stats.plan || merchantStore.storeInfo.plan;
  return plan === "monthly" || plan === "annual";
});

function handleBack() {
  if (props.backTo) {
    router.push(props.backTo);
  } else {
    router.back();
  }
}
</script>

<template>
  <header class="merchant-header">
    <div class="logo-row">
      <button
        type="button"
        class="menu-btn"
        aria-label="Abrir menu de navegação"
        title="Menu"
        @click="sidebarStore.open()"
      >
        <SvgIcon name="menu" :size="18" />
      </button>
      <button
        v-if="backTo"
        type="button"
        class="back-btn"
        aria-label="Voltar"
        @click="handleBack"
      >
        <SvgIcon name="arrow-left" :size="15" :strokeWidth="2.6" />
      </button>
      <svg
        class="cart-icon"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M7 18C5.9 18 5.01 18.9 5.01 20C5.01 21.1 5.9 22 7 22C8.1 22 9 21.1 9 20C9 18.9 8.1 18 7 18ZM1 2V4H3L6.6 11.59L5.24 14.04C5.09 14.32 5 14.65 5 15C5 16.1 5.9 17 7 17H19V15H7.42C7.28 15 7.17 14.89 7.17 14.75L7.2 14.63L8.1 13H15.55C16.3 13 16.96 12.59 17.3 11.97L20.88 5.48C20.95 5.34 21 5.17 21 5C21 4.45 20.55 4 20 4H5.21L4.27 2H1ZM17 18C15.9 18 15.01 18.9 15.01 20C15.01 21.1 15.9 22 17 22C18.1 22 19 21.1 19 20C19 18.9 18.1 18 17 18Z"
          fill="#ffffff"
        />
      </svg>
      <span class="logo-text"
        >Cheap<span class="logo-highlight">Food</span></span
      >
      <span class="badge">Lojista</span>
      <button
        type="button"
        class="plan-pill"
        :class="{ pro: isPro }"
        title="Gerenciar Plano da Loja"
        @click="router.push('/comerciante/planos')"
      >
        <SvgIcon v-if="isPro" name="star-filled" :size="11" />
        {{ planLabel }}
      </button>
      <span class="esg-header-badge" title="Selo Oficial de Combate ao Desperdício">
        <SvgIcon name="leaf" :size="10" />
        <span>ESG Ativo</span>
      </span>
    </div>
    <div class="header-titles">
      <h1 class="title">{{ title }}</h1>
      <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
    </div>
  </header>
</template>

<style scoped>
.merchant-header {
  background: linear-gradient(135deg, var(--mc-purple) 0%, #b8b3f7 100%);
  padding: 20px 16px 18px 16px;
  border-radius: 0 0 var(--cf-radius-lg) var(--cf-radius-lg);
  flex-shrink: 0;
}

.logo-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 7px;
  margin-bottom: 14px;
}

.menu-btn,
.back-btn {
  width: 34px;
  height: 34px;
  padding: 0;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.35);
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
  line-height: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  cursor: pointer;
  transition: background 0.2s;
}
.back-btn {
  border-radius: 50%;
  width: 30px;
  height: 30px;
}
.menu-btn:hover,
.back-btn:hover {
  background: rgba(255, 255, 255, 0.35);
}

.cart-icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
}

.logo-text {
  font-size: 17px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.3px;
  line-height: 1;
}

.logo-highlight {
  color: #f7b657;
}

.badge {
  background-color: rgba(255, 255, 255, 0.2);
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #ffffff;
  line-height: 1;
}

.plan-pill {
  margin-left: auto;
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.35);
  color: #ffffff;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 10px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  transition: transform 0.15s;
}
.plan-pill.pro {
  background: #f7b657;
  border-color: #f7b657;
  color: #1e1b6e;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
}
.plan-pill:hover {
  transform: scale(1.04);
}

.esg-header-badge {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.35);
  border-radius: 999px;
  padding: 3px 8px;
  font-size: 10px;
  font-weight: 800;
  white-space: nowrap;
}

.header-titles {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.title {
  font-size: 17px;
  font-weight: 800;
  color: #ffffff;
  margin: 0;
}

.subtitle {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.85);
  margin: 0;
}
</style>
