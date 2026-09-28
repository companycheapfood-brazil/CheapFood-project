import re

with open('src/views/merchant/OrderDetailView.vue', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix encoding
c = c.replace('CÃ“DIGO DE RETIRADA', 'CÓDIGO DE RETIRADA')
c = c.replace('mai/2026 Â· 4.8 â˜…', 'mai/2026 · 4.8 ★')
c = c.replace('26/05 Ã\xa0s 14:32', '26/05 às 14:32') # weird encoding
c = c.replace('Retira atÃ©', 'Retira até')

# Replace hardcoded values with dynamic
c = c.replace('<span class="detail-val price">R$2,49</span>', '<span class="detail-val price">R${{ order.price ? order.price.toFixed(2).replace(\'.\', \',\') : \'--\' }}</span>')
c = c.replace('<span class="detail-val">26/05 Ã\x83Â\xa0s 14:32</span>', '<span class="detail-val">{{ order.createdAt || \'--\' }}</span>')
c = c.replace('<span class="detail-val">26/05 às 14:32</span>', '<span class="detail-val">{{ order.createdAt || \'--\' }}</span>')

with open('src/views/merchant/OrderDetailView.vue', 'w', encoding='utf-8') as f:
    f.write(c)
