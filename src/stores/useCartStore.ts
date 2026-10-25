import { defineStore } from "pinia";
import { computed, ref } from "vue";
import type { CartItem, Product } from "@/types";
import { authHeaders } from "@/utils/auth";
import { API_URL } from "@/config/api";
import { useToastStore } from "./useToastStore";
import { useAuctionClock } from "@/composables/useAuctionClock";
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
  items: ReceiptItemSummary[];
}

export const useCartStore = defineStore("cart", () => {
  const clock = useAuctionClock();
  const items = ref<CartItem[]>([]);
  const lastReservationCode = ref("");
  const lastReceipt = ref<ReceiptSummary | null>(null);

  const toastStore = useToastStore();

  function addToCart(product: Product, quantity = 1) {
    const existing = items.value.find((i) => i.product.id === product.id);
    if (existing) {
      existing.quantity += quantity;
    } else {
      items.value.push({ product, quantity });
    }
    ShopService.trackPreference((product as any).category, product.id);
    toastStore.addToast("Produto adicionado ao carrinho!", "success");
  }

  function updateQuantity(productId: string, delta: number) {
    const item = items.value.find((i) => i.product.id === productId);
    if (!item) return;

    item.quantity += delta;

    if (item.quantity <= 0) {
      removeFromCart(productId);
    }
  }

  function removeFromCart(productId: string) {
    const index = items.value.findIndex((i) => i.product.id === productId);
    if (index !== -1) {
      items.value.splice(index, 1);
      toastStore.addToast("Produto removido", "info");
    }
  }

  function clearCart() {
    items.value = [];
  }

  async function checkout(): Promise<string> {
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
    if (!res.ok) {
      throw new Error(data.message || "Não foi possível finalizar a reserva.");
    }

    lastReservationCode.value = data.code;
    lastReceipt.value = {
      code: data.code,
      total: Number(data.total ?? subtotal.value),
      savings: Number(data.savings ?? totalSavings.value),
      store: data.store || items.value[0]?.product.store || "Padaria & Empório Central",
      storeAddress: data.storeAddress || "Rua São Paulo, 100 - Centro, Marília/SP",
      items: Array.isArray(data.items)
        ? data.items
        : items.value.map((i) => ({
            id: i.product.id,
            name: i.product.name,
            quantity: i.quantity,
            price: clock.getCurrentPrice(i.product),
            originalPrice: i.product.originalPrice ?? i.product.price,
            total: clock.getCurrentPrice(i.product) * i.quantity,
          })),
    };
    return data.code;
  }

  const totalItems = computed(() =>
    items.value.reduce((sum, i) => sum + i.quantity, 0),
  );

  const subtotal = computed(() =>
    items.value.reduce((sum, i) => {
      return sum + clock.getCurrentPrice(i.product) * i.quantity;
    }, 0),
  );

  const totalSavings = computed(() =>
    items.value.reduce((sum, i) => {
      const original = (i.product as any).old_price ?? i.product.originalPrice ?? i.product.price;
      const current = clock.getCurrentPrice(i.product);
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
    checkout,
  };
});
