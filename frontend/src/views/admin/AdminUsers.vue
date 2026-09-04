<template>
  <div class="admin-users">
    <div class="page-head">
      <div>
        <h1>مدیریت کاربران و نقش‌ها</h1>
        <p class="page-sub">
          هر کاربر بر اساس نقش خود فقط امکانات مرتبط را می‌بیند. نقش از همین صفحه تعیین و با دکمه «ذخیره دسترسی‌ها» اعمال می‌شود.
        </p>
      </div>
    </div>

    <!-- Filters + Search -->
    <div class="toolbar">
      <div class="filter-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          class="filter-tab"
          :class="{ active: activeTab === tab.key }"
          @click="activeTab = tab.key"
        >
          {{ tab.label }}
          <span class="tab-count">{{ tab.count }}</span>
        </button>
      </div>
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input v-model="searchQuery" type="text" placeholder="جستجو با نام، ایمیل یا نام کاربری..." />
      </div>
    </div>

    <div class="card table-card">
      <AppLoader v-if="loading" />
      <template v-else>
        <table class="admin-table">
          <thead>
            <tr>
              <th>کاربر</th>
              <th>نقش‌ها و دسترسی‌ها</th>
              <th>تاریخ عضویت</th>
              <th>وضعیت</th>
              <th class="actions-col"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in visibleUsers" :key="u.id">
              <td>
                <div class="user-cell">
                  <div class="avatar" :class="'avatar-' + avatarColor(u)">{{ userInitial(u) }}</div>
                  <div class="user-meta">
                    <div class="user-name">
                      {{ u.first_name || u.username }} {{ u.last_name }}
                      <span v-if="u.is_superuser" class="badge badge-superuser">مدیر ارشد</span>
                    </div>
                    <div class="user-id">{{ u.username }} · {{ u.email }}</div>
                  </div>
                </div>
              </td>
              <td>
                <div v-if="roleObjects(u).length" class="roles-chips">
                  <span
                    v-for="role in roleObjects(u)"
                    :key="role.id"
                    class="role-chip"
                    :class="isIndependentRole(role) ? 'chip-independent' : isAcademyRole(role) ? 'chip-academy' : 'chip-shop'"
                    :title="role.description || ''"
                  >
                    {{ roleIcon(role.name) }} {{ role.name }}
                  </span>
                </div>
                <span v-else class="role-chip chip-none">👤 کاربر عادی</span>
                <div v-if="!u.is_active" class="disabled-tag">حساب غیرفعال</div>
              </td>
              <td class="text-muted date-cell">{{ formatDate(u.date_joined) }}</td>
              <td>
                <label class="switch">
                  <input
                    type="checkbox"
                    :checked="u.is_active"
                    :disabled="u.id === currentUserId"
                    @change="toggleActive(u, $event.target.checked)"
                  />
                  <span class="switch-state" :class="{ on: u.is_active }">{{ u.is_active ? "فعال" : "غیرفعال" }}</span>
                </label>
              </td>
              <td class="actions-col">
                <button class="btn-access" @click="openEditor(u)">
                  <span>🛡️</span> مدیریت دسترسی‌ها
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="!loading && visibleUsers.length === 0" class="text-muted empty-row">
          {{ searchQuery ? "کاربری با این مشخصات پیدا نشد." : "کاربری در این دسته وجود ندارد." }}
        </p>
      </template>
    </div>

    <!-- Role Editor Modal -->
    <transition name="modal">
      <div v-if="editorUser" class="modal-overlay" @click.self="closeEditor">
        <div class="modal-panel">
          <div class="modal-head">
            <div>
              <h3>🛡️ مدیریت دسترسی‌های {{ editorUser.first_name || editorUser.username }}</h3>
              <p class="modal-sub">نقش‌های موردنظر را تیک بزنید و ذخیره کنید. هر کاربر می‌تواند بیش از یک نقش داشته باشد.</p>
            </div>
            <button class="modal-close" @click="closeEditor">✕</button>
          </div>

          <div v-if="errorMessage" class="form-error-box">{{ errorMessage }}</div>

          <div class="role-sections">
            <!-- Independent roles (مدیرکل) -->
            <div class="role-section section-independent">
              <div class="section-head">
                <span class="section-icon">👑</span>
                <div>
                  <strong>نقش‌های مستقل</strong>
                  <p>مدیرکل سامانه - نه زیرمجموعه آموزشگاه است و نه فروشگاه؛ دسترسی کامل و بالاتر از همه نقش‌ها</p>
                </div>
              </div>
              <div class="role-options">
                <label v-for="role in independentRoles" :key="role.id" class="role-option" :class="{ selected: selected.includes(role.id) }">
                  <input type="checkbox" :value="role.id" v-model="selected" />
                  <span class="option-icon">{{ roleIcon(role.name) }}</span>
                  <span class="option-text">
                    <b>{{ role.name }}</b>
                    <small>{{ role.description || "نقش مستقل سامانه" }}</small>
                  </span>
                </label>
              </div>
              <p v-if="independentRoles.length === 0" class="text-muted section-empty">نقش مستقل ساخته نشده است.</p>
            </div>

            <!-- Academy roles -->
            <div class="role-section">
              <div class="section-head">
                <span class="section-icon">🎓</span>
                <div>
                  <strong>نقش‌های آموزشگاه</strong>
                  <p>دسترسی به پنل هنرجو، پنل استاد یا بخش آموزشگاه در پنل مدیریت</p>
                </div>
              </div>
              <div class="role-options">
                <label v-for="role in academyRoles" :key="role.id" class="role-option" :class="{ selected: selected.includes(role.id) }">
                  <input type="checkbox" :value="role.id" v-model="selected" />
                  <span class="option-icon">{{ roleIcon(role.name) }}</span>
                  <span class="option-text">
                    <b>{{ role.name }}</b>
                    <small>{{ role.description || "نقش سیستمی آموزشگاه" }}</small>
                  </span>
                </label>
              </div>
            </div>

            <!-- Shop / back-office roles -->
            <div class="role-section">
              <div class="section-head">
                <span class="section-icon">🏪</span>
                <div>
                  <strong>نقش‌های فروشگاه و بک‌آفیس</strong>
                  <p>دسترسی به بخش‌های مرتبط در پنل مدیریت (با داشتن این نقش‌ها، ورود به پنل مدیریت فعال می‌شود)</p>
                </div>
              </div>
              <div class="role-options">
                <label v-for="role in shopRoles" :key="role.id" class="role-option" :class="{ selected: selected.includes(role.id) }">
                  <input type="checkbox" :value="role.id" v-model="selected" />
                  <span class="option-icon">{{ roleIcon(role.name) }}</span>
                  <span class="option-text">
                    <b>{{ role.name }}</b>
                    <small>{{ role.description || "نقش تعریف‌شده توسط مدیر" }}</small>
                  </span>
                  <span v-if="!role.is_system" class="tag-custom">سفارشی</span>
                </label>
              </div>
              <p v-if="shopRoles.length === 0" class="text-muted section-empty">
                هنوز نقش فروشگاهی ساخته نشده. از صفحه «نقش‌ها و دسترسی‌ها» می‌توانید نقش جدید بسازید.
              </p>
            </div>

            <div class="plain-note">
              <span class="note-icon">ℹ️</span>
              <p>
                برای تبدیل کاربر به «کاربر عادی» (فقط خرید و مشاهده)، همه نقش‌ها را بردارید.
                اعطای نقش‌های «هنرآموز»/«استاد» پنل اختصاصی کاربر را فعال می‌کند و نقش‌های «مدیرکل»، «مدیر فروشگاه»، «مدیر آموزشگاه» و سایر نقش‌های مدیریتی، دسترسی به پنل مدیریت را فعال می‌کنند.
              </p>
            </div>
          </div>

          <div class="modal-actions">
            <button class="btn btn-outline" @click="closeEditor">انصراف</button>
            <button class="btn btn-primary" :disabled="saving" @click="saveAccess">
              {{ saving ? "در حال ذخیره..." : "ذخیره دسترسی‌ها" }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

const ROLE_ICONS = {
  "مدیرکل": "👑",
  "مدیر فروشگاه": "🏪",
  "هنرآموز": "🎓",
  "استاد": "👨‍🏫",
  "مدیر آموزشگاه": "🏛️",
  "حسابدار": "💰",
  "انباردار": "📦",
};

// نقش‌های آموزشگاه (ثابت). حتی اگر API دسته (category) را برنگرداند یا نام گروه
// فاصله اضافه داشته باشد، این نقش‌ها همیشه زیر «آموزشگاه» نمایش داده می‌شوند.
const ACADEMY_ROLE_NAMES = ["هنرآموز", "استاد", "مدیر آموزشگاه"];
// نقش‌های مستقل (نه آموزشگاه، نه فروشگاه) — بالای صفحه نمایش داده می‌شوند
const INDEPENDENT_ROLE_NAMES = ["مدیرکل", "مدیر کل"];
const normalizeRoleName = (s) => (s || "").replace(/\s+/g, "");

const CATEGORY_LABELS = {
  academy: "آموزشگاه",
  shop: "فروشگاه و بک‌آفیس",
  independent: "مستقل (مدیرکل)",
  customer: "کاربر عادی",
};

const AVATAR_COLORS = ["green", "gold", "teal", "rose", "violet", "slate"];

export default {
  name: "AdminUsers",
  components: { AppLoader },
  data() {
    return {
      users: [],
      roles: [],
      loading: true,
      activeTab: "all",
      searchQuery: "",
      editorUser: null,
      selected: [],
      saving: false,
      errorMessage: "",
    };
  },
  computed: {
    currentUserId() {
      const u = this.$store.getters["auth/currentUser"];
      return u ? u.id : null;
    },
    academyRoles() {
      return this.roles.filter((r) => this.isAcademyRole(r));
    },
    independentRoles() {
      return this.roles.filter((r) => this.isIndependentRole(r));
    },
    shopRoles() {
      return this.roles.filter((r) => !this.isAcademyRole(r) && !this.isIndependentRole(r));
    },
    roleById() {
      const map = {};
      this.roles.forEach((r) => (map[r.id] = r));
      return map;
    },
    tabs() {
      const counts = { all: this.users.length, academy: 0, shop: 0, independent: 0, customer: 0 };
      this.users.forEach((u) => {
        const cat = this.userCategory(u);
        if (counts[cat] !== undefined) counts[cat] += 1;
      });
      return [
        { key: "all", label: "همه کاربران", count: counts.all },
        { key: "academy", label: "🎓 آموزشگاه", count: counts.academy },
        { key: "independent", label: "👑 مستقل", count: counts.independent },
        { key: "shop", label: "🏪 فروشگاه / بک‌آفیس", count: counts.shop },
        { key: "customer", label: "👤 کاربر عادی", count: counts.customer },
      ];
    },
    visibleUsers() {
      const q = this.searchQuery.trim().toLowerCase();
      return this.users.filter((u) => {
        if (this.activeTab !== "all" && this.userCategory(u) !== this.activeTab) return false;
        if (!q) return true;
        return [u.username, u.email, u.first_name, u.last_name]
          .filter(Boolean)
          .some((v) => v.toLowerCase().includes(q));
      });
    },
  },
  async created() {
    await Promise.all([this.fetchUsers(), this.fetchRoles()]);
  },
  methods: {
    formatDate(v) {
      if (!v) return "—";
      return new Date(v).toLocaleDateString("fa-IR");
    },
    userInitial(u) {
      const name = u.first_name || u.username || "؟";
      return name.charAt(0);
    },
    avatarColor(u) {
      return AVATAR_COLORS[(u.id || 0) % AVATAR_COLORS.length];
    },
    roleIcon(name) {
      return ROLE_ICONS[name] || "🛠️";
    },
    roleObjects(u) {
      return (u.groups || [])
        .map((id) => this.roleById[id])
        .filter(Boolean)
        .sort(
          (a, b) =>
            (this.isIndependentRole(a) ? -2 : this.isAcademyRole(a) ? -1 : 1) -
            (this.isIndependentRole(b) ? -2 : this.isAcademyRole(b) ? -1 : 1)
        );
    },
    // آیا نقش، نقشی از آموزشگاه است؟ (اعم از category از سرور یا نام استاندارد)
    isAcademyRole(role) {
      if (!role) return false;
      if (role.category === "academy") return true;
      return ACADEMY_ROLE_NAMES.includes(normalizeRoleName(role.name));
    },
    // نقش مستقل (مدیرکل): نه آموزشگاه، نه فروشگاه
    isIndependentRole(role) {
      if (!role) return false;
      if (role.category === "independent") return true;
      return INDEPENDENT_ROLE_NAMES.includes(normalizeRoleName(role.name));
    },
    // دسته هر کاربر: آموزشگاه | مستقل | فروشگاه/بک‌آفیس | عادی
    userCategory(u) {
      const roles = (u.groups || []).map((id) => this.roleById[id]).filter(Boolean);
      if (roles.some((r) => this.isIndependentRole(r))) return "independent";
      if (roles.some((r) => this.isAcademyRole(r))) return "academy";
      if (roles.some((r) => !this.isAcademyRole(r)) || u.is_staff || u.is_superuser) return "shop";
      return "customer";
    },
    async fetchUsers() {
      this.loading = true;
      try {
        const { data } = await api.get("/admin/users/");
        this.users = data.results || data;
      } catch (e) {
        this.$store.dispatch("notify", { message: "بارگذاری کاربران ناموفق بود.", type: "error" });
      } finally {
        this.loading = false;
      }
    },
    async fetchRoles() {
      try {
        const { data } = await api.get("/admin/roles/");
        this.roles = data.results || data;
      } catch (e) {
        this.roles = [];
      }
    },
    async toggleActive(user, value) {
      if (user.id === this.currentUserId) {
        this.$store.dispatch("notify", { message: "نمی‌توانید حساب کاربری خودتان را غیرفعال کنید.", type: "error" });
        return;
      }
      try {
        await api.patch(`/admin/users/${user.id}/`, { is_active: value });
        user.is_active = value;
        this.$store.dispatch("notify", { message: value ? "کاربر فعال شد." : "کاربر غیرفعال شد." });
      } catch (e) {
        this.$store.dispatch("notify", { message: "به‌روزرسانی ناموفق بود.", type: "error" });
      }
    },
    openEditor(user) {
      this.editorUser = user;
      this.selected = [...(user.groups || [])];
      this.errorMessage = "";
    },
    closeEditor() {
      this.editorUser = null;
      this.selected = [];
      this.errorMessage = "";
    },
    async saveAccess() {
      const user = this.editorUser;
      if (!user) return;
      this.saving = true;
      this.errorMessage = "";
      try {
        const { data } = await api.patch(`/admin/users/${user.id}/`, { groups: this.selected });
        const idx = this.users.findIndex((x) => x.id === user.id);
        if (idx !== -1) this.users.splice(idx, 1, data);
        const summary = CATEGORY_LABELS[this.userCategory(data)];
        this.$store.dispatch("notify", { message: `دسترسی‌های ${data.username} ذخیره شد (دسته: ${summary}).` });
        this.closeEditor();
      } catch (e) {
        const data = e.response && e.response.data;
        if (data && typeof data === "object") {
          this.errorMessage = Object.values(data).flat().join(" ");
        } else {
          this.errorMessage = "ذخیره دسترسی‌ها ناموفق بود. دوباره تلاش کنید.";
        }
      } finally {
        this.saving = false;
      }
    },
  },
};
</script>

<style scoped>
.admin-users h1 {
  font-size: 1.4rem;
  margin: 0 0 4px;
}
.page-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 16px;
}
.page-sub {
  font-size: 0.82rem;
  color: #6b7280;
  margin: 0;
}

/* Toolbar */
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  flex-wrap: wrap;
  margin-bottom: 14px;
}
.filter-tabs {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
.filter-tab {
  border: 1px solid #e5e7eb;
  background: #fff;
  border-radius: 999px;
  padding: 7px 14px;
  font-family: inherit;
  font-size: 0.8rem;
  font-weight: 600;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.15s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.filter-tab:hover {
  border-color: #c9a96e;
}
.filter-tab.active {
  background: linear-gradient(135deg, #1f4b43, #2e6b5e);
  border-color: #1f4b43;
  color: #fff;
}
.tab-count {
  background: rgba(0, 0, 0, 0.06);
  border-radius: 999px;
  padding: 1px 8px;
  font-size: 0.72rem;
}
.filter-tab.active .tab-count {
  background: rgba(255, 255, 255, 0.18);
}
.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #fff;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  padding: 8px 14px;
  min-width: 260px;
  transition: border-color 0.2s;
}
.search-box:focus-within {
  border-color: #c9a96e;
}
.search-box input {
  border: none;
  outline: none;
  font-family: inherit;
  font-size: 0.85rem;
  width: 100%;
  background: transparent;
}

/* Table */
.table-card {
  padding: 0;
  overflow: hidden;
}
.admin-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.86rem;
}
.admin-table th {
  text-align: right;
  color: #6b7280;
  font-weight: 700;
  padding: 12px 18px;
  background: #fafafb;
  border-bottom: 1.5px solid #ececf0;
  font-size: 0.78rem;
}
.admin-table td {
  padding: 14px 18px;
  border-bottom: 1px solid #f0f0f3;
  vertical-align: middle;
}
.admin-table tbody tr:last-child td {
  border-bottom: none;
}
.admin-table tbody tr:hover {
  background: #fafaf7;
}

/* User cell */
.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.95rem;
  flex-shrink: 0;
}
.avatar-green { background: linear-gradient(135deg, #1f4b43, #2e6b5e); }
.avatar-gold { background: linear-gradient(135deg, #b8904a, #d4b87a); }
.avatar-teal { background: linear-gradient(135deg, #0f766e, #14b8a6); }
.avatar-rose { background: linear-gradient(135deg, #9d3f5d, #d16b8d); }
.avatar-violet { background: linear-gradient(135deg, #5b4a94, #8b7bd8); }
.avatar-slate { background: linear-gradient(135deg, #475569, #94a3b8); }
.user-meta {
  min-width: 0;
}
.user-name {
  font-weight: 700;
  color: #111827;
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}
.user-id {
  font-size: 0.76rem;
  color: #9ca3af;
  direction: ltr;
  text-align: right;
}

/* Badges & chips */
.badge-superuser {
  background: linear-gradient(135deg, #b8904a, #d4b87a);
  color: #3b2c0c;
  font-size: 0.66rem;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 999px;
}
.roles-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}
.role-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.74rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 999px;
  white-space: nowrap;
}
.chip-academy {
  background: #e7f3ee;
  color: #1f5c45;
  border: 1px solid #bfe0d2;
}
.chip-shop {
  background: #fdf6e8;
  color: #8a6a1f;
  border: 1px solid #ecd9a8;
}
.chip-independent {
  background: #f3eefb;
  color: #6d3fa8;
  border: 1px solid #d9c9f0;
}
.role-section.section-independent {
  border-color: #d9c9f0;
  background: #fbf9fe;
}
.chip-none {
  background: #f1f2f4;
  color: #6b7280;
  border: 1px dashed #d1d5db;
}
.disabled-tag {
  margin-top: 6px;
  font-size: 0.7rem;
  font-weight: 700;
  color: #dc2626;
}
.date-cell {
  white-space: nowrap;
  font-size: 0.8rem;
}

/* Status switch */
.switch {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}
.switch input {
  cursor: pointer;
}
.switch-state {
  font-size: 0.78rem;
  font-weight: 700;
  color: #9ca3af;
  padding: 3px 10px;
  border-radius: 999px;
  background: #f3f4f6;
}
.switch-state.on {
  background: #d8f5e4;
  color: #1e7a48;
}

/* Access button */
.btn-access {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1px solid #d8d4c8;
  background: #fff;
  color: #4b3c14;
  border-radius: 9px;
  padding: 7px 12px;
  font-family: inherit;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}
.btn-access:hover {
  background: #fdf6e8;
  border-color: #c9a96e;
}
.actions-col {
  width: 150px;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}
.modal-panel {
  background: #fff;
  border-radius: 16px;
  width: 100%;
  max-width: 640px;
  max-height: 92vh;
  overflow-y: auto;
  padding: 24px;
  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.25);
}
.modal-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 6px;
}
.modal-head h3 {
  font-size: 1.05rem;
  margin: 0 0 6px;
  color: #111827;
}
.modal-sub {
  font-size: 0.8rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.7;
}
.modal-close {
  border: none;
  background: #f3f4f6;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  color: #6b7280;
  flex-shrink: 0;
}
.modal-close:hover {
  background: #fee2e2;
  color: #dc2626;
}

/* Role sections */
.role-sections {
  display: flex;
  flex-direction: column;
  gap: 18px;
  margin-top: 14px;
}
.role-section {
  border: 1px solid #ececf0;
  border-radius: 12px;
  padding: 16px;
}
.section-head {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 12px;
}
.section-icon {
  font-size: 1.2rem;
}
.section-head strong {
  font-size: 0.92rem;
  color: #111827;
}
.section-head p {
  font-size: 0.76rem;
  color: #6b7280;
  margin: 3px 0 0;
  line-height: 1.6;
}
.role-options {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 8px;
}
.role-option {
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  padding: 10px 12px;
  cursor: pointer;
  transition: all 0.15s;
  position: relative;
}
.role-option:hover {
  border-color: #c9a96e;
}
.role-option.selected {
  border-color: #2e6b5e;
  background: #f0faf5;
}
.role-option input {
  accent-color: #1f6b52;
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}
.option-icon {
  font-size: 1.15rem;
}
.option-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.option-text b {
  font-size: 0.84rem;
  color: #111827;
}
.option-text small {
  font-size: 0.7rem;
  color: #6b7280;
  line-height: 1.5;
}
.tag-custom {
  position: absolute;
  top: 6px;
  left: 8px;
  font-size: 0.62rem;
  font-weight: 700;
  color: #7c6a1e;
  background: #fdf6e8;
  border: 1px solid #ecd9a8;
  border-radius: 999px;
  padding: 1px 8px;
}
.section-empty {
  font-size: 0.78rem;
  margin: 4px 0;
}

/* Info note */
.plain-note {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  background: #f5f7f6;
  border-radius: 10px;
  padding: 12px 14px;
  font-size: 0.78rem;
  color: #374151;
  line-height: 1.8;
}
.plain-note p {
  margin: 0;
}
.note-icon {
  font-size: 1rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 18px;
  padding-top: 16px;
  border-top: 1px solid #ececf0;
}

.empty-row {
  text-align: center;
  padding: 34px;
}

/* Modal animation */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.18s ease;
}
.modal-enter,
.modal-leave-to {
  opacity: 0;
}

@media (max-width: 720px) {
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }
  .search-box {
    min-width: 0;
  }
  .admin-table {
    min-width: 640px;
  }
  .table-card {
    overflow-x: auto;
  }
}
</style>
