<script setup lang="ts">
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import MerchantHeader from "@/components/merchant/MerchantHeader.vue";
import MerchantBottomNav from "@/components/merchant/MerchantBottomNav.vue";
import SvgIcon from "@/components/ui/SvgIcon.vue";
import { useMerchantStore } from "@/stores/useMerchantStore";
import { useToastStore } from "@/stores/useToastStore";
import { authHeaders, handleUnauthorized } from "@/utils/auth";
import { normalizeImageFile } from "@/utils/image";
import { API_URL } from "@/config/api";
import type { MerchantProduct } from "@/types";

const router = useRouter();
const merchantStore = useMerchantStore();
const toastStore = useToastStore();
const { addProduct } = merchantStore;

const categories = [
  "Laticínios",
  "Padaria",
  "Hortifruti",
  "Bebidas",
  "Carnes",
  "Frios",
  "Congelados",
  "Outros",
];

const name = ref("");
const category = ref("");
const description = ref("");
const validity = ref("");
const originalPrice = ref<number | null>(null);
const promoPrice = ref<number | null>(null);
const quantity = ref<number | null>(null);

const isAuction = ref(false);
const auctionStartPrice = ref<number | null>(null);
const auctionDurationValue = ref<number>(1);
const auctionDurationUnit = ref<string>("hours");

const imageFile = ref<File | null>(null);
const previewUrl = ref<string | null>(null);
const isAnalyzing = ref(false);

async function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    const rawFile = target.files[0];
    if (rawFile) {
      previewUrl.value = URL.createObjectURL(rawFile);
      const normalized = await normalizeImageFile(rawFile);
      imageFile.value = normalized;
    }
  }
}

async function analyzeImage() {
  if (!imageFile.value) {
    toastStore.addToast("Selecione uma imagem primeiro", "error");
    return;
  }

  isAnalyzing.value = true;
  try {
    const preparedFile = await normalizeImageFile(imageFile.value);
    imageFile.value = preparedFile;

    const formData = new FormData();
    formData.append("image", preparedFile);

    const res = await fetch(
      `${API_URL}/merchant/analyze-image`,
      {
        method: "POST",
        headers: authHeaders(),
        body: formData,
      },
    );

    if (handleUnauthorized(res.status)) return;

    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.message || "Falha ao analisar a imagem");

    // Autopreenchimento inteligente completo (sempre sobrescreve ao analisar nova imagem)
    if (data.nome) name.value = data.nome;
    if (data.categoria && categories.includes(data.categoria)) {
      category.value = data.categoria;
    } else if (data.categoria) {
      category.value = "Outros";
    }
    if (data.data_validade) validity.value = data.data_validade;
    if (data.descricao) description.value = data.descricao;
    if (data.preco_original !== undefined && data.preco_original !== null)
      originalPrice.value = Number(data.preco_original);
    if (data.preco_desconto !== undefined && data.preco_desconto !== null)
      promoPrice.value = Number(data.preco_desconto);
    if (!quantity.value) quantity.value = 10;

    if (data.aiProvider === "fallback") {
      toastStore.addToast(
        "Sugestão padrão aplicada (configure GEMINI_API_KEY no Render para reconhecimento visual completo).",
        "info",
      );
    } else {
      toastStore.addToast("Campos preenchidos pela Inteligência Artificial!", "success");
    }
  } catch (error) {
    console.error(error);
    toastStore.addToast(
      error instanceof Error ? error.message : "Erro ao analisar imagem",
      "error",
    );
  } finally {
    isAnalyzing.value = false;
  }
}

const discountPercent = computed(() => {
  if (!originalPrice.value || !promoPrice.value || originalPrice.value <= 0)
    return 0;
  const pct =
    ((originalPrice.value - promoPrice.value) / originalPrice.value) * 100;
  return Math.max(0, Math.round(pct));
});

const canPublish = computed(
  () =>
    name.value.trim() !== "" &&
    category.value !== "" &&
    validity.value !== "" &&
    !!originalPrice.value &&
    !!promoPrice.value &&
    !!quantity.value &&
    (!isAuction.value || (!!auctionStartPrice.value && auctionDurationValue.value > 0)),
);

async function publish() {
  if (!canPublish.value) return;

  const formData = new FormData();
  formData.append("nome", name.value.trim());
  formData.append("categoria", category.value);
  formData.append("descricao", description.value);
  formData.append("data_validade", validity.value);
  formData.append("preco_original", originalPrice.value!.toString());
  formData.append("preco_desconto", promoPrice.value!.toString());
  formData.append("quantidade", quantity.value!.toString());

  if (imageFile.value) {
    formData.append("imagem", imageFile.value);
  }

  if (isAuction.value) {
    formData.append("modo", "LEILAO");
    formData.append("preco_inicial", auctionStartPrice.value!.toString()); 
    formData.append("preco_minimo", promoPrice.value!.toString()); // Buy Now price
    const endDate = new Date();
    if (auctionDurationUnit.value === 'minutes') {
      endDate.setMinutes(endDate.getMinutes() + auctionDurationValue.value);
    } else if (auctionDurationUnit.value === 'hours') {
      endDate.setHours(endDate.getHours() + auctionDurationValue.value);
    } else if (auctionDurationUnit.value === 'days') {
      endDate.setDate(endDate.getDate() + auctionDurationValue.value);
    }
    formData.append("data_fim_leilao", endDate.toISOString());
  } else {
    formData.append("modo", "FIXO");
  }

  try {
    const response = await fetch(`${API_URL}/products`, {
      method: "POST",
      headers: {
        ...authHeaders(),
      },
      body: formData,
    });

    if (handleUnauthorized(response.status)) return;

    if (response.ok) {
      const data = await response.json();

      const newProduct: MerchantProduct = {
        id: data.id,
        name: data.name,
        category: data.category,
        icon: data.icon,
        originalPrice: data.originalPrice,
        promoPrice: data.price,
        quantityAvailable: data.quantity,
        reservedCount: 0,
        validity: data.validity,
        expiresLabel: data.expiresLabel,
        status: "ativo",
        paused: false,
      };

      toastStore.addToast("Produto cadastrado com sucesso!", "success");
      addProduct(newProduct);
      router.push("/comerciante/produtos");
    } else {
      const errText = await response.text();
      console.error("Erro ao cadastrar produto:", errText);
      toastStore.addToast("Erro ao cadastrar produto", "error");
    }
  } catch (err) {
    console.error("Erro na requisição", err);
    toastStore.addToast("Erro de conexão com o servidor", "error");
  }
}
</script>

<template>
  <div class="screen">
    <MerchantHeader title="Cadastrar produto" />

    <main class="content">
      <form class="form" @submit.prevent="publish">
        
        <div class="form-section">
          <h3 class="section-title">Informações Básicas</h3>
          <label class="field">
            <span class="field-label">Nome do produto</span>
            <input
              v-model="name"
              type="text"
              placeholder="Ex: Leite Integral 1L"
            />
          </label>

          <div class="row">
            <label class="field half">
              <span class="field-label">Categoria</span>
              <select v-model="category">
                <option value="" disabled>Selecione</option>
                <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
              </select>
            </label>
            <label class="field half">
              <span class="field-label">Validade</span>
              <input v-model="validity" type="date" />
            </label>
          </div>

          <label class="field">
            <span class="field-label">Descrição (Opcional)</span>
            <textarea
              v-model="description"
              placeholder="Ex: Produto fresco, ideal para..."
              rows="2"
            ></textarea>
          </label>
        </div>

        <div class="form-section">
          <h3 class="section-title">Imagem</h3>
          <div
            v-if="previewUrl"
            style="width: 100%; height: 220px; border-radius: 12px; overflow: hidden; border: 1px solid var(--mc-border); background: #ffffff; padding: 12px; display: flex; align-items: center; justify-content: center;"
          >
            <img
              :src="previewUrl"
              alt="Preview"
              style="max-width: 100%; max-height: 100%; width: auto; height: auto; object-fit: contain; border-radius: 8px;"
            />
          </div>
          <label class="field">
            <input type="file" @change="handleFileChange" accept="image/*" class="file-input" />
          </label>

          <button
            type="button"
            v-if="imageFile"
            class="ai-magic-btn"
            @click="analyzeImage"
            :disabled="isAnalyzing"
          >
            <span v-if="isAnalyzing" class="spinner"></span>
            <svg
              v-else
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path
                d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"
              />
              <path d="M5 3v4" />
              <path d="M19 17v4" />
              <path d="M3 5h4" />
              <path d="M17 19h4" />
            </svg>
            {{
              isAnalyzing
                ? "A IA está analisando a foto..."
                : "Preencher com Inteligência Artificial"
            }}
          </button>
        </div>

        <div class="form-section">
          <h3 class="section-title">Precificação</h3>
          <div class="mode-toggle">
            <label class="toggle-label">
              <input type="checkbox" v-model="isAuction" />
              <span class="slider"></span>
              <span class="toggle-text">Leilão Híbrido</span>
            </label>
            <p class="mode-hint" v-if="isAuction">
              Aceite lances a partir do Lance Inicial, ou venda na hora pelo Preço de Compra Imediata!
            </p>
          </div>

          <label class="field" v-if="isAuction">
            <span class="field-label">Duração do Leilão</span>
            <div style="display: flex; gap: 8px;">
              <input
                v-model.number="auctionDurationValue"
                type="number"
                min="1"
                step="1"
                style="flex: 1;"
              />
              <select v-model="auctionDurationUnit" style="flex: 1;">
                <option value="minutes">Minutos</option>
                <option value="hours">Horas</option>
                <option value="days">Dias</option>
              </select>
            </div>
          </label>

          <div class="row">
            <label class="field half">
              <span class="field-label">Preço Original (R$)</span>
              <input
                v-model.number="originalPrice"
                type="number"
                min="0"
                step="0.01"
                placeholder="4,99"
              />
            </label>

            <label class="field half">
              <span class="field-label">{{ isAuction ? 'Preço de Compra Imediata' : 'Desconto (R$)' }}</span>
              <input
                v-model.number="promoPrice"
                type="number"
                min="0"
                step="0.01"
                placeholder="2,49"
              />
            </label>
          </div>

          <label class="field" v-if="isAuction" style="margin-top: 4px;">
            <span class="field-label">Lance Inicial do Leilão (R$)</span>
            <input
              v-model.number="auctionStartPrice"
              type="number"
              min="0"
              step="0.01"
              placeholder="1,99"
            />
          </label>

          <label class="field">
            <span class="field-label">Quantidade disponível</span>
            <input
              v-model.number="quantity"
              type="number"
              min="0"
              step="1"
              placeholder="10"
            />
          </label>

          <div class="discount-card" v-if="!isAuction">
            <span>Desconto calculado</span>
            <span class="discount-value">{{ discountPercent }}% OFF</span>
          </div>
        </div>

        <button type="submit" class="publish-btn" :disabled="!canPublish">
          Publicar Oferta
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
  padding-bottom: 100px; /* Garante que dá para rolar até o botão passar por cima da navbar */
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
  box-shadow: 0 4px 12px rgba(10, 37, 64, 0.2);
}

.publish-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}

.ai-magic-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(135deg, #ff3b69 0%, #ff7ea5 100%);
  color: white;
  border: none;
  border-radius: var(--cf-radius-sm);
  padding: 12px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
  box-shadow: 0 4px 12px rgba(255, 59, 105, 0.3);
}

.ai-magic-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 59, 105, 0.4);
}

.ai-magic-btn:active:not(:disabled) {
  transform: translateY(0);
}

.ai-magic-btn:disabled {
  opacity: 0.7;
  cursor: wait;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
}

.mode-toggle {
  background: var(--mc-cream);
  border: 1px solid var(--mc-cream-border);
  border-radius: var(--cf-radius-sm);
  padding: 12px 14px;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.toggle-label input {
  display: none;
}

.slider {
  position: relative;
  width: 44px;
  height: 24px;
  background-color: #ccc;
  border-radius: 24px;
  transition: 0.4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  border-radius: 50%;
  transition: 0.4s;
}

input:checked + .slider {
  background-color: #ff3b69;
}

input:checked + .slider:before {
  transform: translateX(20px);
}

.toggle-text {
  font-size: 13px;
  font-weight: 700;
  color: var(--mc-text);
}

.mode-hint {
  font-size: 11px;
  color: #666;
  margin: 8px 0 0 0;
  line-height: 1.4;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
