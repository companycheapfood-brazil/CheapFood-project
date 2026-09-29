import re

with open('src/views/merchant/EditProductView.vue', 'r', encoding='utf-8') as f:
    c = f.read()

# Change title
c = c.replace('MerchantHeader title="Novo Produto"', 'MerchantHeader title="Editar Produto"')
c = c.replace('Adicionar Produto', 'Salvar Alterações')

# Script updates
script_update = """import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import MerchantHeader from '@/components/merchant/MerchantHeader.vue'
import MerchantBottomNav from '@/components/merchant/MerchantBottomNav.vue'
import { useToastStore } from '@/stores/useToastStore'
import { useMerchantStore } from '@/stores/useMerchantStore'

const router = useRouter()
const route = useRoute()
const toast = useToastStore()
const merchantStore = useMerchantStore()

const productId = route.params.id

const form = ref({
  nome: '',
  descricao: '',
  categoria: 'Padaria',
  preco_original: '',
  preco_desconto: '',
  quantidade: '',
  data_validade: ''
})

const file = ref<File | null>(null)
const previewUrl = ref<string | null>(null)
const isLoading = ref(false)

onMounted(async () => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/api/products/${productId}`)
    if (res.ok) {
      const data = await res.json()
      form.value = {
        nome: data.nome,
        descricao: data.descricao || '',
        categoria: data.categoria,
        preco_original: data.preco_original,
        preco_desconto: data.preco_desconto,
        quantidade: data.quantidade,
        data_validade: data.data_validade
      }
      if (data.imagem) {
        previewUrl.value = data.imagem.startsWith('http') ? data.imagem : `http://127.0.0.1:5000${data.imagem}`
      }
    }
  } catch(e) {
    toast.showToast('Erro ao carregar produto', 'error')
  }
})

function handleFile(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    file.value = target.files[0]
    previewUrl.value = URL.createObjectURL(file.value)
  }
}

async function saveProduct() {
  isLoading.value = true
  try {
    const formData = new FormData()
    formData.append('nome', form.value.nome)
    formData.append('descricao', form.value.descricao)
    formData.append('categoria', form.value.categoria)
    formData.append('preco_original', form.value.preco_original)
    formData.append('preco_desconto', form.value.preco_desconto)
    formData.append('quantidade', form.value.quantidade)
    formData.append('data_validade', form.value.data_validade)
    
    if (file.value) {
      formData.append('image', file.value)
    }

    const res = await fetch(`http://127.0.0.1:5000/api/products/${productId}`, {
      method: 'PUT',
      body: formData
    })

    if (res.ok) {
      merchantStore.fetchProducts()
      toast.showToast('Produto atualizado com sucesso!', 'success')
      router.push('/comerciante/produtos')
    } else {
      toast.showToast('Erro ao atualizar produto', 'error')
    }
  } catch(e) {
    console.error(e)
    toast.showToast('Erro de conexão', 'error')
  } finally {
    isLoading.value = false
  }
}"""

# Replace script block
c = re.sub(r'<script setup lang="ts">.*?</script>', '<script setup lang="ts">\n' + script_update + '\n</script>', c, flags=re.DOTALL)

with open('src/views/merchant/EditProductView.vue', 'w', encoding='utf-8') as f:
    f.write(c)
