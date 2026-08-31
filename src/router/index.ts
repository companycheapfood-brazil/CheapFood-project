import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/produto/:id',
      name: 'produto',
      component: () => import('@/views/ProductView.vue'),
      props: true,
    },
    {
      path: '/carrinho',
      name: 'carrinho',
      component: () => import('@/views/CartView.vue'),
    },
    {
      path: '/comprovante',
      name: 'comprovante',
      component: () => import('@/views/ReceiptView.vue'),
    },
    {
      path: '/perfil',
      name: 'perfil',
      component: () => import('@/views/ProfileView.vue'),
    },
    {
      path: '/buscar',
      name: 'buscar',
      component: () => import('@/views/SearchView.vue'),
    },
    // ---------- Painel do lojista ----------
    {
      path: '/comerciante',
      name: 'merchant-dashboard',
      component: () => import('@/views/merchant/DashboardView.vue'),
    },
    {
      path: '/comerciante/novo',
      name: 'merchant-new',
      component: () => import('@/views/merchant/CreateProductView.vue'),
    },
    {
      path: '/comerciante/produtos',
      name: 'merchant-products',
      component: () => import('@/views/merchant/ManageProductsView.vue'),
    },
    {
      path: '/comerciante/pedidos',
      name: 'merchant-orders',
      component: () => import('@/views/merchant/OrdersView.vue'),
    },
    {
      path: '/comerciante/config',
      name: 'merchant-settings',
      component: () => import('@/views/merchant/SettingsView.vue'),
    },
  ],
})

export default router
