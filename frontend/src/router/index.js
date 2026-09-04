import Vue from "vue";
import VueRouter from "vue-router";

import store from "@/store";

Vue.use(VueRouter);

const routes = [
  { path: "/", name: "home", component: () => import("@/views/LandingPage.vue") },
  { path: "/shop", name: "shop", component: () => import("@/views/Home.vue") },
  { path: "/courses", name: "course-list", component: () => import("@/views/CourseList.vue") },
  { path: "/courses/:id/:slug", name: "course-detail", component: () => import("@/views/CourseDetail.vue") },
  { path: "/gallery", name: "gallery", component: () => import("@/views/Gallery.vue") },
  { path: "/workshops", name: "workshop-list", component: () => import("@/views/WorkshopList.vue") },
  {
    path: "/my-courses",
    name: "my-courses",
    component: () => import("@/views/StudentDashboard.vue"),
    meta: { requiresAuth: true },
  },
  { path: "/products", name: "product-list", component: () => import("@/views/ProductList.vue") },
  { path: "/products/:id/:slug", name: "product-detail", component: () => import("@/views/ProductDetail.vue") },
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
    path: "/my-invoices",
    name: "my-invoices",
    component: () => import("@/views/MyInvoices.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/my-invoices/:id",
    name: "my-invoice-detail",
    component: () => import("@/views/InvoiceDetail.vue"),
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
  // ======================== Student Panel ========================
  {
    path: "/student",
    component: () => import("@/views/student/StudentLayout.vue"),
    meta: { requiresAuth: true, requiresStudent: true },
    children: [
      { path: "", redirect: { name: "student-dashboard" } },
      { path: "dashboard", name: "student-dashboard", component: () => import("@/views/student/StudentDashboard.vue") },
      { path: "my-courses", name: "student-my-courses", component: () => import("@/views/student/StudentMyCourses.vue") },
      { path: "grades", name: "student-grades", component: () => import("@/views/student/StudentGrades.vue") },
      { path: "certificates", name: "student-certificates", component: () => import("@/views/student/StudentCertificates.vue") },
      { path: "gallery", name: "student-gallery", component: () => import("@/views/student/StudentGallery.vue") },
      { path: "workshops", name: "student-workshops", component: () => import("@/views/student/StudentWorkshops.vue") },
      { path: "profile", name: "student-profile", component: () => import("@/views/student/StudentProfile.vue") },
    ],
  },
  // ======================== Instructor Panel ========================
  {
    path: "/instructor",
    component: () => import("@/views/instructor/InstructorLayout.vue"),
    meta: { requiresAuth: true, requiresInstructor: true },
    children: [
      { path: "", redirect: { name: "instructor-dashboard" } },
      { path: "dashboard", name: "instructor-dashboard", component: () => import("@/views/instructor/InstructorDashboard.vue") },
      { path: "courses", name: "instructor-courses", component: () => import("@/views/instructor/InstructorCourses.vue") },
      { path: "students", name: "instructor-students", component: () => import("@/views/instructor/InstructorStudents.vue") },
      { path: "attendance", name: "instructor-attendance", component: () => import("@/views/instructor/InstructorAttendance.vue") },
      { path: "grades", name: "instructor-grades", component: () => import("@/views/instructor/InstructorGrades.vue") },
      { path: "gallery", name: "instructor-gallery", component: () => import("@/views/instructor/InstructorGallery.vue") },
      { path: "profile", name: "instructor-profile", component: () => import("@/views/instructor/InstructorProfile.vue") },
    ],
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
        path: "products/:id/edit",
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
      { path: "invoices", name: "admin-invoices", component: () => import("@/views/admin/AdminInvoices.vue") },
      { path: "courses", name: "admin-courses", component: () => import("@/views/admin/AdminCourses.vue") },
      {
        path: "courses/new",
        name: "admin-course-new",
        component: () => import("@/views/admin/AdminCourseForm.vue"),
      },
      {
        path: "courses/:id/edit",
        name: "admin-course-edit",
        component: () => import("@/views/admin/AdminCourseForm.vue"),
      },
      { path: "instructors", name: "admin-instructors", component: () => import("@/views/admin/AdminInstructors.vue") },
      {
        path: "instructors/new",
        name: "admin-instructor-new",
        component: () => import("@/views/admin/AdminInstructorForm.vue"),
      },
      {
        path: "instructors/:id/edit",
        name: "admin-instructor-edit",
        component: () => import("@/views/admin/AdminInstructorForm.vue"),
      },
      { path: "gallery-admin", name: "admin-gallery", component: () => import("@/views/admin/AdminGallery.vue") },
      {
        path: "gallery-admin/new",
        name: "admin-artwork-new",
        component: () => import("@/views/admin/AdminArtworkForm.vue"),
      },
      {
        path: "gallery-admin/:id/edit",
        name: "admin-artwork-edit",
        component: () => import("@/views/admin/AdminArtworkForm.vue"),
      },
      { path: "workshops-admin", name: "admin-workshops", component: () => import("@/views/admin/AdminWorkshops.vue") },
      {
        path: "workshops-admin/new",
        name: "admin-workshop-new",
        component: () => import("@/views/admin/AdminWorkshopForm.vue"),
      },
      {
        path: "workshops-admin/:id/edit",
        name: "admin-workshop-edit",
        component: () => import("@/views/admin/AdminWorkshopForm.vue"),
      },
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
        path: "products/:id/edit",
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

  // اولین بار در هر نشست، پروفایل از سرور تازه شود تا نقش‌ها/دسترسی‌های تازه
  // (که ممکن است مدیر در نشست قبلی تغییر داده باشد) در گارد مسیرها لحاظ شوند.
  if (isAuthenticated && !store.state.auth.profileChecked) {
    try {
      await store.dispatch("auth/fetchProfile");
    } catch (e) {
      // اگر توکن نامعتبر باشد، interceptor خودش کاربر را خارج می‌کند.
    }
  }

  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: "login", query: { redirect: to.fullPath } });
  }

  if (to.meta.guestOnly && isAuthenticated) {
    return next({ name: "home" });
  }

  if (to.meta.requiresAdmin && !store.getters["auth/isAdmin"]) {
    return next({ name: "home" });
  }

  // پنل هنرجو فقط برای کاربرِ دارای نقش «هنرآموز» (یا ابرمدیر برای پیش‌نمایش)
  if (to.meta.requiresStudent && !(store.getters["auth/isStudent"] || store.getters["auth/isSuperUser"])) {
    return next({ name: "my-courses" });
  }

  // پنل استاد فقط برای کاربرِ دارای نقش «استاد» (یا ابرمدیر برای پیش‌نمایش)
  if (to.meta.requiresInstructor && !(store.getters["auth/isInstructor"] || store.getters["auth/isSuperUser"])) {
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