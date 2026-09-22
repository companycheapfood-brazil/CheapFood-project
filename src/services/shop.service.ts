import axios from 'axios';

const API_URL = 'http://localhost:5000/api/';

class ShopService {
  getProducts() {
    return axios.get(API_URL + 'products').then(res => res.data);
  }

  getProduct(id: number | string) {
    return axios.get(API_URL + 'products/' + id).then(res => res.data);
  }

  checkout(items: any[]) {
    return axios.post(API_URL + 'checkout', { items }).then(res => res.data);
  }
}

export default new ShopService();
