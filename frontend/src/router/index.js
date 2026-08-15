import Vue from "vue";
import VueRouter from "vue-router";

import store from "@/store";

Vue.use(VueRouter);

const routes = [
  { path: "/", name: "home", component: () => import("@/views/Home.vue") },
  { path: "/products", name: "product-list", component: () => import("@/views/ProductList.vue") },
  { path: "/products/:slug", name: "product-detail", component: () => import("@/views/ProductDetail.vue") },
  { path: "/cart", name: "cart", component: () => import("@/views/Cart.vue") },
  { path: "/contact", name: "contact", component: () => import("@/views/Contact.vue") },
  { path: "/stores", name: "store-list", component: () => import("@/views/VendorStoreList.vue") },
  { path: "/store/:slug", name: "vendor-store", component: () => import("@/views/VendorStore.vue") },
  {
    path: "/checkout",
    name: "checkout",
    component: () => import("@/views/Checkout.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/order-success/:id",
    name: "order-success",
    component: () => import("@/views/OrderSuccess.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/payment/:orderId",
    name: "payment-select",
    component: () => import("@/views/PaymentSelect.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/payment-result",
    name: "payment-result",
    component: () => import("@/views/PaymentResult.vue"),
  },
  {
    path: "/my-orders",
    name: "my-orders",
    component: () => import("@/views/MyOrders.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/Login.vue"),
    meta: { guestOnly: true },
  },
  {
    path: "/register",
    name: "register",
    component: () => import("@/views/Register.vue"),
    meta: { guestOnly: true },
  },
  {
    path: "/forgot-password",
    name: "forgot-password",
    component: () => import("@/views/ForgotPassword.vue"),
    meta: { guestOnly: true },
  },
  {
    path: "/reset-password/:uid/:token",
    name: "reset-password",
    component: () => import("@/views/ResetPassword.vue"),
    meta: { guestOnly: true },
  },
  {
    path: "/become-vendor",
    name: "become-vendor",
    component: () => import("@/views/BecomeVendor.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/admin",
    component: () => import("@/views/admin/AdminLayout.vue"),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      { path: "", redirect: { name: "admin-dashboard" } },
      { path: "dashboard", name: "admin-dashboard", component: () => import("@/views/admin/AdminDashboard.vue") },
      { path: "products", name: "admin-products", component: () => import("@/views/admin/AdminProducts.vue") },
      { path: "categories", name: "admin-categories", component: () => import("@/views/admin/AdminCategories.vue") },
      { path: "hero-slides", name: "admin-hero-slides", component: () => import("@/views/admin/AdminHeroSlides.vue") },
      {
        path: "products/new",
        name: "admin-product-new",
        component: () => import("@/views/admin/AdminProductForm.vue"),
      },
      {
        path: "products/:slug/edit",
        name: "admin-product-edit",
        component: () => import("@/views/admin/AdminProductForm.vue"),
      },
      { path: "orders", name: "admin-orders", component: () => import("@/views/admin/AdminOrders.vue") },
      { path: "users", name: "admin-users", component: () => import("@/views/admin/AdminUsers.vue") },
      { path: "vendors", name: "admin-vendors", component: () => import("@/views/admin/AdminVendors.vue") },
      { path: "settings", name: "admin-settings", component: () => import("@/views/admin/AdminSettings.vue") },
      { path: "payments", name: "admin-payments", component: () => import("@/views/admin/AdminPayments.vue") },
      {
        path: "payment-settings",
        name: "admin-payment-settings",
        component: () => import("@/views/admin/AdminPaymentSettings.vue"),
      },
      {
        path: "social-auth-settings",
        name: "admin-social-auth-settings",
        component: () => import("@/views/admin/AdminSocialAuthSettings.vue"),
      },
      { path: "roles", name: "admin-roles", component: () => import("@/views/admin/AdminRoles.vue") },
      { path: "inventory", name: "admin-inventory", component: () => import("@/views/admin/AdminInventory.vue") },
      { path: "accounting", name: "admin-accounting", component: () => import("@/views/admin/AdminAccounting.vue") },
    ],
  },
  {
    path: "/vendor",
    component: () => import("@/views/vendor/VendorLayout.vue"),
    meta: { requiresAuth: true, requiresVendor: true },
    children: [
      { path: "", redirect: { name: "vendor-dashboard" } },
      { path: "dashboard", name: "vendor-dashboard", component: () => import("@/views/vendor/VendorDashboard.vue") },
      { path: "products", name: "vendor-products", component: () => import("@/views/vendor/VendorProducts.vue") },
      {
        path: "products/new",
        name: "vendor-product-new",
        component: () => import("@/views/vendor/VendorProductForm.vue"),
      },
      {
        path: "products/:slug/edit",
        name: "vendor-product-edit",
        component: () => import("@/views/vendor/VendorProductForm.vue"),
      },
      { path: "profile", name: "vendor-profile", component: () => import("@/views/vendor/VendorProfile.vue") },
    ],
  },
  { path: "*", name: "not-found", component: () => import("@/views/NotFound.vue") },
];

const router = new VueRouter({
  mode: "history",
  routes,
  scrollBehavior() {
    return { x: 0, y: 0 };
  },
});

router.beforeEach(async (to, from, next) => {
  const isAuthenticated = store.getters["auth/isAuthenticated"];
  const isAdmin = store.getters["auth/isAdmin"];

  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: "login", query: { redirect: to.fullPath } });
  }
  if (to.meta.requiresAdmin && !isAdmin) {
    return next({ name: "home" });
  }
  if (to.meta.guestOnly && isAuthenticated) {
    return next({ name: "home" });
  }
  if (to.meta.requiresVendor) {
    if (!store.state.vendor.checked) {
      await store.dispatch("vendor/fetchMe");
    }
    if (!store.getters["vendor/isApprovedVendor"]) {
      return next({ name: "become-vendor" });
    }
  }
  next();
});

export default router;