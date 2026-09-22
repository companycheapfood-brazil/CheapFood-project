import axios from 'axios';

const API_URL = 'http://localhost:5000/api/auth/';

class AuthService {
  login(user: any) {
    return axios
      .post(API_URL + 'login', {
        email: user.email,
        password: user.password
      })
      .then(response => {
        if (response.data.token) {
          localStorage.setItem('user', JSON.stringify(response.data));
        }
        return response.data;
      });
  }

  async logout() {
    try {
      await axios.post(API_URL + 'logout');
    } catch (e) {
      console.error('Logout error:', e);
    } finally {
      localStorage.removeItem('user');
    }
  }

  register(user: any) {
    return axios.post(API_URL + 'register', {
      name: user.name,
      email: user.email,
      password: user.password,
      role: user.role
    });
  }

  forgotPassword(email: string) {
    return axios.post(API_URL + 'forgot-password', {
      email
    });
  }

  resetPassword(data: any) {
    return axios.post(API_URL + 'reset-password', {
      email: data.email,
      password: data.password
    });
  }
}

export default new AuthService();
