<template>
  <div class="admin-course-form">
    <div class="page-head">
      <h1>{{ isEdit ? "ویرایش دوره" : "دوره جدید" }}</h1>
      <router-link to="/admin/courses" class="btn btn-outline btn-sm">بازگشت به لیست</router-link>
    </div>

    <AppLoader v-if="loading" />

    <form v-else class="card form-card" @submit.prevent="submit">
      <div v-if="errorMessage" class="form-error-box">{{ errorMessage }}</div>

      <h3 class="section-title">اطلاعات پایه</h3>
      <div class="two-col">
        <div class="field">
          <label>عنوان دوره <span class="req">*</span></label>
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
          <label>استاد</label>
          <select v-model="form.instructor">
            <option :value="null">بدون استاد</option>
            <option v-for="i in instructors" :key="i.id" :value="i.id">{{ i.display_name }}</option>
          </select>
        </div>
        <div class="field">
          <label>توضیحات کوتاه</label>
          <input v-model="form.short_description" type="text" maxlength="300" />
        </div>
      </div>

      <div class="field">
        <label>توضیحات کامل دوره</label>
        <textarea v-model="form.description" rows="5"></textarea>
      </div>

      <div class="three-col">
        <div class="field">
          <label>سطح</label>
          <select v-model="form.level">
            <option value="beginner">مبتدی</option>
            <option value="intermediate">متوسط</option>
            <option value="advanced">پیشرفته</option>
            <option value="all">همه سطوح</option>
          </select>
        </div>
        <div class="field">
          <label>نوع قیمت‌گذاری</label>
          <select v-model="form.pricing_type">
            <option value="single">تک دوره</option>
            <option value="subscription">اشتراک ماهانه</option>
            <option value="both">هر دو</option>
          </select>
        </div>
        <div class="field">
          <label>وضعیت</label>
          <select v-model="form.status">
            <option value="draft">پیش‌نویس</option>
            <option value="published">منتشر شده</option>
            <option value="archived">بایگانی</option>
          </select>
        </div>
      </div>

      <h3 class="section-title">قیمت و ظرفیت</h3>
      <div class="three-col">
        <div class="field">
          <label>قیمت (تومان)</label>
          <input v-model.number="form.price" type="number" min="0" />
        </div>
        <div class="field">
          <label>قیمت با تخفیف (اختیاری)</label>
          <input v-model.number="form.discount_price" type="number" min="0" />
        </div>
        <div class="field">
          <label>قیمت اشتراک ماهانه (اختیاری)</label>
          <input v-model.number="form.subscription_price" type="number" min="0" />
        </div>
      </div>

      <div class="three-col">
        <div class="field">
          <label>مدت دوره (هفته)</label>
          <input v-model.number="form.duration_weeks" type="number" min="1" />
        </div>
        <div class="field">
          <label>جلسات در هفته</label>
          <input v-model.number="form.sessions_per_week" type="number" min="1" />
        </div>
        <div class="field">
          <label>مدت هر جلسه (دقیقه)</label>
          <input v-model.number="form.session_duration_minutes" type="number" min="1" />
        </div>
      </div>

      <div class="two-col">
        <div class="field">
          <label>حداکثر ظرفیت</label>
          <input v-model.number="form.max_students" type="number" min="1" />
        </div>
        <div class="field">
          <label>لینک ویدیو معرفی (اختیاری)</label>
          <input v-model="form.promo_video_url" type="url" />
        </div>
      </div>

      <h3 class="section-title">محتوا</h3>
      <div class="two-col">
        <div class="field">
          <label>پیش‌نیازها</label>
          <textarea v-model="form.prerequisites" rows="3"></textarea>
        </div>
        <div class="field">
          <label>وسایل مورد نیاز</label>
          <textarea v-model="form.materials_needed" rows="3"></textarea>
        </div>
      </div>

      <div class="field">
        <label>چه چیزی یاد می‌گیرید (هر مورد در یک خط)</label>
        <textarea v-model="form.what_you_learn" rows="4" placeholder="مثلاً:&#10;ترکیب‌بندی در نقاشی&#10;رنگ‌شناسی پیشرفته"></textarea>
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
        <label><input v-model="form.is_featured" type="checkbox" /> دوره ویژه</label>
        <label><input v-model="form.is_active" type="checkbox" /> فعال / قابل نمایش</label>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary" :disabled="submitting">
          {{ submitting ? "در حال ذخیره..." : (isEdit ? "ذخیره تغییرات" : "ایجاد دوره") }}
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
  level: "all",
  status: "draft",
  pricing_type: "single",
  price: 0,
  subscription_price: null,
  discount_price: null,
  duration_weeks: 1,
  sessions_per_week: 1,
  session_duration_minutes: 90,
  max_students: 20,
  prerequisites: "",
  what_you_learn: "",
  materials_needed: "",
  promo_video_url: "",
  is_featured: false,
  is_active: true,
});

export default {
  name: "AdminCourseForm",
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
          api.get("/courses/categories/"),
          api.get("/instructors/"),
        ]);
        this.categories = catRes.data.results || catRes.data;
        this.instructors = instRes.data.results || instRes.data;

        if (this.isEdit) {
          const { data: course } = await api.get(`/courses/${this.$route.params.id}/`);
          this.form = {
            title: course.title || "",
            category: course.category ? course.category.id : null,
            instructor: course.instructor || null,
            short_description: course.short_description || "",
            description: course.description || "",
            level: course.level || "all",
            status: course.status || "draft",
            pricing_type: course.pricing_type || "single",
            price: Number(course.price) || 0,
            subscription_price: course.subscription_price != null ? Number(course.subscription_price) : null,
            discount_price: course.discount_price != null ? Number(course.discount_price) : null,
            duration_weeks: course.duration_weeks || 1,
            sessions_per_week: course.sessions_per_week || 1,
            session_duration_minutes: course.session_duration_minutes || 90,
            max_students: course.max_students || 20,
            prerequisites: course.prerequisites || "",
            what_you_learn: Array.isArray(course.what_you_learn) ? course.what_you_learn.join("\n") : "",
            materials_needed: course.materials_needed || "",
            promo_video_url: course.promo_video_url || "",
            is_featured: !!course.is_featured,
            is_active: course.is_active !== undefined ? course.is_active : true,
          };
          this.thumbnailFile = null;
          this.coverFile = null;
          this.thumbPreview = course.thumbnail || "";
          this.coverPreview = course.cover_image || "";
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
      fd.append("level", f.level);
      fd.append("status", f.status);
      fd.append("pricing_type", f.pricing_type);
      fd.append("price", f.price);
      if (f.subscription_price !== null && f.subscription_price !== "") fd.append("subscription_price", f.subscription_price);
      if (f.discount_price !== null && f.discount_price !== "") fd.append("discount_price", f.discount_price);
      fd.append("duration_weeks", f.duration_weeks);
      fd.append("sessions_per_week", f.sessions_per_week);
      fd.append("session_duration_minutes", f.session_duration_minutes);
      fd.append("max_students", f.max_students);
      if (f.prerequisites) fd.append("prerequisites", f.prerequisites);
      if (f.materials_needed) fd.append("materials_needed", f.materials_needed);
      fd.append(
        "what_you_learn",
        JSON.stringify(f.what_you_learn.split("\n").map((s) => s.trim()).filter(Boolean))
      );
      if (f.promo_video_url) fd.append("promo_video_url", f.promo_video_url);
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
          await api.patch(`/courses/${this.$route.params.id}/`, fd);
          this.$store.dispatch("notify", { message: "دوره با موفقیت به‌روزرسانی شد." });
        } else {
          await api.post("/courses/", fd);
          this.$store.dispatch("notify", { message: "دوره با موفقیت ایجاد شد." });
        }
        this.$router.push("/admin/courses");
      } catch (e) {
        console.error("خطای ذخیره دوره:", e);
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
        this.errorMessage = `ذخیره دوره ناموفق بود. ${detail}`.trim();
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