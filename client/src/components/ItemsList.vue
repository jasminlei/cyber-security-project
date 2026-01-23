<template>
  <div class="items-list">
    <div class="header">
      <h2>Marketplace Items</h2>
      <div class="search-bar">
        <input
          v-model="searchQuery"
          @input="handleSearch"
          type="text"
          placeholder="Search items..."
        />
      </div>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="items.length === 0" class="no-items">No items found</div>

    <div v-else class="items-grid">
      <div v-for="item in items" :key="item.id" class="item-card">
        <div class="item-image" v-if="item.image_url">
          <img :src="item.image_url" :alt="item.title" />
        </div>
        <div class="item-content">
          <h3>{{ item.title }}</h3>
          <p class="description">{{ item.description }}</p>
          <p class="price">{{ item.price }} €</p>
          <p class="seller">Seller: {{ item.seller_username }}</p>

          <div class="item-actions">
            <button
              v-if="authStore.isAuthenticated"
              @click="toggleLike(item)"
              class="btn-like"
              :class="{ liked: item.is_liked }"
            >
              {{ item.is_liked ? "❤️" : "🤍" }} {{ item.likes_count }}
            </button>
            <router-link :to="`/items/${item.id}`" class="btn-view"> View Details </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useAuthStore } from "../stores/auth";
import api from "../services/api";

const authStore = useAuthStore();
const items = ref([]);
const loading = ref(false);
const searchQuery = ref("");
let searchTimeout = null;

async function fetchItems(search = "") {
  loading.value = true;
  try {
    const response = await api.getItems(search);
    items.value = response.data;
  } catch (error) {
    console.error("Error fetching items:", error);
  } finally {
    loading.value = false;
  }
}

function handleSearch() {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    fetchItems(searchQuery.value);
  }, 300);
}

async function toggleLike(item) {
  try {
    const response = await api.toggleLike(item.id);
    item.is_liked = response.data.liked;
    item.likes_count += response.data.liked ? 1 : -1;
  } catch (error) {
    console.error("Error toggling like:", error);
  }
}

onMounted(() => {
  fetchItems();
});
</script>

<style scoped>
.items-list {
  width: 100%;
}

.header {
  margin-bottom: 2rem;
}

.header h2 {
  color: #1a1f36;
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.search-bar input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e6ebf1;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  background: #f7f9fc;
}

.search-bar input:focus {
  outline: none;
  border-color: #5469d4;
  background: white;
  box-shadow: 0 0 0 3px rgba(84, 105, 212, 0.1);
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.item-card {
  background: white;
  border: 1px solid #e6ebf1;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.item-card:hover {
  box-shadow:
    0 4px 12px rgba(50, 50, 93, 0.1),
    0 1px 3px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.item-image img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  background: #f7f9fc;
}

.item-content {
  padding: 1.25rem;
}

.item-content h3 {
  margin: 0 0 0.5rem;
  color: #1a1f36;
  font-size: 1.125rem;
  font-weight: 600;
  letter-spacing: -0.3px;
}

.description {
  color: #697386;
  margin: 0.5rem 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.5;
  font-size: 0.9rem;
}

.price {
  font-size: 1.5rem;
  font-weight: 700;
  color: #5469d4;
  margin: 0.75rem 0;
  letter-spacing: -0.5px;
}

.seller {
  font-size: 0.85rem;
  color: #8898aa;
  margin-bottom: 1rem;
}

.item-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.btn-like {
  padding: 0.5rem 0.875rem;
  border: 1px solid #e6ebf1;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  color: #697386;
  font-weight: 500;
}

.btn-like:hover {
  border-color: #5469d4;
  background-color: #f7f9fc;
}

.btn-like.liked {
  background: #5469d4;
  color: white;
  border-color: #5469d4;
}

.btn-view {
  flex: 1;
  padding: 0.5rem 0.875rem;
  background: #5469d4;
  color: white;
  text-align: center;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.btn-view:hover {
  background: #4558c9;
  box-shadow: 0 2px 4px rgba(84, 105, 212, 0.2);
}

.loading,
.no-items {
  text-align: center;
  padding: 3rem;
  color: #8898aa;
  font-size: 1rem;
}
</style>
