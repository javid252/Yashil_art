<template>
  <div class="student-dashboard container">
    <div class="page-header">
      <h1>پنل دانشجو</h1>
      <p>خوش آمدید، {{ userDisplay }}</p>
    </div>

    <!-- Tabs -->
    <div class="tabs">
      <button :class="{ active: activeTab === 'courses' }" @click="activeTab = 'courses'">📚 دوره‌های من</button>
      <button :class="{ active: activeTab === 'grades' }" @click="activeTab = 'grades'">📊 نمرات</button>
      <button :class="{ active: activeTab === 'certificates' }" @click="activeTab = 'certificates'">📜 گواهینامه‌ها</button>
      <button :class="{ active: activeTab === 'workshops' }" @click="activeTab = 'workshops'">🎪 کارگاه‌ها</button>
    </div>

    <!-- Courses Tab -->
    <div v-if="activeTab === 'courses'" class="tab-content">
      <div v-if="enrollmentsLoading" class="loading">در حال بارگذاری...</div>
      <div v-else-if="enrollments.length" class="enrollments-grid">
        <div v-for="e in enrollments" :key="e.id" class="enrollment-card">
          <div class="enrollment-thumb">
            <img v-if="e.course_thumbnail" :src="e.course_thumbnail" :alt="e.course_title" />
            <div v-else class="thumb-placeholder">🎨</div>
          </div>
          <div class="enrollment-info">
            <h3>{{ e.course_title }}</h3>
            <span class="badge" :class="statusClass(e.status)">{{ e.status_display }}</span>
            <span class="enrollment-date">ثبت‌نام: {{ formatDate(e.enrolled_at) }}</span>
            <router-link :to="`/courses/${e.course}`" class="btn btn-sm btn-outline">مشاهده دوره</router-link>
          </div>
        </div>
      </div>
      <div v-else class="empty-state">
        <div class="icon">📚</div>
        <p>هنوز در دوره‌ای ثبت‌نام نکرده‌اید</p>
        <router-link to="/courses" class="btn btn-primary">مشاهده دوره‌ها</router-link>
      </div>
    </div>

    <!-- Grades Tab -->
    <div v-if="activeTab === 'grades'" class="tab-content">
      <div v-if="gradesLoading" class="loading">در حال بارگذاری...</div>
      <div v-else-if="grades.length" class="grades-table-wrapper">
        <table class="grades-table">
          <thead>
            <tr>
              <th>دوره</th>
              <th>ارزیابی</th>
              <th>نمره</th>
              <th>درصد</th>
              <th>تاریخ</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="g in grades" :key="g.id">
              <td>{{ g.assessment_title }}</td>
              <td>{{ g.assessment_title }}</td>
              <td><strong>{{ g.score }}</strong></td>
              <td>{{ g.percentage }}٪</td>
              <td>{{ formatDate(g.graded_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="empty-state">
        <div class="icon">📊</div>
        <p>نمره‌ای ثبت نشده</p>
      </div>
    </div>

    <!-- Certificates Tab -->
    <div v-if="activeTab === 'certificates'" class="tab-content">
      <div v-if="certsLoading" class="loading">در حال بارگذاری...</div>
      <div v-else-if="certificates.length" class="certs-grid">
        <div v-for="c in certificates" :key="c.id" class="cert-card">
          <div class="cert-icon">📜</div>
          <div class="cert-info">
            <h3>{{ c.course_name }}</h3>
            <p>شماره: {{ c.certificate_number }}</p>
            <p>تاریخ صدور: {{ c.issued_date }}</p>
            <p v-if="c.grade">نمره: {{ c.grade }}</p>
            <router-link :to="`/certificates/${c.id}`" class="btn btn-sm btn-outline">مشاهده گواهینامه</router-link>
          </div>
        </div>
      </div>
      <div v-else class="empty-state">
        <div class="icon">📜</div>
        <p>گواهینامه‌ای صادر نشده</p>
      </div>
    </div>

    <!-- Workshops Tab -->
    <div v-if="activeTab === 'workshops'" class="tab-content">
      <div v-if="wsLoading" class="loading">در حال بارگذاری...</div>
      <div v-else-if="workshops.length" class="workshops-list">
        <div v-for="ws in workshops" :key="ws.id" class="workshop-item">
          <span class="ws-title">{{ ws.workshop_title }}</span>
          <span class="badge" :class="statusClass(ws.status)">{{ ws.status_display }}</span>
          <span class="ws-date">{{ formatDate(ws.registered_at) }}</span>
        </div>
      </div>
      <div v-else class="empty-state">
        <div class="icon">🎪</div>
        <p>در کارگاهی ثبت‌نام نکرده‌اید</p>
        <router-link to="/workshops" class="btn btn-primary">مشاهده کارگاه‌ها</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import { mapGetters } from "vuex";

export default {
  name: "StudentDashboard",
  data() {
    return {
      activeTab: "courses",
      enrollments: [],
      enrollmentsLoading: true,
      grades: [],
      gradesLoading: true,
      certificates: [],
      certsLoading: true,
      workshops: [],
      wsLoading: true,
    };
  },
  computed: {
    ...mapGetters("auth", ["currentUser"]),
    userDisplay() {
      return this.currentUser?.first_name || this.currentUser?.username || "";
    },
  },
  watch: {
    activeTab(tab) {
      if (tab === "courses" && !this.enrollments.length) this.loadEnrollments();
      if (tab === "grades" && !this.grades.length) this.loadGrades();
      if (tab === "certificates" && !this.certificates.length) this.loadCertificates();
      if (tab === "workshops" && !this.workshops.length) this.loadWorkshops();
    },
  },
  methods: {
    formatDate(d) {
      if (!d) return "";
      return new Date(d).toLocaleDateString("fa-IR");
    },
    statusClass(status) {
      return {
        "badge-active": status === "active",
        "badge-completed": status === "completed",
        "badge-pending": status === "pending",
        "badge-cancelled": status === "cancelled",
      };
    },
    async loadEnrollments() {
      this.enrollmentsLoading = true;
      try {
        const { data } = await api.get("/enrollments/my/");
        this.enrollments = data.results || data;
      } catch (e) { console.error(e); }
      finally { this.enrollmentsLoading = false; }
    },
    async loadGrades() {
      this.gradesLoading = true;
      try {
        const { data } = await api.get("/grades/my/");
        this.grades = data.results || data;
      } catch (e) { console.error(e); }
      finally { this.gradesLoading = false; }
    },
    async loadCertificates() {
      this.certsLoading = true;
      try {
        const { data } = await api.get("/certificates/my/");
        this.certificates = data.results || data;
      } catch (e) { console.error(e); }
      finally { this.certsLoading = false; }
    },
    async loadWorkshops() {
      this.wsLoading = true;
      try {
        const { data } = await api.get("/workshops/my/");
        this.workshops = data.results || data;
      } catch (e) { console.error(e); }
      finally { this.wsLoading = false; }
    },
  },
  created() {
    this.loadEnrollments();
  },
};
</script>

<style scoped>
.student-dashboard { padding: 40px 20px 60px; }
.page-header { margin-bottom: 30px; }
.page-header h1 { font-size: 1.8rem; }
.page-header p { color: var(--color-text-muted); margin-top: 8px; }

.tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 30px;
  border-bottom: 2px solid var(--color-border);
  padding-bottom: 0;
  flex-wrap: wrap;
}

.tabs button {
  padding: 12px 20px;
  border: none;
  background: none;
  font-family: inherit;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-text-muted);
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s;
}

.tabs button.active {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}

.tab-content { min-height: 200px; }
.loading { text-align: center; padding: 40px; color: var(--color-text-muted); }

.enrollments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 20px;
}

.enrollment-card {
  display: flex;
  gap: 16px;
  padding: 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  background: var(--color-surface);
}

.enrollment-thumb {
  width: 100px;
  height: 100px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  flex-shrink: 0;
  background: var(--color-sand);
}

.enrollment-thumb img { width: 100%; height: 100%; object-fit: cover; }
.thumb-placeholder { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 2rem; }

.enrollment-info h3 { font-size: 1rem; margin-bottom: 6px; }
.enrollment-date { display: block; font-size: 0.8rem; color: var(--color-text-muted); margin-top: 8px; }

.badge-active { background: #e4f0ec; color: #2e6b5e; }
.badge-completed { background: #e6eef7; color: #2b5a8f; }
.badge-pending { background: #fdf1de; color: #a86a1c; }
.badge-cancelled { background: #f8e6e2; color: #b3452c; }

.grades-table-wrapper { overflow-x: auto; }
.grades-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-surface);
  border-radius: var(--radius);
  overflow: hidden;
}

.grades-table th, .grades-table td {
  padding: 12px 16px;
  text-align: right;
  border-bottom: 1px solid var(--color-border);
  font-size: 0.88rem;
}

.grades-table th {
  background: var(--color-bg);
  font-weight: 700;
  color: var(--color-text-muted);
}

.certs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.cert-card {
  display: flex;
  gap: 16px;
  padding: 20px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  background: var(--color-surface);
}

.cert-icon { font-size: 2.5rem; }
.cert-info h3 { font-size: 1rem; margin-bottom: 6px; }
.cert-info p { font-size: 0.82rem; color: var(--color-text-muted); margin-bottom: 4px; }

.workshop-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 0;
  border-bottom: 1px solid var(--color-border);
}

.ws-title { font-weight: 600; flex: 1; }
.ws-date { font-size: 0.82rem; color: var(--color-text-muted); }
</style>
