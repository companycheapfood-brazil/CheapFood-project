import { products } from "@/data/products";
import type { Product } from "@/types";

/**
 * Serviço para manipulação de produtos do cliente.
 */
export const ProductService = {
  /**
   * Retorna todos os produtos disponíveis.
   */
  async getProducts(): Promise<Product[]> {
    // Simula uma chamada de API
    return new Promise((resolve) => {
      setTimeout(() => resolve(products), 100);
    });
  },

  /**
   * Busca um produto pelo ID.
   */
  async getProductById(id: string): Promise<Product | undefined> {
    return new Promise((resolve) => {
      setTimeout(() => {
        const product = products.find((p) => p.id === id);
        resolve(product);
      }, 50);
    });
  },

  /**
   * Filtra produtos por categoria e termo de busca.
   */
  filterProducts(
    products: Product[],
    category: string,
    search: string,
  ): Product[] {
    return products.filter((p) => {
      const matchesFilter = category === "Todos" || p.category === category;
      const matchesSearch = p.name.toLowerCase().includes(search.toLowerCase());
      return matchesFilter && matchesSearch;
    });
  },
};
