<script setup lang="ts">
import { ref, onMounted } from 'vue'
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
}
</script>

<template>
  <div class="screen">
    <MerchantHeader title="Cadastrar produto" />

    <main class="content">
      <form class="form" @submit.prevent="publish">
        <label class="field">
          <span class="field-label">Nome do produto</span>
          <input v-model="name" type="text" placeholder="Ex: Leite Integral 1L" />
        </label>

        <label class="field">
          <span class="field-label">Categoria</span>
          <select v-model="category">
            <option value="" disabled>Selecione</option>
            <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
          </select>
        </label>

        <label class="field">
          <span class="field-label">Imagem do produto</span>
          <input type="file" @change="handleFileChange" accept="image/*" />
        </label>

        <label class="field">
          <span class="field-label">Data de validade</span>
          <input v-model="validity" type="text" placeholder="DD/MM/AAAA" />
        </label>

        <label class="field">
          <span class="field-label">Preço original (R$)</span>
          <input v-model.number="originalPrice" type="number" min="0" step="0.01" placeholder="4,99" />
        </label>

        <label class="field">
          <span class="field-label">Preço promocional (R$)</span>
          <input v-model.number="promoPrice" type="number" min="0" step="0.01" placeholder="2,49" />
        </label>

        <label class="field">
          <span class="field-label">Quantidade disponível</span>
          <input v-model.number="quantity" type="number" min="0" step="1" placeholder="10" />
        </label>

        <div class="discount-card">
          <span>Desconto calculado</span>
          <span class="discount-value">{{ discountPercent }}% OFF</span>
        </div>

        <button type="submit" class="publish-btn" :disabled="!canPublish">Publicar oferta</button>
      </form>
    </main>

    <MerchantBottomNav />
  </div>
</template>

<style scoped>
.screen {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--mc-bg);
  color: var(--mc-text);
}

.content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--mc-text);
}

.field input,
.field select {
  background: var(--mc-cream);
  border: 1px solid var(--mc-cream-border);
  border-radius: var(--cf-radius-sm);
  padding: 12px 14px;
  font-size: 13px;
  color: var(--mc-text);
  outline: none;
}

.field input::placeholder {
  color: #b8a67a;
}

.discount-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--mc-cream);
  border: 1px dashed var(--mc-cream-border);
  border-radius: var(--cf-radius-sm);
  padding: 12px 14px;
  font-size: 12px;
  font-weight: 600;
  color: var(--mc-text);
}

.discount-value {
  color: var(--cf-orange-soft);
  font-size: 14px;
  font-weight: 800;
}

.publish-btn {
  background: var(--mc-navy);
  color: #ffffff;
  border: none;
  border-radius: var(--cf-radius-sm);
  padding: 15px;
  font-size: 14px;
  font-weight: 700;
  margin-top: 4px;
}

.publish-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
