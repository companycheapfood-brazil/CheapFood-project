import re

with open('backend/app.py', 'r', encoding='utf-8') as f:
    c = f.read()

old_get_product = """@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    produto = Produto.query.get_or_404(product_id)
    return jsonify(produto.to_dict()), 200"""

new_product_endpoint = """import os
from werkzeug.utils import secure_filename

@app.route('/api/products/<int:product_id>', methods=['GET', 'PUT'])
def get_product(product_id):
    produto = Produto.query.get_or_404(product_id)
    
    if request.method == 'PUT':
        # Update logic
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
            
        if 'nome' in data: produto.nome = data['nome']
        if 'descricao' in data: produto.descricao = data['descricao']
        if 'categoria' in data: produto.categoria = data['categoria']
        if 'preco_original' in data: produto.preco_original = float(data['preco_original'])
        if 'preco_desconto' in data: produto.preco_desconto = float(data['preco_desconto'])
        if 'quantidade' in data: produto.quantidade = int(data['quantidade'])
        if 'data_validade' in data: produto.data_validade = data['data_validade']
        
        # Handle image if uploaded
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                produto.imagem = f'/static/uploads/{filename}'
                
        db.session.commit()
        return jsonify(produto.to_dict()), 200
        
    return jsonify(produto.to_dict()), 200"""

c = c.replace(old_get_product, new_product_endpoint)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(c)
