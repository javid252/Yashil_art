<template>
  <div id="app-shell" :class="{ 'admin-theme': isBareLayout }">
    <AppHeader v-if="!isBareLayout" />
      <NavigationBar v-if="!isBareLayout" />
      <main class="main-content">
      <router-view />
    </main>
    <AppFooter v-if="!isBareLayout" />
    <ToastStack />
  </div>
</template>

<script>
import AppFooter from "@/components/AppFooter.vue";
import AppHeader from "@/components/AppHeader.vue";
import NavigationBar from "@/components/NavigationBar.vue";
import ToastStack from "@/components/ToastStack.vue";

export default {
  name: "App",
  components: { 
    AppHeader,
    NavigationBar,
    AppFooter,
    ToastStack
  },
  computed: {
    isBareLayout() {
      const p = this.$route.path;
      return p.startsWith("/admin") || p.startsWith("/vendor") || p.startsWith("/student") || p.startsWith("/instructor");
    },
  },
  created() {
    this.$store.dispatch("platform/fetchSettings");
    if (this.$store.getters["auth/isAuthenticated"]) {
      this.$store.dispatch("auth/fetchProfile");
      this.$store.dispatch("vendor/fetchMe");
    }
  },
};
</script>