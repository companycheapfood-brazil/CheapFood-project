# Estado do Projeto — CheapFood (G4C)
**Última atualização:** 03/10/2026

---

## 🎯 Visão Geral
O CheapFood é um protótipo MVP funcional de um marketplace que conecta consumidores a lojistas para a venda de produtos próximos ao vencimento, com desconto. O sistema utiliza Vue 3 (Composition API) + Vite no Frontend e Flask + SQLAlchemy no Backend.

---

## ✅ O Que Foi Construído e Resolvido

### 1. Funcionalidades do Consumidor
- **Vitrine e Busca (`/`, `/buscar`)**: Exibição de produtos. Adicionado um sistema de **Favoritos (❤️)** integrado com o backend (tabela `favorito`), salvando preferências em tempo real e mantendo o layout dos cards intacto.
- **Meus Favoritos (`/perfil/favoritos`)**: Nova tela adicionada ao menu do Perfil para listar apenas os produtos favoritados.
- **Carrinho e Checkout (`/carrinho`)**: Bug de imagens gigantes resolvido com uso de Flexbox estrito.
- **Trava de Estoque Automática (Backend)**: Quando um pedido é finalizado no `/api/checkout` e a `quantidade` do produto chega a zero (0), o status dele muda automaticamente para `ESGOTADO`, tirando-o da visão do cliente mas mantendo-o visível no painel do lojista.

### 2. Funcionalidades do Lojista (Painel Administrativo)
- **Dashboard com Filtros Temporais (`/comerciante`)**: 
  - Gráfico e métricas totalmente responsivos aos filtros (Hoje, 7 Dias, Mês, Ano).
  - Backend calcula as datas precisas e soma receita baseada na coluna `criado_em`.
  - Métrica de crescimento percentual (%) real calculada comparando com o período anterior equivalente (ex: este mês vs mês passado).
- **Gestão de Produtos (`/comerciante/produtos`, `/comerciante/editar/:id`)**:
  - Cadastro (`POST /api/products`) aceita `FormData` com upload real de imagens para a pasta `/static/uploads`.
  - Botão "Editar" agora é 100% funcional, puxando dados reais e enviando um `PUT /api/products/:id` para atualizar atributos e a imagem no banco.
- **Gestão de Pedidos (`/comerciante/pedidos`)**:
  - Resolvido bug de Event Bubbling (clicar no botão acionava o clique do card).
  - Tela de detalhes do pedido (`/comerciante/pedidos/:id`) refatorada para buscar os dados reais (preço e data de criação formatada) do banco de dados, abandonando mocks fixos ("R$2,49").
- **Configurações (`/comerciante/config`)**: Totalmente redesenhada, trocando Emojis quebrados por ícones SVG vetoriais bonitos e adicionando botão de Logout real.
- **UI/UX do Lojista**: Criado um cabeçalho personalizado (`MerchantHeader.vue`) contendo a logo da marca ("CheapFood") perfeitamente alinhada e um selo/badge "LOJISTA".

### 3. Segurança e Base (Core)
- **Role-Based Access Control (RBAC)** no Vue Router (`router/index.ts`):
  - Lojista (Merchant) restrito ao `/comerciante`.
  - Cliente (Consumer) impedido de acessar o painel do lojista.
  - Correção de bug no guardião de rota que buscava por `user.type` em vez de `user.role` (retornado pela API).
- **Consistência de Interface**: Alinhamento de todos os SVG de logos corrigido nas 4 telas de Auth (Login, Registro, Esqueci a Senha, etc) garantindo a cor tema `fill="#FF3B69"` em vez de SVG invisível.
- **Banco de Dados**: Refatorações na tabela `Pedido` (colunas precisas) e adição das tabelas `Favorito` para amarração das entidades.

---

## 🔜 O Que Ficou Pendente (Para o próximo Desenvolvedor/Modelo)

Existem algumas áreas secundárias que não foram conectadas a lógicas reais de banco ou negócio e seguem maquiadas (mockadas) no Frontend:
1. **Histórico de Pedidos do Perfil Consumidor**: As abas "Economizados", "Reservas", e os cards da tela `/perfil/historico` ainda estão chumbados no Frontend com os dados "Padaria Central".
2. **Página de Planos Pro (`/comerciante/planos`)**: Interface existe, mas é falsa, sem conexão de gateway de pagamento ou mudança de flag no BD.
3. **Módulo de Notificações In-App**: Previsto no Business Plan, mas ainda sem infraestrutura (WebSockets ou tabela de notificação).

### Integrações Recomendadas (Produção)
- **JWT (flask-jwt-extended)** para blindar endpoints no Backend.
- **PostgreSQL** para substituir o arquivo `.db` estático.
- Integração PIX/MercadoPago para validar o fluxo de pagamento.

---

## 🔑 Credenciais de Teste
| Perfil       | Email                | Senha    |
|-------------|----------------------|----------|
| Lojista      | admin@cheapfood.com  | admin123 |
| Consumidor   | joao@email.com       | 123456   |

## 🛠️ Como Iniciar
```bash
# Terminal 1 - Frontend (Vue)
npm run dev

# Terminal 2 - Backend (Python/Flask)
cd backend
python app.py
```
