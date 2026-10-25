<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import ShopService from "@/services/shop.service";
import ProductCard from "@/components/ProductCard.vue";
import BottomNav from "@/components/BottomNav.vue";
import SvgIcon from "@/components/ui/SvgIcon.vue";
import { useFavoritesStore } from "@/stores/useFavoritesStore";
import { useSidebarStore } from "@/stores/useSidebarStore";

const favoritesStore = useFavoritesStore();
const sidebarStore = useSidebarStore();
const search = ref("");
const sortBy = ref<"forYou" | "price_asc" | "discount">("forYou");
const allProducts = ref<any[]>([]);
const topCategories = ref<string[]>(["Laticínios", "Padaria", "Frios", "Bebidas"]);

const quickChips = ["Nutella", "Leite", "Queijo", "Iogurte", "Padaria", "Laticínios"];

onMounted(async () => {
  favoritesStore.fetchFavorites();
  try {
    const rec = await ShopService.getRecommendations();
    if (rec && rec.rankedProducts && rec.rankedProducts.length > 0) {
      allProducts.value = rec.rankedProducts;
      if (rec.topCategories?.length) topCategories.value = rec.topCategories;
      return;
    }
  } catch {
    // fallback
  }
  allProducts.value = await ShopService.getProducts();
});

function applyQuickChip(term: string) {
  if (search.value.toLowerCase() === term.toLowerCase()) {
    search.value = "";
  } else {
    search.value = term;
    ShopService.trackPreference(term);
  }
}

const results = computed(() => {
  const q = search.value.trim().toLowerCase();
  const list = allProducts.value.filter(
    (p) =>
      !q ||
      p.name.toLowerCase().includes(q) ||
      (p.category && p.category.toLowerCase().includes(q)) ||
      (p.store && p.store.toLowerCase().includes(q)),
  );
  if (sortBy.value === "forYou") {
    return [...list].sort((a, b) => (b.affinityScore ?? 0) - (a.affinityScore ?? 0));
  }
  if (sortBy.value === "price_asc") {
    return [...list].sort((a, b) => a.price - b.price);
  }
  if (sortBy.value === "discount") {
    return [...list].sort((a, b) => {
      const discA = a.old_price ? (a.old_price - a.price) / a.old_price : 0;
      const discB = b.old_price ? (b.old_price - b.price) / b.old_price : 0;
      return discB - discA;
    });
  }
  return list;
});
</script>

<template>
  <div class="screen">
    <header class="header">
      <div class="header-top">
        <div style="display: flex; align-items: center; gap: 10px;">
          <button
            class="header-menu-btn"
            aria-label="Abrir menu lateral"
            @click="sidebarStore.open()"
          >
            <SvgIcon name="menu" :size="19" />
          </button>
          <h1 class="title">Explorar Ofertas</h1>
        </div>
        <span class="count-pill">{{ results.length }} itens</span>
      </div>
      <div class="search-bar">
        <input
          v-model="search"
          type="text"
          placeholder="Buscar por produto, categoria ou loja..."
          autofocus
        />
        <button
          v-if="search"
          class="clear-btn"
          type="button"
          @click="search = ''"
        >
          <SvgIcon name="x" :size="16" />
        </button>
        <span v-else class="search-icon">
          <SvgIcon name="search" :size="18" />
        </span>
      </div>

      <div class="quick-chips">
        <button
          v-for="chip in quickChips"
          :key="chip"
          type="button"
          class="quick-chip"
          :class="{ active: search.toLowerCase() === chip.toLowerCase() }"
          @click="applyQuickChip(chip)"
        >
          {{ chip }}
        </button>
      </div>
    </header>

    <main class="content">
      <div class="sort-tabs">
        <button
          type="button"
          class="sort-tab"
          :class="{ active: sortBy === 'forYou' }"
          @click="sortBy = 'forYou'"
        >
          <SvgIcon name="sparkles" :size="13" />
          <span>Para Você</span>
        </button>
        <button
          type="button"
          class="sort-tab"
          :class="{ active: sortBy === 'discount' }"
          @click="sortBy = 'discount'"
        >
          <SvgIcon name="flame" :size="13" />
          <span>Maior Desconto</span>
        </button>
        <button
          type="button"
          class="sort-tab"
          :class="{ active: sortBy === 'price_asc' }"
          @click="sortBy = 'price_asc'"
        >
          <SvgIcon name="dollar" :size="13" />
          <span>Menor Preço</span>
        </button>
      </div>

      <div class="product-list">
        <ProductCard
          v-for="p in results"
          :key="p.id"
          :product="p"
          :showReason="sortBy === 'forYou'"
        />
        <div v-if="results.length === 0" class="empty-box">
          <span class="empty-icon">
            <SvgIcon name="search" :size="28" />
          </span>
          <p class="empty">Nenhum produto encontrado para "{{ search }}".</p>
          <button class="reset-search-btn" @click="search = ''">
            Limpar busca
          </button>
        </div>
      </div>
    </main>

    <BottomNav />
  </div>
</template>

<style scoped>
.screen {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #fcfaf6;
}

.header {
  background: linear-gradient(145deg, #f5ae4b 0%, #f8c675 100%);
  padding: 20px 18px 16px;
  border-radius: 0 0 24px 24px;
  box-shadow: 0 6px 20px rgba(246, 181, 93, 0.25);
  flex-shrink: 0;
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
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
  font-size: 1.25rem;
  font-weight: 800;
  color: #2b1d0e;
  margin: 0;
}

.count-pill {
  background: rgba(255, 255, 255, 0.8);
  color: #5c3809;
  font-size: 0.75rem;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 999px;
}

.search-bar {
  position: relative;
  background: #ffffff;
  border-radius: 14px;
  display: flex;
  align-items: center;
  box-shadow: 0 6px 16px rgba(92, 56, 9, 0.08);
}

.search-bar input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  padding: 12px 40px 12px 14px;
  font-size: 0.9rem;
  color: #2b1d0e;
}

.search-bar input::placeholder {
  color: #9a886e;
}

.search-icon,
.clear-btn {
  position: absolute;
  right: 12px;
  color: #ff3b69;
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 800;
  display: flex;
  align-items: center;
}

.quick-chips {
  display: flex;
  gap: 6px;
  overflow-x: auto;
  overflow-y: hidden;
  margin-top: 10px;
  padding-bottom: 2px;
  -webkit-overflow-scrolling: touch;
  touch-action: pan-x;
  overscroll-behavior-x: contain;
  scrollbar-width: none;
}

.quick-chips::-webkit-scrollbar {
  display: none;
}

.quick-chip {
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.9);
  color: #5c3809;
  font-size: 0.73rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 999px;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.15s ease;
}

.quick-chip.active {
  background: #ff3b69;
  border-color: #ff3b69;
  color: #fff;
}

.content {
  flex: 1;
  padding: 16px;
  padding-bottom: 95px;
  overflow-y: auto;
}

.sort-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 14px;
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  touch-action: pan-x;
  overscroll-behavior-x: contain;
  scrollbar-width: none;
}

.sort-tabs::-webkit-scrollbar {
  display: none;
}

.sort-tab {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 7px 13px;
  border-radius: 999px;
  border: 1px solid #eadbc0;
  background: #ffffff;
  color: #5c3809;
  font-size: 0.78rem;
  font-weight: 700;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.15s ease;
}

.sort-tab.active {
  background: linear-gradient(135deg, #ff3b69, #e11d48);
  color: #fff;
  border-color: transparent;
  box-shadow: 0 4px 10px rgba(255, 59, 105, 0.25);
}

.product-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.empty-box {
  text-align: center;
  padding: 36px 16px;
  background: #fff;
  border: 1px dashed #eadbc0;
  border-radius: 16px;
}

.empty-icon {
  color: #ff3b69;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: #fff0f4;
  margin-bottom: 10px;
}

.empty {
  color: var(--cf-text-muted);
  font-size: 0.9rem;
  margin: 0 0 12px 0;
}

.reset-search-btn {
  background: #f6b55d;
  color: #4a2c06;
  border: none;
  border-radius: 999px;
  padding: 8px 16px;
  font-size: 0.8rem;
  font-weight: 800;
  cursor: pointer;
}
</style>
