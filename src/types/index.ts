export interface Product {
  id: string
  name: string
  quantityLabel: string // ex: "8 unidades"
  price: number
  originalPrice?: number
  discountLabel?: string // ex: "-50% OFF"
  expiresLabel?: string // ex: "Vence hoje" | "Vence amanhã"
  category: string
  store: string
  distance: string
  validity: string // ex: "12/05/2026"
  icon: string // emoji usado como "foto" do produto
  reviews: Review[]
}

export interface Review {
  authorInitials: string
  authorName: string
  rating: number
  comment: string
}

export interface CartItem {
  product: Product
  quantity: number
}

// ---------- Painel do lojista ----------

export type MerchantProductStatus = 'ativo' | 'vencido' | 'vendido'

export interface MerchantProduct {
  id: string
  name: string
  category: string
  icon: string
  originalPrice: number
  promoPrice: number
  quantityAvailable: number
  reservedCount: number
  validity: string // DD/MM/AAAA
  expiresLabel: string // "Vence amanhã" | "Vence em 2d" | "Vencido"
  status: MerchantProductStatus
  paused: boolean
}

export type OrderStatus = 'pendente' | 'retirado' | 'expirado'

export interface Order {
  id: string
  customerName: string
  productName: string
  quantity: number
  code: string
  pickupDeadline: string // HH:MM
  status: OrderStatus
}

export interface DailySales {
  label: string
  value: number
}

