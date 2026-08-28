<template>
  <div class="container invoice-detail-page">
    <AppLoader v-if="loading" />

    <template v-else-if="invoice">
      <!-- هدر صفحه -->
      <div class="page-header">
        <button class="btn-back" @click="$router.push({ name: 'my-invoices' })">
          ← بازگشت به لیست فاکتورها
        </button>
        <div class="header-actions">
          <button class="btn btn-outline" @click="downloadPdf">
            📥 دانلود PDF
          </button>
        </div>
      </div>

      <!-- فاکتور -->
      <div class="invoice-paper card">
        <!-- هدر فاکتور -->
        <div class="invoice-top">
          <div class="shop-info">
            <div class="shop-logo">🌿</div>
            <div>
              <h2 class="shop-name">یاشیل آرت</h2>
              <p class="shop-desc">فروشگاه آنلاین محصولات هنری</p>
              <p class="shop-url">yashilartshop.ir</p>
            </div>
          </div>
          <div class="invoice-badge-section">
            <div class="invoice-badge">فاکتور فروش</div>
            <div class="invoice-number-display">{{ invoice.invoice_number }}</div>
            <div class="invoice-date-display">
              تاریخ صدور: {{ formatDate(invoice.issued_at || invoice.created_at) }}
            </div>
          </div>
        </div>

        <!-- اطلاعات خریدار و وضعیت -->
        <div class="info-section">
          <div class="buyer-info">
            <h3 class="section-title">اطلاعات خریدار</h3>
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">نام:</span>
                <span class="info-value">{{ invoice.buyer_full_name }}</span>
              </div>
              <div v-if="invoice.buyer_phone" class="info-item">
                <span class="info-label">تلفن:</span>
                <span class="info-value">{{ invoice.buyer_phone }}</span>
              </div>
              <div v-if="invoice.buyer_email" class="info-item">
                <span class="info-label">ایمیل:</span>
                <span class="info-value">{{ invoice.buyer_email }}</span>
              </div>
              <div v-if="invoice.buyer_address" class="info-item full-width">
                <span class="info-label">آدرس:</span>
                <span class="info-value">{{ invoice.buyer_address }}</span>
              </div>
              <div v-if="invoice.buyer_postal_code" class="info-item">
                <span class="info-label">کد پستی:</span>
                <span class="info-value">{{ invoice.buyer_postal_code }}</span>
              </div>
            </div>
          </div>

          <div class="order-info">
            <h3 class="section-title">اطلاعات سفارش</h3>
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">شماره سفارش:</span>
                <span class="info-value">#{{ invoice.order }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">وضعیت فاکتور:</span>
                <span class="info-value">
                  <span class="status-badge" :class="'status-' + invoice.status">
                    {{ invoice.status_display }}
                  </span>
                </span>
              </div>
              <div v-if="invoice.email_sent" class="info-item">
                <span class="info-label">ایمیل ارسال شده:</span>
                <span class="info-value">✅ {{ formatDate(invoice.email_sent_at) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- جدول آیتم‌ها -->
        <div class="items-section">
          <table class="items-table">
            <thead>
              <tr>
                <th class="th-num">#</th>
                <th class="th-product">نام محصول</th>
                <th class="th-variant">مشخصات</th>
                <th class="th-price">قیمت واحد</th>
                <th class="th-qty">تعداد</th>
                <th class="th-total">جمع ردیف</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in items" :key="item.id">
                <td class="text-center">{{ index + 1 }}</td>
                <td class="text-right">{{ item.product_name }}</td>
                <td class="text-center">
                  <span v-if="item.variant_label">{{ item.variant_label }}</span>
                  <span v-else class="text-muted">-</span>
                </td>
                <td class="text-center">{{ item.formatted_unit_price }} تومان</td>
                <td class="text-center">{{ item.quantity }}</td>
                <td class="text-center font-bold">{{ item.formatted_line_total_after_discount }} تومان</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- خلاصه مالی -->
        <div class="summary-section">
          <div class="summary-table">
            <div class="summary-row">
              <span>جمع آیتم‌ها:</span>
              <span>{{ formatPrice(invoice.subtotal) }} تومان</span>
            </div>
            <div v-if="invoice.discount_total > 0" class="summary-row discount">
              <span>تخفیف:</span>
              <span>-{{ formatPrice(invoice.discount_total) }} تومان</span>
            </div>
            <div v-if="invoice.tax_total > 0" class="summary-row">
              <span>مالیات:</span>
              <span>{{ formatPrice(invoice.tax_total) }} تومان</span>
            </div>
            <div class="summary-row total">
              <span>مبلغ نهایی:</span>
              <span>{{ invoice.formatted_grand_total }} تومان</span>
            </div>
          </div>
        </div>

        <!-- یادداشت -->
        <div v-if="invoice.notes" class="notes-section">
          <strong>📝 یادداشت:</strong> {{ invoice.notes }}
        </div>

        <!-- فوتر فاکتور -->
        <div class="invoice-footer">
          <p>این فاکتور به‌صورت خودکار توسط سامانه فروشگاه یاشیل آرت صادر شده است.</p>
          <p>🌿 یاشیل آرت | yashilartshop.ir</p>
        </div>
      </div>
    </template>

    <div v-else class="empty-state">
      <div class="empty-icon">❌</div>
      <h3>فاکتور یافت نشد</h3>
      <router-link to="/my-invoices" class="btn btn-primary">بازگشت به لیست فاکتورها</router-link>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

export default {
  name: "InvoiceDetailView",
  components: { AppLoader },
  data() {
    return {
      invoice: null,
      items: [],
      loading: true,
    };
  },
  async created() {
    try {
      const { data } = await api.get(`/invoices/my/${this.$route.params.id}/`);
      this.invoice = data;
      this.items = data.items || [];
    } catch (e) {
      this.invoice = null;
    } finally {
      this.loading = false;
    }
  },
  methods: {
    formatPrice(v) {
      return Number(v).toLocaleString("fa-IR");
    },
    formatDate(v) {
      if (!v) return "-";
      return new Date(v).toLocaleDateString("fa-IR");
    },
    downloadPdf() {
      const token = localStorage.getItem("kaavan_access_token");
      const baseUrl = `${api.defaults.baseURL}/invoices/my/${this.invoice.id}/download-pdf/`;
      const url = baseUrl + (baseUrl.includes('?') ? '&' : '?') + 'token=' + encodeURIComponent(token);
      window.open(url, '_blank');
    },
  },
};
</script>

<style scoped>
.invoice-detail-page {
  padding: 30px 20px 60px;
}

/* هدر صفحه */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.btn-back {
  background: none;
  border: none;
  font-family: inherit;
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--color-primary);
  cursor: pointer;
  padding: 8px 0;
}

.btn-back:hover {
  text-decoration: underline;
}

/* کاغذ فاکتور */
.invoice-paper {
  max-width: 800px;
  margin: 0 auto;
  padding: 0;
  overflow: hidden;
}

/* هدر فاکتور */
.invoice-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 28px;
  border-bottom: 3px solid var(--color-primary);
  background: linear-gradient(135deg, #f0faf7 0%, #fff 100%);
}

.shop-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.shop-logo {
  font-size: 2.5rem;
}

.shop-name {
  font-size: 1.3rem;
  font-weight: 900;
  color: var(--color-primary);
  margin: 0;
}

.shop-desc {
  font-size: 0.78rem;
  color: var(--color-text-muted);
  margin: 2px 0 0;
}

.shop-url {
  font-size: 0.72rem;
  color: var(--color-primary);
  margin: 2px 0 0;
}

.invoice-badge-section {
  text-align: left;
}

.invoice-badge {
  display: inline-block;
  background: linear-gradient(135deg, var(--color-primary), #1abc9c);
  color: white;
  padding: 6px 18px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 8px;
}

.invoice-number-display {
  font-size: 0.95rem;
  font-weight: bold;
  font-family: monospace;
  color: #333;
}

.invoice-date-display {
  font-size: 0.78rem;
  color: #666;
  margin-top: 2px;
}

/* بخش اطلاعات */
.info-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
}

.buyer-info,
.order-info {
  padding: 20px 28px;
}

.buyer-info {
  border-left: 1px solid var(--color-border);
}

.section-title {
  font-size: 0.85rem;
  font-weight: bold;
  color: var(--color-primary);
  margin-bottom: 12px;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--color-border);
}

.info-grid {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.info-item {
  display: flex;
  gap: 8px;
  font-size: 0.82rem;
}

.info-label {
  color: var(--color-text-muted);
  font-weight: 600;
  min-width: 80px;
}

.info-value {
  color: #333;
}

/* جدول آیتم‌ها */
.items-section {
  padding: 0 28px;
}

.items-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
}

.items-table thead th {
  background: var(--color-primary);
  color: white;
  padding: 10px 8px;
  text-align: center;
  font-weight: bold;
  font-size: 0.78rem;
}

.th-num {
  width: 5%;
}

.th-product {
  width: 35%;
  text-align: right !important;
}

.th-variant {
  width: 15%;
}

.th-price {
  width: 15%;
}

.th-qty {
  width: 10%;
}

.th-total {
  width: 20%;
}

.items-table tbody td {
  padding: 10px 8px;
  border-bottom: 1px solid var(--color-border);
  text-align: center;
}

.items-table tbody tr:nth-child(even) {
  background: var(--color-bg);
}

.text-right {
  text-align: right !important;
}

.text-center {
  text-align: center;
}

.text-muted {
  color: var(--color-text-muted);
}

.font-bold {
  font-weight: 700;
}

/* خلاصه مالی */
.summary-section {
  padding: 20px 28px;
  display: flex;
  justify-content: flex-end;
}

.summary-table {
  width: 280px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  font-size: 0.85rem;
  border-bottom: 1px solid var(--color-border);
}

.summary-row.discount {
  color: #c62828;
}

.summary-row.total {
  border-bottom: none;
  border-top: 2px solid var(--color-primary);
  padding-top: 10px;
  margin-top: 4px;
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--color-primary);
}

/* یادداشت */
.notes-section {
  margin: 0 28px 16px;
  padding: 12px 16px;
  background: #fff8e1;
  border: 1px solid #ffc107;
  border-radius: 8px;
  font-size: 0.82rem;
  color: #856404;
}

/* فوتر فاکتور */
.invoice-footer {
  text-align: center;
  padding: 18px 28px;
  border-top: 2px solid var(--color-primary);
  background: var(--color-bg);
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.invoice-footer p {
  margin: 3px 0;
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

/* ریسپانسیو */
@media (max-width: 700px) {
  .invoice-top {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }

  .invoice-badge-section {
    text-align: center;
  }

  .info-section {
    grid-template-columns: 1fr;
  }

  .buyer-info {
    border-left: none;
    border-bottom: 1px solid var(--color-border);
  }

  .page-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}
</style>