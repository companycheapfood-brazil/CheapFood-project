import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/shop/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/start',
      name: 'start',
      component: () => import('@/views/auth/StartView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/auth/RegisterView.vue'),
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('@/views/auth/ForgotPasswordView.vue'),
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: () => import('@/views/auth/ResetPasswordView.vue'),
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/produto/:id',
      name: 'produto',
      component: () => import('@/views/shop/ProductView.vue'),
      props: true,
    },
    {
      path: '/carrinho',
      name: 'carrinho',
      component: () => import('@/views/shop/CartView.vue'),
    },
    {
      path: '/comprovante',
      name: 'comprovante',
      component: () => import('@/views/shop/ReceiptView.vue'),
    },
    {
      path: '/perfil',
      name: 'perfil',
      component: () => import('@/views/profile/ProfileView.vue'),
    },
    {
      path: '/perfil/editar',
      name: 'perfil-editar',
      component: () => import('@/views/profile/EditProfileView.vue'),
    },
    {
      path: '/perfil/historico',
      name: 'perfil-historico',
      component: () => import('@/views/profile/HistoryView.vue'),
    },
    {
      path: '/perfil/ajuda',
      name: 'perfil-ajuda',
      component: () => import('@/views/profile/HelpView.vue'),
    },
    {
      path: '/perfil/termos',
      name: 'perfil-termos',
      component: () => import('@/views/profile/TermsView.vue'),
    },
    {
      path: '/perfil/excluir',
      name: 'perfil-excluir',
      component: () => import('@/views/profile/DeleteAccountView.vue'),
    },
    {
      path: '/buscar',
      name: 'buscar',
      component: () => import('@/views/shop/SearchView.vue'),
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
      path: '/comerciante/pedidos/:orderId',
      name: 'merchant-order-detail',
      component: () => import('@/views/merchant/OrderDetailView.vue'),
      props: true,
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
    {
      path: '/comerciante/historico',
      name: 'merchant-history',
      component: () => import('@/views/merchant/MerchantHistoryView.vue'),
    },
    {
      path: '/comerciante/planos',
      name: 'merchant-plans',
      component: () => import('@/views/merchant/PlansView.vue'),
    },
    {
      path: '/perfil/planos',
      name: 'perfil-planos',
      component: () => import('@/views/merchant/PlansView.vue'),
    },
  ],
})

router.beforeEach((to, from, next) => {
  const publicPages = ['/start', '/login', '/register', '/forgot-password', '/reset-password']
  const authRequired = !publicPages.includes(to.path)
  const loggedIn = localStorage.getItem('user')

  if (authRequired && !loggedIn) {
    return next('/start')
  }

  next()
})

export default router
