<template>
  <div class="auth-page">
    <form class="auth-card card fade-in" @submit.prevent="submit">
      <router-link to="/" class="auth-brand">🎨 یاشیل آرت</router-link>
      <h1>ساخت حساب کاربری</h1>

      <div v-if="errorMessage" class="form-error-box">{{ errorMessage }}</div>

      <div class="two-col">
        <div class="field">
          <label>نام</label>
          <input v-model="form.first_name" type="text" />
        </div>
        <div class="field">
          <label>نام خانوادگی</label>
          <input v-model="form.last_name" type="text" />
        </div>
      </div>
      <div class="field">
        <label>نام کاربری</label>
        <input v-model="form.username" type="text" required />
      </div>
      <div class="field">
        <label>ایمیل</label>
        <input v-model="form.email" type="email" required />
      </div>
      <div class="field">
        <label>شماره موبایل</label>
        <input v-model="form.phone_number" type="tel" placeholder="09xxxxxxxxx" />
      </div>
      <div class="field">
        <label>رمز عبور</label>
        <input v-model="form.password" type="password" required />
      </div>
      <div class="field">
        <label>تکرار رمز عبور</label>
        <input v-model="form.password_confirm" type="password" required />
      </div>

      <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
        {{ loading ? "در حال ثبت‌نام..." : "ثبت‌نام" }}
      </button>

      <SocialAuthPanel />

      <p class="auth-switch">
        قبلاً ثبت‌نام کرده‌اید؟ <router-link to="/login">ورود</router-link>
      </p>
    </form>
  </div>
</template>

<script>
import SocialAuthPanel from "@/components/SocialAuthPanel.vue";

export default {
  name: "RegisterView",
  components: { SocialAuthPanel },
  data() {
    return {
      form: {
        first_name: "", last_name: "", username: "", email: "",
        phone_number: "", password: "", password_confirm: "",
      },
      loading: false,
      errorMessage: "",
    };
  },
  methods: {
    async submit() {
      if (this.form.password !== this.form.password_confirm) {
        this.errorMessage = "رمزهای عبور یکسان نیستند.";
        return;
      }
      this.loading = true;
      this.errorMessage = "";
      try {
        await this.$store.dispatch("auth/register", this.form);
        this.$store.dispatch("notify", { message: "ثبت‌نام با موفقیت انجام شد. خوش آمدید!" });
        this.$router.push("/");
      } catch (e) {
        const data = e.response && e.response.data;
        if (data) {
          this.errorMessage = Object.values(data).flat().join(" ");
        } else {
          this.errorMessage = "ثبت‌نام ناموفق بود. لطفاً دوباره تلاش کنید.";
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.auth-page {
  min-height: calc(100vh - var(--header-height));
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 16px;
  background: var(--color-sand);
}
.auth-card {
  width: 100%;
  max-width: 440px;
  padding: 34px 30px;
}
.auth-brand {
  display: block;
  text-align: center;
  font-weight: 900;
  color: var(--color-primary);
  margin-bottom: 18px;
  font-size: 1.1rem;
}
.auth-card h1 {
  font-size: 1.2rem;
  text-align: center;
  margin-bottom: 24px;
}
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.auth-switch {
  text-align: center;
  font-size: 0.85rem;
  margin-top: 18px;
  color: var(--color-text-muted);
}
.auth-switch a {
  color: var(--color-primary);
  font-weight: 700;
}
</style>
