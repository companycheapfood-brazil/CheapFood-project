import axios from "axios";
import { API_URL } from "@/config/api";
import { bumpSessionVersion, clearAuthStorage } from "@/utils/auth";

const AUTH_API = `${API_URL}/auth/`;

class AuthService {
  login(user: any) {
    return axios
      .post(AUTH_API + "login", {
        email: user.email,
        password: user.password,
      })
      .then((response) => {
        if (!response.data?.token || !response.data?.user) {
          throw new Error("Resposta inválida do servidor ao autenticar.");
        }
        localStorage.setItem("user", JSON.stringify(response.data));
        bumpSessionVersion();
        return response.data;
      });
  }

  async logout() {
    try {
      await axios.post(AUTH_API + "logout");
    } catch (e) {
      console.error("Logout error:", e);
    } finally {
      clearAuthStorage();
    }
  }

  register(user: any) {
    return axios.post(AUTH_API + "register", {
      name: user.name,
      email: user.email,
      password: user.password,
      role: user.role,
      storeName: user.storeName,
    });
  }

  forgotPassword(email: string) {
    return axios.post(AUTH_API + "forgot-password", {
      email,
    });
  }

  resetPassword(data: any) {
    return axios.post(AUTH_API + "reset-password", {
      token: data.token,
      email: data.email,
      password: data.password,
    });
  }
}

export default new AuthService();
