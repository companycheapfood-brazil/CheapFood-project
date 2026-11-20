import { defineStore } from "pinia";
import { computed, ref } from "vue";
import type { CartItem, Product } from "@/types";
import { authHeaders, handleUnauthorized } from "@/utils/auth";
import { API_URL } from "@/config/api";
import { useToastStore } from "./useToastStore";
import ShopService from "@/services/shop.service";

export interface ReceiptItemSummary {
  id: string;
  name: string;
  quantity: number;
  price: number;
  originalPrice?: number;
  total: number;
}

export interface ReceiptSummary {
  code: string;
  total: number;
  savings: number;
  store: string;
  storeAddress: string;
  paymentMethod?: "pix" | "store";
  items: ReceiptItemSummary[];
}

const PAYMENT_STORAGE_KEY = "cf_payment_methods";

function getProductUnitPrice(product: Product): number {
  const num = Number(product?.price);
  return Number.isFinite(num) && num >= 0 ? num : 0;
}

export const useCartStore = defineStore("cart", () => {
  const CART_STORAGE_KEY = "cf_cart_items";

  function loadInitialCart(): CartItem[] {
    try {
      const raw = localStorage.getItem(CART_STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed)) {
          return parsed
            .filter(
              (entry) =>
                entry &&
                entry.product &&
                entry.product.id != null &&
                Number.isFinite(Number(entry.quantity)) &&
                Number(entry.quantity) > 0,
            )
            .map((entry) => ({
              product: { ...entry.product, id: String(entry.product.id) },
              quantity: Math.floor(Number(entry.quantity)),
            }));
        }
      }
    } catch {}
    return [];
  }

  function persistCart(list: CartItem[]) {
    try {
      localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(list));
    } catch {}
  }

  function saveOrderPaymentMethod(code: string, method: "pix" | "store") {
    try {
      const raw = localStorage.getItem(PAYMENT_STORAGE_KEY);
      const map: Record<string, "pix" | "store"> = raw ? JSON.parse(raw) : {};
      const next = map && typeof map === "object" && !Array.isArray(map) ? map : {};
      next[String(code).toUpperCase()] = method;
      localStorage.setItem(PAYMENT_STORAGE_KEY, JSON.stringify(next));
    } catch {}
  }

  function getOrderPaymentMethod(code: string): "pix" | "store" {
    try {
      const raw = localStorage.getItem(PAYMENT_STORAGE_KEY);
      const map = raw ? JSON.parse(raw) : null;
      const val = map?.[String(code).toUpperCase()];
      if (val === "pix" || val === "store") return val;
    } catch {}
    return "store";
  }

  const items = ref<CartItem[]>(loadInitialCart());
  const lastReservationCode = ref("");
  const lastReceipt = ref<ReceiptSummary | null>(null);

  const toastStore = useToastStore();

  function addToCart(product: Product, quantity = 1) {
    const pid = String(product.id);
    const rawQty = (product as any).quantity;
    const maxStock = rawQty !== undefined && rawQty !== null ? Number(rawQty) : 99;
    const existingIndex = items.value.findIndex((i) => String(i.product.id) === pid);

    if (!Number.isFinite(maxStock) || maxStock <= 0) {
      if (existingIndex !== -1) {
        items.value.splice(existingIndex, 1);
        persistCart(items.value);
      }
      toastStore.addToast("Produto esgotado no momento.", "error");
      return;
    }

    const addQty = Math.max(1, Math.floor(Number(quantity) || 1));
    const normalizedProduct: Product = { ...product, id: pid };

    if (existingIndex !== -1) {
      const existing = items.value[existingIndex]!;
      existing.product = normalizedProduct;
      if (existing.quantity + addQty > maxStock) {
        existing.quantity = maxStock;
        persistCart(items.value);
        toastStore.addToast(`Limite de estoque atingido (${maxStock} un.)`, "info");
        return;
      }
      existing.quantity += addQty;
    } else {
      const initialQty = Math.min(addQty, maxStock);
      items.value.push({ product: normalizedProduct, quantity: initialQty });
    }
    persistCart(items.value);
    ShopService.trackPreference((product as any).category, pid);
    toastStore.addToast("Produto adicionado ao carrinho!", "success");
  }

  function updateQuantity(productId: string | number, delta: number) {
    const pid = String(productId);
    const item = items.value.find((i) => String(i.product.id) === pid);
    if (!item) return;

    const rawQty = (item.product as any).quantity;
    const maxStock = rawQty !== undefined && rawQty !== null ? Number(rawQty) : 99;
    if (delta > 0 && item.quantity + delta > maxStock) {
      toastStore.addToast(`Restam apenas ${maxStock} unidades em estoque`, "info");
      return;
    }

    item.quantity += delta;

    if (item.quantity <= 0) {
      removeFromCart(pid);
    } else {
      persistCart(items.value);
    }
  }

  function removeFromCart(productId: string | number) {
    const pid = String(productId);
    const index = items.value.findIndex((i) => String(i.product.id) === pid);
    if (index !== -1) {
      items.value.splice(index, 1);
      persistCart(items.value);
      toastStore.addToast("Produto removido", "info");
    }
  }

  function clearCart() {
    items.value = [];
    persistCart([]);
  }

  function resetSession() {
    items.value = [];
    lastReservationCode.value = "";
    lastReceipt.value = null;
    persistCart([]);
  }

  async function checkout(paymentMethod: "pix" | "store" = "store"): Promise<string> {
    const payload = {
      items: items.value.map((i) => ({
        id: i.product.id,
        quantity: i.quantity,
      })),
    };

    let res: Response;
    try {
      res = await fetch(`${API_URL}/checkout`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify(payload),
      });
    } catch (e) {
      console.error(e);
      throw new Error(
        "Não foi possível conectar ao servidor. Tente novamente.",
      );
    }

    const data = await res.json().catch(() => ({}));
    if (handleUnauthorized(res.status)) {
      throw new Error("Sessão expirada. Faça login novamente.");
    }
    if (!res.ok) {
      throw new Error(data.message || "Não foi possível finalizar a reserva.");
    }

    const code = String(data.code || "");
    if (code) {
      saveOrderPaymentMethod(code, paymentMethod);
    }

    lastReservationCode.value = code;
    lastReceipt.value = {
      code,
      total: Number(data.total ?? subtotal.value),
      savings: Number(data.savings ?? totalSavings.value),
      store: data.store || items.value[0]?.product.store || "Padaria & Empório Central",
      storeAddress: data.storeAddress || "Rua São Paulo, 100 - Centro, Marília/SP",
      paymentMethod,
      items: Array.isArray(data.items)
        ? data.items
        : items.value.map((i) => ({
            id: String(i.product.id),
            name: i.product.name,
            quantity: i.quantity,
            price: getProductUnitPrice(i.product),
            originalPrice: Number(i.product.originalPrice ?? i.product.price) || 0,
            total: getProductUnitPrice(i.product) * i.quantity,
          })),
    };
    return code;
  }

  const totalItems = computed(() =>
    items.value.reduce((sum, i) => sum + i.quantity, 0),
  );

  const subtotal = computed(() =>
    items.value.reduce((sum, i) => {
      return sum + getProductUnitPrice(i.product) * i.quantity;
    }, 0),
  );

  const totalSavings = computed(() =>
    items.value.reduce((sum, i) => {
      const original = Number((i.product as any).old_price ?? i.product.originalPrice ?? i.product.price) || 0;
      const current = getProductUnitPrice(i.product);
      return sum + Math.max(0, original - current) * i.quantity;
    }, 0),
  );

  return {
    items,
    lastReservationCode,
    lastReceipt,
    totalItems,
    subtotal,
    totalSavings,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart,
    resetSession,
    saveOrderPaymentMethod,
    getOrderPaymentMethod,
    checkout,
  };
});
