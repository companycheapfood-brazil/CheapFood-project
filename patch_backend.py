import re

with open('backend/app.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Add Favorito model
favorito_model = """class Favorito(db.Model):
    __tablename__ = 'favorito'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    
    usuario = db.relationship('Usuario', backref=db.backref('favoritos', lazy=True))
    produto = db.relationship('Produto', backref=db.backref('favoritados', lazy=True))

class Pedido(db.Model):"""

c = c.replace('class Pedido(db.Model):', favorito_model)

# Add auto-lock logic in checkout
old_checkout_loop = """        produto = Produto.query.get(product_id)
        if produto and produto.quantidade >= qty:
            produto.quantidade -= qty
            pedido = Pedido(cliente_id=user.id, produto_id=produto.id, quantidade=qty, codigo_reserva=code)
            db.session.add(pedido)"""

new_checkout_loop = """        produto = Produto.query.get(product_id)
        if produto and produto.quantidade >= qty:
            produto.quantidade -= qty
            if produto.quantidade <= 0:
                produto.status = 'ESGOTADO'
            pedido = Pedido(cliente_id=user.id, produto_id=produto.id, quantidade=qty, codigo_reserva=code)
            db.session.add(pedido)"""

c = c.replace(old_checkout_loop, new_checkout_loop)

# Add Favorites Endpoints
endpoints = """
@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    # in a real app, user_id from token
    user = Usuario.query.first()
    if not user:
        return jsonify([])
    favs = Favorito.query.filter_by(usuario_id=user.id).all()
    fav_ids = [f.produto_id for f in favs]
    return jsonify(fav_ids)

@app.route('/api/favorites/<int:product_id>', methods=['POST', 'DELETE'])
def toggle_favorite(product_id):
    user = Usuario.query.first()
    if not user:
        return jsonify({'message': 'Unauthorized'}), 401
        
    fav = Favorito.query.filter_by(usuario_id=user.id, produto_id=product_id).first()
    
    if request.method == 'POST':
        if not fav:
            new_fav = Favorito(usuario_id=user.id, produto_id=product_id)
            db.session.add(new_fav)
            db.session.commit()
        return jsonify({'status': 'added', 'product_id': product_id})
        
    if request.method == 'DELETE':
        if fav:
            db.session.delete(fav)
            db.session.commit()
        return jsonify({'status': 'removed', 'product_id': product_id})

# ========================
# Run
"""

c = c.replace('# ========================\n# Run', endpoints)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(c)
