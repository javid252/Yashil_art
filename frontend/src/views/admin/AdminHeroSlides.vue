<template>
  <div class="admin-hero-slides">
    <div class="page-head">
      <h1>اسلایدر صفحه اصلی</h1>
      <button class="btn btn-primary btn-sm" @click="startCreate">+ اسلاید جدید</button>
    </div>

    <div v-if="formOpen" class="card form-card">
      <h3>{{ editingId ? "ویرایش اسلاید" : "اسلاید جدید" }}</h3>
      <div v-if="errorMessage" class="form-error-box">{{ errorMessage }}</div>

      <div class="logo-row">
        <div class="logo-preview">
          <img v-if="imagePreview" :src="imagePreview" alt="تصویر اسلاید" />
          <span v-else>🖼️</span>
        </div>
        <div>
          <input type="file" accept="image/*" @change="onImageSelected" />
          <p class="text-muted logo-hint">اندازه پیشنهادی: حدود ۱۹۲۰×۸۰۰ پیکسل (عرض‌گونه).</p>
        </div>
      </div>

      <div class="field">
        <label>لیبل بالای عنوان (اختیاری)</label>
        <input v-model="form.label" type="text" placeholder="مثلاً «فروشگاه آنلاین یاشیل آرت»" />
      </div>

      <div class="field">
        <label>متن بزرگ (تیتر)</label>
        <input v-model="form.title" type="text" required placeholder="مثلاً «هر خرید، آغاز یک مسیر مطمئن»" />
      </div>

      <div class="field">
        <label>متن کوچک (توضیح)</label>
        <textarea v-model="form.description" rows="2"></textarea>
      </div>

      <div class="two-col">
        <div class="field">
          <label>متن دکمه اول</label>
          <input v-model="form.primary_button_text" type="text" placeholder="مشاهده محصولات" />
        </div>
        <div class="field">
          <label>لینک دکمه اول</label>
          <input v-model="form.primary_button_link" type="text" placeholder="/products یا https://..." />
        </div>
      </div>

      <div class="two-col">
        <div class="field">
          <label>متن دکمه دوم</label>
          <input v-model="form.secondary_button_text" type="text" placeholder="پیشنهادهای ویژه" />
        </div>
        <div class="field">
          <label>لینک دکمه دوم</label>
          <input v-model="form.secondary_button_link" type="text" placeholder="/products?featured=1" />
        </div>
      </div>

      <div class="two-col">
        <div class="field">
          <label>ترتیب نمایش</label>
          <input v-model.number="form.order" type="number" min="0" />
        </div>
        <div class="field checkbox-field">
          <label><input v-model="form.is_active" type="checkbox" /> فعال / نمایش در سایت</label>
        </div>
      </div>

      <div class="form-actions">
        <button class="btn btn-outline btn-sm" @click="cancelForm">انصراف</button>
        <button class="btn btn-primary" :disabled="saving" @click="save">
          {{ saving ? "در حال ذخیره..." : "ذخیره" }}
        </button>
      </div>
    </div>

    <div class="card table-card">
      <AppLoader v-if="loading" />
      <table v-else class="admin-table">
        <thead>
          <tr>
            <th>تصویر</th>
            <th>عنوان</th>
            <th>ترتیب</th>
            <th>وضعیت</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in slides" :key="s.id">
            <td>
              <div class="row-thumb">
                <img :src="s.image" :alt="s.title" />
              </div>
            </td>
            <td class="name-cell">{{ s.title }}</td>
            <td>{{ s.order }}</td>
            <td>
              <span class="badge" :class="s.is_active ? 'badge-status-paid' : 'badge-status-cancelled'">
                {{ s.is_active ? "فعال" : "غیرفعال" }}
              </span>
            </td>
            <td class="actions-cell">
              <button class="btn btn-outline btn-sm" @click="startEdit(s)">ویرایش</button>
              <button class="btn btn-danger btn-sm" @click="remove(s)">حذف</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="!loading && slides.length === 0" class="text-muted empty-row">هنوز اسلایدی ثبت نشده.</p>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

const EMPTY_FORM = {
  label: "", title: "", description: "",
  primary_button_text: "", primary_button_link: "",
  secondary_button_text: "", secondary_button_link: "",
  order: 0, is_active: true,
};

export default {
  name: "AdminHeroSlides",
  components: { AppLoader },
  data() {
    return {
      slides: [],
      loading: true,
      formOpen: false,
      saving: false,
      errorMessage: "",
      editingId: null,
      form: { ...EMPTY_FORM },
      imageFile: null,
      imagePreview: null,
    };
  },
  created() {
    this.fetchSlides();
  },
  methods: {
    async fetchSlides() {
      this.loading = true;
      try {
        const { data } = await api.get("/content/hero-slides/", { params: { page_size: 100 } });
        this.slides = data.results || data;
      } finally {
        this.loading = false;
      }
    },
    startCreate() {
      this.editingId = null;
      this.form = { ...EMPTY_FORM };
      this.imageFile = null;
      this.imagePreview = null;
      this.errorMessage = "";
      this.formOpen = true;
    },
    startEdit(slide) {
      this.editingId = slide.id;
      this.form = {
        label: slide.label, title: slide.title, description: slide.description,
        primary_button_text: slide.primary_button_text, primary_button_link: slide.primary_button_link,
        secondary_button_text: slide.secondary_button_text, secondary_button_link: slide.secondary_button_link,
        order: slide.order, is_active: slide.is_active,
      };
      this.imageFile = null;
      this.imagePreview = slide.image;
      this.errorMessage = "";
      this.formOpen = true;
    },
    cancelForm() {
      this.formOpen = false;
    },
    onImageSelected(event) {
      const file = event.target.files[0];
      if (!file) return;
      this.imageFile = file;
      this.imagePreview = URL.createObjectURL(file);
    },
    buildFormData() {
      const formData = new FormData();
      Object.entries(this.form).forEach(([key, value]) => {
        if (value !== null && value !== undefined) formData.append(key, value);
      });
      if (this.imageFile) formData.append("image", this.imageFile);
      return formData;
    },
    async save() {
      if (!this.editingId && !this.imageFile) {
        this.errorMessage = "برای اسلاید جدید، انتخاب تصویر الزامی است.";
        return;
      }
      this.saving = true;
      this.errorMessage = "";
      try {
        const formData = this.buildFormData();
        if (this.editingId) {
          await api.patch(`/content/hero-slides/${this.editingId}/`, formData);
          this.$store.dispatch("notify", { message: "اسلاید به‌روزرسانی شد." });
        } else {
          await api.post("/content/hero-slides/", formData);
          this.$store.dispatch("notify", { message: "اسلاید جدید ثبت شد." });
        }
        this.formOpen = false;
        await this.fetchSlides();
      } catch (e) {
        this.errorMessage = "ذخیره ناموفق بود. مقادیر را بررسی کنید.";
      } finally {
        this.saving = false;
      }
    },
    async remove(slide) {
      if (!confirm(`اسلاید «${slide.title}» حذف شود؟`)) return;
      try {
        await api.delete(`/content/hero-slides/${slide.id}/`);
        this.$store.dispatch("notify", { message: "اسلاید حذف شد." });
        this.fetchSlides();
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
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.page-head h1 {
  font-size: 1.4rem;
}
.form-card {
  padding: 24px;
  margin-bottom: 20px;
  max-width: 720px;
}
.form-card h3 {
  font-size: 1rem;
  margin-bottom: 16px;
}
.logo-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 18px;
  border-bottom: 1px dashed var(--color-border);
}
.logo-preview {
  width: 96px;
  height: 60px;
  border-radius: var(--radius-sm);
  background: var(--color-sand);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-size: 1.6rem;
  flex-shrink: 0;
}
.logo-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.logo-hint {
  font-size: 0.78rem;
  margin-top: 6px;
}
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.checkbox-field {
  display: flex;
  align-items: center;
}
.checkbox-field label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.88rem;
  margin-bottom: 0;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
.table-card {
  padding: 18px;
  overflow-x: auto;
}
.admin-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.87rem;
}
.admin-table th {
  text-align: right;
  color: var(--color-text-muted);
  font-weight: 700;
  padding: 10px 12px;
  border-bottom: 1.5px solid var(--color-border);
  font-size: 0.8rem;
}
.admin-table td {
  padding: 10px 12px;
  border-bottom: 1px solid var(--color-border);
  vertical-align: middle;
}
.row-thumb {
  width: 90px;
  height: 40px;
  border-radius: var(--radius-sm);
  background: var(--color-sand);
  overflow: hidden;
}
.row-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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
  padding: 30px;
}
</style>