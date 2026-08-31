<script setup lang="ts">
defineProps<{
  title: string
  subtitle?: string
}>()
</script>

<template>
  <header class="merchant-header">
    <h1 class="title">{{ title }}</h1>
    <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
  </header>
</template>

<style scoped>
.merchant-header {
  background: linear-gradient(135deg, var(--mc-purple) 0%, #b8b3f7 100%);
  padding: 20px 18px;
  border-radius: 0 0 var(--cf-radius-lg) var(--cf-radius-lg);
  flex-shrink: 0;
}

.title {
  font-size: 17px;
  font-weight: 800;
  color: #ffffff;
}

.subtitle {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.85);
  margin-top: 2px;
}
</style>
