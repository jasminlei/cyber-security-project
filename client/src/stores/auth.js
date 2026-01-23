import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "../services/api";

export const useAuthStore = defineStore("auth", () => {
  const user = ref(null);
  const token = ref(localStorage.getItem("token") || null);

  const isAuthenticated = computed(() => !!token.value);

  async function login(credentials) {
    try {
      const response = await api.login(credentials);
      token.value = response.data.token;
      user.value = response.data.user;
      localStorage.setItem("token", response.data.token);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data || "Login failed" };
    }
  }

  async function register(userData) {
    try {
      const response = await api.register(userData);
      token.value = response.data.token;
      user.value = response.data.user;
      localStorage.setItem("token", response.data.token);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data || "Registration failed" };
    }
  }

  async function logout() {
    try {
      await api.logout();
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      token.value = null;
      user.value = null;
      localStorage.removeItem("token");
    }
  }

  async function fetchCurrentUser() {
    if (!token.value) return;
    try {
      const response = await api.getCurrentUser();
      user.value = response.data;
    } catch (error) {
      console.error("Failed to fetch user:", error);
      logout();
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    fetchCurrentUser,
  };
});
