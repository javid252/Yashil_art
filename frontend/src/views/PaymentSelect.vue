<template>
  <div class="container payment-page">
    <AppLoader v-if="loading" />

    <div v-else-if="!order" class="empty-state">
      <div class="icon">😕</div>
      <p>این سفارش پیدا نشد یا قبلاً پرداخت شده است.</p>
      <router-link to="/my-orders" class="btn btn-primary">سفارش‌های من</router-link>
    </div>

    <template v-else>
      <h1>پرداخت سفارش #{{ order.id }}</h1>
      <p class="text-muted amount-line">مبلغ قابل پرداخت: <strong>{{ formatPrice(order.total_price) }} تومان</strong></p>

      <div v-if="!settings.card_transfer_enabled && !settings.online_gateway_enabled" class="empty-state">
        <div class="icon">🚧</div>
        <p>در حال حاضر هیچ روش پرداختی فعال نیست. لطفاً با پشتیبانی تماس بگیرید.</p>
      </div>

      <div v-else class="method-tabs">
        <button
          v-if="settings.online_gateway_enabled"
          class="method-tab"
          :class="{ active: activeMethod === 'zarinpal' }"
          @click="activeMethod = 'zarinpal'"
        >
          💳 پرداخت آنلاین
        </button>
        <button
          v-if="settings.card_transfer_enabled"
          class="method-tab"
          :class="{ active: activeMethod === 'card_transfer' }"
          @click="activeMethod = 'card_transfer'"
        >
          🏦 کارت‌به‌کارت
        </button>
      </div>

      <!-- Online gateway -->
      <div v-if="activeMethod === 'zarinpal'" class="card method-card">
        <h3>پرداخت آنلاین</h3>
        <p class="text-muted">با کلیک روی دکمه زیر به درگاه پرداخت امن منتقل می‌شوید.</p>
        <div v-if="onlineError" class="form-error-box">{{ onlineError }}</div>
        <button class="btn btn-primary btn-block" :disabled="initiating" @click="initiateOnlinePayment">
          {{ initiating ? "در حال اتصال به درگاه..." : "پرداخت آنلاین" }}
        </button>
      </div>

      <!-- Card transfer -->
      <div v-if="activeMethod === 'card_transfer'" class="card method-card">
        <h3>اطلاعات واریز کارت‌به‌کارت</h3>
        <div class="card-info">
          <div class="card-info__row">
            <span class="text-muted">شماره کارت</span>
            <strong class="selectable">{{ settings.card_number }}</strong>
          </div>
          <div class="card-info__row">
            <span class="text-muted">به نام</span>
            <strong>{{ settings.card_holder_name }}</strong>
          </div>
          <div class="card-info__row" v-if="settings.bank_name">
            <span class="text-muted">بانک</span>
            <strong>{{ settings.bank_name }}</strong>
          </div>
        </div>
        <p v-if="settings.card_transfer_instructions" class="text-muted instructions">
          {{ settings.card_transfer_instructions }}
        </p>

        <div v-if="submittedPayment" class="form-success-box">
          رسید شما ارسال شد و در انتظار بررسی ادمین است. وضعیت سفارش را از «سفارش‌های من» پیگیری کنید.
        </div>

        <template v-else>
          <div v-if="cardError" class="form-error-box">{{ cardError }}</div>
          <div class="field">
            <label>تصویر رسید واریز</label>
            <input type="file" accept="image/*" @change="onReceiptSelected" />
          </div>
          <button class="btn btn-primary btn-block" :disabled="submittingReceipt || !receiptFile" @click="submitReceipt">
            {{ submittingReceipt ? "در حال ارسال..." : "ارسال رسید" }}
          </button>
        </template>
      </div>
    </template>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

export default {
  name: "PaymentSelectView",
  components: { AppLoader },
  data() {
    return {
      loading: true,
      order: null,
      settings: { card_transfer_enabled: false, online_gateway_enabled: false },
      activeMethod: null,

      initiating: false,
      onlineError: "",

      receiptFile: null,
      submittingReceipt: false,
      submittedPayment: false,
      cardError: "",
    };
  },
  async created() {
    try {
      const [orderRes, settingsRes] = await Promise.all([
        api.get("/orders/my/"),
        api.get("/payments/settings/"),
      ]);
      const orders = orderRes.data.results || orderRes.data;
      this.order = orders.find((o) => String(o.id) === this.$route.params.orderId && o.status === "pending") || null;
      this.settings = settingsRes.data;
      this.activeMethod = this.settings.online_gateway_enabled
        ? "zarinpal"
        : this.settings.card_transfer_enabled
        ? "card_transfer"
        : null;
    } finally {
      this.loading = false;
    }
  },
  methods: {
    formatPrice(v) {
      return Number(v).toLocaleString("fa-IR");
    },
    async initiateOnlinePayment() {
      this.initiating = true;
      this.onlineError = "";
      try {
        const { data } = await api.post("/payments/online/initiate/", { order: this.order.id });
        window.location.href = data.redirect_url;
      } catch (e) {
        this.onlineError =
          (e.response && e.response.data && e.response.data.detail) || "اتصال به درگاه پرداخت ناموفق بود.";
      } finally {
        this.initiating = false;
      }
    },
    onReceiptSelected(event) {
      this.receiptFile = event.target.files[0] || null;
    },
    async submitReceipt() {
      if (!this.receiptFile) return;
      this.submittingReceipt = true;
      this.cardError = "";
      try {
        const formData = new FormData();
        formData.append("order", this.order.id);
        formData.append("receipt_image", this.receiptFile);
        await api.post("/payments/card-transfer/", formData);
        this.submittedPayment = true;
        this.$store.dispatch("notify", { message: "رسید با موفقیت ارسال شد." });
      } catch (e) {
        this.cardError = "ارسال رسید ناموفق بود. دوباره تلاش کنید.";
      } finally {
        this.submittingReceipt = false;
      }
    },
  },
};
</script>

<style scoped>
.payment-page {
  padding: 40px 20px 60px;
  max-width: 560px;
  margin: 0 auto;
}
.payment-page h1 {
  font-size: 1.4rem;
  margin-bottom: 6px;
}
.amount-line {
  margin-bottom: 24px;
  font-size: 0.95rem;
}
.method-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 18px;
}
.method-tab {
  flex: 1;
  padding: 12px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  font-family: inherit;
  font-weight: 700;
  font-size: 0.88rem;
}
.method-tab.active {
  border-color: var(--color-primary);
  background: var(--color-sand);
  color: var(--color-primary-dark);
}
.method-card {
  padding: 24px;
}
.method-card h3 {
  font-size: 1rem;
  margin-bottom: 14px;
}
.card-info {
  background: var(--color-sand);
  border-radius: var(--radius-sm);
  padding: 16px;
  margin-bottom: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.card-info__row {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
}
.selectable {
  user-select: all;
  letter-spacing: 0.03em;
}
.instructions {
  font-size: 0.82rem;
  margin-bottom: 18px;
  line-height: 1.7;
}
</style>