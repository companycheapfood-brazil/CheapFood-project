<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";
import type { Product } from "@/types";
import { useCartStore } from "@/stores/useCartStore";
import { useFavoritesStore } from "@/stores/useFavoritesStore";
import AuctionBadge from "@/components/AuctionBadge.vue";
import SvgIcon from "@/components/ui/SvgIcon.vue";
import { isImageUrl, resolveImageUrl } from "@/config/api";
import ShopService from "@/services/shop.service";

const props = defineProps<{
  product: Product & {
    recommendationReason?: string;
    recommendationIcon?: string;
    matchPercent?: number;
    ratingAverage?: number;
    discountLabel?: string | null;
  };
  showReason?: boolean;
}>();

const router = useRouter();
const cartStore = useCartStore();
const favoritesStore = useFavoritesStore();
const { addToCart } = cartStore;

function openProduct() {
  ShopService.trackPreference((props.product as any).category, props.product.id);
  router.push({ name: "produto", params: { id: props.product.id } });
}

function quickAdd(event: MouseEvent) {
  event.stopPropagation();
  addToCart(props.product, 1);
}

const currentPrice = computed(() => props.product.price);

const discountShort = computed(() => {
  const orig = props.product.old_price || props.product.originalPrice;
  if (orig && orig > currentPrice.value) {
    const pct = Math.round(((orig - currentPrice.value) / orig) * 100);
    if (pct > 0) return `-${pct}%`;
  }
  return null;
});
</script>

<template>
  <div class="product-card" @click="openProduct">
    <div class="thumb">
      <span v-if="discountShort" class="thumb-discount">{{ discountShort }}</span>
      <img
        v-if="isImageUrl(product.image)"
        :src="resolveImageUrl(product.image)"
        class="real-image"
      />
      <span v-else v-html="product.image"></span>
    </div>

    <div class="info">
      <div
        v-if="showReason && product.recommendationReason"
        class="reason-pill"
      >
        <SvgIcon :name="product.recommendationIcon || 'sparkles'" :size="11" />
        <span>{{ product.recommendationReason }}</span>
      </div>
      <p class="name">{{ product.name }}</p>
      <p class="store">
        <span class="store-name-text">{{ product.store }}</span>
        <span class="esg-seal" title="Loja Consciente: Alimentos salvos do desperdício">
          <SvgIcon name="leaf" :size="9" />
          <span>Consciente</span>
        </span>
        <span class="store-rating">
          <SvgIcon name="star-filled" :size="11" />
          {{ Number(product.ratingAverage || 5).toFixed(1).replace(".", ",") }}
        </span>
      </p>
      <div class="price-row">
        <span class="price"
          >R$ {{ currentPrice.toFixed(2).replace(".", ",") }}</span
        >
        <span v-if="product.old_price" class="original-price"
          >R$ {{ product.old_price.toFixed(2).replace(".", ",") }}</span
        >
      </div>
      <div class="badges">
        <span
          v-if="product.expires_in"
          class="expires-badge"
          :class="{ urgent: product.expires_in.toLowerCase().includes('hoje') }"
        >
          {{ product.expires_in }}
        </span>
        <AuctionBadge v-if="product.auction" :auction="product.auction" />
      </div>
    </div>

    <div class="card-actions">
      <button
        class="fav-btn"
        :class="{ active: favoritesStore.isFavorite(product.id) }"
        :aria-label="
          favoritesStore.isFavorite(product.id)
            ? 'Remover dos favoritos'
            : 'Adicionar aos favoritos'
        "
        @click.stop="favoritesStore.toggleFavorite(product.id)"
      >
        <svg
          v-if="favoritesStore.isFavorite(product.id)"
          xmlns="http://www.w3.org/2000/svg"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="#FF3B69"
          stroke="#FF3B69"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path
            d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"
          />
        </svg>
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="#bfa47a"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path
            d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"
          />
        </svg>
      </button>

      <button
        class="add-btn"
        aria-label="Adicionar ao carrinho"
        @click="quickAdd"
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.product-card {
  display: grid;
  grid-template-columns: 66px 1fr auto;
  align-items: center;
  gap: 12px;
  background: linear-gradient(145deg, #fffdf9 0%, #fdf6e9 100%);
  border: 1px solid #f0e0be;
  border-radius: 16px;
  padding: 12px 14px;
  position: relative;
  cursor: pointer;
  box-shadow: 0 3px 12px rgba(92, 56, 9, 0.04);
  transition:
    transform 0.22s cubic-bezier(0.22, 1, 0.36, 1),
    box-shadow 0.22s ease,
    border-color 0.22s ease;
}

.product-card:hover {
  transform: translateY(-2px);
  border-color: #f6b55d;
  box-shadow: 0 8px 20px rgba(246, 181, 93, 0.16);
}

.thumb {
  width: 66px;
  height: 66px;
  grid-column: 1;
  grid-row: 1;
  border-radius: 14px;
  background: #ffffff;
  border: 1px solid #f3e6cb;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
}

.thumb-discount {
  position: absolute;
  top: 3px;
  left: 3px;
  background: linear-gradient(135deg, #ff3b69, #e11d48);
  color: #ffffff;
  font-size: 9px;
  font-weight: 800;
  padding: 1.5px 5px;
  border-radius: 6px;
  z-index: 2;
  letter-spacing: 0.2px;
  box-shadow: 0 2px 4px rgba(255, 59, 105, 0.3);
}

.real-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #fff;
  padding: 4px;
}

.info {
  grid-column: 2;
  grid-row: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.reason-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  align-self: flex-start;
  font-size: 9.5px;
  font-weight: 800;
  color: #b45309;
  background: #fef3c7;
  border: 1px solid #fde68a;
  padding: 2px 7px;
  border-radius: 999px;
  margin-bottom: 3px;
  max-width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.name {
  font-size: 14px;
  font-weight: 700;
  color: #2b1d0e;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 0;
}

.store {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: var(--cf-text-muted);
  margin: 2px 0 0 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.store-name-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 90px;
}

.esg-seal {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  background: #f0fdf4;
  color: #16a34a;
  border: 1px solid #bbf7d0;
  border-radius: 999px;
  padding: 1px 5px;
  font-size: 8.5px;
  font-weight: 800;
  flex-shrink: 0;
}

.store-rating {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  color: #d97706;
  font-weight: 800;
  font-size: 10.5px;
  flex-shrink: 0;
}

.price-row {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin-top: 4px;
}

.price {
  font-size: 15.5px;
  font-weight: 800;
  color: #d97706;
}

.original-price {
  font-size: 11px;
  color: #a6957c;
  text-decoration: line-through;
}

.badges {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 5px;
}

.expires-badge {
  font-size: 10px;
  font-weight: 700;
  color: #9a3412;
  background: #ffedd5;
  border: 1px solid #fed7aa;
  padding: 1.5px 8px;
  border-radius: 999px;
}

.expires-badge.urgent {
  color: #fff;
  background: linear-gradient(135deg, #ff3b69, #e11d48);
  border-color: transparent;
}

.add-btn {
  width: 36px;
  height: 36px;
  padding: 0;
  line-height: 0;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #ff3b69 0%, #e11d48 100%);
  color: white;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 4px 10px rgba(255, 59, 105, 0.3);
}

.add-btn:hover {
  transform: translateY(-2px) scale(1.06);
  box-shadow: 0 6px 15px rgba(255, 59, 105, 0.45);
}

.add-btn:active {
  transform: translateY(0) scale(0.95);
}

.card-actions {
  grid-column: 3;
  grid-row: 1;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
}

.fav-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1px solid #f0dfb8;
  background: #ffffff;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition:
    transform 0.2s,
    background-color 0.2s,
    border-color 0.2s;
}
.fav-btn svg {
  display: block;
}
.fav-btn.active {
  background: #fff0f3;
  border-color: #ffb3c6;
}
.fav-btn:hover {
  transform: scale(1.06);
}
.fav-btn:active {
  transform: scale(0.88);
}
</style>
