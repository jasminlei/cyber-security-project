<template>
  <div class="my-items">
    <div class="header">
      <h2>My Items</h2>
      <router-link to="/create-item" class="btn-primary"> Add New Item </router-link>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="items.length === 0" class="no-items">You haven't listed any items yet.</div>

    <div v-else class="items-list">
      <div v-for="item in items" :key="item.id" class="item-row">
        <div class="item-info">
          <h3>{{ item.title }}</h3>
          <p class="price">{{ item.price }} €</p>
          <p class="stats">
            {{ item.likes_count }} likes • Posted {{ formatDate(item.created_at) }}
          </p>
        </div>
        <div class="item-actions">
          <router-link :to="`/items/${item.id}`" class="btn-view"> View </router-link>
          <router-link :to="`/edit-item/${item.id}`" class="btn-edit"> Edit </router-link>
          <button @click="deleteItem(item.id)" class="btn-delete">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import api from "../services/api";

const items = ref([]);
const loading = ref(false);

async function fetchMyItems() {
  loading.value = true;
  try {
    const response = await api.getUserItems();
    items.value = response.data;
  } catch (error) {
    console.error("Error fetching items:", error);
  } finally {
    loading.value = false;
  }
}

async function deleteItem(id) {
  if (confirm("Are you sure you want to delete this item?")) {
    try {
      await api.deleteItem(id);
      items.value = items.value.filter((item) => item.id !== id);
    } catch (error) {
      console.error("Error deleting item:", error);
    }
  }
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString();
}

onMounted(() => {
  fetchMyItems();
});
</script>

<style scoped>
.my-items {
  width: 100%;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h2 {
  color: #1a1f36;
  font-size: 1.75rem;
  margin: 0;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: #5469d4;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.btn-primary:hover {
  background: #4558c9;
  box-shadow: 0 2px 8px rgba(84, 105, 212, 0.3);
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.item-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  background: white;
  border: 1px solid #e6ebf1;
  border-radius: 10px;
  transition: all 0.2s ease;
}

.item-row:hover {
  box-shadow: 0 2px 8px rgba(50, 50, 93, 0.1);
}

.item-info h3 {
  margin: 0 0 0.5rem;
  color: #1a1f36;
  font-size: 1.125rem;
  font-weight: 600;
  letter-spacing: -0.3px;
}

.price {
  font-size: 1.375rem;
  font-weight: 700;
  color: #5469d4;
  margin: 0.25rem 0;
  letter-spacing: -0.5px;
}

.stats {
  font-size: 0.85rem;
  color: #8898aa;
  margin: 0.5rem 0 0;
}

.item-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-view,
.btn-edit,
.btn-delete {
  padding: 0.625rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  font-weight: 600;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.btn-view {
  background: #5469d4;
  color: white;
}

.btn-view:hover {
  background: #4558c9;
  box-shadow: 0 2px 4px rgba(84, 105, 212, 0.2);
}

.btn-edit {
  background-color: #ffc107;
  color: #1a1f36;
}

.btn-edit:hover {
  background-color: #ffb300;
}

.btn-delete {
  background-color: #f7f9fc;
  color: #e25950;
  border: 1px solid #e6ebf1;
}

.btn-delete:hover {
  background-color: #fef6f6;
  border-color: #e25950;
}

.loading,
.no-items {
  text-align: center;
  padding: 3rem;
  color: #8898aa;
  font-size: 1rem;
}
</style>
