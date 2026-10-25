<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import MerchantHeader from "@/components/merchant/MerchantHeader.vue";
import MerchantBottomNav from "@/components/merchant/MerchantBottomNav.vue";
import { useToastStore } from "@/stores/useToastStore";
import { useMerchantStore } from "@/stores/useMerchantStore";
import { API_URL, isImageUrl, resolveImageUrl } from "@/config/api";
import { authHeaders } from "@/utils/auth";

const router = useRouter();
const route = useRoute();
const toast = useToastStore();
const merchantStore = useMerchantStore();

const productId = route.params.id;

const form = ref({
  nome: "",
  descricao: "",
  categoria: "Padaria",
  preco_original: 0,
  preco_desconto: 0,
  quantidade: 0,
  data_validade: "",
});

const file = ref<File | null>(null);
const previewUrl = ref<string | null>(null);
const isLoading = ref(false);

const discountPercent = computed(() => {
  if (!form.value.preco_original || !form.value.preco_desconto || form.value.preco_original <= 0)
    return 0;
  const pct =
    ((form.value.preco_original - form.value.preco_desconto) / form.value.preco_original) * 100;
  return Math.max(0, Math.round(pct));
});

onMounted(async () => {
  try {
    const res = await fetch(`${API_URL}/products/${productId}`);
    if (res.ok) {
      const data = await res.json();
      form.value = {
        nome: data.name,
        descricao: data.description || "",
        categoria: data.category || "Padaria",
        preco_original: data.originalPrice,
        preco_desconto: data.price,
        quantidade: data.quantity,
        data_validade: data.validity,
      };
      const img = data.image || data.imagem || data.icon;
      if (isImageUrl(img)) {
        previewUrl.value = resolveImageUrl(img);
      }
    }
  } catch (e) {
    toast.addToast("Erro ao carregar produto", "error");
  }
});

function handleFile(e: Event) {
  const target = e.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    file.value = target.files[0];
    previewUrl.value = URL.createObjectURL(file.value);
  }
}

async function saveProduct() {
  isLoading.value = true;
  try {
    const formData = new FormData();
    formData.append("nome", form.value.nome);
    formData.append("descricao", form.value.descricao);
    formData.append("categoria", form.value.categoria);
    formData.append("preco_original", String(form.value.preco_original));
    formData.append("preco_desconto", String(form.value.preco_desconto));
    formData.append("quantidade", String(form.value.quantidade));
    formData.append("data_validade", form.value.data_validade);

    if (file.value) {
      formData.append("imagem", file.value);
    }

    const res = await fetch(`${API_URL}/products/${productId}`, {
      method: "PUT",
      headers: {
        ...authHeaders(),
      },
      body: formData,
    });

    if (res.ok) {
      await merchantStore.fetchProducts();
      toast.addToast("Produto atualizado com sucesso!", "success");
      router.push("/comerciante/produtos");
    } else {
      toast.addToast("Erro ao atualizar produto", "error");
    }
  } catch (e) {
    console.error(e);
    toast.addToast("Erro de conexão", "error");
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <div class="screen">
    <MerchantHeader
      title="Editar produto"
      subtitle="Atualize preço, estoque ou validade"
      backTo="/comerciante/produtos"
    />

    <main class="content">
      <form class="form" @submit.prevent="saveProduct">
        <div class="form-section">
          <h3 class="section-title">Informações Básicas</h3>
          <label class="field">
            <span class="field-label">Nome do produto</span>
            <input
              v-model="form.nome"
              type="text"
              placeholder="Ex: Leite Integral 1L"
              required
            />
          </label>

          <div class="row">
            <label class="field half">
              <span class="field-label">Categoria</span>
              <select v-model="form.categoria">
                <option value="" disabled>Selecione</option>
                <option
                  v-for="c in [
                    'Laticínios',
                    'Padaria',
                    'Hortifruti',
                    'Bebidas',
                    'Carnes',
                    'Frios',
                    'Congelados',
                    'Outros',
                  ]"
                  :key="c"
                  :value="c"
                >
                  {{ c }}
                </option>
              </select>
            </label>
            <label class="field half">
              <span class="field-label">Data de validade</span>
              <input v-model="form.data_validade" type="date" required />
            </label>
          </div>
          
          <label class="field">
            <span class="field-label">Descrição (Opcional)</span>
            <textarea
              v-model="form.descricao"
              placeholder="Ex: Produto fresco..."
              rows="2"
            ></textarea>
          </label>
        </div>

        <div class="form-section">
          <h3 class="section-title">Imagem do Produto</h3>
          <div v-if="previewUrl" class="preview-box">
            <img :src="previewUrl" alt="Preview do produto" class="preview-img" />
          </div>
          <label class="field">
            <input type="file" @change="handleFile" accept="image/*" />
          </label>
        </div>

        <div class="form-section">
          <h3 class="section-title">Precificação e Estoque</h3>
          <div class="row">
            <label class="field half">
              <span class="field-label">Original (R$)</span>
              <input
                v-model.number="form.preco_original"
                type="number"
                min="0"
                step="0.01"
                placeholder="4,99"
                required
              />
            </label>

            <label class="field half">
              <span class="field-label">Promocional (R$)</span>
              <input
                v-model.number="form.preco_desconto"
                type="number"
                min="0"
                step="0.01"
                placeholder="2,49"
                required
              />
            </label>
          </div>

          <label class="field">
            <span class="field-label">Quantidade disponível</span>
            <input
              v-model.number="form.quantidade"
              type="number"
              min="0"
              step="1"
              placeholder="10"
              required
            />
          </label>

          <div class="discount-card">
            <span>Desconto aplicado</span>
            <span class="discount-value">{{ discountPercent }}% OFF</span>
          </div>
        </div>

        <button type="submit" class="publish-btn" :disabled="isLoading">
          {{ isLoading ? "Salvando..." : "Salvar alterações" }}
        </button>
      </form>
    </main>

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

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-section {
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: var(--cf-radius-md);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.section-title {
  font-size: 14px;
  font-weight: 800;
  color: var(--mc-navy);
  margin-bottom: 4px;
}

.preview-box {
  width: 100%;
  height: 220px;
  border-radius: var(--cf-radius-sm);
  overflow: hidden;
  border: 1px solid var(--mc-border);
  background: #ffffff;
  padding: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-img {
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  border-radius: 8px;
}

.row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.field.half {
  flex: 1 1 140px;
  min-width: 0;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.field-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--mc-text-muted);
}

.field input,
.field select,
.field textarea {
  background: var(--cf-bg);
  border: 1px solid var(--mc-border);
  border-radius: var(--cf-radius-sm);
  padding: 12px 14px;
  font-size: 13px;
  color: var(--mc-text);
  outline: none;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.2s;
}

.field input:focus,
.field select:focus,
.field textarea:focus {
  border-color: var(--mc-purple);
}

.field input::placeholder,
.field textarea::placeholder {
  color: #bbb;
}

.discount-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--cf-bg);
  border: 1px dashed var(--cf-orange-soft);
  border-radius: var(--cf-radius-sm);
  padding: 12px 14px;
  font-size: 12px;
  font-weight: 600;
  color: var(--mc-text);
}

.discount-value {
  color: var(--cf-orange);
  font-size: 14px;
  font-weight: 800;
}

.publish-btn {
  background: var(--mc-navy);
  color: #ffffff;
  border: none;
  border-radius: var(--cf-radius-md);
  padding: 16px;
  font-size: 15px;
  font-weight: 800;
  margin-top: 10px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(10, 37, 64, 0.2);
}

.publish-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}
</style>
