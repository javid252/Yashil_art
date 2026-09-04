<template>
  <div class="instructor-dashboard">
    <div class="welcome-card">
      <div class="welcome-text">
        <h2>{{ greeting }}، {{ userLabel }} 👋</h2>
        <p>خوش آمدید به پنل استادی یاشیل آرت</p>
      </div>
    </div>

    <div class="stat-grid">
      <div class="stat-card sc-courses">
        <div class="stat-icon">📚</div>
        <div class="stat-value">{{ stats.courses || 0 }}</div>
        <div class="stat-label">دوره فعال</div>
      </div>
      <div class="stat-card sc-students">
        <div class="stat-icon">👥</div>
        <div class="stat-value">{{ stats.students || 0 }}</div>
        <div class="stat-label">دانشجو</div>
      </div>
      <div class="stat-card sc-pending">
        <div class="stat-icon">📝</div>
        <div class="stat-value">{{ stats.pending_grades || 0 }}</div>
        <div class="stat-label">نمره ثبت نشده</div>
      </div>
      <div class="stat-card sc-certs">
        <div class="stat-icon">🏆</div>
        <div class="stat-value">{{ stats.certificates || 0 }}</div>
        <div class="stat-label">گواهینامه صادر شده</div>
      </div>
    </div>

    <div class="dashboard-grid">
      <div class="panel-section">
        <h3>📚 دوره‌های فعال</h3>
        <div v-if="courses.length" class="item-list">
          <div v-for="c in courses" :key="c.id" class="item-row">
            <span class="item-title">{{ c.title }}</span>
            <span class="item-badge">{{ c.enrolled_count || 0 }} دانشجو</span>
          </div>
        </div>
        <p v-else class="empty-text">هنوز دوره‌ای ندارید.</p>
      </div>

      <div class="panel-section">
        <h3>⏰ آخرین فعالیت‌ها</h3>
        <div v-if="recentActivity.length" class="item-list">
          <div v-for="a in recentActivity" :key="a.id" class="item-row">
            <span class="item-title">{{ a.description }}</span>
            <span class="item-date">{{ formatDate(a.date) }}</span>
          </div>
        </div>
        <p v-else class="empty-text">فعالیتی ثبت نشده.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import api from "@/services/api";

export default {
  name: "InstructorDashboard",
  data() {
    return { stats: {}, courses: [], recentActivity: [] };
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
    formatDate(d) {
      if (!d) return "—";
      return new Date(d).toLocaleDateString("fa-IR");
    },
  },
  async mounted() {
    try {
      const [coursesRes, studentsRes] = await Promise.all([
        api.get("/courses/my-courses/").catch(() => ({ data: [] })),
        api.get("/enrollments/instructor-students/").catch(() => ({ data: [] })),
      ]);
      this.courses = Array.isArray(coursesRes.data) ? coursesRes.data : [];
      const students = Array.isArray(studentsRes.data) ? studentsRes.data : [];
      this.stats = {
        courses: this.courses.length,
        students: students.length,
        pending_grades: 0,
        certificates: 0,
      };
    } catch { /* silent */ }
  },
};
</script>

<style scoped>
.instructor-dashboard { max-width: 1100px; }
.welcome-card {
  background: linear-gradient(135deg, #2d1a4e, #4a2c7a);
  color: #fff; border-radius: 14px; padding: 28px 32px; margin-bottom: 24px;
}
.welcome-text h2 { margin: 0 0 6px; font-size: 1.3rem; }
.welcome-text p { margin: 0; opacity: 0.75; font-size: 0.9rem; }
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 28px; }
.stat-card {
  background: #fff; border-radius: 12px; padding: 20px; text-align: center;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06); border-top: 3px solid #ccc;
}
.sc-courses { border-top-color: #8e44ad; }
.sc-students { border-top-color: #3498db; }
.sc-pending { border-top-color: #e67e22; }
.sc-certs { border-top-color: #27ae60; }
.stat-icon { font-size: 1.8rem; margin-bottom: 8px; }
.stat-value { font-size: 1.6rem; font-weight: 900; color: #1a2f1e; }
.stat-label { font-size: 0.82rem; color: #888; margin-top: 4px; }
.dashboard-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.panel-section {
  background: #fff; border-radius: 12px; padding: 22px; box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.panel-section h3 { margin: 0 0 16px; font-size: 1rem; color: #1a2f1e; }
.item-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #f0f0f0; }
.item-row:last-child { border-bottom: none; }
.item-title { font-size: 0.88rem; }
.item-badge { font-size: 0.75rem; background: #f0e6ff; color: #6c3483; padding: 3px 10px; border-radius: 10px; }
.item-date { font-size: 0.78rem; color: #999; }
.empty-text { color: #999; font-size: 0.88rem; text-align: center; padding: 20px; }
@media (max-width: 768px) { .dashboard-grid { grid-template-columns: 1fr; } }
</style>
