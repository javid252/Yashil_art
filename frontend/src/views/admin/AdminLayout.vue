<template>
  <div class="admin-shell">
    <aside class="admin-sidebar">
      <router-link to="/" class="admin-brand">🎨 یاشیل آرت <span>ادمین</span></router-link>
      <nav class="admin-nav">
        <router-link to="/admin/dashboard">📊 داشبورد</router-link>
        <router-link to="/admin/products">📦 محصولات</router-link>
        <router-link to="/admin/categories">🗂️ دسته‌بندی‌ها</router-link>
        <router-link to="/admin/orders">🧾 سفارش‌ها</router-link>
        <router-link to="/admin/users">👥 کاربران</router-link>
        <router-link v-if="multivendorEnabled" to="/admin/vendors">🏪 فروشندگان</router-link>
        <router-link to="/admin/inventory">📊 انبارداری</router-link>
        <router-link to="/admin/accounting">💰 حسابداری</router-link>
        <router-link to="/admin/payments">🧾 پرداخت‌ها</router-link>
        <router-link v-if="isSuperUser" to="/admin/payment-settings">💳 تنظیمات پرداخت</router-link>
        <router-link v-if="isSuperUser" to="/admin/social-auth-settings">🔐 ورود اجتماعی</router-link>
        <router-link v-if="isSuperUser" to="/admin/roles">🛡️ نقش‌ها و دسترسی‌ها</router-link>
        <router-link to="/admin/settings">⚙️ تنظیمات</router-link>
      </nav>
      <router-link to="/" class="admin-back">← بازگشت به فروشگاه</router-link>
    </aside>

    <div class="admin-main">
      <header class="admin-topbar">
        <span class="text-muted">خوش آمدید، {{ userLabel }}</span>
        <button class="btn btn-outline btn-sm" @click="logout">خروج</button>
      </header>
      <div class="admin-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "AdminLayout",
  computed: {
    ...mapGetters("platform", ["multivendorEnabled"]),
    ...mapGetters("auth", ["isSuperUser"]),
    userLabel() {
      const u = this.$store.getters["auth/currentUser"];
      return u ? u.first_name || u.username : "";
    },
  },
  methods: {
    logout() {
      this.$store.dispatch("auth/logout");
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.admin-shell {
  display: flex;
  min-height: 100vh;
  background: var(--color-bg);
  font-family: var(--font-main);
}
.admin-sidebar {
  width: 230px;
  background: var(--color-primary-dark);
  color: #fff;
  display: flex;
  flex-direction: column;
  padding: 22px 16px;
  flex-shrink: 0;
}
.admin-brand {
  font-weight: 900;
  font-size: 1.05rem;
  color: #fff;
  margin-bottom: 30px;
  padding: 0 8px;
}
.admin-brand span {
  color: var(--color-accent);
  font-size: 0.75rem;
  font-weight: 600;
  margin-right: 6px;
}
.admin-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}
.admin-nav a {
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  font-size: 0.88rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.75);
}
.admin-nav a:hover {
  background: rgba(255, 255, 255, 0.06);
  color: #fff;
}
.admin-nav a.router-link-active {
  background: var(--color-accent);
  color: var(--color-primary-dark);
}
.admin-back {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  padding: 10px 12px;
}
.admin-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.admin-topbar {
  height: 60px;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 26px;
  font-size: 0.88rem;
}
.admin-content {
  flex: 1;
  padding: 26px;
  overflow-x: auto;
}
</style>