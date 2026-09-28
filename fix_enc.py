with open('src/views/merchant/DashboardView.vue', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('tilmos', 'Últimos')
c = c.replace('â€” adicione promoÃ§Ãµes!', '— adicione promoções!')
c = c.replace('Ãšltimos', 'Últimos')

with open('src/views/merchant/DashboardView.vue', 'w', encoding='utf-8') as f:
    f.write(c)
