<template>
  <div class="admin-page">
    <div class="page-header">
      <h1>🎪 مدیریت کارگاه‌ها</h1>
      <button class="btn btn-primary" @click="showForm = true">+ کارگاه جدید</button>
    </div>

    <div class="table-wrapper">
      <table class="admin-table">
        <thead>
          <tr>
            <th>عنوان</th>
            <th>دسته‌بندی</th>
            <th>مدرس</th>
            <th>نوع</th>
            <th>تاریخ شروع</th>
            <th>قیمت</th>
            <th>ثبت‌نام</th>
            <th>وضعیت</th>
            <th>عملیات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ws in workshops" :key="ws.id">
            <td><strong>{{ ws.title }}</strong></td>
            <td>{{ ws.category_name || '-' }}</td>
            <td>{{ ws.instructor_name || '-' }}</td>
            <td>{{ ws.duration_type_display }}</td>
            <td>{{ ws.start_date }}</td>
            <td>{{ formatPrice(ws.price) }} تومان</td>
            <td>{{ ws.enrolled_count }}/{{ ws.max_participants }}</td>
            <td>
              <span class="status-badge" :class="`ws-${ws.status}`">{{ ws.status_display }}</span>
            </td>
            <td>
              <button class="btn-sm btn-outline">ویرایش</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="!workshops.length" class="empty">کارگاهی یافت نشد</div>
  </div>
</template>

<script>
import api from "@/services/api";
export default {
  name: "AdminWorkshops",
  data() { return { workshops: [], showForm: false }; },
  methods: {
    formatPrice(p) { return p ? new Intl.NumberFormat("fa-IR").format(p) : "0"; },
    async loadWorkshops() {
      try { const { data } = await api.get("/workshops/"); this.workshops = data.results || data; } catch (e) {}
    },
  },
  created() { this.loadWorkshops(); },
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
.status-badge { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }
.ws-upcoming { background: #d1ecf1; color: #0c5460; }
.ws-ongoing { background: #d4edda; color: #155724; }
.ws-completed { background: #e2e3e5; color: #383d41; }
.ws-cancelled { background: #f8d7da; color: #721c24; }
.btn-sm { padding: 4px 12px; font-size: 0.8rem; }
.btn-outline { border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; }
.btn-primary { background: #6c5ce7; color: white; border: none; padding: 8px 20px; border-radius: 6px; font-weight: 600; cursor: pointer; }
.empty { text-align: center; padding: 40px; color: #999; }
</style>
