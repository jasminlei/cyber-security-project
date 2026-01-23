<template>
  <div class="create-item">
    <h2>{{ editMode ? "Edit Item" : "Create New Item" }}</h2>

    <form @submit.prevent="handleSubmit">
      <div v-if="error" class="error">{{ error }}</div>

      <div class="form-group">
        <label for="title">Title:</label>
        <input id="title" v-model="formData.title" type="text" required />
      </div>

      <div class="form-group">
        <label for="description">Description:</label>
        <textarea id="description" v-model="formData.description" rows="5" required></textarea>
      </div>

      <div class="form-group">
        <label for="price">Price (€):</label>
        <input id="price" v-model="formData.price" type="number" step="0.01" min="0" required />
      </div>

      <div class="form-group">
        <label for="contact">Contact (phone number, email, Telegram etc.):</label>
        <input id="contact" v-model="formData.contact" type="text" />
      </div>

      <div class="form-group">
        <label for="image_url">Image URL (optional):</label>
        <input id="image_url" v-model="formData.image_url" type="url" />
      </div>

      <div class="form-actions">
        <button type="submit" class="btn-primary">{{ editMode ? "Update" : "Create" }} Item</button>
        <button type="button" @click="cancel" class="btn-secondary">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import api from "../services/api";

const router = useRouter();
const route = useRoute();

const editMode = ref(false);
const error = ref("");
const formData = ref({
  title: "",
  description: "",
  price: "",
  contact: "",
  image_url: "",
});

async function handleSubmit() {
  error.value = "";

  try {
    if (editMode.value) {
      await api.updateItem(route.params.id, formData.value);
    } else {
      await api.createItem(formData.value);
    }
    router.push("/my-items");
  } catch (err) {
    error.value = err.response?.data?.detail || "Failed to save item";
  }
}

function cancel() {
  router.back();
}

onMounted(async () => {
  if (route.params.id) {
    editMode.value = true;
    try {
      const response = await api.getItem(route.params.id);
      formData.value = {
        title: response.data.title,
        description: response.data.description,
        price: response.data.price,
        contact: response.data.contact || "",
        image_url: response.data.image_url || "",
      };
    } catch {
      error.value = "Failed to load item";
    }
  }
});
</script>

<style scoped>
.create-item {
  max-width: 1400px;
  margin: 0 auto;
}

.create-item h2 {
  color: #1a1f36;
  font-size: 1.75rem;
  margin-bottom: 2rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #1a1f36;
  font-size: 0.875rem;
}

input,
textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e6ebf1;
  border-radius: 8px;
  font-family: inherit;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  background: #f7f9fc;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #5469d4;
  background: white;
  box-shadow: 0 0 0 3px rgba(84, 105, 212, 0.1);
}

textarea {
  resize: vertical;
  min-height: 120px;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 2rem;
}

.btn-primary,
.btn-secondary {
  flex: 1;
  padding: 0.875rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.btn-primary {
  background: #5469d4;
  color: white;
}

.btn-primary:hover {
  background: #4558c9;
  box-shadow: 0 2px 8px rgba(84, 105, 212, 0.3);
}

.btn-secondary {
  background-color: #f7f9fc;
  color: #697386;
  border: 1px solid #e6ebf1;
}

.btn-secondary:hover {
  background-color: #e6ebf1;
}

.error {
  color: #e25950;
  margin-bottom: 1rem;
  padding: 0.75rem 1rem;
  background-color: #fef6f6;
  border-left: 3px solid #e25950;
  border-radius: 6px;
  font-size: 0.875rem;
}
</style>
