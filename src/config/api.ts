/**
 * Configuração central da API.
 * Defina VITE_API_URL no arquivo .env para apontar para outro backend
 * (ex.: VITE_API_URL=https://api.cheapfood.com.br).
 */
function getDefaultApiBase(): string {
  if (!import.meta.env.PROD) {
    return "http://127.0.0.1:5000";
  }
  if (typeof window !== "undefined") {
    const host = window.location.hostname;
    if (host === "localhost" || host === "127.0.0.1") {
      return "http://127.0.0.1:5000";
    }
    if (host.endsWith(".vercel.app")) {
      return "https://cheapfood-project.onrender.com";
    }
  }
  // Mesmo domínio (ex.: Nginx reverse-proxy em https://cheap-food.altvia.cloud/)
  return "";
}

export const API_BASE: string = (
  (import.meta.env.VITE_API_URL as string | undefined) || getDefaultApiBase()
).replace(/\/+$/, "");

/** Prefixo dos endpoints REST (sem barra final). */
export const API_URL = `${API_BASE}/api`;

/** Indica se o valor de imagem é uma URL/caminho (e não um SVG inline). */
export function isImageUrl(image?: string | null): image is string {
  return !!image && (image.startsWith("/") || image.startsWith("http") || image.startsWith("blob:"));
}

/** Converte caminhos relativos do backend (ex.: /static/uploads/x.jpg) em URL absoluta. */
export function resolveImageUrl(image?: string | null): string {
  if (!image) return "";
  if (image.startsWith("http") || image.startsWith("blob:") || image.startsWith("data:")) return image;
  return `${API_BASE}${image.startsWith("/") ? "" : "/"}${image}`;
}
