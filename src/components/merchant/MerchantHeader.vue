<script setup lang="ts">
defineProps<{
  title: string
  subtitle?: string
}>()
</script>

<template>
  <header class="merchant-header">
    <div class="logo-row">
      <svg class="cart-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M7 18C5.9 18 5.01 18.9 5.01 20C5.01 21.1 5.9 22 7 22C8.1 22 9 21.1 9 20C9 18.9 8.1 18 7 18ZM1 2V4H3L6.6 11.59L5.24 14.04C5.09 14.32 5 14.65 5 15C5 16.1 5.9 17 7 17H19V15H7.42C7.28 15 7.17 14.89 7.17 14.75L7.2 14.63L8.1 13H15.55C16.3 13 16.96 12.59 17.3 11.97L20.88 5.48C20.95 5.34 21 5.17 21 5C21 4.45 20.55 4 20 4H5.21L4.27 2H1ZM17 18C15.9 18 15.01 18.9 15.01 20C15.01 21.1 15.9 22 17 22C18.1 22 19 21.1 19 20C19 18.9 18.1 18 17 18Z" fill="#ffffff"/>
      </svg>
      <span class="logo-text">Cheap<span class="logo-highlight">Food</span></span>
      <span class="badge">Lojista</span>
    </div>
    <div class="header-titles">
      <h1 class="title">{{ title }}</h1>
      <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
    </div>
  </header>
</template>

<style scoped>
.merchant-header {
  background: linear-gradient(135deg, var(--mc-purple) 0%, #b8b3f7 100%);
  padding: 24px 18px 20px 18px;
  border-radius: 0 0 var(--cf-radius-lg) var(--cf-radius-lg);
  flex-shrink: 0;
}

.logo-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.cart-icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
}

.logo-text {
  font-size: 17px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.3px;
  line-height: 1;
}

.logo-highlight {
  color: #f7b657;
}

.badge {
  background-color: rgba(255, 255, 255, 0.2);
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #ffffff;
  line-height: 1;
}

.header-titles {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.title {
  font-size: 17px;
  font-weight: 800;
  color: #ffffff;
  margin: 0;
}

.subtitle {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.85);
  margin: 0;
}
</style>
