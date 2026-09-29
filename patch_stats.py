import re

with open('backend/app.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace get_merchant_stats
old_func_regex = re.compile(r"@app\.route\('/api/merchant/stats', methods=\['GET'\]\)\ndef get_merchant_stats\(\):.*?return jsonify\(\{.*?\}\), 200", re.DOTALL)

new_func = """@app.route('/api/merchant/stats', methods=['GET'])
def get_merchant_stats():
    from datetime import datetime, timedelta
    
    period = request.args.get('period', '7days')
    estab = Estabelecimento.query.first()
    if not estab:
        return jsonify({'revenueRecovered': 0, 'activeProducts': 0, 'expiringSoon': 0, 'reservations': 0, 'dailySales': [], 'growth': 0})

    now = datetime.utcnow()
    
    if period == 'today':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        prev_start = start_date - timedelta(days=1)
        prev_end = start_date
    elif period == 'month':
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        prev_end = start_date
        prev_start = (prev_end - timedelta(days=1)).replace(day=1)
    elif period == 'year':
        start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        prev_end = start_date
        prev_start = prev_end.replace(year=prev_end.year - 1)
    else: # 7days default
        start_date = now - timedelta(days=7)
        prev_start = start_date - timedelta(days=7)
        prev_end = start_date

    # Active products
    active_products = Produto.query.filter_by(estabelecimento_id=estab.id, status='DISPONIVEL', pausado=False).count()
    
    # Current period orders
    all_orders = Pedido.query.join(Produto).filter(Produto.estabelecimento_id == estab.id).all()
    
    current_orders = [o for o in all_orders if o.criado_em >= start_date]
    prev_orders = [o for o in all_orders if prev_start <= o.criado_em < prev_end]
    
    reservations = sum(1 for o in current_orders if o.status == 'pendente')
    
    # Revenue (retirado)
    revenue = sum(o.quantidade * o.produto.preco_desconto for o in current_orders if o.status == 'retirado')
    prev_revenue = sum(o.quantidade * o.produto.preco_desconto for o in prev_orders if o.status == 'retirado')
    
    # Growth
    growth = 0
    if prev_revenue > 0:
        growth = int(((revenue - prev_revenue) / prev_revenue) * 100)
    elif revenue > 0:
        growth = 100
        
    # Chart data
    chart_dict = {}
    completed = [o for o in current_orders if o.status == 'retirado']
    
    if period == 'today':
        for i in range(8, 23, 2): chart_dict[f"{i}h"] = 0
        for o in completed:
            h = o.criado_em.hour
            key = f"{h if h % 2 == 0 else h - 1}h"
            if key in chart_dict: chart_dict[key] += (o.quantidade * o.produto.preco_desconto)
            
    elif period == 'month':
        for i in range(1, 32, 5): chart_dict[f"Dia {i}"] = 0
        for o in completed:
            d = o.criado_em.day
            bucket = ((d - 1) // 5) * 5 + 1
            key = f"Dia {bucket}"
            if key in chart_dict: chart_dict[key] += (o.quantidade * o.produto.preco_desconto)
            
    elif period == 'year':
        months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        for m in months: chart_dict[m] = 0
        for o in completed:
            m = o.criado_em.month
            key = months[m-1]
            chart_dict[key] += (o.quantidade * o.produto.preco_desconto)
            
    else: # 7days
        days = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
        for i in range(7):
            d = start_date + timedelta(days=i)
            # Python weekday() is Mon=0, Sun=6. We want Dom=0, Seg=1
            idx = (d.weekday() + 1) % 7
            chart_dict[days[idx]] = 0
            
        for o in completed:
            idx = (o.criado_em.weekday() + 1) % 7
            key = days[idx]
            if key in chart_dict: chart_dict[key] += (o.quantidade * o.produto.preco_desconto)
            
    daily_sales = [{'label': k, 'value': v} for k, v in chart_dict.items()]
    
    # expiring
    expiring_soon = 48 # dummy
    
    return jsonify({
        'revenueRecovered': revenue,
        'activeProducts': active_products,
        'expiringSoon': expiring_soon,
        'reservations': reservations,
        'dailySales': daily_sales,
        'growth': growth
    }), 200"""

c = old_func_regex.sub(new_func, c)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(c)
