# Resumo do Projeto: CheapFood

## Estado Atual (Atualizado)

### Visão Geral
O **CheapFood** é uma plataforma focada em sustentabilidade e na redução do desperdício de alimentos. A aplicação conecta comerciantes a consumidores para a venda de produtos alimentícios que estão próximos da data de validade, oferecendo-os com descontos (indicados por selos como `-50% OFF`).

### Arquitetura e Tecnologias
- **Stack:** Vue 3 (Composition API), Vite, TypeScript.
- **Roteamento:** Vue Router (`src/router/index.ts`).
- **Requisições HTTP:** Axios (`src/services/`).
- **Gerenciamento de Estado/Lógica:** Vue Composables (`src/composables/`).

### Principais Frentes da Aplicação

#### 1. Área do Cliente (Consumidor)
Telas voltadas para quem vai comprar os alimentos:
- Vitrine e Busca (`HomeView`, `SearchView`).
- Visualização do Produto (`ProductView`).
- Carrinho de Compras (`CartView`).
- Comprovantes e Perfil (`ReceiptView`, `ProfileView`, `EditProfileView`).

#### 2. Painel do Lojista (Comerciante)
Telas administrativas para os estabelecimentos (`/comerciante/*`):
- Dashboard de métricas e acompanhamento (`DashboardView`).
- Cadastro e gerenciamento do catálogo/estoque (`CreateProductView`, `ManageProductsView`).
- Acompanhamento de pedidos - pendentes, retirados, etc (`OrdersView`).
- Configurações do estabelecimento (`SettingsView`).

### O que já fizemos até aqui
- Leitura e mapeamento de toda a estrutura de pastas e arquitetura (identificando os dois fluxos principais: Cliente vs Lojista).
- Resolução de um conflito de merge pendente no arquivo `README.md`.

### Próximos Passos
- (Aguardando definição): Pode envolver criação de novas views, integração dos services com um backend real, ajustes de layout ou refatoração.

---
*Este arquivo serve como memória e contexto para lembrarmos em que pé o projeto está nas próximas interações.*
