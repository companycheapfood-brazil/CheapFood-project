import { defineStore } from "pinia";
import { ref } from "vue";

export interface ToastMessage {
  id: string;
  message: string;
  type: "success" | "error" | "info";
}

export const useToastStore = defineStore("toast", () => {
  const toasts = ref<ToastMessage[]>([]);

  function addToast(
    message: string,
    type: "success" | "error" | "info" = "info",
    duration = 3000,
  ) {
    const cleanMsg = String(message || "").trim();
    if (!cleanMsg) return;
    if (toasts.value.some((t) => t.message === cleanMsg && t.type === type)) {
      return;
    }
    if (toasts.value.length >= 3) {
      toasts.value.shift();
    }
    const id = Math.random().toString(36).substring(2, 9);
    toasts.value.push({ id, message: cleanMsg, type });

    setTimeout(() => {
      removeToast(id);
    }, duration);
  }

  function removeToast(id: string) {
    const index = toasts.value.findIndex((t) => t.id === id);
    if (index > -1) {
      toasts.value.splice(index, 1);
    }
  }

  return { toasts, addToast, removeToast };
});
