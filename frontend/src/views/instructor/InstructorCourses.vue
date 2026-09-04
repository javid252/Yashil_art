<template>
  <div class="instructor-courses">
    <h2>📚 دوره‌های من</h2>
    <div v-if="courses.length" class="courses-list">
      <div v-for="c in courses" :key="c.id" class="course-card">
        <div class="course-header">
          <h3>{{ c.title }}</h3>
          <span class="course-status">{{ c.enrolled_count || 0 }} دانشجو</span>
        </div>
        <p class="text-muted">{{ c.category_name }} · {{ c.level_display }}</p>
        <div class="course-actions">
          <router-link :to="'/instructor/students?course=' + c.id" class="btn-sm">👥 دانشجویان</router-link>
          <router-link :to="'/instructor/grades?course=' + c.id" class="btn-sm">📝 نمرات</router-link>
          <router-link :to="'/instructor/attendance?course=' + c.id" class="btn-sm">📋 حضور و غیاب</router-link>
        </div>
      </div>
    </div>
    <p v-else class="empty">هنوز دوره‌ای به شما اختصاص داده نشده.</p>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "InstructorCourses",
  data() {
    return { courses: [] };
  },
  async mounted() {
    try {
      const { data } = await api.get("/courses/my-courses/");
      this.courses = Array.isArray(data) ? data : [];
    } catch { /* silent */ }
  },
};
</script>

<style scoped>
.instructor-courses h2 { margin-bottom: 16px; color: #1a2f1e; }
.courses-list { display: flex; flex-direction: column; gap: 14px; }
.course-card {
  background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.course-header { display: flex; justify-content: space-between; align-items: center; }
.course-header h3 { margin: 0; font-size: 1rem; }
.course-status { font-size: 0.78rem; background: #f0e6ff; color: #6c3483; padding: 3px 12px; border-radius: 10px; }
.text-muted { font-size: 0.82rem; color: #999; margin: 6px 0 12px; }
.course-actions { display: flex; gap: 8px; flex-wrap: wrap; }
.btn-sm {
  padding: 6px 14px; border: 1px solid #ddd; border-radius: 8px;
  font-size: 0.8rem; text-decoration: none; color: #333; background: #fafafa; transition: all 0.2s;
}
.btn-sm:hover { background: #2d5a3f; color: #fff; border-color: #2d5a3f; }
.empty { color: #999; text-align: center; padding: 40px; }
</style>
