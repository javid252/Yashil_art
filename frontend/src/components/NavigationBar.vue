<template>
  <nav class="navigation-bar">
    <div class="container nav-inner">
      <!-- All Categories -->
      <div class="category-dropdown" @mouseleave="categoriesOpen = false">
        <button class="all-category-btn" @click="categoriesOpen = !categoriesOpen">
          <span>☰</span>
          همه دسته‌بندی‌ها
        </button>
        <div v-if="categoriesOpen" class="category-dropdown__menu" @click="categoriesOpen = false">
          <router-link
            v-for="cat in categories"
            :key="cat.id"
            :to="`/products?category=${cat.slug}`"
          >
            {{ cat.icon }} {{ cat.name }}
          </router-link>
          <p v-if="categories.length === 0" class="text-muted category-dropdown__empty">دسته‌بندی‌ای ثبت نشده</p>
        </div>
      </div>

      <!-- Menu -->
      <div class="nav-links">
        <router-link to="/" exact>خانه</router-link>
        <router-link to="/courses">دوره‌ها</router-link>
        <router-link to="/gallery">گالری</router-link>
        <router-link to="/workshops">کارگاه‌ها</router-link>
        <router-link to="/shop">فروشگاه</router-link>
        <router-link to="/contact">تماس با ما</router-link>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "NavigationBar",
  data() {
    return { categoriesOpen: false };
  },
  computed: {
    ...mapGetters("platform", ["multivendorEnabled"]),
    categories() {
      return this.$store.state.products.categories;
    },
  },
  created() {
    this.$store.dispatch("products/fetchCategories");
  },
};
</script>

<style scoped>
.navigation-bar {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
}
.nav-inner {
  height: 52px;
  display: flex;
  align-items: center;
  gap: 20px;
}

/* CATEGORY BUTTON */
.category-dropdown {
  position: relative;
}
.all-category-btn {
  height: 38px;
  padding: 0 20px;
  border: none;
  border-radius: var(--radius-sm);
  background: var(--color-primary);
  color: white;
  font-family: inherit;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
  cursor: pointer;
}
.category-dropdown__menu {
  position: absolute;
  top: 44px;
  right: 0;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-md);
  border-radius: var(--radius);
  min-width: 200px;
  padding: 8px;
  display: flex;
  flex-direction: column;
  z-index: 60;
}
.category-dropdown__menu a {
  padding: 9px 12px;
  border-radius: var(--radius-sm);
  font-size: 0.86rem;
  font-weight: 600;
  color: var(--color-text);
}
.category-dropdown__menu a:hover {
  background: var(--color-bg);
}
.category-dropdown__empty {
  padding: 9px 12px;
  font-size: 0.82rem;
}

/* LINKS */
.nav-links {
  display: flex;
  align-items: center;
  gap: 28px;
  height: 100%;
}
.nav-links a {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-text-muted);
  position: relative;
  height: 100%;
  display: flex;
  align-items: center;
}
.nav-links a:hover {
  color: var(--color-primary);
}
.nav-links a.router-link-active {
  color: var(--color-primary);
}
.nav-links a.router-link-active::after {
  content: "";
  position: absolute;
  bottom: 0;
  right: 0;
  left: 0;
  height: 3px;
  background: var(--color-accent);
}

@media (max-width: 900px) {
  .nav-inner {
    overflow-x: auto;
  }
  .nav-links {
    gap: 20px;
  }
  .all-category-btn {
    font-size: 0.85rem;
  }
}
</style>