import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useFavoritesStore = defineStore('favorites', () => {
  const favorites = ref<number[]>([])

  const fetchFavorites = async () => {
    try {
      const res = await fetch('http://127.0.0.1:5000/api/favorites')
      const data = await res.json()
      favorites.value = data
    } catch (e) {
      console.error(e)
    }
  }

  const toggleFavorite = async (productId: number) => {
    const isFav = favorites.value.includes(productId)
    const method = isFav ? 'DELETE' : 'POST'
    
    // Optimistic UI update
    if (isFav) {
      favorites.value = favorites.value.filter(id => id !== productId)
    } else {
      favorites.value.push(productId)
    }

    try {
      await fetch(`http://127.0.0.1:5000/api/favorites/${productId}`, {
        method
      })
    } catch (e) {
      console.error(e)
      // Revert if failed
      if (isFav) {
        favorites.value.push(productId)
      } else {
        favorites.value = favorites.value.filter(id => id !== productId)
      }
    }
  }

  const isFavorite = (productId: number) => {
    return favorites.value.includes(productId)
  }

  return {
    favorites,
    fetchFavorites,
    toggleFavorite,
    isFavorite
  }
})
