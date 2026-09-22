import { computed, reactive, readonly } from 'vue'
import { merchantProducts as initialProducts, orders as initialOrders } from '@/data/merchant'
import type { MerchantProduct, Order } from '@/types'

// Estado interno reativo
const state = reactive({
  products: [...initialProducts],
  orders: [...initialOrders],
})

/**
 * Alterna o estado de pausa de um produto.
 */
function togglePause(id: string) {
  const product = state.products.find((p) => p.id === id)
  if (product) {
    product.paused = !product.paused
  }
}

/**
 * Adiciona um novo produto.
 */
function addProduct(product: MerchantProduct) {
  state.products.unshift(product)
}

/**
 * Confirma a retirada de um pedido.
 */
function confirmPickup(orderId: string) {
  const order = state.orders.find((o) => o.id === orderId)
  if (order) {
    order.status = 'retirado'
  }
}

/**
 * Cancela um pedido (expirado).
 */
function cancelOrder(orderId: string) {
  const order = state.orders.find((o) => o.id === orderId)
  if (order) {
    order.status = 'expirado'
  }
}

// Getters calculados
const activeProducts = computed(() => state.products.filter((p) => p.status === 'ativo'))
const expiredProducts = computed(() => state.products.filter((p) => p.status === 'vencido'))
const soldProducts = computed(() => state.products.filter((p) => p.status === 'vendido'))

const pendingOrders = computed(() => state.orders.filter((o) => o.status === 'pendente'))
const pickedUpOrders = computed(() => state.orders.filter((o) => o.status === 'retirado'))
const expiredOrders = computed(() => state.orders.filter((o) => o.status === 'expirado'))

export function useMerchant() {
  return {
    // Estado (readonly)
    products: readonly(state.products),
    orders: readonly(state.orders),

    // Getters
    activeProducts,
    expiredProducts,
    soldProducts,
    pendingOrders,
    pickedUpOrders,
    expiredOrders,

    // Ações
    togglePause,
    addProduct,
    confirmPickup,
    cancelOrder,
  }
}
