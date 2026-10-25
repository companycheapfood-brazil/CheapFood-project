from app import app, db, Produto, Estabelecimento as Lojista, Pedido, Leilao
from datetime import datetime, timedelta

def seed():
    with app.app_context():
        # Clear existing
        Pedido.query.delete()
        Leilao.query.delete()
        Produto.query.delete()
        db.session.commit()

        # Retrieve first Lojista or create
        lojista = Lojista.query.first()
        if not lojista:
            lojista = Lojista(
                nome="Supermercado Padrão",
                cnpj="12.345.678/0001-99",
                email="contato@supermercado.com",
                endereco="Av Principal, 1000",
                cidade="São Paulo",
                estado="SP"
            )
            db.session.add(lojista)
            db.session.commit()

        produtos_data = [
            {
                "nome": "Coca-Cola Original 2L",
                "descricao": "Refrigerante Coca-Cola sabor original em garrafa PET de 2 litros.",
                "categoria": "Bebidas",
                "preco_original": 10.99,
                "preco_desconto": 8.50,
                "quantidade": 50,
                "data_validade": (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                "imagem": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/27/Coca_Cola_Flasche_-_Original_Taste.jpg/500px-Coca_Cola_Flasche_-_Original_Taste.jpg"
            },
            {
                "nome": "Nutella 350g",
                "descricao": "Creme de avelã com cacau Nutella pote de 350g.",
                "categoria": "Padaria",
                "preco_original": 25.90,
                "preco_desconto": 19.90,
                "quantidade": 20,
                "data_validade": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
                "imagem": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/73/Nutella_for_breakfast_-_Flickr_-_love.jsc.jpg/500px-Nutella_for_breakfast_-_Flickr_-_love.jsc.jpg",
                "leilao": True,
                "preco_inicial": 25.90,
                "preco_minimo": 15.00,
                "leilao_fim": datetime.utcnow() + timedelta(hours=4)
            },
            {
                "nome": "Ketchup Heinz 397g",
                "descricao": "Ketchup tradicional Heinz em embalagem squeeze de 397g.",
                "categoria": "Outros",
                "preco_original": 12.50,
                "preco_desconto": 9.90,
                "quantidade": 30,
                "data_validade": (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d'),
                "imagem": "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d3/Heinz_Tomato_Ketchup%2C_Canada_%28front%29%2C_2026-02-19.jpg/500px-Heinz_Tomato_Ketchup%2C_Canada_%28front%29%2C_2026-02-19.jpg"
            },
            {
                "nome": "Arroz Tio João 5kg",
                "descricao": "Arroz branco agulhinha Tio João pacote de 5kg.",
                "categoria": "Outros",
                "preco_original": 28.90,
                "preco_desconto": 24.90,
                "quantidade": 100,
                "data_validade": (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d'),
                "imagem": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/7b/White%2C_Brown%2C_Red_%26_Wild_rice.jpg/500px-White%2C_Brown%2C_Red_%26_Wild_rice.jpg"
            },
            {
                "nome": "Feijão Camil 1kg",
                "descricao": "Feijão carioca tipo 1 Camil pacote de 1kg.",
                "categoria": "Outros",
                "preco_original": 8.50,
                "preco_desconto": 6.90,
                "quantidade": 80,
                "data_validade": (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d'),
                "imagem": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/47/Six_bean_varieties_at_a_gene_bank.jpg/500px-Six_bean_varieties_at_a_gene_bank.jpg"
            },
            {
                "nome": "Nescau 400g",
                "descricao": "Achocolatado em pó Nescau lata de 400g.",
                "categoria": "Padaria",
                "preco_original": 11.90,
                "preco_desconto": 8.90,
                "quantidade": 40,
                "data_validade": (datetime.now() + timedelta(days=25)).strftime('%Y-%m-%d'),
                "imagem": "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/54/Logotipo_Oficial_do_Nescau.png/500px-Logotipo_Oficial_do_Nescau.png"
            },
            {
                "nome": "Batata Ruffles 76g",
                "descricao": "Snack de batata frita Ruffles sabor original.",
                "categoria": "Outros",
                "preco_original": 8.90,
                "preco_desconto": 5.50,
                "quantidade": 60,
                "data_validade": (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
                "imagem": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/bb/Reducedfatrufflesonplate.JPG/500px-Reducedfatrufflesonplate.JPG"
            },
            {
                "nome": "Iogurte Danone 170g",
                "descricao": "Iogurte natural Danone copo de 170g.",
                "categoria": "Laticínios",
                "preco_original": 3.50,
                "preco_desconto": 1.90,
                "quantidade": 25,
                "data_validade": (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
                "imagem": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b8/Joghurt.jpg/500px-Joghurt.jpg",
                "leilao": True,
                "preco_inicial": 3.50,
                "preco_minimo": 1.00,
                "leilao_fim": datetime.utcnow() + timedelta(hours=2)
            },
            {
                "nome": "Leite Ninho Lata 400g",
                "descricao": "Leite em pó integral Ninho Forti+ lata 400g.",
                "categoria": "Laticínios",
                "preco_original": 21.90,
                "preco_desconto": 17.50,
                "quantidade": 30,
                "data_validade": (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                "imagem": "https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b9/Milk_powder_cropped.jpg/500px-Milk_powder_cropped.jpg"
            },
            {
                "nome": "Sabão Omo 1.6kg",
                "descricao": "Lava roupas em pó Omo Lavagem Perfeita 1.6kg.",
                "categoria": "Outros",
                "preco_original": 22.90,
                "preco_desconto": 18.90,
                "quantidade": 15,
                "data_validade": (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'),
                "imagem": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/2a/Pralni_pra%C5%A1ek.JPG/500px-Pralni_pra%C5%A1ek.JPG"
            }
        ]

        for p_data in produtos_data:
            produto = Produto(
                estabelecimento_id=lojista.id,
                nome=p_data['nome'],
                descricao=p_data['descricao'],
                categoria=p_data['categoria'],
                preco_original=p_data['preco_original'],
                preco_desconto=p_data['preco_desconto'],
                quantidade=p_data['quantidade'],
                data_validade=p_data['data_validade'],
                imagem=p_data['imagem']
            )
            db.session.add(produto)
            db.session.flush()

            if p_data.get('leilao'):
                leilao = Leilao(
                    produto_id=produto.id,
                    preco_inicial=p_data['preco_inicial'],
                    preco_minimo=p_data['preco_minimo'],
                    inicio=datetime.utcnow(),
                    fim=p_data['leilao_fim']
                )
                db.session.add(leilao)
                
        db.session.commit()
        print("Database seeded with 10 products successfully!")

if __name__ == '__main__':
    seed()
