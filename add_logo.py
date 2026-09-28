import re

with open('src/components/merchant/MerchantHeader.vue', 'r', encoding='utf-8') as f:
    c = f.read()

new_template = """<template>
  <header class="merchant-header">
    <div class="logo-row">
      <svg class="cart-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M7 18C5.9 18 5.01 18.9 5.01 20C5.01 21.1 5.9 22 7 22C8.1 22 9 21.1 9 20C9 18.9 8.1 18 7 18ZM1 2V4H3L6.6 11.59L5.24 14.04C5.09 14.32 5 14.65 5 15C5 16.1 5.9 17 7 17H19V15H7.42C7.28 15 7.17 14.89 7.17 14.75L7.2 14.63L8.1 13H15.55C16.3 13 16.96 12.59 17.3 11.97L20.88 5.48C20.95 5.34 21 5.17 21 5C21 4.45 20.55 4 20 4H5.21L4.27 2H1ZM17 18C15.9 18 15.01 18.9 15.01 20C15.01 21.1 15.9 22 17 22C18.1 22 19 21.1 19 20C19 18.9 18.1 18 17 18Z" fill="#ffffff"/>
      </svg>
      <span class="logo-text">Cheap<span class="logo-text-highlight">Food</span> <span class="badge">Lojista</span></span>
    </div>
    <div class="header-titles">
      <h1 class="title">{{ title }}</h1>
      <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
    </div>
  </header>
</template>"""

c = re.sub(r'<template>.*?</template>', new_template, c, flags=re.DOTALL)

css_addition = """
.logo-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 20px;
}

.cart-icon {
  width: 22px;
  height: 22px;
}

.logo-text {
  font-size: 18px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.5px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.logo-text-highlight {
  color: var(--cf-primary);
}

.badge {
  background-color: rgba(255, 255, 255, 0.2);
  padding: 2px 6px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.header-titles {
  display: flex;
  flex-direction: column;
}
"""

c = c.replace('</style>', css_addition + '\n</style>')

with open('src/components/merchant/MerchantHeader.vue', 'w', encoding='utf-8') as f:
    f.write(c)
