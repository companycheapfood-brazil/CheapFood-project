import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import type { CartItem, Product } from '@/types'
import { generateId } from '@/utils/helpers'
import { useToastStore } from './useToastStore'

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])
  const lastReservationCode = ref('')
  
  const toastStore = useToastStore()

  function addToCart(product: Product, quantity = 1) {
    const existing = items.value.find((i) => i.product.id === product.id)
    if (existing) {
      existing.quantity += quantity
    } else {
      items.value.push({ product, quantity })
    }
    toastStore.addToast('Produto adicionado ao carrinho!', 'success')
  }

  function updateQuantity(productId: string, delta: number) {
    const item = items.value.find((i) => i.product.id === productId)
    if (!item) return

    item.quantity += delta

    if (item.quantity <= 0) {
      removeFromCart(productId)
    }
  }

  function removeFromCart(productId: string) {
    const index = items.value.findIndex((i) => i.product.id === productId)
    if (index !== -1) {
      items.value.splice(index, 1)
      toastStore.addToast('Produto removido', 'info')
    }
  }

  function clearCart() {
    items.value = []
  }

  async function checkout() {
    try {
      const payload = {
        items: items.value.map(i => ({ id: i.product.id, quantity: i.quantity }))
      }
      const res = await fetch('http://localhost:5000/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (res.ok) {
        const data = await res.json()
        lastReservationCode.value = data.code
        return data.code
      }
    } catch (e) {
      console.error(e)
    }
    const code = generateId(4)
    lastReservationCode.value = code
    return code
  }

  const totalItems = computed(() => items.value.reduce((sum, i) => sum + i.quantity, 0))

  const subtotal = computed(() => items.value.reduce((sum, i) => sum + i.product.price * i.quantity, 0))

  const totalSavings = computed(() =>
    items.value.reduce((sum, i) => {
      const original = (i.product as any).old_price ?? i.product.price
      return sum + (original - i.product.price) * i.quantity
    }, 0),
  )

  return {
    items,
    lastReservationCode,
    totalItems,
    subtotal,
    totalSavings,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart,
    checkout,
  }
})
