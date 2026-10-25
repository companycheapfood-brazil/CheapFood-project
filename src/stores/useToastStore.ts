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
    const id = Math.random().toString(36).substring(2, 9);
    toasts.value.push({ id, message, type });

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
