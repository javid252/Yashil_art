<template>
  <div class="student-dashboard">
    <div class="welcome-card">
      <div class="welcome-text">
        <h2>{{ greeting }}، {{ userLabel }} 👋</h2>
        <p>خوش آمدید به پنل دانشجویی یاشیل آرت</p>
      </div>
    </div>

    <div class="stat-grid">
      <div class="stat-card sc-courses">
        <div class="stat-icon">📚</div>
        <div class="stat-value">{{ stats.enrolled_courses || 0 }}</div>
        <div class="stat-label">دوره ثبت‌نام شده</div>
      </div>
      <div class="stat-card sc-grades">
        <div class="stat-icon">📝</div>
        <div class="stat-value">{{ stats.average_grade || '—' }}</div>
        <div class="stat-label">میانگین نمرات</div>
      </div>
      <div class="stat-card sc-certs">
        <div class="stat-icon">🏆</div>
        <div class="stat-value">{{ stats.certificates || 0 }}</div>
        <div class="stat-label">گواهینامه</div>
      </div>
      <div class="stat-card sc-gallery">
        <div class="stat-icon">🖼️</div>
        <div class="stat-value">{{ stats.artworks || 0 }}</div>
        <div class="stat-label">آثار هنری</div>
      </div>
    </div>

    <div class="dashboard-grid">
      <div class="panel-section">
        <h3>📚 دوره‌های فعال</h3>
        <div v-if="activeCourses.length" class="course-list">
          <div v-for="c in activeCourses" :key="c.id" class="course-item">
            <div class="course-info">
              <strong>{{ c.course_title }}</strong>
              <span class="text-muted">{{ c.instructor_name }}</span>
            </div>
            <div class="course-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: (c.progress || 0) + '%' }"></div>
              </div>
              <span class="progress-text">{{ c.progress || 0 }}%</span>
            </div>
          </div>
        </div>
        <p v-else class="empty-text">هنوز در دوره‌ای ثبت‌نام نکرده‌اید.</p>
      </div>

      <div class="panel-section">
        <h3>📝 آخرین نمرات</h3>
        <div v-if="recentGrades.length" class="grade-list">
          <div v-for="g in recentGrades" :key="g.id" class="grade-item">
            <span class="grade-course">{{ g.course_title }}</span>
            <span class="grade-score" :class="gradeClass(g.score)">{{ g.score }}</span>
          </div>
        </div>
        <p v-else class="empty-text">هنوز نمره‌ای ثبت نشده.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import api from "@/services/api";

export default {
  name: "StudentDashboard",
  data() {
    return {
      stats: {},
      activeCourses: [],
      recentGrades: [],
    };
  },
  computed: {
    ...mapGetters("auth", ["currentUser"]),
    userLabel() {
      return this.currentUser ? this.currentUser.first_name || this.currentUser.username : "";
    },
    greeting() {
      const h = new Date().getHours();
      if (h < 12) return "صبح بخیر";
      if (h < 18) return "عصر بخیر";
      return "شب بخیر";
    },
  },
  methods: {
    gradeClass(score) {
      if (score >= 17) return "grade-excellent";
      if (score >= 14) return "grade-good";
      if (score >= 10) return "grade-average";
      return "grade-low";
    },
  },
  async mounted() {
    try {
      const [statsRes, coursesRes, gradesRes] = await Promise.all([
        api.get("/auth/me/").catch(() => ({ data: {} })),
        api.get("/enrollments/my-enrollments/").catch(() => ({ data: [] })),
        api.get("/grades/my-grades/").catch(() => ({ data: [] })),
      ]);
      this.activeCourses = Array.isArray(coursesRes.data) ? coursesRes.data.slice(0, 5) : [];
      this.recentGrades = Array.isArray(gradesRes.data) ? gradesRes.data.slice(0, 5) : [];
      this.stats = {
        enrolled_courses: this.activeCourses.length,
        certificates: 0,
        artworks: 0,
        average_grade: this.recentGrades.length
          ? (this.recentGrades.reduce((s, g) => s + (g.score || 0), 0) / this.recentGrades.length).toFixed(1)
          : "—",
      };
    } catch { /* silent */ }
  },
};
</script>

<style scoped>
.student-dashboard { max-width: 1100px; }
.welcome-card {
  background: linear-gradient(135deg, #1a2f1e, #2d5a3f);
  color: #fff; border-radius: 14px; padding: 28px 32px; margin-bottom: 24px;
}
.welcome-text h2 { margin: 0 0 6px; font-size: 1.3rem; }
.welcome-text p { margin: 0; opacity: 0.75; font-size: 0.9rem; }
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 28px; }
.stat-card {
  background: #fff; border-radius: 12px; padding: 20px; text-align: center;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06); border-top: 3px solid #ccc;
}
.sc-courses { border-top-color: #3498db; }
.sc-grades { border-top-color: #f39c12; }
.sc-certs { border-top-color: #27ae60; }
.sc-gallery { border-top-color: #9b59b6; }
.stat-icon { font-size: 1.8rem; margin-bottom: 8px; }
.stat-value { font-size: 1.6rem; font-weight: 900; color: #1a2f1e; }
.stat-label { font-size: 0.82rem; color: #888; margin-top: 4px; }
.dashboard-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.panel-section {
  background: #fff; border-radius: 12px; padding: 22px; box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.panel-section h3 { margin: 0 0 16px; font-size: 1rem; color: #1a2f1e; }
.course-item { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #f0f0f0; }
.course-item:last-child { border-bottom: none; }
.course-info { display: flex; flex-direction: column; gap: 4px; }
.course-info strong { font-size: 0.9rem; }
.course-progress { display: flex; align-items: center; gap: 10px; min-width: 140px; }
.progress-bar { flex: 1; height: 6px; background: #eee; border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #27ae60, #2ecc71); border-radius: 3px; }
.progress-text { font-size: 0.78rem; font-weight: 700; color: #27ae60; min-width: 32px; }
.grade-item { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f0f0f0; }
.grade-item:last-child { border-bottom: none; }
.grade-course { font-size: 0.88rem; }
.grade-score { font-weight: 900; padding: 2px 10px; border-radius: 12px; font-size: 0.82rem; }
.grade-excellent { background: #d5f5e3; color: #1e8449; }
.grade-good { background: #d6eaf8; color: #2874a6; }
.grade-average { background: #fdebd0; color: #d68910; }
.grade-low { background: #fadbd8; color: #c0392b; }
.empty-text { color: #999; font-size: 0.88rem; text-align: center; padding: 20px; }
.text-muted { font-size: 0.78rem; color: #999; }
@media (max-width: 768px) { .dashboard-grid { grid-template-columns: 1fr; } }
</style>
