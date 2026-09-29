with open('src/views/merchant/ManageProductsView.vue', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    '<button class="edit-btn" @click="toast.showToast(\'Edição de produto em breve!\', \'info\')">Editar</button>',
    '<button class="edit-btn" @click="$router.push(\'/comerciante/editar/\' + p.id)">Editar</button>'
)

with open('src/views/merchant/ManageProductsView.vue', 'w', encoding='utf-8') as f:
    f.write(c)
