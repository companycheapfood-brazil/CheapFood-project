<script setup lang="ts">
import { useToastStore } from '@/stores/useToastStore'
import { storeToRefs } from 'pinia'

const toastStore = useToastStore()
const { toasts } = storeToRefs(toastStore)
</script>

<template>
  <div class="toast-container">
    <TransitionGroup name="toast-list">
      <div 
        v-for="toast in toasts" 
        :key="toast.id" 
        class="toast"
        :class="toast.type"
      >
        <span class="icon" v-if="toast.type === 'success'">✅</span>
        <span class="icon" v-else-if="toast.type === 'error'">🚨</span>
        <span class="icon" v-else>ℹ️</span>
        <span class="message">{{ toast.message }}</span>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  z-index: 9999;
  pointer-events: none;
  width: 90%;
  max-width: 400px;
}

.toast {
  background: white;
  color: #333;
  padding: 12px 20px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  font-size: 14px;
  pointer-events: auto;
}

.toast.success { border-left: 4px solid #1f8a4c; }
.toast.error { border-left: 4px solid #d92d3f; }
.toast.info { border-left: 4px solid #f5a623; }

.toast-list-enter-active,
.toast-list-leave-active {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.toast-list-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.toast-list-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
