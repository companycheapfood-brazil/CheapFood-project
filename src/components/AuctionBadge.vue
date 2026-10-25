<script setup lang="ts">
import { computed } from "vue";
import {
  computeAuctionState,
  formatBRL,
  formatCountdown,
  useAuctionClock,
} from "@/composables/useAuctionClock";

const props = withDefaults(
  defineProps<{
    auction: any;
    /** compact = selo para cards; full = painel da tela do produto */
    variant?: "compact" | "full";
  }>(),
  { variant: "compact" },
);

const { now } = useAuctionClock();
const state = computed(() => computeAuctionState(props.auction, now.value));
const countdown = computed(() => formatCountdown(state.value.msToEnd));

// Cálculo da régua visual do leilão híbrido
const startPrice = computed(() => Number(props.auction.startPrice || 0));
const currentBid = computed(() => Number(props.auction.highestBid || props.auction.startPrice || 0));
const minPrice = computed(() => Number(props.auction.minPrice || (startPrice.value * 1.5)));

// Porcentagem de progresso do tempo / lances
const progressPercent = computed(() => {
  if (props.auction.ended || (state.value.msToEnd ?? 0) <= 0) return 100;
  const endMs = props.auction.endTime ? Date.parse(props.auction.endTime) : 0;
  if (!endMs || endMs <= now.value) return 100;
  const startMs = props.auction.startTime ? Date.parse(props.auction.startTime) : 0;
  const totalDuration =
    startMs && endMs > startMs ? endMs - startMs : 2 * 60 * 60 * 1000;
  const remaining = Math.max(0, endMs - now.value);
  const pct = Math.min(100, Math.max(10, Math.round(((totalDuration - remaining) / totalDuration) * 100)));
  return pct;
});
</script>

<template>
  <!-- Selo compacto (cards da vitrine) -->
  <span
    v-if="variant === 'compact'"
    class="auction-chip"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="12"
      height="12"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2.5"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <path
        d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"
      />
    </svg>
    Leilão: {{ formatBRL(auction.highestBid || auction.startPrice) }}
  </span>

  <!-- Painel completo com Régua Visual do Leilão Híbrido (tela do produto) -->
  <div v-else class="auction-panel">
    <div class="panel-head">
      <div class="panel-title-group">
        <span class="panel-title">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"
            />
          </svg>
          Leilão Híbrido Ativo
        </span>
        <span class="panel-subtitle">Dispute com lances ou compre agora na hora</span>
      </div>
      <div class="countdown-badge">
        <span class="countdown-label">Termina em:</span>
        <span class="countdown-time">{{ countdown }}</span>
      </div>
    </div>

    <!-- Régua Visual do Leilão -->
    <div class="decay-timeline-box">
      <div class="timeline-track">
        <div class="timeline-fill" :style="{ width: `${progressPercent}%` }"></div>
        <div class="timeline-pointer" :style="{ left: `${progressPercent}%` }">
          <span class="pointer-ping"></span>
          <span class="pointer-value">{{ formatBRL(currentBid) }}</span>
        </div>
      </div>
      <div class="timeline-milestones">
        <div class="milestone start">
          <span class="m-label">Lance Inicial</span>
          <strong class="m-price">{{ formatBRL(startPrice) }}</strong>
        </div>
        <div class="milestone current">
          <span class="m-label">Maior Lance</span>
          <strong class="m-price highlighted">{{ formatBRL(currentBid) }}</strong>
        </div>
        <div class="milestone min">
          <span class="m-label">Compra Direta</span>
          <strong class="m-price">{{ formatBRL(minPrice) }}</strong>
        </div>
      </div>
    </div>

    <div class="panel-footer-hint">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="14"
        height="14"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <circle cx="12" cy="12" r="10" />
        <line x1="12" y1="16" x2="12" y2="12" />
        <line x1="12" y1="8" x2="12.01" y2="8" />
      </svg>
      <span>
        Você pode <strong>Comprar Agora</strong> para garantir a unidade imediatamente, ou <strong>dar um lance</strong> para disputar pelo menor valor.
      </span>
    </div>
  </div>
</template>

<style scoped>
.auction-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 10px;
  font-weight: 700;
  color: #fff;
  background: linear-gradient(135deg, #ff3b69 0%, #ff7a45 100%);
  padding: 2px 8px;
  border-radius: 999px;
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
  box-shadow: 0 2px 6px rgba(255, 59, 105, 0.25);
}

.auction-panel {
  background: #ffffff;
  border: 1px solid #ffd2dd;
  border-radius: 18px;
  padding: 16px;
  margin-bottom: 1.25rem;
  box-shadow: 0 6px 20px rgba(255, 59, 105, 0.09);
}

.panel-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 14px;
}

.panel-title-group {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.panel-title {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-weight: 800;
  color: #ff3b69;
  font-size: 0.95rem;
}

.panel-subtitle {
  font-size: 0.72rem;
  color: #6b7280;
  font-weight: 500;
}

.countdown-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #fff0f3;
  border: 1px solid #ffd0dc;
  border-radius: 10px;
  padding: 5px 10px;
}

.countdown-label {
  font-size: 0.68rem;
  color: #ff3b69;
  font-weight: 700;
  text-transform: uppercase;
}

.countdown-time {
  font-weight: 800;
  font-size: 0.95rem;
  color: #1f2937;
  font-variant-numeric: tabular-nums;
}

/* Régua Visual de Decaimento */
.decay-timeline-box {
  background: #fdfaf7;
  border: 1px solid #fae8d8;
  border-radius: 14px;
  padding: 14px 12px 10px;
  margin-bottom: 12px;
}

.timeline-track {
  position: relative;
  height: 8px;
  background: #e5e7eb;
  border-radius: 999px;
  margin: 18px 8px 10px;
}

.timeline-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff7a45 0%, #ff3b69 100%);
  border-radius: 999px;
  transition: width 0.3s ease;
}

.timeline-pointer {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}

.pointer-ping {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #ff3b69;
  border: 3px solid #ffffff;
  box-shadow: 0 0 0 3px rgba(255, 59, 105, 0.35);
  animation: pulse-ring 1.8s infinite;
}

@keyframes pulse-ring {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 59, 105, 0.5);
  }
  70% {
    box-shadow: 0 0 0 8px rgba(255, 59, 105, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 59, 105, 0);
  }
}

.pointer-value {
  position: absolute;
  top: -24px;
  background: #1f2937;
  color: #ffffff;
  font-size: 0.68rem;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 6px;
  white-space: nowrap;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.timeline-milestones {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 0.72rem;
}

.milestone {
  display: flex;
  flex-direction: column;
}

.milestone.start {
  align-items: flex-start;
}

.milestone.current {
  align-items: center;
}

.milestone.min {
  align-items: flex-end;
}

.m-label {
  font-size: 0.65rem;
  color: #9ca3af;
  font-weight: 600;
  text-transform: uppercase;
}

.m-price {
  font-size: 0.82rem;
  font-weight: 700;
  color: #4b5563;
}

.m-price.highlighted {
  color: #ff3b69;
  font-weight: 800;
}

.panel-footer-hint {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 0.73rem;
  color: #6b7280;
  line-height: 1.4;
  background: #fafaf9;
  border-radius: 10px;
  padding: 8px 10px;
}

.panel-footer-hint svg {
  color: #f59e0b;
  flex-shrink: 0;
  margin-top: 1px;
}
</style>
