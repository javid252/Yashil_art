<template>
  <div class="admin-page">
    <div class="page-header">
      <h1>👨‍🏫 مدیریت اساتید</h1>
      <button class="btn btn-primary" @click="showForm = true">+ استاد جدید</button>
    </div>

    <div class="table-wrapper">
      <table class="admin-table">
        <thead>
          <tr>
            <th>نام</th>
            <th>تخصص‌ها</th>
            <th>تجربه</th>
            <th>دانشجو</th>
            <th>امتیاز</th>
            <th>ویژه</th>
            <th>عملیات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="inst in instructors" :key="inst.id">
            <td><strong>{{ inst.display_name }}</strong></td>
            <td>
              <span v-for="s in (inst.specializations || []).slice(0, 2)" :key="s" class="tag">{{ s }}</span>
            </td>
            <td>{{ inst.years_experience }} سال</td>
            <td>{{ inst.students_count }}</td>
            <td>⭐ {{ inst.rating }}</td>
            <td>{{ inst.is_featured ? '✅' : '—' }}</td>
            <td>
              <button class="btn-sm btn-outline">ویرایش</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="!instructors.length" class="empty">استادی یافت نشد</div>
  </div>
</template>

<script>
import api from "@/services/api";
export default {
  name: "AdminInstructors",
  data() { return { instructors: [], showForm: false }; },
  methods: {
    async loadInstructors() {
      try { const { data } = await api.get("/instructors/"); this.instructors = data.results || data; } catch (e) {}
    },
  },
  created() { this.loadInstructors(); },
};
</script>

<style scoped>
.admin-page { padding: 0; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.page-header h1 { font-size: 1.4rem; }
.table-wrapper { overflow-x: auto; }
.admin-table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; }
.admin-table th, .admin-table td { padding: 12px 16px; text-align: right; border-bottom: 1px solid #eee; font-size: 0.88rem; }
.admin-table th { background: #f8f9fa; font-weight: 700; color: #555; }
.tag { display: inline-block; background: #f0f0f0; padding: 2px 8px; border-radius: 8px; font-size: 0.72rem; margin-left: 4px; }
.btn-sm { padding: 4px 12px; font-size: 0.8rem; }
.btn-outline { border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; }
.btn-primary { background: #6c5ce7; color: white; border: none; padding: 8px 20px; border-radius: 6px; font-weight: 600; cursor: pointer; }
.empty { text-align: center; padding: 40px; color: #999; }
</style>
