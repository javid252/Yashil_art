<template>
  <div class="container result-page">
    <div class="card result-card fade-in">
      <template v-if="status === 'success'">
        <div class="icon">✅</div>
        <h1>پرداخت با موفقیت انجام شد</h1>
        <p class="text-muted">سفارش #{{ orderId }} پرداخت شد و در حال آماده‌سازی است.</p>
      </template>
      <template v-else-if="status === 'cancelled'">
        <div class="icon">⏹️</div>
        <h1>پرداخت لغو شد</h1>
        <p class="text-muted">می‌توانید دوباره تلاش کنید یا روش دیگری انتخاب کنید.</p>
      </template>
      <template v-else-if="status === 'failed'">
        <div class="icon">❌</div>
        <h1>پرداخت ناموفق بود</h1>
        <p class="text-muted">مبلغی از حساب شما کسر نشده است. لطفاً دوباره تلاش کنید.</p>
      </template>
      <template v-else>
        <div class="icon">⚠️</div>
        <h1>مشکلی پیش آمد</h1>
        <p class="text-muted">وضعیت این پرداخت مشخص نیست؛ لطفاً از «سفارش‌های من» بررسی کنید یا با پشتیبانی تماس بگیرید.</p>
      </template>

      <div class="result-actions">
        <router-link v-if="orderId && status !== 'success'" :to="`/payment/${orderId}`" class="btn btn-primary">
          تلاش دوباره
        </router-link>
        <router-link to="/my-orders" class="btn btn-outline">سفارش‌های من</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PaymentResultView",
  computed: {
    status() {
      return this.$route.query.status || "error";
    },
    orderId() {
      return this.$route.query.order || null;
    },
  },
};
</script>

<style scoped>
.result-page {
  padding: 60px 20px;
  display: flex;
  justify-content: center;
}
.result-card {
  max-width: 460px;
  text-align: center;
  padding: 44px 32px;
}
.icon {
  font-size: 2.6rem;
  margin-bottom: 14px;
}
.result-card h1 {
  font-size: 1.3rem;
  margin-bottom: 8px;
}
.result-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 26px;
}
</style>