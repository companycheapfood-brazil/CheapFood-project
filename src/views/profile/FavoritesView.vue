<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import ShopService from "@/services/shop.service";
import ProductCard from "@/components/ProductCard.vue";
import BottomNav from "@/components/BottomNav.vue";
import { useFavoritesStore } from "@/stores/useFavoritesStore";

const router = useRouter();
const favoritesStore = useFavoritesStore();
const allProducts = ref<any[]>([]);
const isLoading = ref(true);
const loadError = ref("");

async function loadFavorites() {
  isLoading.value = true;
  loadError.value = "";
  try {
    const [, prods] = await Promise.all([
      favoritesStore.fetchFavorites(),
      ShopService.getProducts(),
    ]);
    const list = Array.isArray(prods) ? prods : [];
    allProducts.value = list.filter(
      (p: any) => !String(p.expires_in || "").includes("Vencido"),
    );
  } catch {
    loadError.value = "Não foi possível carregar seus favoritos.";
  } finally {
    isLoading.value = false;
  }
}

onMounted(loadFavorites);

const results = computed(() => {
  return allProducts.value.filter((p) => favoritesStore.isFavorite(p.id));
});
</script>

<template>
  <div class="screen">
    <header class="header">
      <button type="button" class="back-btn" @click="router.push('/perfil')" aria-label="Voltar">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="m15 18-6-6 6-6" />
        </svg>
      </button>
      <h1 class="title">Meus Favoritos</h1>
    </header>

    <main class="content">
      <div class="product-list">
        <p v-if="isLoading" class="empty">Carregando seus favoritos...</p>
        <div v-else-if="loadError" class="empty">
          <p style="margin-bottom: 12px">{{ loadError }}</p>
          <button
            type="button"
            style="background: #ff3b69; color: #fff; border: none; border-radius: 999px; padding: 8px 16px; font-weight: 700; cursor: pointer;"
            @click="loadFavorites"
          >
            Tentar novamente
          </button>
        </div>
        <template v-else>
          <ProductCard v-for="p in results" :key="p.id" :product="p" />
          <p v-if="results.length === 0" class="empty">
            Você ainda não tem produtos favoritos disponíveis.
          </p>
        </template>
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
  background: var(--cf-bg);
}

.header {
  background: #ff3b69;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  color: white;
  border-radius: 0 0 20px 20px;
}

.title {
  font-size: 18px;
  font-weight: 700;
  margin: 0;
}

.back-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.product-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-bottom: 80px;
}

.empty {
  text-align: center;
  color: #bfa47a;
  margin-top: 40px;
  font-weight: 500;
}
</style>
