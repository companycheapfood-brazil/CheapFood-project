<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import BottomNav from "@/components/BottomNav.vue";
import SvgIcon from "@/components/ui/SvgIcon.vue";
import { useToastStore } from "@/stores/useToastStore";
import { API_URL, resolveImageUrl } from "@/config/api";
import { authHeaders, bumpSessionVersion, handleUnauthorized } from "@/utils/auth";
import { normalizeImageFile } from "@/utils/image";
import axios from "axios";

const router = useRouter();
const toast = useToastStore();

const name = ref("");
const email = ref("");
const phone = ref("");
const cpf = ref("");
const fotoUrl = ref("");
const avatarError = ref(false);
const selectedFile = ref<File | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);
const isSaving = ref(false);
const isProcessingImage = ref(false);
let activeBlobUrl: string | null = null;

function revokeActiveBlob() {
  if (activeBlobUrl) {
    URL.revokeObjectURL(activeBlobUrl);
    activeBlobUrl = null;
  }
}

onUnmounted(() => {
  revokeActiveBlob();
});

function populateFromUser(u: any) {
  if (!u) return;
  name.value = u.name || "";
  email.value = u.email || "";
  phone.value = u.telefone || "";
  cpf.value = u.cpf || "";
  avatarError.value = false;
  if (u.foto && !selectedFile.value) {
    fotoUrl.value = resolveImageUrl(u.foto);
  }
}

onMounted(async () => {
  const userData = localStorage.getItem("user");
  if (userData) {
    try {
      const parsed = JSON.parse(userData);
      populateFromUser(parsed?.user || parsed);
    } catch {
      // ignore corrupted storage
    }
  }

  try {
    const res = await fetch(`${API_URL}/auth/me`, { headers: authHeaders() });
    if (handleUnauthorized(res.status)) return;
    if (res.ok) {
      const data = await res.json().catch(() => null);
      if (data?.user) {
        populateFromUser(data.user);
      }
    }
  } catch {
    // mantém valores do cache local
  }
});

function triggerFileInput() {
  fileInput.value?.click();
}

async function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement;
  const rawFile = target.files?.[0];
  if (!rawFile) return;

  isProcessingImage.value = true;
  try {
    revokeActiveBlob();
    activeBlobUrl = URL.createObjectURL(rawFile);
    fotoUrl.value = activeBlobUrl;
    avatarError.value = false;
    selectedFile.value = await normalizeImageFile(rawFile);
  } catch {
    toast.addToast("Não foi possível processar esta imagem.", "error");
  } finally {
    isProcessingImage.value = false;
    target.value = "";
  }
}

async function saveProfile() {
  if (isSaving.value || isProcessingImage.value) return;
  if (!name.value.trim()) {
    toast.addToast("Informe seu nome completo.", "error");
    return;
  }

  isSaving.value = true;
  try {
    const formData = new FormData();
    formData.append("name", name.value.trim());
    formData.append("telefone", phone.value.trim());
    formData.append("cpf", cpf.value.trim());
    if (selectedFile.value) {
      formData.append("foto", selectedFile.value);
    }

    const res = await axios.put(`${API_URL}/profile`, formData, {
      headers: { ...authHeaders() },
    });

    if (res.data?.user) {
      try {
        const userData = localStorage.getItem("user");
        if (userData) {
          const parsed = JSON.parse(userData);
          parsed.user = res.data.user;
          localStorage.setItem("user", JSON.stringify(parsed));
        }
      } catch {}
      selectedFile.value = null;
      revokeActiveBlob();
      populateFromUser(res.data.user);
      bumpSessionVersion();
    }

    toast.addToast("Perfil atualizado com sucesso!", "success");
  } catch (error: any) {
    if (error?.response?.status && handleUnauthorized(error.response.status)) {
      return;
    }
    console.error("Erro ao salvar perfil:", error);
    toast.addToast(
      error?.response?.data?.message || "Erro ao atualizar perfil.",
      "error",
    );
  } finally {
    isSaving.value = false;
  }
}
</script>

<template>
  <div class="screen">
    <header class="edit-header">
      <button class="back-btn" type="button" @click="router.push('/perfil')" aria-label="Voltar">
        <SvgIcon name="arrow-left" :size="17" />
      </button>
      <h1 class="title">Editar perfil</h1>
      <span style="width: 34px"></span>
    </header>

    <main class="content">
      <div class="avatar-section">
        <div class="avatar-circle" @click="triggerFileInput" style="cursor: pointer; overflow: hidden; color: #8c5b16;">
          <img
            v-if="fotoUrl && !avatarError"
            :src="fotoUrl"
            alt="Foto de perfil"
            style="width: 100%; height: 100%; object-fit: cover;"
            @error="avatarError = true"
          />
          <SvgIcon v-else name="user" :size="32" />
        </div>
        <button
          type="button"
          class="change-photo-btn"
          :disabled="isProcessingImage"
          @click="triggerFileInput"
          style="display: inline-flex; align-items: center; gap: 5px;"
        >
          <SvgIcon name="camera" :size="14" />
          <span>{{ isProcessingImage ? "Processando foto..." : "Alterar foto" }}</span>
        </button>
        <input type="file" ref="fileInput" @change="handleFileChange" accept="image/*" style="display: none" />
      </div>

      <form class="edit-form" @submit.prevent="saveProfile">
        <div class="form-group">
          <label>Nome completo</label>
          <input type="text" v-model="name" maxlength="100" required />
        </div>
        <div class="form-group">
          <label>E-mail</label>
          <input type="email" v-model="email" disabled />
        </div>
        <div class="form-group">
          <label>Telefone</label>
          <input type="text" v-model="phone" maxlength="20" placeholder="(00) 00000-0000" />
        </div>
        <div class="form-group">
          <label>CPF</label>
          <input type="text" v-model="cpf" maxlength="20" placeholder="000.000.000-00" />
        </div>

        <button type="submit" class="save-btn" :disabled="isSaving || isProcessingImage">
          {{ isSaving ? "Salvando..." : isProcessingImage ? "Preparando imagem..." : "Salvar alterações" }}
        </button>
      </form>
    </main>

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

.edit-header {
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

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
}

.avatar-circle {
  width: 70px;
  height: 70px;
  background-color: #fdf6e9;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  font-size: 2rem;
}

.change-photo-btn {
  background: none;
  border: none;
  color: #f6b55d;
  font-weight: 700;
  font-size: 0.85rem;
  margin-top: 0.5rem;
  cursor: pointer;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
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
  font-weight: 500;
}

.form-group input:disabled {
  color: #aaa;
  background-color: #f9f9f9;
  border-color: #eee;
}

.save-btn {
  width: 100%;
  background-color: #f7b75e;
  color: #5c3809;
  padding: 1.2rem;
  border: none;
  border-radius: 20px;
  font-size: 1.1rem;
  font-weight: 800;
  margin-top: 1rem;
  cursor: pointer;
}
</style>
