<template>
  <div class="product-list-page">
    <!-- Breadcrumb -->
    <div class="container">
      <nav class="breadcrumb">
        <router-link to="/">خانه</router-link>
        <span class="separator">‹</span>
        <span class="current">محصولات</span>
        <span v-if="activeCategoryName" class="separator">‹</span>
        <span v-if="activeCategoryName" class="current">{{ activeCategoryName }}</span>
      </nav>
    </div>

    <!-- Page Header -->
    <div class="container page-header">
      <div class="page-header__text">
        <h1>محصولات</h1>
        <p class="text-muted" v-if="!loading">{{ count }} محصول پیدا شد</p>
      </div>
      <div class="page-header__actions">
        <div class="sort-mobile">
          <select v-model="filters.ordering" @change="fetchProducts">
            <option value="-created_at">جدیدترین</option>
            <option value="-sales_count">پرفروش‌ترین</option>
            <option value="price">ارزان‌ترین</option>
            <option value="-price">گران‌ترین</option>
          </select>
        </div>
        <button class="btn-filter-toggle" @click="showMobileFilter = true">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M6 12h12M8 18h8"/></svg>
          فیلترها
        </button>
      </div>
    </div>

    <!-- Active Filters Bar -->
    <div v-if="hasActiveFilters" class="container active-filters">
      <div class="active-filters__list">
        <span v-if="filters.search" class="active-tag">
          جستجو: "{{ filters.search }}"
          <button @click="clearFilter('search')">×</button>
        </span>
        <span v-if="filters.category" class="active-tag">
          {{ activeCategoryName }}
          <button @click="clearFilter('category')">×</button>
        </span>
        <span v-if="filters.min_price" class="active-tag">
          از {{ formatPrice(filters.min_price) }} تومان
          <button @click="clearFilter('min_price')">×</button>
        </span>
        <span v-if="filters.max_price" class="active-tag">
          تا {{ formatPrice(filters.max_price) }} تومان
          <button @click="clearFilter('max_price')">×</button>
        </span>
        <span v-if="filters.has_discount" class="active-tag">
          تخفیف‌دار
          <button @click="clearFilter('has_discount')">×</button>
        </span>
      </div>
      <button class="clear-all" @click="clearAllFilters">پاک کردن همه فیلترها</button>
    </div>

    <div class="container main-layout">
      <!-- Desktop Sidebar -->
      <aside class="sidebar card">
        <div class="sidebar__header">
          <h3>فیلترها</h3>
          <button v-if="hasActiveFilters" class="clear-all-sm" @click="clearAllFilters">پاک کردن</button>
        </div>

        <!-- Search -->
        <div class="filter-section" :class="{ open: openSections.search }">
          <button class="filter-section__toggle" @click="openSections.search = !openSections.search">
            <span>جستجو</span>
            <span class="chevron" :class="{ rotated: openSections.search }">‹</span>
          </button>
          <div v-show="openSections.search" class="filter-section__body">
            <div class="search-input-wrap">
              <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
              <input v-model="filters.search" type="text" placeholder="نام محصول..." @input="debouncedFetch" />
            </div>
          </div>
        </div>

        <!-- Categories -->
        <div class="filter-section" :class="{ open: openSections.category }">
          <button class="filter-section__toggle" @click="openSections.category = !openSections.category">
            <span>دسته‌بندی</span>
            <span class="chevron" :class="{ rotated: openSections.category }">‹</span>
          </button>
          <div v-show="openSections.category" class="filter-section__body">
            <div class="filter-options">
              <button class="filter-chip" :class="{ active: !filters.category }" @click="setCategory('')">
                <span class="chip-icon">📦</span> همه
              </button>
              <button
                v-for="cat in categories"
                :key="cat.id"
                class="filter-chip"
                :class="{ active: filters.category === cat.slug }"
                @click="setCategory(cat.slug)"
              >
                <span class="chip-icon">{{ cat.icon || '🛍️' }}</span> {{ cat.name }}
              </button>
            </div>
          </div>
        </div>

        <!-- Price Range -->
        <div class="filter-section" :class="{ open: openSections.price }">
          <button class="filter-section__toggle" @click="openSections.price = !openSections.price">
            <span>محدوده قیمت</span>
            <span class="chevron" :class="{ rotated: openSections.price }">‹</span>
          </button>
          <div v-show="openSections.price" class="filter-section__body">
            <!-- Range Slider -->
            <div class="price-range-slider">
              <div class="range-track">
                <div class="range-fill" :style="rangeFillStyle"></div>
              </div>
              <input
                type="range"
                class="range-input range-min"
                :min="0"
                :max="priceBound"
                :value="filters.min_price || 0"
                @input="onSliderMin"
              />
              <input
                type="range"
                class="range-input range-max"
                :min="0"
                :max="priceBound"
                :value="filters.max_price || priceBound"
                @input="onSliderMax"
              />
            </div>
            <div class="price-range-labels">
              <span>{{ formatPrice(filters.min_price || 0) }}</span>
              <span>{{ formatPrice(filters.max_price || priceBound) }}</span>
            </div>
            <!-- Input Boxes -->
            <div class="price-inputs">
              <div class="price-input-group">
                <label class="price-label">حداقل قیمت</label>
                <div class="price-input-wrap">
                  <input v-model="priceMinText" type="text" inputmode="numeric" placeholder="۰" @blur="onPriceBlur('min')" />
                  <span class="price-unit">تومان</span>
                </div>
              </div>
              <div class="price-input-group">
                <label class="price-label">حداکثر قیمت</label>
                <div class="price-input-wrap">
                  <input v-model="priceMaxText" type="text" inputmode="numeric" :placeholder="formatPriceInput(priceBound)" @blur="onPriceBlur('max')" />
                  <span class="price-unit">تومان</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Discount -->
        <div class="filter-section" :class="{ open: openSections.discount }">
          <button class="filter-section__toggle" @click="openSections.discount = !openSections.discount">
            <span>تخفیف</span>
            <span class="chevron" :class="{ rotated: openSections.discount }">‹</span>
          </button>
          <div v-show="openSections.discount" class="filter-section__body">
            <label class="toggle-label">
              <span class="toggle-switch" :class="{ on: filters.has_discount }" @click="filters.has_discount = filters.has_discount ? '' : 'true'; fetchProducts()">
                <span class="toggle-knob"></span>
              </span>
              <span>فقط محصولات تخفیف‌دار</span>
            </label>
          </div>
        </div>
      </aside>

      <!-- Results -->
      <section class="results">
        <!-- Skeleton Loading -->
        <div v-if="loading" class="product-grid">
          <div v-for="n in 8" :key="n" class="skeleton-card">
            <div class="skeleton-image"></div>
            <div class="skeleton-body">
              <div class="skeleton-line short"></div>
              <div class="skeleton-line medium"></div>
              <div class="skeleton-line long"></div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="products.length === 0" class="empty-state">
          <div class="empty-state__icon">🔍</div>
          <h3>محصولی پیدا نشد</h3>
          <p>با فیلترهای فعلی محصولی یافت نشد. فیلترها رو تغییر بدید یا پاک کنید.</p>
          <button class="btn btn-primary" @click="clearAllFilters">پاک کردن فیلترها</button>
        </div>

        <!-- Product Grid -->
        <div v-else class="product-grid">
          <ProductCard v-for="p in products" :key="p.id" :product="p" />
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination">
          <button class="page-btn" :disabled="page <= 1" @click="goPage(page - 1)">
            <span>‹</span> قبلی
          </button>

          <template v-for="p in paginationRange">
            <span v-if="p === '...'" :key="'dots-' + p" class="page-dots">...</span>
            <button
              v-else
              :key="p"
              class="page-num"
              :class="{ active: p === page }"
              @click="goPage(p)"
            >{{ p }}</button>
          </template>

          <button class="page-btn" :disabled="page >= totalPages" @click="goPage(page + 1)">
            بعدی <span>›</span>
          </button>
        </div>
      </section>
    </div>

    <!-- Mobile Filter Drawer -->
    <div class="drawer-overlay" :class="{ visible: showMobileFilter }" @click="showMobileFilter = false"></div>
    <div class="drawer" :class="{ open: showMobileFilter }">
      <div class="drawer__header">
        <h3>فیلترها</h3>
        <button class="drawer__close" @click="showMobileFilter = false">×</button>
      </div>
      <div class="drawer__body">
        <div class="filter-section open">
          <div class="filter-section__body">
            <div class="search-input-wrap">
              <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
              <input v-model="filters.search" type="text" placeholder="نام محصول..." @input="debouncedFetch" />
            </div>
          </div>
        </div>

        <div class="filter-section open">
          <div class="filter-section__toggle-static">دسته‌بندی</div>
          <div class="filter-section__body">
            <div class="filter-options">
              <button class="filter-chip" :class="{ active: !filters.category }" @click="setCategory('')">همه</button>
              <button v-for="cat in categories" :key="cat.id" class="filter-chip" :class="{ active: filters.category === cat.slug }" @click="setCategory(cat.slug)">
                {{ cat.icon }} {{ cat.name }}
              </button>
            </div>
          </div>
        </div>

        <div class="filter-section open">
          <div class="filter-section__toggle-static">قیمت</div>
          <div class="filter-section__body">
            <div class="price-range-slider">
              <div class="range-track">
                <div class="range-fill" :style="rangeFillStyle"></div>
              </div>
              <input type="range" class="range-input range-min" :min="0" :max="priceBound" :value="filters.min_price || 0" @input="onSliderMin" />
              <input type="range" class="range-input range-max" :min="0" :max="priceBound" :value="filters.max_price || priceBound" @input="onSliderMax" />
            </div>
            <div class="price-range-labels">
              <span>{{ formatPrice(filters.min_price || 0) }}</span>
              <span>{{ formatPrice(filters.max_price || priceBound) }}</span>
            </div>
            <div class="price-inputs">
              <div class="price-input-group">
                <label class="price-label">حداقل</label>
                <div class="price-input-wrap">
                  <input v-model="priceMinText" type="text" inputmode="numeric" placeholder="۰" @blur="onPriceBlur('min')" />
                  <span class="price-unit">تومان</span>
                </div>
              </div>
              <div class="price-input-group">
                <label class="price-label">حداکثر</label>
                <div class="price-input-wrap">
                  <input v-model="priceMaxText" type="text" inputmode="numeric" :placeholder="formatPriceInput(priceBound)" @blur="onPriceBlur('max')" />
                  <span class="price-unit">تومان</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="filter-section open">
          <label class="checkbox-label">
            <input type="checkbox" v-model="filters.has_discount" true-value="true" false-value="" @change="fetchProducts" />
            فقط تخفیف‌دار
          </label>
        </div>
      </div>
      <div class="drawer__footer">
        <button class="btn btn-primary btn-block" @click="showMobileFilter = false">نمایش نتایج</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import ProductCard from "@/components/ProductCard.vue";

export default {
  name: "ProductListView",
  components: { ProductCard },
  data() {
    return {
      products: [],
      count: 0,
      page: 1,
      loading: true,
      debounceTimer: null,
      showMobileFilter: false,
      priceMinText: "",
      priceMaxText: "",
      openSections: { search: true, category: true, price: false, discount: false },
      filters: {
        search: this.$route.query.search || "",
        category: this.$route.query.category || "",
        min_price: null,
        max_price: null,
        ordering: this.$route.query.ordering || "-created_at",
        is_featured: this.$route.query.featured ? true : undefined,
        has_discount: this.$route.query.has_discount ? true : undefined,
      },
    };
  },
  computed: {
    categories() {
      return this.$store.state.products.categories;
    },
    priceBound() {
      return 50000000;
    },
    rangeFillStyle() {
      const min = this.filters.min_price || 0;
      const max = this.filters.max_price || this.priceBound;
      // RTL: right = small values (min), left = large values (max)
      const right = (min / this.priceBound) * 100;
      const left = 100 - (max / this.priceBound) * 100;
      return { left: left + '%', right: right + '%' };
    },
    totalPages() {
      return Math.max(Math.ceil(this.count / 12), 1);
    },
    activeCategoryName() {
      if (!this.filters.category) return "";
      const cat = this.categories.find((c) => c.slug === this.filters.category);
      return cat ? cat.name : "";
    },
    hasActiveFilters() {
      return this.filters.search || this.filters.category || this.filters.min_price || this.filters.max_price || this.filters.has_discount;
    },
    paginationRange() {
      const total = this.totalPages;
      const current = this.page;
      if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1);
      const range = [];
      range.push(1);
      if (current > 3) range.push("...");
      for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
        range.push(i);
      }
      if (current < total - 2) range.push("...");
      range.push(total);
      return range;
    },
  },
  created() {
    this.$store.dispatch("products/fetchCategories");
    this.initPriceTexts();
    this.fetchProducts();
  },
  watch: {
    "$route.query"(newQuery, oldQuery) {
      if (JSON.stringify(newQuery) === JSON.stringify(oldQuery)) return;
      this.filters.search = newQuery.search || "";
      this.filters.category = newQuery.category || "";
      this.filters.ordering = newQuery.ordering || "-created_at";
      this.filters.is_featured = newQuery.featured ? true : undefined;
      this.filters.has_discount = newQuery.has_discount ? true : undefined;
      this.page = 1;
      this.fetchProducts();
    },
  },
  methods: {
    formatPrice(v) {
      return Number(v || 0).toLocaleString("fa-IR");
    },
    formatPriceInput(num) {
      if (num == null || num === "") return "";
      return Number(num).toLocaleString("fa-IR");
    },
    parsePriceInput(str) {
      if (!str) return null;
      let result = str.toString();
      // Convert Persian digits to Latin
      result = result.replace(/[۰-۹]/g, function(d) { return '۰۱۲۳۴۵۶۷۸۹'.indexOf(d).toString(); });
      // Convert Arabic digits to Latin
      result = result.replace(/[٠-٩]/g, function(d) { return '٠١٢٣٤٥٦٧٨٩'.indexOf(d).toString(); });
      // Remove separators
      result = result.replace(/[,،\s]/g, "");
      return result ? Number(result) : null;
    },
    initPriceTexts() {
      this.priceMinText = this.formatPriceInput(this.filters.min_price);
      this.priceMaxText = this.formatPriceInput(this.filters.max_price);
    },
    onPriceBlur(which) {
      const key = which === "min" ? "priceMinText" : "priceMaxText";
      const raw = this.parsePriceInput(this[key]);
      this.filters[which === "min" ? "min_price" : "max_price"] = raw;
      this[key] = this.formatPriceInput(raw);
      this.page = 1;
      this.fetchProducts();
    },
    onSliderMin(e) {
      const val = Number(e.target.value);
      this.filters.min_price = val;
      this.priceMinText = this.formatPriceInput(val);
      if (this.filters.max_price && val > this.filters.max_price) {
        this.filters.max_price = val;
        this.priceMaxText = this.formatPriceInput(val);
      }
      this.debouncedFetch();
    },
    onSliderMax(e) {
      const val = Number(e.target.value);
      this.filters.max_price = val;
      this.priceMaxText = this.formatPriceInput(val);
      if (this.filters.min_price && val < this.filters.min_price) {
        this.filters.min_price = val;
        this.priceMinText = this.formatPriceInput(val);
      }
      this.debouncedFetch();
    },
    setCategory(slug) {
      this.filters.category = slug;
      this.fetchProducts();
    },
    clearFilter(key) {
      if (key === "has_discount") this.filters[key] = undefined;
      else if (key === "min_price" || key === "max_price") this.filters[key] = null;
      else this.filters[key] = "";
      this.page = 1;
      this.fetchProducts();
    },
    clearAllFilters() {
      this.filters.search = "";
      this.filters.category = "";
      this.filters.min_price = null;
      this.filters.max_price = null;
      this.filters.has_discount = undefined;
      this.filters.ordering = "-created_at";
      this.page = 1;
      this.initPriceTexts();
      this.fetchProducts();
    },
    debouncedFetch() {
      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => this.fetchProducts(), 400);
    },
    goPage(p) {
      this.page = p;
      this.fetchProducts();
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
    async fetchProducts() {
      this.loading = true;
      try {
        const params = { page: this.page, ...this.filters };
        Object.keys(params).forEach((k) => (params[k] === "" || params[k] == null) && delete params[k]);
        const { data } = await api.get("/products/", { params });
        this.products = data.results || data;
        this.count = data.count ?? this.products.length;
      } catch (e) {
        this.$store.dispatch("notify", { message: "بارگذاری محصولات ناموفق بود.", type: "error" });
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* ========== Breadcrumb ========== */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 0 0;
  font-size: 0.82rem;
  color: var(--color-text-muted);
}
.breadcrumb a { color: var(--color-primary); font-weight: 600; }
.breadcrumb a:hover { text-decoration: underline; }
.breadcrumb .separator { opacity: 0.4; transform: scaleX(-1); display: inline-block; }
.breadcrumb .current { color: var(--color-text); font-weight: 600; }

/* ========== Page Header ========== */
.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding: 20px 20px 0;
  margin-bottom: 16px;
}
.page-header h1 { font-size: 1.6rem; margin: 0 0 4px; }
.page-header__actions { display: flex; gap: 10px; align-items: center; }
.btn-filter-toggle {
  display: none;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  font-family: inherit;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
}
.sort-mobile select {
  padding: 8px 12px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.85rem;
  background: var(--color-surface);
}

/* ========== Active Filters ========== */
.active-filters {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 20px 16px;
  flex-wrap: wrap;
}
.active-filters__list { display: flex; gap: 8px; flex-wrap: wrap; flex: 1; }
.active-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  background: var(--color-sand);
  border-radius: 20px;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--color-primary-dark);
}
.active-tag button {
  background: none;
  border: none;
  color: var(--color-text-muted);
  font-size: 1rem;
  cursor: pointer;
  line-height: 1;
  padding: 0;
}
.active-tag button:hover { color: var(--color-danger); }
.clear-all {
  background: none;
  border: none;
  color: var(--color-danger);
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}

/* ========== Main Layout ========== */
.main-layout {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 28px;
  padding: 0 20px 60px;
}

/* ========== Sidebar ========== */
.sidebar {
  padding: 20px;
  align-self: start;
  position: sticky;
  top: calc(var(--header-height) + 20px);
  border-radius: var(--radius);
}
.sidebar__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.sidebar__header h3 { font-size: 1rem; margin: 0; }
.clear-all-sm {
  background: none;
  border: none;
  color: var(--color-danger);
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
}

/* Filter Sections */
.filter-section { border-bottom: 1px solid var(--color-border); }
.filter-section:last-child { border-bottom: none; }
.filter-section__toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 14px 0;
  background: none;
  border: none;
  font-family: inherit;
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--color-text);
  cursor: pointer;
}
.chevron {
  transition: transform 0.2s;
  font-size: 1.1rem;
  opacity: 0.4;
}
.chevron.rotated { transform: rotate(90deg); }
.filter-section__body { padding-bottom: 14px; }
.filter-section__toggle-static {
  padding: 14px 0 8px;
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--color-text);
}

/* Search */
.search-input-wrap {
  position: relative;
}
.search-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-muted);
}
.search-input-wrap input {
  width: 100%;
  padding: 9px 12px 9px 32px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.87rem;
  background: var(--color-bg);
  transition: border-color 0.15s;
}
.search-input-wrap input:focus {
  outline: none;
  border-color: var(--color-primary);
}

/* Filter Options */
.filter-options { display: flex; flex-direction: column; gap: 4px; }
.filter-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  text-align: right;
  background: none;
  border: none;
  padding: 8px 10px;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  color: var(--color-text-muted);
  cursor: pointer;
  transition: all 0.15s;
}
.filter-chip:hover { background: var(--color-sand); color: var(--color-text); }
.filter-chip.active {
  background: var(--color-primary);
  color: #fff;
  font-weight: 700;
}
.chip-icon { font-size: 1rem; }

/* Price Range Slider */
.price-range-slider {
  position: relative;
  height: 32px;
  margin-bottom: 4px;
}
.range-track {
  position: absolute;
  top: 14px;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--color-border);
  border-radius: 2px;
}
.range-fill {
  position: absolute;
  top: 0;
  bottom: 0;
  background: var(--color-primary);
  border-radius: 2px;
}
.range-input {
  position: absolute;
  top: 4px;
  left: 0;
  width: 100%;
  height: 24px;
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
  pointer-events: none;
  margin: 0;
}
.range-input::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--color-primary);
  border: 3px solid #fff;
  box-shadow: 0 1px 4px rgba(0,0,0,0.2);
  cursor: pointer;
  pointer-events: all;
  position: relative;
  z-index: 2;
}
.range-input::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--color-primary);
  border: 3px solid #fff;
  box-shadow: 0 1px 4px rgba(0,0,0,0.2);
  cursor: pointer;
  pointer-events: all;
}
.range-input::-webkit-slider-runnable-track {
  height: 24px;
  background: transparent;
}
.range-input::-moz-range-track {
  height: 24px;
  background: transparent;
}
.price-range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  color: var(--color-text-muted);
  font-weight: 600;
  margin-bottom: 14px;
}
.price-inputs {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.price-input-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.price-label {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--color-text-muted);
}
.price-input-wrap {
  position: relative;
}
.price-input-wrap input {
  width: 100%;
  padding: 9px 60px 9px 10px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.85rem;
  background: var(--color-bg);
  transition: border-color 0.15s;
  box-sizing: border-box;
  direction: rtl;
  text-align: right;
}
.price-input-wrap input:focus {
  outline: none;
  border-color: var(--color-primary);
}
.price-unit {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.75rem;
  color: var(--color-text-muted);
  font-weight: 600;
  pointer-events: none;
}
.price-sep { color: var(--color-text-muted); }

/* Toggle */
.toggle-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
}
.toggle-switch {
  width: 40px;
  height: 22px;
  background: var(--color-border);
  border-radius: 11px;
  position: relative;
  transition: background 0.2s;
  cursor: pointer;
  flex-shrink: 0;
}
.toggle-switch.on { background: var(--color-primary); }
.toggle-knob {
  width: 18px;
  height: 18px;
  background: #fff;
  border-radius: 50%;
  position: absolute;
  top: 2px;
  right: 2px;
  transition: transform 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.15);
}
.toggle-switch.on .toggle-knob { transform: translateX(-18px); }

/* Checkbox (mobile) */
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  padding: 14px 0;
}

/* ========== Product Grid ========== */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

/* ========== Skeleton ========== */
.skeleton-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  overflow: hidden;
}
.skeleton-image {
  aspect-ratio: 1/1;
  background: linear-gradient(110deg, var(--color-sand) 30%, var(--color-bg) 50%, var(--color-sand) 70%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
.skeleton-body { padding: 14px; }
.skeleton-line {
  height: 12px;
  border-radius: 6px;
  margin-bottom: 10px;
  background: linear-gradient(110deg, var(--color-sand) 30%, var(--color-bg) 50%, var(--color-sand) 70%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
.skeleton-line.short { width: 40%; }
.skeleton-line.medium { width: 70%; }
.skeleton-line.long { width: 55%; }
@keyframes shimmer { to { background-position: -200% 0; } }

/* ========== Empty State ========== */
.empty-state {
  text-align: center;
  padding: 80px 20px;
}
.empty-state__icon { font-size: 3.5rem; margin-bottom: 16px; }
.empty-state h3 { font-size: 1.2rem; margin: 0 0 8px; }
.empty-state p { color: var(--color-text-muted); margin: 0 0 24px; max-width: 360px; margin-left: auto; margin-right: auto; }

/* ========== Pagination ========== */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 40px;
}
.page-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 8px 16px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  font-family: inherit;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}
.page-btn:hover:not(:disabled) { border-color: var(--color-primary); color: var(--color-primary); }
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.page-btn span { font-size: 1rem; }
.page-num {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  font-family: inherit;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}
.page-num:hover { border-color: var(--color-primary); color: var(--color-primary); }
.page-num.active {
  background: var(--color-primary);
  color: #fff;
  border-color: var(--color-primary);
}
.page-dots { padding: 0 4px; color: var(--color-text-muted); font-weight: 600; }

/* ========== Drawer (Mobile) ========== */
.drawer-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 100;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s, visibility 0.3s;
}
.drawer-overlay.visible { opacity: 1; visibility: visible; }
.drawer {
  position: fixed;
  bottom: 0;
  right: 0;
  width: 100%;
  max-height: 85vh;
  background: var(--color-surface);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  z-index: 101;
  transform: translateY(100%);
  transition: transform 0.35s cubic-bezier(0.32, 0.72, 0, 1);
  display: flex;
  flex-direction: column;
}
.drawer.open { transform: translateY(0); }
.drawer__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--color-border);
}
.drawer__header h3 { margin: 0; font-size: 1rem; }
.drawer__close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-text-muted);
  padding: 4px;
}
.drawer__body {
  flex: 1;
  overflow-y: auto;
  padding: 0 20px;
}
.drawer__footer {
  padding: 16px 20px;
  border-top: 1px solid var(--color-border);
}
.btn-block { width: 100%; }

/* ========== Responsive ========== */
@media (max-width: 860px) {
  .main-layout { grid-template-columns: 1fr; }
  .sidebar { display: none; }
  .btn-filter-toggle { display: inline-flex; }
  .product-grid { grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; }
}
</style>