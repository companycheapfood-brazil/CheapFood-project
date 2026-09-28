import re

with open('src/views/merchant/SettingsView.vue', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix encoding issues
c = c.replace('HorÃ¡rio de funcionamento', 'Horário de funcionamento')
c = c.replace('NotificaÃ§Ãµes', 'Notificações')
c = c.replace('ConfiguraÃ§Ãµes', 'Configurações')
c = c.replace('â€º', '›')

# Replace the whole script setup with SVG-based icons
old_script = """<script setup lang="ts">
import MerchantHeader from '@/components/merchant/MerchantHeader.vue'
import MerchantBottomNav from '@/components/merchant/MerchantBottomNav.vue'
import { merchantStats } from '@/data/merchant'

const menuItems = [
  { label: 'Dados da loja', icon: 'ðŸª' },
  { label: 'Horário de funcionamento', icon: 'ðŸ•'' },
  { label: 'Formas de pagamento', icon: 'ðŸ'³' },
  { label: 'Notificações', icon: 'ðŸ""' },
  { label: 'Central de ajuda', icon: 'â"' },
]
</script>"""

new_script = """<script setup lang="ts">
import { useRouter } from 'vue-router'
import MerchantHeader from '@/components/merchant/MerchantHeader.vue'
import MerchantBottomNav from '@/components/merchant/MerchantBottomNav.vue'

const router = useRouter()

const menuItems = [
  { label: 'Dados da loja', icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4"/><path d="M2 7h20"/><path d="M22 7v3a2 2 0 0 1-2 2a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 16 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 12 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 8 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 4 12a2 2 0 0 1-2-2V7"/></svg>' },
  { label: 'Horário de funcionamento', icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>' },
  { label: 'Formas de pagamento', icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>' },
  { label: 'Notificações', icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>' },
  { label: 'Central de ajuda', icon: '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg>' },
]

const logout = () => {
  localStorage.removeItem('user')
  router.push('/start')
}
</script>"""

c = c.replace(old_script, new_script)

# Also fix the template to use v-html for icons and the logout
old_template_part = """        <button v-for="item in menuItems" :key="item.label" class="menu-row">
          <span>{{ item.icon }} {{ item.label }}</span>
          <span class="chevron">›</span>
        </button>"""

new_template_part = """        <button v-for="item in menuItems" :key="item.label" class="menu-row" style="cursor: pointer;">
          <span class="menu-item-content">
            <span class="menu-icon" v-html="item.icon"></span>
            {{ item.label }}
          </span>
          <svg class="chevron-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
        </button>"""

c = c.replace(old_template_part, new_template_part)

# Fix the logout button
c = c.replace(
    '<button class="menu-row danger">Sair da conta</button>',
    '<button class="menu-row danger" @click="logout" style="cursor: pointer;"><span class="menu-item-content"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/></svg>Sair da conta</span></button>'
)

# Fix the header merchantStats reference
c = c.replace(
    ':subtitle="merchantStats.storeName"',
    'subtitle="Padaria Central"'
)

# Add new CSS
new_css = """
.menu-item-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.menu-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: var(--mc-purple-soft, #f0eeff);
  color: var(--mc-purple, #7c6fea);
  flex-shrink: 0;
}

.chevron-icon {
  color: var(--mc-text-muted);
  flex-shrink: 0;
}

.menu-row:hover {
  background-color: var(--cf-bg, #fafafa);
}

.menu-row.danger .menu-item-content {
  gap: 12px;
}

.menu-row.danger svg {
  color: var(--mc-danger);
}
"""

c = c.replace('</style>', new_css + '\n</style>')

with open('src/views/merchant/SettingsView.vue', 'w', encoding='utf-8') as f:
    f.write(c)
