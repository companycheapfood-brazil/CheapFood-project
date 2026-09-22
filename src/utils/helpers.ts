/**
 * Gera uma string de estrelas baseada em um rating.
 * @param rating Avaliação de 0 a 5.
 * @returns String com estrelas preenchidas e vazias (ex: "★★★☆☆")
 */
export function getStarRating(rating: number): string {
  return '★'.repeat(rating) + '☆'.repeat(5 - rating)
}

/**
 * Gera um código aleatório para reserva.
 */
export function generateId(length = 4): string {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
  let result = ''
  for (let i = 0; i < length; i++) {
    result += chars[Math.floor(Math.random() * chars.length)]
  }
  return result
}
