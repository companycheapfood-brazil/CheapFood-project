
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
    daily_sales = [
        {'label': 'Seg', 'value': 2},
        {'label': 'Ter', 'value': 5},
        {'label': 'Qua', 'value': 3},
        {'label': 'Qui', 'value': 8},
        {'label': 'Sex', 'value': 4},
        {'label': 'Sab', 'value': 9},
        {'label': 'Dom', 'value': len(orders)}
    ]
    
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

