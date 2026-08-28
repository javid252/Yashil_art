<template>
  <div class="container my-invoices-page">
    <div class="page-header">
      <h1>🧾 فاکتورهای من</h1>
      <p class="text-muted">لیست فاکتورهای صادر شده برای سفارشات شما</p>
    </div>

    <AppLoader v-if="loading" />

    <div v-else-if="invoices.length === 0" class="empty-state">
      <div class="empty-icon">🧾</div>
      <h3>هنوز فاکتوری ندارید</h3>
      <p class="text-muted">فاکتورها پس از ثبت سفارش به‌صورت خودکار صادر می‌شوند.</p>
      <router-link to="/products" class="btn btn-primary">شروع خرید</router-link>
    </div>

    <div v-else>
      <!-- فیلترها -->
      <div class="filter-bar">
        <div class="filter-tabs">
          <button
            v-for="tab in statusTabs"
            :key="tab.value"
            class="filter-tab"
            :class="{ active: activeFilter === tab.value }"
            @click="activeFilter = tab.value"
          >
            {{ tab.label }}
            <span v-if="getCountByStatus(tab.value) > 0" class="filter-count">
              {{ getCountByStatus(tab.value) }}
            </span>
          </button>
        </div>
      </div>

      <!-- لیست فاکتورها -->
      <div class="invoices-grid">
        <div
          v-for="invoice in filteredInvoices"
          :key="invoice.id"
          class="invoice-card card"
          @click="goToDetail(invoice.id)"
        >
          <div class="invoice-card__header">
            <div class="invoice-number">
              <span class="number-label">شماره فاکتور</span>
              <span class="number-value">{{ invoice.invoice_number }}</span>
            </div>
            <span class="status-badge" :class="'status-' + invoice.status">
              {{ invoice.status_display }}
            </span>
          </div>

          <div class="invoice-card__body">
            <div class="invoice-meta">
              <div class="meta-item">
                <span class="meta-label">شماره سفارش</span>
                <span class="meta-value">#{{ invoice.order }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">تاریخ صدور</span>
                <span class="meta-value">{{ formatDate(invoice.issued_at || invoice.created_at) }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">تعداد اقلام</span>
                <span class="meta-value">{{ invoice.items_count }} قلم</span>
              </div>
            </div>
          </div>

          <div class="invoice-card__footer">
            <div class="total-section">
              <span class="total-label">مبلغ نهایی</span>
              <span class="total-value">{{ invoice.formatted_grand_total }} تومان</span>
            </div>
            <div class="actions">
              <button
                class="btn btn-sm btn-outline"
                @click.stop="downloadPdf(invoice)"
                title="دانلود PDF"
              >
                📥 PDF
              </button>
              <span class="arrow-icon">←</span>
            </div>
          </div>

          <!-- نوار وضعیت -->
          <div class="invoice-card__status-bar" :class="'bar-' + invoice.status"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

const STATUS_TABS = [
  { value: "all", label: "همه" },
  { value: "issued", label: "صادر شده" },
  { value: "paid", label: "پرداخت شده" },
  { value: "draft", label: "پیش‌نویس" },
  { value: "cancelled", label: "لغو شده" },
  { value: "archived", label: "بایگانی" },
];

export default {
  name: "MyInvoicesView",
  components: { AppLoader },
  data() {
    return {
      invoices: [],
      loading: true,
      activeFilter: "all",
      statusTabs: STATUS_TABS,
    };
  },
  computed: {
    filteredInvoices() {
      if (this.activeFilter === "all") return this.invoices;
      if (this.activeFilter === "archived") {
        return this.invoices.filter((inv) => inv.is_archived);
      }
      return this.invoices.filter((inv) => inv.status === this.activeFilter);
    },
  },
  async created() {
    try {
      const { data } = await api.get("/invoices/my/");
      this.invoices = data.results || data;
    } finally {
      this.loading = false;
    }
  },
  methods: {
    formatDate(v) {
      if (!v) return "-";
      return new Date(v).toLocaleDateString("fa-IR");
    },
    getCountByStatus(status) {
      if (status === "all") return this.invoices.length;
      if (status === "archived") return this.invoices.filter((i) => i.is_archived).length;
      return this.invoices.filter((i) => i.status === status).length;
    },
    goToDetail(id) {
      this.$router.push({ name: "my-invoice-detail", params: { id } });
    },
    downloadPdf(invoice) {
      const token = localStorage.getItem("kaavan_access_token");
      const baseUrl = `${api.defaults.baseURL}/invoices/my/${invoice.id}/download-pdf/`;
      const url = baseUrl + (baseUrl.includes('?') ? '&' : '?') + 'token=' + encodeURIComponent(token);
      window.open(url, '_blank');
    },
  },
};
</script>

<style scoped>
.my-invoices-page {
  padding: 36px 20px 60px;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 1.6rem;
  margin-bottom: 6px;
}

/* فیلترها */
.filter-bar {
  margin-bottom: 24px;
}

.filter-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1.5px solid var(--color-border);
  border-radius: 24px;
  background: var(--color-surface);
  font-family: inherit;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--color-text-muted);
  cursor: pointer;
  transition: all 0.2s;
}

.filter-tab:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.filter-tab.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: #fff;
}

.filter-count {
  background: rgba(0, 0, 0, 0.1);
  padding: 1px 7px;
  border-radius: 10px;
  font-size: 0.72rem;
}

.filter-tab.active .filter-count {
  background: rgba(255, 255, 255, 0.25);
}

/* خالی بودن */
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 1.2rem;
  margin-bottom: 8px;
}

/* کارت فاکتور */
.invoices-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.invoice-card {
  padding: 0;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.invoice-card:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.invoice-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 22px 12px;
  border-bottom: 1px dashed var(--color-border);
}

.number-label {
  display: block;
  font-size: 0.72rem;
  color: var(--color-text-muted);
  margin-bottom: 2px;
}

.number-value {
  font-size: 1rem;
  font-weight: 800;
  color: var(--color-primary);
  font-family: monospace;
  letter-spacing: 0.5px;
}

/* وضعیت */
.status-badge {
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
}

.status-draft {
  background: #f0f0f0;
  color: #666;
}

.status-issued {
  background: #e8f8f5;
  color: #16a085;
}

.status-paid {
  background: #e3f2fd;
  color: #1976d2;
}

.status-cancelled {
  background: #fce4ec;
  color: #c62828;
}

.status-archived {
  background: #f3e5f5;
  color: #7b1fa2;
}

/* بدنه */
.invoice-card__body {
  padding: 14px 22px;
}

.invoice-meta {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.meta-item {
  display: flex;
  flex-direction: column;
}

.meta-label {
  font-size: 0.7rem;
  color: var(--color-text-muted);
  margin-bottom: 3px;
}

.meta-value {
  font-size: 0.88rem;
  font-weight: 600;
}

/* فوتر */
.invoice-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 22px;
  background: var(--color-bg);
  border-top: 1px solid var(--color-border);
}

.total-label {
  display: block;
  font-size: 0.7rem;
  color: var(--color-text-muted);
}

.total-value {
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--color-primary);
}

.actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.arrow-icon {
  font-size: 1.1rem;
  color: var(--color-text-muted);
}

/* نوار وضعیت */
.invoice-card__status-bar {
  height: 3px;
  width: 100%;
}

.bar-draft {
  background: #9e9e9e;
}

.bar-issued {
  background: linear-gradient(90deg, #16a085, #1abc9c);
}

.bar-paid {
  background: linear-gradient(90deg, #1976d2, #42a5f5);
}

.bar-cancelled {
  background: #c62828;
}

.bar-archived {
  background: linear-gradient(90deg, #7b1fa2, #ab47bc);
}

/* ریسپانسیو */
@media (max-width: 600px) {
  .invoice-meta {
    grid-template-columns: 1fr 1fr;
  }

  .invoice-card__footer {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}
</style>