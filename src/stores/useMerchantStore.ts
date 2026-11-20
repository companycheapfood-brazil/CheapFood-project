import { defineStore } from "pinia";
import { computed, ref } from "vue";
import type { MerchantProduct, Order } from "@/types";
import { API_URL } from "@/config/api";
import { authHeaders, handleUnauthorized } from "@/utils/auth";
import { useToastStore } from "./useToastStore";

export interface StoreInfo {
  id?: number;
  name: string;
  category?: string;
  cnpj: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  state: string;
  cep: string;
  openingHours: string;
  plan: "free" | "monthly" | "annual";
  paymentMethods: string;
  notificationsEnabled: boolean;
}

function createDefaultStats() {
  return {
    revenueRecovered: 0,
    activeProducts: 0,
    expiringSoon: 0,
    reservations: 0,
    completedOrdersCount: 0,
    dailySales: [] as { label: string; value: number }[],
    growth: "0%" as string | number,
    storeName: "",
    plan: "free" as "free" | "monthly" | "annual",
    itemsSaved: 0,
    foodSavedKg: 0,
    co2AvoidedKg: 0,
    ratingAverage: 0,
    ratingCount: 0,
    recentReviews: [] as any[],
  };
}

function createDefaultStoreInfo(): StoreInfo {
  return {
    name: "",
    category: "Padaria e Confeitaria",
    cnpj: "",
    email: "",
    phone: "",
    address: "",
    city: "",
    state: "",
    cep: "",
    openingHours: "",
    plan: "free",
    paymentMethods: "PIX, Cartão de Crédito, Cartão de Débito, Dinheiro",
    notificationsEnabled: true,
  };
}

export const useMerchantStore = defineStore("merchant", () => {
  const products = ref<MerchantProduct[]>([]);
  const orders = ref<Order[]>([]);
  const stats = ref(createDefaultStats());
  const storeInfo = ref<StoreInfo>(createDefaultStoreInfo());
  const lastError = ref("");
  let statsRequestSeq = 0;

  const toastStore = useToastStore();

  function resetState() {
    statsRequestSeq += 1;
    products.value = [];
    orders.value = [];
    stats.value = createDefaultStats();
    storeInfo.value = createDefaultStoreInfo();
    lastError.value = "";
  }

  async function fetchDashboardStats(period?: string) {
    const seq = ++statsRequestSeq;
    try {
      const url = period
        ? `${API_URL}/merchant/stats?period=${encodeURIComponent(period)}`
        : `${API_URL}/merchant/stats`;
      const res = await fetch(url, { headers: { ...authHeaders() } });
      if (handleUnauthorized(res.status)) return;
      if (res.ok) {
        const data = await res.json().catch(() => ({}));
        if (seq !== statsRequestSeq) return;
        stats.value = {
          revenueRecovered: Number(data.revenueRecovered ?? 0) || 0,
          activeProducts: Number(data.activeProducts ?? 0) || 0,
          expiringSoon: Number(data.expiringSoon ?? 0) || 0,
          reservations: Number(data.reservations ?? 0) || 0,
          completedOrdersCount: Number(data.completedOrdersCount ?? 0) || 0,
          dailySales: Array.isArray(data.dailySales) ? data.dailySales : [],
          growth: data.growth ?? "0%",
          storeName: data.storeName || storeInfo.value.name,
          plan: data.plan || storeInfo.value.plan,
          itemsSaved: Number(data.itemsSaved ?? 0) || 0,
          foodSavedKg: Number(data.foodSavedKg ?? 0) || 0,
          co2AvoidedKg: Number(data.co2AvoidedKg ?? 0) || 0,
          ratingAverage: Number(data.ratingAverage ?? 0) || 0,
          ratingCount: Number(data.ratingCount ?? 0) || 0,
          recentReviews: Array.isArray(data.recentReviews) ? data.recentReviews : [],
        };
        if (data.storeName) storeInfo.value.name = data.storeName;
        if (data.plan) storeInfo.value.plan = data.plan;
      }
    } catch (e) {
      console.error(e);
    }
  }

  async function replyToReview(reviewId: number, reply: string) {
    try {
      const res = await fetch(`${API_URL}/merchant/reviews/${reviewId}/reply`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ reply }),
      });
      if (handleUnauthorized(res.status)) return false;
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        toastStore.addToast(data.message || "Erro ao responder avaliação", "error");
        return false;
      }
      const idx = stats.value.recentReviews.findIndex((r: any) => r.id === reviewId);
      if (idx >= 0 && data.review) {
        stats.value.recentReviews[idx] = data.review;
      }
      toastStore.addToast(data.message || "Resposta enviada com sucesso!", "success");
      return true;
    } catch {
      toastStore.addToast("Erro de conexão ao salvar resposta", "error");
      return false;
    }
  }

  async function fetchStoreInfo() {
    try {
      const res = await fetch(`${API_URL}/merchant/store`, {
        headers: { ...authHeaders() },
      });
      if (handleUnauthorized(res.status)) return;
      if (res.ok) {
        const data = await res.json().catch(() => null);
        if (data) {
          storeInfo.value = data;
          stats.value.storeName = data.name || "";
          stats.value.plan = data.plan || "free";
        }
      }
    } catch (e) {
      console.error(e);
    }
  }

  async function updateStoreInfo(payload: Partial<StoreInfo>) {
    lastError.value = "";
    try {
      const res = await fetch(`${API_URL}/merchant/store`, {
        method: "PUT",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify(payload),
      });
      if (handleUnauthorized(res.status)) return false;
      const data = await res.json().catch(() => ({}));
      if (res.ok && data.store) {
        storeInfo.value = data.store;
        stats.value.storeName = data.store.name;
        stats.value.plan = data.store.plan;
        return true;
      }
      lastError.value = data.message || "Não foi possível salvar os dados do estabelecimento.";
      return false;
    } catch (e) {
      console.error(e);
      lastError.value = "Erro de conexão ao salvar os dados.";
      return false;
    }
  }

  async function updatePlan(plan: "free" | "monthly" | "annual") {
    lastError.value = "";
    try {
      const res = await fetch(`${API_URL}/merchant/plan`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ plan }),
      });
      if (handleUnauthorized(res.status)) return false;
      const data = await res.json().catch(() => ({}));
      if (res.ok && data.store) {
        storeInfo.value = data.store;
        stats.value.plan = data.store.plan;
        return true;
      }
      lastError.value = data.message || "Erro ao atualizar plano.";
      return false;
    } catch (e) {
      console.error(e);
      lastError.value = "Erro de conexão ao atualizar plano.";
      return false;
    }
  }

  async function fetchProducts() {
    try {
      const res = await fetch(`${API_URL}/merchant/products`, {
        headers: { ...authHeaders() },
      });
      if (handleUnauthorized(res.status)) return;
      if (res.ok) {
        const data = await res.json().catch(() => []);
        products.value = Array.isArray(data) ? data : [];
      }
    } catch (e) {
      console.error(e);
    }
  }

  async function fetchOrders() {
    try {
      const res = await fetch(`${API_URL}/merchant/orders`, {
        headers: { ...authHeaders() },
      });
      if (handleUnauthorized(res.status)) return;
      if (res.ok) {
        const data = await res.json().catch(() => []);
        orders.value = Array.isArray(data) ? data : [];
      }
    } catch (e) {
      console.error(e);
    }
  }

  async function togglePause(id: string) {
    try {
      const res = await fetch(`${API_URL}/merchant/products/${id}/pause`, {
        method: "PATCH",
        headers: { ...authHeaders() },
      });
      if (handleUnauthorized(res.status)) return false;
      const data = await res.json().catch(() => ({}));
      if (res.ok) {
        const product = products.value.find((p) => p.id === id);
        const nextPaused = typeof data.paused === "boolean" ? data.paused : !(product?.paused ?? false);
        if (product) {
          product.paused = nextPaused;
        }
        toastStore.addToast(
          `Produto ${nextPaused ? "pausado na vitrine" : "reativado na vitrine"}`,
          "info",
        );
        return true;
      }
      toastStore.addToast(data.message || "Não foi possível alterar o status do produto.", "error");
      return false;
    } catch (e) {
      console.error(e);
      toastStore.addToast("Erro de conexão ao atualizar produto.", "error");
      return false;
    }
  }

  async function applyExtraDiscount(id: string, percent = 20) {
    try {
      const res = await fetch(`${API_URL}/merchant/products/${id}/discount`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ percent }),
      });
      if (handleUnauthorized(res.status)) return false;
      const data = await res.json().catch(() => ({}));
      if (res.ok) {
        await fetchProducts();
        return true;
      }
      lastError.value = data.message || "Erro ao aplicar desconto.";
      return false;
    } catch (e) {
      console.error(e);
      lastError.value = "Erro de conexão ao aplicar desconto.";
      return false;
    }
  }

  function addProduct(product: MerchantProduct) {
    products.value.unshift(product);
  }

  async function confirmPickup(orderId: string) {
    lastError.value = "";
    try {
      const res = await fetch(`${API_URL}/merchant/orders/${orderId}/status`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ status: "retirado" }),
      });
      if (handleUnauthorized(res.status)) return false;
      const data = await res.json().catch(() => ({}));
      if (res.ok) {
        const order = orders.value.find((o) => o.id === orderId);
        if (order) {
          order.status = "retirado";
        }
        return true;
      }
      lastError.value = data.message || "Não foi possível confirmar a retirada.";
      toastStore.addToast(lastError.value, "error");
    } catch (e) {
      console.error(e);
      lastError.value = "Erro de conexão ao confirmar retirada.";
      toastStore.addToast(lastError.value, "error");
    }
    return false;
  }

  async function cancelOrder(orderId: string) {
    lastError.value = "";
    try {
      const res = await fetch(`${API_URL}/merchant/orders/${orderId}/status`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ status: "expirado" }),
      });
      if (handleUnauthorized(res.status)) return false;
      const data = await res.json().catch(() => ({}));
      if (res.ok) {
        const order = orders.value.find((o) => o.id === orderId);
        if (order) {
          order.status = "expirado";
        }
        return true;
      }
      lastError.value = data.message || "Não foi possível cancelar o pedido.";
      toastStore.addToast(lastError.value, "error");
    } catch (e) {
      console.error(e);
      lastError.value = "Erro de conexão ao cancelar o pedido.";
      toastStore.addToast(lastError.value, "error");
    }
    return false;
  }

  async function validateOrderPin(code: string, confirm = false, period?: string) {
    try {
      const res = await fetch(`${API_URL}/merchant/orders/validate-pin`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ code, confirm }),
      });
      if (handleUnauthorized(res.status)) return null;
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        toastStore.addToast(data.message || "Código PIN não encontrado", "error");
        return null;
      }
      if (confirm) {
        toastStore.addToast(data.message || "Retirada confirmada!", "success");
        await Promise.all([fetchOrders(), fetchDashboardStats(period)]);
      }
      return data;
    } catch (e) {
      console.error(e);
      toastStore.addToast("Erro ao validar código PIN", "error");
      return null;
    }
  }

  async function resetDemoData() {
    try {
      const res = await fetch(`${API_URL}/merchant/reset-demo`, {
        method: "POST",
        headers: { ...authHeaders() },
      });
      if (handleUnauthorized(res.status)) return false;
      const data = await res.json().catch(() => ({}));
      if (res.ok) {
        await Promise.all([
          fetchDashboardStats(),
          fetchStoreInfo(),
          fetchProducts(),
          fetchOrders(),
        ]);
        toastStore.addToast(
          data.message || "Cenário da apresentação restaurado!",
          "success",
        );
        return true;
      }
      toastStore.addToast(data.message || "Erro ao restaurar dados", "error");
      return false;
    } catch (e) {
      console.error(e);
      toastStore.addToast("Erro de conexão ao restaurar dados", "error");
      return false;
    }
  }

  const activeProducts = computed(() =>
    products.value.filter((p) => p.status === "ativo"),
  );
  const expiredProducts = computed(() =>
    products.value.filter((p) => p.status === "vencido"),
  );
  const soldProducts = computed(() =>
    products.value.filter((p) => p.status === "vendido"),
  );

  const pendingOrders = computed(() =>
    orders.value.filter((o) => o.status === "pendente"),
  );
  const pickedUpOrders = computed(() =>
    orders.value.filter((o) => o.status === "retirado"),
  );
  const expiredOrders = computed(() =>
    orders.value.filter((o) => o.status === "expirado"),
  );

  return {
    products,
    orders,
    stats,
    storeInfo,
    lastError,
    activeProducts,
    expiredProducts,
    soldProducts,
    pendingOrders,
    pickedUpOrders,
    expiredOrders,
    resetState,
    fetchDashboardStats,
    fetchStoreInfo,
    updateStoreInfo,
    updatePlan,
    fetchProducts,
    fetchOrders,
    togglePause,
    applyExtraDiscount,
    addProduct,
    confirmPickup,
    cancelOrder,
    validateOrderPin,
    resetDemoData,
    replyToReview,
  };
});
