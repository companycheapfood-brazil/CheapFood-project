import re

with open('src/views/merchant/DashboardView.vue', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix script
script_update = """import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MerchantHeader from '@/components/merchant/MerchantHeader.vue'
import MerchantBottomNav from '@/components/merchant/MerchantBottomNav.vue'
import { useMerchantStore } from '@/stores/useMerchantStore'
import { storeToRefs } from 'pinia'

const route = useRoute()
const router = useRouter()
const showEmptyState = computed(() => route.query.new === '1')

const merchantStore = useMerchantStore()
const { stats } = storeToRefs(merchantStore)

const activePeriod = ref('7days')

const periodLabels: Record<string, string> = {
  'today': 'Hoje',
  '7days': 'Últimos 7 dias',
  'month': 'Este Mês',
  'year': 'Este Ano'
}

const subtitleText = computed(() => periodLabels[activePeriod.value])

watch(activePeriod, (newPeriod) => {
  merchantStore.fetchDashboardStats(newPeriod)
})

onMounted(() => {
  merchantStore.fetchDashboardStats(activePeriod.value)
})

const maxSales = computed(() => Math.max(1, ...stats.value.dailySales.map((d) => d.value)))
"""

c = re.sub(r'<script setup lang="ts">.*?</script>', '<script setup lang="ts">\n' + script_update + '\n</script>', c, flags=re.DOTALL)

# Update MerchantHeader subtitle
c = c.replace('subtitle="Últimos 7 dias"', ':subtitle="subtitleText"')

# Update Toggle UI
toggle_html = """    <main class="content">
      <div class="filter-tabs">
        <button :class="{ active: activePeriod === 'today' }" @click="activePeriod = 'today'">Hoje</button>
        <button :class="{ active: activePeriod === '7days' }" @click="activePeriod = '7days'">7 Dias</button>
        <button :class="{ active: activePeriod === 'month' }" @click="activePeriod = 'month'">Mês</button>
        <button :class="{ active: activePeriod === 'year' }" @click="activePeriod = 'year'">Ano</button>
      </div>

      <div class="metrics-grid">"""

c = c.replace("""    <main class="content">
      <div class="metrics-grid">""", toggle_html)

# Update subtitle inside the chart and the extra stats labels
c = c.replace('<span class="chart-subtitle">Últimos 7 dias</span>', '<span class="chart-subtitle">{{ subtitleText }}</span>')

# Update "+14%" to be dynamic
c = c.replace('14%', '{{ stats.growth }}%')
c = c.replace('vs semana anterior', '{{ activePeriod === \'today\' ? \'vs ontem\' : activePeriod === \'month\' ? \'vs mês anterior\' : activePeriod === \'year\' ? \'vs ano passado\' : \'vs semana anterior\' }}')
c = c.replace('Ticket Médio (Semanal)', 'Ticket Médio ({{ activePeriod === \'today\' ? \'Hoje\' : activePeriod === \'month\' ? \'Mensal\' : activePeriod === \'year\' ? \'Anual\' : \'Semanal\' }})')

# Add Filter Tabs CSS
css = """
.filter-tabs {
  display: flex;
  background: var(--mc-surface);
  border: 1px solid var(--mc-border);
  border-radius: var(--cf-radius-md);
  padding: 4px;
  margin-bottom: 16px;
}
.filter-tabs button {
  flex: 1;
  background: transparent;
  border: none;
  padding: 8px 0;
  font-size: 12px;
  font-weight: 600;
  color: var(--mc-text-muted);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}
.filter-tabs button.active {
  background: var(--mc-purple);
  color: #fff;
  box-shadow: 0 2px 5px rgba(124, 111, 234, 0.3);
}
"""

if '.filter-tabs' not in c:
    c = c.replace('</style>', css + '\n</style>')

with open('src/views/merchant/DashboardView.vue', 'w', encoding='utf-8') as f:
    f.write(c)
