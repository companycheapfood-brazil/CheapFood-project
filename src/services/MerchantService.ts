import { merchantProducts, orders } from "@/data/merchant";
import type { MerchantProduct, Order } from "@/types";

/**
 * Serviço para o painel do lojista.
 */
export const MerchantService = {
  /**
   * Retorna os produtos do lojista.
   */
  async getProducts(): Promise<MerchantProduct[]> {
    return new Promise((resolve) => {
      setTimeout(() => resolve([...merchantProducts]), 100);
    });
  },

  /**
   * Retorna os pedidos do lojista.
   */
  async getOrders(): Promise<Order[]> {
    return new Promise((resolve) => {
      setTimeout(() => resolve([...orders]), 100);
    });
  },

  /**
   * Mock para simular atualização de status de produto.
   */
  async updateProductStatus(
    id: string,
    updates: Partial<MerchantProduct>,
  ): Promise<void> {
    return new Promise((resolve) => {
      setTimeout(resolve, 50);
    });
  },
};
