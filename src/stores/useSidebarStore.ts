import { defineStore } from "pinia";
import { ref } from "vue";

export const useSidebarStore = defineStore("sidebar", () => {
  const isOpen = ref(false);
  const mobileFrame = ref(false);

  function open() {
    isOpen.value = true;
  }

  function close() {
    isOpen.value = false;
  }

  function toggle() {
    isOpen.value = !isOpen.value;
  }

  function toggleMobileFrame() {
    mobileFrame.value = !mobileFrame.value;
  }

  return {
    isOpen,
    mobileFrame,
    open,
    close,
    toggle,
    toggleMobileFrame,
  };
});
