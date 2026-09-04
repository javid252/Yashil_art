<template>
  <div class="admin-artwork-form">
    <div class="page-head">
      <h1>{{ isEdit ? "ویرایش اثر هنری" : "اثر هنری جدید" }}</h1>
      <router-link to="/admin/gallery-admin" class="btn btn-outline btn-sm">بازگشت به لیست</router-link>
    </div>

    <AppLoader v-if="loading" />

    <form v-else class="card form-card" @submit.prevent="submit">
      <div v-if="errorMessage" class="form-error-box">{{ errorMessage }}</div>

      <div class="two-col">
        <div class="field">
          <label>عنوان اثر <span class="req">*</span></label>
          <input v-model="form.title" type="text" required />
        </div>
        <div class="field">
          <label>تکنیک / مدیوم <span class="req">*</span></label>
          <select v-model="form.medium" required>
            <option value="painting">نقاشی</option>
            <option value="sculpture">مجسمه‌سازی</option>
            <option value="calligraphy">خوشنویسی</option>
            <option value="digital">دیجیتال آرت</option>
            <option value="photography">عکاسی</option>
            <option value="pottery">سفالگری</option>
            <option value="textile">نساجی و بافندگی</option>
            <option value="mixed">تکنیک ترکیبی</option>
            <option value="other">سایر</option>
          </select>
        </div>
      </div>

      <div class="two-col">
        <div class="field">
          <label>هنرمند</label>
          <select v-model="form.artist">
            <option :value="null">(بدون انتخاب - مدیر به‌عنوان سازنده ثبت می‌شود)</option>
            <option v-for="a in artists" :key="a.id" :value="a.id">{{ a.name }}</option>
          </select>
        </div>
        <div class="field">
          <label>استاد راهنما</label>
          <select v-model="form.instructor">
            <option :value="null">بدون استاد</option>
            <option v-for="i in instructors" :key="i.id" :value="i.id">{{ i.display_name }}</option>
          </select>
        </div>
      </div>

      <div class="two-col">
        <div class="field">
          <label>دسته‌بندی</label>
          <select v-model="form.category">
            <option :value="null">بدون دسته</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>
        <div class="field">
          <label>نمایشگاه (اختیاری)</label>
          <select v-model="form.exhibition">
            <option :value="null">بدون نمایشگاه</option>
            <option v-for="e in exhibitions" :key="e.id" :value="e.id">{{ e.title }}</option>
          </select>
        </div>
      </div>

      <div class="field">
        <label>توضیحات اثر</label>
        <textarea v-model="form.description" rows="4"></textarea>
      </div>

      <div class="three-col">
        <div class="field">
          <label>ابعاد</label>
          <input v-model="form.dimensions" type="text" placeholder="مثلاً 50x70 سانتی‌متر" />
        </div>
        <div class="field">
          <label>سال خلق</label>
          <input v-model.number="form.year_created" type="number" min="1300" max="1500" />
        </div>
        <div class="field">
          <label>قیمت فروش (تومان)</label>
          <input v-model.number="form.sale_price" type="number" min="0" :disabled="!form.is_for_sale" />
        </div>
      </div>

      <h3 class="section-title">تصویر اثر</h3>
      <div class="two-col">
        <div class="field">
          <label>تصویر اثر <span v-if="!isEdit" class="req">*</span></label>
          <img v-if="imagePreview" :src="imagePreview" class="image-preview" />
          <input type="file" accept="image/*" @change="onImage" />
        </div>
        <div class="field">
          <label>تصویر بندانگشتی (اختیاری)</label>
          <img v-if="thumbPreview" :src="thumbPreview" class="image-preview" />
          <input type="file" accept="image/*" @change="onThumb" />
        </div>
      </div>

      <div class="checkbox-row">
        <label><input v-model="form.is_published" type="checkbox" /> منتشر شده</label>
        <label><input v-model="form.is_featured" type="checkbox" /> اثر ویژه</label>
        <label><input v-model="form.is_for_sale" type="checkbox" /> قابل فروش</label>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary" :disabled="submitting">
          {{ submitting ? "در حال ذخیره..." : (isEdit ? "ذخیره تغییرات" : "ایجاد اثر") }}
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
  artist: null,
  instructor: null,
  category: null,
  exhibition: null,
  description: "",
  medium: "painting",
  dimensions: "",
  year_created: null,
  sale_price: null,
  is_published: true,
  is_featured: false,
  is_for_sale: false,
});

export default {
  name: "AdminArtworkForm",
  components: { AppLoader },
  data() {
    return {
      loading: true,
      submitting: false,
      errorMessage: "",
      categories: [],
      exhibitions: [],
      artists: [],
      instructors: [],
      form: emptyForm(),
      imageFile: null,
      thumbFile: null,
      imagePreview: "",
      thumbPreview: "",
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
    onImage(event) {
      const file = event.target.files[0];
      if (!file) return;
      this.imageFile = file;
      this.imagePreview = URL.createObjectURL(file);
    },
    onThumb(event) {
      const file = event.target.files[0];
      if (!file) return;
      this.thumbFile = file;
      this.thumbPreview = URL.createObjectURL(file);
    },
    async loadForm() {
      this.loading = true;
      this.errorMessage = "";
      try {
        const [catRes, exhRes, artistRes, instRes] = await Promise.all([
          api.get("/gallery/categories/"),
          api.get("/gallery/exhibitions/"),
          api.get("/gallery/artworks/artist_options/"),
          api.get("/instructors/"),
        ]);
        this.categories = catRes.data.results || catRes.data;
        this.exhibitions = exhRes.data.results || exhRes.data;
        this.artists = artistRes.data.results || artistRes.data || [];
        this.instructors = instRes.data.results || instRes.data;

        if (this.isEdit) {
          const { data: art } = await api.get(`/gallery/artworks/${this.$route.params.id}/`);
          this.form = {
            title: art.title || "",
            artist: art.artist || null,
            instructor: art.instructor || null,
            category: art.category || null,
            exhibition: art.exhibition || null,
            description: art.description || "",
            medium: art.medium || "painting",
            dimensions: art.dimensions || "",
            year_created: art.year_created || null,
            sale_price: art.sale_price != null ? Number(art.sale_price) : null,
            is_published: art.is_published !== undefined ? art.is_published : true,
            is_featured: !!art.is_featured,
            is_for_sale: !!art.is_for_sale,
          };
          this.imageFile = null;
          this.thumbFile = null;
          this.imagePreview = art.image || "";
          this.thumbPreview = art.thumbnail || "";
        } else {
          this.form = emptyForm();
          this.imageFile = null;
          this.thumbFile = null;
          this.imagePreview = "";
          this.thumbPreview = "";
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
      fd.append("medium", f.medium);
      if (f.artist) fd.append("artist", f.artist);
      if (f.instructor) fd.append("instructor", f.instructor);
      if (f.category) fd.append("category", f.category);
      if (f.exhibition) fd.append("exhibition", f.exhibition);
      if (f.description) fd.append("description", f.description);
      if (f.dimensions) fd.append("dimensions", f.dimensions);
      if (f.year_created) fd.append("year_created", f.year_created);
      if (f.is_for_sale && f.sale_price !== null && f.sale_price !== "") fd.append("sale_price", f.sale_price);
      fd.append("is_published", f.is_published ? "true" : "false");
      fd.append("is_featured", f.is_featured ? "true" : "false");
      fd.append("is_for_sale", f.is_for_sale ? "true" : "false");
      if (this.imageFile) fd.append("image", this.imageFile);
      if (this.thumbFile) fd.append("thumbnail", this.thumbFile);
      return fd;
    },
    async submit() {
      if (!this.isEdit && !this.imageFile) {
        this.errorMessage = "برای ایجاد اثر، تصویر اثر الزامی است.";
        return;
      }
      this.submitting = true;
      this.errorMessage = "";
      try {
        const fd = this.buildFormData();
        if (this.isEdit) {
          await api.patch(`/gallery/artworks/${this.$route.params.id}/`, fd);
          this.$store.dispatch("notify", { message: "اثر با موفقیت به‌روزرسانی شد." });
        } else {
          await api.post("/gallery/artworks/", fd);
          this.$store.dispatch("notify", { message: "اثر با موفقیت ایجاد شد." });
        }
        this.$router.push("/admin/gallery-admin");
      } catch (e) {
        console.error("خطای ذخیره اثر هنری:", e);
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
        this.errorMessage = `ذخیره اثر ناموفق بود. ${detail}`.trim();
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
  max-height: 180px;
  object-fit: cover;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
  margin-bottom: 8px;
}
.req {
  color: var(--color-danger);
}
</style>