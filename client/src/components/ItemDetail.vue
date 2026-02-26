<template>
  <div class="item-detail" v-if="item">
    <div class="item-header">
      <h2>{{ item.title }}</h2>
      <button v-if="isOwner" @click="deleteItem" class="btn-delete">Delete Item</button>
    </div>

    <div class="item-info">
      <p class="price">{{ item.price }} €</p>
      <!-- FLAW 3: A03 - Injection (Stored XSS) -->
      <!-- Using v-html allows HTML/JavaScript execution from user input -->
      <!-- Try: <img src=x onerror="alert('XSS')" /> -->
      <p class="description" v-html="item.description"></p>
      <!-- FIX: Use {{ item.description }} instead of v-html -->
      <!-- <p class="description">{{ item.description }}</p> -->
      <p class="seller">Seller: {{ item.seller_username }}</p>
      <p class="contact" v-if="item.contact">Contact: {{ item.contact }}</p>
      <p class="image-link" v-if="item.image_url">
        Image: <a :href="item.image_url" target="_blank" rel="noopener">{{ item.image_url }}</a>
      </p>
      <p class="date">Posted: {{ formatDate(item.created_at) }}</p>

      <div class="actions" v-if="authStore.isAuthenticated && !isOwner">
        <button @click="toggleLike" class="btn-like" :class="{ liked: item.is_liked }">
          {{ item.is_liked ? "❤️ Liked" : "🤍 Like" }} ({{ item.likes_count }})
        </button>
      </div>
    </div>
  </div>
  <div v-else-if="loading" class="loading">Loading...</div>
  <div v-else class="error">Item not found</div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import api from "../services/api";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const item = ref(null);
const loading = ref(true);

const isOwner = computed(() => {
  return authStore.user && item.value && authStore.user.id === item.value.seller;
});

async function fetchItem() {
  try {
    const response = await api.getItem(route.params.id);
    item.value = response.data;
  } catch (error) {
    console.error("Error fetching item:", error);
  } finally {
    loading.value = false;
  }
}

async function toggleLike() {
  try {
    const response = await api.toggleLike(item.value.id);
    item.value.is_liked = response.data.liked;
    item.value.likes_count += response.data.liked ? 1 : -1;
  } catch (error) {
    console.error("Error toggling like:", error);
  }
}

async function deleteItem() {
  if (confirm("Are you sure you want to delete this item?")) {
    try {
      await api.deleteItem(item.value.id);
      router.push("/");
    } catch (error) {
      console.error("Error deleting item:", error);
    }
  }
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString();
}

onMounted(async () => {
  await fetchItem();
  if (authStore.isAuthenticated && !authStore.user) {
    await authStore.fetchCurrentUser();
  }
});
</script>

<style scoped>
.item-detail {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.item-header h2 {
  color: #1a1f36;
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.5px;
}

.item-image img {
  width: 100%;
  max-height: 500px;
  object-fit: cover;
  border-radius: 10px;
  margin-bottom: 2rem;
  border: 1px solid #e6ebf1;
}

.item-info {
  margin: 1.5rem 0;
}

.price {
  font-size: 2.25rem;
  font-weight: 700;
  color: #5469d4;
  margin: 0.5rem 0 1rem;
  letter-spacing: -0.5px;
}

.description {
  font-size: 1.05rem;
  margin: 1.5rem 0;
  line-height: 1.65;
  color: #1a1f36;
}

.seller,
.contact,
.image-link,
.date {
  color: #8898aa;
  margin: 0.75rem 0;
  font-size: 0.9rem;
}

.image-link a {
  color: #5469d4;
  text-decoration: none;
  word-break: break-all;
}

.image-link a:hover {
  text-decoration: underline;
}

.actions {
  margin: 1.5rem 0;
}

.btn-like {
  padding: 0.75rem 1.5rem;
  border: 1px solid #e6ebf1;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  transition: all 0.2s ease;
  color: #697386;
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

.btn-delete {
  padding: 0.625rem 1rem;
  background-color: #f7f9fc;
  color: #e25950;
  border: 1px solid #e6ebf1;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.btn-delete:hover {
  background-color: #fef6f6;
  border-color: #e25950;
}

.loading,
.error {
  text-align: center;
  padding: 3rem;
  font-size: 1rem;
  color: #8898aa;
}
</style>
