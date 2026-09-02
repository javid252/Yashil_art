<template>
  <div class="admin-page">
    <div class="page-header">
      <h1>📚 مدیریت دوره‌ها</h1>
      <button class="btn btn-primary" @click="showForm = true">+ دوره جدید</button>
    </div>

    <!-- Filters -->
    <div class="filters">
      <input v-model="search" @input="loadCourses" placeholder="جستجو..." class="filter-input" />
      <select v-model="statusFilter" @change="loadCourses" class="filter-select">
        <option value="">همه وضعیت‌ها</option>
        <option value="draft">پیش‌نویس</option>
        <option value="published">منتشر شده</option>
        <option value="archived">بایگانی</option>
      </select>
    </div>

    <!-- Table -->
    <div class="table-wrapper">
      <table class="admin-table">
        <thead>
          <tr>
            <th>عنوان</th>
            <th>دسته‌بندی</th>
            <th>استاد</th>
            <th>سطح</th>
            <th>قیمت</th>
            <th>ظرفیت</th>
            <th>وضعیت</th>
            <th>عملیات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="course in courses" :key="course.id">
            <td><strong>{{ course.title }}</strong></td>
            <td>{{ course.category_name || '-' }}</td>
            <td>{{ course.instructor_name || '-' }}</td>
            <td>{{ course.level_display }}</td>
            <td>{{ formatPrice(course.price) }} تومان</td>
            <td>{{ course.enrolled_count }}/{{ course.max_students }}</td>
            <td>
              <span class="status-badge" :class="`status-${course.status}`">{{ statusLabel(course.status) }}</span>
            </td>
            <td>
              <button class="btn-sm btn-outline" @click="editCourse(course)">ویرایش</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="!courses.length" class="empty">دوره‌ای یافت نشد</div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "AdminCourses",
  data() {
    return {
      courses: [],
      search: "",
      statusFilter: "",
      showForm: false,
    };
  },
  methods: {
    formatPrice(p) {
      return p ? new Intl.NumberFormat("fa-IR").format(p) : "0";
    },
    statusLabel(s) {
      return { draft: "پیش‌نویس", published: "منتشر شده", archived: "بایگانی" }[s] || s;
    },
    editCourse(course) {
      // TODO: Open edit modal
      console.log("Edit:", course);
    },
    async loadCourses() {
      try {
        const params = {};
        if (this.search) params.search = this.search;
        if (this.statusFilter) params.status = this.statusFilter;
        const { data } = await api.get("/courses/", { params });
        this.courses = data.results || data;
      } catch (e) { console.error(e); }
    },
  },
  created() {
    this.loadCourses();
  },
};
</script>

<style scoped>
.admin-page { padding: 0; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.page-header h1 { font-size: 1.4rem; }

.filters { display: flex; gap: 12px; margin-bottom: 20px; }
.filter-input, .filter-select {
  padding: 8px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
  font-size: 0.88rem;
}
.filter-input { flex: 1; max-width: 300px; }

.table-wrapper { overflow-x: auto; }
.admin-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}
.admin-table th, .admin-table td {
  padding: 12px 16px;
  text-align: right;
  border-bottom: 1px solid #eee;
  font-size: 0.88rem;
}
.admin-table th { background: #f8f9fa; font-weight: 700; color: #555; }
.admin-table tr:hover { background: #f8f9fa; }

.status-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}
.status-draft { background: #fff3cd; color: #856404; }
.status-published { background: #d4edda; color: #155724; }
.status-archived { background: #e2e3e5; color: #383d41; }

.btn-sm { padding: 4px 12px; font-size: 0.8rem; }
.btn-outline { border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; }
.btn-outline:hover { border-color: #6c5ce7; color: #6c5ce7; }
.btn-primary { background: #6c5ce7; color: white; border: none; padding: 8px 20px; border-radius: 6px; font-weight: 600; cursor: pointer; }

.empty { text-align: center; padding: 40px; color: #999; }
</style>
