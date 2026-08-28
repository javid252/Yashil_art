<template>
  <header class="site-header">
    <!-- Top Bar -->
    <div class="top-bar">
      <div class="container top-bar-inner">
        <div class="top-right">
          <span>🚚 ارسال رایگان</span>
          <span>🎧 پشتیبانی</span>
          <span>☎ ۰۲۱-۹۱۰۰۰۰۰۰</span>
        </div>
        <div class="top-left">
          <router-link v-if="multivendorEnabled && !isVendor" to="/become-vendor">فروشنده شوید</router-link>
          <router-link v-else-if="isVendor && !isApprovedVendor" to="/become-vendor">وضعیت درخواست فروشندگی</router-link>
        </div>
      </div>
    </div>

    <!-- Main Header -->
    <div class="main-header">
      <div class="container header-inner">
        <!-- Logo -->
        <router-link to="/" class="brand">
          <span class="brand-icon">🎨</span>
          <span class="brand-name">یاشیل آرت</span>
        </router-link>

        <!-- Search -->
        <form class="search-box" @submit.prevent="submitSearch">
          <input v-model="searchQuery" type="text" placeholder="جستجو در محصولات..." />
          <button type="submit" aria-label="جستجو">🔍</button>
        </form>

        <!-- Actions -->
        <div class="header-actions">
          <!-- Cart -->
          <router-link to="/cart" class="header-action">
            <span class="header-action__icon">🛒</span>
            <span class="header-action__label">سبد خرید</span>
            <b v-if="itemCount" class="header-action__badge">{{ itemCount }}</b>
          </router-link>

          <!-- User -->
          <div v-if="isAuthenticated" class="user-box" @mouseleave="menuOpen = false">
            <button class="user-box__btn" @click="menuOpen = !menuOpen">
              <span class="user-box__icon">👤</span>
              <span class="user-box__name">{{ userLabel }}</span>
            </button>

            <transition name="dropdown">
              <div v-if="menuOpen" class="user-dropdown" @click="menuOpen = false">
                <router-link to="/my-orders">📋 سفارش‌های من</router-link>
                <router-link to="/my-invoices">🧾 فاکتورهای من</router-link>
                <router-link v-if="isApprovedVendor" to="/vendor">🏪 پنل فروشنده</router-link>
                <router-link v-if="isAdmin" to="/admin">⚙️ پنل ادمین</router-link>
                <button class="logout-btn" @click="logout">🚪 خروج</button>
              </div>
            </transition>
          </div>

          <router-link v-else to="/login" class="login-btn">
            <span class="login-btn__icon">👤</span>
            <span class="login-btn__text">ورود / ثبت‌نام</span>
          </router-link>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "AppHeader",
  data() {
    return {
      menuOpen: false,
      searchQuery: "",
    };
  },
  computed: {
    ...mapGetters("auth", ["isAuthenticated", "isAdmin", "currentUser"]),
    ...mapGetters("cart", ["itemCount"]),
    ...mapGetters("platform", ["multivendorEnabled"]),
    ...mapGetters("vendor", ["isVendor", "isApprovedVendor"]),
    userLabel() {
      return this.currentUser ? this.currentUser.first_name || this.currentUser.username : "";
    },
  },
  methods: {
    submitSearch() {
      const query = this.searchQuery.trim();
      if (!query) return;
      this.$router.push({ path: "/products", query: { search: query } });
    },
    logout() {
      this.$store.dispatch("auth/logout");
      this.$store.dispatch("notify", { message: "با موفقیت خارج شدید." });
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.site-header {
  background: var(--color-surface);
  position: sticky;
  top: 0;
  z-index: 50;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

/* TOP BAR */
.top-bar {
  background: var(--color-primary-dark);
  color: #fff;
  font-size: 0.82rem;
}
.top-bar-inner {
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.top-right,
.top-left {
  display: flex;
  align-items: center;
  gap: 22px;
}
.top-bar a {
  color: #fff;
  font-weight: 600;
}

/* MAIN HEADER */
.main-header {
  border-bottom: 1px solid var(--color-border);
}
.header-inner {
  height: 78px;
  display: flex;
  align-items: center;
  gap: 18px;
}

/* BRAND */
.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.35rem;
  font-weight: 900;
  color: var(--color-primary);
  flex-shrink: 0;
}
.brand-icon {
  font-size: 1.8rem;
}

/* SEARCH */
.search-box {
  flex: 1;
  display: flex;
  height: 46px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius);
  overflow: hidden;
  transition: border-color 0.2s;
}
.search-box:focus-within {
  border-color: var(--color-primary);
}
.search-box input {
  flex: 1;
  border: none;
  padding: 0 18px;
  font-family: inherit;
  font-size: 0.9rem;
  background: transparent;
}
.search-box input:focus {
  outline: none;
}
.search-box button {
  width: 55px;
  border: none;
  background: var(--color-primary);
  color: #fff;
  cursor: pointer;
  font-size: 1.1rem;
  transition: background 0.2s;
}
.search-box button:hover {
  background: var(--color-primary-light);
}

/* ACTIONS */
.header-actions {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-shrink: 0;
}

.header-action {
  position: relative;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  font-weight: 700;
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  transition: background 0.2s;
}
.header-action:hover {
  background: var(--color-bg);
}
.header-action__icon {
  font-size: 1.2rem;
}
.header-action__badge {
  position: absolute;
  top: 2px;
  right: 2px;
  background: var(--color-accent);
  border-radius: 50%;
  font-size: 0.65rem;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1a1a2e;
}

.login-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--color-primary);
  color: #fff;
  padding: 10px 18px;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  font-weight: 700;
  transition: background 0.2s;
}
.login-btn:hover {
  background: var(--color-primary-light);
}

/* USER BOX */
.user-box {
  position: relative;
}
.user-box__btn {
  display: flex;
  align-items: center;
  gap: 6px;
  border: none;
  background: var(--color-sand);
  padding: 10px 16px;
  border-radius: 24px;
  font-family: inherit;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.user-box__btn:hover {
  background: var(--color-border);
}

/* DROPDOWN */
.user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: white;
  border: 1px solid var(--color-border);
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.12);
  border-radius: var(--radius);
  width: 200px;
  padding: 8px;
  display: flex;
  flex-direction: column;
  z-index: 60;
}
.user-dropdown a,
.user-dropdown button {
  padding: 10px 14px;
  border: none;
  background: none;
  text-align: right;
  font-family: inherit;
  font-size: 0.86rem;
  border-radius: var(--radius-sm);
  transition: background 0.15s;
}
.user-dropdown a:hover,
.user-dropdown button:hover {
  background: var(--color-bg);
}
.logout-btn {
  color: var(--color-danger) !important;
  border-top: 1px solid var(--color-border);
  margin-top: 4px;
  padding-top: 12px !important;
}

/* DROPDOWN ANIMATION */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}
.dropdown-enter,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* ========== ریسپانسیو ========== */
@media (max-width: 900px) {
  .top-bar {
    display: none;
  }
  .header-inner {
    height: auto;
    padding: 12px 0;
    flex-wrap: wrap;
    gap: 10px;
  }
  .brand-name {
    display: none;
  }
  .search-box {
    order: 3;
    width: 100%;
    height: 42px;
  }
  .search-box button {
    width: 48px;
  }
  .header-action__label {
    display: none;
  }
  .user-box__name {
    display: none;
  }
  .login-btn__text {
    display: none;
  }
}

@media (max-width: 480px) {
  .header-inner {
    padding: 10px 0;
  }
  .header-actions {
    gap: 6px;
  }
  .header-action {
    padding: 8px;
  }
  .user-box__btn {
    padding: 8px 12px;
  }
  .login-btn {
    padding: 8px 14px;
  }
}
</style>