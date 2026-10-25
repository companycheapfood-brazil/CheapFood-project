# Estado do Projeto — CheapFood (G4C) — Versão Final TCC
**Última atualização:** 18/10/2026

---

## 🎯 Visão Geral
O **CheapFood** é uma plataforma e marketplace (web/mobile-first) que conecta consumidores a estabelecimentos para a venda de produtos próximos à data de vencimento com descontos progressivos e modelos de leilão híbrido, combatendo o desperdício de alimentos e recuperando receita para o varejo local.
- **Frontend:** Vue 3 (Composition API) + TypeScript + Vite + Pinia + Vue Router.
- **Backend:** Python + Flask + SQLAlchemy + SQLite (`cheapfood.db`) + Google Generative AI (Gemini Flash para catalogação inteligente).

---

## ✅ Funcionalidades Implementadas e Validadas para Apresentação do TCC

### 1. Experiência do Consumidor (Loja, Busca, Leilão, Carrinho e Comprovante)
- **Vitrine & Busca Avançada ([HomeView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/shop/HomeView.vue), [SearchView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/shop/SearchView.vue)):**
  - Filtro em tempo real por nome, loja e categoria (`Todos`, `Leilões`, `Padaria`, `Hortifruti`, `Laticínios`, `Carnes`, `Frios`, `Bebidas`, `Congelados`).
  - Ordenação dinâmica na busca por *Relevância*, *Menor Preço* e *Maior Desconto*.
  - Seleção interativa do endereço/região do consumidor no topo da vitrine.
- **Detalhe do Produto & Leilão Híbrido ([ProductView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/shop/ProductView.vue), [AuctionBadge.vue](file:///C:/Users/tavin/CheapFood-project/src/components/AuctionBadge.vue)):**
  - Suporte completo a produtos de **Preço Fixo** e **Leilão Híbrido** ("Compre Agora ou Dê um Lance") com cronômetro regressivo ao vivo ([useAuctionClock.ts](file:///C:/Users/tavin/CheapFood-project/src/composables/useAuctionClock.ts)).
  - Avaliações dinâmicas por categoria e endereço real da loja parceira.
- **Sacola & Simulação de Pagamento ([CartView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/shop/CartView.vue)):**
  - Seleção de forma de pagamento para reserva/retirada (*PIX na Retirada*, *Cartão na Loja*, *Vale-Refeição / Alimentação* ou *Dinheiro*), exibindo o cálculo em tempo real da economia obtida.
- **Comprovante Digital com QR Code & PIN ([ReceiptView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/shop/ReceiptView.vue)):**
  - Conectado ao endpoint `GET /api/orders/code/<codigo>` para exibir os itens reais reservados, código PIN de 4 caracteres (com botão de cópia rápida), QR Code visual dinâmico, endereço de retirada e economia total.

### 2. Perfil do Consumidor & Métricas de Impacto Ambiental (ESG)
- **Painel de Impacto Sustentável ([ProfileView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/profile/ProfileView.vue)):**
  - Abas interativas (**Economizado**, **Salvos**, **Histórico**) calculadas a partir dos pedidos reais do usuário:
    - Total economizado em R$ e percentual médio de desconto.
    - Estimativa de **kg de alimentos salvos** do desperdício e **kg de CO₂ evitados** na atmosfera.
    - Atalho para os últimos pedidos com abertura direta do comprovante.
- **Histórico, Ajuda, Termos LGPD e Conta ([HistoryView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/profile/HistoryView.vue), [HelpView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/profile/HelpView.vue), [TermsView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/profile/TermsView.vue), [EditProfileView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/profile/EditProfileView.vue), [DeleteAccountView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/profile/DeleteAccountView.vue)):**
  - Central de ajuda com busca instantânea e acordeões interativos; Termos de Uso e Política de Privacidade completa (LGPD); edição de perfil com foto e exclusão de conta.

### 3. Painel do Comerciante (Dashboard, Produtos, IA, Pedidos, Planos e Configurações)
- **Dashboard Analítico Multi-Período ([DashboardView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/merchant/DashboardView.vue)):**
  - Filtros interativos **Hoje**, **7 Dias**, **Este Mês** e **Este Ano** conectados ao backend (`GET /api/merchant/stats?period=...`).
  - Indicadores de *Produtos Ativos*, *Receita Recuperada*, *Reservas*, *Ticket Médio*, *Crescimento (%)* e alerta clicável de produtos próximos ao vencimento.
- **Gestão de Produtos, Leilões e Reativação ([ManageProductsView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/merchant/ManageProductsView.vue), [CreateProductView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/merchant/CreateProductView.vue), [EditProductView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/merchant/EditProductView.vue)):**
  - Catalogação assistida por **IA (Google Gemini Vision)** a partir da foto da embalagem.
  - Ações funcionais para **Editar**, **Pausar/Ativar**, **Parar Leilão** e **+20% Desconto e Reativar** em itens vencidos (`PATCH /api/merchant/products/<id>/discount`).
- **Conferência de Pedidos e Retirada por PIN ([OrdersView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/merchant/OrdersView.vue), [OrderDetailView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/merchant/OrderDetailView.vue), [MerchantHistoryView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/merchant/MerchantHistoryView.vue)):**
  - Busca rápida por código PIN de 4 dígitos ou nome do cliente, confirmação de retirada no balcão, cancelamento com estorno automático de estoque e histórico consolidado de vendas.
- **Configurações da Loja e Planos CheapFood Pro ([SettingsView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/merchant/SettingsView.vue), [PlansView.vue](file:///C:/Users/tavin/CheapFood-project/src/views/merchant/PlansView.vue)):**
  - Persistência real no SQLite (`GET / PUT /api/merchant/store` e `PATCH /api/merchant/plan`) para Dados da Loja, Horário de Funcionamento, Formas de Pagamento, Notificações e Assinatura de Planos (*Gratuito*, *Pro Mensal* e *Pro Anual VIP*), refletindo em tempo real no selo do cabeçalho ([MerchantHeader.vue](file:///C:/Users/tavin/CheapFood-project/src/components/merchant/MerchantHeader.vue)).

---

## 🔑 Credenciais de Demonstração (TCC)
| Perfil       | Email                | Senha    |
|-------------|----------------------|----------|
| **Lojista (Padaria Central)** | `admin@cheapfood.com` | `admin123` |
| **Consumidor** | `joao@email.com` | `123456` |

---

## 🛠️ Como Iniciar ou Popular Dados para a Banca

```bash
# Popular / Resetar o banco de dados com dados ricos para apresentação do TCC:
cd backend
python seed_tcc.py

# Terminal 1 - Backend (Python / Flask em http://127.0.0.1:5000)
cd backend
python app.py

# Terminal 2 - Frontend (Vue 3 + Vite em http://localhost:5173)
npm.cmd run dev
```

---

## 🚀 Preparação para Deploy (Concluída)
- **Zero Erros de Build:** `npm run build` compilando com sucesso via `vue-tsc` e `vite build`.
- **Rotas SPA Resolvidas:** `vercel.json` e `public/_redirects` inclusos para evitar 404 em rotas como `/comerciante` e `/carrinho`.
- **Segurança & Tokens:**
  - Autenticação real com token assinado (`itsdangerous` / Bearer token).
  - Rotas do comerciante protegidas com `@require_merchant` e isolamento por estabelecimento (`usuario_id`).
  - Redefinição de senha com token criptográfico de uso único e prazo de expiração (1h).
  - Migração de banco automática e idempotente via `ensure_schema()` para SQLite e PostgreSQL.
- **Pronto para Hospedagem Gratuita:**
  - Backend: `Procfile` configurado para `gunicorn` no Render/Railway, com suporte dinâmico a `DATABASE_URL` (PostgreSQL/SQLite).
  - Frontend: `VITE_API_URL` centralizado e configurável via `.env`.
  - Exemplos completos de configuração em `.env.example` e `backend/.env.example`.
