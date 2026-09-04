<template>
  <div class="admin-roles">
    <div class="page-head">
      <div>
        <h1>نقش‌ها و دسترسی‌ها</h1>
        <p class="page-sub">
          نقش‌های سیستمی (ثابت) با آیکون قفل مشخص شده‌اند: «مدیرکل» نقش مستقل و بالاتر از همه دسته‌هاست و «مدیر فروشگاه» هم به‌عنوان نقش سیستمی فروشگاه تعریف شده است. برای نیازهای خاص، نقش فروشگاهی جدید بسازید و از صفحه «کاربران» به افراد تخصیص دهید.
        </p>
      </div>
    </div>

    <div v-if="errorMessage" class="form-error-box global-error">{{ errorMessage }}</div>

    <!-- Create / edit form -->
    <div v-if="formOpen" class="card form-card">
      <h3>{{ editingId ? "ویرایش نقش" : "نقش فروشگاهی جدید" }}</h3>

      <div class="field">
        <label>نام نقش</label>
        <input v-model="form.name" type="text" placeholder="مثلاً پشتیبان فروشگاه" required />
      </div>

      <div class="field">
        <label>دسترسی‌ها</label>
        <p class="field-hint">فقط دسترسی‌هایی را تیک بزنید که این نقش باید ببیند؛ کاربر دارای این نقش، در پنل مدیریت فقط همین بخش‌ها را می‌بیند.</p>
        <div class="perm-groups">
          <div v-for="(perms, app) in permissionCatalogue" :key="app" class="perm-group">
            <div class="perm-group__head">
              <label>
                <input
                  type="checkbox"
                  :checked="isAppFullySelected(perms)"
                  @change="toggleApp(perms, $event.target.checked)"
                />
                <strong>{{ appLabel(app) }}</strong>
              </label>
            </div>
            <div class="perm-group__items">
              <label v-for="perm in perms" :key="perm.id" class="perm-item">
                <input type="checkbox" :value="perm.id" v-model="form.permission_ids" />
                {{ perm.name }}
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="form-actions">
        <button class="btn btn-outline btn-sm" @click="cancelForm">انصراف</button>
        <button class="btn btn-primary" :disabled="saving" @click="save">
          {{ saving ? "در حال ذخیره..." : "ذخیره نقش" }}
        </button>
      </div>
    </div>

    <!-- Independent roles (read-only) -->
    <div class="section-card card-independent">
      <div class="section-title">
        <span class="sec-icon">👑</span>
        <div>
          <h3>نقش‌های مستقل</h3>
          <p>نه زیرمجموعه آموزشگاه است و نه فروشگاه؛ بالاتر از همه دسته‌ها و با دسترسی کامل به پنل مدیریت.</p>
        </div>
      </div>
      <AppLoader v-if="loading" />
      <table v-else class="admin-table">
        <thead>
          <tr>
            <th>نقش</th>
            <th>دسته</th>
            <th>توضیح</th>
            <th>دسترسی‌ها</th>
            <th>کاربران</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="role in independentRoles" :key="role.id">
            <td>
              <span class="role-name"><span class="lock-icon">🔒</span> {{ roleIcon(role.name) }} {{ role.name }}</span>
            </td>
            <td>
              <span class="cat-chip cat-independent">👑 مستقل</span>
            </td>
            <td class="desc-cell">{{ role.description || "—" }}</td>
            <td>{{ role.permissions.length }}</td>
            <td>{{ role.user_count }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- System roles (read-only) -->
    <div class="section-card">
      <div class="section-title">
        <span class="sec-icon">🗂️</span>
        <div>
          <h3>نقش‌های سیستمی</h3>
          <p>از پیش تعریف‌شده و غیرقابل ویرایش؛ از صفحه «کاربران» تخصیص داده می‌شوند.</p>
        </div>
      </div>
      <AppLoader v-if="loading" />
      <table v-else class="admin-table">
        <thead>
          <tr>
            <th>نقش</th>
            <th>دسته</th>
            <th>توضیح</th>
            <th>دسترسی‌ها</th>
            <th>کاربران</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="role in systemRoles" :key="role.id">
            <td>
              <span class="role-name"><span class="lock-icon">🔒</span> {{ roleIcon(role.name) }} {{ role.name }}</span>
            </td>
            <td>
              <span class="cat-chip" :class="isAcademyRole(role) ? 'cat-academy' : 'cat-shop'">
                {{ isAcademyRole(role) ? "🎓 آموزشگاه" : "🏪 فروشگاه / بک‌آفیس" }}
              </span>
            </td>
            <td class="desc-cell">{{ role.description || "—" }}</td>
            <td>{{ role.permissions.length }}</td>
            <td>{{ role.user_count }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Custom roles (editable) -->
    <div class="section-card">
      <div class="section-title with-action">
        <div class="section-title-text">
          <span class="sec-icon">🧩</span>
          <div>
            <h3>نقش‌های سفارشی فروشگاه</h3>
            <p>ساخته‌شده توسط مدیر؛ برای مسئولیت‌های خاص (مثلاً پشتیبانی، انباردار اختصاصی و ...).</p>
          </div>
        </div>
        <button class="btn btn-primary btn-sm" @click="startCreate">+ نقش جدید</button>
      </div>
      <table v-if="customRoles.length" class="admin-table">
        <thead>
          <tr>
            <th>نام نقش</th>
            <th>تعداد دسترسی‌ها</th>
            <th>تعداد کاربران</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="role in customRoles" :key="role.id">
            <td class="name-cell">{{ role.name }}</td>
            <td>{{ role.permissions.length }}</td>
            <td>{{ role.user_count }}</td>
            <td class="actions-cell">
              <button class="btn btn-outline btn-sm" @click="startEdit(role)">ویرایش</button>
              <button class="btn btn-danger btn-sm" @click="remove(role)">حذف</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else-if="!loading" class="text-muted empty-row">
        هنوز نقش سفارشی ساخته نشده. با «نقش جدید» اولین نقش را بسازید.
      </p>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

const APP_LABELS = {
  accounts: "کاربران",
  products: "محصولات",
  cart: "سبد خرید",
  orders: "سفارش‌ها",
  dashboard: "داشبورد",
  vendors: "فروشندگان",
  access: "دسترسی‌ها",
  inventory: "انبارداری",
  accounting: "حسابداری",
  content: "محتوا (اسلایدر)",
  invoices: "فاکتورها",
  payments: "پرداخت‌ها",
};

const ROLE_ICONS = {
  "مدیرکل": "👑",
  "مدیر فروشگاه": "🏪",
  "هنرآموز": "🎓",
  "استاد": "👨‍🏫",
  "مدیر آموزشگاه": "🏛️",
  "حسابدار": "💰",
  "انباردار": "📦",
};

// نقش‌های آموزشگاه (ثابت) — دسته‌بندی حتی اگر API دسته را برنگرداند درست بماند
const ACADEMY_ROLE_NAMES = ["هنرآموز", "استاد", "مدیر آموزشگاه"];
// نقش‌های مستقل (نه آموزشگاه، نه فروشگاه)
const INDEPENDENT_ROLE_NAMES = ["مدیرکل", "مدیر کل"];
const normalizeRoleName = (s) => (s || "").replace(/\s+/g, "");

export default {
  name: "AdminRoles",
  components: { AppLoader },
  data() {
    return {
      roles: [],
      permissionCatalogue: {},
      loading: true,
      formOpen: false,
      saving: false,
      errorMessage: "",
      editingId: null,
      form: { name: "", permission_ids: [] },
    };
  },
  computed: {
    independentRoles() {
      return this.roles.filter((r) => r.is_system && this.isIndependentRole(r));
    },
    systemRoles() {
      return this.roles
        .filter((r) => r.is_system && !this.isIndependentRole(r))
        .sort((a, b) => (this.isAcademyRole(a) ? -1 : 1) - (this.isAcademyRole(b) ? -1 : 1));
    },
    customRoles() {
      return this.roles.filter((r) => !r.is_system);
    },
  },
  async created() {
    try {
      const [rolesRes, permsRes] = await Promise.all([
        api.get("/admin/roles/"),
        api.get("/admin/permissions/"),
      ]);
      this.roles = rolesRes.data.results || rolesRes.data;
      this.permissionCatalogue = permsRes.data;
    } catch (e) {
      this.errorMessage = "بارگذاری نقش‌ها ناموفق بود.";
    } finally {
      this.loading = false;
    }
  },
  methods: {
    roleIcon(name) {
      return ROLE_ICONS[name] || "🛠️";
    },
    isAcademyRole(role) {
      if (!role) return false;
      if (role.category === "academy") return true;
      return ACADEMY_ROLE_NAMES.includes(normalizeRoleName(role.name));
    },
    isIndependentRole(role) {
      if (!role) return false;
      if (role.category === "independent") return true;
      return INDEPENDENT_ROLE_NAMES.includes(normalizeRoleName(role.name));
    },
    appLabel(app) {
      return APP_LABELS[app] || app;
    },
    isAppFullySelected(perms) {
      return perms.every((p) => this.form.permission_ids.includes(p.id));
    },
    toggleApp(perms, checked) {
      const ids = perms.map((p) => p.id);
      if (checked) {
        this.form.permission_ids = [...new Set([...this.form.permission_ids, ...ids])];
      } else {
        this.form.permission_ids = this.form.permission_ids.filter((id) => !ids.includes(id));
      }
    },
    startCreate() {
      this.editingId = null;
      this.form = { name: "", permission_ids: [] };
      this.errorMessage = "";
      this.formOpen = true;
    },
    startEdit(role) {
      this.editingId = role.id;
      this.form = { name: role.name, permission_ids: role.permissions.map((p) => p.id) };
      this.errorMessage = "";
      this.formOpen = true;
    },
    cancelForm() {
      this.formOpen = false;
    },
    async save() {
      this.saving = true;
      this.errorMessage = "";
      try {
        if (this.editingId) {
          const { data } = await api.patch(`/admin/roles/${this.editingId}/`, this.form);
          const idx = this.roles.findIndex((r) => r.id === this.editingId);
          this.roles.splice(idx, 1, data);
          this.$store.dispatch("notify", { message: "نقش به‌روزرسانی شد." });
        } else {
          const { data } = await api.post("/admin/roles/", this.form);
          this.roles.push(data);
          this.$store.dispatch("notify", { message: "نقش جدید ساخته شد." });
        }
        this.formOpen = false;
      } catch (e) {
        const data = e.response && e.response.data;
        if (data && typeof data === "object") {
          this.errorMessage = Object.values(data).flat().join(" ");
        } else {
          this.errorMessage = "ذخیره نقش ناموفق بود.";
        }
      } finally {
        this.saving = false;
      }
    },
    async remove(role) {
      if (!confirm(`نقش «${role.name}» حذف شود؟ کاربرانی که این نقش را دارند، دسترسی‌های آن را از دست می‌دهند.`)) return;
      try {
        await api.delete(`/admin/roles/${role.id}/`);
        this.roles = this.roles.filter((r) => r.id !== role.id);
        this.$store.dispatch("notify", { message: "نقش حذف شد." });
      } catch (e) {
        this.$store.dispatch("notify", { message: "حذف ناموفق بود.", type: "error" });
      }
    },
  },
};
</script>

<style scoped>
.page-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 16px;
}
.page-head h1 {
  font-size: 1.4rem;
  margin: 0 0 4px;
}
.page-sub {
  font-size: 0.82rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.8;
  max-width: 720px;
}
.global-error {
  margin-bottom: 14px;
}
.form-card {
  padding: 24px;
  margin-bottom: 20px;
  max-width: 760px;
}
.form-card h3 {
  font-size: 1rem;
  margin-bottom: 16px;
}
.field-hint {
  font-size: 0.78rem;
  color: #6b7280;
  margin: -6px 0 10px;
  line-height: 1.7;
}
.perm-groups {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 420px;
  overflow-y: auto;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 12px;
}
.perm-group {
  border-bottom: 1px dashed var(--color-border);
  padding-bottom: 10px;
}
.perm-group:last-child {
  border-bottom: none;
  padding-bottom: 0;
}
.perm-group__head label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.88rem;
  margin-bottom: 8px;
}
.perm-group__items {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 6px;
  padding-right: 22px;
}
.perm-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  color: var(--color-text-muted);
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 16px;
}

/* Sections */
.section-card {
  background: #fff;
  border: 1px solid #ececf0;
  border-radius: 14px;
  padding: 20px;
  margin-bottom: 20px;
}
.section-title {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 16px;
}
.section-title.with-action {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
.section-title-text {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}
.sec-icon {
  font-size: 1.25rem;
}
.section-title h3 {
  font-size: 0.98rem;
  margin: 0 0 3px;
  color: #111827;
}
.section-title p {
  font-size: 0.76rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.7;
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
  padding: 10px 12px;
  background: #fafafb;
  border-bottom: 1.5px solid #ececf0;
  font-size: 0.76rem;
}
.admin-table td {
  padding: 12px;
  border-bottom: 1px solid #f0f0f3;
  vertical-align: middle;
}
.admin-table tbody tr:last-child td {
  border-bottom: none;
}
.role-name {
  font-weight: 700;
  color: #111827;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.lock-icon {
  font-size: 0.85rem;
  opacity: 0.7;
}
.cat-chip {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 999px;
  white-space: nowrap;
}
.cat-academy {
  background: #e7f3ee;
  color: #1f5c45;
}
.cat-shop {
  background: #fdf6e8;
  color: #8a6a1f;
}
.cat-independent {
  background: #f3eefb;
  color: #6d3fa8;
}
.card-independent {
  border-color: #d9c9f0;
  background: linear-gradient(180deg, #fbf9fe, #fff);
}
.desc-cell {
  color: #6b7280;
  font-size: 0.8rem;
  max-width: 340px;
}
.name-cell {
  font-weight: 700;
}
.actions-cell {
  display: flex;
  gap: 8px;
}
.empty-row {
  text-align: center;
  padding: 24px;
  margin: 0;
}
</style>
