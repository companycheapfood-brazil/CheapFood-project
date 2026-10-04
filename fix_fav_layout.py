import re

with open('src/components/ProductCard.vue', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the template price-row to restore original flow
old_template = """<div class="price-row" style="display:flex; justify-content:space-between; align-items:center; width: 100%">
        <div>
          <span class="price">R$ {{ product.price.toFixed(2).replace('.', ',') }}</span>
          <span v-if="product.old_price" class="original-price">
            R$ {{ product.old_price.toFixed(2).replace('.', ',') }}
          </span>
        </div>
        <button class="fav-btn" @click.stop="favoritesStore.toggleFavorite(product.id)">
          <svg v-if="favoritesStore.isFavorite(product.id)" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="#FF3B69" stroke="#FF3B69" stroke-width="2" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z\"/></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#bfa47a\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z\"/></svg>
        </button>
      </div>"""

new_template = """<div class="price-row">
        <span class="price">R$ {{ product.price.toFixed(2).replace('.', ',') }}</span>
        <span v-if="product.old_price" class="original-price">R$ {{ product.old_price.toFixed(2).replace('.', ',') }}</span>
        <button class="fav-btn" @click.stop="favoritesStore.toggleFavorite(product.id)">
          <svg v-if="favoritesStore.isFavorite(product.id)" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="#FF3B69" stroke="#FF3B69" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#bfa47a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
        </button>
      </div>"""

c = c.replace(old_template, new_template)

# Restore CSS for price-row
c = re.sub(r'\.price-row\s*\{[^}]*\}', '.price-row {\n  display: flex;\n  align-items: center;\n  gap: 6px;\n  margin-top: 4px;\n}', c)
c = re.sub(r'\.fav-btn\s*\{[^}]*\}', '.fav-btn {\n  background: none;\n  border: none;\n  cursor: pointer;\n  padding: 0;\n  margin-left: auto;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  transition: transform 0.2s;\n}', c)

with open('src/components/ProductCard.vue', 'w', encoding='utf-8') as f:
    f.write(c)
