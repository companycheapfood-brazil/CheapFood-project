import re

def fix_logo(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Fix encoding
    c = c.replace('desperdÃ­cio', 'desperdício')

    # Replace logo container structure
    # Match the old logo container content
    pattern = re.compile(r'<div class="logo-container(?:-small)?">.*?</svg>\s*<h1 class="logo-text(?:-small)?">Cheap<span class="logo-text-highlight">Food</span></h1>', re.DOTALL)
    
    def repl(m):
        content = m.group(0)
        # wrap svg and h1 in a logo-row div
        content = content.replace('<svg', '<div class="logo-row">\n      <svg')
        content = content.replace('</h1>', '</h1>\n      </div>')
        return content
        
    c = pattern.sub(repl, c)

    # Add logo-row CSS if not exists
    if '.logo-row' not in c:
        css = """
.logo-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 0.5rem;
}
"""
        c = c.replace('</style>', css + '\n</style>')
        
        # fix cart-icon size
        c = re.sub(r'\.cart-icon\s*\{[^}]*\}', '.cart-icon {\n  width: 50px;\n  height: 50px;\n}', c)
        c = re.sub(r'\.cart-icon-small\s*\{[^}]*\}', '.cart-icon-small {\n  width: 40px;\n  height: 40px;\n}', c)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(c)

for file in ['src/views/auth/StartView.vue', 'src/views/auth/LoginView.vue', 'src/views/auth/RegisterView.vue', 'src/views/auth/ForgotPasswordView.vue', 'src/views/auth/ResetPasswordView.vue']:
    try:
        fix_logo(file)
        print(f"Fixed {file}")
    except Exception as e:
        print(f"Error fixing {file}: {e}")
