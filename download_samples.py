import sqlite3
import urllib.request
import os
import uuid
import re

os.makedirs('backend/static/uploads', exist_ok=True)

# Hand-picked valid Unsplash food photos mapped to keywords
category_map = {
    'pizza': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&q=80',
    'pão': 'https://images.unsplash.com/photo-1543353071-873f17a7a088?w=400&q=80',
    'pao': 'https://images.unsplash.com/photo-1543353071-873f17a7a088?w=400&q=80',
    'sanduíche': 'https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=400&q=80',
    'hambúrguer': 'https://images.unsplash.com/photo-1499028344343-cd173ffc68a9?w=400&q=80',
    'burger': 'https://images.unsplash.com/photo-1460306855393-0410f61241c7?w=400&q=80',
    'carne': 'https://images.unsplash.com/photo-1432139555190-58524dae6a55?w=400&q=80',
    'frango': 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400&q=80', # Chicken/Restaurant dish
    'salada': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&q=80',
    'alface': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&q=80',
    'massa': 'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=400&q=80',
    'lasanha': 'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=400&q=80',
    'peixe': 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400&q=80',
    'doce': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&q=80',
    'bolo': 'https://images.unsplash.com/photo-1484723091791-c0e7e53c979a?w=400&q=80', # Pancakes/pastry
    'biscoito': 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=400&q=80', # Healthy snacks
    'tomate': 'https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?w=400&q=80',
    'sopa': 'https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?w=400&q=80',
    'taco': 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400&q=80',
    'porco': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&q=80', # Steak
    'leite': 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&q=80', # Added valid milk from prev attempt
    'iogurte': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400&q=80',
    'fruta': 'https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=400&q=80',
    'uva': 'https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=400&q=80',
    'banana': 'https://images.unsplash.com/photo-1610832958506-aa56368176cf?w=400&q=80',
    'bebida': 'https://images.unsplash.com/photo-1556881286-fc6915169721?w=400&q=80',
    'refrigerante': 'https://images.unsplash.com/photo-1556881286-fc6915169721?w=400&q=80',
    'suco': 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400&q=80',
    'café': 'https://images.unsplash.com/photo-1559525839-b184a4d698c7?w=400&q=80',
    'cerveja': 'https://images.unsplash.com/photo-1614316784013-1a43a05ec9b5?w=400&q=80',
    'frios': 'https://images.unsplash.com/photo-1603048297172-c92544798d5e?w=400&q=80',
    'presunto': 'https://images.unsplash.com/photo-1603048297172-c92544798d5e?w=400&q=80',
    'queijo': 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=400&q=80',
    'mussarela': 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=400&q=80',
    'padrão': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&q=80', # Default bowl
}

conn = sqlite3.connect('cheapfood.db')
cursor = conn.cursor()

cursor.execute('SELECT id, nome FROM produto')
produtos = cursor.fetchall()

for prod_id, nome in produtos:
    nome_lower = nome.lower()
    url = category_map['padrão']
    
    for key, img_url in category_map.items():
        if key in nome_lower:
            url = img_url
            break
            
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req)
        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join('backend', 'static', 'uploads', filename)
        with open(filepath, 'wb') as f:
            f.write(response.read())
            
        img_val = f"http://127.0.0.1:5000/static/uploads/{filename}"
        cursor.execute('UPDATE produto SET imagem = ? WHERE id = ?', (img_val, prod_id))
        print(f"Updated {nome} with {url}")
    except Exception as e:
        print(f"Failed to download for {nome}: {e}")

conn.commit()
conn.close()
