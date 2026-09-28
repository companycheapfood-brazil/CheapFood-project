import sqlite3
import urllib.request
import os
import uuid
import random

os.makedirs('backend/static/uploads', exist_ok=True)

# A large list of valid Unsplash food photos
food_urls = [
    'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&q=80', # Food bowl
    'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&q=80', # Pizza
    'https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=400&q=80', # Sandwich
    'https://images.unsplash.com/photo-1484723091791-c0e7e53c979a?w=400&q=80', # Pancakes
    'https://images.unsplash.com/photo-1499028344343-cd173ffc68a9?w=400&q=80', # Burger
    'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=400&q=80', # Pasta
    'https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?w=400&q=80', # Spices/Curry
    'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&q=80', # Steak
    'https://images.unsplash.com/photo-1432139555190-58524dae6a55?w=400&q=80', # Meat
    'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&q=80', # Salad
    'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400&q=80', # Restaurant dish
    'https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=400&q=80', # Tacos
    'https://images.unsplash.com/photo-1529042410759-befb1204b468?w=400&q=80', # Meatballs
    'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=400&q=80', # Healthy food
    'https://images.unsplash.com/photo-1543353071-873f17a7a088?w=400&q=80', # Pastry
    'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400&q=80', # Fish
    'https://images.unsplash.com/photo-1460306855393-0410f61241c7?w=400&q=80', # Burger 2
    'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&q=80', # Skewers
    'https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?w=400&q=80', # Tomato/soup
    'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400&q=80', # Tacos 2
]

conn = sqlite3.connect('cheapfood.db')
cursor = conn.cursor()

cursor.execute('SELECT id, nome FROM produto')
produtos = cursor.fetchall()

for prod_id, nome in produtos:
    url = random.choice(food_urls)
            
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req)
        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join('backend', 'static', 'uploads', filename)
        with open(filepath, 'wb') as f:
            f.write(response.read())
            
        img_val = f"http://127.0.0.1:5000/static/uploads/{filename}"
        cursor.execute('UPDATE produto SET imagem = ? WHERE id = ?', (img_val, prod_id))
        print(f"Updated {nome}")
    except Exception as e:
        print(f"Failed: {e}")

conn.commit()
conn.close()
