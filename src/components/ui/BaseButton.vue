<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  variant?: "primary" | "secondary" | "danger";
  type?: "button" | "submit" | "reset";
  disabled?: boolean;
}>();

const emit = defineEmits<{
  (e: "click", event: MouseEvent): void;
}>();

const btnClass = computed(() => {
  return `base-btn base-btn-${props.variant || "primary"}`;
});
</script>

<template>
  <button
    :class="btnClass"
    :type="type || 'button'"
    :disabled="disabled"
    @click="emit('click', $event)"
  >
    <slot />
  </button>
</template>

<style scoped>
.base-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 14px 24px;
  border-radius: var(--cf-radius-md, 12px);
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
  width: 100%;
}

.base-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.base-btn-primary {
  background: var(--cf-orange, #f5a623);
  color: white;
}

.base-btn-primary:not(:disabled):hover {
  background: var(--cf-orange-hover, #e69512);
  transform: translateY(-1px);
}

.base-btn-secondary {
  background: var(--cf-bg-soft, #f5f5f5);
  color: var(--cf-text, #333);
}

.base-btn-danger {
  background: var(--cf-pink, #ff3b69);
  color: white;
}
</style>
