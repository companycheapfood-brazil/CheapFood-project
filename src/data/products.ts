import type { Product } from "@/types";

export const products: Product[] = [
  {
    id: "leite-integral-1l",
    name: "Leite Integral 1L",
    quantityLabel: "8 unidades",
    price: 2.49,
    originalPrice: 4.99,
    discountLabel: "-50% OFF",
    expiresLabel: "Vence em 2d",
    category: "Laticínios",
    store: "Supermercado Bom Preço",
    distance: "450m de você",
    validity: "12/05/2026",
    icon: "🥛",
    reviews: [
      {
        authorInitials: "MC",
        authorName: "Maria C.",
        rating: 5,
        comment: "Produto fresco, embalagem perfeita. Ótima economia!",
      },
    ],
  },
  {
    id: "queijo-mussarela-300g",
    name: "Queijo Mussarela 300g",
    quantityLabel: "5 unidades",
    price: 8.9,
    originalPrice: 18.0,
    discountLabel: "-50% OFF",
    expiresLabel: "Vence hoje",
    category: "Laticínios",
    store: "Açougue do Zé",
    distance: "800m de você",
    validity: "17/08/2026",
    icon: "🧀",
    reviews: [
      {
        authorInitials: "JP",
        authorName: "João P.",
        rating: 4,
        comment: "Bom custo-benefício, chegou dentro da validade.",
      },
    ],
  },
  {
    id: "pao-integral-500g",
    name: "Pão Integral 500g",
    quantityLabel: "10 unidades",
    price: 3.6,
    originalPrice: 6.5,
    discountLabel: "-44% OFF",
    expiresLabel: "Vence amanhã",
    category: "Padaria",
    store: "Padaria Central",
    distance: "300m de você",
    validity: "18/08/2026",
    icon: "🍞",
    reviews: [
      {
        authorInitials: "AL",
        authorName: "Ana L.",
        rating: 5,
        comment: "Fresquinho e bem mais barato que o normal.",
      },
    ],
  },
];

export function getProductById(id: string): Product | undefined {
  return products.find((p) => p.id === id);
}
