import { defineStore } from "pinia";
import { computed, ref } from "vue";
import type { MerchantProduct, Order } from "@/types";
import { API_URL } from "@/config/api";
import { authHeaders } from "@/utils/auth";
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

export const useMerchantStore = defineStore("merchant", () => {
  const products = ref<MerchantProduct[]>([]);
  const orders = ref<Order[]>([]);
  const stats = ref({
    revenueRecovered: 0,
    activeProducts: 0,
    expiringSoon: 0,
    reservations: 0,
    dailySales: [] as { label: string; value: number }[],
    growth: "+18%" as string | number,
    storeName: "Padaria & Empório Central",
    plan: "monthly" as "free" | "monthly" | "annual",
    itemsSaved: 0,
    foodSavedKg: 0,
    co2AvoidedKg: 0,
    ratingAverage: 5.0,
    ratingCount: 0,
    recentReviews: [] as any[],
  });

  const storeInfo = ref<StoreInfo>({
    name: "Padaria & Empório Central",
    category: "Padaria e Confeitaria",
    cnpj: "12.345.678/0001-90",
    email: "contato@padariacentral.com.br",
    phone: "(14) 3433-1020",
    address: "Rua São Paulo, 100 - Centro",
    city: "Marília",
    state: "SP",
    cep: "17500-010",
    openingHours: "Seg a Sáb: 08:00 às 20:00",
    plan: "monthly",
    paymentMethods: "PIX, Cartão de Crédito/Débito e Dinheiro",
    notificationsEnabled: true,
  });

  const toastStore = useToastStore();

  async function fetchDashboardStats(period?: string) {
    try {
      const url = period
        ? `${API_URL}/merchant/stats?period=${period}`
        : `${API_URL}/merchant/stats`;
      const res = await fetch(url, { headers: { ...authHeaders() } });
      if (res.ok) {
        const data = await res.json();
        stats.value = {
          revenueRecovered: data.revenueRecovered ?? 0,
          activeProducts: data.activeProducts ?? 0,
          expiringSoon: data.expiringSoon ?? 0,
          reservations: data.reservations ?? 0,
          dailySales: data.dailySales ?? [],
          growth: data.growth ?? "+18%",
          storeName: data.storeName || storeInfo.value.name,
          plan: data.plan || storeInfo.value.plan,
          itemsSaved: data.itemsSaved ?? 0,
          foodSavedKg: data.foodSavedKg ?? 0,
          co2AvoidedKg: data.co2AvoidedKg ?? 0,
          ratingAverage: data.ratingAverage ?? 5.0,
          ratingCount: data.ratingCount ?? 0,
          recentReviews: data.recentReviews ?? [],
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
      const data = await res.json();
      if (!res.ok) {
        toastStore.addToast(data.message || "Erro ao responder avaliação", "error");
        return false;
      }
      const idx = stats.value.recentReviews.findIndex((r: any) => r.id === reviewId);
      if (idx >= 0) {
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
      if (res.ok) {
        const data = await res.json();
        storeInfo.value = data;
        stats.value.storeName = data.name;
        stats.value.plan = data.plan;
      }
    } catch (e) {
      console.error(e);
    }
  }

  async function updateStoreInfo(payload: Partial<StoreInfo>) {
    try {
      const res = await fetch(`${API_URL}/merchant/store`, {
        method: "PUT",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (res.ok && data.store) {
        storeInfo.value = data.store;
        stats.value.storeName = data.store.name;
        stats.value.plan = data.store.plan;
        return true;
      }
      return false;
    } catch (e) {
      console.error(e);
      return false;
    }
  }

  async function updatePlan(plan: "free" | "monthly" | "annual") {
    try {
      const res = await fetch(`${API_URL}/merchant/plan`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ plan }),
      });
      const data = await res.json();
      if (res.ok && data.store) {
        storeInfo.value = data.store;
        stats.value.plan = data.store.plan;
        return true;
      }
      return false;
    } catch (e) {
      console.error(e);
      return false;
    }
  }

  async function fetchProducts() {
    try {
      const res = await fetch(`${API_URL}/merchant/products`, {
        headers: { ...authHeaders() },
      });
      if (res.ok) {
        products.value = await res.json();
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
      if (res.ok) {
        orders.value = await res.json();
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
      if (res.ok) {
        const product = products.value.find((p) => p.id === id);
        if (product) {
          product.paused = !product.paused;
          toastStore.addToast(
            `Produto ${product.paused ? "pausado na vitrine" : "reativado na vitrine"}`,
            "info",
          );
        }
      }
    } catch (e) {
      console.error(e);
    }
  }

  async function applyExtraDiscount(id: string, percent = 20) {
    try {
      const res = await fetch(`${API_URL}/merchant/products/${id}/discount`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ percent }),
      });
      if (res.ok) {
        await fetchProducts();
        return true;
      } else {
        return false;
      }
    } catch (e) {
      console.error(e);
      return false;
    }
  }

  function addProduct(product: MerchantProduct) {
    products.value.unshift(product);
  }

  async function confirmPickup(orderId: string) {
    try {
      const res = await fetch(`${API_URL}/merchant/orders/${orderId}/status`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ status: "retirado" }),
      });
      if (res.ok) {
        const order = orders.value.find((o) => o.id === orderId);
        if (order) {
          order.status = "retirado";
        }
        return true;
      }
    } catch (e) {
      console.error(e);
    }
    return false;
  }

  async function cancelOrder(orderId: string) {
    try {
      const res = await fetch(`${API_URL}/merchant/orders/${orderId}/status`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ status: "expirado" }),
      });
      if (res.ok) {
        const order = orders.value.find((o) => o.id === orderId);
        if (order) {
          order.status = "expirado";
        }
        return true;
      }
    } catch (e) {
      console.error(e);
    }
    return false;
  }

  async function validateOrderPin(code: string, confirm = false) {
    try {
      const res = await fetch(`${API_URL}/merchant/orders/validate-pin`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify({ code, confirm }),
      });
      const data = await res.json();
      if (!res.ok) {
        toastStore.addToast(data.message || "Código PIN não encontrado", "error");
        return null;
      }
      if (confirm) {
        toastStore.addToast(data.message || "Retirada confirmada!", "success");
        await fetchOrders();
        await fetchDashboardStats();
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
      const data = await res.json();
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
    activeProducts,
    expiredProducts,
    soldProducts,
    pendingOrders,
    pickedUpOrders,
    expiredOrders,
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
