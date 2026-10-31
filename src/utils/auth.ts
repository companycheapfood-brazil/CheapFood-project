/**
 * Helpers de autenticação compartilhados entre stores/services.
 * O AuthService salva `{ token, user: { id, name, email, role } }` em localStorage['user'].
 */

/** Retorna o ID do usuário logado (string) ou null se não houver sessão. */
export function getLoggedUserId(): string | null {
  const raw = localStorage.getItem("user");
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw);
    const user = parsed.user || parsed;
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
    localStorage.removeItem("user");
    localStorage.removeItem("cf_token");
    localStorage.removeItem("cf_cart_items");
    const publicPaths = ["/login", "/register", "/recuperar-senha"];
    if (
      typeof window !== "undefined" &&
      !publicPaths.includes(window.location.pathname)
    ) {
      window.location.href = "/login";
    }
    return true;
  }
  return false;
}
