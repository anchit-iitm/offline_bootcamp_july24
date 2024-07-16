import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import Example from "@/views/example.vue";
import AdminDash from "@/views/adminDash.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/example",
    name: 'example',
    component: Example,
  },
  {
    path: "/login",
    component: () => import("@/views/login.vue"),
  },
  {
    path: "/create_category",
    component: () => import("@/views/create_category.vue"),
  },
  {
    path: "/admindash",
    component: AdminDash,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
