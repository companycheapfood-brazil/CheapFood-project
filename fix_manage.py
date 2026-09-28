import re

with open('src/views/merchant/ManageProductsView.vue', 'r', encoding='utf-8') as f:
    c = f.read()

# Add useToastStore
if 'useToastStore' not in c:
    c = c.replace("import { useMerchantStore } from '@/stores/useMerchantStore'", "import { useMerchantStore } from '@/stores/useMerchantStore'\nimport { useToastStore } from '@/stores/useToastStore'")
    c = c.replace("const merchantStore = useMerchantStore()", "const merchantStore = useMerchantStore()\nconst toast = useToastStore()")

c = c.replace('<button class="edit-btn">Editar</button>', '<button class="edit-btn" @click="toast.showToast(\'Edição de produto em breve!\', \'info\')">Editar</button>')
c = c.replace('<button v-else-if="p.status === \'vencido\'" class="action-btn discount">+Desc.</button>', '<button v-else-if="p.status === \'vencido\'" class="action-btn discount" @click="toast.showToast(\'Promoção extra em breve!\', \'info\')">+Desc.</button>')

with open('src/views/merchant/ManageProductsView.vue', 'w', encoding='utf-8') as f:
    f.write(c)
