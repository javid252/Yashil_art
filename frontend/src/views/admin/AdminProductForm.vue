<template>
  <div class="admin-product-form">
    <div class="page-head">
      <h1>{{ isEdit ? "ویرایش محصول" : "محصول جدید" }}</h1>
      <router-link to="/admin/products" class="btn btn-outline btn-sm">بازگشت به لیست</router-link>
    </div>

    <AppLoader v-if="loading" />

    <form v-else class="card form-card" @submit.prevent="submit">
      <div v-if="errorMessage" class="form-error-box">{{ errorMessage }}</div>

      <div class="two-col">
        <div class="field">
          <label>نام محصول</label>
          <input v-model="form.name" type="text" required />
        </div>
        <div class="field">
          <label>دسته‌بندی</label>
          <select v-model="form.category">
            <option :value="null">بدون دسته</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>
      </div>

      <div class="field">
        <label>توضیحات</label>
        <textarea v-model="form.description" rows="4"></textarea>
      </div>

      <div class="three-col">
        <div class="field">
          <label>قیمت (تومان)</label>
          <input v-model.number="form.price" type="number" min="0" required />
        </div>
        <div class="field">
          <label>قیمت با تخفیف (اختیاری)</label>
          <input v-model.number="form.discount_price" type="number" min="0" />
        </div>
        <div class="field">
          <label>موجودی انبار</label>
          <input v-model.number="form.stock" type="number" min="0" required />
        </div>
      </div>

      <div class="checkbox-row">
        <label><input v-model="form.is_active" type="checkbox" /> فعال / قابل نمایش</label>
        <label><input v-model="form.is_featured" type="checkbox" /> محصول ویژه</label>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary" :disabled="submitting">
          {{ submitting ? "در حال ذخیره..." : "ذخیره محصول" }}
        </button>
      </div>
    </form>

    <div v-if="!loading && productId" class="card image-card">
      <h3>تصاویر محصول</h3>
      <p class="text-muted image-hint">اولین تصویر به‌صورت خودکار تصویر اصلی محصول در نظر گرفته می‌شود.</p>

      <div class="image-grid">
        <div v-for="img in images" :key="img.id" class="image-item">
          <img :src="img.image" :alt="form.name" />
          <span v-if="img.is_main" class="badge badge-accent image-item__main-badge">تصویر اصلی</span>
          <div class="image-item__actions">
            <button v-if="!img.is_main" type="button" class="btn btn-outline btn-sm" @click="setMainImage(img)">
              تصویر اصلی کن
            </button>
            <button type="button" class="btn btn-danger btn-sm" @click="deleteImage(img)">حذف</button>
          </div>
        </div>
      </div>

      <div class="image-upload-row">
        <input ref="fileInput" type="file" accept="image/*" multiple @change="onFilesSelected" />
        <button type="button" class="btn btn-accent btn-sm" :disabled="uploadingImage || !pendingFiles.length" @click="uploadImages">
          {{ uploadingImage ? "در حال آپلود..." : "آپلود تصویر(های) انتخاب‌شده" }}
        </button>
      </div>
    </div>
    <div v-else-if="!loading && !isEdit" class="card image-card">
      <p class="text-muted">برای افزودن تصویر، اول محصول را ذخیره کنید؛ بعد از ذخیره، بخش آپلود تصویر همین‌جا نمایش داده می‌شود.</p>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

export default {
  name: "AdminProductForm",
  components: { AppLoader },
  data() {
    return {
      loading: true,
      submitting: false,
      errorMessage: "",
      categories: [],
      form: {
        name: "", category: null, description: "", price: 0,
        discount_price: null, stock: 0, is_active: true, is_featured: false,
      },
      productId: null,
      images: [],
      pendingFiles: [],
      uploadingImage: false,
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
    async loadForm() {
      this.loading = true;
      this.errorMessage = "";
      try {
        const { data } = await api.get("/categories/");
        this.categories = data.results || data;

        if (this.isEdit) {
          const { data: product } = await api.get(`/products/${this.$route.params.id}/`);
          this.productId = product.id;
          this.images = product.images;
          this.form = {
            name: product.name,
            category: product.category ? product.category.id : null,
            description: product.description,
            price: Number(product.price),
            discount_price: product.discount_price ? Number(product.discount_price) : null,
            stock: product.stock,
            is_active: product.is_active !== undefined ? product.is_active : true,
            is_featured: product.is_featured,
          };
        } else {
          this.productId = null;
          this.images = [];
          this.form = {
            name: "", category: null, description: "", price: 0,
            discount_price: null, stock: 0, is_active: true, is_featured: false,
          };
        }
      } catch (e) {
        this.errorMessage = this.isEdit
          ? "بارگذاری اطلاعات محصول ناموفق بود. ممکن است محصول حذف شده باشد یا اتصال به سرور برقرار نشود."
          : "بارگذاری دسته‌بندی‌ها ناموفق بود. اتصال به سرور را بررسی کنید.";
      } finally {
        this.loading = false;
      }
    },
    async submit() {
      this.submitting = true;
      this.errorMessage = "";
      try {
        if (this.isEdit) {
          await api.patch(`/products/${this.$route.params.id}/`, this.form);
          this.$store.dispatch("notify", { message: "محصول با موفقیت به‌روزرسانی شد." });
        } else {
          const { data } = await api.post("/products/", this.form);
          this.productId = data.id;
          this.$store.dispatch("notify", { message: "محصول ثبت شد؛ حالا می‌توانید تصویر اضافه کنید." });
          this.$router.replace(`/admin/products/${data.id}/edit`);
          return;
        }
        this.$router.push("/admin/products");
      } catch (e) {
        this.errorMessage = "ذخیره محصول ناموفق بود. مقادیر را بررسی کنید.";
      } finally {
        this.submitting = false;
      }
    },
    onFilesSelected(event) {
      this.pendingFiles = Array.from(event.target.files || []);
    },
    async uploadImages() {
      if (!this.pendingFiles.length) return;
      this.uploadingImage = true;
      try {
        for (const file of this.pendingFiles) {
          const formData = new FormData();
          formData.append("product", this.productId);
          formData.append("image", file);
          formData.append("is_main", this.images.length === 0 ? "true" : "false");
          const { data } = await api.post("/product-images/", formData);
          this.images.push(data);
        }
        this.pendingFiles = [];
        this.$refs.fileInput.value = "";
        this.$store.dispatch("notify", { message: "تصاویر با موفقیت آپلود شدند." });
      } catch (e) {
        this.$store.dispatch("notify", { message: "آپلود تصویر ناموفق بود.", type: "error" });
      } finally {
        this.uploadingImage = false;
      }
    },
    async setMainImage(img) {
      try {
        const previousMain = this.images.find((i) => i.is_main);
        if (previousMain) {
          await api.patch(`/product-images/${previousMain.id}/`, { is_main: false });
          previousMain.is_main = false;
        }
        await api.patch(`/product-images/${img.id}/`, { is_main: true });
        img.is_main = true;
      } catch (e) {
        this.$store.dispatch("notify", { message: "تغییر تصویر اصلی ناموفق بود.", type: "error" });
      }
    },
    async deleteImage(img) {
      if (!confirm("این تصویر حذف شود؟")) return;
      try {
        await api.delete(`/product-images/${img.id}/`);
        this.images = this.images.filter((i) => i.id !== img.id);
      } catch (e) {
        this.$store.dispatch("notify", { message: "حذف تصویر ناموفق بود.", type: "error" });
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
  max-width: 720px;
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
  margin-bottom: 22px;
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
.image-card {
  max-width: 720px;
  padding: 26px;
  margin-top: 20px;
}
.image-card h3 {
  font-size: 1rem;
  margin-bottom: 6px;
}
.image-hint {
  font-size: 0.8rem;
  margin-bottom: 16px;
}
.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}
.image-item {
  position: relative;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  overflow: hidden;
}
.image-item img {
  width: 100%;
  height: 100px;
  object-fit: cover;
}
.image-item__main-badge {
  position: absolute;
  top: 6px;
  right: 6px;
}
.image-item__actions {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 6px;
}
.image-upload-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
</style>