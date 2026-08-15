<template>
  <footer class="site-footer">
    <div class="container footer-inner">
      <div class="footer-col">
        <div class="brand">🎨 یاشیل آرت</div>
        <p class="text-muted">
          فروشگاه آنلاین یاشیل آرت؛ مسیری مطمئن از انتخاب تا تحویل درِ خانه.
        </p>
      </div>
      <div class="footer-col">
        <h4>دسترسی سریع</h4>
        <router-link to="/products">محصولات</router-link>
        <router-link to="/cart">سبد خرید</router-link>
        <router-link to="/my-orders">سفارش‌های من</router-link>
      </div>
      <div class="footer-col">
        <h4>پشتیبانی</h4>
        <span class="text-muted">۰۲۱-۹۱۰۰۰۰۰۰</span>
        <span class="text-muted">support@kaavan-shop.local</span>
        <span class="text-muted">شنبه تا پنجشنبه، ۹ تا ۱۸</span>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="container">© {{ year }} فروشگاه یاشیل آرت — تمامی حقوق محفوظ است.</div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "AppFooter",
  computed: {
    year() {
      return new Date().getFullYear();
    },
  },
};
</script>

<style scoped>
.site-footer {
  background: var(--color-primary-dark);
  color: rgba(255, 255, 255, 0.85);
  margin-top: 60px;
}
.footer-inner {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 30px;
  padding: 44px 20px 28px;
}
.footer-col {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.footer-col h4 {
  color: #fff;
  margin-bottom: 4px;
  font-size: 0.95rem;
}
.footer-col a {
  color: rgba(255, 255, 255, 0.75);
  font-size: 0.88rem;
}
.footer-col a:hover {
  color: var(--color-accent);
}
.footer-col .text-muted {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.85rem;
}
.brand {
  font-weight: 900;
  font-size: 1.15rem;
  color: #fff;
}
.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  padding: 14px 0;
  font-size: 0.78rem;
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
}
@media (max-width: 720px) {
  .footer-inner {
    grid-template-columns: 1fr;
  }
}
</style>
