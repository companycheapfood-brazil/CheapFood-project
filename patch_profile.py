with open('src/views/profile/ProfileView.vue', 'r', encoding='utf-8') as f:
    c = f.read()

if '/perfil/favoritos' not in c:
    c = c.replace(
        "{ label: 'Planos', to: '/perfil/planos' },",
        "{ label: 'Planos', to: '/perfil/planos' },\n  { label: 'Meus Favoritos', to: '/perfil/favoritos' },"
    )

    with open('src/views/profile/ProfileView.vue', 'w', encoding='utf-8') as f:
        f.write(c)
