with open('src/views/merchant/DashboardView.vue', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix the subtitle prop
c = c.replace('subtitle="ltimos 7 dias"', 'subtitle="Últimos 7 dias"')

with open('src/views/merchant/DashboardView.vue', 'w', encoding='utf-8') as f:
    f.write(c)
