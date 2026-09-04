<template>
  <div class="instructor-students">
    <h2>👥 دانشجویان</h2>
    <div class="filter-bar">
      <select v-model="selectedCourse" class="filter-select">
        <option value="">همه دوره‌ها</option>
        <option v-for="c in courses" :key="c.id" :value="c.id">{{ c.title }}</option>
      </select>
    </div>
    <div v-if="filtered.length" class="students-table-wrapper">
      <table class="students-table">
        <thead>
          <tr>
            <th>نام</th>
            <th>ایمیل</th>
            <th>دوره</th>
            <th>تاریخ ثبت‌نام</th>
            <th>وضعیت</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in filtered" :key="s.id">
            <td>{{ s.student_name }}</td>
            <td>{{ s.student_email }}</td>
            <td>{{ s.course_title }}</td>
            <td>{{ formatDate(s.enrolled_at) }}</td>
            <td>
              <span class="status-badge" :class="'status-' + (s.status || 'active')">
                {{ s.status === 'completed' ? 'تکمیل' : 'فعال' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-else class="empty">دانشجویی یافت نشد.</p>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "InstructorStudents",
  data() {
    return { students: [], courses: [], selectedCourse: "" };
  },
  computed: {
    filtered() {
      if (!this.selectedCourse) return this.students;
      return this.students.filter(s => s.course_id == this.selectedCourse);
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
      const [studentsRes, coursesRes] = await Promise.all([
        api.get("/enrollments/instructor-students/").catch(() => ({ data: [] })),
        api.get("/courses/my-courses/").catch(() => ({ data: [] })),
      ]);
      this.students = Array.isArray(studentsRes.data) ? studentsRes.data : [];
      this.courses = Array.isArray(coursesRes.data) ? coursesRes.data : [];
    } catch { /* silent */ }
  },
};
</script>

<style scoped>
.instructor-students h2 { margin-bottom: 16px; color: #1a2f1e; }
.filter-bar { margin-bottom: 16px; }
.filter-select {
  padding: 8px 16px; border: 1px solid #ddd; border-radius: 8px;
  font-family: inherit; font-size: 0.85rem;
}
.students-table-wrapper { background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.students-table { width: 100%; border-collapse: collapse; }
.students-table th { background: #f8f9fa; padding: 12px 16px; text-align: right; font-size: 0.82rem; color: #666; }
.students-table td { padding: 12px 16px; border-bottom: 1px solid #f0f0f0; font-size: 0.85rem; }
.status-badge { font-size: 0.75rem; font-weight: 700; padding: 3px 10px; border-radius: 10px; }
.status-active { background: #d5f5e3; color: #1e8449; }
.status-completed { background: #d6eaf8; color: #2874a6; }
.empty { color: #999; text-align: center; padding: 40px; }
</style>
