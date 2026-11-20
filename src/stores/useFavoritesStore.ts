import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { getLoggedUserId, authHeaders, handleUnauthorized } from "@/utils/auth";
import { API_URL } from "@/config/api";
import { useToastStore } from "./useToastStore";

const FAVORITES_API = `${API_URL}/favorites`;

export const useFavoritesStore = defineStore("favorites", () => {
  // IDs sempre como string, igual a Product.id vindo da API
  const favorites = ref<string[]>([]);
  const inFlight = new Set<string>();
  const toastStore = useToastStore();

  const count = computed(() => favorites.value.length);

  const resetState = () => {
    favorites.value = [];
    inFlight.clear();
  };

  const fetchFavorites = async () => {
    if (!getLoggedUserId()) {
      favorites.value = [];
      return;
    }
    try {
      const res = await fetch(FAVORITES_API, { headers: authHeaders() });
      if (handleUnauthorized(res.status)) return;
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json().catch(() => []);
      favorites.value = Array.isArray(data)
        ? data.map((id: string | number) => String(id))
        : [];
    } catch (e) {
      console.error("Erro ao carregar favoritos:", e);
    }
  };

  const toggleFavorite = async (productId: string | number) => {
    const id = String(productId);
    if (inFlight.has(id)) return;
    inFlight.add(id);

    const isFav = favorites.value.includes(id);
    const previous = [...favorites.value];

    // Optimistic UI update
    favorites.value = isFav
      ? favorites.value.filter((f) => f !== id)
      : [...favorites.value, id];

    try {
      const res = await fetch(`${FAVORITES_API}/${id}`, {
        method: isFav ? "DELETE" : "POST",
        headers: authHeaders(),
      });
      if (handleUnauthorized(res.status)) return;
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.message || `HTTP ${res.status}`);
      // Sincroniza com a lista real do servidor
      if (Array.isArray(data.favorites)) {
        favorites.value = data.favorites.map((f: string | number) => String(f));
      }
    } catch (e: any) {
      console.error("Erro ao atualizar favorito:", e);
      // Revert if failed
      favorites.value = previous;
      toastStore.addToast(e?.message || "Não foi possível atualizar os favoritos.", "error");
    } finally {
      inFlight.delete(id);
    }
  };

  const isFavorite = (productId: string | number) => {
    return favorites.value.includes(String(productId));
  };

  return {
    favorites,
    count,
    resetState,
    fetchFavorites,
    toggleFavorite,
    isFavorite,
  };
});
