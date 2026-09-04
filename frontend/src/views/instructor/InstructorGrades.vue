<template>
  <div class="instructor-grades">
    <h2>📝 ثبت نمرات</h2>
    <div class="filter-bar">
      <select v-model="selectedCourse" class="filter-select" @change="loadStudents">
        <option value="">دوره را انتخاب کنید</option>
        <option v-for="c in courses" :key="c.id" :value="c.id">{{ c.title }}</option>
      </select>
    </div>
    <div v-if="students.length" class="grades-form">
      <div v-for="s in students" :key="s.id" class="grade-row">
        <span class="student-name">{{ s.student_name }}</span>
        <input v-model="grades[s.id]" type="number" min="0" max="20" class="grade-input" placeholder="نمره" />
        <input v-model="comments[s.id]" type="text" class="comment-input" placeholder="توضیح (اختیاری)" />
      </div>
      <button class="btn-save" @click="saveGrades" :disabled="!selectedCourse">ذخیره نمرات</button>
    </div>
    <p v-else class="empty">دوره را انتخاب کنید.</p>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "InstructorGrades",
  data() {
    return { courses: [], students: [], selectedCourse: "", grades: {}, comments: {} };
  },
  methods: {
    async loadStudents() {
      if (!this.selectedCourse) return;
      try {
        const { data } = await api.get(`/enrollments/instructor-students/?course=${this.selectedCourse}`);
        this.students = Array.isArray(data) ? data : [];
      } catch { /* silent */ }
    },
    async saveGrades() {
      try {
        const records = Object.entries(this.grades)
          .filter(([, score]) => score)
          .map(([student_id, score]) => ({
            student_id,
            score: Number(score),
            comment: this.comments[student_id] || "",
          }));
        await api.post("/grades/bulk-create/", {
          course_id: this.selectedCourse,
          records,
        });
        alert("نمرات با موفقیت ذخیره شد.");
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
.instructor-grades h2 { margin-bottom: 16px; color: #1a2f1e; }
.filter-bar { margin-bottom: 16px; }
.filter-select { padding: 8px 16px; border: 1px solid #ddd; border-radius: 8px; font-family: inherit; font-size: 0.85rem; }
.grades-form { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.grade-row { display: flex; gap: 12px; align-items: center; padding: 10px 0; border-bottom: 1px solid #f0f0f0; }
.grade-row:last-child { border-bottom: none; }
.student-name { min-width: 140px; font-size: 0.88rem; font-weight: 600; }
.grade-input { width: 70px; padding: 6px 10px; border: 1px solid #ddd; border-radius: 6px; text-align: center; }
.comment-input { flex: 1; padding: 6px 10px; border: 1px solid #ddd; border-radius: 6px; font-family: inherit; font-size: 0.82rem; }
.btn-save {
  margin-top: 16px; padding: 10px 24px; background: #2d5a3f; color: #fff;
  border: none; border-radius: 8px; font-family: inherit; font-size: 0.88rem; cursor: pointer;
}
.btn-save:disabled { opacity: 0.5; }
.empty { color: #999; text-align: center; padding: 40px; }
</style>
