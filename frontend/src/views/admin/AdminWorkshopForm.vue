<template>
  <div class="admin-workshop-form">
    <div class="page-head">
      <h1>{{ isEdit ? "ویرایش کارگاه" : "کارگاه جدید" }}</h1>
      <router-link to="/admin/workshops-admin" class="btn btn-outline btn-sm">بازگشت به لیست</router-link>
    </div>

    <AppLoader v-if="loading" />

    <form v-else class="card form-card" @submit.prevent="submit">
      <div v-if="errorMessage" class="form-error-box">{{ errorMessage }}</div>

      <h3 class="section-title">اطلاعات پایه</h3>
      <div class="two-col">
        <div class="field">
          <label>عنوان کارگاه <span class="req">*</span></label>
          <input v-model="form.title" type="text" required />
        </div>
        <div class="field">
          <label>دسته‌بندی</label>
          <select v-model="form.category">
            <option :value="null">بدون دسته</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>
      </div>

      <div class="two-col">
        <div class="field">
          <label>مدرس</label>
          <select v-model="form.instructor">
            <option :value="null">بدون مدرس</option>
            <option v-for="i in instructors" :key="i.id" :value="i.id">{{ i.display_name }}</option>
          </select>
        </div>
        <div class="field">
          <label>توضیحات کوتاه</label>
          <input v-model="form.short_description" type="text" maxlength="300" />
        </div>
      </div>

      <div class="field">
        <label>توضیحات کامل کارگاه</label>
        <textarea v-model="form.description" rows="5"></textarea>
      </div>

      <div class="three-col">
        <div class="field">
          <label>نوع مدت</label>
          <select v-model="form.duration_type">
            <option value="short">کوتاه‌مدت</option>
            <option value="long">بلندمدت</option>
            <option value="one">تک جلسه‌ای</option>
            <option value="intensive">فشرده</option>
          </select>
        </div>
        <div class="field">
          <label>وضعیت</label>
          <select v-model="form.status">
            <option value="upcoming">پیش رو</option>
            <option value="ongoing">در حال برگزاری</option>
            <option value="completed">تکمیل شده</option>
            <option value="cancelled">لغو شده</option>
          </select>
        </div>
        <div class="field">
          <label>تعداد جلسات</label>
          <input v-model.number="form.sessions_count" type="number" min="1" />
        </div>
      </div>

      <h3 class="section-title">زمان‌بندی</h3>
      <div class="three-col">
        <div class="field">
          <label>تاریخ شروع <span class="req">*</span></label>
          <input v-model="form.start_date" type="date" required />
        </div>
        <div class="field">
          <label>تاریخ پایان (اختیاری)</label>
          <input v-model="form.end_date" type="date" />
        </div>
        <div class="field">
          <label>محل برگزاری</label>
          <input v-model="form.location" type="text" />
        </div>
      </div>

      <div class="three-col">
        <div class="field">
          <label>ساعت شروع <span class="req">*</span></label>
          <input v-model="form.start_time" type="time" required />
        </div>
        <div class="field">
          <label>ساعت پایان <span class="req">*</span></label>
          <input v-model="form.end_time" type="time" required />
        </div>
        <div class="field">
          <label>قیمت (تومان)</label>
          <input v-model.number="form.price" type="number" min="0" />
        </div>
      </div>

      <div class="two-col">
        <div class="field">
          <label>حداکثر شرکت‌کننده</label>
          <input v-model.number="form.max_participants" type="number" min="1" />
        </div>
        <div class="field">
          <label>پیش‌نیازها</label>
          <input v-model="form.prerequisites" type="text" />
        </div>
      </div>

      <div class="field">
        <label>وسایل مورد نیاز</label>
        <textarea v-model="form.materials" rows="3"></textarea>
      </div>

      <h3 class="section-title">تصاویر</h3>
      <div class="two-col">
        <div class="field">
          <label>تصویر بندانگشتی</label>
          <img v-if="thumbPreview" :src="thumbPreview" class="image-preview" />
          <input type="file" accept="image/*" @change="onFile($event, 'thumbnail')" />
        </div>
        <div class="field">
          <label>تصویر کاور</label>
          <img v-if="coverPreview" :src="coverPreview" class="image-preview" />
          <input type="file" accept="image/*" @change="onFile($event, 'cover')" />
        </div>
      </div>

      <div class="checkbox-row">
        <label><input v-model="form.is_online" type="checkbox" /> آنلاین</label>
        <label><input v-model="form.is_featured" type="checkbox" /> کارگاه ویژه</label>
        <label><input v-model="form.is_active" type="checkbox" /> فعال / قابل نمایش</label>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary" :disabled="submitting">
          {{ submitting ? "در حال ذخیره..." : (isEdit ? "ذخیره تغییرات" : "ایجاد کارگاه") }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

const emptyForm = () => ({
  title: "",
  category: null,
  instructor: null,
  short_description: "",
  description: "",
  duration_type: "short",
  status: "upcoming",
  start_date: "",
  end_date: "",
  start_time: "",
  end_time: "",
  sessions_count: 1,
  price: 0,
  max_participants: 20,
  location: "",
  prerequisites: "",
  materials: "",
  is_online: false,
  is_featured: false,
  is_active: true,
});

export default {
  name: "AdminWorkshopForm",
  components: { AppLoader },
  data() {
    return {
      loading: true,
      submitting: false,
      errorMessage: "",
      categories: [],
      instructors: [],
      form: emptyForm(),
      thumbnailFile: null,
      coverFile: null,
      thumbPreview: "",
      coverPreview: "",
    };
  },
  computed: {
    isEdit() {
      return !!this.$route.params.id;
    },
  },
  created() {
    this.loadForm();
  },
  watch: {
    "$route.params.id"() {
      this.loadForm();
    },
  },
  methods: {
    onFile(event, kind) {
      const file = event.target.files[0];
      if (!file) return;
      if (kind === "thumbnail") {
        this.thumbnailFile = file;
        this.thumbPreview = URL.createObjectURL(file);
      } else {
        this.coverFile = file;
        this.coverPreview = URL.createObjectURL(file);
      }
    },
    async loadForm() {
      this.loading = true;
      this.errorMessage = "";
      try {
        const [catRes, instRes] = await Promise.all([
          api.get("/workshops/categories/"),
          api.get("/instructors/"),
        ]);
        this.categories = catRes.data.results || catRes.data;
        this.instructors = instRes.data.results || instRes.data;

        if (this.isEdit) {
          const { data: ws } = await api.get(`/workshops/${this.$route.params.id}/`);
          this.form = {
            title: ws.title || "",
            category: ws.category ? ws.category.id : null,
            instructor: ws.instructor || null,
            short_description: ws.short_description || "",
            description: ws.description || "",
            duration_type: ws.duration_type || "short",
            status: ws.status || "upcoming",
            start_date: ws.start_date || "",
            end_date: ws.end_date || "",
            start_time: ws.start_time || "",
            end_time: ws.end_time || "",
            sessions_count: ws.sessions_count || 1,
            price: Number(ws.price) || 0,
            max_participants: ws.max_participants || 20,
            location: ws.location || "",
            prerequisites: ws.prerequisites || "",
            materials: ws.materials || "",
            is_online: !!ws.is_online,
            is_featured: !!ws.is_featured,
            is_active: ws.is_active !== undefined ? ws.is_active : true,
          };
          this.thumbnailFile = null;
          this.coverFile = null;
          this.thumbPreview = ws.thumbnail || "";
          this.coverPreview = ws.cover_image || "";
        } else {
          this.form = emptyForm();
          this.thumbnailFile = null;
          this.coverFile = null;
          this.thumbPreview = "";
          this.coverPreview = "";
        }
      } catch (e) {
        this.errorMessage = "بارگذاری اطلاعات ناموفق بود. اتصال به سرور را بررسی کنید.";
      } finally {
        this.loading = false;
      }
    },
    buildFormData() {
      const fd = new FormData();
      const f = this.form;
      fd.append("title", f.title);
      fd.append("description", f.description);
      if (f.category) fd.append("category", f.category);
      if (f.instructor) fd.append("instructor", f.instructor);
      if (f.short_description) fd.append("short_description", f.short_description);
      fd.append("duration_type", f.duration_type);
      fd.append("status", f.status);
      fd.append("start_date", f.start_date);
      if (f.end_date) fd.append("end_date", f.end_date);
      fd.append("start_time", f.start_time);
      fd.append("end_time", f.end_time);
      fd.append("sessions_count", f.sessions_count);
      fd.append("price", f.price);
      fd.append("max_participants", f.max_participants);
      if (f.location) fd.append("location", f.location);
      if (f.prerequisites) fd.append("prerequisites", f.prerequisites);
      if (f.materials) fd.append("materials", f.materials);
      fd.append("is_online", f.is_online ? "true" : "false");
      fd.append("is_featured", f.is_featured ? "true" : "false");
      fd.append("is_active", f.is_active ? "true" : "false");
      if (this.thumbnailFile) fd.append("thumbnail", this.thumbnailFile);
      if (this.coverFile) fd.append("cover_image", this.coverFile);
      return fd;
    },
    async submit() {
      this.submitting = true;
      this.errorMessage = "";
      try {
        const fd = this.buildFormData();
        if (this.isEdit) {
          await api.patch(`/workshops/${this.$route.params.id}/`, fd);
          this.$store.dispatch("notify", { message: "کارگاه با موفقیت به‌روزرسانی شد." });
        } else {
          await api.post("/workshops/", fd);
          this.$store.dispatch("notify", { message: "کارگاه با موفقیت ایجاد شد." });
        }
        this.$router.push("/admin/workshops-admin");
      } catch (e) {
        console.error("خطای ذخیره کارگاه:", e);
        let detail = "";
        if (e.response && e.response.data) {
          if (typeof e.response.data === "string") {
            detail = e.response.data;
          } else if (typeof e.response.data === "object") {
            detail = Object.values(e.response.data).flat().join(" — ");
          }
        } else if (e.message) {
          detail = e.message;
        }
        this.errorMessage = `ذخیره کارگاه ناموفق بود. ${detail}`.trim();
      } finally {
        this.submitting = false;
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
  padding: 26px;
  max-width: 860px;
}
.section-title {
  font-size: 0.95rem;
  font-weight: 800;
  color: #1f2937;
  margin: 26px 0 14px;
  padding-bottom: 8px;
  border-bottom: 1.5px solid var(--color-border);
}
.two-col {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 16px;
}
.three-col {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
}
.checkbox-row {
  display: flex;
  gap: 24px;
  margin: 22px 0;
  font-size: 0.88rem;
  flex-wrap: wrap;
}
.checkbox-row label {
  display: flex;
  align-items: center;
  gap: 6px;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
}
.image-preview {
  width: 100%;
  max-height: 160px;
  object-fit: cover;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
  margin-bottom: 8px;
}
.req {
  color: var(--color-danger);
}
</style>