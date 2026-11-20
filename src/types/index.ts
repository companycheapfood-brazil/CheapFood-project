/** Lance de um leilão, conforme retornado pela API. */
export interface AuctionBid {
  id: number;
  valor: number;
  usuario: string;
  usuario_id: string;
  data: string | null; // ISO UTC
}

/**
 * Leilão híbrido ("Compre Agora ou Dê um Lance"), conforme retornado pela API.
 * Datas em ISO UTC.
 */
export interface AuctionInfo {
  active?: boolean;
  startPrice: number;
  minPrice?: number;
  highestBid: number;
  startTime?: string | null;
  endTime: string;
  bids: AuctionBid[];
  /** ID (string) do usuário com o maior lance, ou null se não houver lances. */
  winnerId: string | null;
  ended: boolean;
}

export interface Product {
  id: string;
  name: string;
  quantityLabel: string; // ex: "8 unidades"
  price: number;
  originalPrice?: number;
  discountLabel?: string; // ex: "-50% OFF"
  expiresLabel?: string; // ex: "Vence hoje" | "Vence amanhã"
  category: string;
  store: string;
  storeAddress?: string;
  distance: string;
  validity: string; // ex: "12/05/2026"
  icon: string; // emoji usado como "foto" do produto
  reviews: Review[];
  // Campos adicionais retornados pela API
  image?: string;
  old_price?: number;
  expires_in?: string;
  description?: string;
  quantity?: number;
  auction?: AuctionInfo | null;
}

export interface Review {
  id?: number;
  authorInitials?: string;
  authorName?: string;
  author?: string;
  initials?: string;
  rating: number;
  comment: string;
  tags?: string[];
  merchantReply?: string | null;
  productName?: string;
  dateFormatted?: string;
}

export interface CartItem {
  product: Product;
  quantity: number;
}

// ---------- Painel do lojista ----------

export type MerchantProductStatus = "ativo" | "vencido" | "vendido" | "pausado";

export interface MerchantProduct {
  id: string;
  name: string;
  category: string;
  icon: string;
  originalPrice: number;
  promoPrice: number;
  quantityAvailable: number;
  reservedCount: number;
  validity: string; // DD/MM/AAAA
  expiresLabel: string; // "Vence amanhã" | "Vence em 2d" | "Vencido"
  status: MerchantProductStatus;
  paused: boolean;
  image?: string;
  auction?: AuctionInfo | null;
}

export type OrderStatus = "pendente" | "retirado" | "expirado";

export interface Order {
  id: string;
  customerName: string;
  customerEmail?: string;
  customerPhone?: string;
  productName: string;
  productImage?: string | null;
  quantity: number;
  code: string;
  pickupDeadline: string; // HH:MM
  status: OrderStatus;
  price?: number;
  total?: number;
  createdAt?: string;
}

export interface DailySales {
  label: string;
  value: number;
}
