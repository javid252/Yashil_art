<template>
  <div class="admin-invoices">
    <h1>🧾 مدیریت فاکتورها</h1>

    <div class="card table-card">
      <AppLoader v-if="loading" />

      <template v-else>
        <!-- فیلتر و جستجو -->
        <div class="toolbar">
          <div class="search-box">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="جستجو بر اساس شماره فاکتور، نام یا ایمیل..."
              class="search-input"
            />
          </div>
          <div class="filter-group">
            <select v-model="statusFilter" class="filter-select">
              <option value="">همه وضعیت‌ها</option>
              <option value="draft">پیش‌نویس</option>
              <option value="issued">صادر شده</option>
              <option value="paid">پرداخت شده</option>
              <option value="cancelled">لغو شده</option>
              <option value="archived">بایگانی شده</option>
            </select>
          </div>
        </div>

        <!-- جدول -->
        <table class="admin-table">
          <thead>
            <tr>
              <th>شماره فاکتور</th>
              <th>سفارش</th>
              <th>خریدار</th>
              <th>مبلغ نهایی</th>
              <th>تاریخ صدور</th>
              <th>وضعیت</th>
              <th>ایمیل</th>
              <th>عملیات</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="invoice in filteredInvoices" :key="invoice.id">
              <td>
                <span class="mono-text">{{ invoice.invoice_number }}</span>
              </td>
              <td>
                <router-link :to="{ name: 'admin-orders' }" class="link-primary">
                  #{{ invoice.order }}
                </router-link>
              </td>
              <td>
                <div class="buyer-cell">
                  <span class="buyer-name">{{ invoice.buyer_full_name }}</span>
                  <span v-if="invoice.buyer_phone" class="text-muted">
                    {{ invoice.buyer_phone }}
                  </span>
                </div>
              </td>
              <td class="font-bold">{{ invoice.formatted_grand_total }} تومان</td>
              <td>{{ formatDate(invoice.issued_at || invoice.created_at) }}</td>
              <td>
                <select
                  class="status-select"
                  :class="'status-' + invoice.status"
                  :value="invoice.status"
                  @change="updateStatus(invoice, $event.target.value)"
                >
                  <option v-for="s in statuses" :key="s.value" :value="s.value">
                    {{ s.label }}
                  </option>
                </select>
              </td>
              <td>
                <span v-if="invoice.email_sent" class="email-sent">✅ ارسال شده</span>
                <span v-else class="email-pending">—</span>
              </td>
              <td>
                <div class="action-btns">
                  <button
                    class="btn btn-xs btn-outline"
                    @click="downloadPdf(invoice)"
                    title="دانلود PDF"
                  >
                    📥
                  </button>
                  <button
                    class="btn btn-xs btn-outline"
                    :disabled="!invoice.buyer_email || invoice.email_sent"
                    @click="sendEmail(invoice)"
                    title="ارسال ایمیل"
                  >
                    📧
                  </button>
                  <button
                    class="btn btn-xs btn-outline"
                    @click="toggleArchive(invoice)"
                    :title="invoice.is_archived ? 'خارج از بایگانی' : 'بایگانی'"
                  >
                    {{ invoice.is_archived ? "📤" : "📁" }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <p v-if="filteredInvoices.length === 0" class="text-muted empty-row">
          فاکتوری یافت نشد.
        </p>
      </template>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

const STATUSES = [
  { value: "draft", label: "پیش‌نویس" },
  { value: "issued", label: "صادر شده" },
  { value: "paid", label: "پرداخت شده" },
  { value: "cancelled", label: "لغو شده" },
  { value: "archived", label: "بایگانی شده" },
];

export default {
  name: "AdminInvoices",
  components: { AppLoader },
  data() {
    return {
      invoices: [],
      loading: true,
      statuses: STATUSES,
      searchQuery: "",
      statusFilter: "",
    };
  },
  computed: {
    filteredInvoices() {
      let list = this.invoices;
      if (this.statusFilter) {
        list = list.filter((inv) => inv.status === this.statusFilter);
      }
      if (this.searchQuery.trim()) {
        const q = this.searchQuery.trim().toLowerCase();
        list = list.filter(
          (inv) =>
            inv.invoice_number.toLowerCase().includes(q) ||
            (inv.buyer_full_name && inv.buyer_full_name.toLowerCase().includes(q)) ||
            (inv.buyer_email && inv.buyer_email.toLowerCase().includes(q))
        );
      }
      return list;
    },
  },
  created() {
    this.fetchInvoices();
  },
  methods: {
    formatDate(v) {
      if (!v) return "-";
      return new Date(v).toLocaleDateString("fa-IR");
    },
    async fetchInvoices() {
      this.loading = true;
      try {
        const { data } = await api.get("/invoices/admin/", {
          params: { page_size: 200 },
        });
        this.invoices = data.results || data;
      } finally {
        this.loading = false;
      }
    },
    async updateStatus(invoice, status) {
      try {
        await api.patch(`/invoices/admin/${invoice.id}/`, { status });
        invoice.status = status;
        this.$store.dispatch("notify", {
          message: `وضعیت فاکتور ${invoice.invoice_number} به‌روزرسانی شد.`,
        });
      } catch (e) {
        this.$store.dispatch("notify", {
          message: "خطا در به‌روزرسانی وضعیت.",
          type: "error",
        });
      }
    },
    async toggleArchive(invoice) {
      try {
        const { data } = await api.post(`/invoices/admin/${invoice.id}/archive/`, {
          archive: !invoice.is_archived,
        });
        Object.assign(invoice, data);
        this.$store.dispatch("notify", {
          message: invoice.is_archived
            ? `فاکتور ${invoice.invoice_number} بایگانی شد.`
            : `فاکتور ${invoice.invoice_number} از بایگانی خارج شد.`,
        });
      } catch (e) {
        this.$store.dispatch("notify", {
          message: "خطا در بایگانی فاکتور.",
          type: "error",
        });
      }
    },
    async sendEmail(invoice) {
      if (!invoice.buyer_email) {
        this.$store.dispatch("notify", {
          message: "ایمیل خریدار ثبت نشده است.",
          type: "error",
        });
        return;
      }
      try {
        await api.post(`/invoices/admin/${invoice.id}/send-email/`);
        invoice.email_sent = true;
        this.$store.dispatch("notify", {
          message: `ایمیل فاکتور ${invoice.invoice_number} ارسال شد.`,
        });
      } catch (e) {
        this.$store.dispatch("notify", {
          message: "خطا در ارسال ایمیل.",
          type: "error",
        });
      }
    },
    downloadPdf(invoice) {
      const token = localStorage.getItem("kaavan_access_token");
      const baseUrl = `${api.defaults.baseURL}/invoices/admin/${invoice.id}/download-pdf/`;
      const url = baseUrl + (baseUrl.includes('?') ? '&' : '?') + 'token=' + encodeURIComponent(token);
      window.open(url, '_blank');
    },
  },
};
</script>

<style scoped>
.admin-invoices h1 {
  font-size: 1.4rem;
  margin-bottom: 20px;
}

.table-card {
  padding: 18px;
  overflow-x: auto;
}

/* نوار ابزار */
.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 18px;
  flex-wrap: wrap;
}

.search-input {
  padding: 8px 14px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.82rem;
  min-width: 280px;
  transition: border-color 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.filter-select {
  padding: 8px 12px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.82rem;
}

/* جدول */
.admin-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
  min-width: 900px;
}

.admin-table th {
  text-align: right;
  color: var(--color-text-muted);
  font-weight: 700;
  padding: 10px 12px;
  border-bottom: 1.5px solid var(--color-border);
  font-size: 0.75rem;
}

.admin-table td {
  padding: 12px;
  border-bottom: 1px solid var(--color-border);
  vertical-align: middle;
}

.mono-text {
  font-family: monospace;
  font-size: 0.82rem;
  font-weight: 600;
}

.link-primary {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
}

.link-primary:hover {
  text-decoration: underline;
}

.buyer-cell {
  display: flex;
  flex-direction: column;
}

.buyer-name {
  font-weight: 600;
}

.font-bold {
  font-weight: 700;
}

/* وضعیت */
.status-select {
  padding: 5px 10px;
  border-radius: var(--radius-sm);
  border: 1.5px solid var(--color-border);
  font-family: inherit;
  font-size: 0.78rem;
  font-weight: 600;
}

.status-draft {
  color: #666;
}

.status-issued {
  color: #16a085;
  border-color: #16a085;
  background: #e8f8f5;
}

.status-paid {
  color: #1976d2;
  border-color: #1976d2;
  background: #e3f2fd;
}

.status-cancelled {
  color: #c62828;
  border-color: #c62828;
  background: #fce4ec;
}

.status-archived {
  color: #7b1fa2;
  border-color: #7b1fa2;
  background: #f3e5f5;
}

/* ایمیل */
.email-sent {
  font-size: 0.75rem;
  color: #2e7d32;
}

.email-pending {
  color: var(--color-text-muted);
}

/* دکمه‌ها */
.action-btns {
  display: flex;
  gap: 4px;
}

.btn-xs {
  padding: 4px 8px;
  font-size: 0.85rem;
  min-width: auto;
}

.btn-xs:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.text-muted {
  color: var(--color-text-muted);
}

.empty-row {
  text-align: center;
  padding: 30px;
}
</style>