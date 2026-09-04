<template>
  <div class="panel-shell">
    <aside class="panel-sidebar">
      <router-link to="/" class="panel-brand">🎨 یاشیل آرت <span>پنل دانشجو</span></router-link>
      <div class="panel-user">{{ userLabel }}</div>
      <nav class="panel-nav">
        <router-link to="/student/dashboard">📊 داشبورد</router-link>
        <router-link to="/student/my-courses">📚 دوره‌های من</router-link>
        <router-link to="/student/grades">📝 نمرات</router-link>
        <router-link to="/student/certificates">🏆 گواهینامه‌ها</router-link>
        <router-link to="/student/gallery">🖼️ آثار هنری</router-link>
        <router-link to="/student/workshops">🎓 کارگاه‌ها</router-link>
        <router-link to="/student/profile">👤 پروفایل</router-link>
      </nav>
      <router-link to="/" class="panel-back">← بازگشت به سایت</router-link>
    </aside>
    <div class="panel-main">
      <header class="panel-topbar">
        <span class="text-muted">خوش آمدید، {{ userLabel }}</span>
        <button class="btn-logout" @click="logout">خروج</button>
      </header>
      <div class="panel-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "StudentLayout",
  computed: {
    ...mapGetters("auth", ["currentUser"]),
    userLabel() {
      return this.currentUser ? this.currentUser.first_name || this.currentUser.username : "";
    },
  },
  methods: {
    logout() {
      this.$store.dispatch("auth/logout");
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.panel-shell { display: flex; min-height: 100vh; background: #f5f6fa; font-family: 'Vazirmatn', Tahoma, sans-serif; }
.panel-sidebar {
  width: 240px; background: linear-gradient(180deg, #1a2f1e 0%, #0f1a12 100%);
  color: #fff; display: flex; flex-direction: column; padding: 22px 14px; flex-shrink: 0;
}
.panel-brand { font-weight: 900; font-size: 1.05rem; color: #fff; margin-bottom: 4px; padding: 0 8px; text-decoration: none; }
.panel-brand span { color: #c9a96e; font-size: 0.72rem; font-weight: 600; margin-right: 6px; }
.panel-user { padding: 0 8px; margin-bottom: 24px; font-size: 0.78rem; color: rgba(255,255,255,0.6); }
.panel-nav { display: flex; flex-direction: column; gap: 3px; flex: 1; }
.panel-nav a {
  padding: 10px 12px; border-radius: 8px; font-size: 0.88rem; font-weight: 600;
  color: rgba(255,255,255,0.75); text-decoration: none; transition: all 0.2s;
}
.panel-nav a:hover { background: rgba(255,255,255,0.08); color: #fff; }
.panel-nav a.router-link-exact-active { background: #c9a96e; color: #1a2f1e; }
.panel-back { font-size: 0.8rem; color: rgba(255,255,255,0.5); padding: 10px 12px; text-decoration: none; }
.panel-main { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.panel-topbar {
  height: 56px; background: #fff; border-bottom: 1px solid #e8e8e8;
  display: flex; align-items: center; justify-content: space-between; padding: 0 24px; font-size: 0.88rem;
}
.btn-logout {
  background: none; border: 1px solid #e74c3c; color: #e74c3c; padding: 6px 14px;
  border-radius: 6px; font-family: inherit; font-size: 0.82rem; cursor: pointer;
}
.btn-logout:hover { background: #e74c3c; color: #fff; }
.panel-content { flex: 1; padding: 24px; overflow-x: auto; }
.text-muted { color: #666; }
@media (max-width: 768px) {
  .panel-sidebar { width: 60px; padding: 16px 8px; }
  .panel-brand span, .panel-user, .panel-back { display: none; }
  .panel-nav a { font-size: 1.2rem; text-align: center; padding: 12px 6px; }
}
</style>
