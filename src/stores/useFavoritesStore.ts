import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { getLoggedUserId, authHeaders } from "@/utils/auth";
import { API_URL } from "@/config/api";

const FAVORITES_API = `${API_URL}/favorites`;

export const useFavoritesStore = defineStore("favorites", () => {
  // IDs sempre como string, igual a Product.id vindo da API
  const favorites = ref<string[]>([]);

  const count = computed(() => favorites.value.length);

  const fetchFavorites = async () => {
    if (!getLoggedUserId()) {
      favorites.value = [];
      return;
    }
    try {
      const res = await fetch(FAVORITES_API, { headers: authHeaders() });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      favorites.value = Array.isArray(data)
        ? data.map((id: string | number) => String(id))
        : [];
    } catch (e) {
      console.error("Erro ao carregar favoritos:", e);
    }
  };

  const toggleFavorite = async (productId: string | number) => {
    const id = String(productId);
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
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      // Sincroniza com a lista real do servidor
      if (Array.isArray(data.favorites)) {
        favorites.value = data.favorites.map((f: string | number) => String(f));
      }
    } catch (e) {
      console.error("Erro ao atualizar favorito:", e);
      // Revert if failed
      favorites.value = previous;
    }
  };

  const isFavorite = (productId: string | number) => {
    return favorites.value.includes(String(productId));
  };

  return {
    favorites,
    count,
    fetchFavorites,
    toggleFavorite,
    isFavorite,
  };
});
