<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import BottomNav from "@/components/BottomNav.vue";
import AuctionBadge from "@/components/AuctionBadge.vue";
import SvgIcon from "@/components/ui/SvgIcon.vue";
import ShopService from "@/services/shop.service";
import { useCartStore } from "@/stores/useCartStore";
import { useToastStore } from "@/stores/useToastStore";
import { useAuctionClock } from "@/composables/useAuctionClock";
import { API_URL, isImageUrl, resolveImageUrl } from "@/config/api";
import { authHeaders, getLoggedUserId } from "@/utils/auth";

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const router = useRouter();
const product = ref<any>(null);
const cartStore = useCartStore();
const toastStore = useToastStore();
const { addToCart: addCartAction } = cartStore;
const clock = useAuctionClock();
const bidValue = ref<number | null>(null);
const isSubmittingBid = ref(false);
const isClaiming = ref(false);

onMounted(async () => {
  product.value = await ShopService.getProduct(props.id);
});

const auctionEndMs = computed(() =>
  product.value?.auction ? Date.parse(product.value.auction.endTime) : null,
);

const isAuctionEnded = computed(() => {
  const auction = product.value?.auction;
  if (!auction) return false;
  if (auction.ended) return true;
  return auctionEndMs.value !== null && auctionEndMs.value <= clock.now.value;
});

const hasBids = computed(() => (product.value?.auction?.bids?.length ?? 0) > 0);

const isWinner = computed(() => {
  if (!isAuctionEnded.value || !hasBids.value) return false;
  const userId = getLoggedUserId();
  return !!userId && product.value.auction.winnerId === userId;
});

/** Lance mínimo sugerido: maior lance + R$ 0,50. */
const minNextBid = computed(() => {
  const a = product.value?.auction;
  if (!a) return 0;
  return Math.round(((hasBids.value ? a.highestBid : a.startPrice) + 0.5) * 100) / 100;
});

const discountLabel = computed(() => product.value?.discountLabel || null);

const validityLabel = computed(() => {
  const v: string | undefined = product.value?.validity;
  if (!v) return "Confira na embalagem";
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(v);
  return m ? `${m[3]}/${m[2]}/${m[1]}` : v;
});

const addToCart = () => {
  addCartAction(product.value, 1);
  router.push("/carrinho");
};

const claimWinningAuction = async () => {
  if (isClaiming.value) return;
  isClaiming.value = true;
  try {
    const res = await fetch(`${API_URL}/checkout`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...authHeaders(),
      },
      body: JSON.stringify({
        items: [{ id: product.value.id, quantity: 1 }],
      }),
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.message || "Erro ao resgatar leilão");
    }

    toastStore.addToast("Leilão resgatado com sucesso!", "success");
    router.push({
      path: "/comprovante",
      query: { code: data.code, subtotal: data.total, savings: data.savings },
    });
  } catch (err: any) {
    toastStore.addToast(err.message, "error");
  } finally {
    isClaiming.value = false;
  }
};

const showBidModal = ref(false);
const bidModalMessage = ref("");
const bidModalType = ref<"success" | "error">("success");

// Modal de Avaliação Real
const showReviewModal = ref(false);
const reviewRating = ref(5);
const reviewComment = ref("");
const selectedTags = ref<string[]>(["Produto fresquinho", "Ótimo desconto"]);
const isSubmittingReview = ref(false);

const availableTags = [
  "Produto fresquinho",
  "Ótimo desconto",
  "Retirada rápida",
  "Embalagem impecável",
  "Sustentável",
  "Ótimo atendimento",
];

function toggleTag(tag: string) {
  const idx = selectedTags.value.indexOf(tag);
  if (idx >= 0) {
    selectedTags.value.splice(idx, 1);
  } else {
    selectedTags.value.push(tag);
  }
}

async function submitReview() {
  if (isSubmittingReview.value || !product.value) return;
  isSubmittingReview.value = true;
  try {
    const res = await fetch(`${API_URL}/reviews`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...authHeaders(),
      },
      body: JSON.stringify({
        productId: product.value.id,
        rating: reviewRating.value,
        comment: reviewComment.value,
        tags: selectedTags.value,
      }),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.message || "Erro ao enviar avaliação");
    }
    // Recarrega os dados do produto com a avaliação atualizada e nova média
    product.value = await ShopService.getProduct(props.id);
    showReviewModal.value = false;
    reviewComment.value = "";
    reviewRating.value = 5;
    toastStore.addToast("Avaliação publicada com sucesso! ⭐", "success");
  } catch (err: any) {
    toastStore.addToast(err.message || "Não foi possível enviar a avaliação", "error");
  } finally {
    isSubmittingReview.value = false;
  }
}

function openBidModal(type: "success" | "error", message: string) {
  bidModalType.value = type;
  bidModalMessage.value = message;
  showBidModal.value = true;
}

const submitBid = async () => {
  if (!getLoggedUserId()) {
    openBidModal("error", "Faça login para dar um lance.");
    return;
  }
  if (!bidValue.value || bidValue.value <= 0) {
    openBidModal("error", "Por favor, insira um valor para o lance.");
    return;
  }
  if (isSubmittingBid.value) return;
  isSubmittingBid.value = true;
  try {
    const res = await fetch(`${API_URL}/products/${props.id}/bids`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...authHeaders(),
      },
      body: JSON.stringify({ valor: bidValue.value }),
    });
    const data = await res.json().catch(() => ({}));
    if (res.ok) {
      product.value = data;
      bidValue.value = null;
      openBidModal("success", "Lance enviado com sucesso! Boa sorte.");
    } else {
      openBidModal("error", data.message || "Erro ao dar lance");
    }
  } catch {
    openBidModal("error", "Não foi possível conectar ao servidor.");
  } finally {
    isSubmittingBid.value = false;
  }
};
</script>

<template>
  <div class="screen" v-if="product">
    <header class="product-header">
      <button class="back-btn-top" aria-label="Voltar" @click="router.back()">
        <SvgIcon name="arrow-left" :size="15" />
        <span>Voltar</span>
      </button>
      <div class="product-image-large">
        <img
          v-if="isImageUrl(product.image)"
          :src="resolveImageUrl(product.image)"
          class="real-image-large"
        />
        <span v-else class="emoji-img" v-html="product.image"></span>
      </div>
      <h1 class="product-title">{{ product.name }}</h1>
      <p class="product-store">
        {{ product.store }}
        <span class="store-rating-pill">
          <SvgIcon name="star-filled" :size="12" style="color: #f5a623" />
          <span>
            {{ Number(product.ratingAverage || 5).toFixed(1).replace('.', ',') }}
            ({{ product.ratingCount || (product.reviews ? product.reviews.length : 1) }})
          </span>
        </span>
      </p>

      <div class="price-row">
        <span class="price"
          >R${{
            clock.getCurrentPrice(product).toFixed(2).replace(".", ",")
          }}</span
        >
        <span class="old-price" v-if="product.old_price"
          >R${{ product.old_price.toFixed(2).replace(".", ",") }}</span
        >
      </div>

      <div class="tag-row">
        <span v-if="discountLabel" class="discount-tag">{{ discountLabel }}</span>
        <span
          class="expire-tag"
          :class="{ danger: product.expires_in && product.expires_in.includes('hoje') }"
          >{{ product.expires_in }}</span
        >
      </div>
      <div style="margin-top: 12px; width: 100%">
        <AuctionBadge
          v-if="product.auction"
          :auction="product.auction"
          variant="full"
        />
      </div>
    </header>

    <main class="content">
      <p v-if="product.description" class="product-desc-box">
        {{ product.description }}
      </p>

      <div class="details-table">
        <div class="detail-row">
          <span class="label">Validade</span>
          <span class="value pink">{{ validityLabel }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Categoria</span>
          <span class="value">• {{ product.category }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Quantidade disponível</span>
          <span class="value">{{ product.quantity }} unidades</span>
        </div>
        <div class="detail-row">
          <span class="label">Estabelecimento</span>
          <span class="value store-badge-wrapper">
            <span>{{ product.store }}</span>
            <span class="esg-seal-tag" title="Certificação CheapFood de Combate ao Desperdício">
              <SvgIcon name="leaf" :size="11" />
              <span>Loja Consciente</span>
            </span>
          </span>
        </div>
        <div v-if="product.storeAddress" class="detail-row">
          <span class="label">Endereço de retirada</span>
          <span class="value">{{ product.storeAddress }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Distância</span>
          <span class="value orange">{{ product.distance }}</span>
        </div>
      </div>

      <div class="reviews-section">
        <div class="reviews-top-row">
          <div>
            <h3 class="section-title" style="margin-bottom: 2px;">Avaliações de Clientes</h3>
            <p class="reviews-subtitle">
              <SvgIcon name="star-filled" :size="13" style="color: #f5a623" />
              <strong>{{ Number(product.ratingAverage || 5).toFixed(1).replace('.', ',') }}</strong> de 5,0 •
              {{ product.ratingCount || (product.reviews ? product.reviews.length : 0) }} avaliações verificadas
            </p>
          </div>
          <button class="write-review-btn" @click="showReviewModal = true">
            <SvgIcon name="star-filled" :size="13" />
            <span>Avaliar</span>
          </button>
        </div>

        <template v-if="product.reviews && product.reviews.length > 0">
          <div
            v-for="(rev, idx) in product.reviews"
            :key="rev.id || idx"
            class="review-card"
            style="margin-bottom: 12px"
          >
            <div class="review-header">
              <div class="reviewer-avatar">{{ rev.initials || rev.authorInitials || 'CF' }}</div>
              <div class="reviewer-meta">
                <span class="reviewer-name">{{ rev.author || rev.authorName || 'Cliente' }}</span>
                <span v-if="rev.dateFormatted" class="review-date">{{ rev.dateFormatted }}</span>
              </div>
              <div class="stars">
                <SvgIcon
                  v-for="s in (rev.rating || 5)"
                  :key="s"
                  name="star-filled"
                  :size="13"
                />
              </div>
            </div>

            <div v-if="rev.tags && rev.tags.length > 0" class="review-tags-row">
              <span v-for="t in rev.tags" :key="t" class="review-tag-chip">{{ t }}</span>
            </div>

            <p class="review-text">{{ rev.comment }}</p>

            <div v-if="rev.merchantReply" class="merchant-reply-box">
              <span class="merchant-reply-title">
                <SvgIcon name="store" :size="13" />
                <span>Resposta de {{ product.store }}:</span>
              </span>
              <p class="merchant-reply-text">{{ rev.merchantReply }}</p>
            </div>
          </div>
        </template>
        <div v-else class="review-card">
          <p class="review-text">Seja o primeiro a avaliar este produto!</p>
        </div>
      </div>

      <template v-if="product.auction">
        <template v-if="!isAuctionEnded">
          <div class="bid-section">
            <h3 class="section-title">Dar um Lance</h3>
            <div class="bid-input-row">
              <input
                type="number"
                step="0.50"
                v-model.number="bidValue"
                :placeholder="`Mínimo R$ ${minNextBid.toFixed(2).replace('.', ',')}`"
                class="bid-input"
              />
              <button class="bid-button" :disabled="isSubmittingBid" @click="submitBid">
                {{ isSubmittingBid ? 'Enviando...' : 'Dar Lance' }}
              </button>
            </div>
          </div>
          <button class="add-button" @click="addToCart">Comprar Agora por R${{ product.price.toFixed(2).replace(".", ",") }}</button>
        </template>
        <template v-else>
          <div v-if="isWinner" class="bid-section" style="text-align: center;">
            <h3 class="section-title" style="display: inline-flex; align-items: center; gap: 6px;">
              <SvgIcon name="check-circle" :size="18" style="color: #15803d" />
              <span>Você venceu este leilão!</span>
            </h3>
            <button class="add-button" @click="claimWinningAuction" style="background: var(--mc-green); color: #ffffff;">Resgatar e Gerar Ticket por R$ {{ product.auction.highestBid.toFixed(2).replace('.', ',') }}</button>
          </div>
          <div v-else class="bid-section" style="text-align: center; color: #888;">
            <p v-if="product.auction.bids && product.auction.bids.length > 0">Leilão Encerrado. Arrematado por R$ {{ product.auction.highestBid.toFixed(2).replace('.', ',') }}</p>
            <p v-else>Encerrado sem lances</p>
          </div>
        </template>
      </template>
      <template v-else>
        <button class="add-button" @click="addToCart">Adicionar ao Carrinho</button>
      </template>
    </main>

    <!-- Modal de Avaliação Real -->
    <div v-if="showReviewModal" class="modal-overlay" @click.self="showReviewModal = false">
      <div class="modal-content review-modal-content">
        <h3 class="modal-title" style="margin-bottom: 4px;">Avaliar Produto</h3>
        <p class="modal-text" style="margin-bottom: 12px; font-size: 0.85rem;">
          {{ product.name }} • {{ product.store }}
        </p>

        <div class="star-picker">
          <button
            v-for="star in 5"
            :key="star"
            type="button"
            class="star-pick-btn"
            :class="{ active: star <= reviewRating }"
            @click="reviewRating = star"
          >
            <SvgIcon name="star-filled" :size="28" />
          </button>
        </div>
        <p class="star-rating-caption">
          {{
            reviewRating === 5
              ? "Excelente (5 estrelas)"
              : reviewRating === 4
              ? "Muito Bom (4 estrelas)"
              : reviewRating === 3
              ? "Bom (3 estrelas)"
              : reviewRating === 2
              ? "Regular (2 estrelas)"
              : "Ruim (1 estrela)"
          }}
        </p>

        <div class="quick-tags-picker">
          <button
            v-for="tag in availableTags"
            :key="tag"
            type="button"
            class="tag-pick-chip"
            :class="{ selected: selectedTags.includes(tag) }"
            @click="toggleTag(tag)"
          >
            {{ tag }}
          </button>
        </div>

        <textarea
          v-model="reviewComment"
          class="review-textarea"
          rows="3"
          placeholder="Conte como foi a qualidade do produto, validade e retirada na loja..."
        ></textarea>

        <div class="review-modal-actions">
          <button type="button" class="modal-cancel-btn" @click="showReviewModal = false">
            Cancelar
          </button>
          <button
            type="button"
            class="modal-btn"
            :disabled="isSubmittingReview"
            @click="submitReview"
          >
            {{ isSubmittingReview ? "Publicando..." : "Publicar Avaliação" }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de Lance -->
    <div v-if="showBidModal" class="modal-overlay" @click.self="showBidModal = false">
      <div class="modal-content">
        <div class="modal-icon" :class="bidModalType">
          <svg v-if="bidModalType === 'success'" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        </div>
        <h3 class="modal-title">{{ bidModalType === 'success' ? 'Sucesso!' : 'Atenção' }}</h3>
        <p class="modal-text">{{ bidModalMessage }}</p>
        <button class="modal-btn" @click="showBidModal = false">Entendi</button>
      </div>
    </div>

    <BottomNav />
  </div>
  <div v-else class="screen" style="align-items: center; justify-content: center; padding: 2rem; text-align: center;">
    <p style="color: #888; font-weight: 600;">Carregando detalhes do produto...</p>
  </div>
</template>

<style scoped>
.screen {
  background-color: #ffffff;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.product-header {
  position: relative;
  background: linear-gradient(to bottom, #f9b657, #f7d299);
  padding: 3.2rem 1.5rem 2rem 1.5rem;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
  text-align: center;
}

.back-btn-top {
  position: absolute;
  top: 16px;
  left: 16px;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(255, 255, 255, 0.88);
  border: none;
  border-radius: 999px;
  padding: 6px 14px;
  font-size: 0.82rem;
  font-weight: 800;
  color: #5c3809;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.product-desc-box {
  background: #fdf6e9;
  border: 1px solid #f0dfb8;
  border-radius: 12px;
  padding: 12px 14px;
  font-size: 0.88rem;
  color: #5c3809;
  line-height: 1.45;
  margin-bottom: 1rem;
}

.product-image-large {
  font-size: 5rem;
  margin-bottom: 1rem;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 140px;
  height: 140px;
  margin: 0 auto 1.5rem auto;
  border-radius: 20px;
  background: white;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}
.real-image-large {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 6px;
  border-radius: 20px;
}

.product-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #333;
  margin: 0 0 0.3rem 0;
}

.product-store {
  font-size: 0.85rem;
  color: #5c3809;
  margin: 0 0 1rem 0;
}

.price-row {
  display: flex;
  justify-content: center;
  align-items: baseline;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.price {
  font-size: 2rem;
  font-weight: 800;
  color: #333;
}

.old-price {
  font-size: 1rem;
  color: #8c5b16;
  text-decoration: line-through;
}

.tag-row {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.discount-tag {
  background-color: #ff3b69;
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 800;
}

.expire-tag {
  background-color: white;
  color: #8c5b16;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 700;
}

.content {
  padding: 1.5rem;
  flex: 1;
  overflow-y: auto;
  padding-bottom: 100px;
}

.details-table {
  display: flex;
  flex-direction: column;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 1rem 0;
  border-bottom: 1px solid #f0f0f0;
  font-size: 0.9rem;
}

.detail-row:last-child {
  border-bottom: none;
}

.label {
  color: #888;
}

.value {
  font-weight: 700;
  color: #333;
}

.value.pink {
  color: #ff3b69;
}

.value.orange {
  color: #f5a623;
}

.store-badge-wrapper {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.esg-seal-tag {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  background: #f0fdf4;
  color: #16a34a;
  border: 1px solid #bbf7d0;
  border-radius: 999px;
  padding: 2px 7px;
  font-size: 0.72rem;
  font-weight: 800;
}

.reviews-section {
  margin-top: 2rem;
}

.store-rating-pill {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  background: rgba(255, 255, 255, 0.85);
  color: #5c3809;
  font-weight: 800;
  font-size: 0.76rem;
  padding: 2px 9px;
  border-radius: 999px;
  margin-left: 6px;
}

.reviews-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 12px;
}

.reviews-subtitle {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin: 0;
  font-size: 0.8rem;
  color: #7b6647;
}

.write-review-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: #ff3b69;
  color: #fff;
  border: none;
  border-radius: 999px;
  padding: 8px 14px;
  font-size: 0.8rem;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 3px 10px rgba(255, 59, 105, 0.28);
  transition: transform 0.15s ease;
  flex-shrink: 0;
}

.write-review-btn:hover {
  transform: translateY(-1px);
}

.section-title {
  font-size: 1.1rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #333;
}

.review-card {
  border: 1px solid #f0dfb8;
  background-color: #fdf6e9;
  border-radius: 12px;
  padding: 1.1rem;
}

.review-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.6rem;
}

.reviewer-avatar {
  background-color: #ff3b69;
  color: white;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.8rem;
  flex-shrink: 0;
}

.reviewer-meta {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.reviewer-name {
  font-weight: 700;
  font-size: 0.9rem;
  color: #333;
}

.review-date {
  font-size: 0.72rem;
  color: #9a8464;
}

.stars {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  color: #f5a623;
  flex-shrink: 0;
}

.review-tags-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 8px;
}

.review-tag-chip {
  font-size: 0.7rem;
  font-weight: 700;
  background: #fff;
  color: #8c5b16;
  border: 1px solid #edd6a7;
  padding: 2px 8px;
  border-radius: 999px;
}

.review-text {
  font-size: 0.85rem;
  color: #555;
  line-height: 1.45;
  margin: 0;
}

.merchant-reply-box {
  margin-top: 10px;
  padding: 9px 11px;
  background: #fff9ef;
  border-left: 3px solid #f5a623;
  border-radius: 8px;
}

.merchant-reply-title {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.74rem;
  font-weight: 800;
  color: #8c5b16;
  margin-bottom: 3px;
}

.merchant-reply-text {
  margin: 0;
  font-size: 0.8rem;
  color: #5c3809;
  line-height: 1.38;
}

.review-modal-content {
  max-width: 380px;
  padding: 1.5rem;
}

.star-picker {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 6px;
}

.star-pick-btn {
  background: none;
  border: none;
  color: #e0d4be;
  cursor: pointer;
  padding: 2px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s ease, color 0.15s ease;
}

.star-pick-btn.active {
  color: #f5a623;
  transform: scale(1.08);
}

.star-rating-caption {
  font-size: 0.8rem;
  font-weight: 700;
  color: #8c5b16;
  margin: 0 0 12px 0;
}

.quick-tags-picker {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 6px;
  margin-bottom: 12px;
}

.tag-pick-chip {
  border: 1px solid #e6d4b3;
  background: #fdf6e9;
  color: #6b4c1b;
  border-radius: 999px;
  padding: 5px 10px;
  font-size: 0.74rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
}

.tag-pick-chip.selected {
  background: #ff3b69;
  border-color: #ff3b69;
  color: #fff;
}

.review-textarea {
  width: 100%;
  border: 1px solid #e2d5be;
  border-radius: 12px;
  padding: 10px 12px;
  font-size: 0.86rem;
  font-family: inherit;
  resize: none;
  margin-bottom: 12px;
  outline: none;
}

.review-textarea:focus {
  border-color: #f5a623;
}

.review-modal-actions {
  display: flex;
  gap: 8px;
}

.modal-cancel-btn {
  flex: 1;
  padding: 0.9rem;
  background: #f3eee4;
  color: #5c3809;
  border: none;
  border-radius: 14px;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
}

.add-button {
  width: 100%;
  background-color: #f7b75e;
  color: #5c3809;
  padding: 1.2rem;
  border: none;
  border-radius: 20px;
  font-size: 1.1rem;
  font-weight: 800;
  margin-top: 2rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 15px rgba(247, 183, 94, 0.4);
}

.add-button:hover {
  background-color: #e6a245;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(247, 183, 94, 0.5);
}

.add-button:active {
  transform: translateY(0) scale(0.98);
}

.bid-section {
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.bid-input-row {
  display: flex;
  gap: 10px;
}

.bid-input {
  flex: 1;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 12px;
  font-size: 1rem;
}

.bid-button {
  background-color: #ff3b69;
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0 1.5rem;
  font-weight: 800;
  cursor: pointer;
}

/* Modal CSS */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
  animation: fadeIn 0.2s ease;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 24px;
  width: 90%;
  max-width: 320px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease;
}

.modal-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem auto;
  color: white;
}

.modal-icon.success {
  background-color: #4caf50;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.modal-icon.error {
  background-color: #f44336;
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.3);
}

.modal-title {
  font-size: 1.3rem;
  font-weight: 800;
  color: #333;
  margin-bottom: 0.5rem;
}

.modal-text {
  font-size: 0.95rem;
  color: #666;
  margin-bottom: 1.5rem;
  line-height: 1.4;
}

.modal-btn {
  flex: 1.4;
  width: 100%;
  padding: 0.9rem 1rem;
  background-color: #f7b75e;
  color: #5c3809;
  border: none;
  border-radius: 14px;
  font-size: 0.95rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.2s ease;
}

.modal-btn:hover {
  background-color: #e6a245;
  transform: translateY(-2px);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
