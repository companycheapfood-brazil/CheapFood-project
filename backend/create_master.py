
from app import app, db, Usuario
from werkzeug.security import generate_password_hash

with app.app_context():
    existing = Usuario.query.filter_by(email='master@cheapfood.com').first()
    if not existing:
        master = Usuario(
            nome='Master Administrador',
            email='master@cheapfood.com',
            senha=generate_password_hash('master123'),
            telefone='',
            tipo='ADMIN'
        )
        db.session.add(master)
        db.session.commit()
        print('Conta master criada: email=master@cheapfood.com, senha=master123')
    else:
        existing.senha = generate_password_hash('master123')
        db.session.commit()
        print('Conta master atualizada. Senha=master123')

