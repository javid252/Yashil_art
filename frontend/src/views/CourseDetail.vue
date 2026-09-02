<template>
  <div v-if="loading" class="loading-state container">
    <div class="skeleton-detail"></div>
  </div>
  <div v-else-if="course" class="course-detail">
    <!-- Hero -->
    <section class="detail-hero">
      <div class="container detail-hero-inner">
        <div class="detail-hero-text">
          <span class="course-level badge" :class="levelClass(course.level)">{{ course.level_display }}</span>
          <h1>{{ course.title }}</h1>
          <p class="detail-short-desc">{{ course.short_description }}</p>
          <div class="detail-meta">
            <span v-if="course.instructor_name">🎓 {{ course.instructor_name }}</span>
            <span>⏱ {{ course.duration_weeks }} هفته</span>
            <span>📚 {{ course.total_sessions }} جلسه</span>
            <span>👤 {{ course.enrolled_count }}/{{ course.max_students }} نفر</span>
          </div>
          <div class="detail-price">
            <span class="price" v-if="course.discount_price">{{ formatPrice(course.discount_price) }} تومان</span>
            <span class="price" v-else-if="course.price">{{ formatPrice(course.price) }} تومان</span>
            <span class="price-free" v-else>رایگان</span>
            <span class="price-old" v-if="course.discount_price">{{ formatPrice(course.price) }}</span>
          </div>
          <button
            v-if="!course.is_enrolled"
            class="btn btn-primary btn-lg"
            @click="enroll"
            :disabled="course.is_full"
          >
            {{ course.is_full ? 'ظرفیت تکمیل' : 'ثبت‌نام در دوره' }}
          </button>
          <router-link v-else to="/my-courses" class="btn btn-primary btn-lg">
            مشاهده دوره من
          </router-link>
        </div>
        <div class="detail-hero-image">
          <img v-if="course.cover_image" :src="course.cover_image" :alt="course.title" />
          <div v-else class="detail-hero-placeholder">🎨</div>
        </div>
      </div>
    </section>

    <!-- Content -->
    <section class="detail-content container">
      <div class="detail-grid">
        <!-- Main Content -->
        <div class="detail-main">
          <div class="detail-section">
            <h2>توضیحات دوره</h2>
            <div class="detail-description" v-html="course.description"></div>
          </div>

          <div class="detail-section" v-if="course.what_you_learn && course.what_you_learn.length">
            <h2>چه چیزی یاد می‌گیرید؟</h2>
            <ul class="learn-list">
              <li v-for="(item, i) in course.what_you_learn" :key="i">✅ {{ item }}</li>
            </ul>
          </div>

          <div class="detail-section" v-if="course.prerequisites">
            <h2>پیش‌نیازها</h2>
            <p>{{ course.prerequisites }}</p>
          </div>

          <div class="detail-section" v-if="course.materials_needed">
            <h2>وسایل مورد نیاز</h2>
            <p>{{ course.materials_needed }}</p>
          </div>

          <!-- Gallery -->
          <div class="detail-section" v-if="course.gallery_images && course.gallery_images.length">
            <h2>گالری دوره</h2>
            <div class="detail-gallery">
              <div v-for="img in course.gallery_images" :key="img.id" class="gallery-thumb">
                <img :src="img.image" :alt="img.caption" />
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="detail-sidebar">
          <div class="sidebar-card">
            <h3>برنامه زمانی</h3>
            <div v-if="course.schedules && course.schedules.length" class="schedule-list">
              <div v-for="s in course.schedules" :key="s.id" class="schedule-item">
                <span class="schedule-day">{{ s.day_display }}</span>
                <span class="schedule-time">{{ s.start_time }} - {{ s.end_time }}</span>
                <span class="schedule-room" v-if="s.room">{{ s.room }}</span>
              </div>
            </div>
            <p v-else class="text-muted">برنامه زمانی ثابت ندارد</p>
          </div>

          <div class="sidebar-card">
            <h3>اطلاعات دوره</h3>
            <div class="info-list">
              <div class="info-row">
                <span>سطح</span>
                <span>{{ course.level_display }}</span>
              </div>
              <div class="info-row">
                <span>مدت</span>
                <span>{{ course.duration_weeks }} هفته</span>
              </div>
              <div class="info-row">
                <span>جلسات</span>
                <span>{{ course.total_sessions }} جلسه</span>
              </div>
              <div class="info-row">
                <span>مدت هر جلسه</span>
                <span>{{ course.session_duration_minutes }} دقیقه</span>
              </div>
              <div class="info-row">
                <span>ظرفیت</span>
                <span>{{ course.max_students }} نفر</span>
              </div>
              <div class="info-row" v-if="course.available_spots > 0">
                <span>ظرفیت باقیمانده</span>
                <span class="text-success">{{ course.available_spots }} نفر</span>
              </div>
            </div>
          </div>

          <div class="sidebar-card instructor-card" v-if="course.instructor_name">
            <h3>استاد دوره</h3>
            <div class="instructor-info">
              <router-link :to="`/instructors/${course.instructor}`" class="instructor-link">
                <strong>{{ course.instructor_name }}</strong>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
  <div v-else class="empty-state container">
    <div class="icon">📚</div>
    <p>دوره یافت نشد</p>
  </div>
</template>

<script>
import api from "@/services/api";
import { mapGetters } from "vuex";

export default {
  name: "CourseDetail",
  data() {
    return { course: null, loading: true };
  },
  computed: {
    ...mapGetters("auth", ["isAuthenticated"]),
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
    async loadCourse() {
      try {
        const { data } = await api.get(`/courses/${this.$route.params.id}/`);
        this.course = data;
      } catch (e) {
        console.error(e);
      } finally {
        this.loading = false;
      }
    },
    async enroll() {
      if (!this.isAuthenticated) {
        this.$router.push({ name: "login", query: { redirect: this.$route.fullPath } });
        return;
      }
      try {
        await api.post("/enrollments/my/enroll/", {
          course_id: this.course.id,
          payment_type: "single",
        });
        this.$store.dispatch("notify", { message: "ثبت‌نام با موفقیت انجام شد!" });
        this.loadCourse();
      } catch (e) {
        const msg = e.response?.data?.error || "خطا در ثبت‌نام";
        this.$store.dispatch("notify", { message: msg, type: "error" });
      }
    },
  },
  created() {
    this.loadCourse();
  },
};
</script>

<style scoped>
.detail-hero {
  background: linear-gradient(135deg, #1f4b43, #0d2b26);
  color: white;
  padding: 60px 0;
}

.detail-hero-inner {
  display: flex;
  align-items: center;
  gap: 40px;
}

.detail-hero-text {
  flex: 1;
}

.detail-hero-text h1 {
  font-size: 2rem;
  margin: 16px 0;
}

.detail-short-desc {
  color: rgba(255,255,255,0.8);
  font-size: 1.05rem;
  margin-bottom: 20px;
}

.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  font-size: 0.9rem;
  color: rgba(255,255,255,0.7);
  margin-bottom: 20px;
}

.detail-price {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  font-size: 1.3rem;
}

.detail-hero-image {
  width: 380px;
  height: 260px;
  border-radius: var(--radius-lg);
  overflow: hidden;
  flex-shrink: 0;
}

.detail-hero-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.detail-hero-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 5rem;
  background: rgba(255,255,255,0.1);
}

.btn-lg { padding: 14px 36px; font-size: 1rem; }

.detail-content { padding: 40px 20px; }

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 30px;
}

.detail-section {
  margin-bottom: 36px;
}

.detail-section h2 {
  font-size: 1.3rem;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--color-border);
}

.detail-description {
  line-height: 1.9;
  color: var(--color-text);
}

.learn-list {
  list-style: none;
  padding: 0;
}

.learn-list li {
  padding: 8px 0;
  font-size: 0.95rem;
}

.detail-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
}

.gallery-thumb {
  border-radius: var(--radius-sm);
  overflow: hidden;
  aspect-ratio: 1;
}

.gallery-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.sidebar-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 20px;
  margin-bottom: 20px;
}

.sidebar-card h3 {
  font-size: 1rem;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--color-border);
}

.schedule-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid var(--color-border);
  font-size: 0.88rem;
}

.schedule-day { font-weight: 700; color: var(--color-primary); }
.schedule-time { color: var(--color-text-muted); }

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid var(--color-border);
  font-size: 0.88rem;
}

.text-success { color: var(--color-success); font-weight: 700; }

.loading-state { padding: 100px 20px; text-align: center; }
.skeleton-detail { height: 400px; border-radius: var(--radius); background: linear-gradient(110deg, var(--color-sand) 30%, var(--color-bg) 50%, var(--color-sand) 70%); background-size: 200% 100%; animation: shimmer 1.5s infinite; }
@keyframes shimmer { to { background-position: -200% 0; } }

@media (max-width: 800px) {
  .detail-hero-inner { flex-direction: column; }
  .detail-hero-image { width: 100%; height: 200px; }
  .detail-grid { grid-template-columns: 1fr; }
}
</style>
