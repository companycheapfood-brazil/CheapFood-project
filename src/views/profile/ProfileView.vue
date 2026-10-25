<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import BottomNav from "@/components/BottomNav.vue";
import SvgIcon from "@/components/ui/SvgIcon.vue";
import AuthService from "@/services/auth.service";
import { useSidebarStore } from "@/stores/useSidebarStore";
import { API_URL, resolveImageUrl } from "@/config/api";
import { authHeaders } from "@/utils/auth";

const router = useRouter();
const sidebarStore = useSidebarStore();

const handleLogout = async () => {
  try {
    await AuthService.logout();
  } catch (e) {
    console.error("Logout error:", e);
  }
  router.push("/start");
};

const tabs = ["Economizados", "Reservas", "Comida salva"];
const activeTab = ref("Economizados");

const menuItems = [
  { icon: "heart-filled", iconColor: "#ff3b69", label: "Meus Favoritos", sub: "Produtos salvos que alimentam seu feed", to: "/perfil/favoritos" },
  { icon: "receipt", iconColor: "#d97706", label: "Histórico de pedidos", sub: "Acompanhe reservas, códigos e avalie lojas", to: "/perfil/historico" },
  { icon: "edit", iconColor: "#d97706", label: "Editar dados", sub: "Foto de perfil, nome, telefone e senha", to: "/perfil/editar" },
  { icon: "help-circle", iconColor: "#d97706", label: "Central de ajuda", sub: "Dúvidas frequentes e suporte", to: "/perfil/ajuda" },
  { icon: "file-text", iconColor: "#d97706", label: "Termos e privacidade", sub: "Regras de uso e LGPD", to: "/perfil/termos" },
  { icon: "trash", iconColor: "#e11d48", label: "Excluir conta", sub: "Encerramento permanente de dados", to: "/perfil/excluir" },
];

const user = ref({
  name: "João Silva",
  role: "Consumidor Consciente",
  fotoUrl: "",
});

const orders = ref<any[]>([]);

const totalSavedMoney = computed(() =>
  orders.value
    .filter((o) => o.status !== "expirado")
    .reduce((acc, o) => acc + Number(o.savings ?? 0), 0),
);

const totalReservations = computed(() => orders.value.length);
const pendingReservations = computed(
  () => orders.value.filter((o) => o.status === "pendente").length,
);

const totalItemsSaved = computed(() =>
  orders.value
    .filter((o) => o.status !== "expirado")
    .reduce((acc, o) => acc + Number(o.quantity ?? 1), 0),
);

const estimatedKgSaved = computed(() =>
  (totalItemsSaved.value * 0.42).toFixed(1).replace(".", ","),
);

const estimatedCo2Saved = computed(() =>
  (totalItemsSaved.value * 0.42 * 2.5).toFixed(1).replace(".", ","),
);

const ecoLevel = computed(() => {
  const items = totalItemsSaved.value;
  if (items >= 8) {
    return {
      title: "Herói do Planeta",
      badge: "Nível 3 (Mestre)",
      current: items,
      target: 15,
      progress: Math.min(100, Math.round((items / 15) * 100)),
      desc: "Você é uma referência no combate ao desperdício de alimentos!",
      icon: "flame",
    };
  } else if (items >= 3) {
    return {
      title: "Guardião Verde",
      badge: "Nível 2 (Intermediário)",
      current: items,
      target: 8,
      progress: Math.min(100, Math.round((items / 8) * 100)),
      desc: "Excelente impacto! Faltam poucos resgates para o nível máximo.",
      icon: "leaf",
    };
  } else {
    return {
      title: "Resgatador Consciente",
      badge: "Nível 1 (Iniciante)",
      current: items,
      target: 3,
      progress: Math.min(100, Math.round((items / 3) * 100)),
      desc: "Dê o próximo passo resgatando alimentos com super desconto.",
      icon: "sparkles",
    };
  }
});

const achievements = computed(() => [
  {
    id: 1,
    title: "Primeiro Resgate",
    desc: "1 produto salvo do lixo",
    unlocked: totalItemsSaved.value >= 1,
    icon: "shopping-bag",
  },
  {
    id: 2,
    title: "Amigo do Clima",
    desc: "Evitou emissão de CO₂",
    unlocked: totalItemsSaved.value >= 3,
    icon: "leaf",
  },
  {
    id: 3,
    title: "Super Economia",
    desc: "+R$ 40 economizados",
    unlocked: totalSavedMoney.value >= 40,
    icon: "wallet",
  },
]);

onMounted(async () => {
  const userData = localStorage.getItem("user");
  if (userData) {
    try {
      const parsed = JSON.parse(userData);
      const u = parsed.user || parsed;
      if (u) {
        user.value.name = u.name || "Consumidor";
        user.value.role = u.role === "merchant" ? "Comerciante" : "Consumidor Consciente";
        if (u.foto) {
          user.value.fotoUrl = resolveImageUrl(u.foto);
        }
      }
    } catch (e) {
      console.error(e);
    }
  }

  try {
    const res = await fetch(`${API_URL}/orders`, { headers: authHeaders() });
    if (res.ok) {
      orders.value = await res.json();
    }
  } catch (e) {
    console.error(e);
  }
});
</script>

<template>
  <div class="screen">
    <header class="profile-header">
      <div class="profile-header-top">
        <button
          class="header-menu-btn"
          aria-label="Abrir menu lateral"
          @click="sidebarStore.open()"
        >
          <SvgIcon name="menu" :size="19" />
        </button>
        <h1 class="title">Meu Perfil</h1>
        <div style="width: 36px;"></div>
      </div>
      <div class="avatar-block">
        <div
          class="avatar"
          style="
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #8c5b16;
          "
        >
          <img
            v-if="user.fotoUrl"
            :src="user.fotoUrl"
            style="width: 100%; height: 100%; object-fit: cover"
          />
          <SvgIcon v-else name="user" :size="34" />
        </div>
        <p class="user-name">{{ user.name }}</p>
        <span class="user-role-badge">
          <SvgIcon name="leaf" :size="13" />
          <span>{{ user.role }}</span>
        </span>
      </div>

      <div class="tabs">
        <button
          v-for="t in tabs"
          :key="t"
          class="tab"
          :class="{ active: activeTab === t }"
          @click="activeTab = t"
        >
          {{ t }}
        </button>
      </div>
    </header>

    <main class="content">
      <div class="impact-banner">
        <template v-if="activeTab === 'Economizados'">
          <span class="impact-icon" style="color: #d97706">
            <SvgIcon name="wallet" :size="24" />
          </span>
          <div class="impact-info">
            <span class="impact-label">Economia acumulada no CheapFood</span>
            <strong class="impact-value"
              >R$ {{ totalSavedMoney.toFixed(2).replace(".", ",") }}</strong
            >
            <span class="impact-sub"
              >Comprando produtos próximos ao vencimento com desconto</span
            >
          </div>
        </template>

        <template v-else-if="activeTab === 'Reservas'">
          <span class="impact-icon" style="color: #ff3b69">
            <SvgIcon name="shopping-bag" :size="24" />
          </span>
          <div class="impact-info">
            <span class="impact-label">Total de reservas realizadas</span>
            <strong class="impact-value">{{ totalReservations }} pedidos</strong>
            <span class="impact-sub"
              >{{ pendingReservations }} aguardando retirada no momento</span
            >
          </div>
        </template>

        <template v-else>
          <span class="impact-icon" style="color: #15803d">
            <SvgIcon name="leaf" :size="24" />
          </span>
          <div class="impact-info">
            <span class="impact-label">Impacto contra o desperdício</span>
            <strong class="impact-value"
              >~{{ estimatedKgSaved }} kg ({{ totalItemsSaved }} itens)</strong
            >
            <span class="impact-sub"
              >Alimentos perfeitos salvos de irem para o lixo</span
            >
          </div>
        </template>
      </div>

      <!-- Card Gamificação: EcoHero & Conquistas -->
      <div class="eco-hero-card">
        <div class="eco-header">
          <div class="eco-level-tag">
            <SvgIcon :name="ecoLevel.icon" :size="15" />
            <span>{{ ecoLevel.badge }}</span>
          </div>
          <span class="eco-co2-chip">
            <SvgIcon name="leaf" :size="13" />
            <span>~{{ estimatedCo2Saved }} kg CO₂ evitado</span>
          </span>
        </div>

        <h3 class="eco-hero-title">{{ ecoLevel.title }}</h3>
        <p class="eco-hero-desc">{{ ecoLevel.desc }}</p>

        <!-- Barra de Progresso de Nível -->
        <div class="eco-progress-box">
          <div class="eco-progress-labels">
            <span>Progresso da Jornada</span>
            <strong>{{ ecoLevel.current }} / {{ ecoLevel.target }} itens ({{ ecoLevel.progress }}%)</strong>
          </div>
          <div class="eco-progress-bar">
            <div class="eco-progress-fill" :style="{ width: `${ecoLevel.progress}%` }"></div>
          </div>
        </div>

        <!-- Badges / Conquistas Desbloqueáveis -->
        <div class="achievements-grid">
          <div
            v-for="ach in achievements"
            :key="ach.id"
            class="achievement-item"
            :class="{ unlocked: ach.unlocked }"
          >
            <div class="ach-icon-wrapper">
              <SvgIcon :name="ach.icon" :size="16" />
            </div>
            <div class="ach-info">
              <span class="ach-title">{{ ach.title }}</span>
              <span class="ach-desc">{{ ach.desc }}</span>
            </div>
            <span v-if="ach.unlocked" class="ach-check">
              <SvgIcon name="check-circle" :size="14" />
            </span>
          </div>
        </div>
      </div>

      <div class="menu-list">
        <RouterLink
          v-for="item in menuItems"
          :key="item.label"
          :to="item.to"
          class="menu-row"
        >
          <div class="menu-left">
            <span class="menu-icon" :style="{ color: item.iconColor }">
              <SvgIcon :name="item.icon" :size="19" />
            </span>
            <div class="menu-texts">
              <span class="menu-title">{{ item.label }}</span>
              <span class="menu-sub">{{ item.sub }}</span>
            </div>
          </div>
          <span class="menu-arrow">
            <SvgIcon name="chevron-right" :size="18" />
          </span>
        </RouterLink>
        <button class="menu-row danger" @click="handleLogout">
          <div class="menu-left">
            <span class="menu-icon danger-icon" style="color: #ff3b69">
              <SvgIcon name="log-out" :size="19" />
            </span>
            <div class="menu-texts">
              <span class="menu-title">Sair da conta</span>
              <span class="menu-sub">Encerrar sessão neste dispositivo</span>
            </div>
          </div>
          <span class="menu-arrow">
            <SvgIcon name="chevron-right" :size="18" />
          </span>
        </button>
      </div>
    </main>

    <BottomNav />
  </div>
</template>

<style scoped>
.screen {
  background-color: #fbfaf8;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.profile-header {
  background: linear-gradient(135deg, #f6b55d 0%, #f5a623 100%);
  padding: 1.5rem 1.5rem 0 1.5rem;
  text-align: center;
  border-bottom-left-radius: 26px;
  border-bottom-right-radius: 26px;
  box-shadow: 0 8px 24px rgba(245, 166, 35, 0.22);
}

.profile-header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.9rem;
}

.header-menu-btn {
  width: 36px;
  height: 36px;
  padding: 0;
  line-height: 0;
  border-radius: 10px;
  border: none;
  background: rgba(255, 255, 255, 0.9);
  color: #2b1d0e;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(92, 56, 9, 0.08);
}

.title {
  font-size: 1.2rem;
  font-weight: 800;
  color: #1f160a;
  margin: 0;
}

.avatar-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1.1rem;
}

.avatar {
  width: 78px;
  height: 78px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.85);
  border: 3px solid #ffffff;
  margin-bottom: 0.65rem;
  box-shadow: 0 6px 18px rgba(92, 56, 9, 0.16);
}

.user-name {
  font-size: 1.32rem;
  font-weight: 900;
  color: #1f160a;
  margin: 0 0 0.3rem 0;
}

.user-role-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.78rem;
  font-weight: 800;
  color: #5c3809;
  background: rgba(255, 255, 255, 0.55);
  padding: 4px 12px;
  border-radius: 999px;
}

.tabs {
  display: flex;
  justify-content: space-around;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  padding-top: 0.25rem;
}

.tab {
  flex: 1;
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  color: #5c3809;
  font-size: 0.84rem;
  font-weight: 800;
  padding: 0.85rem 0;
  cursor: pointer;
  transition: all 0.2s;
}

.tab.active {
  color: #1f160a;
  border-bottom-color: #ff3b69;
  background: rgba(255, 255, 255, 0.28);
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.content {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 92px;
}

.impact-banner {
  margin: 1.2rem 1.25rem 0.9rem 1.25rem;
  padding: 1.15rem 1.2rem;
  background: linear-gradient(135deg, #fffdf8 0%, #fdf6e9 100%);
  border: 1px solid #f0dfb8;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: 0 6px 18px rgba(160, 132, 90, 0.12);
}

.impact-icon {
  font-size: 1.9rem;
  background: #ffffff;
  width: 54px;
  height: 54px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 1px solid #f0dfb8;
  box-shadow: 0 3px 8px rgba(160, 132, 90, 0.1);
}

.impact-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.impact-label {
  font-size: 0.72rem;
  font-weight: 800;
  color: #a0845a;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.impact-value {
  font-size: 1.38rem;
  font-weight: 900;
  color: #ff3b69;
}

.impact-sub {
  font-size: 0.78rem;
  color: #6b5a3e;
  font-weight: 600;
}

.menu-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 0 1.25rem;
}

.menu-row {
  width: 100%;
  padding: 0.95rem 1.1rem;
  background: #ffffff;
  border: 1px solid #f0dfb8;
  border-radius: 16px;
  text-align: left;
  color: #2b2111;
  text-decoration: none;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 3px 10px rgba(92, 56, 9, 0.04);
  transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
}

.menu-row:hover {
  transform: translateY(-1px);
  border-color: #e6c687;
  box-shadow: 0 6px 14px rgba(92, 56, 9, 0.08);
}

.menu-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.menu-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: #fdf6e9;
  border: 1px solid #f0dfb8;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.15rem;
  flex-shrink: 0;
}

.danger-icon {
  background: #fff0f4;
  border-color: #ffd0dc;
}

.menu-texts {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.menu-title {
  font-size: 0.94rem;
  font-weight: 800;
  color: #2b2111;
}

.menu-sub {
  font-size: 0.74rem;
  color: #8c7148;
  font-weight: 600;
}

.menu-arrow {
  color: #c5a97c;
  font-size: 1.35rem;
  font-weight: 700;
}

.menu-row.danger {
  border-color: #ffd0dc;
}

.menu-row.danger .menu-title {
  color: #ff3b69;
}

/* EcoHero Gamification Card */
.eco-hero-card {
  margin-top: 1.2rem;
  background: #ffffff;
  border-radius: 20px;
  padding: 1.25rem;
  border: 1px solid #e8dfd3;
  box-shadow: 0 4px 14px rgba(60, 40, 10, 0.05);
}

.eco-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.6rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.eco-level-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #f0fdf4;
  color: #15803d;
  font-size: 0.76rem;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid #bbf7d0;
}

.eco-co2-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: #ecfdf5;
  color: #047857;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 999px;
}

.eco-hero-title {
  font-size: 1.15rem;
  font-weight: 900;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.eco-hero-desc {
  font-size: 0.8rem;
  color: #6b7280;
  line-height: 1.35;
  margin-bottom: 1rem;
}

.eco-progress-box {
  background: #f9fafb;
  border-radius: 12px;
  padding: 0.75rem;
  margin-bottom: 1rem;
  border: 1px solid #f3f4f6;
}

.eco-progress-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.73rem;
  color: #4b5563;
  margin-bottom: 0.4rem;
}

.eco-progress-labels strong {
  color: #15803d;
}

.eco-progress-bar {
  width: 100%;
  height: 8px;
  background: #e5e7eb;
  border-radius: 999px;
  overflow: hidden;
}

.eco-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
  border-radius: 999px;
  transition: width 0.4s ease;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 0.6rem;
}

.achievement-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #fafaf9;
  border: 1px dashed #d6d3d1;
  border-radius: 12px;
  padding: 0.6rem;
  opacity: 0.6;
  position: relative;
  transition: all 0.2s ease;
}

.achievement-item.unlocked {
  opacity: 1;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
}

.ach-icon-wrapper {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  flex-shrink: 0;
}

.achievement-item.unlocked .ach-icon-wrapper {
  color: #15803d;
  background: #dcfce7;
}

.ach-info {
  display: flex;
  flex-direction: column;
}

.ach-title {
  font-size: 0.72rem;
  font-weight: 800;
  color: #1f2937;
}

.ach-desc {
  font-size: 0.62rem;
  color: #6b7280;
}

.ach-check {
  margin-left: auto;
  color: #16a34a;
}
</style>
