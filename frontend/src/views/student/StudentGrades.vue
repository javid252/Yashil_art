<template>
  <div class="student-grades">
    <h2>📝 نمرات من</h2>
    <div v-if="grades.length" class="grades-table-wrapper">
      <table class="grades-table">
        <thead>
          <tr>
            <th>دوره</th>
            <th>تاریخ</th>
            <th>نمره</th>
            <th>وضعیت</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="g in grades" :key="g.id">
            <td>{{ g.course_title }}</td>
            <td>{{ formatDate(g.created_at) }}</td>
            <td><span class="score-badge" :class="gradeClass(g.score)">{{ g.score }}</span></td>
            <td>{{ g.passed ? '✅ قبول' : '❌ مردود' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-else class="empty">هنوز نمره‌ای ثبت نشده.</p>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "StudentGrades",
  data() {
    return { grades: [] };
  },
  methods: {
    gradeClass(score) {
      if (score >= 17) return "excellent";
      if (score >= 14) return "good";
      if (score >= 10) return "average";
      return "low";
    },
    formatDate(d) {
      if (!d) return "—";
      return new Date(d).toLocaleDateString("fa-IR");
    },
  },
  async mounted() {
    try {
      const { data } = await api.get("/grades/my-grades/");
      this.grades = Array.isArray(data) ? data : [];
    } catch { /* silent */ }
  },
};
</script>

<style scoped>
.student-grades h2 { margin-bottom: 16px; color: #1a2f1e; }
.grades-table-wrapper { background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.05); }
.grades-table { width: 100%; border-collapse: collapse; }
.grades-table th { background: #f8f9fa; padding: 12px 16px; text-align: right; font-size: 0.82rem; color: #666; border-bottom: 2px solid #eee; }
.grades-table td { padding: 12px 16px; border-bottom: 1px solid #f0f0f0; font-size: 0.88rem; }
.score-badge { font-weight: 900; padding: 3px 12px; border-radius: 10px; font-size: 0.82rem; }
.excellent { background: #d5f5e3; color: #1e8449; }
.good { background: #d6eaf8; color: #2874a6; }
.average { background: #fdebd0; color: #d68910; }
.low { background: #fadbd8; color: #c0392b; }
.empty { color: #999; text-align: center; padding: 40px; }
</style>
