with open('src/views/merchant/DashboardView.vue', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('{{ Math.floor(Math.random() * 12) + 5 }}%', '14%')

with open('src/views/merchant/DashboardView.vue', 'w', encoding='utf-8') as f:
    f.write(c)
