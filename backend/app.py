from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__name__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../cheapfood.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Estabelecimento(db.Model):
    __tablename__ = 'estabelecimento'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    cnpj = db.Column(db.String(18), unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    cep = db.Column(db.String(9))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    estabelecimento_id = db.Column(db.Integer, db.ForeignKey('estabelecimento.id'), nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(80))
    preco_original = db.Column(db.Float, nullable=False)
    preco_desconto = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_validade = db.Column(db.String(20), nullable=False) # stored as text 'YYYY-MM-DD'
    imagem = db.Column(db.String(500))
    status = db.Column(db.String(20), nullable=False, default='DISPONIVEL')
    
    estabelecimento = db.relationship('Estabelecimento', backref=db.backref('produtos', lazy=True))

    def to_dict(self):
        # Calculate days until expiration
        try:
            validity_date = datetime.strptime(self.data_validade, '%Y-%m-%d').date()
            diff = (validity_date - datetime.now().date()).days
            if diff < 0:
                expires_in = "Vencido"
            elif diff == 0:
                expires_in = "Vence hoje!"
            elif diff == 1:
                expires_in = "Vence amanhã!"
            else:
                expires_in = f"Vence em {diff} dias"
        except:
            expires_in = self.data_validade

        # Mapeamento de emojis caso a imagem seja NULL
        emoji = "🛒"
        if self.categoria:
            cat = self.categoria.lower()
            if "latic" in cat: emoji = "🥛"
            elif "carne" in cat: emoji = "🥩"
            elif "padaria" in cat: emoji = "🍞"
            elif "horti" in cat: emoji = "🥦"
            elif "bebid" in cat: emoji = "🧃"
            elif "frios" in cat: emoji = "🧀"

        return {
            'id': str(self.id),
            'name': self.nome,
            'store': self.estabelecimento.nome if self.estabelecimento else "Loja Desconhecida",
            'price': float(self.preco_desconto),
            'old_price': float(self.preco_original),
            'category': self.categoria,
            'expires_in': expires_in,
            'image': self.imagem if self.imagem else emoji,
            'distance': "2km de você", # Mocado pois não temos lat/long do usuário ainda
            'quantity': self.quantidade
        }


@app.route('/api/products', methods=['GET'])
def get_products():
    produtos = Produto.query.filter(Produto.status == 'DISPONIVEL').all()
    return jsonify([p.to_dict() for p in produtos]), 200

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    produto = Produto.query.get_or_404(product_id)
    return jsonify(produto.to_dict()), 200

@app.route('/api/checkout', methods=['POST'])
def checkout():
    import random
    import string
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return jsonify({'message': 'Reserva confirmada!', 'code': code}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
