<template>
  <div class="courses-page container">
    <div class="page-header">
      <span class="eyebrow">دوره‌های آموزشی</span>
      <h1>دوره‌ها و کارگاه‌ها</h1>
      <p>از میان دوره‌های متنوع ما، بهترین را برای خود انتخاب کنید</p>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="filter-group">
        <label>دسته‌بندی</label>
        <select v-model="filters.category" @change="loadCourses">
          <option value="">همه</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
        </select>
      </div>
      <div class="filter-group">
        <label>سطح</label>
        <select v-model="filters.level" @change="loadCourses">
          <option value="">همه</option>
          <option value="beginner">مبتدی</option>
          <option value="intermediate">متوسط</option>
          <option value="advanced">پیشرفته</option>
          <option value="all">همه سطوح</option>
        </select>
      </div>
      <div class="filter-group">
        <label>مرتب‌سازی</label>
        <select v-model="filters.ordering" @change="loadCourses">
          <option value="-created_at">جدیدترین</option>
          <option value="price">ارزان‌ترین</option>
          <option value="-price">گران‌ترین</option>
          <option value="-enrolled_count">محبوب‌ترین</option>
        </select>
      </div>
      <div class="filter-group search-group">
        <input v-model="filters.search" @keyup.enter="loadCourses" placeholder="جستجو..." />
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="courses-grid">
      <div v-for="n in 8" :key="n" class="course-skeleton">
        <div class="skeleton-image"></div>
        <div class="skeleton-body">
          <div class="skeleton-line short"></div>
          <div class="skeleton-line long"></div>
        </div>
      </div>
    </div>

    <!-- Courses Grid -->
    <div v-else-if="courses.length" class="courses-grid">
      <router-link
        v-for="course in courses"
        :key="course.id"
        :to="`/courses/${course.id}/${course.slug}`"
        class="course-card"
      >
        <div class="course-thumb">
          <img v-if="course.thumbnail" :src="course.thumbnail" :alt="course.title" />
          <div v-else class="course-thumb-placeholder">🎨</div>
          <span class="course-level badge" :class="levelClass(course.level)">{{ course.level_display }}</span>
        </div>
        <div class="course-info">
          <span class="course-category-name">{{ course.category_name }}</span>
          <h3>{{ course.title }}</h3>
          <p class="course-desc">{{ course.short_description }}</p>
          <div class="course-meta">
            <span>⏱ {{ course.duration_weeks }} هفته</span>
            <span>📚 {{ course.total_sessions }} جلسه</span>
            <span>👤 {{ course.enrolled_count }}/{{ course.max_students }}</span>
          </div>
          <div class="course-price">
            <span class="price" v-if="course.discount_price">{{ formatPrice(course.discount_price) }} تومان</span>
            <span class="price" v-else-if="course.price">{{ formatPrice(course.price) }} تومان</span>
            <span class="price-free" v-else>رایگان</span>
            <span class="price-old" v-if="course.discount_price">{{ formatPrice(course.price) }}</span>
            <span class="discount-badge" v-if="course.discount_percent">{{ course.discount_percent }}٪ تخفیف</span>
          </div>
          <div class="course-instructor" v-if="course.instructor_name">
            <span>🎓 {{ course.instructor_name }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="icon">📚</div>
      <p>دوره‌ای یافت نشد</p>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pagination">
      <button :disabled="currentPage <= 1" @click="changePage(currentPage - 1)">قبلی</button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button :disabled="currentPage >= totalPages" @click="changePage(currentPage + 1)">بعدی</button>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "CourseList",
  data() {
    return {
      courses: [],
      categories: [],
      loading: true,
      currentPage: 1,
      totalPages: 1,
      filters: {
        category: this.$route.query.category || "",
        level: "",
        ordering: "-created_at",
        search: "",
      },
    };
  },
  methods: {
    formatPrice(price) {
      return new Intl.NumberFormat("fa-IR").format(price);
    },
    levelClass(level) {
      return {
        "badge-beginner": level === "beginner",
        "badge-intermediate": level === "intermediate",
        "badge-advanced": level === "advanced",
      };
    },
    async loadCategories() {
      try {
        const { data } = await api.get("/courses/categories/");
        this.categories = data;
      } catch (e) {
        console.error(e);
      }
    },
    async loadCourses() {
      this.loading = true;
      try {
        const params = {
          page: this.currentPage,
          ordering: this.filters.ordering,
        };
        if (this.filters.category) params.category = this.filters.category;
        if (this.filters.level) params.level = this.filters.level;
        if (this.filters.search) params.search = this.filters.search;

        const { data } = await api.get("/courses/", { params });
        this.courses = data.results || data;
        this.totalPages = Math.ceil((data.count || this.courses.length) / 12);
      } catch (e) {
        console.error(e);
      } finally {
        this.loading = false;
      }
    },
    changePage(page) {
      this.currentPage = page;
      this.loadCourses();
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
  },
  created() {
    this.loadCategories();
    this.loadCourses();
  },
};
</script>

<style scoped>
.courses-page {
  padding: 40px 20px 60px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 2rem;
  margin-top: 10px;
}

.page-header p {
  color: var(--color-text-muted);
  margin-top: 10px;
}

.filters-bar {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 30px;
  padding: 16px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.filter-group label {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--color-text-muted);
}

.filter-group select,
.filter-group input {
  padding: 8px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.88rem;
  background: var(--color-bg);
}

.search-group {
  flex: 1;
  min-width: 200px;
}

.search-group input {
  width: 100%;
  height: 36px;
  margin-top: 18px;
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.course-card {
  border-radius: var(--radius);
  overflow: hidden;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  transition: all 0.3s ease;
}

.course-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(31, 75, 67, 0.1);
}

.course-thumb {
  position: relative;
  aspect-ratio: 16/10;
  overflow: hidden;
  background: var(--color-sand);
}

.course-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.course-thumb-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
}

.course-level {
  position: absolute;
  top: 12px;
  right: 12px;
  font-size: 0.75rem;
}

.badge-beginner { background: #e4f0ec; color: #2e6b5e; }
.badge-intermediate { background: #e6eef7; color: #2b5a8f; }
.badge-advanced { background: #f8e6e2; color: #b3452c; }

.course-info {
  padding: 18px;
}

.course-category-name {
  font-size: 0.78rem;
  color: var(--color-primary);
  font-weight: 600;
}

.course-info h3 {
  font-size: 1.05rem;
  margin: 8px 0;
}

.course-desc {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  line-height: 1.6;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.course-meta {
  display: flex;
  gap: 14px;
  font-size: 0.8rem;
  color: var(--color-text-muted);
  margin-bottom: 12px;
}

.course-price {
  display: flex;
  align-items: center;
  gap: 10px;
}

.price-free {
  color: var(--color-success);
  font-weight: 700;
}

.discount-badge {
  background: rgba(227, 168, 87, 0.15);
  color: #c98a3b;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 700;
}

.course-instructor {
  margin-top: 10px;
  font-size: 0.82rem;
  color: var(--color-text-muted);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 40px;
}

.pagination button {
  padding: 8px 20px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  font-family: inherit;
  font-size: 0.88rem;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.course-skeleton {
  border-radius: var(--radius);
  overflow: hidden;
  border: 1px solid var(--color-border);
}

.skeleton-image {
  aspect-ratio: 16/10;
  background: linear-gradient(110deg, var(--color-sand) 30%, var(--color-bg) 50%, var(--color-sand) 70%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton-body { padding: 18px; }
.skeleton-line { height: 12px; border-radius: 6px; margin-bottom: 10px; background: linear-gradient(110deg, var(--color-sand) 30%, var(--color-bg) 50%, var(--color-sand) 70%); background-size: 200% 100%; animation: shimmer 1.5s infinite; }
.skeleton-line.short { width: 40%; }
.skeleton-line.long { width: 70%; }

@keyframes shimmer { to { background-position: -200% 0; } }
</style>
