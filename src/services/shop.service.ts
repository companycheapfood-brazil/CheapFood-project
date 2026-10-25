import axios from "axios";
import { authHeaders } from "@/utils/auth";
import { API_URL } from "@/config/api";

const RECENT_CATS_KEY = "cf_recent_categories";
const RECENT_IDS_KEY = "cf_recent_product_ids";

class ShopService {
  getProducts() {
    return axios.get(`${API_URL}/products`).then((res) => {
      return res.data;
    });
  }

  getProduct(id: number | string) {
    return axios.get(`${API_URL}/products/${id}`).then((res) => {
      const prod = res.data;
      if (prod && prod.category) {
        this.trackPreference(prod.category, prod.id);
      }
      return prod;
    });
  }

  /** Registra escolhas recentes do usuário (categorias e produtos clicados/comprados) para alimentar o algoritmo do feed */
  trackPreference(category?: string, productId?: string | number) {
    try {
      if (category && category !== "Todos") {
        const cats: string[] = JSON.parse(localStorage.getItem(RECENT_CATS_KEY) || "[]");
        const updatedCats = [category, ...cats.filter((c) => c !== category)].slice(0, 6);
        localStorage.setItem(RECENT_CATS_KEY, JSON.stringify(updatedCats));
      }
      if (productId !== undefined && productId !== null) {
        const pid = String(productId);
        const ids: string[] = JSON.parse(localStorage.getItem(RECENT_IDS_KEY) || "[]");
        const updatedIds = [pid, ...ids.filter((i) => i !== pid)].slice(0, 8);
        localStorage.setItem(RECENT_IDS_KEY, JSON.stringify(updatedIds));
      }
    } catch {
      // ignore storage errors
    }
  }

  getRecentPreferences() {
    try {
      const cats: string[] = JSON.parse(localStorage.getItem(RECENT_CATS_KEY) || "[]");
      const ids: string[] = JSON.parse(localStorage.getItem(RECENT_IDS_KEY) || "[]");
      return { cats, ids };
    } catch {
      return { cats: [], ids: [] };
    }
  }

  /** Feed personalizado estilo iFood com base nas escolhas do usuário */
  getRecommendations() {
    const { cats, ids } = this.getRecentPreferences();
    const params = new URLSearchParams();
    if (cats.length > 0) params.set("recentCategories", cats.join(","));
    if (ids.length > 0) params.set("recentIds", ids.join(","));
    const qs = params.toString() ? `?${params.toString()}` : "";
    return axios
      .get(`${API_URL}/recommendations${qs}`, { headers: authHeaders() })
      .then((res) => res.data);
  }

  /** Produtos em leilão ativos */
  getAuctions() {
    return axios.get(`${API_URL}/auctions`).then((res) => {
      return res.data;
    });
  }

  checkout(items: any[]) {
    return axios
      .post(`${API_URL}/checkout`, { items }, { headers: authHeaders() })
      .then((res) => res.data);
  }
}

export default new ShopService();
