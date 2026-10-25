<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import BottomNav from "@/components/BottomNav.vue";
import SvgIcon from "@/components/ui/SvgIcon.vue";

const router = useRouter();
const activeTab = ref("Termos de uso");

const terms = [
  {
    title: "1. Aceitação dos Termos",
    desc: "Ao utilizar o CheapFood, você concorda com estes Termos de Uso, que regulam a reserva de produtos alimentícios próximos à data de validade e a participação em leilões híbridos.",
  },
  {
    title: "2. Uso do Serviço e Reservas",
    desc: "O CheapFood conecta consumidores a estabelecimentos locais para evitar o desperdício alimentar. Ao confirmar uma reserva, um código único é gerado e o estoque é bloqueado automaticamente.",
  },
  {
    title: "3. Responsabilidades do Estabelecimento",
    desc: "Os comerciantes parceiros são integralmente responsáveis pela veracidade da data de validade, conservação e qualidade sanitária dos itens anunciados.",
  },
  {
    title: "4. Prazos e Cancelamentos",
    desc: "Reservas não retiradas dentro do prazo limite retornam automaticamente ao estoque disponível da loja.",
  },
];

const privacy = [
  {
    title: "1. Coleta de Dados (LGPD)",
    desc: "Coletamos apenas dados essenciais (nome, e-mail e telefone) para identificação das reservas, lances em leilões e comunicação entre cliente e loja.",
  },
  {
    title: "2. Uso das Informações",
    desc: "Seus dados são utilizados exclusivamente para gerar seus códigos de retirada, histórico de economia e notificações de ofertas favoritadas.",
  },
  {
    title: "3. Segurança e Armazenamento",
    desc: "As senhas são armazenadas com criptografia hash e nenhum dado pessoal é vendido ou compartilhado com terceiros para fins publicitários.",
  },
  {
    title: "4. Exclusão de Conta",
    desc: "Você tem direito de solicitar a exclusão definitiva da sua conta e de todo o seu histórico a qualquer momento pelo menu Perfil > Excluir conta.",
  },
];
</script>

<template>
  <div class="screen">
    <header class="terms-header">
      <button class="back-btn" @click="router.push('/perfil')" aria-label="Voltar">
        <SvgIcon name="arrow-left" :size="18" />
      </button>
      <h1 class="title">Termos e privacidade</h1>
      <span style="width: 34px"></span>
    </header>

    <main class="content">
      <div class="toggle-container">
        <button
          class="toggle-btn"
          :class="{ active: activeTab === 'Termos de uso' }"
          @click="activeTab = 'Termos de uso'"
        >
          Termos de uso
        </button>
        <button
          class="toggle-btn"
          :class="{ active: activeTab === 'Privacidade' }"
          @click="activeTab = 'Privacidade'"
        >
          Privacidade
        </button>
      </div>

      <div class="terms-list" v-if="activeTab === 'Termos de uso'">
        <div class="term-item" v-for="term in terms" :key="term.title">
          <h3 class="term-title">{{ term.title }}</h3>
          <p class="term-desc">{{ term.desc }}</p>
        </div>
      </div>
      <div class="terms-list" v-else>
        <div class="term-item" v-for="item in privacy" :key="item.title">
          <h3 class="term-title">{{ item.title }}</h3>
          <p class="term-desc">{{ item.desc }}</p>
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

.terms-header {
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
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.85);
  color: #333;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  line-height: 0;
  cursor: pointer;
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

.toggle-container {
  display: flex;
  background-color: #f5f5f5;
  border-radius: 12px;
  padding: 0.3rem;
  margin-bottom: 2rem;
}

.toggle-btn {
  flex: 1;
  padding: 0.8rem;
  border-radius: 10px;
  border: none;
  background: transparent;
  font-size: 0.85rem;
  font-weight: 700;
  color: #888;
  cursor: pointer;
}

.toggle-btn.active {
  background-color: white;
  color: #333;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.terms-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.term-item {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.term-title {
  font-size: 0.9rem;
  font-weight: 800;
  color: #333;
  margin: 0;
}

.term-desc {
  font-size: 0.85rem;
  color: #a0a0a0;
  line-height: 1.5;
  margin: 0;
}
</style>
