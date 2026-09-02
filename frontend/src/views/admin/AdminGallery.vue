<template>
  <div class="admin-page">
    <div class="page-header">
      <h1>🖼️ مدیریت گالری</h1>
      <button class="btn btn-primary" @click="showForm = true">+ اثر جدید</button>
    </div>

    <div class="table-wrapper">
      <table class="admin-table">
        <thead>
          <tr>
            <th>اثر</th>
            <th>هنرمند</th>
            <th>تکنیک</th>
            <th>دسته‌بندی</th>
            <th>لایک</th>
            <th>بازدید</th>
            <th>قابل فروش</th>
            <th>عملیات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="art in artworks" :key="art.id">
            <td>
              <div class="art-cell">
                <img v-if="art.image" :src="art.image" class="art-thumb" />
                <strong>{{ art.title }}</strong>
              </div>
            </td>
            <td>{{ art.artist_name }}</td>
            <td>{{ art.medium_display }}</td>
            <td>{{ art.category_name || '-' }}</td>
            <td>❤️ {{ art.likes_count }}</td>
            <td>👁 {{ art.views_count }}</td>
            <td>{{ art.is_for_sale ? (art.is_sold ? 'فروخته شده' : '✅') : '—' }}</td>
            <td>
              <button class="btn-sm btn-outline">ویرایش</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="!artworks.length" class="empty">اثری یافت نشد</div>
  </div>
</template>

<script>
import api from "@/services/api";
export default {
  name: "AdminGallery",
  data() { return { artworks: [], showForm: false }; },
  methods: {
    async loadArtworks() {
      try { const { data } = await api.get("/gallery/artworks/"); this.artworks = data.results || data; } catch (e) {}
    },
  },
  created() { this.loadArtworks(); },
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
.art-cell { display: flex; align-items: center; gap: 10px; }
.art-thumb { width: 40px; height: 40px; border-radius: 6px; object-fit: cover; }
.btn-sm { padding: 4px 12px; font-size: 0.8rem; }
.btn-outline { border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; }
.btn-primary { background: #6c5ce7; color: white; border: none; padding: 8px 20px; border-radius: 6px; font-weight: 600; cursor: pointer; }
.empty { text-align: center; padding: 40px; color: #999; }
</style>
