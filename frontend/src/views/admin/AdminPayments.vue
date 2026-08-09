<template>
  <div class="admin-payments">
    <h1>پرداخت‌ها</h1>

    <div class="card table-card">
      <AppLoader v-if="loading" />
      <table v-else class="admin-table">
        <thead>
          <tr>
            <th>سفارش</th>
            <th>مشتری</th>
            <th>روش</th>
            <th>مبلغ</th>
            <th>رسید</th>
            <th>وضعیت</th>
            <th>تاریخ</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in payments" :key="p.id">
            <td>#{{ p.order_id }}</td>
            <td>{{ p.customer_username || "—" }}</td>
            <td>{{ p.method_display }}</td>
            <td>{{ formatPrice(p.amount) }}</td>
            <td>
              <a v-if="p.receipt_image" :href="p.receipt_image" target="_blank" rel="noopener" class="receipt-link">
                مشاهده رسید
              </a>
              <span v-else class="text-muted">—</span>
            </td>
            <td>
              <span class="badge" :class="statusClass(p.status)">{{ p.status_display }}</span>
            </td>
            <td class="text-muted">{{ formatDate(p.created_at) }}</td>
            <td class="actions-cell">
              <template v-if="p.status === 'submitted'">
                <button class="btn btn-primary btn-sm" @click="review(p, 'verified')">تایید</button>
                <button class="btn btn-danger btn-sm" @click="review(p, 'rejected')">رد</button>
              </template>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="!loading && payments.length === 0" class="text-muted empty-row">پرداختی ثبت نشده.</p>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

export default {
  name: "AdminPayments",
  components: { AppLoader },
  data() {
    return { payments: [], loading: true };
  },
  created() {
    this.fetchPayments();
  },
  methods: {
    formatPrice(v) {
      return Number(v).toLocaleString("fa-IR");
    },
    formatDate(v) {
      return new Date(v).toLocaleString("fa-IR");
    },
    statusClass(status) {
      const map = {
        pending: "badge-status-pending",
        submitted: "badge-status-pending",
        verified: "badge-status-paid",
        rejected: "badge-status-cancelled",
        failed: "badge-status-cancelled",
      };
      return map[status] || "badge-muted";
    },
    async fetchPayments() {
      this.loading = true;
      try {
        const { data } = await api.get("/admin/payments/", { params: { page_size: 100 } });
        this.payments = data.results || data;
      } finally {
        this.loading = false;
      }
    },
    async review(payment, status) {
      if (status === "rejected" && !confirm("این رسید رد شود؟")) return;
      try {
        const { data } = await api.patch(`/admin/payments/${payment.id}/`, { status });
        Object.assign(payment, data);
        this.$store.dispatch("notify", {
          message: status === "verified" ? "پرداخت تایید شد و سفارش پرداخت‌شده علامت خورد." : "رسید رد شد.",
        });
      } catch (e) {
        this.$store.dispatch("notify", { message: "به‌روزرسانی ناموفق بود.", type: "error" });
      }
    },
  },
};
</script>

<style scoped>
.admin-payments h1 {
  font-size: 1.4rem;
  margin-bottom: 20px;
}
.table-card {
  padding: 18px;
  overflow-x: auto;
}
.admin-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
  min-width: 820px;
}
.admin-table th {
  text-align: right;
  color: var(--color-text-muted);
  font-weight: 700;
  padding: 10px 12px;
  border-bottom: 1.5px solid var(--color-border);
  font-size: 0.78rem;
}
.admin-table td {
  padding: 10px 12px;
  border-bottom: 1px solid var(--color-border);
}
.receipt-link {
  color: var(--color-primary);
  font-weight: 700;
  font-size: 0.82rem;
}
.actions-cell {
  display: flex;
  gap: 6px;
}
.empty-row {
  text-align: center;
  padding: 30px;
}
</style>