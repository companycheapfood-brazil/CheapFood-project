<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import BottomNav from "@/components/BottomNav.vue";
import SvgIcon from "@/components/ui/SvgIcon.vue";
import { useCartStore } from "@/stores/useCartStore";
import { useToastStore } from "@/stores/useToastStore";
import { useSidebarStore } from "@/stores/useSidebarStore";
import { formatBRL } from "@/composables/useAuctionClock";
import { isImageUrl, resolveImageUrl } from "@/config/api";
import ShopService from "@/services/shop.service";
import { storeToRefs } from "pinia";

const router = useRouter();
const cartStore = useCartStore();
const sidebarStore = useSidebarStore();
const {
  items: cartItems,
  totalItems,
  subtotal,
  totalSavings: savings,
} = storeToRefs(cartStore);
const { updateQuantity, clearCart, addToCart } = cartStore;

const toastStore = useToastStore();
const paymentMethod = ref<"pickup" | "pix">("pickup");
const isSubmitting = ref(false);
const recommendedPool = ref<any[]>([]);
const brokenImages = ref<Record<string, boolean>>({});

function markBroken(key: string) {
  brokenImages.value[key] = true;
}

onMounted(async () => {
  try {
    const rec = await ShopService.getRecommendations();
    if (rec && Array.isArray(rec.forYou)) {
      recommendedPool.value = rec.forYou;
    }
  } catch {
    // ignore
  }
});

const cartSuggestions = computed(() => {
  const inCartIds = new Set(cartItems.value.map((i) => String(i.product.id)));
  return recommendedPool.value
    .filter((p) => !inCartIds.has(String(p.id)))
    .slice(0, 3);
});

const checkout = async () => {
  if (isSubmitting.value) return;
  isSubmitting.value = true;
  try {
    const subVal = subtotal.value;
    const savVal = savings.value;
    const payMode = paymentMethod.value === "pix" ? "pix" : "store";
    const code = await cartStore.checkout(payMode);
    clearCart();
    router.push({
      path: "/comprovante",
      query: {
        code,
        subtotal: subVal.toFixed(2),
        savings: savVal.toFixed(2),
        pay: paymentMethod.value,
      },
    });
  } catch (error) {
    console.error(error);
    toastStore.addToast(
      error instanceof Error
        ? error.message
        : "Não foi possível finalizar a reserva.",
      "error",
    );
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div class="screen">
    <header class="cart-header">
      <div style="display: flex; align-items: center; gap: 10px; min-width: 0;">
        <button
          class="header-menu-btn"
          aria-label="Abrir menu lateral"
          @click="sidebarStore.open()"
        >
          <SvgIcon name="menu" :size="19" />
        </button>
        <div style="min-width: 0;">
          <h1 class="header-title">Meu Carrinho</h1>
          <p class="header-sub">Reserva garantida para retirada rápida</p>
        </div>
      </div>
      <span class="header-badge">{{ totalItems }} {{ totalItems === 1 ? "item" : "itens" }}</span>
    </header>

    <main class="content">
      <div v-if="cartItems.length === 0" class="empty-cart">
        <div class="empty-circle">
          <SvgIcon name="shopping-cart" :size="30" />
        </div>
        <p class="empty-title">Seu carrinho está vazio</p>
        <p class="empty-desc">
          Aproveite produtos próximos do vencimento com até 60% de desconto!
        </p>
        <button
          class="checkout-btn"
          style="max-width: 240px; margin: 0 auto; padding: 0.95rem 1.4rem; font-size: 0.95rem"
          @click="router.push('/')"
        >
          Explorar ofertas
        </button>
      </div>

      <div v-else class="cart-items">
        <div class="cart-item" v-for="item in cartItems" :key="item.product.id">
          <div class="item-img">
            <img
              v-if="isImageUrl(item.product.image) && !brokenImages['c-' + item.product.id]"
              :src="resolveImageUrl(item.product.image)"
              :alt="item.product.name"
              class="real-image"
              @error="markBroken('c-' + item.product.id)"
            />
            <span v-else-if="item.product.image && !isImageUrl(item.product.image)" class="emoji-img" v-html="item.product.image"></span>
            <SvgIcon v-else name="shopping-bag" :size="22" style="color: #bfa47a" />
          </div>
          <div class="item-details">
            <h3 class="item-name">{{ item.product.name }}</h3>
            <p class="item-store">{{ item.product.store }}</p>
            <p class="item-price">{{ formatBRL(item.product.price) }}</p>
          </div>
          <div class="quantity-selector">
            <button class="q-btn" @click="updateQuantity(item.product.id, -1)" aria-label="Diminuir">
              <SvgIcon name="minus" :size="14" :strokeWidth="2.8" />
            </button>
            <span class="q-val">{{ item.quantity }}</span>
            <button class="q-btn" @click="updateQuantity(item.product.id, 1)" aria-label="Aumentar">
              <SvgIcon name="plus" :size="14" :strokeWidth="2.8" />
            </button>
          </div>
        </div>
      </div>

      <!-- Sugestões Inteligentes no Carrinho (Cross-sell) -->
      <section
        v-if="cartItems.length > 0 && cartSuggestions.length > 0"
        class="upsell-section"
      >
        <p class="upsell-title">
          <SvgIcon name="sparkles" :size="15" />
          <span>Complete sua sacola com desconto</span>
        </p>
        <div class="upsell-row">
          <div
            v-for="sug in cartSuggestions"
            :key="sug.id"
            class="upsell-card"
          >
            <img
              v-if="isImageUrl(sug.image) && !brokenImages['u-' + sug.id]"
              :src="resolveImageUrl(sug.image)"
              :alt="sug.name"
              class="upsell-thumb"
              @error="markBroken('u-' + sug.id)"
            />
            <span
              v-else
              class="upsell-thumb"
              style="display: inline-flex; align-items: center; justify-content: center; color: #bfa47a;"
            >
              <SvgIcon name="shopping-bag" :size="16" />
            </span>
            <div class="upsell-info">
              <p class="upsell-name">{{ sug.name }}</p>
              <strong class="upsell-price">{{ formatBRL(sug.price) }}</strong>
            </div>
            <button
              type="button"
              class="upsell-add"
              @click="addToCart(sug, 1)"
            >
              <SvgIcon name="plus" :size="12" :strokeWidth="2.8" />
              <span>Adicionar</span>
            </button>
          </div>
        </div>
      </section>

      <div class="summary-card" v-if="cartItems.length > 0">
        <div style="margin-bottom: 1.1rem">
          <p class="pay-section-label">Forma de Pagamento</p>
          <div class="pay-options">
            <button
              type="button"
              class="pay-option-btn"
              :class="{ active: paymentMethod === 'pickup' }"
              @click="paymentMethod = 'pickup'"
            >
              <SvgIcon name="store" :size="15" />
              <span>Pagar na Retirada</span>
            </button>
            <button
              type="button"
              class="pay-option-btn"
              :class="{ active: paymentMethod === 'pix' }"
              @click="paymentMethod = 'pix'"
            >
              <SvgIcon name="pix" :size="15" />
              <span>PIX Instantâneo</span>
            </button>
          </div>
        </div>

        <div class="summary-row">
          <span class="label">Subtotal</span>
          <span class="value"
            >R$ {{ subtotal.toFixed(2).replace(".", ",") }}</span
          >
        </div>
        <div class="summary-row">
          <span class="label">Economia total</span>
          <span class="value pink"
            >- R$ {{ savings.toFixed(2).replace(".", ",") }}</span
          >
        </div>
        <hr class="divider" />
        <div class="summary-row total-row">
          <span class="label">Total a pagar</span>
          <span class="value"
            >R$ {{ subtotal.toFixed(2).replace(".", ",") }}</span
          >
        </div>

        <div class="savings-badge">
          <SvgIcon name="leaf" :size="15" />
          <span>Você está economizando R$ {{ savings.toFixed(2).replace(".", ",") }} e evitando desperdício!</span>
        </div>
      </div>

      <button
        v-if="cartItems.length > 0"
        class="checkout-btn"
        :disabled="isSubmitting"
        @click="checkout"
      >
        {{ isSubmitting ? "Processando reserva..." : "Confirmar Reserva e Gerar PIN" }}
      </button>
      <p v-if="cartItems.length > 0" class="checkout-hint">
        <SvgIcon name="clock" :size="13" />
        <span>Itens reservados por 3h para retirada no estabelecimento</span>
      </p>
    </main>

    <BottomNav />
  </div>
</template>

<style scoped>
.screen {
  background-color: #fcfaf6;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.cart-header {
  background: linear-gradient(145deg, #f5ae4b 0%, #f8c675 100%);
  padding: 1.75rem 1.5rem 1.4rem 1.5rem;
  border-bottom-left-radius: 24px;
  border-bottom-right-radius: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 6px 20px rgba(246, 181, 93, 0.25);
}

.header-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: #2b1d0e;
  margin: 0;
}

.header-sub {
  font-size: 0.76rem;
  color: #5c3809;
  margin: 2px 0 0 0;
  font-weight: 600;
}

.header-badge {
  background: linear-gradient(135deg, #ff3b69, #e11d48);
  color: white;
  padding: 0.35rem 0.85rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 800;
  box-shadow: 0 3px 8px rgba(255, 59, 105, 0.3);
}

.content {
  padding: 1.35rem;
  flex: 1;
  overflow-y: auto;
  padding-bottom: 105px;
}

.empty-cart {
  text-align: center;
  background: #ffffff;
  border: 1px dashed #eadbc0;
  border-radius: 20px;
  padding: 2.5rem 1.5rem;
  margin-top: 1.5rem;
}

.empty-circle {
  width: 68px;
  height: 68px;
  border-radius: 50%;
  background: #fdf6e9;
  color: #d97706;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 0.9rem auto;
}

.empty-title {
  font-weight: 800;
  font-size: 1.05rem;
  color: #2b1d0e;
  margin: 0 0 0.35rem 0;
}

.empty-desc {
  font-size: 0.85rem;
  color: #8c7658;
  margin: 0 0 1.4rem 0;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.cart-item {
  display: flex;
  align-items: center;
  padding: 12px;
  background: #ffffff;
  border: 1px solid #f0e0be;
  border-radius: 16px;
  gap: 12px;
  box-shadow: 0 3px 10px rgba(92, 56, 9, 0.04);
}

.item-details {
  flex: 1;
  min-width: 0;
}

.item-name {
  font-size: 0.92rem;
  font-weight: 800;
  color: #2b1d0e;
  margin: 0 0 2px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-store {
  font-size: 0.74rem;
  color: #8c7658;
  margin: 0 0 4px 0;
}

.item-price {
  font-size: 1rem;
  font-weight: 800;
  color: #d97706;
  margin: 0;
}

.quantity-selector {
  display: flex;
  align-items: center;
  border: 1px solid #ebd7b2;
  border-radius: 999px;
  background-color: #fdf6e9;
  overflow: hidden;
  flex-shrink: 0;
}

.q-btn {
  background: transparent;
  border: none;
  width: 32px;
  height: 32px;
  padding: 0;
  line-height: 0;
  color: #8c5b16;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.q-btn:hover {
  background-color: #f5e4c6;
}

.q-val {
  width: 22px;
  text-align: center;
  font-weight: 800;
  color: #2b1d0e;
  font-size: 0.9rem;
}

.upsell-section {
  margin-top: 1.35rem;
}

.upsell-title {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.84rem;
  font-weight: 800;
  color: #5c3809;
  margin: 0 0 8px 0;
}

.upsell-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.upsell-card {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #fffdf9;
  border: 1px dashed #e6cfa3;
  border-radius: 12px;
  padding: 8px 10px;
}

.upsell-thumb {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  object-fit: contain;
  background: #fff;
  padding: 2px;
  border: 1px solid #f2e4c9;
}

.upsell-info {
  flex: 1;
  min-width: 0;
}

.upsell-name {
  margin: 0;
  font-size: 0.8rem;
  font-weight: 700;
  color: #2b1d0e;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.upsell-price {
  font-size: 0.78rem;
  color: #d97706;
  font-weight: 800;
}

.upsell-add {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  background: #fdf6e9;
  border: 1px solid #f6b55d;
  color: #8c5b16;
  border-radius: 999px;
  padding: 6px 11px;
  font-size: 0.74rem;
  font-weight: 800;
  cursor: pointer;
}

.summary-card {
  background: linear-gradient(160deg, #ffffff 0%, #fdf6e9 100%);
  border: 1px solid #f0dfb8;
  border-radius: 18px;
  padding: 1.35rem;
  margin-top: 1.4rem;
  box-shadow: 0 6px 18px rgba(92, 56, 9, 0.06);
}

.pay-section-label {
  font-size: 0.75rem;
  font-weight: 800;
  color: #5c3809;
  margin: 0 0 0.5rem 0;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.pay-options {
  display: flex;
  gap: 8px;
}

.pay-option-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px;
  border-radius: 12px;
  border: 1px solid #eadbc0;
  background: #ffffff;
  font-weight: 700;
  font-size: 0.78rem;
  color: #4a2c06;
  cursor: pointer;
  transition: all 0.15s ease;
}

.pay-option-btn.active {
  border: 2px solid #ff3b69;
  background: #fff0f3;
  color: #b91c1c;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  font-size: 0.9rem;
}

.summary-row .label {
  color: #7b6647;
}

.summary-row .value {
  font-weight: 800;
  color: #2b1d0e;
}

.summary-row .value.pink {
  color: #ff3b69;
}

.divider {
  border: none;
  border-top: 1px dashed #dcb985;
  margin: 0.9rem 0;
}

.total-row {
  font-size: 1.12rem;
}

.total-row .label {
  font-weight: 800;
  color: #2b1d0e;
}

.savings-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: linear-gradient(135deg, #ff3b69 0%, #e11d48 100%);
  color: white;
  text-align: center;
  padding: 0.65rem 0.9rem;
  border-radius: 14px;
  font-weight: 800;
  font-size: 0.8rem;
  margin-top: 1.1rem;
  box-shadow: 0 4px 12px rgba(255, 59, 105, 0.25);
}

.checkout-btn {
  width: 100%;
  background: linear-gradient(135deg, #f7b75e 0%, #f39c38 100%);
  color: #3d2305;
  padding: 1.15rem;
  border: none;
  border-radius: 18px;
  font-size: 1.05rem;
  font-weight: 800;
  margin-top: 1.4rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 6px 18px rgba(243, 156, 56, 0.35);
}

.checkout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 22px rgba(243, 156, 56, 0.45);
}

.checkout-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  text-align: center;
  color: #8c7658;
  font-size: 0.75rem;
  font-weight: 600;
  margin-top: 0.7rem;
}

.item-img {
  width: 60px;
  min-width: 60px;
  height: 60px;
  flex-shrink: 0;
  background-color: #ffffff;
  border: 1px solid #f0dfb8;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
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

.real-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 3px;
}

@media (max-width: 400px) {
  .cart-header {
    padding: 1.25rem 1rem 1.15rem 1rem;
  }

  .header-title {
    font-size: 1.15rem;
  }

  .pay-options {
    flex-direction: column;
  }
}
</style>

