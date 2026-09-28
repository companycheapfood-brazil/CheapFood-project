import re

with open('src/components/ProductCard.vue', 'r', encoding='utf-8') as f:
    c = f.read()

# Add the store import
script_setup_regex = re.compile(r'<script setup lang="ts">(.*?)</script>', re.DOTALL)
m = script_setup_regex.search(c)
if m:
    script_content = m.group(1)
    if 'useFavoritesStore' not in script_content:
        new_script = script_content + '\nimport { useFavoritesStore } from \'@/stores/useFavoritesStore\'\nconst favoritesStore = useFavoritesStore()\n'
        c = c.replace(script_content, new_script)

# Add the heart icon to the template
old_template_part = """<div class="price-row">
        <p class="price">R${{ p.price.toFixed(2).replace('.', ',') }} <span class="original">R${{ p.originalPrice.toFixed(2).replace('.', ',') }}</span></p>
      </div>"""

new_template_part = """<div class="price-row">
        <p class="price">R${{ p.price.toFixed(2).replace('.', ',') }} <span class="original">R${{ p.originalPrice.toFixed(2).replace('.', ',') }}</span></p>
        <button class="fav-btn" @click.stop="favoritesStore.toggleFavorite(p.id)">
          <svg v-if="favoritesStore.isFavorite(p.id)" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="#FF3B69" stroke="#FF3B69" stroke-width="2" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z\"/></svg>
          <svg v-else xmlns=\"http://www.w3.org/2000/svg\" width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#bfa47a\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z\"/></svg>
        </button>
      </div>"""

c = c.replace(old_template_part, new_template_part)

# Add CSS
css = """
.price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.fav-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s;
}
.fav-btn:active {
  transform: scale(0.8);
}
"""

if '.fav-btn' not in c:
    c = c.replace('</style>', css + '\n</style>')

with open('src/components/ProductCard.vue', 'w', encoding='utf-8') as f:
    f.write(c)
