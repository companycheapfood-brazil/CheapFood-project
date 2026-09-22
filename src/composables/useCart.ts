import { computed, reactive, readonly } from 'vue'
import type { CartItem, Product } from '@/types'
import { generateId } from '@/utils/helpers'

// Estado interno reativo
const state = reactive({
  items: [] as CartItem[],
  lastReservationCode: '',
})

/**
 * Adiciona um produto ao carrinho.
 */
function addToCart(product: Product, quantity = 1) {
  const existing = state.items.find((i) => i.product.id === product.id)
  if (existing) {
    existing.quantity += quantity
  } else {
    state.items.push({ product, quantity })
  }
}

/**
 * Atualiza a quantidade de um item.
 */
function updateQuantity(productId: string, delta: number) {
  const item = state.items.find((i) => i.product.id === productId)
  if (!item) return

  item.quantity += delta

  if (item.quantity <= 0) {
    removeFromCart(productId)
  }
}

/**
 * Remove um item do carrinho.
 */
function removeFromCart(productId: string) {
  const index = state.items.findIndex((i) => i.product.id === productId)
  if (index !== -1) {
    state.items.splice(index, 1)
  }
}

/**
 * Limpa o carrinho.
 */
function clearCart() {
  state.items = []
}

/**
 * Gera um código de reserva e limpa o carrinho.
 */
function checkout() {
  const code = generateId(4)
  state.lastReservationCode = code
  // clearCart() // Opcional: dependendo se quer limpar logo após gerar ou depois
  return code
}

// Getters calculados
const totalItems = computed(() => state.items.reduce((sum, i) => sum + i.quantity, 0))

const subtotal = computed(() => state.items.reduce((sum, i) => sum + i.product.price * i.quantity, 0))

const totalSavings = computed(() =>
  state.items.reduce((sum, i) => {
    const original = (i.product as any).old_price ?? i.product.price
    return sum + (original - i.product.price) * i.quantity
  }, 0),
)

export function useCart() {
  return {
    // Estado (somente leitura para o exterior)
    items: readonly(state.items),
    lastReservationCode: computed(() => state.lastReservationCode),

    // Getters
    totalItems,
    subtotal,
    totalSavings,

    // Ações
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart,
    checkout,
  }
}
