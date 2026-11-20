import { onMounted, onUnmounted, readonly, ref } from "vue";
import type { AuctionInfo } from "@/types";

const nowMs = ref(Date.now());
let timer: ReturnType<typeof setInterval> | null = null;
let consumers = 0;

function tick() {
  nowMs.value = Date.now();
}

export function useAuctionClock() {
  onMounted(() => {
    consumers++;
    tick();
    if (!timer) timer = setInterval(tick, 1000);
  });
  onUnmounted(() => {
    consumers = Math.max(0, consumers - 1);
    if (consumers === 0 && timer) {
      clearInterval(timer);
      timer = null;
    }
  });

  function getCurrentPrice(product: {
    price: number;
    auction?: AuctionInfo | null;
  }) {
    return product.price;
  }

  return { now: readonly(nowMs), getCurrentPrice };
}

export const auctionNow = readonly(nowMs);

export interface AuctionState {
  msToEnd: number | null;
}

export function computeAuctionState(a: AuctionInfo, now: number): AuctionState {
  const end = Date.parse(a.endTime);
  if (!Number.isFinite(end)) {
    return { msToEnd: 0 };
  }
  const msToEnd = Math.max(0, end - now);
  return {
    msToEnd: msToEnd > 0 ? msToEnd : 0,
  };
}

export function formatCountdown(ms: number | null): string {
  if (ms === null || !Number.isFinite(ms) || ms <= 0) return "Encerrado";
  const total = Math.ceil(ms / 1000);
  const h = Math.floor(total / 3600);
  const m = Math.floor((total % 3600) / 60);
  const s = total % 60;
  if (h > 0) return `${h}h ${String(m).padStart(2, "0")}min`;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

export function formatBRL(v: number | string | null | undefined): string {
  const num = Number(v);
  if (!Number.isFinite(num)) return "R$ 0,00";
  return `R$ ${num.toFixed(2).replace(".", ",")}`;
}

