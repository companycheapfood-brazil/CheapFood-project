# Estado do Projeto - CheapFood (Antigravity)

## O Que Foi Feito Recentemente
- **Design & UI**: Refinamento de bordas, cantos e cursores em todas as telas (Home, Search, Product, Cart, ManageProducts).
- **Imagens Populares**: Um robô substituiu todas as miniaturas SVG por +45 fotos de altíssima qualidade (comida real), puxadas via Unsplash e servidas pela API Flask (/static/uploads).
- **Carrinho**: Correção do CSS da imagem .real-image que transbordava do contêiner.
- **Painel do Comerciante**:
  - Tabela pedido recriada do zero (incluindo as colunas corretas de cliente_id e estabelecimento_id).
  - Geração de 15 pedidos dummy (etirado, pendente, expirado) via script para povoar o DB.
  - Correção na string replacement e bug Vue Compiler na tela /comerciante.
  - Melhorias no visual do Gráfico de Vendas, que agora agrupa os dias do array stats.dailySales retornado pelo servidor e mostra de fato as cifras exatas na interface, com destaque visual de picos.
  - O banco SQLite agora é 100% capaz de rodar a rota Lojista (Merchant) com produtos mapeados, faturamento somado dinamicamente e reservas.

## Próximos Passos
- Refinar detalhes de edição/deleção de produtos no Dashboard.
- Configurar autenticação JWT (caso necessite escala ou deploy final).
- Ajustes finos adicionais solicitados pelo usuário.
