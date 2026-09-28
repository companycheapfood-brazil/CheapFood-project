<script setup lang="ts">
import ToastContainer from '@/components/ui/ToastContainer.vue'
</script>

<template>
  <div class="app-shell">
    <ToastContainer />
    <router-view v-slot="{ Component }">
      <transition name="page" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<style>
.app-shell {
  min-height: 100vh;
  background: var(--cf-bg);
  overflow-x: hidden;
}

.page-enter-active,
.page-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateX(10px);
}

.page-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}
</style>
