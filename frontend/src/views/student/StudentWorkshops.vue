<template>
  <div class="student-workshops">
    <h2>🎓 کارگاه‌های من</h2>
    <div v-if="workshops.length" class="workshops-grid">
      <div v-for="w in workshops" :key="w.id" class="workshop-card">
        <div class="ws-date">{{ formatDate(w.date) }}</div>
        <h3>{{ w.title }}</h3>
        <p class="ws-instructor">👨‍🏫 {{ w.instructor_name }}</p>
        <p class="ws-location">📍 {{ w.location || 'آنلاین' }}</p>
        <span class="ws-status" :class="'ws-' + (w.status || 'upcoming')">
          {{ w.status === 'completed' ? 'تکمیل شده' : 'پیش رو' }}
        </span>
      </div>
    </div>
    <p v-else class="empty">هنوز در کارگاهی شرکت نکرده‌اید.</p>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "StudentWorkshops",
  data() {
    return { workshops: [] };
  },
  methods: {
    formatDate(d) {
      if (!d) return "—";
      return new Date(d).toLocaleDateString("fa-IR");
    },
  },
  async mounted() {
    try {
      const { data } = await api.get("/workshops/my-workshops/");
      this.workshops = Array.isArray(data) ? data : [];
    } catch { /* silent */ }
  },
};
</script>

<style scoped>
.student-workshops h2 { margin-bottom: 16px; color: #1a2f1e; }
.workshops-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.workshop-card {
  background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); position: relative;
}
.ws-date { font-size: 0.75rem; color: #c9a96e; font-weight: 700; margin-bottom: 6px; }
.workshop-card h3 { margin: 0 0 8px; font-size: 0.95rem; }
.ws-instructor, .ws-location { font-size: 0.82rem; color: #888; margin: 3px 0; }
.ws-status {
  position: absolute; top: 14px; left: 14px; font-size: 0.72rem; font-weight: 700;
  padding: 3px 10px; border-radius: 10px;
}
.ws-upcoming { background: #fef9e7; color: #b7950b; }
.ws-completed { background: #d5f5e3; color: #1e8449; }
.empty { color: #999; text-align: center; padding: 40px; }
</style>
