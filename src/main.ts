import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.mount("#app");

// Registrar Service Worker PWA para suporte offline e instalação no celular
if ("serviceWorker" in navigator && !window.location.host.includes("localhost:5173")) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/sw.js")
      .then((reg) => console.log("CheapFood PWA ServiceWorker ativo:", reg.scope))
      .catch((err) => console.log("Falha ao registrar ServiceWorker:", err));
  });
}
