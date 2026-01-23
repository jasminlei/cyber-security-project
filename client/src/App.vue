<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import { onMounted } from "vue";
import { useAuthStore } from "./stores/auth";

const authStore = useAuthStore();

onMounted(() => {
  if (authStore.isAuthenticated) {
    authStore.fetchCurrentUser();
  }
});

function handleLogout() {
  authStore.logout();
}
</script>

<template>
  <div id="app">
    <header>
      <h1 class="site-title">Secondhand Marketplace</h1>

      <nav>
        <template v-if="authStore.isAuthenticated">
          <RouterLink to="/">Browse</RouterLink>
          <RouterLink to="/my-items">My Items</RouterLink>
          <RouterLink to="/create-item">Sell</RouterLink>
          <span class="user-info">{{ authStore.user?.username }}</span>
          <button @click="handleLogout" class="btn-logout">Logout</button>
        </template>

        <template v-else>
          <RouterLink to="/">Browse</RouterLink>
          <RouterLink to="/auth" class="btn-login">Login</RouterLink>
        </template>
      </nav>
    </header>

    <main>
      <div class="content-wrapper">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family:
    "Inter",
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    Roboto,
    sans-serif;
  color: #1a1f36;
  background: #f7f9fc;
  min-height: 100vh;
  margin: 0;
  padding: 0;
}

h2,
h3,
h4,
h5,
h6 {
  font-family: "Space Grotesk", sans-serif;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  width: 100vw;
}

header {
  background-color: #ffffff;
  border-bottom: 1px solid #e6ebf1;
  padding: 1.5rem 2.5rem 1rem 2.5rem;
  width: 100vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  position: relative;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
}

.site-title {
  font-family: "Pacifico", cursive;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 2rem;
  font-weight: 400;
  margin: 0;
  letter-spacing: 0.5px;
  text-align: center;
}

nav {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  justify-content: center;
}

nav a {
  text-decoration: none;
  color: #697386;
  font-weight: 500;
  padding: 0.625rem 1rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

nav a:hover {
  background-color: #f6f8fa;
  color: #1a1f36;
}

nav a.router-link-exact-active {
  background-color: #5469d4;
  color: white;
}

.btn-login {
  background-color: #5469d4;
  color: white !important;
}

.btn-login:hover {
  background-color: #4558c9;
  color: white !important;
}

.user-info {
  color: #697386;
  font-size: 0.875rem;
  padding: 0 0.75rem;
  font-weight: 500;
}

.btn-logout {
  padding: 0.625rem 1rem;
  background-color: #fff;
  color: #697386;
  border: 1px solid #e6ebf1;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-logout:hover {
  background-color: #f6f8fa;
  color: #1a1f36;
}
main {
  flex: 1;
  padding: 2.5rem;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  background: #f7f9fc;
}

.content-wrapper {
  background-color: white;
  border-radius: 12px;
  border: 1px solid #e6ebf1;
  padding: 2.5rem;
  width: 1400px;
  max-width: 95vw;
  min-height: 500px;
  box-shadow:
    0 1px 3px rgba(50, 50, 93, 0.04),
    0 1px 0 rgba(0, 0, 0, 0.02);
}

@media (max-width: 768px) {
  header {
    padding: 1.25rem 1.5rem 0.75rem 1.5rem;
  }

  .site-title {
    font-size: 1.5rem;
  }

  nav {
    flex-wrap: wrap;
    justify-content: center;
  }

  main {
    padding: 1.5rem 1rem;
  }

  .content-wrapper {
    padding: 1.5rem;
    border-radius: 8px;
  }
}
</style>
