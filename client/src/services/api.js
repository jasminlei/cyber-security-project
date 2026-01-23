import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default {
  // Auth
  register(data) {
    return api.post("/auth/register/", data);
  },
  login(data) {
    return api.post("/auth/login/", data);
  },
  logout() {
    return api.post("/auth/logout/");
  },
  getCurrentUser() {
    return api.get("/auth/me/");
  },

  // Items
  getItems(search = "") {
    return api.get("/items/", { params: { search } });
  },
  getItem(id) {
    return api.get(`/items/${id}/`);
  },
  createItem(data) {
    return api.post("/items/", data);
  },
  updateItem(id, data) {
    return api.put(`/items/${id}/`, data);
  },
  deleteItem(id) {
    return api.delete(`/items/${id}/`);
  },
  getUserItems() {
    return api.get("/items/my-items/");
  },
  toggleLike(itemId) {
    return api.post(`/items/${itemId}/like/`);
  },
  getLikedItems() {
    return api.get("/items/liked/");
  },
};
