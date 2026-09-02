<template>
  <div class="workshops-page container">
    <div class="page-header">
      <span class="eyebrow">کارگاه‌ها</span>
      <h1>کارگاه‌های آموزشی</h1>
      <p>کارگاه‌های کوتاه‌مدت و بلندمدت ویژه علاقه‌مندان به هنر</p>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="filter-group">
        <select v-model="filters.duration_type" @change="loadWorkshops">
          <option value="">همه انواع</option>
          <option value="one">تک جلسه‌ای</option>
          <option value="short">کوتاه‌مدت</option>
          <option value="long">بلندمدت</option>
          <option value="intensive">فشرده</option>
        </select>
      </div>
      <div class="filter-group">
        <select v-model="filters.ordering" @change="loadWorkshops">
          <option value="start_date">نزدیک‌ترین</option>
          <option value="-created_at">جدیدترین</option>
          <option value="price">ارزان‌ترین</option>
          <option value="-price">گران‌ترین</option>
        </select>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="workshops-grid">
      <div v-for="n in 6" :key="n" class="workshop-skeleton"></div>
    </div>

    <!-- Workshops -->
    <div v-else-if="workshops.length" class="workshops-grid">
      <router-link
        v-for="ws in workshops"
        :key="ws.id"
        :to="`/workshops/${ws.id}/${ws.slug}`"
        class="workshop-card"
      >
        <div class="workshop-thumb">
          <img v-if="ws.thumbnail" :src="ws.thumbnail" :alt="ws.title" />
          <div v-else class="workshop-thumb-placeholder">🎪</div>
          <span class="workshop-type badge">{{ ws.duration_type_display }}</span>
          <span v-if="ws.is_online" class="workshop-online">آنلاین</span>
        </div>
        <div class="workshop-info">
          <span class="workshop-category">{{ ws.category_name }}</span>
          <h3>{{ ws.title }}</h3>
          <p class="workshop-desc">{{ ws.short_description }}</p>
          <div class="workshop-meta">
            <span>📅 {{ ws.start_date }}</span>
            <span>⏰ {{ ws.start_time }}</span>
            <span>⏱ {{ ws.duration_display }}</span>
          </div>
          <div class="workshop-meta">
            <span>📍 {{ ws.location || (ws.is_online ? 'آنلاین' : 'حضوری') }}</span>
            <span>👥 {{ ws.enrolled_count }}/{{ ws.max_participants }}</span>
          </div>
          <div class="workshop-price">
            <span class="price">{{ formatPrice(ws.price) }} تومان</span>
            <span v-if="ws.available_spots > 0" class="spots-left">{{ ws.available_spots }} ظرفیت باقیمانده</span>
            <span v-else class="spots-full">تکمیل ظرفیت</span>
          </div>
          <div class="workshop-instructor" v-if="ws.instructor_name">
            <span>🎓 {{ ws.instructor_name }}</span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Empty -->
    <div v-else class="empty-state">
      <div class="icon">🎪</div>
      <p>کارگاهی یافت نشد</p>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "WorkshopList",
  data() {
    return {
      workshops: [],
      loading: true,
      filters: {
        duration_type: "",
        ordering: "start_date",
      },
    };
  },
  methods: {
    formatPrice(price) {
      return new Intl.NumberFormat("fa-IR").format(price);
    },
    async loadWorkshops() {
      this.loading = true;
      try {
        const params = { ordering: this.filters.ordering };
        if (this.filters.duration_type) params.duration_type = this.filters.duration_type;

        const { data } = await api.get("/workshops/", { params });
        this.workshops = data.results || data;
      } catch (e) { console.error(e); }
      finally { this.loading = false; }
    },
  },
  created() {
    this.loadWorkshops();
  },
};
</script>

<style scoped>
.workshops-page { padding: 40px 20px 60px; }
.page-header { text-align: center; margin-bottom: 30px; }
.page-header h1 { font-size: 2rem; margin-top: 10px; }
.page-header p { color: var(--color-text-muted); margin-top: 10px; }

.filters-bar {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  margin-bottom: 30px;
  padding: 14px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
}

.filter-group select {
  padding: 8px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.88rem;
  background: var(--color-bg);
}

.workshops-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
}

.workshop-card {
  border-radius: var(--radius);
  overflow: hidden;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  transition: all 0.3s ease;
}

.workshop-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(31, 75, 67, 0.1);
}

.workshop-thumb {
  position: relative;
  height: 200px;
  overflow: hidden;
  background: var(--color-sand);
}

.workshop-thumb img { width: 100%; height: 100%; object-fit: cover; }
.workshop-thumb-placeholder { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 3rem; }

.workshop-type {
  position: absolute;
  top: 12px;
  left: 12px;
  background: rgba(227, 168, 87, 0.9);
  color: #1f4b43;
}

.workshop-online {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(46, 107, 94, 0.9);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
}

.workshop-info { padding: 18px; }
.workshop-category { font-size: 0.78rem; color: var(--color-primary); font-weight: 600; }
.workshop-info h3 { font-size: 1.1rem; margin: 8px 0; }
.workshop-desc { font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 12px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.workshop-meta { display: flex; flex-wrap: wrap; gap: 14px; font-size: 0.82rem; color: var(--color-text-muted); margin-bottom: 8px; }

.workshop-price { display: flex; align-items: center; gap: 12px; margin-top: 12px; }
.spots-left { font-size: 0.78rem; color: var(--color-success); font-weight: 600; }
.spots-full { font-size: 0.78rem; color: var(--color-danger); font-weight: 600; }
.workshop-instructor { margin-top: 10px; font-size: 0.82rem; color: var(--color-text-muted); }

.workshop-skeleton {
  height: 380px;
  border-radius: var(--radius);
  background: linear-gradient(110deg, var(--color-sand) 30%, var(--color-bg) 50%, var(--color-sand) 70%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer { to { background-position: -200% 0; } }
</style>
