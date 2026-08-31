import { computed, reactive } from 'vue'
import type { CartItem, Product } from '@/types'

// Estado reativo único, compartilhado por todos os componentes que
// importarem este composable (padrão "store" simples sem Pinia).
const items = reactive<CartItem[]>([])
const lastReservationCode = reactive({ value: '' })

function addToCart(product: Product, quantity = 1) {
  const existing = items.find((i) => i.product.id === product.id)
  if (existing) {
    existing.quantity += quantity
  } else {
    items.push({ product, quantity })
  }
}

function updateQuantity(productId: string, delta: number) {
  const item = items.find((i) => i.product.id === productId)
  if (!item) return
  item.quantity += delta
  if (item.quantity <= 0) {
    removeFromCart(productId)
  }
}

function removeFromCart(productId: string) {
  const index = items.findIndex((i) => i.product.id === productId)
  if (index !== -1) items.splice(index, 1)
}

function clearCart() {
  items.splice(0, items.length)
}

function generateReservationCode() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
  let code = ''
  for (let i = 0; i < 4; i++) {
    code += chars[Math.floor(Math.random() * chars.length)]
  }
  lastReservationCode.value = code
  return code
}

const totalItems = computed(() => items.reduce((sum, i) => sum + i.quantity, 0))

const subtotal = computed(() =>
  items.reduce((sum, i) => sum + i.product.price * i.quantity, 0),
)

const totalSavings = computed(() =>
  items.reduce((sum, i) => {
    const original = i.product.originalPrice ?? i.product.price
    return sum + (original - i.product.price) * i.quantity
  }, 0),
)

export function useCart() {
  return {
    items,
    totalItems,
    subtotal,
    totalSavings,
    lastReservationCode,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart,
    generateReservationCode,
  }
}
