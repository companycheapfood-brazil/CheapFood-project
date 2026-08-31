import { computed, reactive } from 'vue'
import { merchantProducts as initialProducts, orders as initialOrders } from '@/data/merchant'
import type { MerchantProduct, Order } from '@/types'

const products = reactive<MerchantProduct[]>([...initialProducts])
const merchantOrders = reactive<Order[]>([...initialOrders])

function togglePause(id: string) {
  const product = products.find((p) => p.id === id)
  if (product) product.paused = !product.paused
}

function addProduct(product: MerchantProduct) {
  products.unshift(product)
}

function confirmPickup(orderId: string) {
  const order = merchantOrders.find((o) => o.id === orderId)
  if (order) order.status = 'retirado'
}

function cancelOrder(orderId: string) {
  const order = merchantOrders.find((o) => o.id === orderId)
  if (order) order.status = 'expirado'
}

const activeProducts = computed(() => products.filter((p) => p.status === 'ativo'))
const expiredProducts = computed(() => products.filter((p) => p.status === 'vencido'))
const soldProducts = computed(() => products.filter((p) => p.status === 'vendido'))

const pendingOrders = computed(() => merchantOrders.filter((o) => o.status === 'pendente'))
const pickedUpOrders = computed(() => merchantOrders.filter((o) => o.status === 'retirado'))
const expiredOrders = computed(() => merchantOrders.filter((o) => o.status === 'expirado'))

export function useMerchant() {
  return {
    products,
    activeProducts,
    expiredProducts,
    soldProducts,
    togglePause,
    addProduct,
    merchantOrders,
    pendingOrders,
    pickedUpOrders,
    expiredOrders,
    confirmPickup,
    cancelOrder,
  }
}
