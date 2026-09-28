import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import type { MerchantProduct, Order } from '@/types'
import { useToastStore } from './useToastStore'

export const useMerchantStore = defineStore('merchant', () => {
  const products = ref<MerchantProduct[]>([])
  const orders = ref<Order[]>([])
  const stats = ref({
    revenueRecovered: 0,
    activeProducts: 0,
    expiringSoon: 0,
    reservations: 0,
    dailySales: [] as {label: string, value: number}[]
  })
  
  const toastStore = useToastStore()
  
  async function fetchDashboardStats() {
    try {
      const res = await fetch('http://localhost:5000/api/merchant/stats')
      stats.value = await res.json()
    } catch (e) {
      console.error(e)
    }
  }
  
  async function fetchProducts() {
    try {
      const res = await fetch('http://localhost:5000/api/merchant/products')
      products.value = await res.json()
    } catch (e) {
      console.error(e)
    }
  }
  
  async function fetchOrders() {
    try {
      const res = await fetch('http://localhost:5000/api/merchant/orders')
      orders.value = await res.json()
    } catch (e) {
      console.error(e)
    }
  }

  async function togglePause(id: string) {
    try {
      const res = await fetch(`http://localhost:5000/api/merchant/products/${id}/pause`, { method: 'PATCH' })
      if (res.ok) {
        const product = products.value.find((p) => p.id === id)
        if (product) {
          product.paused = !product.paused
          product.status = product.paused ? 'pausado' : 'ativo'
          toastStore.addToast(`Produto ${product.paused ? 'pausado' : 'reativado'}`, 'info')
        }
      }
    } catch (e) {
      console.error(e)
    }
  }

  function addProduct(product: MerchantProduct) {
    products.value.unshift(product)
  }

  async function confirmPickup(orderId: string) {
    try {
      const res = await fetch(`http://localhost:5000/api/merchant/orders/${orderId}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: 'retirado' })
      })
      if (res.ok) {
        const order = orders.value.find((o) => o.id === orderId)
        if (order) {
          order.status = 'retirado'
          toastStore.addToast('Retirada confirmada com sucesso', 'success')
        }
      }
    } catch (e) {}
  }

  async function cancelOrder(orderId: string) {
    try {
      const res = await fetch(`http://localhost:5000/api/merchant/orders/${orderId}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: 'expirado' })
      })
      if (res.ok) {
        const order = orders.value.find((o) => o.id === orderId)
        if (order) {
          order.status = 'expirado'
          toastStore.addToast('Pedido cancelado', 'error')
        }
      }
    } catch (e) {}
  }

  const activeProducts = computed(() => products.value.filter((p) => p.status === 'ativo'))
  const expiredProducts = computed(() => products.value.filter((p) => p.status === 'vencido'))
  const soldProducts = computed(() => products.value.filter((p) => p.status === 'vendido'))

  const pendingOrders = computed(() => orders.value.filter((o) => o.status === 'pendente'))
  const pickedUpOrders = computed(() => orders.value.filter((o) => o.status === 'retirado'))
  const expiredOrders = computed(() => orders.value.filter((o) => o.status === 'expirado'))

  return {
    products,
    orders,
    stats,
    activeProducts,
    expiredProducts,
    soldProducts,
    pendingOrders,
    pickedUpOrders,
    expiredOrders,
    fetchDashboardStats,
    fetchProducts,
    fetchOrders,
    togglePause,
    addProduct,
    confirmPickup,
    cancelOrder,
  }
})
