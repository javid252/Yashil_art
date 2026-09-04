<template>
  <div class="admin-instructor-form">
    <div class="page-head">
      <h1>{{ isEdit ? "ویرایش استاد" : "استاد جدید" }}</h1>
      <router-link to="/admin/instructors" class="btn btn-outline btn-sm">بازگشت به لیست</router-link>
    </div>

    <AppLoader v-if="loading" />

    <form v-else class="card form-card" @submit.prevent="submit">
      <div v-if="errorMessage" class="form-error-box">{{ errorMessage }}</div>

      <div class="two-col">
        <div class="field">
          <label>نام نمایشی <span class="req">*</span></label>
          <input v-model="form.display_name" type="text" required />
        </div>
        <div class="field">
          <label>سال‌های تجربه</label>
          <input v-model.number="form.years_experience" type="number" min="0" />
        </div>
      </div>

      <div class="field">
        <label>بیوگرافی</label>
        <textarea v-model="form.bio" rows="5"></textarea>
      </div>

      <div class="field">
        <label>تخصص‌ها (هر مورد در یک خط)</label>
        <textarea
          v-model="form.specializations"
          rows="4"
          placeholder="مثلاً:&#10;نقاشی رنگ روغن&#10;طراحی فیگوراتیو"
        ></textarea>
      </div>

      <div class="three-col">
        <div class="field">
          <label>تعداد دانشجو</label>
          <input v-model.number="form.students_count" type="number" min="0" />
        </div>
        <div class="field">
          <label>امتیاز (۰ تا ۵)</label>
          <input v-model.number="form.rating" type="number" min="0" max="5" step="0.1" />
        </div>
        <div class="field">
          <label>وب‌سایت شخصی</label>
          <input v-model="form.website" type="url" />
        </div>
      </div>

      <div class="two-col">
        <div class="field">
          <label>اینستاگرام</label>
          <input v-model="form.instagram" type="text" placeholder="مثلاً yashil_art" />
        </div>
        <div class="field">
          <label>تلگرام</label>
          <input v-model="form.telegram" type="text" placeholder="مثلاً @yashil_art" />
        </div>
      </div>

      <div class="two-col">
        <div class="field">
          <label>عکس پروفایل</label>
          <img v-if="photoPreview" :src="photoPreview" class="image-preview" />
          <input type="file" accept="image/*" @change="onPhoto" />
        </div>
        <div class="field">
          <label>فایل رزومه</label>
          <p v-if="form.resume_name" class="resume-name">📄 {{ form.resume_name }}</p>
          <input type="file" accept=".pdf,.doc,.docx" @change="onResume" />
        </div>
      </div>

      <div class="checkbox-row">
        <label><input v-model="form.is_featured" type="checkbox" /> استاد ویژه</label>
        <label><input v-model="form.is_active" type="checkbox" /> فعال / قابل نمایش</label>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary" :disabled="submitting">
          {{ submitting ? "در حال ذخیره..." : (isEdit ? "ذخیره تغییرات" : "ایجاد استاد") }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

const emptyForm = () => ({
  display_name: "",
  bio: "",
  specializations: "",
  photo: null,
  resume: null,
  website: "",
  instagram: "",
  telegram: "",
  years_experience: 0,
  students_count: 0,
  rating: 0,
  is_featured: false,
  is_active: true,
});

export default {
  name: "AdminInstructorForm",
  components: { AppLoader },
  data() {
    return {
      loading: true,
      submitting: false,
      errorMessage: "",
      form: emptyForm(),
      photoFile: null,
      resumeFile: null,
      photoPreview: "",
      resumeName: "",
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
    onPhoto(event) {
      const file = event.target.files[0];
      if (!file) return;
      this.photoFile = file;
      this.photoPreview = URL.createObjectURL(file);
    },
    onResume(event) {
      const file = event.target.files[0];
      if (!file) return;
      this.resumeFile = file;
      this.resumeName = file.name;
    },
    async loadForm() {
      this.loading = true;
      this.errorMessage = "";
      try {
        if (this.isEdit) {
          const { data: inst } = await api.get(`/instructors/${this.$route.params.id}/`);
          this.form = {
            display_name: inst.display_name || "",
            bio: inst.bio || "",
            specializations: Array.isArray(inst.specializations) ? inst.specializations.join("\n") : "",
            photo: null,
            resume: null,
            website: inst.website || "",
            instagram: inst.instagram || "",
            telegram: inst.telegram || "",
            years_experience: inst.years_experience || 0,
            students_count: inst.students_count || 0,
            rating: Number(inst.rating) || 0,
            is_featured: !!inst.is_featured,
            is_active: inst.is_active !== undefined ? inst.is_active : true,
          };
          this.photoFile = null;
          this.resumeFile = null;
          this.photoPreview = inst.photo || "";
          this.resumeName = inst.resume ? inst.resume.split("/").pop() : "";
        } else {
          this.form = emptyForm();
          this.photoFile = null;
          this.resumeFile = null;
          this.photoPreview = "";
          this.resumeName = "";
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
      fd.append("display_name", f.display_name);
      fd.append("bio", f.bio);
      fd.append(
        "specializations",
        JSON.stringify(f.specializations.split("\n").map((s) => s.trim()).filter(Boolean))
      );
      if (f.website) fd.append("website", f.website);
      if (f.instagram) fd.append("instagram", f.instagram);
      if (f.telegram) fd.append("telegram", f.telegram);
      fd.append("years_experience", f.years_experience);
      fd.append("students_count", f.students_count);
      fd.append("rating", f.rating);
      fd.append("is_featured", f.is_featured ? "true" : "false");
      fd.append("is_active", f.is_active ? "true" : "false");
      if (this.photoFile) fd.append("photo", this.photoFile);
      if (this.resumeFile) fd.append("resume", this.resumeFile);
      return fd;
    },
    async submit() {
      this.submitting = true;
      this.errorMessage = "";
      try {
        const fd = this.buildFormData();
        if (this.isEdit) {
          await api.patch(`/instructors/${this.$route.params.id}/`, fd);
          this.$store.dispatch("notify", { message: "استاد با موفقیت به‌روزرسانی شد." });
        } else {
          await api.post("/instructors/", fd);
          this.$store.dispatch("notify", { message: "استاد با موفقیت ایجاد شد." });
        }
        this.$router.push("/admin/instructors");
      } catch (e) {
        console.error("خطای ذخیره استاد:", e);
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
        this.errorMessage = `ذخیره استاد ناموفق بود. ${detail}`.trim();
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
.resume-name {
  font-size: 0.8rem;
  color: var(--color-text-muted);
  margin-bottom: 6px;
}
.req {
  color: var(--color-danger);
}
</style>