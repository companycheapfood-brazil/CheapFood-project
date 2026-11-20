import { ref } from "vue";

/**
 * Helpers de autenticação compartilhados entre stores/services.
 * O AuthService salva `{ token, user: { id, name, email, role } }` em localStorage['user'].
 */

/** Contador reativo incrementado em login/logout/troca de perfil para remontar views. */
export const sessionVersion = ref(0);

export function bumpSessionVersion(): void {
  sessionVersion.value += 1;
}

/** Normaliza o papel do usuário entre formatos novos (`role`) e legados (`tipo`). */
export function normalizeUserRole(user: any): "consumer" | "merchant" {
  if (!user) return "consumer";
  if (user.role === "merchant" || user.tipo === "ADMIN") return "merchant";
  return "consumer";
}

/** Limpa completamente os dados de sessão e preferências locais. */
export function clearAuthStorage(): void {
  try {
    localStorage.removeItem("user");
    localStorage.removeItem("cf_token");
    localStorage.removeItem("cf_cart_items");
    localStorage.removeItem("cf_recent_categories");
    localStorage.removeItem("cf_recent_product_ids");
    localStorage.removeItem("cf_payment_methods");
  } catch {
    // ignore storage errors
  }
  bumpSessionVersion();
}

/** Retorna o ID do usuário logado (string) ou null se não houver sessão. */
export function getLoggedUserId(): string | null {
  const raw = localStorage.getItem("user");
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw);
    const user = parsed?.user || parsed;
    return user?.id != null ? String(user.id) : null;
  } catch {
    return null;
  }
}

/** Retorna o token de autenticação assinado ou null se não houver sessão. */
export function getAuthToken(): string | null {
  const raw = localStorage.getItem("user");
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw);
    return parsed?.token || null;
  } catch {
    return null;
  }
}

/** Headers enviados para o backend com token de autorização. */
export function authHeaders(): Record<string, string> {
  const headers: Record<string, string> = {};
  const token = getAuthToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

/**
 * Trata respostas 401 (Unauthorized) limpando a sessão expirada/inválida
 * e redirecionando para a tela de login.
 */
export function handleUnauthorized(status: number): boolean {
  if (status === 401) {
    clearAuthStorage();
    const publicPaths = ["/start", "/login", "/register", "/forgot-password", "/reset-password"];
    if (typeof window !== "undefined") {
      const normalizedPath = window.location.pathname.replace(/\/+$/, "") || "/";
      if (!publicPaths.includes(normalizedPath)) {
        window.location.href = "/login";
      }
    }
    return true;
  }
  return false;
}
