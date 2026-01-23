<template>
  <div class="auth-form">
    <h2>{{ isLogin ? "Login" : "Register" }}</h2>
    <form @submit.prevent="handleSubmit">
      <div v-if="error" class="error">{{ error }}</div>

      <div class="form-group">
        <label for="username">Username:</label>
        <input id="username" v-model="formData.username" type="text" required />
      </div>

      <div v-if="!isLogin" class="form-group">
        <label for="email">Email:</label>
        <input id="email" v-model="formData.email" type="email" :required="!isLogin" />
      </div>

      <div class="form-group">
        <label for="password">Password:</label>
        <input id="password" v-model="formData.password" type="password" required />
      </div>

      <div v-if="!isLogin" class="form-group">
        <label for="password2">Confirm Password:</label>
        <input id="password2" v-model="formData.password2" type="password" :required="!isLogin" />
      </div>

      <button type="submit" class="btn-primary">
        {{ isLogin ? "Login" : "Register" }}
      </button>
    </form>

    <p class="toggle-auth">
      {{ isLogin ? "Don't have an account?" : "Already have an account?" }}
      <button @click="toggleMode" class="btn-link">
        {{ isLogin ? "Register" : "Login" }}
      </button>
    </p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const isLogin = ref(true);
const error = ref("");
const formData = ref({
  username: "",
  email: "",
  password: "",
  password2: "",
});

function toggleMode() {
  isLogin.value = !isLogin.value;
  error.value = "";
  formData.value = {
    username: "",
    email: "",
    password: "",
    password2: "",
  };
}

async function handleSubmit() {
  error.value = "";

  if (isLogin.value) {
    const result = await authStore.login({
      username: formData.value.username,
      password: formData.value.password,
    });

    if (result.success) {
      router.push("/");
    } else {
      error.value = typeof result.error === "string" ? result.error : JSON.stringify(result.error);
    }
  } else {
    if (formData.value.password !== formData.value.password2) {
      error.value = "Passwords don't match";
      return;
    }

    const result = await authStore.register(formData.value);

    if (result.success) {
      router.push("/");
    } else {
      error.value = typeof result.error === "string" ? result.error : JSON.stringify(result.error);
    }
  }
}
</script>

<style scoped>
.auth-form {
  max-width: 420px;
  margin: 0 auto;
}

.auth-form h2 {
  color: #1a1f36;
  font-size: 1.75rem;
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.form-group {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #1a1f36;
  font-size: 0.875rem;
}

input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e6ebf1;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  background: #f7f9fc;
}

input:focus {
  outline: none;
  border-color: #5469d4;
  background: white;
  box-shadow: 0 0 0 3px rgba(84, 105, 212, 0.1);
}

.btn-primary {
  width: 100%;
  padding: 0.875rem;
  background: #5469d4;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  margin-top: 1rem;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: #4558c9;
  box-shadow: 0 2px 8px rgba(84, 105, 212, 0.3);
}

.btn-primary:active {
  transform: scale(0.98);
}

.btn-link {
  background: none;
  border: none;
  color: #5469d4;
  cursor: pointer;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s ease;
}

.btn-link:hover {
  color: #4558c9;
  text-decoration: underline;
}

.toggle-auth {
  margin-top: 1.5rem;
  text-align: center;
  color: #697386;
  font-size: 0.9rem;
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
