<script setup lang="ts">
import { ref, onMounted, computed, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import BottomNav from "@/components/BottomNav.vue";
import ProductCard from "@/components/ProductCard.vue";
import SvgIcon from "@/components/ui/SvgIcon.vue";
import ShopService from "@/services/shop.service";
import { useCartStore } from "@/stores/useCartStore";
import { useFavoritesStore } from "@/stores/useFavoritesStore";
import { useSidebarStore } from "@/stores/useSidebarStore";
import { isImageUrl, resolveImageUrl } from "@/config/api";

const router = useRouter();
const cartStore = useCartStore();
const favoritesStore = useFavoritesStore();
const sidebarStore = useSidebarStore();
const { addToCart: addCartAction } = cartStore;

const search = ref("");
const activeFilter = ref("Todos");
const sortBy = ref<"forYou" | "discount" | "expiring" | "price">("forYou");

const filters = [
  {
    name: "Todos",
    svg: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>',
  },
  {
    name: "Laticínios",
    svg: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2v20"/><path d="M18 2v20"/><path d="M6 12h12"/><path d="M6 6h12"/><path d="M6 18h12"/></svg>',
  },
  {
    name: "Padaria",
    svg: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m4.6 13.4-.6 1.5c-.7 1.9.1 3.9 1.8 5.1l.3.2c1.7 1.1 4 .8 5.4-.8l.8-.9c.7-.8 1.9-.8 2.6 0l.8.9c1.4 1.6 3.7 1.9 5.4.8l.3-.2c1.7-1.2 2.5-3.2 1.8-5.1l-.6-1.5"/><path d="M10.5 8.5 9 12"/><path d="M13.5 8.5 15 12"/><path d="m14.5 3.5 1.5 5"/><path d="m9.5 3.5-1.5 5"/><path d="m4.5 5.5 1.5 4"/><path d="m19.5 5.5-1.5 4"/></svg>',
  },
  {
    name: "Frios",
    svg: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m10.1 2.182a2 2 0 0 1 3.8 0l1.341 4.124a2 2 0 0 0 1.82 1.322h4.32a2 2 0 0 1 1.177 3.62l-3.496 2.54a2 2 0 0 0-.714 2.196l1.34 4.124a2 2 0 0 1-3.076 2.235l-3.496-2.54a2 2 0 0 0-2.352 0l-3.496 2.54a2 2 0 0 1-3.076-2.235l1.34-4.124a2 2 0 0 0-.714-2.196l-3.496-2.54a2 2 0 0 1 1.176-3.62h4.32a2 2 0 0 0 1.82-1.322L10.1 2.182Z"/></svg>',
  },
  {
    name: "Hortifruti",
    svg: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>',
  },
  {
    name: "Bebidas",
    svg: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 8 1.75 12.2A2 2 0 0 0 9.71 22h4.58a2 2 0 0 0 1.96-1.8L18 8"/><path d="M5 8h14"/><path d="M7 15a6.47 6.47 0 0 1 5 0 6.47 6.47 0 0 0 5 0"/><path d="m12 8 1-6h2"/></svg>',
  },
  {
    name: "Outros",
    svg: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>',
  },
];

const products = ref<any[]>([]);
const auctions = ref<any[]>([]);
const recommendedForYou = ref<any[]>([]);
const buyAgainList = ref<any[]>([]);
const topUserCategories = ref<string[]>([]);
const greetingName = ref("Você");

let timer: ReturnType<typeof setInterval> | null = null;

async function refreshRecommendations() {
  try {
    const rec = await ShopService.getRecommendations();
    if (rec) {
      recommendedForYou.value = rec.forYou || [];
      buyAgainList.value = rec.buyAgain || [];
      topUserCategories.value = rec.topCategories || [];
      if (rec.userName) greetingName.value = rec.userName;
      if (rec.rankedProducts && rec.rankedProducts.length > 0) {
        products.value = rec.rankedProducts;
      }
    }
  } catch {
    // fallback silencioso caso falhe
  }
}

onMounted(async () => {
  favoritesStore.fetchFavorites();
  const [prods, aucts] = await Promise.all([
    ShopService.getProducts(),
    ShopService.getAuctions().catch(() => []),
  ]);
  products.value = prods.filter((p: any) => !String(p.expires_in || "").includes("Vencido"));
  auctions.value = aucts;
  await refreshRecommendations();

  // poll de leilões a cada 10s para reordenar / remover vencidos da vitrine
  timer = setInterval(async () => {
    auctions.value = await ShopService.getAuctions().catch(() => []);
  }, 10000);
});

onUnmounted(() => {
  if (timer) clearInterval(timer);
});

async function selectCategory(catName: string) {
  activeFilter.value = catName;
  if (catName !== "Todos") {
    ShopService.trackPreference(catName);
    await refreshRecommendations();
  }
}

const filteredProducts = computed(() => {
  const list = products.value.filter((p) => {
    const matchesSearch =
      p.name.toLowerCase().includes(search.value.toLowerCase()) ||
      p.store.toLowerCase().includes(search.value.toLowerCase());
    const matchesFilter =
      activeFilter.value === "Todos" || p.category === activeFilter.value;
    return matchesSearch && matchesFilter;
  });

  return [...list].sort((a, b) => {
    if (sortBy.value === "forYou") {
      return (b.affinityScore ?? 0) - (a.affinityScore ?? 0);
    }
    if (sortBy.value === "discount") {
      const discA = a.old_price ? (a.old_price - a.price) / a.old_price : 0;
      const discB = b.old_price ? (b.old_price - b.price) / b.old_price : 0;
      return discB - discA;
    }
    if (sortBy.value === "expiring") {
      return String(a.validity || "").localeCompare(String(b.validity || ""));
    }
    if (sortBy.value === "price") {
      return a.price - b.price;
    }
    return 0;
  });
});

const goToProduct = (product: any) => {
  ShopService.trackPreference(product.category, product.id);
  router.push("/produto/" + product.id);
};

const quickAddRec = async (event: MouseEvent, product: any) => {
  event.stopPropagation();
  addCartAction(product, 1);
  await refreshRecommendations();
};
</script>

<template>
  <div class="screen">
    <header class="home-header">
      <div class="header-top-meta">
        <button
          class="header-menu-btn"
          aria-label="Abrir menu de navegação"
          @click="sidebarStore.open()"
        >
          <SvgIcon name="menu" :size="20" />
        </button>

        <div class="location-pill">
          <SvgIcon name="map-pin" :size="14" class="loc-pin-svg" />
          <span>Retirada próxima • <strong>Marília, SP</strong></span>
        </div>

        <button
          class="fav-shortcut"
          aria-label="Meus favoritos"
          @click="router.push({ name: 'perfil-favoritos' })"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="19"
            height="19"
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
          <span v-if="favoritesStore.count > 0" class="fav-shortcut-badge">{{
            favoritesStore.count
          }}</span>
        </button>
      </div>

      <div class="logo-container">
        <svg
          class="cart-icon"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M7 18C5.9 18 5.01 18.9 5.01 20C5.01 21.1 5.9 22 7 22C8.1 22 9 21.1 9 20C9 18.9 8.1 18 7 18ZM1 2V4H3L6.6 11.59L5.24 14.04C5.09 14.32 5 14.65 5 15C5 16.1 5.9 17 7 17H19V15H7.42C7.28 15 7.17 14.89 7.17 14.75L7.2 14.63L8.1 13H15.55C16.3 13 16.96 12.59 17.3 11.97L20.88 5.48C20.95 5.34 21 5.17 21 5C21 4.45 20.55 4 20 4H5.21L4.27 2H1ZM17 18C15.9 18 15.01 18.9 15.01 20C15.01 21.1 15.9 22 17 22C18.1 22 19 21.1 19 20C19 18.9 18.1 18 17 18Z"
            fill="#FF3B69"
          />
        </svg>
        <h1 class="logo-text">
          Cheap<span class="logo-text-highlight">Food</span>
        </h1>
      </div>

      <div class="search-bar">
        <input
          type="text"
          v-model="search"
          placeholder="Buscar produtos, categorias ou lojas..."
        />
        <span class="search-icon">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
        </span>

        <!-- Dropdown de Busca -->
        <div class="search-dropdown" v-if="search.length > 0">
          <ul v-if="filteredProducts.length > 0">
            <li
              v-for="p in filteredProducts"
              :key="p.id"
              @click="
                search = '';
                goToProduct(p);
              "
            >
              <img
                v-if="isImageUrl(p.image)"
                :src="resolveImageUrl(p.image)"
                class="search-thumb"
              />
              <span
                v-else
                v-html="p.image || p.icon"
                class="search-emoji"
              ></span>
              <div class="search-details">
                <span class="search-name">{{ p.name }}</span>
                <span class="search-price"
                  >R$ {{ p.price.toFixed(2).replace(".", ",") }}</span
                >
              </div>
            </li>
          </ul>
          <div v-else class="search-empty">Nenhum produto encontrado.</div>
        </div>
      </div>
    </header>

    <main class="content">
      <!-- Banner Promocional Interativo -->
      <div
        class="promo-card"
        style="cursor: pointer"
        @click="selectCategory(activeFilter === 'Laticínios' ? 'Todos' : 'Laticínios')"
      >
        <div class="promo-info">
          <span class="promo-kicker">
            <SvgIcon name="flame" :size="13" />
            <span>OFERTA SUSTENTÁVEL DO DIA</span>
          </span>
          <h2 class="promo-title">Até 60% OFF</h2>
          <h3 class="promo-subtitle">em laticínios, frios e padaria</h3>
          <p class="promo-desc">
            Toque para filtrar • Padaria & Empório Central
          </p>
        </div>
        <div class="promo-img">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="32"
            height="32"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"
            />
            <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8" />
            <path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4" />
            <path d="M2 7h20" />
            <path
              d="M22 7v3a2 2 0 0 1-2 2v0a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 16 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 12 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 8 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 4 12v0a2 2 0 0 1-2-2V7"
            />
          </svg>
        </div>
      </div>

      <!-- Categorias -->
      <div class="categories">
        <button
          v-for="filter in filters"
          :key="filter.name"
          class="category-btn"
          :class="{ active: activeFilter === filter.name }"
          @click="selectCategory(filter.name)"
        >
          <span v-if="filter.svg" class="cat-icon" v-html="filter.svg"></span>
          {{ filter.name }}
        </button>
      </div>

      <!-- SEÇÃO 1: ALGORITMO DE FEED PERSONALIZADO ("PARA VOCÊ" ESTILO IFOOD) -->
      <section
        v-if="recommendedForYou.length > 0 && activeFilter === 'Todos'"
        class="smart-feed-section"
      >
        <div class="smart-feed-head">
          <div>
            <div class="smart-title-row">
              <h2 class="heading-with-icon">
                <SvgIcon name="sparkles" :size="18" class="icon-pink" />
                <span>Sugestões para {{ greetingName }}</span>
              </h2>
              <span class="ai-feed-badge">Feed Inteligente</span>
            </div>
            <p class="smart-subtitle" v-if="topUserCategories.length > 0">
              Baseado nas suas escolhas em
              <strong>{{ topUserCategories.slice(0, 2).join(" e ") }}</strong>
            </p>
          </div>
        </div>

        <div class="foryou-carousel">
          <div
            v-for="item in recommendedForYou"
            :key="'rec-' + item.id"
            class="foryou-card"
            @click="goToProduct(item)"
          >
            <div class="foryou-top-badges">
              <span class="match-badge">{{ item.matchPercent || 95 }}% seu perfil</span>
              <span v-if="item.discountLabel" class="disc-mini">{{
                item.discountLabel.replace(" OFF", "")
              }}</span>
            </div>

            <div class="foryou-img-wrap">
              <img
                v-if="isImageUrl(item.image)"
                :src="resolveImageUrl(item.image)"
                class="foryou-img"
              />
              <span v-else class="foryou-svg" v-html="item.image"></span>
            </div>

            <span class="foryou-reason">
              <SvgIcon :name="item.recommendationIcon || 'sparkles'" :size="11" />
              <span class="reason-text">{{ item.recommendationReason }}</span>
            </span>
            <h4 class="foryou-name">{{ item.name }}</h4>
            <p class="foryou-store">{{ item.store }}</p>

            <div class="foryou-bottom">
              <div class="foryou-prices">
                <strong class="foryou-price"
                  >R$ {{ item.price.toFixed(2).replace(".", ",") }}</strong
                >
                <span v-if="item.old_price" class="foryou-old"
                  >R$ {{ item.old_price.toFixed(2).replace(".", ",") }}</span
                >
              </div>
              <button
                class="foryou-add-btn"
                aria-label="Adicionar"
                @click="quickAddRec($event, item)"
              >
                <SvgIcon name="plus" :size="15" :strokeWidth="3" />
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- SEÇÃO 2: PEÇA NOVAMENTE (HISTÓRICO REAL DO USUÁRIO) -->
      <section
        v-if="buyAgainList.length > 0 && activeFilter === 'Todos'"
        class="buy-again-section"
      >
        <div class="section-header" style="margin-bottom: 10px">
          <h2 class="heading-with-icon">
            <SvgIcon name="repeat" :size="18" class="icon-amber" />
            <span>Peça novamente</span>
          </h2>
          <a
            href="#"
            class="see-all"
            @click.prevent="router.push('/perfil/historico')"
            >Ver histórico</a
          >
        </div>
        <div class="buy-again-row">
          <div
            v-for="item in buyAgainList"
            :key="'again-' + item.id"
            class="buy-again-chip"
            @click="goToProduct(item)"
          >
            <img
              v-if="isImageUrl(item.image)"
              :src="resolveImageUrl(item.image)"
              class="again-thumb"
            />
            <div class="again-info">
              <p class="again-name">{{ item.name }}</p>
              <span class="again-meta"
                >R$ {{ item.price.toFixed(2).replace(".", ",") }} • Pediu
                {{ item.timesOrdered || 1 }}x</span
              >
            </div>
            <button
              class="again-add"
              @click="quickAddRec($event, item)"
              title="Pedir novamente"
            >
              <SvgIcon name="plus" :size="14" :strokeWidth="2.8" />
            </button>
          </div>
        </div>
      </section>

      <!-- SEÇÃO 3: LEILÕES AO VIVO -->
      <template v-if="auctions.length > 0 && activeFilter === 'Todos'">
        <div class="section-header">
          <h2 class="heading-with-icon">
            <SvgIcon name="gavel" :size="18" class="icon-pink" />
            <span>Leilões ao vivo</span>
          </h2>
          <span class="live-pulse-tag">● Tempo real</span>
        </div>
        <div class="auction-slider">
          <ProductCard
            v-for="p in auctions"
            :key="p.id"
            :product="p"
            class="slider-card"
          />
        </div>
      </template>

      <!-- SEÇÃO 4: FEED PRINCIPAL COM ORDENAÇÃO INTELIGENTE -->
      <div class="section-header" style="margin-bottom: 10px">
        <h2 class="heading-with-icon">
          <SvgIcon name="tag" :size="18" class="icon-amber" />
          <span>{{
            activeFilter === "Todos"
              ? "Feed de Ofertas"
              : `${activeFilter} em Oferta`
          }}</span>
        </h2>
        <a href="#" class="see-all" @click.prevent="router.push('/buscar')"
          >Busca avançada →</a
        >
      </div>

      <div class="feed-sort-bar">
        <button
          class="sort-pill"
          :class="{ active: sortBy === 'forYou' }"
          @click="sortBy = 'forYou'"
        >
          <SvgIcon name="sparkles" :size="13" />
          <span>Para Você</span>
        </button>
        <button
          class="sort-pill"
          :class="{ active: sortBy === 'discount' }"
          @click="sortBy = 'discount'"
        >
          <SvgIcon name="flame" :size="13" />
          <span>Maior Desconto</span>
        </button>
        <button
          class="sort-pill"
          :class="{ active: sortBy === 'expiring' }"
          @click="sortBy = 'expiring'"
        >
          <SvgIcon name="clock" :size="13" />
          <span>Vence Primeiro</span>
        </button>
        <button
          class="sort-pill"
          :class="{ active: sortBy === 'price' }"
          @click="sortBy = 'price'"
        >
          <SvgIcon name="dollar" :size="13" />
          <span>Menor Preço</span>
        </button>
      </div>

      <div class="product-list">
        <ProductCard
          v-for="product in filteredProducts"
          :key="product.id"
          :product="product"
          :showReason="sortBy === 'forYou'"
        />
        <p v-if="filteredProducts.length === 0" class="search-empty">
          Nenhum produto encontrado nesta categoria.
        </p>
      </div>
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

.home-header {
  background: linear-gradient(145deg, #f5ae4b 0%, #f8c675 100%);
  padding: 1.25rem 1.35rem 1.5rem 1.35rem;
  border-bottom-left-radius: 24px;
  border-bottom-right-radius: 24px;
  box-shadow: 0 6px 20px rgba(246, 181, 93, 0.25);
}

.header-top-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.7rem;
}

.location-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(255, 255, 255, 0.78);
  backdrop-filter: blur(4px);
  padding: 5px 11px;
  border-radius: 999px;
  font-size: 0.74rem;
  color: #5c3809;
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.fav-shortcut {
  position: relative;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: none;
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.fav-shortcut:hover {
  transform: scale(1.06);
}

.fav-shortcut-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #ff3b69;
  color: white;
  font-size: 10px;
  font-weight: 800;
  line-height: 1;
  padding: 3px 5px;
  border-radius: 999px;
  min-width: 18px;
  text-align: center;
  border: 2px solid #f6b55d;
}

.cart-icon {
  width: 26px;
  height: 26px;
}

.logo-text {
  font-size: 1.55rem;
  font-weight: 800;
  color: white;
  margin: 0;
  text-shadow: 0 2px 6px rgba(92, 56, 9, 0.12);
}

.logo-text-highlight {
  color: #ff3b69;
}

.search-bar {
  position: relative;
  width: 100%;
}

.search-bar input {
  width: 100%;
  padding: 0.85rem 2.8rem 0.85rem 1.1rem;
  border-radius: 14px;
  border: 1px solid rgba(255, 255, 255, 0.9);
  background-color: #ffffff;
  font-size: 0.92rem;
  color: #333;
  box-shadow: 0 6px 16px rgba(92, 56, 9, 0.08);
  outline: none;
  transition: box-shadow 0.2s ease;
}

.search-bar input:focus {
  box-shadow: 0 8px 22px rgba(255, 59, 105, 0.18);
}

.search-icon {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 2.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ff3b69;
}

.search-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background: white;
  border-radius: 14px;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.16);
  margin-top: 8px;
  z-index: 1000;
  max-height: 300px;
  overflow-y: auto;
}

.search-dropdown ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.search-dropdown li {
  display: flex;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #f3eee4;
  cursor: pointer;
  transition: background 0.2s;
}

.search-dropdown li:hover {
  background: #fdf6e9;
}

.search-thumb {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  object-fit: contain;
  background: #fff;
  margin-right: 12px;
}

.search-emoji {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  background: #fdf6e9;
  border-radius: 8px;
  margin-right: 12px;
}

.search-details {
  display: flex;
  flex-direction: column;
}

.search-name {
  font-weight: 700;
  font-size: 0.9rem;
  color: #333;
}

.search-price {
  font-weight: 800;
  color: #ff3b69;
  font-size: 0.85rem;
  margin-top: 2px;
}

.search-empty {
  padding: 18px;
  text-align: center;
  color: #888;
  font-size: 0.9rem;
}

.content {
  padding: 1.25rem 1.25rem 100px 1.25rem;
  flex: 1;
  overflow-y: auto;
}

.promo-card {
  background: linear-gradient(135deg, #f6b55d 0%, #f39c38 100%);
  border-radius: 18px;
  padding: 1.2rem 1.3rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #4a2c06;
  margin-bottom: 1.2rem;
  box-shadow: 0 8px 20px rgba(243, 156, 56, 0.28);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.promo-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(243, 156, 56, 0.38);
}

.promo-kicker {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(255, 255, 255, 0.85);
  color: #d92d3f;
  font-size: 0.65rem;
  font-weight: 800;
  padding: 3px 9px;
  border-radius: 999px;
  margin-bottom: 6px;
  letter-spacing: 0.4px;
}

.promo-title {
  font-size: 1.35rem;
  font-weight: 900;
  margin: 0;
  color: #2b1d0e;
}

.promo-subtitle {
  font-size: 0.98rem;
  font-weight: 700;
  margin: 0 0 0.35rem 0;
}

.promo-desc {
  font-size: 0.74rem;
  opacity: 0.9;
  margin: 0;
  font-weight: 600;
}

.promo-img {
  background-color: rgba(255, 255, 255, 0.35);
  border-radius: 50%;
  width: 58px;
  min-width: 58px;
  height: 58px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.categories {
  display: flex;
  gap: 0.6rem;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 4px 1.25rem 0.6rem 1.25rem;
  margin: 0 -1.25rem 1.2rem -1.25rem;
  -webkit-overflow-scrolling: touch;
  touch-action: pan-x;
  overscroll-behavior-x: contain;
  scrollbar-width: none;
}

.categories::-webkit-scrollbar {
  display: none;
}

.category-btn {
  flex-shrink: 0;
  padding: 0.58rem 0.95rem;
  border-radius: 999px;
  border: 1px solid #eadbc0;
  background: #ffffff;
  font-weight: 700;
  font-size: 0.82rem;
  color: #5c3809;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(92, 56, 9, 0.04);
}

.cat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.category-btn:hover {
  background-color: #fff0f3;
  border-color: #ffb3c6;
  transform: translateY(-1px);
}

.category-btn.active {
  background: linear-gradient(135deg, #ff3b69 0%, #e11d48 100%);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 12px rgba(255, 59, 105, 0.3);
}

/* SMART FEED SECTION (ESTILO IFOOD) */
.smart-feed-section {
  margin-bottom: 1.5rem;
  width: 100%;
  max-width: 100%;
}

.smart-feed-head {
  margin-bottom: 0.75rem;
}

.smart-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.smart-title-row h2 {
  font-size: 1.08rem;
  font-weight: 800;
  color: #2b1d0e;
  margin: 0;
}

.heading-with-icon {
  display: inline-flex;
  align-items: center;
  gap: 7px;
}

.icon-pink {
  color: #ff3b69;
}

.icon-amber {
  color: #d97706;
}

.loc-pin-svg {
  color: #ff3b69;
}

.ai-feed-badge {
  background: linear-gradient(135deg, #fff0f3, #ffe4e9);
  color: #e11d48;
  border: 1px solid #fecdd3;
  font-size: 0.68rem;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 999px;
}

.smart-subtitle {
  margin: 2px 0 0 0;
  font-size: 0.76rem;
  color: #7b6647;
}

.foryou-carousel {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 6px 1.25rem 14px 1.25rem;
  margin: 0 -1.25rem;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  touch-action: pan-x;
  overscroll-behavior-x: contain;
  scrollbar-width: none;
}

.foryou-carousel::-webkit-scrollbar {
  display: none;
}

.foryou-card {
  flex: 0 0 166px;
  min-width: 166px;
  max-width: 166px;
  flex-shrink: 0;
  background: linear-gradient(160deg, #ffffff 0%, #fdf6e9 100%);
  border: 1px solid #efe0c2;
  border-radius: 16px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  scroll-snap-align: start;
  box-shadow: 0 4px 14px rgba(92, 56, 9, 0.06);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    border-color 0.2s ease;
}

.foryou-card:hover {
  transform: translateY(-3px);
  border-color: #f6b55d;
  box-shadow: 0 8px 20px rgba(246, 181, 93, 0.2);
}

.foryou-top-badges {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 4px;
  margin-bottom: 6px;
}

.match-badge {
  font-size: 9px;
  font-weight: 800;
  color: #15803d;
  background: #dcfce7;
  padding: 2px 6px;
  border-radius: 999px;
}

.disc-mini {
  font-size: 9px;
  font-weight: 800;
  color: #fff;
  background: #ff3b69;
  padding: 2px 6px;
  border-radius: 999px;
}

.foryou-img-wrap {
  width: 100%;
  height: 86px;
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #f5ead4;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  margin-bottom: 7px;
}

.foryou-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 4px;
}

.foryou-svg {
  font-size: 26px;
  color: #d97706;
}

.foryou-reason {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 9.5px;
  font-weight: 800;
  color: #b45309;
  background: #fef3c7;
  padding: 3px 6px;
  border-radius: 6px;
  margin-bottom: 5px;
  white-space: nowrap;
  overflow: hidden;
}

.reason-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.foryou-name {
  font-size: 12.5px;
  font-weight: 800;
  color: #2b1d0e;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.foryou-store {
  font-size: 10.5px;
  color: #8c7658;
  margin: 1px 0 8px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.foryou-bottom {
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.foryou-prices {
  display: flex;
  flex-direction: column;
}

.foryou-price {
  font-size: 13.5px;
  font-weight: 900;
  color: #d97706;
}

.foryou-old {
  font-size: 10px;
  color: #a6957c;
  text-decoration: line-through;
}

.foryou-add-btn {
  width: 30px;
  height: 30px;
  padding: 0;
  line-height: 0;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #ff3b69, #e11d48);
  color: #fff;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 3px 8px rgba(255, 59, 105, 0.3);
}

/* PEÇA NOVAMENTE */
.buy-again-section {
  margin-bottom: 1.5rem;
}

.buy-again-row {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 4px 1.25rem 10px 1.25rem;
  margin: 0 -1.25rem;
  -webkit-overflow-scrolling: touch;
  touch-action: pan-x;
  overscroll-behavior-x: contain;
  scrollbar-width: none;
}

.buy-again-row::-webkit-scrollbar {
  display: none;
}

.buy-again-chip {
  flex: 0 0 220px;
  min-width: 220px;
  flex-shrink: 0;
  background: #ffffff;
  border: 1px solid #f0e0be;
  border-radius: 14px;
  padding: 8px 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(92, 56, 9, 0.04);
  transition: border-color 0.2s ease;
}

.buy-again-chip:hover {
  border-color: #f6b55d;
}

.again-thumb {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  object-fit: contain;
  background: #fdf6e9;
  padding: 2px;
  flex-shrink: 0;
}

.again-info {
  flex: 1;
  min-width: 0;
}

.again-name {
  margin: 0;
  font-size: 12px;
  font-weight: 800;
  color: #2b1d0e;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.again-meta {
  font-size: 10.5px;
  color: #b45309;
  font-weight: 700;
}

.again-add {
  width: 28px;
  height: 28px;
  padding: 0;
  line-height: 0;
  border-radius: 50%;
  border: 1px solid #f6b55d;
  background: #fdf6e9;
  color: #b45309;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.9rem;
}

.section-header h2 {
  font-size: 1.08rem;
  font-weight: 800;
  color: #2b1d0e;
  margin: 0;
}

.live-pulse-tag {
  font-size: 0.72rem;
  font-weight: 800;
  color: #e11d48;
  background: #ffe4e9;
  padding: 3px 9px;
  border-radius: 999px;
}

.see-all {
  color: #ff3b69;
  font-size: 0.82rem;
  font-weight: 700;
  text-decoration: none;
}

.feed-sort-bar {
  display: flex;
  gap: 6px;
  overflow-x: auto;
  overflow-y: hidden;
  margin: 0 -1.25rem 12px -1.25rem;
  padding: 2px 1.25rem 8px 1.25rem;
  -webkit-overflow-scrolling: touch;
  touch-action: pan-x;
  overscroll-behavior-x: contain;
  scrollbar-width: none;
}

.feed-sort-bar::-webkit-scrollbar {
  display: none;
}

.sort-pill {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  border: 1px solid #eadbc0;
  background: #fff;
  color: #6b4c1b;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 6px 12px;
  border-radius: 999px;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.15s ease;
}

.sort-pill.active {
  background: #2b1d0e;
  color: #f8c675;
  border-color: #2b1d0e;
}

.header-menu-btn {
  width: 38px;
  height: 38px;
  padding: 0;
  line-height: 0;
  border-radius: 12px;
  border: none;
  background-color: #ffffff;
  color: #2b1d0e;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.header-menu-btn:hover {
  transform: scale(1.06);
}

.product-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.auction-slider {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  margin-bottom: 24px;
}

.slider-card {
  width: 100%;
}

@media (max-width: 400px) {
  .home-header {
    padding: 1rem 1rem 1.25rem 1rem;
  }

  .content {
    padding: 1rem 0.9rem 100px 0.9rem;
  }

  .location-pill {
    font-size: 0.68rem;
    padding: 4px 8px;
    max-width: calc(100% - 92px);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .promo-card {
    padding: 1rem;
  }

  .promo-title {
    font-size: 1.15rem;
  }
}
</style>

