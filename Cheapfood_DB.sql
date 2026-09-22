-- ==========================================
-- CHEAPFOOD
-- ==========================================

-- USUÁRIO
CREATE TABLE usuario (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    tipo VARCHAR(20) NOT NULL DEFAULT 'CLIENTE',
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_usuario_tipo
        CHECK (tipo IN ('CLIENTE', 'ADMIN'))
);


-- ESTABELECIMENTO
CREATE TABLE estabelecimento (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cnpj VARCHAR(18) UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    endereco VARCHAR(200) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(2) NOT NULL,
    cep VARCHAR(9),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- PRODUTO
CREATE TABLE produto (
    id BIGSERIAL PRIMARY KEY,
    estabelecimento_id BIGINT NOT NULL,

    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(80),

    preco_original DECIMAL(10,2) NOT NULL,
    preco_desconto DECIMAL(10,2) NOT NULL,

    quantidade INTEGER NOT NULL,
    data_validade DATE NOT NULL,

    imagem VARCHAR(500),

    status VARCHAR(20) NOT NULL DEFAULT 'DISPONIVEL',

    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_produto_estabelecimento
        FOREIGN KEY (estabelecimento_id)
        REFERENCES estabelecimento(id),

    CONSTRAINT chk_preco_original
        CHECK (preco_original >= 0),

    CONSTRAINT chk_preco_desconto
        CHECK (preco_desconto >= 0),

    CONSTRAINT chk_preco_promocional
        CHECK (preco_desconto <= preco_original),

    CONSTRAINT chk_quantidade
        CHECK (quantidade >= 0),

    CONSTRAINT chk_produto_status
        CHECK (status IN (
            'DISPONIVEL',
            'ESGOTADO',
            'EXPIRADO',
            'INATIVO'
        ))
);


-- PEDIDO
CREATE TABLE pedido (
    id BIGSERIAL PRIMARY KEY,

    usuario_id BIGINT NOT NULL,
    estabelecimento_id BIGINT NOT NULL,

    valor_total DECIMAL(10,2) NOT NULL DEFAULT 0,

    status VARCHAR(30) NOT NULL DEFAULT 'PENDENTE',

    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_pedido_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id),

    CONSTRAINT fk_pedido_estabelecimento
        FOREIGN KEY (estabelecimento_id)
        REFERENCES estabelecimento(id),

    CONSTRAINT chk_pedido_valor
        CHECK (valor_total >= 0),

    CONSTRAINT chk_pedido_status
        CHECK (status IN (
            'PENDENTE',
            'CONFIRMADO',
            'PREPARANDO',
            'PRONTO',
            'FINALIZADO',
            'CANCELADO'
        ))
);


-- ITEM DO PEDIDO
CREATE TABLE item_pedido (
    id BIGSERIAL PRIMARY KEY,

    pedido_id BIGINT NOT NULL,
    produto_id BIGINT NOT NULL,

    quantidade INTEGER NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_item_pedido
        FOREIGN KEY (pedido_id)
        REFERENCES pedido(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_item_produto
        FOREIGN KEY (produto_id)
        REFERENCES produto(id),

    CONSTRAINT chk_item_quantidade
        CHECK (quantidade > 0),

    CONSTRAINT chk_item_preco
        CHECK (preco_unitario >= 0),

    CONSTRAINT chk_item_subtotal
        CHECK (subtotal >= 0)
);


-- PAGAMENTO
CREATE TABLE pagamento (
    id BIGSERIAL PRIMARY KEY,

    pedido_id BIGINT NOT NULL UNIQUE,

    metodo VARCHAR(30) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDENTE',

    valor DECIMAL(10,2) NOT NULL,

    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_pagamento_pedido
        FOREIGN KEY (pedido_id)
        REFERENCES pedido(id),

    CONSTRAINT chk_pagamento_metodo
        CHECK (metodo IN (
            'PIX',
            'CARTAO_CREDITO',
            'CARTAO_DEBITO',
            'DINHEIRO'
        )),

    CONSTRAINT chk_pagamento_status
        CHECK (status IN (
            'PENDENTE',
            'APROVADO',
            'RECUSADO',
            'ESTORNADO'
        )),

    CONSTRAINT chk_pagamento_valor
        CHECK (valor >= 0)
);


INSERT INTO usuario
(nome, email, senha, telefone, tipo)
VALUES
('João Silva', 'joao@email.com', '123456', '(14) 99999-1111', 'CLIENTE'),
('Maria Souza', 'maria@email.com', '123456', '(14) 99999-2222', 'CLIENTE'),
('Carlos Oliveira', 'carlos@email.com', '123456', '(14) 99999-3333', 'CLIENTE'),
('Administrador', 'admin@cheapfood.com', 'admin123', '(14) 99999-0000', 'ADMIN');

INSERT INTO estabelecimento
(nome, cnpj, email, telefone, endereco, cidade, estado, cep, latitude, longitude)
VALUES
(
    'Padaria Central',
    '12.345.678/0001-90',
    'contato@padariacentral.com',
    '(14) 3433-1111',
    'Rua São Paulo, 100',
    'Marília',
    'SP',
    '17500-000',
    -22.2171,
    -49.9500
),
(
    'Mercado Bom Preço',
    '98.765.432/0001-10',
    'contato@mercadobompreco.com',
    '(14) 3433-2222',
    'Avenida das Flores, 500',
    'Marília',
    'SP',
    '17501-000',
    -22.2200,
    -49.9450
),
(
    'Pizzaria Bella Massa',
    '45.678.901/0001-22',
    'contato@bellamassa.com',
    '(14) 3433-3333',
    'Rua das Palmeiras, 250',
    'Marília',
    'SP',
    '17502-000',
    -22.2150,
    -49.9550
);

INSERT INTO produto
(
    estabelecimento_id,
    nome,
    descricao,
    categoria,
    preco_original,
    preco_desconto,
    quantidade,
    data_validade,
    imagem,
    status
)
VALUES

-- LATICÍNIOS
(1, 'Leite Integral 1L', 'Leite integral UHT', 'Laticínios',
 5.99, 3.99, 15, CURRENT_DATE + 3, NULL, 'DISPONIVEL'),

(1, 'Iogurte Natural 170g', 'Iogurte natural refrigerado', 'Laticínios',
 4.99, 2.99, 18, CURRENT_DATE + 2, NULL, 'DISPONIVEL'),

(2, 'Iogurte de Morango 540g', 'Iogurte sabor morango', 'Laticínios',
 9.90, 5.90, 12, CURRENT_DATE + 4, NULL, 'DISPONIVEL'),

(2, 'Requeijão Cremoso 200g', 'Requeijão cremoso', 'Laticínios',
 9.90, 5.90, 10, CURRENT_DATE + 5, NULL, 'DISPONIVEL'),

(2, 'Creme de Leite 200g', 'Creme de leite UHT', 'Laticínios',
 4.90, 2.99, 20, CURRENT_DATE + 8, NULL, 'DISPONIVEL'),

(2, 'Leite Condensado 395g', 'Leite condensado', 'Laticínios',
 7.90, 4.90, 14, CURRENT_DATE + 10, NULL, 'DISPONIVEL'),

(2, 'Mussarela Fatiada 300g', 'Queijo mussarela fatiado', 'Frios',
 18.90, 12.90, 8, CURRENT_DATE + 3, NULL, 'DISPONIVEL'),

(2, 'Presunto Fatiado 300g', 'Presunto cozido fatiado', 'Frios',
 14.90, 9.90, 10, CURRENT_DATE + 2, NULL, 'DISPONIVEL'),

(2, 'Mortadela Fatiada 500g', 'Mortadela tradicional fatiada', 'Frios',
 12.90, 7.90, 8, CURRENT_DATE + 4, NULL, 'DISPONIVEL'),


-- CARNES
(2, 'Carne Moída 500g', 'Carne bovina moída fresca', 'Carnes',
 18.90, 12.90, 8, CURRENT_DATE + 1, NULL, 'DISPONIVEL'),

(2, 'Peito de Frango 1kg', 'Peito de frango resfriado', 'Carnes',
 19.90, 13.90, 10, CURRENT_DATE + 2, NULL, 'DISPONIVEL'),

(2, 'Linguiça Toscana 500g', 'Linguiça suína fresca', 'Carnes',
 16.90, 10.90, 7, CURRENT_DATE + 2, NULL, 'DISPONIVEL'),

(2, 'Salsicha 500g', 'Salsicha refrigerada', 'Carnes',
 11.90, 7.90, 12, CURRENT_DATE + 5, NULL, 'DISPONIVEL'),

(2, 'Hambúrguer Bovino 672g', 'Hambúrguer bovino congelado', 'Congelados',
 19.90, 13.90, 10, CURRENT_DATE + 40, NULL, 'DISPONIVEL'),


-- PADARIA
(1, 'Pão de Forma Tradicional', 'Pão de forma fatiado', 'Padaria',
 10.90, 6.90, 12, CURRENT_DATE + 4, NULL, 'DISPONIVEL'),

(1, 'Pão de Forma Integral', 'Pão de forma integral fatiado', 'Padaria',
 12.90, 7.90, 8, CURRENT_DATE + 3, NULL, 'DISPONIVEL'),

(1, 'Bisnaguinha 300g', 'Pão tipo bisnaguinha', 'Padaria',
 8.90, 5.50, 10, CURRENT_DATE + 3, NULL, 'DISPONIVEL'),

(1, 'Pão de Leite 500g', 'Pão de leite macio', 'Padaria',
 11.90, 6.90, 8, CURRENT_DATE + 2, NULL, 'DISPONIVEL'),

(1, 'Bolo de Chocolate 400g', 'Bolo de chocolate embalado', 'Padaria',
 18.90, 11.90, 6, CURRENT_DATE + 3, NULL, 'DISPONIVEL'),

(1, 'Bolo de Cenoura 400g', 'Bolo de cenoura com cobertura', 'Padaria',
 18.90, 11.90, 5, CURRENT_DATE + 2, NULL, 'DISPONIVEL'),

(1, 'Torradas 160g', 'Torradas tradicionais', 'Padaria',
 7.90, 4.90, 10, CURRENT_DATE + 12, NULL, 'DISPONIVEL'),


-- HORTIFRUTI
(2, 'Banana Prata 1kg', 'Banana prata fresca', 'Hortifruti',
 7.90, 4.90, 20, CURRENT_DATE + 4, NULL, 'DISPONIVEL'),

(2, 'Maçã 1kg', 'Maçã nacional', 'Hortifruti',
 9.90, 6.90, 15, CURRENT_DATE + 7, NULL, 'DISPONIVEL'),

(2, 'Morangos 300g', 'Bandeja de morangos frescos', 'Hortifruti',
 12.90, 7.90, 12, CURRENT_DATE + 2, NULL, 'DISPONIVEL'),

(2, 'Uvas 500g', 'Uvas frescas', 'Hortifruti',
 10.90, 6.90, 10, CURRENT_DATE + 4, NULL, 'DISPONIVEL'),

(2, 'Tomate 1kg', 'Tomates frescos', 'Hortifruti',
 8.90, 5.90, 15, CURRENT_DATE + 3, NULL, 'DISPONIVEL'),

(2, 'Alface Crespa', 'Alface fresca', 'Hortifruti',
 4.50, 2.50, 15, CURRENT_DATE + 2, NULL, 'DISPONIVEL'),

(2, 'Mamão Formosa', 'Mamão formosa fresco', 'Hortifruti',
 8.90, 5.90, 8, CURRENT_DATE + 3, NULL, 'DISPONIVEL'),


-- MERCEARIA
(2, 'Biscoito Recheado Chocolate', 'Biscoito recheado sabor chocolate', 'Mercearia',
 4.99, 2.99, 20, CURRENT_DATE + 30, NULL, 'DISPONIVEL'),

(2, 'Biscoito Cream Cracker', 'Biscoito salgado tradicional', 'Mercearia',
 5.99, 3.49, 18, CURRENT_DATE + 25, NULL, 'DISPONIVEL'),

(2, 'Granola 250g', 'Granola tradicional', 'Mercearia',
 12.90, 7.90, 10, CURRENT_DATE + 20, NULL, 'DISPONIVEL'),

(2, 'Cereal de Milho 300g', 'Cereal de milho', 'Mercearia',
 11.90, 7.90, 12, CURRENT_DATE + 35, NULL, 'DISPONIVEL'),

(2, 'Maionese 500g', 'Maionese tradicional', 'Mercearia',
 9.90, 6.90, 15, CURRENT_DATE + 20, NULL, 'DISPONIVEL'),

(2, 'Ketchup 400g', 'Ketchup tradicional', 'Mercearia',
 8.90, 5.90, 15, CURRENT_DATE + 25, NULL, 'DISPONIVEL'),


-- CONGELADOS
(2, 'Lasanha Bolonhesa 600g', 'Lasanha congelada de carne', 'Congelados',
 18.90, 12.90, 8, CURRENT_DATE + 45, NULL, 'DISPONIVEL'),

(2, 'Pizza Congelada Calabresa', 'Pizza congelada de calabresa', 'Congelados',
 16.90, 10.90, 10, CURRENT_DATE + 60, NULL, 'DISPONIVEL'),

(2, 'Nuggets de Frango 300g', 'Nuggets de frango congelados', 'Congelados',
 13.90, 8.90, 12, CURRENT_DATE + 50, NULL, 'DISPONIVEL'),

(2, 'Batata Frita Congelada 1kg', 'Batata pré-frita congelada', 'Congelados',
 18.90, 12.90, 8, CURRENT_DATE + 90, NULL, 'DISPONIVEL'),


-- BEBIDAS
(1, 'Suco de Laranja 1L', 'Suco de laranja refrigerado', 'Bebidas',
 10.90, 6.90, 8, CURRENT_DATE + 3, NULL, 'DISPONIVEL'),

(2, 'Refrigerante Cola 2L', 'Refrigerante sabor cola', 'Bebidas',
 11.90, 7.90, 20, CURRENT_DATE + 15, NULL, 'DISPONIVEL'),

(2, 'Refrigerante Guaraná 2L', 'Refrigerante sabor guaraná', 'Bebidas',
 10.90, 6.90, 18, CURRENT_DATE + 12, NULL, 'DISPONIVEL'),

(2, 'Energético 473ml', 'Bebida energética', 'Bebidas',
 12.90, 8.90, 15, CURRENT_DATE + 20, NULL, 'DISPONIVEL'),

(2, 'Cerveja Pilsen Lata 350ml', 'Cerveja pilsen em lata', 'Bebidas Alcoólicas',
 4.50, 2.99, 40, CURRENT_DATE + 20, NULL, 'DISPONIVEL'),

(2, 'Cerveja Puro Malte Lata 350ml', 'Cerveja puro malte em lata', 'Bebidas Alcoólicas',
 5.50, 3.49, 30, CURRENT_DATE + 18, NULL, 'DISPONIVEL'),

(3, 'Cerveja Long Neck 355ml', 'Cerveja pilsen long neck', 'Bebidas Alcoólicas',
 6.50, 4.49, 20, CURRENT_DATE + 15, NULL, 'DISPONIVEL');

-- Conferir os produtos
SELECT *
FROM produto
ORDER BY data_validade ASC;

-- Buscar somente produtos que vencem nos próximos 7 dias:
SELECT
    id,
    nome,
    categoria,
    preco_original,
    preco_desconto,
    quantidade,
    data_validade
FROM produto
WHERE data_validade <= CURRENT_DATE + 7
  AND data_validade >= CURRENT_DATE
  AND status = 'DISPONIVEL'
ORDER BY data_validade ASC;

-- Calcular quantos dias faltam
SELECT
    id,
    nome,
    categoria,
    preco_desconto,
    data_validade,
    data_validade - CURRENT_DATE AS dias_para_vencer
FROM produto
WHERE status = 'DISPONIVEL'
ORDER BY data_validade ASC;

-- View consulta salva no banco
CREATE OR REPLACE VIEW produtos_proximos_validade AS
SELECT
    p.id,
    p.nome AS produto,
    p.categoria,
    p.preco_original,
    p.preco_desconto,

    ROUND(
        ((p.preco_original - p.preco_desconto)
        / p.preco_original) * 100,
        2
    ) AS percentual_desconto,

    p.quantidade,
    p.data_validade,

    (p.data_validade - CURRENT_DATE) AS dias_para_vencer,

    e.nome AS estabelecimento,

    CASE
        WHEN p.data_validade < CURRENT_DATE THEN 'VENCIDO'
        WHEN p.data_validade = CURRENT_DATE THEN 'VENCE HOJE'
        WHEN p.data_validade <= CURRENT_DATE + 3 THEN 'VENCE EM ATÉ 3 DIAS'
        WHEN p.data_validade <= CURRENT_DATE + 7 THEN 'VENCE EM ATÉ 7 DIAS'
        ELSE 'VALIDADE NORMAL'
    END AS situacao_validade

FROM produto p

INNER JOIN estabelecimento e
    ON e.id = p.estabelecimento_id

WHERE p.status = 'DISPONIVEL';

-- select do View
SELECT *
FROM produtos_proximos_validade
ORDER BY dias_para_vencer ASC;
