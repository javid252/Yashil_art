<template>
  <div class="auth-page">
    <form class="auth-card card fade-in" @submit.prevent="submit">
      <router-link to="/" class="auth-brand">🎨 یاشیل آرت</router-link>
      <h1>ورود به حساب کاربری</h1>

      <div v-if="errorMessage" class="form-error-box">{{ errorMessage }}</div>

      <div class="field">
        <label>نام کاربری یا ایمیل</label>
        <input v-model="form.username" type="text" required autofocus />
      </div>
      <div class="field">
        <label>رمز عبور</label>
        <input v-model="form.password" type="password" required />
      </div>

      <div class="auth-row">
        <router-link to="/forgot-password">رمز عبور را فراموش کرده‌اید؟</router-link>
      </div>

      <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
        {{ loading ? "در حال ورود..." : "ورود" }}
      </button>

      <SocialAuthPanel />

      <p class="auth-switch">
        حساب کاربری ندارید؟ <router-link to="/register">ثبت‌نام کنید</router-link>
      </p>
    </form>
  </div>
</template>

<script>
import SocialAuthPanel from "@/components/SocialAuthPanel.vue";

export default {
  name: "LoginView",
  components: { SocialAuthPanel },
  data() {
    return {
      form: { username: "", password: "" },
      loading: false,
      errorMessage: "",
    };
  },
  methods: {
    async submit() {
      this.loading = true;
      this.errorMessage = "";
      try {
        await this.$store.dispatch("auth/login", this.form);
        this.$store.dispatch("notify", { message: "خوش آمدید!" });
        const redirect = this.$route.query.redirect;
        if (redirect) {
          this.$router.push(redirect);
          return;
        }
        const u = this.$store.getters["auth/currentUser"];
        if (u) {
          if (u.is_staff || u.is_superuser) this.$router.push("/admin");
          else if (u.is_instructor) this.$router.push("/instructor");
          else if (u.is_student) this.$router.push("/student");
          else this.$router.push("/");
        } else {
          this.$router.push("/");
        }
      } catch (e) {
        this.errorMessage = "نام کاربری یا رمز عبور نادرست است.";
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
  max-width: 400px;
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
.auth-row {
  display: flex;
  justify-content: flex-end;
  margin: -8px 0 18px;
  font-size: 0.82rem;
}
.auth-row a {
  color: var(--color-primary);
  font-weight: 600;
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
