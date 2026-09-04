<template>
  <div class="student-courses">
    <h2>📚 دوره‌های من</h2>
    <div class="filter-bar">
      <button v-for="f in filters" :key="f.key" :class="['filter-btn', { active: activeFilter === f.key }]" @click="activeFilter = f.key">
        {{ f.label }}
      </button>
    </div>
    <div v-if="filtered.length" class="courses-grid">
      <div v-for="c in filtered" :key="c.id" class="course-card">
        <div class="course-status" :class="'status-' + (c.status || 'active')">
          {{ statusLabel(c.status) }}
        </div>
        <h3>{{ c.course_title }}</h3>
        <p class="text-muted">👨‍🏫 {{ c.instructor_name }}</p>
        <div class="course-progress">
          <div class="progress-bar"><div class="progress-fill" :style="{ width: (c.progress || 0) + '%' }"></div></div>
          <span>{{ c.progress || 0 }}%</span>
        </div>
        <router-link :to="'/courses/' + c.course + '/' + c.course_slug" class="btn-detail">مشاهده دوره</router-link>
      </div>
    </div>
    <p v-else class="empty">هنوز در دوره‌ای ثبت‌نام نکرده‌اید.</p>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "StudentMyCourses",
  data() {
    return { courses: [], activeFilter: "all" };
  },
  computed: {
    filters() {
      return [
        { key: "all", label: "همه" },
        { key: "active", label: "در حال برگزاری" },
        { key: "completed", label: "تکمیل شده" },
      ];
    },
    filtered() {
      if (this.activeFilter === "all") return this.courses;
      return this.courses.filter(c => c.status === this.activeFilter);
    },
  },
  methods: {
    statusLabel(s) {
      return { active: "در حال برگزاری", completed: "تکمیل شده" }[s] || "فعال";
    },
  },
  async mounted() {
    try {
      const { data } = await api.get("/enrollments/my-enrollments/");
      this.courses = Array.isArray(data) ? data : [];
    } catch { /* silent */ }
  },
};
</script>

<style scoped>
.student-courses h2 { margin-bottom: 16px; color: #1a2f1e; }
.filter-bar { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
.filter-btn {
  padding: 7px 16px; border: 1px solid #ddd; border-radius: 20px;
  background: #fff; font-family: inherit; font-size: 0.82rem; cursor: pointer; transition: all 0.2s;
}
.filter-btn.active { background: #2d5a3f; color: #fff; border-color: #2d5a3f; }
.courses-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 18px; }
.course-card {
  background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); position: relative;
}
.course-status {
  position: absolute; top: 12px; left: 12px; font-size: 0.72rem; font-weight: 700;
  padding: 3px 10px; border-radius: 10px;
}
.status-active { background: #d5f5e3; color: #1e8449; }
.status-completed { background: #d6eaf8; color: #2874a6; }
.course-card h3 { margin: 0 0 8px; font-size: 0.95rem; }
.course-progress { display: flex; align-items: center; gap: 10px; margin: 12px 0; }
.progress-bar { flex: 1; height: 6px; background: #eee; border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #27ae60, #2ecc71); border-radius: 3px; }
.btn-detail {
  display: inline-block; padding: 8px 16px; background: #2d5a3f; color: #fff;
  border-radius: 8px; font-size: 0.82rem; text-decoration: none; font-weight: 600;
}
.text-muted { font-size: 0.82rem; color: #999; }
.empty { color: #999; text-align: center; padding: 40px; }
</style>
