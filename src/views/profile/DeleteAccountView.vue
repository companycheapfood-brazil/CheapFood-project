<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import BottomNav from "@/components/BottomNav.vue";
import SvgIcon from "@/components/ui/SvgIcon.vue";
import AuthService from "@/services/auth.service";
import { API_URL } from "@/config/api";
import { authHeaders, handleUnauthorized } from "@/utils/auth";
import { useToastStore } from "@/stores/useToastStore";
import { useCartStore } from "@/stores/useCartStore";
import { useFavoritesStore } from "@/stores/useFavoritesStore";
import { useMerchantStore } from "@/stores/useMerchantStore";

const router = useRouter();
const toast = useToastStore();
const cartStore = useCartStore();
const favoritesStore = useFavoritesStore();
const merchantStore = useMerchantStore();
const password = ref("");
const isDeleting = ref(false);
const showConfirmModal = ref(false);

const requestDelete = () => {
  if (!password.value) {
    toast.addToast("Por favor, digite sua senha.", "error");
    return;
  }
  showConfirmModal.value = true;
};

const confirmDeleteAccount = async () => {
  if (isDeleting.value) return;
  isDeleting.value = true;
  try {
    const res = await fetch(`${API_URL}/profile`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        ...authHeaders(),
      },
      body: JSON.stringify({ password: password.value }),
    });

    if (handleUnauthorized(res.status)) return;
    const data = await res.json().catch(() => ({}));
    if (res.ok) {
      showConfirmModal.value = false;
      cartStore.resetSession();
      favoritesStore.resetState();
      merchantStore.resetState();
      toast.addToast("Conta excluída com sucesso.", "success");
      await AuthService.logout();
      router.push("/start");
    } else {
      showConfirmModal.value = false;
      toast.addToast(data.message || "Erro ao excluir conta", "error");
    }
  } catch {
    showConfirmModal.value = false;
    toast.addToast("Erro de conexão ao excluir conta", "error");
  } finally {
    isDeleting.value = false;
  }
};
</script>

<template>
  <div class="screen">
    <header class="delete-header">
      <button type="button" class="back-btn" @click="router.push('/perfil')" aria-label="Voltar">
        <SvgIcon name="arrow-left" :size="17" />
      </button>
      <h1 class="title">Excluir conta</h1>
      <span style="width: 34px"></span>
    </header>

    <main class="content">
      <div class="warning-section">
        <div class="warning-icon" style="color: #ff3b69">
          <SvgIcon name="alert-triangle" :size="30" />
        </div>
        <h2 class="warning-title">Tem certeza?</h2>
        <p class="warning-desc">
          Esta ação é permanente e não pode ser desfeita. Você perderá todo o
          histórico de pedidos e reservas.
        </p>
      </div>

      <div class="info-card">
        <h3 class="info-title">O que será excluído:</h3>
        <ul class="info-list">
          <li><span class="cross"><SvgIcon name="x" :size="14" /></span> Perfil e dados pessoais</li>
          <li><span class="cross"><SvgIcon name="x" :size="14" /></span> Histórico de pedidos</li>
          <li><span class="cross"><SvgIcon name="x" :size="14" /></span> Favoritos e avaliações</li>
        </ul>
      </div>

      <form @submit.prevent="requestDelete">
        <div class="form-group">
          <label>Digite sua senha para confirmar</label>
          <input type="password" v-model="password" placeholder="••••••••" required />
        </div>

        <div class="actions">
          <button type="submit" class="btn-delete" :disabled="isDeleting">
            {{ isDeleting ? "Excluindo..." : "Excluir minha conta" }}
          </button>
          <button type="button" class="btn-cancel" @click="router.push('/perfil')">Cancelar</button>
        </div>
      </form>
    </main>

    <div
      v-if="showConfirmModal"
      class="confirm-overlay"
      @click.self="!isDeleting && (showConfirmModal = false)"
    >
      <div class="confirm-card">
        <h3 class="confirm-title">Confirmar exclusão permanente</h3>
        <p class="confirm-desc">
          Todos os seus dados serão removidos imediatamente. Deseja prosseguir?
        </p>
        <div class="confirm-actions">
          <button
            type="button"
            class="btn-cancel"
            style="padding: 0.85rem"
            :disabled="isDeleting"
            @click="showConfirmModal = false"
          >
            Voltar
          </button>
          <button
            type="button"
            class="btn-delete"
            style="padding: 0.85rem"
            :disabled="isDeleting"
            @click="confirmDeleteAccount"
          >
            {{ isDeleting ? "Excluindo..." : "Sim, excluir" }}
          </button>
        </div>
      </div>
    </div>

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

.delete-header {
  background-color: #f6b55d;
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.back-btn {
  width: 34px;
  height: 34px;
  padding: 0;
  line-height: 0;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.88);
  color: #333;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.title {
  font-size: 1.2rem;
  font-weight: 800;
  color: #333;
  margin: 0;
}

.content {
  padding: 1.5rem;
  flex: 1;
  overflow-y: auto;
  padding-bottom: 100px;
}

.warning-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-top: 1rem;
  margin-bottom: 2rem;
}

.warning-icon {
  width: 70px;
  height: 70px;
  background-color: #fff0f3;
  border-radius: 50%;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

.warning-title {
  font-size: 1.2rem;
  font-weight: 800;
  color: #333;
  margin: 0 0 0.5rem 0;
}

.warning-desc {
  font-size: 0.85rem;
  color: #a0a0a0;
  line-height: 1.5;
  margin: 0;
}

.info-card {
  border: 1px solid #f0dfb8;
  border-radius: 12px;
  padding: 1.2rem;
  margin-bottom: 2rem;
}

.info-title {
  font-size: 0.85rem;
  font-weight: 800;
  color: #ff3b69;
  margin: 0 0 1rem 0;
}

.info-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.info-list li {
  font-size: 0.85rem;
  color: #555;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cross {
  color: #ff3b69;
  font-weight: bold;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.form-group label {
  font-size: 0.8rem;
  font-weight: 700;
  color: #888;
}

.form-group input {
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid #f0dfb8;
  background-color: #fdf6e9;
  font-size: 0.95rem;
  color: #333;
  letter-spacing: 2px;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn-delete {
  width: 100%;
  background-color: #e6103e;
  color: white;
  padding: 1.2rem;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 800;
  cursor: pointer;
}

.btn-cancel {
  width: 100%;
  background-color: transparent;
  color: #f6b55d;
  padding: 1.2rem;
  border: 1px solid #f6b55d;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 800;
  cursor: pointer;
}

.confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 16px;
}

.confirm-card {
  width: 100%;
  max-width: 340px;
  background: #ffffff;
  border-radius: 18px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 14px 36px rgba(0, 0, 0, 0.2);
}

.confirm-title {
  margin: 0 0 8px 0;
  font-size: 1.05rem;
  font-weight: 800;
  color: #1f2937;
}

.confirm-desc {
  margin: 0 0 18px 0;
  font-size: 0.85rem;
  color: #6b7280;
  line-height: 1.4;
}

.confirm-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
</style>
