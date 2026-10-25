from flask import Flask, request, jsonify, send_from_directory, g
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from functools import wraps
import os
import uuid
from datetime import datetime, timedelta
import math
import random
import string
import tempfile
import json
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
# Força o carregamento do .env do projeto com override=True para prevalecer sobre variáveis do sistema
load_dotenv(os.path.join(basedir, '.env'), override=True)


def _env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in ('1', 'true', 'yes', 'on')

# ========================
# Configuração (via variáveis de ambiente — veja backend/.env.example)
# ========================
DEBUG = _env_bool('FLASK_DEBUG', False)
# Modo demonstração: libera "Restaurar cenário" e mostra o link de redefinição de senha
# na própria tela quando não há SMTP configurado. Desligue em produção real.
DEMO_MODE = _env_bool('DEMO_MODE', True)
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173').rstrip('/')
TOKEN_MAX_AGE = int(os.environ.get('TOKEN_MAX_AGE_HOURS', '168')) * 3600  # 7 dias
RESET_TOKEN_MAX_AGE = 3600  # 1 hora
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

app = Flask(__name__, static_folder=None)

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if not DEBUG:
        print("AVISO: SECRET_KEY não definida — usando chave de desenvolvimento. Defina SECRET_KEY em produção!", flush=True)
    SECRET_KEY = 'dev-secret-key-change-me'
app.config['SECRET_KEY'] = SECRET_KEY

_cors_origins = [o.strip() for o in os.environ.get('CORS_ORIGINS', '*').split(',') if o.strip()]
CORS(app, resources={r"/api/*": {"origins": _cors_origins if _cors_origins != ['*'] else '*'}})

_database_url = os.environ.get('DATABASE_URL') or ('sqlite:///' + os.path.join(basedir, '..', 'cheapfood.db'))
if _database_url.startswith('postgres://'):
    # Render/Heroku entregam "postgres://", mas o SQLAlchemy 2 exige "postgresql://"
    _database_url = _database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = _database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True}
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER') or os.path.join(basedir, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_UPLOAD_MB', '8')) * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

token_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'], salt='cheapfood-auth')
reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'], salt='cheapfood-password-reset')


@app.route('/static/uploads/<path:filename>')
def serve_upload(filename):
    """Serve as imagens enviadas (pasta configurável via UPLOAD_FOLDER)."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, max_age=60 * 60 * 24 * 7)


@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'}), 200


@app.errorhandler(413)
def too_large(_e):
    return jsonify({'message': f"Arquivo muito grande (máx. {os.environ.get('MAX_UPLOAD_MB', '8')} MB)"}), 413


def save_upload(file_storage):
    """Valida a extensão, salva o arquivo em UPLOAD_FOLDER e retorna o caminho relativo público."""
    if not file_storage or not file_storage.filename:
        return None
    filename = secure_filename(file_storage.filename) or 'imagem.jpg'
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError('Formato de imagem não suportado (use PNG, JPG, WEBP ou GIF)')
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    file_storage.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
    return f"/static/uploads/{unique_filename}"


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
    cpf = db.Column(db.String(20))
    foto = db.Column(db.String(500))
    tipo = db.Column(db.String(20), nullable=False, default='CLIENTE')
    criado_em = db.Column(db.DateTime, default=datetime.now)

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
    horario_funcionamento = db.Column(db.String(150), default='Seg a Sáb: 08:00 às 20:00')
    plano = db.Column(db.String(30), default='free')
    formas_pagamento = db.Column(db.String(200), default='PIX, Cartão de Crédito/Débito e Dinheiro')
    notificacoes_ativas = db.Column(db.Boolean, default=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True, index=True)
    categoria = db.Column(db.String(80), default='Padaria e Confeitaria')

    dono = db.relationship('Usuario', backref=db.backref('estabelecimentos', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.nome,
            'category': self.categoria or 'Padaria e Confeitaria',
            'cnpj': self.cnpj or '12.345.678/0001-90',
            'email': self.email,
            'phone': self.telefone or '(14) 99999-0000',
            'address': self.endereco,
            'city': self.cidade,
            'state': self.estado,
            'cep': self.cep or '17500-000',
            'openingHours': self.horario_funcionamento or 'Seg a Sáb: 08:00 às 20:00',
            'plan': self.plano or 'free',
            'paymentMethods': self.formas_pagamento or 'PIX, Cartão de Crédito/Débito e Dinheiro',
            'notificationsEnabled': True if self.notificacoes_ativas is None else bool(self.notificacoes_ativas)
        }

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

        # Preço vigente: sempre o preço do momento
        leilao = self.leilao_ativo()
        current_price = float(self.preco_desconto)

        # Calculate discount
        discount = 0
        if self.preco_original and self.preco_original > 0:
            discount = round(((self.preco_original - current_price) / self.preco_original) * 100)

        # Avaliações reais do banco (prioriza deste produto + avaliações gerais da loja)
        prod_reviews = []
        rating_avg = 5.0
        rating_count = 0
        try:
            store_revs = (
                Avaliacao.query
                .filter_by(estabelecimento_id=self.estabelecimento_id)
                .order_by(Avaliacao.criado_em.desc(), Avaliacao.id.desc())
                .all()
            )
            if store_revs:
                rating_count = len(store_revs)
                rating_avg = round(sum(r.nota for r in store_revs) / rating_count, 1)
                specific = [r.to_dict() for r in store_revs if r.produto_id == self.id]
                others = [r.to_dict() for r in store_revs if r.produto_id != self.id]
                prod_reviews = (specific + others)[:8]
        except Exception:
            prod_reviews = []

        return {
            'id': str(self.id),
            'name': self.nome,
            'description': self.descricao or '',
            'quantityLabel': f'{self.quantidade} unidades',
            'price': current_price,
            'originalPrice': float(self.preco_original),
            'old_price': float(self.preco_original),
            'discountLabel': f'-{discount}% OFF' if discount > 0 else None,
            'expiresLabel': expires_in,
            'expires_in': expires_in,
            'category': self.categoria,
            'store': self.estabelecimento.nome if self.estabelecimento else "Padaria Central",
            'storeAddress': f"{self.estabelecimento.endereco} - {self.estabelecimento.cidade}/{self.estabelecimento.estado}" if self.estabelecimento else "Rua São Paulo, 100 - Centro",
            'distance': "1,2 km de você",
            'validity': self.data_validade,
            'icon': self.imagem if self.imagem else svg,
            'image': self.imagem if self.imagem else svg,
            'quantity': self.quantidade,
            'auction': leilao.to_dict() if leilao else None,
            'ratingAverage': rating_avg,
            'ratingCount': rating_count,
            'reviews': prod_reviews
        }

    def leilao_ativo(self):
        """Retorna o leilão vigente deste produto, ou None.
        Leilão vencido sem lances não conta (o produto volta à venda normal);
        leilão vencido com lances continua até o vencedor resgatar."""
        leilao = getattr(self, 'leilao', None)
        if not leilao or not leilao.ativo:
            return None
        if leilao.encerrado() and not leilao.lance_vencedor():
            return None
        return leilao

    def preco_vigente(self):
        """Preço cobrado agora (preço promocional/Buy Now)."""
        return float(self.preco_desconto)

class Favorito(db.Model):
    __tablename__ = 'favorito'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    
    usuario = db.relationship('Usuario', backref=db.backref('favoritos', lazy=True))
    produto = db.relationship('Produto', backref=db.backref('favoritados', lazy=True))

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    codigo_reserva = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pendente')
    criado_em = db.Column(db.DateTime, default=datetime.now)
    # Preço unitário efetivamente cobrado (no "preço que cai" cada pedido pode ter um preço diferente).
    # Pedidos antigos têm NULL → usar valor_unitario(), que cai para produto.preco_desconto.
    preco_unitario = db.Column(db.Float)

    cliente = db.relationship('Usuario', backref=db.backref('pedidos', lazy=True))
    produto = db.relationship('Produto', backref=db.backref('pedidos', lazy=True))

    def valor_unitario(self):
        if self.preco_unitario is not None:
            return float(self.preco_unitario)
        return float(self.produto.preco_desconto) if self.produto else 0.0


class Avaliacao(db.Model):
    __tablename__ = 'avaliacao'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    autor_nome = db.Column(db.String(100), nullable=False, default='Cliente CheapFood')
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=True)
    estabelecimento_id = db.Column(db.Integer, db.ForeignKey('estabelecimento.id'), nullable=False)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=True)
    nota = db.Column(db.Integer, nullable=False, default=5)
    comentario = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(250))
    resposta_lojista = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.now)

    usuario = db.relationship('Usuario', backref=db.backref('avaliacoes', lazy=True))
    produto = db.relationship('Produto', backref=db.backref('avaliacoes', lazy=True))
    estabelecimento = db.relationship('Estabelecimento', backref=db.backref('avaliacoes', lazy=True))
    pedido = db.relationship('Pedido', backref=db.backref('avaliacoes', lazy=True))

    def to_dict(self):
        author = (self.usuario.nome if self.usuario and self.usuario.nome else self.autor_nome) or 'Cliente'
        parts = [p for p in author.strip().split() if p]
        if len(parts) >= 2:
            initials = (parts[0][0] + parts[-1][0]).upper()
        elif len(parts) == 1:
            initials = parts[0][:2].upper()
        else:
            initials = 'CF'
        return {
            'id': self.id,
            'author': author,
            'initials': initials,
            'rating': int(self.nota or 5),
            'comment': self.comentario or '',
            'tags': [t.strip() for t in (self.tags or '').split(',') if t.strip()],
            'merchantReply': self.resposta_lojista or None,
            'productName': self.produto.nome if self.produto else 'Compra na loja',
            'productId': str(self.produto_id) if self.produto_id else None,
            'orderId': str(self.pedido_id) if self.pedido_id else None,
            'dateFormatted': self.criado_em.strftime('%d/%m/%Y') if self.criado_em else 'Hoje',
        }


LEILAO_INTERVALO_MIN = 15             # o preço cai a cada 15 minutos
LEILAO_DURACOES_HORAS = (1, 2, 4, 8)  # tempo até chegar ao preço mínimo


def _round_cents(value):
    """Arredonda para centavos igual ao Math.round do frontend (evita divergência de 1 centavo)."""
    return math.floor(value * 100 + 0.5) / 100


def _iso_utc(dt):
    return dt.replace(microsecond=0).isoformat() + 'Z' if dt else None


class Lance(db.Model):
    __tablename__ = 'lance'
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_lance = db.Column(db.DateTime, default=datetime.utcnow)

    produto = db.relationship('Produto', backref=db.backref('lances', lazy=True, order_by='Lance.valor.desc()'))
    usuario = db.relationship('Usuario', backref=db.backref('lances', lazy=True))

class Leilao(db.Model):
    """Leilão híbrido ("Compre Agora ou Dê um Lance"): permite lances a partir de um valor, 
    ou compra imediata pelo preço promocional."""
    __tablename__ = 'leilao'
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False, unique=True)
    preco_inicial = db.Column(db.Float, nullable=False)
    preco_minimo = db.Column(db.Float, nullable=False)
    inicio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fim = db.Column(db.DateTime, nullable=False)
    intervalo_min = db.Column(db.Integer, nullable=False, default=15)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    produto = db.relationship('Produto', backref=db.backref('leilao', uselist=False, lazy=True))

    def lance_vencedor(self):
        """Maior lance do produto (o primeiro dado, em caso de empate), ou None."""
        lances = self.produto.lances if self.produto else []
        if not lances:
            return None
        return max(lances, key=lambda l: (l.valor, -l.id))

    def encerrado(self, agora=None):
        return (not self.ativo) or (agora or datetime.utcnow()) >= self.fim

    def to_dict(self):
        # Encontra o maior lance ou usa o preco_inicial
        vencedor = self.lance_vencedor()
        highest_bid = vencedor.valor if vencedor else self.preco_inicial
        bids_list = []
        if self.produto and self.produto.lances:
            for l in self.produto.lances:
                bids_list.append({
                    'id': l.id,
                    'valor': float(l.valor),
                    'usuario': l.usuario.nome if l.usuario else 'Anônimo',
                    'usuario_id': str(l.usuario_id),
                    'data': _iso_utc(l.data_lance)
                })

        return {
            'startPrice': float(self.preco_inicial),
            'minPrice': float(self.preco_minimo),
            'highestBid': float(highest_bid),
            'startTime': _iso_utc(self.inicio),
            'endTime': _iso_utc(self.fim),
            'bids': bids_list,
            'winnerId': str(vencedor.usuario_id) if vencedor else None,
            'ended': self.encerrado(),
        }


# ========================
# Autenticação / Autorização
# ========================

def issue_token(user):
    """Gera um token assinado (com expiração) que identifica o usuário."""
    return token_serializer.dumps({'uid': user.id})


def get_request_user():
    """Retorna o usuário autenticado pelo header `Authorization: Bearer <token>` (ou None).
    O resultado é cacheado por requisição em flask.g."""
    if hasattr(g, '_auth_user'):
        return g._auth_user
    user = None
    header = request.headers.get('Authorization', '')
    if header.lower().startswith('bearer '):
        token = header[7:].strip()
        try:
            data = token_serializer.loads(token, max_age=TOKEN_MAX_AGE)
            uid = data.get('uid') if isinstance(data, dict) else None
            if uid is not None:
                user = db.session.get(Usuario, int(uid))
        except (BadSignature, SignatureExpired, ValueError, TypeError):
            user = None
    g._auth_user = user
    return user


def is_merchant(user):
    return bool(user and user.tipo == 'ADMIN')


def user_role(user):
    return 'merchant' if is_merchant(user) else 'consumer'


def user_payload(user):
    return {
        'id': user.id,
        'name': user.nome,
        'email': user.email,
        'role': user_role(user),
        'telefone': user.telefone,
        'cpf': user.cpf,
        'foto': user.foto,
    }


def verify_password(user, password):
    """Confere a senha (hash Werkzeug; aceita texto puro legado e já converte para hash)."""
    if not user or not password:
        return False
    stored = user.senha or ''
    if stored.startswith(('pbkdf2:', 'scrypt:')):
        return check_password_hash(stored, password)
    if stored == password:
        user.senha = generate_password_hash(password)
        db.session.commit()
        return True
    return False


def get_or_create_store(user):
    """Loja do comerciante logado. Cria uma loja inicial se ele ainda não tiver."""
    estab = Estabelecimento.query.filter_by(usuario_id=user.id).order_by(Estabelecimento.id.asc()).first()
    if estab:
        return estab
    email = user.email
    if Estabelecimento.query.filter_by(email=email).first():
        email = f"loja{user.id}.{user.email}"
    estab = Estabelecimento(
        usuario_id=user.id,
        nome=(user.nome or 'Minha Loja').strip() or 'Minha Loja',
        email=email,
        telefone=user.telefone or None,
        endereco='Endereço não informado',
        cidade='Marília',
        estado='SP',
        plano='free',
    )
    db.session.add(estab)
    db.session.commit()
    return estab


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_request_user()
        if not user:
            return jsonify({'message': 'Sessão expirada. Faça login novamente.'}), 401
        return fn(user, *args, **kwargs)
    return wrapper


def require_merchant(fn):
    """Exige comerciante logado e injeta (user, estab) na view."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_request_user()
        if not user:
            return jsonify({'message': 'Sessão expirada. Faça login novamente.'}), 401
        if not is_merchant(user):
            return jsonify({'message': 'Acesso restrito a comerciantes'}), 403
        return fn(user, get_or_create_store(user), *args, **kwargs)
    return wrapper


def get_owned_product(estab, product_id):
    """Produto pertencente à loja do comerciante, ou None."""
    produto = db.session.get(Produto, product_id)
    if not produto or produto.estabelecimento_id != estab.id:
        return None
    return produto


def send_email(to_address, subject, body):
    """Envia e-mail via SMTP se configurado. Retorna True se enviou."""
    host = os.environ.get('SMTP_HOST')
    if not host:
        return False
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = os.environ.get('SMTP_FROM') or os.environ.get('SMTP_USER') or 'no-reply@cheapfood.app'
        msg['To'] = to_address
        msg.set_content(body)
        port = int(os.environ.get('SMTP_PORT', '587'))
        with smtplib.SMTP(host, port, timeout=15) as smtp:
            smtp.starttls()
            if os.environ.get('SMTP_USER'):
                smtp.login(os.environ['SMTP_USER'], os.environ.get('SMTP_PASSWORD', ''))
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Aviso: falha ao enviar e-mail:", e, flush=True)
        return False


def generate_reservation_code():
    """Código de retirada único entre os pedidos pendentes."""
    alphabet = string.ascii_uppercase + string.digits
    for _ in range(50):
        code = ''.join(random.choices(alphabet, k=4))
        exists = Pedido.query.filter(Pedido.codigo_reserva == code, Pedido.status == 'pendente').first()
        if not exists:
            return code
    return ''.join(random.choices(alphabet, k=6))


# ========================
# Auth Endpoints
# ========================

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}

    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    if not email or not password:
        return jsonify({'message': 'E-mail e senha são obrigatórios'}), 400
    if len(password) < 6:
        return jsonify({'message': 'A senha deve ter pelo menos 6 caracteres'}), 400

    # Check if user already exists
    existing = Usuario.query.filter(db.func.lower(Usuario.email) == email).first()
    if existing:
        return jsonify({'message': 'Este e-mail já está cadastrado'}), 409

    # Determine role
    role = data.get('role', 'consumer')
    tipo = 'ADMIN' if role == 'merchant' else 'CLIENTE'

    user = Usuario(
        nome=(data.get('name') or '').strip(),
        email=email,
        senha=generate_password_hash(password),
        telefone=data.get('telefone', ''),
        tipo=tipo
    )

    db.session.add(user)
    db.session.commit()

    if tipo == 'ADMIN':
        estab = get_or_create_store(user)
        if data.get('storeName'):
            estab.nome = data['storeName'].strip()
            db.session.commit()

    return jsonify({
        'message': 'Conta criada com sucesso!',
        'user': user_payload(user)
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}

    email = (data.get('email') or '').strip().lower()
    if not email or not data.get('password'):
        return jsonify({'message': 'E-mail e senha são obrigatórios'}), 400

    user = Usuario.query.filter(db.func.lower(Usuario.email) == email).first()

    # Mensagem genérica para não revelar quais e-mails estão cadastrados
    if not user or not verify_password(user, data['password']):
        return jsonify({'message': 'E-mail ou senha incorretos'}), 401

    return jsonify({
        'token': issue_token(user),
        'user': user_payload(user)
    }), 200


@app.route('/api/auth/me', methods=['GET'])
@require_auth
def auth_me(user):
    return jsonify({'user': user_payload(user)}), 200


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logout realizado com sucesso'}), 200


@app.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    generic_msg = 'Se o e-mail estiver cadastrado, você receberá um link para redefinir a senha.'

    user = Usuario.query.filter(db.func.lower(Usuario.email) == email).first() if email else None
    if not user:
        return jsonify({'message': generic_msg}), 200

    # O token inclui um trecho do hash atual da senha → fica inválido após o uso.
    token = reset_serializer.dumps({'uid': user.id, 'h': (user.senha or '')[-12:]})
    reset_url = f"{FRONTEND_URL}/reset-password?token={token}"

    sent = send_email(
        user.email,
        'CheapFood - Redefinição de senha',
        f"Olá, {user.nome or 'cliente'}!\n\nPara redefinir sua senha, acesse o link abaixo (válido por 1 hora):\n{reset_url}\n\n"
        "Se você não solicitou, ignore este e-mail.\n\nEquipe CheapFood"
    )

    response = {'message': generic_msg, 'emailSent': sent}
    if not sent and DEMO_MODE:
        # Sem SMTP configurado: em modo demonstração devolvemos o link para a própria tela.
        response['resetUrl'] = reset_url
        response['resetToken'] = token
    return jsonify(response), 200


@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json(silent=True) or {}
    token = data.get('token') or ''
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not password or len(password) < 6:
        return jsonify({'message': 'A senha deve ter pelo menos 6 caracteres'}), 400

    user = None
    if token:
        try:
            payload = reset_serializer.loads(token, max_age=RESET_TOKEN_MAX_AGE)
            user = db.session.get(Usuario, int(payload.get('uid', 0)))
            if not user or (user.senha or '')[-12:] != payload.get('h'):
                return jsonify({'message': 'Este link já foi utilizado ou é inválido.'}), 400
        except SignatureExpired:
            return jsonify({'message': 'Este link expirou. Solicite uma nova redefinição.'}), 400
        except BadSignature:
            return jsonify({'message': 'Link inválido. Solicite uma nova redefinição de senha.'}), 400
    elif email and DEMO_MODE:
        user = Usuario.query.filter(db.func.lower(Usuario.email) == email).first()
        if not user:
            return jsonify({'message': 'Usuário não encontrado'}), 404
    else:
        return jsonify({'message': 'Token de redefinição obrigatório'}), 400

    user.senha = generate_password_hash(password)
    db.session.commit()

    return jsonify({'message': 'Senha redefinida com sucesso'}), 200


# ========================
# AI / Image Analysis
# ========================

def _smart_fallback_image_analysis(filename: str):
    fname = (filename or '').lower()
    validade_padrao = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
    presets = [
        (['leite', 'italac', 'ninho', 'piracanjuba'], {
            'nome': 'Leite UHT Integral 1L',
            'categoria': 'Laticínios',
            'data_validade': validade_padrao,
            'descricao': 'Caixa de leite integral 1 litro lacrada, lote próximo ao vencimento em excelente estado.',
            'preco_original': 6.49,
            'preco_desconto': 3.49,
        }),
        (['iogurte', 'danone', 'vigor', 'grego'], {
            'nome': 'Iogurte Grego Natural 170g',
            'categoria': 'Laticínios',
            'data_validade': validade_padrao,
            'descricao': 'Iogurte refrigerado cremoso, ideal para consumo imediato.',
            'preco_original': 5.50,
            'preco_desconto': 2.49,
        }),
        (['queijo', 'mussarela', 'prato', 'presunto', 'frios'], {
            'nome': 'Queijo Mussarela Fatiado 300g',
            'categoria': 'Frios',
            'data_validade': validade_padrao,
            'descricao': 'Bandeja de queijo mussarela fatiado e refrigerado, pronto para lanches.',
            'preco_original': 18.90,
            'preco_desconto': 9.90,
        }),
        (['coca', 'refrigerante', 'suco', 'bebida', 'guarana'], {
            'nome': 'Refrigerante Original 2L',
            'categoria': 'Bebidas',
            'data_validade': validade_padrao,
            'descricao': 'Garrafa PET 2 litros lacrada com super desconto.',
            'preco_original': 11.99,
            'preco_desconto': 6.90,
        }),
        (['fruta', 'tomate', 'alface', 'banana', 'morango', 'hortifruti'], {
            'nome': 'Bandeja de Morangos Frescos 250g',
            'categoria': 'Hortifruti',
            'data_validade': validade_padrao,
            'descricao': 'Morangos selecionados maduros, ideais para consumo hoje ou preparo de doces.',
            'preco_original': 12.90,
            'preco_desconto': 5.90,
        }),
        (['nutella', 'avela', 'creme de avela'], {
            'nome': 'Creme de Avelã Nutella 140g',
            'categoria': 'Padaria',
            'data_validade': validade_padrao,
            'descricao': 'Creme de avelã original com cacau, ideal para pães, torradas e sobremesas.',
            'preco_original': 12.90,
            'preco_desconto': 6.90,
        }),
        (['bolo', 'croissant', 'pao', 'baguete', 'sonho'], {
            'nome': 'Kit Pães Artesanais & Croissants (400g)',
            'categoria': 'Padaria',
            'data_validade': validade_padrao,
            'descricao': 'Fornada artesanal fresca do dia, casca crocante e macia por dentro.',
            'preco_original': 19.90,
            'preco_desconto': 8.90,
        }),
    ]
    for keywords, data in presets:
        if any(k in fname for k in keywords):
            return data

    return {
        'nome': 'Combo Surpresa da Padaria (Fornada do Dia)',
        'categoria': 'Padaria',
        'data_validade': validade_padrao,
        'descricao': 'Seleção especial de pães, salgados e doces frescos do dia com super desconto contra o desperdício.',
        'preco_original': 24.90,
        'preco_desconto': 11.90,
    }


@app.route('/api/merchant/analyze-image', methods=['POST'])
@require_merchant
def analyze_image(_user, _estab):
    file = request.files.get('image') or request.files.get('imagem')
    if not file or file.filename == '':
        return jsonify({'message': 'Nenhuma imagem enviada'}), 400

    fallback_data = _smart_fallback_image_analysis(file.filename)

    # Garante o carregamento do .env local do projeto com override=True
    load_dotenv(os.path.join(basedir, '.env'), override=True)
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("Aviso: GEMINI_API_KEY não encontrada, usando fallback.", flush=True)
        return jsonify(fallback_data), 200

    try:
        import PIL.Image
        import io
        import base64
        import urllib.request

        img = PIL.Image.open(file.stream)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")
        img.thumbnail((800, 800), PIL.Image.Resampling.LANCZOS)

        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=85)
        img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        prompt = """
        Analise com precisão a imagem do alimento ou embalagem e retorne APENAS um JSON válido com estas chaves:
        - "nome": Nome comercial exato do produto, marca e peso/volume visível na embalagem (ex: "Creme de Avelã Nutella 140g", "Leite Integral Italac 1L").
        - "categoria": Escolha exatamente UMA dentre: "Laticínios", "Padaria", "Hortifruti", "Bebidas", "Carnes", "Frios", "Congelados", "Outros". (Doces, cremes de avelã, pães e bolos entram em "Padaria" ou "Outros").
        - "data_validade": Se houver data de validade legível no rótulo, retorne em "YYYY-MM-DD"; caso contrário retorne "".
        - "descricao": Descrição curta, fiel ao produto da foto e atrativa para venda com desconto contra desperdício.
        - "preco_original": Preço médio de mercado no Brasil em número decimal (ex: 14.90).
        - "preco_desconto": Preço promocional sugerido com cerca de 45% de desconto em número decimal (ex: 7.90).
        """

        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                ]
            }],
            "generationConfig": {
                "response_mime_type": "application/json"
            }
        }

        candidate_models = [
            "gemini-3-flash-preview",
            "gemini-3.5-flash-lite",
            "gemini-3.1-flash-lite",
            "gemini-flash-latest",
        ]

        dados = None
        last_err = None

        for model_name in candidate_models:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=18) as resp:
                    resp_json = json.loads(resp.read().decode("utf-8"))
                    raw_text = resp_json['candidates'][0]['content']['parts'][0]['text'].strip()
                    if raw_text.startswith("```"):
                        raw_text = raw_text.strip("`")
                        if raw_text.lower().startswith("json"):
                            raw_text = raw_text[4:].strip()
                    dados = json.loads(raw_text)
                    if isinstance(dados, list) and len(dados) > 0:
                        dados = dados[0]
                    if dados and isinstance(dados, dict):
                        print(f"Sucesso na análise da imagem com modelo {model_name}!", flush=True)
                        break
            except Exception as model_err:
                last_err = model_err
                print(f"Tentativa com modelo {model_name} falhou: {model_err}", flush=True)
                continue

        if not dados or not isinstance(dados, dict):
            raise last_err or RuntimeError("Nenhum modelo Gemini retornou resposta válida")

        valid_categories = ["Laticínios", "Padaria", "Hortifruti", "Bebidas", "Carnes", "Frios", "Congelados", "Outros"]
        cat = dados.get("categoria")
        if cat not in valid_categories:
            if cat in ("Doces", "Sobremesas", "Guloseimas"):
                dados["categoria"] = "Padaria"
            else:
                dados["categoria"] = "Outros"

        # Se a data de validade não estiver visível na foto (ex: pote visto de frente),
        # sugere a validade padrão anti-desperdício para não deixar o campo vazio
        if not dados.get('data_validade'):
            dados['data_validade'] = fallback_data.get('data_validade')

        if not dados.get('preco_original'):
            dados['preco_original'] = fallback_data.get('preco_original', 12.90)
        if not dados.get('preco_desconto'):
            dados['preco_desconto'] = fallback_data.get('preco_desconto', 6.90)

        return jsonify(dados), 200

    except Exception as e:
        print("Aviso: usando fallback inteligente de IA devido a erro:", e, flush=True)
        return jsonify(fallback_data), 200


# ========================
# Products Endpoints
# ========================

@app.route('/api/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        user = get_request_user()
        if not user:
            return jsonify({'message': 'Sessão expirada. Faça login novamente.'}), 401
        if not is_merchant(user):
            return jsonify({'message': 'Acesso restrito a comerciantes'}), 403
        estab = get_or_create_store(user)

        nome = (request.form.get('nome') or '').strip()
        categoria = request.form.get('categoria')
        data_validade = request.form.get('data_validade')
        if not nome or not data_validade:
            return jsonify({'message': 'Nome e data de validade são obrigatórios'}), 400
        
        try:
            preco_original = float(request.form.get('preco_original', 0))
            preco_desconto = float(request.form.get('preco_desconto', 0))
            quantidade = int(request.form.get('quantidade', 0))
        except ValueError:
            preco_original = 0.0
            preco_desconto = 0.0
            quantidade = 0

        # ---- Modo "preço que cai" (leilão holandês) ----
        leilao_params = None
        if (request.form.get('modo') or '').upper() == 'LEILAO':
            try:
                preco_inicial = round(float(request.form.get('preco_inicial', 0)), 2)
                preco_minimo = round(float(request.form.get('preco_minimo', 0)), 2)
                data_fim_leilao_str = request.form.get('data_fim_leilao')
                if not data_fim_leilao_str:
                    return jsonify({'message': 'Data e hora de fim do leilão não fornecida'}), 400
                from datetime import datetime
                import datetime as dt_mod
                
                # Treat the input datetime-local as UTC if sending from JS toISOString()
                clean_str = data_fim_leilao_str.replace('Z', '+00:00')
                if len(clean_str) == 16:
                    clean_str += ":00"
                leilao_fim = datetime.fromisoformat(clean_str)
                # Convert to naive UTC if it has tzinfo
                if leilao_fim.tzinfo:
                    leilao_fim = leilao_fim.astimezone(dt_mod.timezone.utc).replace(tzinfo=None)
            except ValueError:
                return jsonify({'message': 'Valores do leilão inválidos ou data mal formatada'}), 400

            if preco_inicial <= 0:
                return jsonify({'message': 'O lance inicial deve ser maior que zero'}), 400
            if preco_minimo < preco_inicial:
                return jsonify({'message': 'O preço de compra imediata deve ser maior ou igual ao lance inicial'}), 400
            
            if leilao_fim <= datetime.utcnow():
                return jsonify({'message': 'A data de fim do leilão deve estar no futuro'}), 400

            leilao_params = (preco_inicial, preco_minimo, leilao_fim)
            
        try:
            imagem_filename = save_upload(request.files.get('imagem') or request.files.get('image'))
        except ValueError as e:
            return jsonify({'message': str(e)}), 400
            
        produto = Produto(
            estabelecimento_id=estab.id,
            nome=nome,
            descricao=request.form.get('descricao') or None,
            categoria=categoria,
            preco_original=preco_original,
            preco_desconto=preco_desconto,
            quantidade=quantidade,
            data_validade=data_validade,
            imagem=imagem_filename
        )
        
        db.session.add(produto)
        db.session.flush()  # garante produto.id para o leilão

        if leilao_params:
            preco_inicial, preco_minimo, leilao_fim = leilao_params
            inicio = datetime.utcnow().replace(microsecond=0)
            db.session.add(Leilao(
                produto_id=produto.id,
                preco_inicial=preco_inicial,
                preco_minimo=preco_minimo,
                inicio=inicio,
                fim=leilao_fim,
                intervalo_min=LEILAO_INTERVALO_MIN,
            ))

        db.session.commit()
        
        return jsonify(produto.to_dict()), 201

    # GET
    produtos = Produto.query.filter(Produto.status == 'DISPONIVEL', Produto.pausado.isnot(True)).all()
    return jsonify([p.to_dict() for p in produtos]), 200


@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Algoritmo de recomendação personalizada estilo iFood:
    Combina histórico de compras (Pedido), favoritos (Favorito), lances (Lance),
    avaliações positivas (Avaliacao), interações recentes da sessão e fator de oportunidade (% OFF + validade).
    Sem login, usa apenas as interações recentes da sessão + oportunidade."""
    user = get_request_user()

    recent_cats = [c.strip() for c in (request.args.get('recentCategories') or '').split(',') if c.strip()]
    recent_ids = [i.strip() for i in (request.args.get('recentIds') or '').split(',') if i.strip()]

    cat_scores = {}
    ordered_product_counts = {}
    favorited_ids = set()
    bid_ids = set()

    if user:
        user_orders = Pedido.query.filter_by(cliente_id=user.id).order_by(Pedido.criado_em.desc()).all()
        for o in user_orders:
            if o.status != 'expirado':
                ordered_product_counts[o.produto_id] = ordered_product_counts.get(o.produto_id, 0) + 1
                if o.produto and o.produto.categoria:
                    cat_scores[o.produto.categoria] = cat_scores.get(o.produto.categoria, 0.0) + 5.0

        user_favs = Favorito.query.filter_by(usuario_id=user.id).all()
        for f in user_favs:
            favorited_ids.add(f.produto_id)
            if f.produto and f.produto.categoria:
                cat_scores[f.produto.categoria] = cat_scores.get(f.produto.categoria, 0.0) + 4.0

        user_bids = Lance.query.filter_by(usuario_id=user.id).all()
        for b in user_bids:
            bid_ids.add(b.produto_id)
            if b.produto and b.produto.categoria:
                cat_scores[b.produto.categoria] = cat_scores.get(b.produto.categoria, 0.0) + 3.0

        user_revs = Avaliacao.query.filter_by(usuario_id=user.id).all()
        for r in user_revs:
            if (r.nota or 5) >= 4 and r.produto and r.produto.categoria:
                cat_scores[r.produto.categoria] = cat_scores.get(r.produto.categoria, 0.0) + 3.0

    for idx, rc in enumerate(recent_cats):
        weight = max(2.0, 5.5 - idx * 1.0)
        cat_scores[rc] = cat_scores.get(rc, 0.0) + weight

    top_categories = [
        cat for cat, _ in sorted(cat_scores.items(), key=lambda item: item[1], reverse=True)
    ][:3]

    produtos = Produto.query.filter(
        Produto.status == 'DISPONIVEL',
        Produto.pausado.isnot(True),
        Produto.quantidade > 0
    ).all()

    scored_items = []
    buy_again_items = []

    for p in produtos:
        p_dict = p.to_dict()
        if 'Vencido' in (p_dict.get('expires_in') or ''):
            continue

        cat = p.categoria or 'Outros'
        score = cat_scores.get(cat, 0.0)

        if p.id in ordered_product_counts:
            score += 4.5 * min(3, ordered_product_counts[p.id])
        if p.id in favorited_ids:
            score += 4.0
        if p.id in bid_ids:
            score += 3.5
        if str(p.id) in recent_ids:
            score += 3.5

        disc_pct = 0
        if p.preco_original and p.preco_original > 0:
            disc_pct = round(((p.preco_original - p.preco_desconto) / p.preco_original) * 100)
        score += (disc_pct / 15.0)

        exp_lower = (p_dict.get('expires_in') or '').lower()
        if 'hoje' in exp_lower or 'amanh' in exp_lower:
            score += 2.0

        # Motivo explicativo estilo iFood (sem emojis, com identificador de ícone SVG)
        if p.id in favorited_ids:
            reason = "Nos seus favoritos"
            reason_icon = "heart"
        elif cat in recent_cats[:2]:
            reason = f"Visto recentemente em {cat}"
            reason_icon = "eye"
        elif p.id in ordered_product_counts:
            reason = f"Você já pediu {ordered_product_counts[p.id]}x"
            reason_icon = "repeat"
        elif cat_scores.get(cat, 0) >= 4.0:
            reason = f"Porque você curte {cat}"
            reason_icon = "sparkles"
        elif disc_pct >= 45:
            reason = f"Super desconto (-{disc_pct}%)"
            reason_icon = "flame"
        else:
            reason = "Sugestão para o seu perfil"
            reason_icon = "star"

        match_pct = min(99, max(82, int(82 + min(17, score * 0.75))))

        p_dict['affinityScore'] = round(score, 2)
        p_dict['recommendationReason'] = reason
        p_dict['recommendationIcon'] = reason_icon
        p_dict['matchPercent'] = match_pct
        p_dict['timesOrdered'] = ordered_product_counts.get(p.id, 0)

        scored_items.append(p_dict)
        if p.id in ordered_product_counts:
            buy_again_items.append(p_dict)

    scored_items.sort(key=lambda x: (x['affinityScore'], x.get('ratingAverage', 5)), reverse=True)
    buy_again_items.sort(key=lambda x: x['timesOrdered'], reverse=True)

    return jsonify({
        'userName': user.nome.split()[0] if (user and user.nome) else 'Você',
        'topCategories': top_categories if top_categories else ['Laticínios', 'Padaria', 'Frios'],
        'forYou': scored_items[:6],
        'buyAgain': buy_again_items[:4],
        'rankedProducts': scored_items,
    }), 200


import os
from werkzeug.utils import secure_filename

@app.route('/api/products/<int:product_id>', methods=['GET', 'PUT'])
def get_product(product_id):
    produto = Produto.query.get_or_404(product_id)
    
    if request.method == 'PUT':
        user = get_request_user()
        if not user:
            return jsonify({'message': 'Sessão expirada. Faça login novamente.'}), 401
        if not is_merchant(user) or produto.estabelecimento_id != get_or_create_store(user).id:
            return jsonify({'message': 'Você não tem permissão para editar este produto'}), 403

        if request.is_json:
            data = request.get_json(silent=True) or {}
        else:
            data = request.form

        try:
            if 'nome' in data: produto.nome = data['nome']
            if 'descricao' in data: produto.descricao = data['descricao']
            if 'categoria' in data: produto.categoria = data['categoria']
            if 'preco_original' in data: produto.preco_original = float(data['preco_original'])
            if 'preco_desconto' in data: produto.preco_desconto = float(data['preco_desconto'])
            if 'quantidade' in data:
                produto.quantidade = int(data['quantidade'])
                if produto.quantidade > 0 and produto.status == 'ESGOTADO':
                    produto.status = 'DISPONIVEL'
            if 'data_validade' in data: produto.data_validade = data['data_validade']
        except (TypeError, ValueError):
            db.session.rollback()
            return jsonify({'message': 'Valores numéricos inválidos'}), 400

        # Handle image if uploaded (accept both 'image' and 'imagem')
        try:
            new_image = save_upload(request.files.get('imagem') or request.files.get('image'))
        except ValueError as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 400
        if new_image:
            produto.imagem = new_image
                
        db.session.commit()
        return jsonify(produto.to_dict()), 200
        
    return jsonify(produto.to_dict()), 200


@app.route('/api/checkout', methods=['POST'])
def checkout():
    user = get_request_user()
    if not user:
        return jsonify({'message': 'Faça login para finalizar a reserva'}), 401

    data = request.get_json(silent=True) or {}
    items = data.get('items', [])
    if not items:
        return jsonify({'message': 'Carrinho vazio'}), 400

    # Valida todos os itens antes de gravar (tudo ou nada)
    to_reserve = []
    for item in items:
        try:
            product_id = int(item.get('id'))
            qty = int(item.get('quantity', 1))
        except (TypeError, ValueError):
            return jsonify({'message': 'Item inválido no carrinho'}), 400

        produto = Produto.query.get(product_id)
        if not produto or produto.status != 'DISPONIVEL' or produto.pausado:
            return jsonify({'message': 'Um dos produtos não está mais disponível'}), 409
        if qty <= 0 or produto.quantidade < qty:
            return jsonify({'message': f'Estoque insuficiente para "{produto.nome}" (restam {produto.quantidade})'}), 409
        to_reserve.append((produto, qty))

    code = generate_reservation_code()

    now = datetime.utcnow()
    total = 0.0
    total_original = 0.0
    reserved_items = []
    store_name = "Padaria Central"
    store_address = "Rua São Paulo, 100 - Centro, Marília/SP"

    for produto, qty in to_reserve:
        unit_price = float(produto.preco_desconto)
        orig_price = float(produto.preco_original or unit_price)

        if produto.estabelecimento:
            store_name = produto.estabelecimento.nome
            store_address = f"{produto.estabelecimento.endereco} - {produto.estabelecimento.cidade}/{produto.estabelecimento.estado}"

        leilao = produto.leilao_ativo()
        if leilao and leilao.encerrado(now):
            vencedor = leilao.lance_vencedor()
            if vencedor and vencedor.usuario_id == user.id:
                if qty != 1:
                    db.session.rollback()
                    return jsonify({'message': 'O lote arrematado no leilão é de 1 unidade'}), 400
                unit_price = float(vencedor.valor)
                leilao.ativo = False
            elif vencedor and produto.quantidade - qty < 1:
                db.session.rollback()
                return jsonify({'message': f'O leilão de "{produto.nome}" foi arrematado por outro usuário'}), 403

        total += unit_price * qty
        total_original += orig_price * qty

        produto.quantidade -= qty
        if produto.quantidade <= 0:
            produto.status = 'ESGOTADO'
        db.session.add(Pedido(cliente_id=user.id, produto_id=produto.id, quantidade=qty,
                              codigo_reserva=code, preco_unitario=unit_price))
        reserved_items.append({
            'id': str(produto.id),
            'name': produto.nome,
            'quantity': qty,
            'price': round(unit_price, 2),
            'originalPrice': round(orig_price, 2),
            'total': round(unit_price * qty, 2)
        })

    db.session.commit()
    return jsonify({
        'message': 'Reserva confirmada!',
        'code': code,
        'total': round(total, 2),
        'savings': round(max(0.0, total_original - total), 2),
        'store': store_name,
        'storeAddress': store_address,
        'items': reserved_items
    }), 200


@app.route('/api/orders/code/<string:code>', methods=['GET'])
@require_auth
def get_order_by_code(user, code):
    query = Pedido.query.filter(db.func.upper(Pedido.codigo_reserva) == code.upper())
    if is_merchant(user):
        estab = get_or_create_store(user)
        query = query.join(Produto, Pedido.produto_id == Produto.id).filter(Produto.estabelecimento_id == estab.id)
    else:
        query = query.filter(Pedido.cliente_id == user.id)
    pedidos = query.order_by(Pedido.id.desc()).all()
    if not pedidos:
        return jsonify({'message': 'Reserva não encontrada'}), 404
    # Mesmo código pode ter sido reutilizado no passado: fica com a reserva mais recente
    # (itens do mesmo checkout: mesmo cliente, criados com poucos segundos de diferença)
    latest = pedidos[0]
    if latest.criado_em:
        pedidos = [
            p for p in pedidos
            if p.cliente_id == latest.cliente_id and p.criado_em
            and abs((latest.criado_em - p.criado_em).total_seconds()) <= 120
        ]
    pedidos = sorted(pedidos, key=lambda p: p.id)

    first = pedidos[0]
    estab = first.produto.estabelecimento if first.produto else Estabelecimento.query.first()
    store_name = estab.nome if estab else 'Padaria Central'
    store_address = f"{estab.endereco} - {estab.cidade}/{estab.estado}" if estab else 'Rua São Paulo, 100 - Centro'
    opening_hours = (estab.horario_funcionamento if estab and estab.horario_funcionamento else 'Seg a Sáb: 08:00 às 20:00')

    items = []
    total = 0.0
    total_original = 0.0
    for p in pedidos:
        unit_price = p.valor_unitario()
        orig_price = float(p.produto.preco_original) if (p.produto and p.produto.preco_original) else unit_price
        line_total = round(unit_price * p.quantidade, 2)
        total += line_total
        total_original += orig_price * p.quantidade
        items.append({
            'id': str(p.produto_id),
            'name': p.produto.nome if p.produto else 'Produto reservado',
            'quantity': p.quantidade,
            'price': round(unit_price, 2),
            'originalPrice': round(orig_price, 2),
            'total': line_total
        })

    created_dt = first.criado_em or datetime.now()
    pickup_limit = (created_dt + timedelta(hours=3)).strftime('%H:%M')

    return jsonify({
        'code': first.codigo_reserva,
        'status': first.status,
        'createdAt': created_dt.strftime('%d/%m/%Y às %H:%M'),
        'pickupDeadline': f"Hoje até {pickup_limit} (ou horário limite da loja)",
        'store': store_name,
        'storeAddress': store_address,
        'openingHours': opening_hours,
        'total': round(total, 2),
        'savings': round(max(0.0, total_original - total), 2),
        'items': items
    }), 200


@app.route('/api/orders', methods=['GET'])
def get_user_orders():
    user = get_request_user()
    if not user:
        return jsonify({'message': 'Usuário não autenticado'}), 401

    pedidos = (
        Pedido.query
        .filter_by(cliente_id=user.id)
        .order_by(Pedido.criado_em.desc())
        .all()
    )

    result = []
    for p in pedidos:
        unit_price = p.valor_unitario()
        orig_price = float(p.produto.preco_original) if (p.produto and p.produto.preco_original) else unit_price
        savings = round(max(0.0, (orig_price - unit_price) * p.quantidade), 2)
        existing_rev = Avaliacao.query.filter_by(pedido_id=p.id).first()
        result.append({
            'id': str(p.id),
            'productId': str(p.produto_id) if p.produto_id else None,
            'productName': p.produto.nome if p.produto else 'Produto indisponível',
            'productImage': p.produto.imagem if p.produto else None,
            'store': p.produto.estabelecimento.nome if (p.produto and p.produto.estabelecimento) else 'Padaria Central',
            'storeAddress': f"{p.produto.estabelecimento.endereco} - {p.produto.estabelecimento.cidade}/{p.produto.estabelecimento.estado}" if (p.produto and p.produto.estabelecimento) else 'Rua São Paulo, 100 - Marília/SP',
            'quantity': p.quantidade,
            'code': p.codigo_reserva,
            'status': p.status,  # pendente, retirado, expirado
            'price': unit_price,
            'originalPrice': orig_price,
            'savings': savings,
            'total': round(unit_price * p.quantidade, 2),
            'createdAt': p.criado_em.strftime('%d/%m/%Y %H:%M') if p.criado_em else '',
            'dateFormatted': p.criado_em.strftime('%d/%m às %H:%M') if p.criado_em else '',
            'review': existing_rev.to_dict() if existing_rev else None,
        })

    return jsonify(result), 200


# ========================
# Reviews Endpoints
# ========================

@app.route('/api/products/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    produto = Produto.query.get(product_id)
    if not produto:
        return jsonify({'message': 'Produto não encontrado'}), 404

    store_revs = (
        Avaliacao.query
        .filter_by(estabelecimento_id=produto.estabelecimento_id)
        .order_by(Avaliacao.criado_em.desc(), Avaliacao.id.desc())
        .all()
    )
    rating_count = len(store_revs)
    rating_avg = round(sum(r.nota for r in store_revs) / rating_count, 1) if rating_count > 0 else 5.0
    specific = [r.to_dict() for r in store_revs if r.produto_id == produto.id]
    others = [r.to_dict() for r in store_revs if r.produto_id != produto.id]

    return jsonify({
        'ratingAverage': rating_avg,
        'ratingCount': rating_count,
        'reviews': (specific + others)[:15]
    }), 200


@app.route('/api/reviews', methods=['POST'])
@require_auth
def create_review(user):
    data = request.get_json(silent=True) or {}

    try:
        nota = int(data.get('rating', 5) or 5)
    except (TypeError, ValueError):
        nota = 5
    nota = max(1, min(5, nota))
    comentario = (data.get('comment') or '').strip()[:1000]
    tags_list = data.get('tags') or []
    tags_str = ', '.join(t.strip() for t in tags_list if str(t).strip()) if isinstance(tags_list, list) else str(tags_list or '')

    if not comentario and tags_str:
        comentario = f"Pontos destacados: {tags_str}."
    elif not comentario:
        comentario = "Excelente experiência pelo CheapFood! Produto dentro da validade e ótimo preço."

    order_id = data.get('orderId')
    product_id = data.get('productId')

    pedido = None
    produto = None

    if order_id and str(order_id).isdigit():
        pedido = db.session.get(Pedido, int(order_id))
        if pedido and pedido.cliente_id != user.id:
            return jsonify({'message': 'Você só pode avaliar os seus próprios pedidos'}), 403
        if pedido and pedido.produto:
            produto = pedido.produto

    if not produto and product_id and str(product_id).isdigit():
        produto = db.session.get(Produto, int(product_id))

    estab = produto.estabelecimento if (produto and produto.estabelecimento) else None
    if not estab:
        return jsonify({'message': 'Produto ou estabelecimento não encontrado'}), 404

    autor_nome = (user.nome or 'Cliente CheapFood').strip()

    # Se for avaliação de um pedido específico (ou do mesmo usuário para o mesmo produto) e já existir, atualiza
    rev = None
    if pedido:
        rev = Avaliacao.query.filter_by(pedido_id=pedido.id).first()
    elif produto:
        rev = Avaliacao.query.filter_by(usuario_id=user.id, produto_id=produto.id, pedido_id=None).first()

    if rev:
        rev.nota = nota
        rev.comentario = comentario
        rev.tags = tags_str
        rev.criado_em = datetime.now()
    else:
        rev = Avaliacao(
            usuario_id=user.id,
            autor_nome=autor_nome,
            produto_id=produto.id if produto else None,
            estabelecimento_id=estab.id,
            pedido_id=pedido.id if pedido else None,
            nota=nota,
            comentario=comentario,
            tags=tags_str,
            criado_em=datetime.now()
        )
        db.session.add(rev)

    db.session.commit()

    return jsonify({
        'message': 'Avaliação enviada com sucesso!',
        'review': rev.to_dict()
    }), 201


@app.route('/api/merchant/reviews', methods=['GET'])
@require_merchant
def get_merchant_reviews(_user, estab):
    revs = (
        Avaliacao.query
        .filter_by(estabelecimento_id=estab.id)
        .order_by(Avaliacao.criado_em.desc(), Avaliacao.id.desc())
        .all()
    )
    count = len(revs)
    avg = round(sum(r.nota for r in revs) / count, 1) if count > 0 else 5.0
    return jsonify({
        'ratingAverage': avg,
        'ratingCount': count,
        'reviews': [r.to_dict() for r in revs]
    }), 200


@app.route('/api/merchant/reviews/<int:review_id>/reply', methods=['POST'])
@require_merchant
def reply_merchant_review(_user, estab, review_id):
    rev = Avaliacao.query.get(review_id)
    if not rev or rev.estabelecimento_id != estab.id:
        return jsonify({'message': 'Avaliação não encontrada'}), 404

    data = request.get_json(silent=True) or {}
    reply = (data.get('reply') or '').strip()
    rev.resposta_lojista = reply if reply else None
    db.session.commit()

    return jsonify({
        'message': 'Resposta salva com sucesso!',
        'review': rev.to_dict()
    }), 200


# ========================
# Merchant Endpoints
# ========================

@app.route('/api/merchant/store', methods=['GET', 'PUT'])
@require_merchant
def merchant_store(_user, estab):
    if request.method == 'PUT':
        data = request.get_json(silent=True) or {}
        if 'name' in data and data['name']:
            estab.nome = data['name'].strip()
        if 'category' in data and data['category']:
            estab.categoria = data['category'].strip()
        if 'cnpj' in data:
            estab.cnpj = data['cnpj'].strip()
        if 'email' in data and data['email']:
            estab.email = data['email'].strip()
        if 'phone' in data:
            estab.telefone = data['phone'].strip()
        if 'address' in data and data['address']:
            estab.endereco = data['address'].strip()
        if 'city' in data and data['city']:
            estab.cidade = data['city'].strip()
        if 'state' in data and data['state']:
            estab.estado = data['state'][:2].upper()
        if 'cep' in data:
            estab.cep = data['cep'].strip()
        if 'openingHours' in data:
            estab.horario_funcionamento = data['openingHours'].strip()
        if 'paymentMethods' in data:
            estab.formas_pagamento = data['paymentMethods'].strip()
        if 'notificationsEnabled' in data:
            estab.notificacoes_ativas = bool(data['notificationsEnabled'])
        if 'plan' in data and data['plan'] in ('free', 'monthly', 'annual'):
            estab.plano = data['plan']
        db.session.commit()
        return jsonify({'message': 'Configurações da loja atualizadas com sucesso!', 'store': estab.to_dict()}), 200

    return jsonify(estab.to_dict()), 200


@app.route('/api/merchant/plan', methods=['PATCH'])
@require_merchant
def update_merchant_plan(_user, estab):
    data = request.get_json(silent=True) or {}
    new_plan = data.get('plan', 'free')
    if new_plan not in ('free', 'monthly', 'annual'):
        return jsonify({'message': 'Plano inválido'}), 400
    estab.plano = new_plan
    db.session.commit()
    return jsonify({'message': 'Plano atualizado com sucesso!', 'store': estab.to_dict()}), 200


@app.route('/api/merchant/stats', methods=['GET'])
@require_merchant
def get_merchant_stats(_user, estab):
    period = request.args.get('period', '7days')

    now = datetime.now()
    today = now.date()

    if period == 'today':
        start_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)
        prev_start = start_dt - timedelta(days=1)
        prev_end = start_dt
    elif period == 'month':
        start_dt = (now - timedelta(days=29)).replace(hour=0, minute=0, second=0, microsecond=0)
        prev_end = start_dt
        prev_start = start_dt - timedelta(days=30)
    elif period == 'year':
        start_dt = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        prev_end = start_dt
        prev_start = start_dt.replace(year=start_dt.year - 1)
    else:  # 7days default
        start_dt = (now - timedelta(days=6)).replace(hour=0, minute=0, second=0, microsecond=0)
        prev_end = start_dt
        prev_start = start_dt - timedelta(days=7)

    # Produtos Ativos e Vencendo em breve (próximos 5 dias)
    all_estab_products = Produto.query.filter_by(estabelecimento_id=estab.id).all()
    active_products = 0
    expiring_soon = 0
    for p in all_estab_products:
        if p.status == 'DISPONIVEL' and not p.pausado and p.quantidade > 0:
            active_products += 1
            try:
                v_date = datetime.strptime(p.data_validade, '%Y-%m-%d').date()
                diff = (v_date - today).days
                if 0 <= diff <= 5:
                    expiring_soon += 1
            except Exception:
                pass

    all_orders = Pedido.query.join(Produto).filter(Produto.estabelecimento_id == estab.id).all()
    reservations = sum(1 for o in all_orders if o.status == 'pendente')

    completed_orders = [o for o in all_orders if o.status == 'retirado' and o.criado_em]
    current_completed = [o for o in completed_orders if o.criado_em >= start_dt]
    prev_completed = [o for o in completed_orders if prev_start <= o.criado_em < prev_end]

    revenue = round(sum(o.quantidade * o.valor_unitario() for o in current_completed), 2)
    prev_revenue = round(sum(o.quantidade * o.valor_unitario() for o in prev_completed), 2)

    if prev_revenue > 0:
        growth = round(((revenue - prev_revenue) / prev_revenue) * 100)
    elif revenue > 0:
        growth = 18
    else:
        growth = 0

    daily_sales = []
    if period == 'today':
        buckets = [('08h', 8, 10), ('10h', 10, 12), ('12h', 12, 14), ('14h', 14, 16), ('16h', 16, 18), ('18h', 18, 21), ('20h', 21, 24)]
        for label, h_start, h_end in buckets:
            val = sum(
                o.quantidade * o.valor_unitario()
                for o in current_completed
                if h_start <= o.criado_em.hour < h_end
            )
            daily_sales.append({'label': label, 'value': round(val, 2)})
    elif period == 'month':
        # 4 semanas dos últimos 28 dias
        for w in range(4):
            w_start = (now - timedelta(days=(3 - w) * 7 + 6)).date()
            w_end = (now - timedelta(days=(3 - w) * 7)).date()
            val = sum(
                o.quantidade * o.valor_unitario()
                for o in current_completed
                if w_start <= o.criado_em.date() <= w_end
            )
            daily_sales.append({'label': f'Sem {w + 1}', 'value': round(val, 2)})
    elif period == 'year':
        months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        current_month = now.month
        start_m = max(1, current_month - 5)
        for m in range(start_m, current_month + 1):
            val = sum(
                o.quantidade * o.valor_unitario()
                for o in current_completed
                if o.criado_em.month == m
            )
            daily_sales.append({'label': months[m - 1], 'value': round(val, 2)})
    else:  # 7days
        weekdays = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        sales_map = {(today - timedelta(days=i)): 0.0 for i in range(6, -1, -1)}
        for o in current_completed:
            dt = o.criado_em.date()
            if dt in sales_map:
                sales_map[dt] += (o.quantidade * o.valor_unitario())
        for dt, val in sales_map.items():
            daily_sales.append({'label': weekdays[dt.weekday()], 'value': round(val, 2)})

    items_saved = sum(o.quantidade for o in current_completed)
    food_saved_kg = round(items_saved * 0.45, 1)
    co2_avoided_kg = round(food_saved_kg * 2.5, 1)

    store_revs = (
        Avaliacao.query
        .filter_by(estabelecimento_id=estab.id)
        .order_by(Avaliacao.criado_em.desc(), Avaliacao.id.desc())
        .all()
    )
    rating_count = len(store_revs)
    rating_avg = round(sum(r.nota for r in store_revs) / rating_count, 1) if rating_count > 0 else 5.0

    return jsonify({
        'revenueRecovered': revenue,
        'activeProducts': active_products,
        'expiringSoon': expiring_soon,
        'reservations': reservations,
        'dailySales': daily_sales,
        'growth': f"+{growth}%" if growth >= 0 else f"{growth}%",
        'storeName': estab.nome,
        'plan': estab.plano or 'free',
        'itemsSaved': items_saved,
        'foodSavedKg': food_saved_kg,
        'co2AvoidedKg': co2_avoided_kg,
        'ratingAverage': rating_avg,
        'ratingCount': rating_count,
        'recentReviews': [r.to_dict() for r in store_revs[:12]],
    }), 200


@app.route('/api/merchant/orders', methods=['GET'])
@require_merchant
def get_merchant_orders(_user, estab):
    orders = Pedido.query.join(Produto).filter(Produto.estabelecimento_id == estab.id).order_by(Pedido.criado_em.desc()).all()
    
    result = []
    for o in orders:
        unit_price = o.valor_unitario()
        created_dt = o.criado_em or datetime.now()
        pickup_limit = (created_dt + timedelta(hours=3)).strftime('%H:%M')
        result.append({
            'id': str(o.id),
            'customerName': o.cliente.nome if o.cliente else 'Cliente',
            'customerEmail': o.cliente.email if o.cliente else '',
            'customerPhone': o.cliente.telefone if (o.cliente and o.cliente.telefone) else '(14) 99712-3456',
            'productName': o.produto.nome if o.produto else 'Produto',
            'productImage': o.produto.imagem if o.produto else None,
            'quantity': o.quantidade,
            'code': o.codigo_reserva,
            'pickupDeadline': pickup_limit,
            'status': o.status,
            'price': unit_price,
            'total': round(unit_price * o.quantidade, 2),
            'createdAt': o.criado_em.strftime('%d/%m às %H:%M') if o.criado_em else ''
        })
    return jsonify(result)


@app.route('/api/merchant/orders/<int:order_id>/status', methods=['PATCH'])
@require_merchant
def update_order_status(_user, estab, order_id):
    order = Pedido.query.get(order_id)
    if not order or not order.produto or order.produto.estabelecimento_id != estab.id:
        return jsonify({'message': 'Pedido não encontrado'}), 404

    data = request.get_json(silent=True) or {}
    new_status = data.get('status')
    if new_status not in ('pendente', 'retirado', 'expirado'):
        return jsonify({'message': 'Status inválido'}), 400

    if new_status == 'expirado' and order.status == 'pendente':
        order.produto.quantidade += order.quantidade
        if order.produto.quantidade > 0 and order.produto.status == 'ESGOTADO':
            order.produto.status = 'DISPONIVEL'

    order.status = new_status
    db.session.commit()
    return jsonify({'message': 'Status atualizado', 'status': order.status})


@app.route('/api/merchant/orders/validate-pin', methods=['POST'])
@require_merchant
def validate_order_pin(_user, estab):
    data = request.get_json(silent=True) or {}
    code = (data.get('code') or '').strip().upper()
    confirm = bool(data.get('confirm', False))

    if not code or len(code) < 3:
        return jsonify({'message': 'Informe um código PIN válido de 4 caracteres'}), 400

    pedidos = (
        Pedido.query
        .join(Produto, Pedido.produto_id == Produto.id)
        .filter(Produto.estabelecimento_id == estab.id)
        .filter(db.func.upper(Pedido.codigo_reserva) == code)
        .order_by(Pedido.id.desc())
        .all()
    )
    if not pedidos:
        return jsonify({'message': f'Nenhum pedido da sua loja encontrado com o código {code}'}), 404

    latest = pedidos[0]
    if latest.criado_em:
        pedidos = [
            p for p in pedidos
            if p.cliente_id == latest.cliente_id and p.criado_em
            and abs((latest.criado_em - p.criado_em).total_seconds()) <= 120
        ]
    pedidos = sorted(pedidos, key=lambda p: p.id)

    if confirm:
        for p in pedidos:
            if p.status == 'pendente':
                p.status = 'retirado'
        db.session.commit()

    first = pedidos[0]
    items = []
    total = 0.0
    for p in pedidos:
        unit_price = p.valor_unitario()
        line_total = round(unit_price * p.quantidade, 2)
        total += line_total
        items.append({
            'orderId': str(p.id),
            'productName': p.produto.nome if p.produto else 'Produto',
            'quantity': p.quantidade,
            'price': unit_price,
            'total': line_total,
            'status': p.status,
        })

    return jsonify({
        'code': first.codigo_reserva,
        'customerName': first.cliente.nome if first.cliente else 'Cliente',
        'status': first.status,
        'createdAt': first.criado_em.strftime('%d/%m às %H:%M') if first.criado_em else 'Hoje',
        'total': round(total, 2),
        'items': items,
        'message': 'Retirada confirmada com sucesso!' if confirm else 'Pedido localizado!'
    }), 200


@app.route('/api/merchant/reset-demo', methods=['POST'])
@require_merchant
def reset_demo_data(_user, _estab):
    if not DEMO_MODE:
        return jsonify({'message': 'Restauração de demonstração desabilitada em produção'}), 403
    try:
        from seed_tcc import seed_tcc
        seed_tcc()
        return jsonify({'message': 'Cenário de apresentação restaurado com sucesso!'}), 200
    except Exception as e:
        return jsonify({'message': 'Erro ao restaurar dados de demonstração', 'error': str(e)}), 500


@app.route('/api/merchant/products', methods=['GET'])
@require_merchant
def get_merchant_products(_user, estab):
    produtos = Produto.query.filter_by(estabelecimento_id=estab.id).order_by(Produto.id.desc()).all()
    
    result = []
    for p in produtos:
        p_dict = p.to_dict()
        p_dict['paused'] = bool(p.pausado)
        p_dict['promoPrice'] = p_dict['price']
        reserved_count = sum(o.quantidade for o in (p.pedidos or []) if o.status == 'pendente')
        p_dict['reservedCount'] = reserved_count
        p_dict['quantityAvailable'] = p.quantidade
        if p.quantidade <= 0:
            p_dict['status'] = 'vendido'
        elif 'Vencido' in p_dict['expires_in']:
            p_dict['status'] = 'vencido'
        else:
            p_dict['status'] = 'ativo'
            
        result.append(p_dict)
        
    return jsonify(result)


@app.route('/api/merchant/products/<int:product_id>/pause', methods=['PATCH'])
@require_merchant
def toggle_product_pause(_user, estab, product_id):
    product = get_owned_product(estab, product_id)
    if not product:
        return jsonify({'message': 'Produto não encontrado na sua loja'}), 404
        
    product.pausado = not product.pausado
    db.session.commit()
    return jsonify({'message': 'Produto atualizado', 'paused': product.pausado})


@app.route('/api/merchant/products/<int:product_id>/discount', methods=['PATCH'])
@require_merchant
def apply_extra_discount(_user, estab, product_id):
    product = get_owned_product(estab, product_id)
    if not product:
        return jsonify({'message': 'Produto não encontrado na sua loja'}), 404

    data = request.get_json(silent=True) or {}
    try:
        percent = float(data.get('percent', 20))
    except (TypeError, ValueError):
        percent = 20.0
    new_price = round(max(0.50, float(product.preco_desconto) * (1.0 - percent / 100.0)), 2)
    product.preco_desconto = new_price

    # Se o produto estava vencido, renova a validade do lote em +2 dias para voltar à vitrine
    try:
        v_date = datetime.strptime(product.data_validade, '%Y-%m-%d').date()
        if v_date < datetime.now().date():
            product.data_validade = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
    except Exception:
        product.data_validade = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')

    product.pausado = False
    if product.quantidade <= 0:
        product.quantidade = 5
    product.status = 'DISPONIVEL'
    db.session.commit()

    return jsonify({
        'message': f'Desconto extra de {int(percent)}% aplicado! Novo preço: R$ {new_price:.2f}',
        'product': product.to_dict()
    }), 200


# ========================
# Leilão "Preço que Cai"
# ========================

@app.route('/api/products/<int:product_id>/bids', methods=['POST'])
def add_bid(product_id):
    user = get_request_user()
    if not user:
        return jsonify({'message': 'Faça login para dar um lance'}), 401

    produto = Produto.query.get(product_id)
    if not produto or produto.status != 'DISPONIVEL' or produto.pausado:
        return jsonify({'message': 'Produto indisponível'}), 409

    leilao = produto.leilao_ativo()
    if not leilao:
        return jsonify({'message': 'Produto não está em leilão'}), 409

    from datetime import datetime
    if datetime.utcnow() >= leilao.fim:
        return jsonify({'message': 'Este leilão já foi encerrado.'}), 400

    data = request.get_json(silent=True) or {}
    if 'valor' not in data:
        return jsonify({'message': 'Valor do lance não fornecido'}), 400

    try:
        valor = float(data['valor'])
    except (TypeError, ValueError):
        return jsonify({'message': 'Valor inválido'}), 400

    if math.isnan(valor) or math.isinf(valor) or valor <= 0:
        return jsonify({'message': 'Informe um valor de lance válido'}), 400

    if is_merchant(user) and produto.estabelecimento_id == get_or_create_store(user).id:
        return jsonify({'message': 'O lojista não pode dar lance no próprio produto'}), 403

    has_bids = bool(produto.lances)
    highest_bid = max(l.valor for l in produto.lances) if has_bids else leilao.preco_inicial

    if has_bids and valor <= highest_bid:
        return jsonify({'message': f'O lance deve ser maior que o maior lance atual (R$ {highest_bid:.2f})'}), 400
    if not has_bids and valor < leilao.preco_inicial:
        return jsonify({'message': f'O lance deve ser de pelo menos R$ {leilao.preco_inicial:.2f}'}), 400
    if produto.preco_desconto and valor >= float(produto.preco_desconto):
        return jsonify({'message': f'Para pagar R$ {produto.preco_desconto:.2f} ou mais, use o botão Comprar Agora!'}), 400

    lance = Lance(produto_id=produto.id, usuario_id=user.id, valor=valor)
    db.session.add(lance)
    db.session.commit()

    return jsonify(produto.to_dict()), 201

@app.route('/api/auctions', methods=['GET'])
def list_auctions():
    """Leilões ativos e disponíveis na vitrine."""
    produtos = (
        Produto.query
        .join(Leilao, Leilao.produto_id == Produto.id)
        .filter(Leilao.ativo.is_(True), Produto.status == 'DISPONIVEL', Produto.pausado.isnot(True))
        .all()
    )
    result = [p.to_dict() for p in produtos]
    return jsonify(result), 200


@app.route('/api/merchant/products/<int:product_id>/auction/stop', methods=['POST'])
@require_merchant
def stop_auction(_user, estab, product_id):
    """Encerra o leilão agora.
    - Com lances: o leilão termina e o maior lance vence (o vencedor resgata pelo valor do lance).
    - Sem lances: o leilão é desativado e o produto volta à venda normal pelo preço promocional."""
    produto = get_owned_product(estab, product_id)
    if not produto:
        return jsonify({'message': 'Produto não encontrado na sua loja'}), 404

    leilao = produto.leilao_ativo()
    if not leilao:
        return jsonify({'message': 'Este produto não está em leilão'}), 409

    agora = datetime.utcnow().replace(microsecond=0)
    if leilao.lance_vencedor():
        if leilao.fim > agora:
            leilao.fim = agora
        msg = 'Leilão encerrado. O maior lance venceu e pode resgatar o produto.'
    else:
        leilao.ativo = False
        msg = 'Leilão encerrado sem lances. O produto voltou à venda normal.'

    db.session.commit()
    return jsonify({'message': msg, 'product': produto.to_dict()}), 200


def list_user_favorite_ids(user):
    """Retorna os IDs (string) dos produtos favoritados que ainda estão visíveis na vitrine."""
    favs = (
        Favorito.query
        .join(Produto, Favorito.produto_id == Produto.id)
        .filter(Favorito.usuario_id == user.id, Produto.status == 'DISPONIVEL')
        .all()
    )
    return [str(f.produto_id) for f in favs]


@app.route('/api/favorites', methods=['GET'])
@require_auth
def get_favorites(user):
    return jsonify(list_user_favorite_ids(user))


@app.route('/api/favorites/<int:product_id>', methods=['POST', 'DELETE'])
@require_auth
def toggle_favorite(user, product_id):
    if not Produto.query.get(product_id):
        return jsonify({'message': 'Produto não encontrado'}), 404

    fav = Favorito.query.filter_by(usuario_id=user.id, produto_id=product_id).first()

    if request.method == 'POST':
        if not fav:
            db.session.add(Favorito(usuario_id=user.id, produto_id=product_id))
            db.session.commit()
        status = 'added'
    else:
        if fav:
            db.session.delete(fav)
            db.session.commit()
        status = 'removed'

    return jsonify({
        'status': status,
        'product_id': str(product_id),
        'favorites': list_user_favorite_ids(user)
    })


@app.route('/api/profile', methods=['PUT'])
@require_auth
def update_profile(user):
    if request.form.get('name'):
        user.nome = request.form.get('name').strip()
    if request.form.get('telefone') is not None:
        user.telefone = request.form.get('telefone').strip()
    if request.form.get('cpf') is not None:
        user.cpf = request.form.get('cpf').strip()

    # Atualiza foto de perfil se enviada
    file = request.files.get('foto') or request.files.get('photo')
    if file and file.filename:
        try:
            user.foto = save_upload(file)
        except ValueError as e:
            return jsonify({'message': str(e)}), 400

    db.session.commit()

    return jsonify({
        'message': 'Perfil atualizado com sucesso!',
        'user': user_payload(user)
    }), 200


@app.route('/api/profile', methods=['DELETE'])
@require_auth
def delete_profile(user):
    data = request.get_json(silent=True) or {}
    password = data.get('password')
    if not password:
        return jsonify({'message': 'Digite sua senha para confirmar a exclusão'}), 400

    if not verify_password(user, password):
        return jsonify({'message': 'Senha incorreta'}), 400

    try:
        # Limpa avaliações feitas por este usuário
        Avaliacao.query.filter_by(usuario_id=user.id).delete()

        # Limpa pedidos feitos por este usuário (e devolve estoque de pendentes)
        user_orders = Pedido.query.filter_by(cliente_id=user.id).all()
        for o in user_orders:
            Avaliacao.query.filter_by(pedido_id=o.id).delete()
            if o.status == 'pendente' and o.produto:
                o.produto.quantidade += o.quantidade
                if o.produto.quantidade > 0 and o.produto.status == 'ESGOTADO':
                    o.produto.status = 'DISPONIVEL'
            db.session.delete(o)

        # Se for comerciante, exclui produtos (e dependências) e loja
        if is_merchant(user):
            estabs = Estabelecimento.query.filter_by(usuario_id=user.id).all()
            for estab in estabs:
                Avaliacao.query.filter_by(estabelecimento_id=estab.id).delete()
                for p in list(estab.produtos):
                    Avaliacao.query.filter_by(produto_id=p.id).delete()
                    Favorito.query.filter_by(produto_id=p.id).delete()
                    Lance.query.filter_by(produto_id=p.id).delete()
                    Leilao.query.filter_by(produto_id=p.id).delete()
                    Pedido.query.filter_by(produto_id=p.id).delete()
                    db.session.delete(p)
                db.session.delete(estab)

        # Limpa favoritos e lances vinculados
        Favorito.query.filter_by(usuario_id=user.id).delete()
        Lance.query.filter_by(usuario_id=user.id).delete()
        # Remove usuário
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Conta excluída com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao excluir conta', 'error': str(e)}), 500


def ensure_schema():
    """Cria tabelas e adiciona colunas faltantes em SQLite/Postgres de forma idempotente."""
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print("Aviso ao executar db.create_all():", e, flush=True)

        try:
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()

            if 'usuario' in tables:
                existing_user_cols = [c['name'] for c in inspector.get_columns('usuario')]
                if 'cpf' not in existing_user_cols:
                    db.session.execute(db.text("ALTER TABLE usuario ADD COLUMN cpf VARCHAR(20)"))
                    print("Migração: adicionada coluna usuario.cpf", flush=True)

            if 'estabelecimento' in tables:
                existing_estab_cols = [c['name'] for c in inspector.get_columns('estabelecimento')]
                if 'usuario_id' not in existing_estab_cols:
                    db.session.execute(db.text("ALTER TABLE estabelecimento ADD COLUMN usuario_id INTEGER"))
                    print("Migração: adicionada coluna estabelecimento.usuario_id", flush=True)
                if 'categoria' not in existing_estab_cols:
                    db.session.execute(db.text("ALTER TABLE estabelecimento ADD COLUMN categoria VARCHAR(80) DEFAULT 'Padaria e Confeitaria'"))
                    print("Migração: adicionada coluna estabelecimento.categoria", flush=True)
                if 'horario_funcionamento' not in existing_estab_cols:
                    db.session.execute(db.text("ALTER TABLE estabelecimento ADD COLUMN horario_funcionamento VARCHAR(150) DEFAULT 'Seg a Sáb: 08:00 às 20:00'"))
                if 'plano' not in existing_estab_cols:
                    db.session.execute(db.text("ALTER TABLE estabelecimento ADD COLUMN plano VARCHAR(30) DEFAULT 'free'"))
                if 'formas_pagamento' not in existing_estab_cols:
                    db.session.execute(db.text("ALTER TABLE estabelecimento ADD COLUMN formas_pagamento VARCHAR(200) DEFAULT 'PIX, Cartão de Crédito/Débito e Dinheiro'"))
                if 'notificacoes_ativas' not in existing_estab_cols:
                    db.session.execute(db.text("ALTER TABLE estabelecimento ADD COLUMN notificacoes_ativas BOOLEAN DEFAULT 1"))

            if 'pedido' in tables:
                existing_pedido_cols = [c['name'] for c in inspector.get_columns('pedido')]
                if 'preco_unitario' not in existing_pedido_cols:
                    db.session.execute(db.text("ALTER TABLE pedido ADD COLUMN preco_unitario REAL"))
                    print("Migração: adicionada coluna pedido.preco_unitario", flush=True)

            db.session.commit()

            # Vincula estabelecimentos órfãos ao primeiro usuário comerciante (ADMIN)
            admin_user = Usuario.query.filter_by(tipo='ADMIN').first()
            if admin_user:
                orphan_estabs = Estabelecimento.query.filter(Estabelecimento.usuario_id.is_(None)).all()
                for est in orphan_estabs:
                    est.usuario_id = admin_user.id
                if orphan_estabs:
                    db.session.commit()
                    print(f"Migração: vinculados {len(orphan_estabs)} estabelecimentos ao usuário {admin_user.email}", flush=True)
        except Exception as e:
            db.session.rollback()
            print("Aviso ao rodar migrações leves de schema:", e, flush=True)


ensure_schema()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n=== CheapFood Backend rodando na porta {port} (debug={DEBUG}) ===")
    app.run(host='0.0.0.0', debug=DEBUG, port=port)



