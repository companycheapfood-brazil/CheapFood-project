import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/shop/HomeView.vue";
import { normalizeUserRole } from "@/utils/auth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/start",
      name: "start",
      component: () => import("@/views/auth/StartView.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("@/views/auth/LoginView.vue"),
    },
    {
      path: "/register",
      name: "register",
      component: () => import("@/views/auth/RegisterView.vue"),
    },
    {
      path: "/forgot-password",
      name: "forgot-password",
      component: () => import("@/views/auth/ForgotPasswordView.vue"),
    },
    {
      path: "/reset-password",
      name: "reset-password",
      component: () => import("@/views/auth/ResetPasswordView.vue"),
    },
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/produto/:id",
      name: "produto",
      component: () => import("@/views/shop/ProductView.vue"),
      props: true,
    },
    {
      path: "/carrinho",
      name: "carrinho",
      component: () => import("@/views/shop/CartView.vue"),
    },
    {
      path: "/comprovante",
      name: "comprovante",
      component: () => import("@/views/shop/ReceiptView.vue"),
    },
    {
      path: "/perfil",
      name: "perfil",
      component: () => import("@/views/profile/ProfileView.vue"),
    },
    {
      path: "/perfil/editar",
      name: "perfil-editar",
      component: () => import("@/views/profile/EditProfileView.vue"),
    },
    {
      path: "/perfil/favoritos",
      name: "perfil-favoritos",
      component: () => import("@/views/profile/FavoritesView.vue"),
    },
    {
      path: "/perfil/historico",
      name: "perfil-historico",
      component: () => import("@/views/profile/HistoryView.vue"),
    },
    {
      path: "/perfil/ajuda",
      name: "perfil-ajuda",
      component: () => import("@/views/profile/HelpView.vue"),
    },
    {
      path: "/perfil/termos",
      name: "perfil-termos",
      component: () => import("@/views/profile/TermsView.vue"),
    },
    {
      path: "/perfil/excluir",
      name: "perfil-excluir",
      component: () => import("@/views/profile/DeleteAccountView.vue"),
    },
    {
      path: "/buscar",
      name: "buscar",
      component: () => import("@/views/shop/SearchView.vue"),
    },
    // ---------- Painel do lojista ----------
    {
      path: "/comerciante",
      name: "merchant-dashboard",
      component: () => import("@/views/merchant/DashboardView.vue"),
    },
    {
      path: "/comerciante/novo",
      name: "merchant-new",
      component: () => import("@/views/merchant/CreateProductView.vue"),
    },
    {
      path: "/comerciante/editar/:id",
      name: "merchant-edit",
      component: () => import("@/views/merchant/EditProductView.vue"),
    },
    {
      path: "/comerciante/produtos",
      name: "merchant-products",
      component: () => import("@/views/merchant/ManageProductsView.vue"),
    },
    {
      path: "/comerciante/pedidos/:orderId",
      name: "merchant-order-detail",
      component: () => import("@/views/merchant/OrderDetailView.vue"),
      props: true,
    },
    {
      path: "/comerciante/pedidos",
      name: "merchant-orders",
      component: () => import("@/views/merchant/OrdersView.vue"),
    },
    {
      path: "/comerciante/config",
      name: "merchant-settings",
      component: () => import("@/views/merchant/SettingsView.vue"),
    },
    {
      path: "/comerciante/historico",
      name: "merchant-history",
      component: () => import("@/views/merchant/MerchantHistoryView.vue"),
    },
    {
      path: "/comerciante/planos",
      name: "merchant-plans",
      component: () => import("@/views/merchant/PlansView.vue"),
    },
    {
      path: "/perfil/planos",
      redirect: "/perfil",
    },
    {
      path: "/historico",
      redirect: "/perfil/historico",
    },
    {
      path: "/ajuda",
      redirect: "/perfil/ajuda",
    },
    {
      path: "/termos",
      redirect: "/perfil/termos",
    },
    {
      path: "/favoritos",
      redirect: "/perfil/favoritos",
    },
    {
      path: "/:pathMatch(.*)*",
      redirect: "/",
    },
  ],
});

router.beforeEach((to, _from, next) => {
  const publicPages = [
    "/start",
    "/login",
    "/register",
    "/forgot-password",
    "/reset-password",
  ];
  const normalizedPath = to.path.length > 1 ? to.path.replace(/\/+$/, "") : to.path;
  const authRequired = !publicPages.includes(normalizedPath);

  const userStr = localStorage.getItem("user");
  let user: any = null;
  if (userStr) {
    try {
      const parsed = JSON.parse(userStr);
      const candidate = parsed?.user || parsed;
      if (parsed && parsed.token && candidate && candidate.id != null) {
        user = candidate;
      } else {
        localStorage.removeItem("user");
      }
    } catch {
      localStorage.removeItem("user");
    }
  }

  if (authRequired && !user) {
    return next("/start");
  }

  // Controle de Acesso por Tipo de Perfil (CLIENTE vs COMERCIANTE)
  if (user) {
    const role = normalizeUserRole(user);
    const isMerchantRoute = normalizedPath.startsWith("/comerciante");
    const isPublic = publicPages.includes(normalizedPath);

    // Se logado e tentar acessar login/start, redireciona para a área do perfil
    if (isPublic) {
      return next(role === "merchant" ? "/comerciante" : "/");
    }

    if (isMerchantRoute && role !== "merchant") {
      return next("/");
    }

    // Lojista não deve navegar nas telas de compra, favoritos ou histórico do consumidor
    const isConsumerRoute =
      normalizedPath === "/" ||
      normalizedPath.startsWith("/produto") ||
      normalizedPath.startsWith("/carrinho") ||
      normalizedPath.startsWith("/buscar") ||
      normalizedPath.startsWith("/comprovante") ||
      normalizedPath === "/perfil/favoritos" ||
      normalizedPath === "/perfil/historico";

    if (isConsumerRoute && role === "merchant") {
      return next("/comerciante");
    }
  }

  next();
});

router.onError((err) => {
  const msg = String(err?.message || "");
  if (
    msg.includes("Failed to fetch dynamically imported module") ||
    msg.includes("Importing a module script failed")
  ) {
    const key = "cf_router_chunk_reloaded";
    if (!sessionStorage.getItem(key)) {
      sessionStorage.setItem(key, "1");
      window.location.reload();
    }
  }
});

export default router;
