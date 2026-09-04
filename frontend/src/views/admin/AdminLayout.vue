<template>
  <div class="admin-shell" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
    <!-- Sidebar -->
    <aside class="admin-sidebar">
      <!-- Brand -->
      <div class="sidebar-brand">
        <div class="brand-icon">🎨</div>
        <div class="brand-text" v-show="!sidebarCollapsed">
          <span class="brand-name">یاشیل آرت</span>
          <span class="brand-badge">پنل مدیریت</span>
        </div>
        <button class="collapse-toggle" @click="sidebarCollapsed = !sidebarCollapsed">
          <span v-if="sidebarCollapsed">☰</span>
          <span v-else>✕</span>
        </button>
      </div>

      <!-- Navigation Groups -->
      <nav class="admin-nav">
        <!-- Dashboard (همیشه برای کاربران پنل مدیریت) -->
        <router-link to="/admin/dashboard" class="nav-single">
          <span class="nav-icon">📊</span>
          <span class="nav-label">داشبورد</span>
        </router-link>

        <!-- گروه‌ها فقط با آیتم‌هایی که کاربر به آن‌ها دسترسی دارد نمایش داده می‌شوند -->
        <template v-for="group in visibleGroups">
          <div :key="group.key" class="nav-group" :class="{ open: openGroups[group.key] }">
            <button class="nav-group-header" @click="toggleGroup(group.key)">
              <span class="nav-icon">{{ group.icon }}</span>
              <span class="nav-label">{{ group.label }}</span>
              <span class="nav-chevron">{{ openGroups[group.key] ? '▾' : '◂' }}</span>
            </button>
            <div class="nav-group-items" v-show="openGroups[group.key]">
              <router-link
                v-for="item in group.visibleItems"
                :key="item.label"
                :to="{ name: item.routeNames[0] }"
              >
                {{ item.label }}
              </router-link>
            </div>
          </div>
        </template>
      </nav>

      <!-- Bottom Link -->
      <router-link to="/" class="nav-back">
        <span class="nav-icon">←</span>
        <span class="nav-label" v-show="!sidebarCollapsed">بازگشت به سایت</span>
      </router-link>
    </aside>

    <!-- Main Content -->
    <div class="admin-main">
      <!-- Topbar -->
      <header class="admin-topbar">
        <div class="topbar-right">
          <h2 class="topbar-title">{{ pageTitle }}</h2>
        </div>
        <div class="topbar-left">
          <div class="user-info">
            <div class="user-avatar">{{ userInitial }}</div>
            <div class="user-meta" v-show="!sidebarCollapsed">
              <span class="user-name">{{ userLabel }}</span>
              <span class="user-role">{{ roleBadge }}</span>
            </div>
          </div>
          <button class="btn-logout" @click="logout">
            <span>خروج</span>
          </button>
        </div>
      </header>

      <!-- Page Content -->
      <div class="admin-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

// ── تعریف گروه‌ها و آیتم‌های منوی پنل مدیریت + شرط نمایش هر آیتم ──
// هر کاربر فقط آیتم‌هایی را می‌بیند که به نقشش مرتبط است:
//   perms     -> پرمیشن‌های ماژول (نقش‌های فروشگاه/بک‌آفیس)
//   roles     -> عضویت در نقش مشخص (نقش‌های آموزشگاه مثل مدیر آموزشگاه)
//   superuser -> فقط ادمین ارشد
const NAV_GROUPS = [
  {
    key: "shop",
    icon: "🏪",
    label: "فروشگاه",
    items: [
      { label: "محصولات", routeNames: ["admin-products", "admin-product-new", "admin-product-edit"], perms: ["products.view_product"] },
      { label: "دسته‌بندی‌ها", routeNames: ["admin-categories"], perms: ["products.view_category"] },
      { label: "اسلایدر صفحه اصلی", routeNames: ["admin-hero-slides"], perms: ["content.view_heroslide"] },
      { label: "انبارداری", routeNames: ["admin-inventory"], perms: ["inventory.view_stockmovement", "inventory.view_warehouse"] },
    ],
  },
  {
    key: "finance",
    icon: "💰",
    label: "سفارشات و مالی",
    items: [
      { label: "سفارش‌ها", routeNames: ["admin-orders"], perms: ["orders.view_order"] },
      { label: "فاکتورها", routeNames: ["admin-invoices"], perms: ["invoices.view_invoice"] },
      { label: "پرداخت‌ها", routeNames: ["admin-payments"], perms: ["payments.view_payment"] },
      { label: "حسابداری", routeNames: ["admin-accounting"], perms: ["accounting.view_transaction"] },
    ],
  },
  {
    key: "academy",
    icon: "🎓",
    label: "آموزشگاه",
    items: [
      { label: "دوره‌ها", routeNames: ["admin-courses"], roles: ["مدیر آموزشگاه", "مدیرکل"] },
      { label: "اساتید", routeNames: ["admin-instructors"], roles: ["مدیر آموزشگاه", "مدیرکل"] },
      { label: "گالری", routeNames: ["admin-gallery"], roles: ["مدیر آموزشگاه", "مدیرکل"] },
      { label: "کارگاه‌ها", routeNames: ["admin-workshops"], roles: ["مدیر آموزشگاه", "مدیرکل"] },
    ],
  },
  {
    key: "users",
    icon: "👥",
    label: "کاربران",
    items: [
      { label: "همه کاربران", routeNames: ["admin-users"], superuser: true },
      { label: "فروشندگان", routeNames: ["admin-vendors"], superuser: true },
    ],
  },
  {
    key: "settings",
    icon: "⚙️",
    label: "تنظیمات",
    items: [
      { label: "تنظیمات عمومی", routeNames: ["admin-settings"], superuser: true },
      { label: "تنظیمات پرداخت", routeNames: ["admin-payment-settings"], superuser: true },
      { label: "ورود اجتماعی", routeNames: ["admin-social-auth-settings"], superuser: true },
      { label: "نقش‌ها و دسترسی‌ها", routeNames: ["admin-roles"], superuser: true },
    ],
  },
];

const PAGE_TITLES = {
  "admin-dashboard": "داشبورد مدیریت",
  "admin-products": "مدیریت محصولات",
  "admin-product-new": "محصول جدید",
  "admin-product-edit": "ویرایش محصول",
  "admin-categories": "دسته‌بندی‌ها",
  "admin-hero-slides": "اسلایدر صفحه اصلی",
  "admin-orders": "مدیریت سفارش‌ها",
  "admin-users": "مدیریت کاربران",
  "admin-vendors": "فروشندگان",
  "admin-inventory": "انبارداری",
  "admin-accounting": "حسابداری",
  "admin-invoices": "فاکتورها",
  "admin-payments": "پرداخت‌ها",
  "admin-courses": "مدیریت دوره‌ها",
  "admin-course-new": "دوره جدید",
  "admin-course-edit": "ویرایش دوره",
  "admin-instructors": "مدیریت اساتید",
  "admin-instructor-new": "استاد جدید",
  "admin-instructor-edit": "ویرایش استاد",
  "admin-gallery": "مدیریت گالری",
  "admin-artwork-new": "اثر هنری جدید",
  "admin-artwork-edit": "ویرایش اثر هنری",
  "admin-workshops": "مدیریت کارگاه‌ها",
  "admin-workshop-new": "کارگاه جدید",
  "admin-workshop-edit": "ویرایش کارگاه",
  "admin-settings": "تنظیمات",
  "admin-payment-settings": "تنظیمات پرداخت",
  "admin-social-auth-settings": "ورود اجتماعی",
  "admin-roles": "نقش‌ها و دسترسی‌ها",
};

export default {
  name: "AdminLayout",
  data() {
    return {
      sidebarCollapsed: false,
      openGroups: {
        shop: false,
        finance: false,
        academy: false,
        users: false,
        settings: false,
      },
    };
  },
  computed: {
    ...mapGetters("auth", ["isSuperUser", "isAcademyManager"]),
    permissions() {
      return this.$store.getters["auth/permissions"];
    },
    roleNames() {
      return this.$store.getters["auth/roleNames"];
    },
    // فقط گروه‌هایی که حداقل یک آیتم قابل‌مشاهده دارند
    visibleGroups() {
      return NAV_GROUPS.map((group) => ({
        ...group,
        visibleItems: group.items.filter((item) => this.canShow(item)),
      })).filter((group) => group.visibleItems.length > 0);
    },
    userLabel() {
      const u = this.$store.getters["auth/currentUser"];
      return u ? u.first_name || u.username : "";
    },
    userInitial() {
      return this.userLabel ? this.userLabel.charAt(0) : "A";
    },
    roleBadge() {
      if (this.isSuperUser) return "مدیر ارشد";
      if (this.isAcademyManager) return "مدیر آموزشگاه";
      if (this.roleNames.length) return this.roleNames.join("، ");
      return "کاربر پنل مدیریت";
    },
    pageTitle() {
      return PAGE_TITLES[this.$route.name] || "پنل مدیریت";
    },
  },
  watch: {
    "$route.name"() {
      // باز کردن خودکار گروه حاوی مسیر فعال
      this.autoOpenGroup();
    },
    visibleGroups() {
      this.autoOpenGroup();
    },
  },
  methods: {
    canShow(item) {
      if (this.isSuperUser) return true;
      if (item.superuser) return false;
      if (item.roles) return item.roles.some((r) => this.roleNames.includes(r));
      if (item.perms) return item.perms.some((p) => this.permissions.includes(p));
      return true;
    },
    toggleGroup(name) {
      this.openGroups[name] = !this.openGroups[name];
    },
    autoOpenGroup() {
      const route = this.$route.name;
      const group = this.visibleGroups.find((g) =>
        g.visibleItems.some((item) => item.routeNames.includes(route))
      );
      if (group) {
        this.openGroups[group.key] = true;
      } else if (route === "admin-dashboard" && this.visibleGroups.length) {
        // در داشبورد، اولین گروهِ در دسترس باز باشد
        this.openGroups[this.visibleGroups[0].key] = true;
      }
    },
    logout() {
      this.$store.dispatch("auth/logout");
      this.$router.push("/");
    },
  },
  mounted() {
    this.autoOpenGroup();
  },
};
</script>

<style scoped>
/* ==========================================
   ADMIN SHELL
   ========================================== */
.admin-shell {
  display: flex;
  min-height: 100vh;
  background: #f0f2f5;
  font-family: var(--font-main);
}

/* ==========================================
   SIDEBAR
   ========================================== */
.admin-sidebar {
  width: 270px;
  background: linear-gradient(180deg, #0f1a14 0%, #142419 40%, #1a2f20 100%);
  color: #fff;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  transition: width 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  position: relative;
  z-index: 100;
}
.sidebar-collapsed .admin-sidebar {
  width: 68px;
}

/* Brand */
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 18px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
  margin-bottom: 8px;
}
.brand-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #c9a96e, #e3a857);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  flex-shrink: 0;
}
.brand-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.brand-name {
  font-size: 1rem;
  font-weight: 800;
  color: #fff;
  white-space: nowrap;
}
.brand-badge {
  font-size: 0.65rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.45);
  letter-spacing: 0.03em;
}
.collapse-toggle {
  margin-right: auto;
  background: rgba(255, 255, 255, 0.06);
  border: none;
  color: rgba(255, 255, 255, 0.5);
  width: 28px;
  height: 28px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  cursor: pointer;
  transition: background 0.15s;
}
.collapse-toggle:hover {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
}
.sidebar-collapsed .brand-text,
.sidebar-collapsed .collapse-toggle {
  display: none;
}

/* Navigation */
.admin-nav {
  flex: 1;
  padding: 6px 10px;
  overflow-y: auto;
  overflow-x: hidden;
}
.admin-nav::-webkit-scrollbar {
  width: 3px;
}
.admin-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 3px;
}

/* Single Link (Dashboard) */
.nav-single {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 0.88rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 4px;
  transition: all 0.15s;
}
.nav-single:hover {
  background: rgba(255, 255, 255, 0.07);
  color: #fff;
}
.nav-single.router-link-active {
  background: linear-gradient(135deg, #c9a96e, #d4b87a);
  color: #1a2f20;
  font-weight: 700;
  box-shadow: 0 2px 12px rgba(201, 169, 110, 0.3);
}

/* Group */
.nav-group {
  margin-bottom: 2px;
}
.nav-group-header {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 14px;
  border: none;
  background: none;
  border-radius: 8px;
  font-family: inherit;
  font-size: 0.88rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.15s;
  text-align: right;
}
.nav-group-header:hover {
  background: rgba(255, 255, 255, 0.07);
  color: #fff;
}
.nav-icon {
  width: 20px;
  text-align: center;
  flex-shrink: 0;
  font-size: 0.95rem;
}
.nav-label {
  flex: 1;
  white-space: nowrap;
}
.nav-chevron {
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.3);
  transition: transform 0.2s;
}
.nav-group.open .nav-chevron {
  transform: rotate(0deg);
}

/* Group Items */
.nav-group-items {
  display: flex;
  flex-direction: column;
  padding: 2px 0 6px;
}
.nav-group-items a {
  display: block;
  padding: 8px 14px 8px 14px;
  margin: 1px 0;
  margin-right: 44px;
  border-radius: 6px;
  font-size: 0.82rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.5);
  transition: all 0.15s;
  white-space: nowrap;
  position: relative;
}
.nav-group-items a::before {
  content: "";
  position: absolute;
  right: -10px;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  transition: all 0.15s;
}
.nav-group-items a:hover {
  color: rgba(255, 255, 255, 0.9);
  background: rgba(255, 255, 255, 0.05);
}
.nav-group-items a:hover::before {
  background: rgba(255, 255, 255, 0.5);
}
.nav-group-items a.router-link-exact-active,
.nav-group-items a.router-link-active {
  color: #fff;
  background: rgba(201, 169, 110, 0.15);
  font-weight: 700;
}
.nav-group-items a.router-link-exact-active::before,
.nav-group-items a.router-link-active::before {
  background: #c9a96e;
  width: 4px;
  height: 4px;
}

/* Collapsed Sidebar Styles */
.sidebar-collapsed .nav-single,
.sidebar-collapsed .nav-group-header {
  justify-content: center;
  padding: 10px;
}
.sidebar-collapsed .nav-label,
.sidebar-collapsed .nav-chevron {
  display: none;
}
.sidebar-collapsed .nav-group-items a {
  margin-right: 0;
  padding: 8px;
  text-align: center;
  font-size: 0;
}
.sidebar-collapsed .nav-group-items a::before {
  right: 50%;
  transform: translateX(-50%);
}

/* Back Link */
.nav-back {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  border-top: 1px solid rgba(255, 255, 255, 0.07);
  font-size: 0.82rem;
  color: rgba(255, 255, 255, 0.4);
  transition: color 0.15s;
}
.nav-back:hover {
  color: rgba(255, 255, 255, 0.8);
}
.sidebar-collapsed .nav-back {
  justify-content: center;
}

/* ==========================================
   MAIN CONTENT
   ========================================== */
.admin-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

/* Topbar */
.admin-topbar {
  height: 64px;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  flex-shrink: 0;
}
.topbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.topbar-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #1f2937;
}
.topbar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}
.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, #1f4b43, #2e6b5e);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
}
.user-meta {
  display: flex;
  flex-direction: column;
}
.user-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.2;
}
.user-role {
  font-size: 0.7rem;
  color: #9ca3af;
}
.btn-logout {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fff;
  color: #6b7280;
  font-size: 0.8rem;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-logout:hover {
  border-color: #dc2626;
  color: #dc2626;
  background: #fef2f2;
}

/* Content */
.admin-content {
  flex: 1;
  padding: 28px;
  overflow-x: auto;
}
</style>
