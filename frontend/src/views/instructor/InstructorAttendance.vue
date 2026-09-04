<template>
  <div class="instructor-attendance">
    <h2>📋 حضور و غیاب</h2>
    <div class="filter-bar">
      <select v-model="selectedCourse" class="filter-select" @change="loadStudents">
        <option value="">دوره را انتخاب کنید</option>
        <option v-for="c in courses" :key="c.id" :value="c.id">{{ c.title }}</option>
      </select>
      <input v-model="sessionDate" type="date" class="filter-input" />
    </div>
    <div v-if="students.length" class="attendance-list">
      <div v-for="s in students" :key="s.id" class="attendance-row">
        <span class="student-name">{{ s.student_name }}</span>
        <div class="attendance-options">
          <button :class="['att-btn', 'att-present', { active: attendance[s.id] === 'present' }]" @click="setAtt(s.id, 'present')">✅ حاضر</button>
          <button :class="['att-btn', 'att-absent', { active: attendance[s.id] === 'absent' }]" @click="setAtt(s.id, 'absent')">❌ غایب</button>
          <button :class="['att-btn', 'att-excused', { active: attendance[s.id] === 'excused' }]" @click="setAtt(s.id, 'excused')">🕐 مرخصی</button>
        </div>
      </div>
      <button class="btn-save" @click="saveAttendance" :disabled="!selectedCourse || !sessionDate">ذخیره</button>
    </div>
    <p v-else class="empty">دوره و تاریخ را انتخاب کنید.</p>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "InstructorAttendance",
  data() {
    return { courses: [], students: [], selectedCourse: "", sessionDate: "", attendance: {} };
  },
  methods: {
    setAtt(id, status) {
      this.attendance = { ...this.attendance, [id]: status };
    },
    async loadStudents() {
      if (!this.selectedCourse) return;
      try {
        const { data } = await api.get(`/enrollments/instructor-students/?course=${this.selectedCourse}`);
        this.students = Array.isArray(data) ? data : [];
      } catch { /* silent */ }
    },
    async saveAttendance() {
      try {
        await api.post("/attendance/bulk-create/", {
          course_id: this.selectedCourse,
          date: this.sessionDate,
          records: Object.entries(this.attendance).map(([student_id, status]) => ({ student_id, status })),
        });
        alert("حضور و غیاب با موفقیت ذخیره شد.");
      } catch { /* silent */ }
    },
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
.instructor-attendance h2 { margin-bottom: 16px; color: #1a2f1e; }
.filter-bar { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.filter-select, .filter-input { padding: 8px 14px; border: 1px solid #ddd; border-radius: 8px; font-family: inherit; font-size: 0.85rem; }
.attendance-list { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.attendance-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 12px 0; border-bottom: 1px solid #f0f0f0;
}
.attendance-row:last-child { border-bottom: none; }
.student-name { font-weight: 600; font-size: 0.9rem; }
.attendance-options { display: flex; gap: 6px; }
.att-btn { padding: 6px 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 0.78rem; cursor: pointer; background: #fff; transition: all 0.2s; }
.att-present.active { background: #d5f5e3; border-color: #27ae60; }
.att-absent.active { background: #fadbd8; border-color: #e74c3c; }
.att-excused.active { background: #fef9e7; border-color: #f39c12; }
.btn-save {
  margin-top: 16px; padding: 10px 24px; background: #2d5a3f; color: #fff;
  border: none; border-radius: 8px; font-family: inherit; font-size: 0.88rem; cursor: pointer;
}
.btn-save:disabled { opacity: 0.5; }
.empty { color: #999; text-align: center; padding: 40px; }
</style>
