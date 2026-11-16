from app import app, db, Usuario, Estabelecimento, Produto, Pedido, Leilao, Lance, Favorito, Avaliacao, ensure_schema
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, timezone


def seed_tcc(run_migrations=True):
    if run_migrations:
        ensure_schema()
    with app.app_context():
        now_local = datetime.now()
        now_utc = datetime.now(timezone.utc).replace(tzinfo=None)

        # 1. Garantir usuários principais de demonstração
        def get_or_create_user(email, nome, senha, tipo, telefone):
            u = Usuario.query.filter_by(email=email).first()
            if not u:
                u = Usuario(
                    nome=nome,
                    email=email,
                    senha=generate_password_hash(senha),
                    telefone=telefone,
                    tipo=tipo
                )
                db.session.add(u)
                db.session.flush()
            else:
                u.nome = nome
                u.tipo = tipo
                u.foto = None
                if not u.telefone:
                    u.telefone = telefone
            return u

        admin = get_or_create_user('admin@cheapfood.com', 'Padaria Central (Admin)', 'admin123', 'ADMIN', '(14) 99811-2233')
        joao = get_or_create_user('joao@email.com', 'João Silva', '123456', 'CLIENTE', '(14) 99712-3456')
        maria = get_or_create_user('maria@email.com', 'Maria Souza', '123456', 'CLIENTE', '(14) 99654-7890')
        carlos = get_or_create_user('carlos@email.com', 'Carlos Oliveira', '123456', 'CLIENTE', '(14) 99123-4567')

        # 2. Garantir estabelecimento principal configurado
        estab = Estabelecimento.query.first()
        if not estab:
            estab = Estabelecimento(
                usuario_id=admin.id,
                categoria='Padaria e Confeitaria',
                nome='Padaria & Empório Central',
                cnpj='12.345.678/0001-90',
                email='contato@padariacentral.com.br',
                telefone='(14) 3433-1020',
                endereco='Rua São Paulo, 100 - Centro',
                cidade='Marília',
                estado='SP',
                cep='17500-010',
                horario_funcionamento='Seg a Sáb: 08:00 às 20:00',
                plano='monthly',
                formas_pagamento='PIX, Cartão de Crédito/Débito e Dinheiro',
                notificacoes_ativas=True
            )
            db.session.add(estab)
        else:
            estab.usuario_id = admin.id
            estab.categoria = estab.categoria or 'Padaria e Confeitaria'
            estab.nome = 'Padaria & Empório Central'
            estab.cnpj = estab.cnpj or '12.345.678/0001-90'
            estab.telefone = estab.telefone or '(14) 3433-1020'
            estab.endereco = 'Rua São Paulo, 100 - Centro'
            estab.cidade = 'Marília'
            estab.estado = 'SP'
            estab.cep = '17500-010'
            estab.horario_funcionamento = 'Seg a Sáb: 08:00 às 20:00'
            estab.plano = estab.plano if estab.plano in ('free', 'monthly', 'annual') else 'monthly'
            estab.formas_pagamento = 'PIX, Cartão de Crédito/Débito e Dinheiro'
            estab.notificacoes_ativas = True
        db.session.flush()

        # 3. Limpar produtos, leilões, lances, avaliações e pedidos antigos para recriar vitrine limpa
        Avaliacao.query.delete()
        Favorito.query.delete()
        Lance.query.delete()
        Leilao.query.delete()
        Pedido.query.delete()
        Produto.query.delete()
        db.session.commit()

        # 4. Cadastrar 12 produtos variados com datas relativas a HOJE
        produtos_data = [
            {
                "nome": "Nutella Creme de Avelã 350g",
                "descricao": "Pote de 350g lacrado, lote próximo ao vencimento em perfeito estado.",
                "categoria": "Padaria",
                "preco_original": 26.90,
                "preco_desconto": 14.90,
                "quantidade": 8,
                "dias_validade": 2,
                "imagem": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/73/Nutella_for_breakfast_-_Flickr_-_love.jsc.jpg/500px-Nutella_for_breakfast_-_Flickr_-_love.jsc.jpg",
                "leilao": {
                    "preco_inicial": 9.90,
                    "preco_minimo": 14.90,
                    "horas_fim": 3,
                    "lances": [
                        (maria.id, 10.50, 45),
                        (joao.id, 11.90, 20),
                    ]
                }
            },
            {
                "nome": "Iogurte Grego Natural 170g",
                "descricao": "Iogurte grego tradicional refrigerado, textura cremosa. Vence amanhã!",
                "categoria": "Laticínios",
                "preco_original": 5.50,
                "preco_desconto": 2.20,
                "quantidade": 15,
                "dias_validade": 1,
                "imagem": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b8/Joghurt.jpg/500px-Joghurt.jpg",
                "leilao": {
                    "preco_inicial": 1.20,
                    "preco_minimo": 2.20,
                    "horas_fim": 2,
                    "lances": [
                        (carlos.id, 1.50, 30),
                    ]
                }
            },
            {
                "nome": "Leite UHT Integral Italac 1L",
                "descricao": "Caixa de leite UHT integral 1 litro, embalagem intacta.",
                "categoria": "Laticínios",
                "preco_original": 6.49,
                "preco_desconto": 3.49,
                "quantidade": 24,
                "dias_validade": 3,
                "imagem": "/static/uploads/88a21411725e48b4931157e24e8807fd_leite-italic.jpg",
                "leilao": {
                    "preco_inicial": 2.00,
                    "preco_minimo": 3.49,
                    "horas_fim": 5,
                    "lances": [
                        (maria.id, 2.30, 50),
                        (carlos.id, 2.60, 15),
                    ]
                }
            },
            {
                "nome": "Pão Artesanal de Fermentação Natural 500g",
                "descricao": "Fornada do dia anterior, casca crocante, ideal para torradas e lanches.",
                "categoria": "Padaria",
                "preco_original": 16.00,
                "preco_desconto": 6.90,
                "quantidade": 6,
                "dias_validade": 0,  # Vence hoje!
                "imagem": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=500&q=80"
            },
            {
                "nome": "Queijo Mussarela Fatiado 300g",
                "descricao": "Bandeja de mussarela fatiada resfriada 300g, pronta para consumo.",
                "categoria": "Frios",
                "preco_original": 18.90,
                "preco_desconto": 9.90,
                "quantidade": 10,
                "dias_validade": 1,  # Vence amanhã!
                "imagem": "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?auto=format&fit=crop&w=500&q=80"
            },
            {
                "nome": "Coca-Cola Original 2L",
                "descricao": "Refrigerante Coca-Cola sabor original em garrafa PET de 2 litros.",
                "categoria": "Bebidas",
                "preco_original": 11.99,
                "preco_desconto": 6.99,
                "quantidade": 18,
                "dias_validade": 5,
                "imagem": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/27/Coca_Cola_Flasche_-_Original_Taste.jpg/500px-Coca_Cola_Flasche_-_Original_Taste.jpg"
            },
            {
                "nome": "Ketchup Heinz Tradicional 397g",
                "descricao": "Ketchup tradicional Heinz squeeze 397g com super desconto.",
                "categoria": "Outros",
                "preco_original": 14.50,
                "preco_desconto": 7.90,
                "quantidade": 12,
                "dias_validade": 7,
                "imagem": "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d3/Heinz_Tomato_Ketchup%2C_Canada_%28front%29%2C_2026-02-19.jpg/500px-Heinz_Tomato_Ketchup%2C_Canada_%28front%29%2C_2026-02-19.jpg"
            },
            {
                "nome": "Cesta Hortifruti Orgânica 1,5kg",
                "descricao": "Mix de tomates maduros, alface americana e cenouras selecionadas para consumo imediato.",
                "categoria": "Hortifruti",
                "preco_original": 22.00,
                "preco_desconto": 9.50,
                "quantidade": 5,
                "dias_validade": 1,
                "imagem": "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=500&q=80"
            },
            {
                "nome": "Leite em Pó Ninho Forti+ Lata 400g",
                "descricao": "Lata de 400g lacrada de Leite Ninho integral instantâneo.",
                "categoria": "Laticínios",
                "preco_original": 21.90,
                "preco_desconto": 13.90,
                "quantidade": 14,
                "dias_validade": 10,
                "imagem": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b9/Milk_powder_cropped.jpg/500px-Milk_powder_cropped.jpg"
            },
            {
                "nome": "Batata Ruffles Original 76g",
                "descricao": "Pacote de batata frita ondulada Ruffles 76g crocante.",
                "categoria": "Outros",
                "preco_original": 8.90,
                "preco_desconto": 4.50,
                "quantidade": 20,
                "dias_validade": 4,
                "imagem": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/bb/Reducedfatrufflesonplate.JPG/500px-Reducedfatrufflesonplate.JPG"
            },
            {
                "nome": "Achocolatado Nescau Lata 400g",
                "descricao": "Achocolatado em pó Nescau 2.0 lata de 400g.",
                "categoria": "Padaria",
                "preco_original": 11.90,
                "preco_desconto": 6.90,
                "quantidade": 16,
                "dias_validade": 12,
                "imagem": "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/54/Logotipo_Oficial_do_Nescau.png/500px-Logotipo_Oficial_do_Nescau.png"
            },
            {
                "nome": "Croissant Amanteigado pacote c/ 4 un.",
                "descricao": "Lote com validade encerrada ontem — ideal para demonstrar revalidação/desconto extra no painel.",
                "categoria": "Padaria",
                "preco_original": 18.00,
                "preco_desconto": 8.00,
                "quantidade": 4,
                "dias_validade": -1,  # Vencido (para demonstrar aba Vencidos e botão + Desconto)
                "imagem": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=500&q=80"
            }
        ]

        created_products = []
        for p_info in produtos_data:
            val_str = (now_local + timedelta(days=p_info["dias_validade"])).strftime('%Y-%m-%d')
            prod = Produto(
                estabelecimento_id=estab.id,
                nome=p_info["nome"],
                descricao=p_info["descricao"],
                categoria=p_info["categoria"],
                preco_original=p_info["preco_original"],
                preco_desconto=p_info["preco_desconto"],
                quantidade=p_info["quantidade"],
                data_validade=val_str,
                imagem=p_info["imagem"],
                status='DISPONIVEL',
                pausado=False
            )
            db.session.add(prod)
            db.session.flush()
            created_products.append(prod)

            if "leilao" in p_info:
                l_cfg = p_info["leilao"]
                leilao = Leilao(
                    produto_id=prod.id,
                    preco_inicial=l_cfg["preco_inicial"],
                    preco_minimo=l_cfg["preco_minimo"],
                    inicio=now_utc - timedelta(hours=1),
                    fim=now_utc + timedelta(hours=l_cfg["horas_fim"]),
                    intervalo_min=15,
                    ativo=True
                )
                db.session.add(leilao)
                db.session.flush()
                for uid, valor, mins_ago in l_cfg.get("lances", []):
                    db.session.add(Lance(
                        produto_id=prod.id,
                        usuario_id=uid,
                        valor=valor,
                        data_lance=now_utc - timedelta(minutes=mins_ago)
                    ))

        # 5. Favoritos iniciais do João
        for p in created_products[:3]:
            db.session.add(Favorito(usuario_id=joao.id, produto_id=p.id))

        # 6. Criar histórico de pedidos realista (pendentes + retirados nos últimos dias/meses)
        # Pedidos pendentes para demonstração ao vivo no painel do comerciante e histórico do cliente
        pending_specs = [
            (joao.id, created_products[0], 1, 'CF26', now_local - timedelta(minutes=35)),
            (joao.id, created_products[4], 2, 'B9K4', now_local - timedelta(hours=1, minutes=10)),
            (maria.id, created_products[3], 2, 'P7M2', now_local - timedelta(minutes=50)),
        ]
        for uid, prod, qty, code, dt in pending_specs:
            db.session.add(Pedido(
                cliente_id=uid,
                produto_id=prod.id,
                quantidade=qty,
                codigo_reserva=code,
                status='pendente',
                criado_em=dt,
                preco_unitario=prod.preco_desconto
            ))

        # Pedidos retirados distribuídos hoje, nos últimos 7 dias e nos meses anteriores
        completed_specs = [
            # Hoje (em diferentes horários para o filtro "Hoje")
            (joao.id, created_products[2], 3, 'R101', now_local.replace(hour=9, minute=15), 3.49),
            (maria.id, created_products[5], 2, 'R102', now_local.replace(hour=11, minute=30), 6.99),
            (carlos.id, created_products[4], 2, 'R103', now_local.replace(hour=12, minute=20), 9.90),
            # Últimos 6 dias (para preencher todas as barras do gráfico de 7 dias)
            (joao.id, created_products[0], 2, 'R201', now_local - timedelta(days=1, hours=2), 14.90),
            (maria.id, created_products[8], 2, 'R202', now_local - timedelta(days=2, hours=3), 13.90),
            (carlos.id, created_products[5], 4, 'R203', now_local - timedelta(days=3, hours=1), 6.99),
            (joao.id, created_products[4], 3, 'R204', now_local - timedelta(days=4, hours=4), 9.90),
            (maria.id, created_products[6], 3, 'R205', now_local - timedelta(days=5, hours=2), 7.90),
            (carlos.id, created_products[8], 3, 'R206', now_local - timedelta(days=6, hours=3), 13.90),
            # Semanas anteriores deste mês (para o filtro "Mês")
            (joao.id, created_products[0], 3, 'R301', now_local - timedelta(days=9), 14.90),
            (maria.id, created_products[8], 4, 'R302', now_local - timedelta(days=14), 13.90),
            (carlos.id, created_products[4], 5, 'R303', now_local - timedelta(days=19), 9.90),
            (joao.id, created_products[5], 6, 'R304', now_local - timedelta(days=25), 6.99),
            # Meses anteriores do ano (para o filtro "Ano" e cálculo de crescimento)
            (maria.id, created_products[0], 8, 'R401', now_local - timedelta(days=40), 14.90),
            (carlos.id, created_products[8], 10, 'R402', now_local - timedelta(days=70), 13.90),
            (joao.id, created_products[4], 12, 'R403', now_local - timedelta(days=100), 9.90),
            (maria.id, created_products[5], 15, 'R404', now_local - timedelta(days=130), 6.99),
            # 1 pedido expirado para demonstrar a aba "Expirados" no histórico
            (joao.id, created_products[9], 2, 'EXP1', now_local - timedelta(days=3), 4.50),
        ]

        created_completed_orders = []
        for idx, (uid, prod, qty, code, dt, unit_p) in enumerate(completed_specs):
            status = 'expirado' if code == 'EXP1' else 'retirado'
            ped = Pedido(
                cliente_id=uid,
                produto_id=prod.id,
                quantidade=qty,
                codigo_reserva=code,
                status=status,
                criado_em=dt,
                preco_unitario=unit_p
            )
            db.session.add(ped)
            db.session.flush()
            created_completed_orders.append(ped)

        # 7. Avaliações iniciais reais vinculadas aos produtos e pedidos
        reviews_seed = [
            Avaliacao(
                usuario_id=maria.id,
                autor_nome=maria.nome,
                produto_id=created_products[0].id,
                estabelecimento_id=estab.id,
                pedido_id=created_completed_orders[1].id,
                nota=5,
                comentario='Produto fresquinho e embalagem intacta! Economizei quase 50% e fui super bem atendida no balcão.',
                tags='Produto fresquinho, Ótimo desconto, Retirada rápida',
                resposta_lojista='Muito obrigado, Maria! Ficamos felizes em ajudar a economizar evitando o desperdício. Volte sempre! 😊',
                criado_em=now_local - timedelta(hours=5)
            ),
            Avaliacao(
                usuario_id=carlos.id,
                autor_nome=carlos.nome,
                produto_id=created_products[4].id,
                estabelecimento_id=estab.id,
                pedido_id=created_completed_orders[2].id,
                nota=5,
                comentario='Retirada super rápida apenas informando o PIN de 4 dígitos. Qualidade impecável dos frios.',
                tags='Retirada rápida, Embalagem impecável',
                resposta_lojista='Valeu, Carlos! Nosso objetivo é tornar a retirada no balcão o mais ágil possível.',
                criado_em=now_local - timedelta(days=1, hours=2)
            ),
            Avaliacao(
                usuario_id=joao.id,
                autor_nome=joao.nome,
                produto_id=created_products[4].id,
                estabelecimento_id=estab.id,
                pedido_id=created_completed_orders[6].id,
                nota=5,
                comentario='Comprei pelo app e retirei na saída do trabalho. Tudo certinho e muito mais barato que no mercado!',
                tags='Ótimo custo-benefício, Produto fresquinho',
                resposta_lojista=None,
                criado_em=now_local - timedelta(days=3)
            ),
            Avaliacao(
                usuario_id=maria.id,
                autor_nome=maria.nome,
                produto_id=created_products[8].id,
                estabelecimento_id=estab.id,
                pedido_id=created_completed_orders[4].id,
                nota=4,
                comentario='Lata perfeitamente lacrada e bom atendimento. Recomendo muito o aplicativo!',
                tags='Embalagem impecável, Sustentável',
                resposta_lojista=None,
                criado_em=now_local - timedelta(days=2)
            ),
        ]
        db.session.add_all(reviews_seed)

        db.session.commit()
        print("Seed TCC concluído com sucesso! Produtos, leilões ativos, avaliações e histórico de vendas populados.")


if __name__ == '__main__':
    seed_tcc()
