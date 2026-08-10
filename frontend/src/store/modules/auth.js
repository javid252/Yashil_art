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
  }),
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    isAdmin: (state) => !!(state.user && state.user.is_staff),
    isSuperUser: (state) => !!(state.user && state.user.is_superuser),
    permissions: (state) => (state.user && state.user.permissions) || [],
    hasPermission: (state) => (codename) => {
      if (state.user && state.user.is_superuser) return true;
      return !!(state.user && state.user.permissions && state.user.permissions.includes(codename));
    },
    currentUser: (state) => state.user,
  },
  mutations: {
    SET_AUTH(state, { user, access, refresh }) {
      state.user = user;
      state.accessToken = access;
      localStorage.setItem("kaavan_user", JSON.stringify(user));
      localStorage.setItem("kaavan_access_token", access);
      if (refresh) localStorage.setItem("kaavan_refresh_token", refresh);
    },
    SET_USER(state, user) {
      state.user = user;
      localStorage.setItem("kaavan_user", JSON.stringify(user));
    },
    CLEAR_AUTH(state) {
      state.user = null;
      state.accessToken = null;
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
