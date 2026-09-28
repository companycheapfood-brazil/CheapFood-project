<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import MerchantHeader from '@/components/merchant/MerchantHeader.vue'
import MerchantBottomNav from '@/components/merchant/MerchantBottomNav.vue'
import { useMerchantStore } from '@/stores/useMerchantStore'
import type { MerchantProduct } from '@/types'

const router = useRouter()
const merchantStore = useMerchantStore()
const { addProduct } = merchantStore

const categories = ['Laticínios', 'Padaria', 'Hortifruti', 'Bebidas', 'Mercearia']

const name = ref('')
const category = ref('')
const validity = ref('')
const originalPrice = ref<number | null>(null)
const promoPrice = ref<number | null>(null)
const quantity = ref<number | null>(null)

const imageFile = ref<File | null>(null)

function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    imageFile.value = target.files[0]
  }
}

const discountPercent = computed(() => {
  if (!originalPrice.value || !promoPrice.value || originalPrice.value <= 0) return 0
  const pct = ((originalPrice.value - promoPrice.value) / originalPrice.value) * 100
  return Math.max(0, Math.round(pct))
})

const canPublish = computed(
  () =>
    name.value.trim() !== '' &&
    category.value !== '' &&
    validity.value !== '' &&
    !!originalPrice.value &&
    !!promoPrice.value &&
    !!quantity.value,
)

async function publish() {
  if (!canPublish.value) return

  const formData = new FormData()
  formData.append('nome', name.value.trim())
  formData.append('categoria', category.value)
  formData.append('data_validade', validity.value)
  formData.append('preco_original', originalPrice.value!.toString())
  formData.append('preco_desconto', promoPrice.value!.toString())
  formData.append('quantidade', quantity.value!.toString())
  
  if (imageFile.value) {
    formData.append('imagem', imageFile.value)
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/api/products', {
      method: 'POST',
      body: formData
    })
    
    if (response.ok) {
      const data = await response.json()
      
      const newProduct: MerchantProduct = {
        id: data.id,
        name: data.name,
        category: data.category,
        icon: data.icon,
        originalPrice: data.originalPrice,
        promoPrice: data.price,
        quantityAvailable: data.quantity,
        reservedCount: 0,
        validity: data.validity,
        expiresLabel: data.expiresLabel,
        status: 'ativo',
        paused: false,
      }
      
      addProduct(newProduct)
      router.push('/comerciante/produtos')
    } else {
      console.error('Erro ao cadastrar produto:', await response.text())
      alert('Erro ao cadastrar produto')
    }
  } catch (err) {
    console.error('Erro na requisição', err)
    alert('Erro de conexão com o servidor')
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
