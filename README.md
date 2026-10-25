# CheapFood 🍞🥦

Plataforma inteligente contra o desperdício de alimentos que conecta estabelecimentos comerciais (padarias, supermercados, hortifrutis) a consumidores locais. Desenvolvida como Trabalho de Conclusão de Curso (TCC).

---

## 🌟 Principais Recursos

- **Vitrine e Feed Personalizado:** algoritmo estilo iFood que recomenda produtos por afinidade, compras anteriores e urgência de consumo.
- **Leilão "Preço que Cai" (Holandês/Híbrido):** o lojista pode iniciar um leilão onde o preço reduz gradualmente ou o comprador pode arrematar imediatamente.
- **Preenchimento Automático por IA (Google Gemini):** o comerciante tira uma foto do produto e a IA preenche nome, descrição, categoria, validade e preços sugeridos.
- **Painel do Comerciante Completo:** métricas com filtros temporais, impacto ecológico (kg de alimentos salvos e CO₂ evitado), gerenciamento de produtos com pausa/desconto extra, validação de pedidos por PIN de 4 dígitos e gestão de avaliações.
- **Avaliações Reais com Resposta do Lojista:** notas de 1 a 5, tags dinâmicas e resposta oficial do comerciante.
- **Totalmente Responsivo:** navegação mobile otimizada com sidebar lateral, barra inferior e simulador de tela 430px.

---

## 👥 Contas de Demonstração (Demo / TCC)

| Perfil | E-mail | Senha |
|---|---|---|
| **Consumidor** | `joao@email.com` | `123456` |
| **Comerciante (Padaria Central)** | `admin@cheapfood.com` | `admin123` |
| **Outros Clientes** | `maria@email.com`, `carlos@email.com` | `123456` |

> 💡 Se precisar resetar o cenário para a apresentação da banca, basta acessar **Comerciante > Configurações > Restaurar Cenário de Demonstração** ou rodar `python backend/seed_tcc.py`.

---

## 💻 Como Rodar Localmente

### 1. Backend (Flask + SQLite)

```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
python app.py
```
O backend rodará em `http://127.0.0.1:5000`.

### 2. Frontend (Vue 3 + Vite + Pinia)

```bash
npm install
npm run dev
```
O frontend rodará em `http://localhost:5173`.

---

## 🚀 Guia de Deploy (Pronto para Produção)

O projeto está 100% configurado para deploy gratuito com separação frontend/backend:

### A. Deploy do Backend (Render / Railway)

1. Crie um novo **Web Service** no [Render](https://render.com/) ou [Railway](https://railway.app/) conectado a este repositório Git.
2. Defina os campos:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
3. Configure as **Environment Variables** (veja `backend/.env.example`):
   - `SECRET_KEY`: Uma chave aleatória longa e segura.
   - `FLASK_DEBUG`: `False`
   - `DEMO_MODE`: `True` (ou `False` para produção estrita)
   - `FRONTEND_URL`: `https://seu-app.vercel.app`
   - `CORS_ORIGINS`: `https://seu-app.vercel.app`
   - `GEMINI_API_KEY`: Sua chave de API do Google Gemini.
   - *(Opcional)* `DATABASE_URL`: String de conexão PostgreSQL (Render Postgres ou Neon). Se omitida, usará SQLite.

### B. Deploy do Frontend (Vercel / Netlify)

1. Importe este repositório na [Vercel](https://vercel.com/) ou [Netlify](https://netlify.com/).
2. Defina:
   - **Framework Preset:** `Vite`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
3. Adicione a variável de ambiente:
   - `VITE_API_URL`: A URL do backend publicado (ex.: `https://cheapfood-backend.onrender.com`).
4. O arquivo `vercel.json` e `public/_redirects` já estão incluídos na raiz para garantir que rotas de SPA (como `/comerciante` e `/carrinho`) não deem erro 404 ao atualizar a página.

---

## 🧪 Verificação do Build

Para garantir a integridade do código antes de enviar ao Git:

```bash
npm run build
```
O comando valida tipagem TypeScript (`vue-tsc`) e gera o bundle minificado com zero erros.
