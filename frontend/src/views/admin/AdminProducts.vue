<template>
  <div class="admin-products">
    <div class="page-head">
      <h1>محصولات</h1>
      <router-link to="/admin/products/new" class="btn btn-primary btn-sm">+ محصول جدید</router-link>
    </div>

    <div class="card table-card">
      <div class="table-toolbar">
        <input v-model="search" type="text" placeholder="جستجوی محصول..." @input="debouncedFetch" />
      </div>

      <AppLoader v-if="loading" />
      <table v-else class="admin-table">
        <thead>
          <tr>
            <th>نام</th>
            <th>دسته‌بندی</th>
            <th>قیمت</th>
            <th>موجودی</th>
            <th>وضعیت</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in products" :key="p.id">
            <td class="product-name-cell">{{ p.name }}</td>
            <td>{{ p.category_name || "—" }}</td>
            <td>{{ formatPrice(p.final_price) }}</td>
            <td :class="{ 'low-stock-text': p.stock <= 5 }">{{ p.stock != null ? p.stock : "—" }}</td>
            <td>
              <span class="badge" :class="p.in_stock ? 'badge-status-paid' : 'badge-status-cancelled'">
                {{ p.in_stock ? "موجود" : "ناموجود" }}
              </span>
            </td>
            <td class="actions-cell">
              <router-link :to="`/admin/products/${p.id}/edit`" class="btn btn-outline btn-sm">ویرایش</router-link>
              <button class="btn btn-danger btn-sm" @click="remove(p)">حذف</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="!loading && products.length === 0" class="text-muted empty-row">محصولی یافت نشد.</p>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

export default {
  name: "AdminProducts",
  components: { AppLoader },
  data() {
    return { products: [], loading: true, search: "", debounceTimer: null };
  },
  created() {
    this.fetchProducts();
  },
  methods: {
    formatPrice(v) {
      return Number(v).toLocaleString("fa-IR");
    },
    debouncedFetch() {
      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => this.fetchProducts(), 350);
    },
    async fetchProducts() {
      this.loading = true;
      try {
        const { data } = await api.get("/products/", { params: { search: this.search, page_size: 100 } });
        this.products = data.results || data;
      } finally {
        this.loading = false;
      }
    },
    async remove(product) {
      if (!confirm(`محصول «${product.name}» حذف شود؟`)) return;
      try {
        await api.delete(`/products/${product.id}/`);
        this.$store.dispatch("notify", { message: "محصول حذف شد." });
        this.fetchProducts();
      } catch (e) {
        this.$store.dispatch("notify", { message: "حذف محصول ناموفق بود.", type: "error" });
      }
    },
  },
};
</script>

<style scoped>
.page-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.page-head h1 {
  font-size: 1.4rem;
}
.table-card {
  padding: 18px;
}
.table-toolbar {
  margin-bottom: 14px;
}
.table-toolbar input {
  width: 260px;
  padding: 9px 12px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.87rem;
}
.admin-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.87rem;
}
.admin-table th {
  text-align: right;
  color: var(--color-text-muted);
  font-weight: 700;
  padding: 10px 12px;
  border-bottom: 1.5px solid var(--color-border);
  font-size: 0.8rem;
}
.admin-table td {
  padding: 12px;
  border-bottom: 1px solid var(--color-border);
}
.product-name-cell {
  font-weight: 700;
}
.low-stock-text {
  color: var(--color-danger);
  font-weight: 700;
}
.actions-cell {
  display: flex;
  gap: 8px;
}
.empty-row {
  text-align: center;
  padding: 30px;
}
</style>
