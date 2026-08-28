<template>
  <div class="container success-page">
    <div class="success-card card fade-in">
      <div class="success-icon">🎨</div>
      <h1>سفارش شما ثبت شد!</h1>
      <p class="text-muted">
        شماره سفارش شما <strong>#{{ $route.params.id }}</strong> است. کاروان یاشیل آرت به‌زودی سفارش شما را به مقصد می‌رساند.
      </p>
      <div class="success-actions">
        <router-link to="/my-orders" class="btn btn-primary">پیگیری سفارش‌ها</router-link>
        <router-link to="/my-invoices" class="btn btn-outline">🧾 فاکتور خرید</router-link>
        <router-link to="/products" class="btn btn-outline">ادامه خرید</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "OrderSuccessView",
};
</script>

<style scoped>
.success-page {
  padding: 60px 20px;
  display: flex;
  justify-content: center;
}
.success-card {
  max-width: 480px;
  text-align: center;
  padding: 46px 34px;
}
.success-icon {
  font-size: 3rem;
  margin-bottom: 14px;
}
.success-card h1 {
  font-size: 1.4rem;
  margin-bottom: 10px;
}
.success-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 26px;
}
</style>