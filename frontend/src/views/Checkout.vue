<template>
  <div class="container checkout-page">
    <h1>تکمیل خرید</h1>

    <div v-if="cartItems.length === 0" class="empty-state">
      <div class="icon">🛒</div>
      <p>سبد خرید شما خالی است.</p>
      <router-link to="/products" class="btn btn-primary">مشاهده محصولات</router-link>
    </div>

    <form v-else class="checkout-layout" @submit.prevent="submitOrder">
      <div class="checkout-form card">
        <h3>اطلاعات ارسال</h3>
        <div v-if="errorMessage" class="form-error-box">{{ errorMessage }}</div>

        <div class="field">
          <label>نام و نام خانوادگی گیرنده</label>
          <input v-model="form.full_name" type="text" required />
        </div>
        <div class="field">
          <label>شماره موبایل</label>
          <input v-model="form.phone_number" type="tel" required placeholder="09xxxxxxxxx" />
        </div>
        <div class="field">
          <label>آدرس کامل</label>
          <textarea v-model="form.address" rows="3" required></textarea>
        </div>
        <div class="field">
          <label>کد پستی (اختیاری)</label>
          <input v-model="form.postal_code" type="text" />
        </div>

        <button type="submit" class="btn btn-primary btn-block" :disabled="submitting">
          {{ submitting ? "در حال ثبت سفارش..." : "ثبت سفارش و انتخاب روش پرداخت" }}
        </button>
      </div>

      <aside class="order-summary card">
        <h3>سفارش شما</h3>
        <div v-for="line in cartItems" :key="`${line.product_id}-${line.variant_id || 0}`" class="summary-line">
          <span>{{ line.name }} <span class="text-muted">× {{ line.quantity }}</span></span>
          <span>{{ formatPrice(line.price * line.quantity) }}</span>
        </div>
        <RouteDivider margin="14px 0" />
        <div class="summary-row summary-row--total">
          <span>مجموع</span>
          <span>{{ formatPrice(subtotal) }} تومان</span>
        </div>
        <p class="text-muted note">بعد از ثبت این فرم، روش پرداخت (کارت‌به‌کارت یا آنلاین) را انتخاب می‌کنید.</p>
      </aside>
    </form>
  </div>
</template>

<script>
import { mapState } from "vuex";
import api from "@/services/api";
import RouteDivider from "@/components/RouteDivider.vue";

export default {
  name: "CheckoutView",
  components: { RouteDivider },
  data() {
    return {
      form: { full_name: "", phone_number: "", address: "", postal_code: "" },
      submitting: false,
      errorMessage: "",
    };
  },
  computed: {
    ...mapState("cart", ["items"]),
    cartItems() {
      return this.items;
    },
    subtotal() {
      return this.items.reduce((sum, i) => sum + i.price * i.quantity, 0);
    },
  },
  created() {
    const user = this.$store.getters["auth/currentUser"];
    if (user) {
      this.form.full_name = `${user.first_name || ""} ${user.last_name || ""}`.trim() || user.username;
      this.form.phone_number = user.phone_number || "";
    }
  },
  methods: {
    formatPrice(v) {
      return Number(v).toLocaleString("fa-IR");
    },
    async submitOrder() {
      this.submitting = true;
      this.errorMessage = "";
      try {
        const { data } = await api.post("/orders/checkout/", {
          ...this.form,
          items: this.items.map((i) => ({
            product_id: i.product_id,
            variant_id: i.variant_id || null,
            quantity: i.quantity,
          })),
        });
        this.$store.dispatch("cart/clearCart");
        this.$store.dispatch("notify", { message: "سفارش شما ثبت شد؛ حالا روش پرداخت را انتخاب کنید." });
        this.$router.push(`/payment/${data.id}`);
      } catch (e) {
        this.errorMessage = "ثبت سفارش با خطا مواجه شد. لطفاً دوباره تلاش کنید.";
      } finally {
        this.submitting = false;
      }
    },
  },
};
</script>

<style scoped>
.checkout-page {
  padding: 36px 20px 60px;
}
.checkout-page h1 {
  font-size: 1.6rem;
  margin-bottom: 26px;
}
.checkout-layout {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 30px;
  align-items: start;
}
.checkout-form,
.order-summary {
  padding: 22px;
}
.checkout-form h3,
.order-summary h3 {
  font-size: 1rem;
  margin-bottom: 18px;
}
.summary-line {
  display: flex;
  justify-content: space-between;
  font-size: 0.87rem;
  margin-bottom: 8px;
}
.summary-row--total {
  display: flex;
  justify-content: space-between;
  font-weight: 800;
  font-size: 1.05rem;
  margin-bottom: 12px;
}
.note {
  font-size: 0.78rem;
  line-height: 1.6;
}

@media (max-width: 800px) {
  .checkout-layout {
    grid-template-columns: 1fr;
  }
}
</style>
