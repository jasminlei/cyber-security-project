import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";
import ItemsList from "../components/ItemsList.vue";
import ItemDetail from "../components/ItemDetail.vue";
import AuthForm from "../components/AuthForm.vue";
import MyItems from "../components/MyItems.vue";
import ItemForm from "../components/ItemForm.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: ItemsList,
    },
    {
      path: "/auth",
      name: "auth",
      component: AuthForm,
    },
    {
      path: "/items/:id",
      name: "item-detail",
      component: ItemDetail,
    },
    {
      path: "/my-items",
      name: "my-items",
      component: MyItems,
      meta: { requiresAuth: true },
    },
    {
      path: "/create-item",
      name: "create-item",
      component: ItemForm,
      meta: { requiresAuth: true },
    },
    {
      path: "/edit-item/:id",
      name: "edit-item",
      component: ItemForm,
      meta: { requiresAuth: true },
    },
  ],
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next("/auth");
  } else if (to.path === "/auth" && authStore.isAuthenticated) {
    next("/");
  } else {
    next();
  }
});

export default router;
