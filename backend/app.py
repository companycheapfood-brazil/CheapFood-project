from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
import random
import string

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'cheapfood.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# ========================
# Models
# ========================

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20))
    tipo = db.Column(db.String(20), nullable=False, default='CLIENTE')
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

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
    data_validade = db.Column(db.String(20), nullable=False)
    imagem = db.Column(db.String(500))
    status = db.Column(db.String(20), nullable=False, default='DISPONIVEL')
    pausado = db.Column(db.Boolean, default=False)
    
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

        # Mapeamento de SVGs profissionais caso a imagem seja NULL
        svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4"/><path d="M2 7h20"/><path d="M22 7v3a2 2 0 0 1-2 2v0a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 16 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 12 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 8 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 4 12v0a2 2 0 0 1-2-2V7"/></svg>'
        if self.categoria:
            cat = self.categoria.lower()
            if "latic" in cat: svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2v20"/><path d="M18 2v20"/><path d="M6 12h12"/><path d="M6 6h12"/><path d="M6 18h12"/></svg>'
            elif "carne" in cat: svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m18 5-2.4 2.4a2 2 0 1 0-2.8 2.8L18.4 16A6.2 6.2 0 0 0 22 12a6.2 6.2 0 0 0-4-7Z"/><path d="M12.8 15.2 6.6 21.4a2 2 0 1 1-2.8-2.8l6.2-6.2"/></svg>'
            elif "padaria" in cat: svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m4.6 13.4-.6 1.5c-.7 1.9.1 3.9 1.8 5.1l.3.2c1.7 1.1 4 .8 5.4-.8l.8-.9c.7-.8 1.9-.8 2.6 0l.8.9c1.4 1.6 3.7 1.9 5.4.8l.3-.2c1.7-1.2 2.5-3.2 1.8-5.1l-.6-1.5"/><path d="M10.5 8.5 9 12"/><path d="M13.5 8.5 15 12"/><path d="m14.5 3.5 1.5 5"/><path d="m9.5 3.5-1.5 5"/><path d="m4.5 5.5 1.5 4"/><path d="m19.5 5.5-1.5 4"/></svg>'
            elif "horti" in cat: svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>'
            elif "bebid" in cat: svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 8 1.75 12.2A2 2 0 0 0 9.71 22h4.58a2 2 0 0 0 1.96-1.8L18 8"/><path d="M5 8h14"/><path d="M7 15a6.47 6.47 0 0 1 5 0 6.47 6.47 0 0 0 5 0"/><path d="m12 8 1-6h2"/></svg>'
            elif "frios" in cat: svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m10.1 2.182a2 2 0 0 1 3.8 0l1.341 4.124a2 2 0 0 0 1.82 1.322h4.32a2 2 0 0 1 1.177 3.62l-3.496 2.54a2 2 0 0 0-.714 2.196l1.34 4.124a2 2 0 0 1-3.076 2.235l-3.496-2.54a2 2 0 0 0-2.352 0l-3.496 2.54a2 2 0 0 1-3.076-2.235l1.34-4.124a2 2 0 0 0-.714-2.196l-3.496-2.54a2 2 0 0 1 1.176-3.62h4.32a2 2 0 0 0 1.82-1.322L10.1 2.182Z"/></svg>'
            elif "congel" in cat: svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="M4 14l8-8 8 8"/><path d="M22 12H2"/></svg>'

        # Calculate discount
        discount = 0
        if self.preco_original and self.preco_original > 0:
            discount = round(((self.preco_original - self.preco_desconto) / self.preco_original) * 100)

        return {
            'id': str(self.id),
            'name': self.nome,
            'quantityLabel': f'{self.quantidade} unidades',
            'price': float(self.preco_desconto),
            'originalPrice': float(self.preco_original),
            'old_price': float(self.preco_original),
            'discountLabel': f'-{discount}% OFF' if discount > 0 else None,
            'expiresLabel': expires_in,
            'expires_in': expires_in,
            'category': self.categoria,
            'store': self.estabelecimento.nome if self.estabelecimento else "Loja Desconhecida",
            'distance': "2km de você",
            'validity': self.data_validade,
            'icon': self.imagem if self.imagem else svg,
            'image': self.imagem if self.imagem else svg,
            'quantity': self.quantidade,
            'reviews': []
        }

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    codigo_reserva = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pendente')
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    cliente = db.relationship('Usuario', backref=db.backref('pedidos', lazy=True))
    produto = db.relationship('Produto', backref=db.backref('pedidos', lazy=True))


# ========================
# Auth Endpoints
# ========================

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'E-mail e senha são obrigatórios'}), 400

    # Check if user already exists
    existing = Usuario.query.filter_by(email=data['email']).first()
    if existing:
        return jsonify({'message': 'Este e-mail já está cadastrado'}), 409

    # Determine role
    role = data.get('role', 'consumer')
    tipo = 'ADMIN' if role == 'merchant' else 'CLIENTE'

    user = Usuario(
        nome=data.get('name', ''),
        email=data['email'],
        senha=generate_password_hash(data['password']),
        telefone=data.get('telefone', ''),
        tipo=tipo
    )
    
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'Conta criada com sucesso!',
        'user': {
            'id': user.id,
            'name': user.nome,
            'email': user.email,
            'role': 'merchant' if user.tipo == 'ADMIN' else 'consumer'
        }
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'E-mail e senha são obrigatórios'}), 400

    user = Usuario.query.filter_by(email=data['email']).first()

    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 401

    # Support both hashed and plain-text passwords (legacy data has plain text)
    if user.senha.startswith('pbkdf2:'):
        password_ok = check_password_hash(user.senha, data['password'])
    else:
        password_ok = (user.senha == data['password'])

    if not password_ok:
        return jsonify({'message': 'Senha incorreta'}), 401

    # Generate a simple token (in production, use JWT)
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'name': user.nome,
            'email': user.email,
            'role': 'merchant' if user.tipo == 'ADMIN' else 'consumer'
        }
    }), 200


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logout realizado com sucesso'}), 200


@app.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email', '') if data else ''
    
    user = Usuario.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'E-mail não encontrado'}), 404

    # In production, send email with reset link
    return jsonify({'message': 'Link de redefinição enviado para seu e-mail'}), 200


@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Dados inválidos'}), 400

    user = Usuario.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    user.senha = generate_password_hash(data['password'])
    db.session.commit()

    return jsonify({'message': 'Senha redefinida com sucesso'}), 200


# ========================
# Products Endpoints
# ========================

@app.route('/api/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')
        data_validade = request.form.get('data_validade')
        
        try:
            preco_original = float(request.form.get('preco_original', 0))
            preco_desconto = float(request.form.get('preco_desconto', 0))
            quantidade = int(request.form.get('quantidade', 0))
        except ValueError:
            preco_original = 0.0
            preco_desconto = 0.0
            quantidade = 0
            
        imagem_filename = None
        if 'imagem' in request.files:
            file = request.files['imagem']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                imagem_filename = f"http://127.0.0.1:5000/static/uploads/{unique_filename}"
                
        # Handle default estabelecimento
        estab = Estabelecimento.query.first()
        if not estab:
            estab = Estabelecimento(
                nome="Estabelecimento Padrão",
                cnpj="00.000.000/0001-00",
                email="loja@exemplo.com",
                endereco="Rua Padrão, 123",
                cidade="Cidade",
                estado="SP"
            )
            db.session.add(estab)
            db.session.commit()
            
        produto = Produto(
            estabelecimento_id=estab.id,
            nome=nome,
            categoria=categoria,
            preco_original=preco_original,
            preco_desconto=preco_desconto,
            quantidade=quantidade,
            data_validade=data_validade,
            imagem=imagem_filename
        )
        
        db.session.add(produto)
        db.session.commit()
        
        return jsonify(produto.to_dict()), 201

    # GET
    produtos = Produto.query.filter(Produto.status == 'DISPONIVEL').all()
    return jsonify([p.to_dict() for p in produtos]), 200


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    produto = Produto.query.get_or_404(product_id)
    return jsonify(produto.to_dict()), 200


@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    items = data.get('items', [])
    
    # Check for a user or use dummy
    user = Usuario.query.first()
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
        
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    for item in items:
        product_id = item.get('id')
        qty = item.get('quantity', 1)
        
        produto = Produto.query.get(product_id)
        if produto and produto.quantidade >= qty:
            produto.quantidade -= qty
            pedido = Pedido(cliente_id=user.id, produto_id=produto.id, quantidade=qty, codigo_reserva=code)
            db.session.add(pedido)
            
    db.session.commit()
    return jsonify({'message': 'Reserva confirmada!', 'code': code}), 200


# ========================
# Merchant Endpoints
# ========================

@app.route('/api/merchant/stats', methods=['GET'])
def get_merchant_stats():
    # Para o prototipo, pegamos o primeiro estabelecimento
    estab = Estabelecimento.query.first()
    if not estab:
        return jsonify({'revenueRecovered': 0, 'activeProducts': 0, 'expiringSoon': 0, 'reservations': 0, 'dailySales': []})

    # Produtos Ativos
    active_products = Produto.query.filter_by(estabelecimento_id=estab.id, status='DISPONIVEL', pausado=False).count()
    
    # Reservas Totais (Pendentes)
    reservations = Pedido.query.join(Produto).filter(Produto.estabelecimento_id == estab.id, Pedido.status == 'pendente').count()
    
    # Revenue (Vendas retiradas)
    revenue = 0
    orders = Pedido.query.join(Produto).filter(Produto.estabelecimento_id == estab.id, Pedido.status == 'retirado').all()
    for o in orders:
        revenue += (o.quantidade * o.produto.preco_desconto)
        
    # Expiring Soon (fake demo calc)
    expiring_soon = Produto.query.filter_by(estabelecimento_id=estab.id).count() # Just show something
    
    # Daily Sales mockup based on orders or just static if no orders
    daily_sales = []
    from datetime import datetime, timedelta
    today = datetime.now().date()
    # sum revenue grouped by day over last 7 days
    sales_map = { (today - timedelta(days=i)): 0 for i in range(6, -1, -1) }
    
    for o in orders:
        if o.criado_em:
            dt = o.criado_em.date() if hasattr(o.criado_em, 'date') else o.criado_em
            if dt in sales_map:
                sales_map[dt] += (o.quantidade * o.produto.preco_desconto)
                
    weekdays = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
    for dt, val in sales_map.items():
        daily_sales.append({'label': weekdays[dt.weekday()], 'value': val})

    
    return jsonify({
        'revenueRecovered': revenue,
        'activeProducts': active_products,
        'expiringSoon': expiring_soon,
        'reservations': reservations,
        'dailySales': daily_sales
    })

@app.route('/api/merchant/orders', methods=['GET'])
def get_merchant_orders():
    estab = Estabelecimento.query.first()
    if not estab:
        return jsonify([])
        
    orders = Pedido.query.join(Produto).filter(Produto.estabelecimento_id == estab.id).order_by(Pedido.criado_em.desc()).all()
    
    result = []
    for o in orders:
        result.append({
            'id': str(o.id),
            'customerName': o.cliente.nome if o.cliente else 'Cliente',
            'productName': o.produto.nome,
            'quantity': o.quantidade,
            'code': o.codigo_reserva,
            'pickupDeadline': o.produto.data_validade,
            'status': o.status
        })
    return jsonify(result)

@app.route('/api/merchant/orders/<int:order_id>/status', methods=['PATCH'])
def update_order_status(order_id):
    data = request.get_json()
    new_status = data.get('status')
    
    order = Pedido.query.get(order_id)
    if not order:
        return jsonify({'message': 'Pedido não encontrado'}), 404
        
    order.status = new_status
    db.session.commit()
    return jsonify({'message': 'Status atualizado', 'status': order.status})

@app.route('/api/merchant/products', methods=['GET'])
def get_merchant_products():
    estab = Estabelecimento.query.first()
    if not estab:
        return jsonify([])
        
    produtos = Produto.query.filter_by(estabelecimento_id=estab.id).order_by(Produto.id.desc()).all()
    
    result = []
    for p in produtos:
        p_dict = p.to_dict()
        # Append merchant specific fields
        p_dict['paused'] = p.pausado
        # Determine status for dashboard
        if p.quantidade <= 0:
            p_dict['status'] = 'vendido'
        elif p.pausado:
            p_dict['status'] = 'pausado'
        elif 'Vencido' in p_dict['expires_in']:
            p_dict['status'] = 'vencido'
        else:
            p_dict['status'] = 'ativo'
            
        result.append(p_dict)
        
    return jsonify(result)

@app.route('/api/merchant/products/<int:product_id>/pause', methods=['PATCH'])
def toggle_product_pause(product_id):
    product = Produto.query.get(product_id)
    if not product:
        return jsonify({'message': 'Produto não encontrado'}), 404
        
    product.pausado = not product.pausado
    db.session.commit()
    return jsonify({'message': 'Produto atualizado', 'paused': product.pausado})





# ========================
# Run
# ========================

if __name__ == '__main__':
    print("\n=== CheapFood Backend ===")
    print("Endpoints disponíveis:")
    print("  POST /api/auth/register")
    print("  POST /api/auth/login")
    print("  POST /api/auth/logout")
    print("  POST /api/auth/forgot-password")
    print("  POST /api/auth/reset-password")
    print("  GET  /api/products")
    print("  GET  /api/products/<id>")
    print("  POST /api/checkout")
    print("========================\n")
    app.run(debug=True, port=5000)



