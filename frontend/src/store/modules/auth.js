import api from "@/services/api";

function loadUser() {
  try {
    const raw = localStorage.getItem("kaavan_user");
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export default {
  namespaced: true,
  state: () => ({
    user: loadUser(),
    accessToken: localStorage.getItem("kaavan_access_token") || null,
    // آیا پروفایل کاربر در این نشست از سرور تازه‌سازی شده؟ (برای احراز نقش‌های تازه)
    profileChecked: false,
  }),
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    isAdmin: (state) => !!(state.user && state.user.is_staff),
    isSuperUser: (state) => !!(state.user && state.user.is_superuser),
    isStudent: (state) => !!(state.user && state.user.is_student),
    isInstructor: (state) => !!(state.user && state.user.is_instructor),
    groupNames: (state) => (state.user && state.user.group_names) || [],
    roleNames: (state) => (state.user && state.user.group_names) || [],
    isAcademyManager: (state) =>
      !!(
        state.user &&
        Array.isArray(state.user.group_names) &&
        state.user.group_names.includes("مدیر آموزشگاه")
      ),
    permissions: (state) => (state.user && state.user.permissions) || [],
    hasPermission: (state) => (codename) => {
      if (state.user && state.user.is_superuser) return true;
      return !!(state.user && state.user.permissions && state.user.permissions.includes(codename));
    },
    hasRole: (state) => (roleName) =>
      !!(state.user && Array.isArray(state.user.group_names) && state.user.group_names.includes(roleName)),
    currentUser: (state) => state.user,
  },
  mutations: {
    SET_AUTH(state, { user, access, refresh }) {
      state.user = user;
      state.accessToken = access;
      state.profileChecked = true;
      localStorage.setItem("kaavan_user", JSON.stringify(user));
      localStorage.setItem("kaavan_access_token", access);
      if (refresh) localStorage.setItem("kaavan_refresh_token", refresh);
    },
    SET_USER(state, user) {
      state.user = user;
      state.profileChecked = true;
      localStorage.setItem("kaavan_user", JSON.stringify(user));
    },
    CLEAR_AUTH(state) {
      state.user = null;
      state.accessToken = null;
      state.profileChecked = false;
      localStorage.removeItem("kaavan_user");
      localStorage.removeItem("kaavan_access_token");
      localStorage.removeItem("kaavan_refresh_token");
    },
  },
  actions: {
    async login({ commit }, credentials) {
      const { data } = await api.post("/auth/login/", credentials);
      commit("SET_AUTH", { user: data.user, access: data.access, refresh: data.refresh });
      return data.user;
    },
    async register({ commit }, payload) {
      await api.post("/auth/register/", payload);
      return this.dispatch("auth/login", {
        username: payload.username,
        password: payload.password,
      });
    },
    async fetchProfile({ commit }) {
      const { data } = await api.get("/auth/me/");
      commit("SET_USER", data);
      return data;
    },
    applySocialLogin({ commit }, data) {
      commit("SET_AUTH", { user: data.user, access: data.access, refresh: data.refresh });
      return data.user;
    },
    logout({ commit }) {
      commit("CLEAR_AUTH");
      this.commit("vendor/CLEAR");
    },
    async requestPasswordReset(_, email) {
      await api.post("/auth/password-reset/", { email });
    },
    async confirmPasswordReset(_, payload) {
      await api.post("/auth/password-reset/confirm/", payload);
    },
  },
};
