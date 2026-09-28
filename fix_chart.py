import re

with open('src/views/merchant/DashboardView.vue', 'r', encoding='utf-8') as f:
    content = f.read()

old_chart_html = """      <section class="chart-card">
        <p class="chart-title">Vendas por dia</p>
        <div class="chart-bars">
          <div v-for="(d, i) in stats.dailySales" :key="d.label" class="bar-col">
            <div
              class="bar"
              :class="{ peak: i === peakDayIndex }"
              :style="{ height: `${(d.value / maxSales) * 100}%` }"
            ></div>
            <span class="bar-label">{{ d.label }}</span>
          </div>
        </div>
      </section>"""

new_chart_html = """      <section class="chart-card">
        <div class="chart-header">
          <p class="chart-title">Faturamento Diário</p>
          <span class="chart-subtitle">Últimos 7 dias</span>
        </div>
        <div class="chart-bars">
          <div v-for="(d, i) in stats.dailySales" :key="d.label" class="bar-col">
            <span class="bar-value" v-if="d.value > 0">{{ d.value >= 1000 ? (d.value/1000).toFixed(1) + 'k' : Math.round(d.value) }}</span>
            <span class="bar-value zero" v-else>-</span>
            <div
              class="bar"
              :class="{ peak: i === peakDayIndex && d.value > 0 }"
              :style="{ height: `${(d.value / maxSales) * 100}%`, minHeight: d.value > 0 ? '12px' : '4px' }"
            ></div>
            <span class="bar-label" :class="{ today: i === stats.dailySales.length - 1 }">{{ d.label }}</span>
          </div>
        </div>
        <div class="chart-footer">
          <div class="indicator">
            <span class="dot peak-dot"></span> Maior Faturamento
          </div>
          <div class="indicator">
            <span class="dot"></span> Regular
          </div>
        </div>
      </section>"""

content = content.replace(old_chart_html, new_chart_html)

new_css = """
.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.chart-title {
  font-size: 14px;
  font-weight: 800;
  color: var(--mc-navy);
  margin: 0;
}

.chart-subtitle {
  font-size: 11px;
  color: var(--mc-text-muted);
  font-weight: 600;
  background: var(--cf-bg);
  padding: 4px 8px;
  border-radius: 12px;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  height: 120px;
  gap: 6px;
}

.bar-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  height: 100%;
}

.bar-value {
  font-size: 10px;
  font-weight: 700;
  color: var(--mc-navy);
  margin-bottom: 6px;
}

.bar-value.zero {
  color: #ccc;
}

.bar {
  width: 100%;
  max-width: 24px;
  background: var(--mc-cream-border);
  border-radius: 6px 6px 2px 2px;
  transition: all 0.3s ease;
}

.bar.peak {
  background: var(--mc-navy);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.bar:hover {
  filter: brightness(0.9);
}

.bar-label {
  font-size: 10px;
  color: var(--mc-text-muted);
  margin-top: 8px;
  font-weight: 600;
}

.bar-label.today {
  color: var(--mc-navy);
  font-weight: 800;
}

.chart-footer {
  display: flex;
  gap: 16px;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px dashed var(--mc-border);
}

.indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  font-weight: 600;
  color: var(--mc-text-muted);
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--mc-cream-border);
}

.dot.peak-dot {
  background: var(--mc-navy);
}
"""

# Replace old CSS with new
# I will just replace from .chart-title to .bar-label
css_to_replace_regex = r'\.chart-title \{.*?(?=\.alert-banner \{)'
content = re.sub(css_to_replace_regex, new_css.strip() + "\n\n", content, flags=re.DOTALL)

with open('src/views/merchant/DashboardView.vue', 'w', encoding='utf-8') as f:
    f.write(content)
