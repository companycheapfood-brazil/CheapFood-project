<script setup lang="ts">
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import BottomNav from "@/components/BottomNav.vue";
import SvgIcon from "@/components/ui/SvgIcon.vue";
import { useToastStore } from "@/stores/useToastStore";

const router = useRouter();
const toastStore = useToastStore();
const search = ref("");
const openIndex = ref<number | null>(0);

const faqs = [
  {
    q: "Como funciona a reserva no CheapFood?",
    a: "Você escolhe os produtos próximos ao vencimento com desconto, confirma a reserva pelo aplicativo e recebe um código exclusivo de 4 dígitos (e QR Code). O item fica reservado para você retirar na loja!",
  },
  {
    q: "Como funciona o Leilão Híbrido?",
    a: "Nos produtos em leilão, você pode dar um lance a partir do valor mínimo sugerido ou clicar em 'Comprar Agora' pelo preço promocional fixo. Se o seu lance for o maior ao término do tempo, você arremata o lote pelo valor do lance!",
  },
  {
    q: "Como retirar meu pedido na loja?",
    a: "Basta comparecer ao endereço do estabelecimento dentro do prazo da reserva e apresentar o código de 4 dígitos exibido na tela de Comprovante ou em Histórico de Pedidos.",
  },
  {
    q: "Posso cancelar uma reserva?",
    a: "Sim! Caso você não compareça dentro do prazo limite estipulado pela loja, a reserva expira automaticamente sem cobrança de multa e o item retorna para a vitrine.",
  },
  {
    q: "Os produtos próximos ao vencimento são seguros?",
    a: "Totalmente! Todos os produtos estão dentro do prazo de validade vigente, com embalagem intacta e inspecionados pelo estabelecimento parceiro.",
  },
];

const filteredFaqs = computed(() => {
  const term = search.value.trim().toLowerCase();
  if (!term) return faqs;
  return faqs.filter(
    (f) => f.q.toLowerCase().includes(term) || f.a.toLowerCase().includes(term),
  );
});

function toggleFaq(idx: number) {
  openIndex.value = openIndex.value === idx ? null : idx;
}

function handleContactSupport() {
  toastStore.addToast(
    "Canal de suporte CheapFood: atendimento iniciado! (suporte@cheapfood.com.br)",
    "info",
  );
}
</script>

<template>
  <div class="screen">
    <header class="help-header">
      <button class="back-btn" @click="router.push('/perfil')" aria-label="Voltar">
        <SvgIcon name="arrow-left" :size="17" />
      </button>
      <h1 class="title">Central de ajuda</h1>
      <span style="width: 34px"></span>
    </header>

    <main class="content">
      <div class="search-bar">
        <input type="text" v-model="search" placeholder="Pesquisar dúvida..." />
        <span class="search-icon">
          <SvgIcon name="search" :size="17" />
        </span>
      </div>

      <div class="section">
        <h2 class="section-title">PERGUNTAS FREQUENTES</h2>
        <div class="faq-list">
          <div
            class="faq-item"
            v-for="(faq, idx) in filteredFaqs"
            :key="faq.q"
            @click="toggleFaq(idx)"
          >
            <div class="faq-header">
              <span>{{ faq.q }}</span>
              <span class="faq-chevron">
                <SvgIcon :name="openIndex === idx ? 'minus' : 'plus'" :size="16" :strokeWidth="2.8" />
              </span>
            </div>
            <p v-if="openIndex === idx" class="faq-answer">
              {{ faq.a }}
            </p>
          </div>
          <p v-if="filteredFaqs.length === 0" style="text-align: center; color: #888; font-size: 0.9rem">
            Nenhuma pergunta encontrada para "{{ search }}".
          </p>
        </div>
      </div>

      <div class="section">
        <h2 class="section-title">CONTATO DIRETO</h2>
        <div class="contact-card" style="cursor: pointer" @click="handleContactSupport">
          <p class="contact-title" style="display: inline-flex; align-items: center; gap: 6px;">
            <SvgIcon name="message-square" :size="16" style="color: #ff3b69" />
            <span>Chat com suporte CheapFood</span>
          </p>
          <p class="contact-subtitle">Toque para iniciar atendimento · Resposta em até 2h</p>
        </div>
      </div>
    </main>

    <BottomNav />
  </div>
</template>

<style scoped>
.screen {
  background-color: #ffffff;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.help-header {
  background-color: #f6b55d;
  padding: 2rem 1.5rem 1.5rem 1.5rem;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.back-btn {
  width: 34px;
  height: 34px;
  padding: 0;
  line-height: 0;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.88);
  color: #333;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.title {
  font-size: 1.2rem;
  font-weight: 800;
  color: #333;
  margin: 0;
}

.content {
  padding: 1.5rem;
  flex: 1;
  overflow-y: auto;
  padding-bottom: 100px;
}

.search-bar {
  position: relative;
  width: 100%;
  margin-bottom: 1.6rem;
}

.search-bar input {
  width: 100%;
  padding: 0.95rem 2.5rem 0.95rem 1rem;
  border-radius: 12px;
  border: 1px solid #f0dfb8;
  background-color: #fdf6e9;
  font-size: 0.95rem;
  color: #333;
}

.search-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #a0845a;
}

.section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 0.75rem;
  font-weight: 800;
  color: #b0b0b0;
  margin-bottom: 1rem;
  letter-spacing: 1px;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.faq-item {
  padding: 1.1rem 1.2rem;
  border-radius: 12px;
  border: 1px solid #f0dfb8;
  background-color: white;
  font-size: 0.9rem;
  font-weight: 700;
  color: #333;
  cursor: pointer;
  transition: background 0.2s;
}

.faq-item:hover {
  background-color: #fdfaf5;
}

.faq-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.faq-chevron {
  font-size: 1.2rem;
  color: #ff3b69;
  font-weight: 900;
}

.faq-answer {
  margin-top: 0.7rem;
  padding-top: 0.7rem;
  border-top: 1px dashed #f0dfb8;
  font-size: 0.84rem;
  font-weight: 500;
  color: #555;
  line-height: 1.45;
}

.contact-card {
  padding: 1.4rem;
  border-radius: 12px;
  border: 1px solid #f0dfb8;
  background-color: #fdf6e9;
  text-align: center;
  transition: transform 0.15s;
}

.contact-card:hover {
  transform: translateY(-2px);
}

.contact-title {
  font-size: 0.95rem;
  font-weight: 800;
  color: #333;
  margin: 0 0 0.3rem 0;
}

.contact-subtitle {
  font-size: 0.8rem;
  color: #a0845a;
  margin: 0;
}
</style>
