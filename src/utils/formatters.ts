/**
 * Formata um número para o formato de moeda Real (BRL).
 * @param value Valor numérico a ser formatado.
 * @returns String formatada (ex: "R$ 10,00")
 */
export function formatCurrency(value: number): string {
  return value.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  })
}

/**
 * Formata uma data para o padrão brasileiro (DD/MM/AAAA).
 * @param date Objeto Date ou string de data.
 * @returns String formatada.
 */
export function formatDate(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date
  return d.toLocaleDateString('pt-BR')
}
