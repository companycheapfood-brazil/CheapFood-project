import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";
import axios from "axios";
import App from "./App.vue";
import router from "./router";
import { handleUnauthorized } from "./utils/auth";

axios.defaults.timeout = 30000;

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status;
    const reqUrl = String(error?.config?.url || "");
    if (status === 401 && !reqUrl.includes("/auth/login")) {
      handleUnauthorized(401);
    }
    return Promise.reject(error);
  },
);

if (typeof window !== "undefined") {
  window.addEventListener("vite:preloadError", () => {
    const key = "cf_preload_reloaded";
    if (!sessionStorage.getItem(key)) {
      sessionStorage.setItem(key, "1");
      window.location.reload();
    }
  });
}

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.mount("#app");

// Registrar Service Worker PWA apenas em produção fora de localhost
if (
  import.meta.env.PROD &&
  "serviceWorker" in navigator &&
  !["localhost", "127.0.0.1"].includes(window.location.hostname)
) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/sw.js")
      .catch((err) => console.warn("Falha ao registrar ServiceWorker:", err));
  });
}
