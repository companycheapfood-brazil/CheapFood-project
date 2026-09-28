with open('src/views/merchant/OrdersView.vue', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('@click="confirmPickup(order.id)"', '@click.stop="confirmPickup(order.id)"')
c = c.replace('@click="cancelOrder(order.id)"', '@click.stop="cancelOrder(order.id)"')

with open('src/views/merchant/OrdersView.vue', 'w', encoding='utf-8') as f:
    f.write(c)
