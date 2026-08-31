<script setup lang="ts">
// App.vue agora só define o "frame" do app mobile.
// Cada tela cuida do próprio header e da BottomNav.
</script>

<template>
  <div class="app-shell">
    <RouterView />
  </div>
</template>

<style>
.app-shell {
  min-height: 100vh;
  background: var(--cf-bg);
}
</style>
