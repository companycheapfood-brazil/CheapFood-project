# Estado do Projeto — CheapFood (G4C)
**Última atualização:** 27/09/2026 — 23:39

---

## ✅ O Que Foi Concluído

### Frontend (Vue 3 + Vite + TypeScript)
- **Migração para Pinia**: Stores globais (`useCartStore`, `useMerchantStore`, `useToastStore`) substituíram os composables antigos.
- **Transições de Rota**: `<Transition>` aplicado no `<RouterView>` para animações suaves entre páginas.
- **Toast Notifications**: Sistema global de notificações (`ToastContainer.vue`).
- **Ícones SVG profissionais**: Todos os ícones antigos (emojis e strings) foram substituídos por SVGs vetoriais (Lucide Icons) — inclusive na tela de Configurações do Comerciante.
- **Imagens Reais**: +45 fotos de alta qualidade (Unsplash) mapeadas por categoria de produto (leite, pão, carne, frutas, etc.) substituíram os SVGs placeholder.
- **Logo no Header do Lojista**: Ícone de carrinho + "CheapFood" + badge "LOJISTA" no cabeçalho roxo do comerciante.
- **Cursor Pointer**: Adicionado em todos os cards clicáveis (Busca, Home, Produtos).
- **Imagem do Produto (`/produto/:id`)**: Redimensionada com `border-radius`, sombra e `overflow: hidden`.
- **Carrinho (`/carrinho`)**: Bug de imagem gigante resolvido com `flex-shrink: 0`, `min-width` e `overflow: hidden`.
- **Botão "+" centralizado**: Na Home, o botão rosa de adicionar ao carrinho está centralizado verticalmente no card.

### Backend (Flask + SQLAlchemy + SQLite)
- **Tabela `Pedido`** criada com colunas corretas (`cliente_id`, `produto_id`, `quantidade`, `codigo_reserva`, `status`, `criado_em`).
- **Endpoints do Comerciante**:
  - `GET /api/merchant/stats` — Estatísticas reais (produtos ativos, receita, reservas, gráfico diário).
  - `GET /api/merchant/orders` — Lista de pedidos com status.
  - `PATCH /api/merchant/orders/<id>/status` — Atualizar status do pedido.
  - `GET /api/merchant/products` — Produtos do estabelecimento.
  - `POST /api/products` — Upload de imagem via `FormData` (aceita JPG, PNG, WEBP, GIF).
- **Gráfico de Vendas**: Dados reais agrupados por dia da semana nos últimos 7 dias.
- **15 pedidos simulados** inseridos no banco para povoar o Dashboard.

### Segurança
- **RBAC (Role-Based Access Control)** no Vue Router:
  - Cliente (`CLIENTE`) não acessa rotas `/comerciante/*`.
  - Comerciante (`COMERCIANTE`) não acessa rotas de consumidor (`/`, `/carrinho`, `/buscar`, `/produto/*`).
  - Usuários logados são redirecionados se tentarem acessar `/login`.

### Dashboard do Comerciante
- **Métricas extras**: Ticket Médio Semanal + Crescimento % vs semana anterior.
- **Gráfico melhorado**: Valores numéricos acima de cada barra, destaque visual no pico, legenda indicadora, totalizador de receita.
- **Textos corrigidos**: Encoding UTF-8 resolvido (acentos estavam quebrados).

---

## 🔜 Próximos Passos para Produção

1. **JWT (flask-jwt-extended)** — Autenticação segura com tokens.
2. **PostgreSQL** — Migrar de SQLite para banco de produção.
3. **QR Code real** — Gerar QR para retirada de pedidos.
4. **Pagamento (Mercado Pago / Stripe)** — Integração de pagamento real.
5. **Deploy (Vercel + Railway)** — Colocar o app online com domínio próprio.
6. **PWA (vite-plugin-pwa)** — Tornar o app instalável no celular.

---

## 🔑 Contas de Teste
| Perfil       | Email                | Senha    |
|-------------|----------------------|----------|
| Admin/Lojista | admin@cheapfood.com | admin123 |
| Consumidor   | joao@email.com      | 123456   |

## 🛠️ Como Rodar
```bash
# Frontend
npm run dev

# Backend
cd backend && python app.py
```

## 📦 Formatos de Upload Aceitos
`.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`
