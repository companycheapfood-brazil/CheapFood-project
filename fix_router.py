with open('src/router/index.ts', 'r', encoding='utf-8') as f:
    c = f.read()

import re

new_guard = """router.beforeEach((to, from, next) => {
  const publicPages = ['/start', '/login', '/register', '/forgot-password', '/reset-password']
  const authRequired = !publicPages.includes(to.path)
  
  const userStr = localStorage.getItem('user')
  let user = null
  if (userStr) {
    try {
      user = JSON.parse(userStr)
    } catch(e) {}
  }

  if (authRequired && !user) {
    return next('/start')
  }

  // Controle de Acesso por Tipo de Perfil (CLIENTE vs COMERCIANTE)
  if (user) {
    const isMerchantRoute = to.path.startsWith('/comerciante')
    const isPublic = publicPages.includes(to.path)
    
    // Se logado e tentar acessar login, redireciona
    if (isPublic) {
      return next(user.type === 'COMERCIANTE' ? '/comerciante' : '/')
    }

    if (isMerchantRoute && user.type !== 'COMERCIANTE') {
      // Segurança: Cliente tentando acessar área de comerciante
      return next('/')
    }

    // Segurança: Lojista não deve navegar nas telas de compra do consumidor
    // Perfis permitidos compartilhados: /perfil (minha conta)
    const isConsumerRoute = to.path === '/' || to.path.startsWith('/produto') || to.path.startsWith('/carrinho') || to.path.startsWith('/buscar') || to.path.startsWith('/comprovante')
    
    if (isConsumerRoute && user.type === 'COMERCIANTE') {
      return next('/comerciante')
    }
  }

  next()
})"""

# Replace existing router.beforeEach
c = re.sub(r'router\.beforeEach\(.*?\n\}\)', new_guard, c, flags=re.DOTALL)

with open('src/router/index.ts', 'w', encoding='utf-8') as f:
    f.write(c)
