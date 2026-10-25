<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import BottomNav from "@/components/BottomNav.vue";
import SvgIcon from "@/components/ui/SvgIcon.vue";
import { API_URL } from "@/config/api";
import { authHeaders } from "@/utils/auth";
import { useToastStore } from "@/stores/useToastStore";

const router = useRouter();
const toastStore = useToastStore();

interface OrderReviewData {
  id: number;
  rating: number;
  comment: string;
  tags?: string[];
  merchantReply?: string | null;
}

interface OrderHistoryItem {
  id: string;
  productId?: string | null;
  productName: string;
  productImage?: string | null;
  store: string;
  quantity: number;
  code: string;
  status: "pendente" | "retirado" | "expirado";
  price: number;
  total: number;
  createdAt: string;
  dateFormatted: string;
  review?: OrderReviewData | null;
}

const orders = ref<OrderHistoryItem[]>([]);
const isLoading = ref(true);
const activeTab = ref<"todos" | "pendentes" | "retirados" | "expirados">("todos");

// Modal de avaliação do pedido
const ratingModalOrder = ref<OrderHistoryItem | null>(null);
const ratingValue = ref(5);
const ratingComment = ref("");
const ratingTags = ref<string[]>(["Produto fresquinho", "Retirada rápida"]);
const isSubmittingReview = ref(false);

const quickTagOptions = [
  "Produto fresquinho",
  "Retirada rápida",
  "Ótimo desconto",
  "Embalagem impecável",
  "Sustentável",
  "Ótimo atendimento",
];

function openRatingModal(order: OrderHistoryItem) {
  ratingModalOrder.value = order;
  if (order.review) {
    ratingValue.value = order.review.rating || 5;
    ratingComment.value = order.review.comment || "";
    ratingTags.value = order.review.tags?.length
      ? [...order.review.tags]
      : ["Produto fresquinho"];
  } else {
    ratingValue.value = 5;
    ratingComment.value = "";
    ratingTags.value = ["Produto fresquinho", "Retirada rápida"];
  }
}

function toggleRatingTag(tag: string) {
  const idx = ratingTags.value.indexOf(tag);
  if (idx >= 0) {
    ratingTags.value.splice(idx, 1);
  } else {
    ratingTags.value.push(tag);
  }
}

async function submitOrderReview() {
  if (!ratingModalOrder.value || isSubmittingReview.value) return;
  isSubmittingReview.value = true;
  try {
    const res = await fetch(`${API_URL}/reviews`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...authHeaders(),
      },
      body: JSON.stringify({
        orderId: ratingModalOrder.value.id,
        productId: ratingModalOrder.value.productId,
        rating: ratingValue.value,
        comment: ratingComment.value,
        tags: ratingTags.value,
      }),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.message || "Erro ao enviar avaliação");
    }
    ratingModalOrder.value.review = data.review;
    ratingModalOrder.value = null;
    toastStore.addToast("Avaliação do pedido salva com sucesso! ⭐", "success");
  } catch (err: any) {
    toastStore.addToast(err.message || "Erro ao salvar avaliação", "error");
  } finally {
    isSubmittingReview.value = false;
  }
}

onMounted(async () => {
  try {
    const res = await fetch(`${API_URL}/orders`, {
      headers: authHeaders(),
    });
    if (res.ok) {
      orders.value = await res.json();
    }
  } catch (e) {
    console.error("Erro ao carregar histórico:", e);
  } finally {
    isLoading.value = false;
  }
});

const filteredOrders = computed(() => {
  if (activeTab.value === "todos") return orders.value;
  if (activeTab.value === "pendentes") return orders.value.filter((o) => o.status === "pendente");
  if (activeTab.value === "retirados") return orders.value.filter((o) => o.status === "retirado");
  return orders.value.filter((o) => o.status === "expirado");
});

function formatStatus(status: string) {
  if (status === "retirado") return "Retirado";
  if (status === "expirado") return "Expirado";
  return "Pendente";
}

function formatBRL(v: number) {
  return `R$ ${v.toFixed(2).replace(".", ",")}`;
}

function openReceipt(order: OrderHistoryItem) {
  router.push({
    path: "/comprovante",
    query: { code: order.code },
  });
}
</script>

<template>
  <div class="screen">
    <header class="history-header">
      <button class="back-btn" @click="router.push('/perfil')" aria-label="Voltar">
        <SvgIcon name="arrow-left" :size="17" />
      </button>
      <h1 class="title">Histórico de pedidos</h1>
      <span style="width: 34px"></span>
    </header>

    <main class="content">
      <div class="filters">
        <button
          class="filter-btn"
          :class="{ active: activeTab === 'todos' }"
          @click="activeTab = 'todos'"
        >
          Todos ({{ orders.length }})
        </button>
        <button
          class="filter-btn"
          :class="{ active: activeTab === 'pendentes' }"
          @click="activeTab = 'pendentes'"
        >
          Pendentes
        </button>
        <button
          class="filter-btn"
          :class="{ active: activeTab === 'retirados' }"
          @click="activeTab = 'retirados'"
        >
          Retirados
        </button>
        <button
          class="filter-btn"
          :class="{ active: activeTab === 'expirados' }"
          @click="activeTab = 'expirados'"
        >
          Expirados
        </button>
      </div>

      <div v-if="isLoading" class="empty-state">
        <p>Carregando seus pedidos...</p>
      </div>

      <div v-else-if="filteredOrders.length === 0" class="empty-state">
        <p>Nenhum pedido encontrado nesta aba.</p>
      </div>

      <div v-else class="order-list">
        <div
          class="order-card"
          v-for="order in filteredOrders"
          :key="order.id"
          style="cursor: pointer"
          @click="openReceipt(order)"
        >
          <div class="card-top">
            <h3 class="order-name">{{ order.productName }}</h3>
            <span
              class="status-badge"
              :class="{
                expired: order.status === 'expirado',
                success: order.status === 'retirado',
                pending: order.status === 'pendente',
              }"
            >
              {{ formatStatus(order.status) }}
            </span>
          </div>
          <p class="order-details">
            {{ order.store }} • {{ order.quantity }} un. • {{ order.dateFormatted || order.createdAt }}
          </p>
          <div class="card-bottom">
            <span class="order-code">
              <SvgIcon name="receipt" :size="14" />
              <span>Código {{ order.code }} · Ver comprovante →</span>
            </span>
            <span
              class="order-price"
              :class="{ 'expired-price': order.status === 'expirado' }"
            >
              {{ formatBRL(order.total) }}
            </span>
          </div>

          <!-- Área de Avaliação em Pedidos Retirados -->
          <div
            v-if="order.status === 'retirado'"
            class="order-review-row"
            @click.stop
          >
            <template v-if="order.review">
              <div class="reviewed-summary">
                <div class="reviewed-top">
                  <span class="reviewed-stars">
                    <SvgIcon
                      v-for="s in order.review.rating"
                      :key="s"
                      name="star-filled"
                      :size="13"
                    />
                  </span>
                  <span class="reviewed-label">Sua avaliação</span>
                  <button class="edit-review-link" @click="openRatingModal(order)">
                    Editar
                  </button>
                </div>
                <p class="reviewed-comment">“{{ order.review.comment }}”</p>
                <p v-if="order.review.merchantReply" class="reviewed-reply">
                  <strong>
                    <SvgIcon name="store" :size="13" />
                    <span>Resposta da loja:</span>
                  </strong>
                  {{ order.review.merchantReply }}
                </p>
              </div>
            </template>
            <button
              v-else
              type="button"
              class="rate-order-btn"
              @click="openRatingModal(order)"
            >
              <SvgIcon name="star-filled" :size="14" />
              <span>Avaliar Pedido e Loja</span>
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal de Avaliação do Pedido -->
    <div
      v-if="ratingModalOrder"
      class="rating-modal-backdrop"
      @click.self="ratingModalOrder = null"
    >
      <div class="rating-modal-card">
        <h3 class="rating-modal-title">Avaliar Pedido Retirado</h3>
        <p class="rating-modal-sub">
          {{ ratingModalOrder.productName }} • {{ ratingModalOrder.store }}
        </p>

        <div class="star-selector">
          <button
            v-for="s in 5"
            :key="s"
            type="button"
            class="star-btn"
            :class="{ active: s <= ratingValue }"
            @click="ratingValue = s"
          >
            <SvgIcon name="star-filled" :size="26" />
          </button>
        </div>

        <div class="tag-selector">
          <button
            v-for="tag in quickTagOptions"
            :key="tag"
            type="button"
            class="tag-chip"
            :class="{ active: ratingTags.includes(tag) }"
            @click="toggleRatingTag(tag)"
          >
            {{ tag }}
          </button>
        </div>

        <textarea
          v-model="ratingComment"
          rows="3"
          class="rating-textarea"
          placeholder="Como estava o produto e o atendimento na retirada?"
        ></textarea>

        <div class="rating-modal-actions">
          <button
            type="button"
            class="rating-cancel-btn"
            @click="ratingModalOrder = null"
          >
            Cancelar
          </button>
          <button
            type="button"
            class="rating-submit-btn"
            :disabled="isSubmittingReview"
            @click="submitOrderReview"
          >
            {{ isSubmittingReview ? "Salvando..." : "Enviar Avaliação" }}
          </button>
        </div>
      </div>
    </div>

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

.history-header {
  background: linear-gradient(135deg, #f6b55d 0%, #f5a623 100%);
  padding: 1.8rem 1.5rem 1.4rem 1.5rem;
  border-bottom-left-radius: 24px;
  border-bottom-right-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 8px 24px rgba(245, 166, 35, 0.22);
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

.filters {
  display: flex;
  gap: 0.6rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.filter-btn {
  background-color: #fdf6e9;
  border: none;
  padding: 0.5rem 0.9rem;
  border-radius: 20px;
  font-size: 0.82rem;
  font-weight: 700;
  color: #a0845a;
  cursor: pointer;
}

.filter-btn.active {
  background-color: #f6b55d;
  color: white;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.order-card {
  border: 1px solid #f0dfb8;
  border-radius: 16px;
  padding: 1rem;
  background-color: white;
  box-shadow: 0 3px 10px rgba(92, 56, 9, 0.04);
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.order-name {
  font-size: 0.95rem;
  font-weight: 800;
  color: #333;
  margin: 0;
}

.status-badge {
  background-color: #eafbe4;
  color: #2ecc71;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 800;
}

.status-badge.expired {
  background-color: #f5f5f5;
  color: #888;
}

.status-badge.pending {
  background-color: #fff4e5;
  color: #e67e22;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #999;
  font-weight: 600;
}

.order-details {
  font-size: 0.85rem;
  color: #888;
  margin: 0 0 1rem 0;
}

.card-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-code {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.84rem;
  font-weight: 600;
  color: #8c7148;
}

.order-price {
  font-size: 1rem;
  font-weight: 800;
  color: #f6b55d;
}

.order-price.expired-price {
  color: #b0b0b0;
}

.order-review-row {
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px dashed #f0dfb8;
}

.rate-order-btn {
  width: 100%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: #fdf6e9;
  border: 1px solid #f6b55d;
  color: #8c5b16;
  border-radius: 10px;
  padding: 8px 12px;
  font-size: 0.82rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.15s ease;
}

.rate-order-btn:hover {
  background: #f6b55d;
  color: #fff;
}

.reviewed-summary {
  background: #fdf8ee;
  border-radius: 10px;
  padding: 8px 10px;
}

.reviewed-top {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
}

.reviewed-stars {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  color: #f5a623;
}

.reviewed-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #8c5b16;
  flex: 1;
}

.edit-review-link {
  background: none;
  border: none;
  color: #ff3b69;
  font-size: 0.75rem;
  font-weight: 700;
  cursor: pointer;
}

.reviewed-comment {
  margin: 0;
  font-size: 0.8rem;
  color: #555;
  font-style: italic;
}

.reviewed-reply {
  margin: 6px 0 0 0;
  font-size: 0.76rem;
  color: #5c3809;
  background: #fff;
  padding: 5px 8px;
  border-left: 3px solid #f6b55d;
  border-radius: 6px;
}

.reviewed-reply strong {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-right: 4px;
}

.rating-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
}

.rating-modal-card {
  background: #fff;
  width: 100%;
  max-width: 360px;
  border-radius: 20px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
}

.rating-modal-title {
  margin: 0 0 4px 0;
  font-size: 1.15rem;
  font-weight: 800;
  color: #333;
}

.rating-modal-sub {
  margin: 0 0 12px 0;
  font-size: 0.82rem;
  color: #777;
}

.star-selector {
  display: flex;
  justify-content: center;
  gap: 6px;
  margin-bottom: 12px;
}

.star-btn {
  background: none;
  border: none;
  padding: 2px;
  color: #e0d4be;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s ease, color 0.15s ease;
}

.star-btn.active {
  color: #f5a623;
  transform: scale(1.08);
}

.tag-selector {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 6px;
  margin-bottom: 12px;
}

.tag-chip {
  border: 1px solid #e6d4b3;
  background: #fdf6e9;
  color: #6b4c1b;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 0.73rem;
  font-weight: 700;
  cursor: pointer;
}

.tag-chip.active {
  background: #ff3b69;
  border-color: #ff3b69;
  color: #fff;
}

.rating-textarea {
  width: 100%;
  border: 1px solid #e2d5be;
  border-radius: 12px;
  padding: 10px;
  font-size: 0.85rem;
  font-family: inherit;
  resize: none;
  margin-bottom: 12px;
}

.rating-modal-actions {
  display: flex;
  gap: 8px;
}

.rating-cancel-btn {
  flex: 1;
  padding: 10px;
  border-radius: 12px;
  border: none;
  background: #f3eee4;
  color: #5c3809;
  font-weight: 700;
  cursor: pointer;
}

.rating-submit-btn {
  flex: 1.4;
  padding: 10px;
  border-radius: 12px;
  border: none;
  background: #f6b55d;
  color: #5c3809;
  font-weight: 800;
  cursor: pointer;
}
</style>
