<template>
  <div class="student-gallery">
    <h2>🖼️ آثار هنری من</h2>
    <div class="upload-section">
      <div class="upload-box" @click="$refs.fileInput.click()">
        <input ref="fileInput" type="file" accept="image/*" hidden @change="handleUpload" />
        <span class="upload-icon">📤</span>
        <span>بارگذاری اثر جدید</span>
      </div>
      <input v-model="newTitle" type="text" placeholder="عنوان اثر" class="input-title" />
      <select v-model="newCategory" class="select-cat">
        <option value="painting">نقاشی</option>
        <option value="sculpture">مجسمه‌سازی</option>
        <option value="photography">عکاسی</option>
        <option value="calligraphy">خوشنویسی</option>
        <option value="digital">دیجیتال آرت</option>
        <option value="other">سایر</option>
      </select>
      <button class="btn-upload" @click="submitArtwork" :disabled="!uploadFile">ارسال</button>
    </div>
    <div v-if="artworks.length" class="gallery-grid">
      <div v-for="a in artworks" :key="a.id" class="art-card">
        <div class="art-image" :style="{ backgroundImage: 'url(' + a.image + ')' }"></div>
        <div class="art-info">
          <h4>{{ a.title }}</h4>
          <span class="art-cat">{{ a.category_display || a.category }}</span>
        </div>
      </div>
    </div>
    <p v-else class="empty">هنوز اثری بارگذاری نکرده‌اید.</p>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "StudentGallery",
  data() {
    return { artworks: [], uploadFile: null, newTitle: "", newCategory: "painting" };
  },
  methods: {
    handleUpload(e) {
      this.uploadFile = e.target.files[0] || null;
    },
    async submitArtwork() {
      if (!this.uploadFile || !this.newTitle) return;
      const fd = new FormData();
      fd.append("image", this.uploadFile);
      fd.append("title", this.newTitle);
      fd.append("category", this.newCategory);
      try {
        await api.post("/gallery/artworks/", fd, { headers: { "Content-Type": "multipart/form-data" } });
        this.uploadFile = null;
        this.newTitle = "";
        const { data } = await api.get("/gallery/my-artworks/");
        this.artworks = Array.isArray(data) ? data : [];
      } catch { /* silent */ }
    },
  },
  async mounted() {
    try {
      const { data } = await api.get("/gallery/my-artworks/");
      this.artworks = Array.isArray(data) ? data : [];
    } catch { /* silent */ }
  },
};
</script>

<style scoped>
.student-gallery h2 { margin-bottom: 16px; color: #1a2f1e; }
.upload-section {
  display: flex; gap: 12px; align-items: center; flex-wrap: wrap;
  background: #fff; padding: 16px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.upload-box {
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  padding: 16px 20px; border: 2px dashed #ccc; border-radius: 10px; cursor: pointer; font-size: 0.82rem;
}
.upload-box:hover { border-color: #2d5a3f; }
.upload-icon { font-size: 1.5rem; }
.input-title { padding: 8px 14px; border: 1px solid #ddd; border-radius: 8px; font-family: inherit; font-size: 0.85rem; }
.select-cat { padding: 8px 14px; border: 1px solid #ddd; border-radius: 8px; font-family: inherit; font-size: 0.85rem; }
.btn-upload {
  padding: 8px 20px; background: #2d5a3f; color: #fff; border: none;
  border-radius: 8px; font-family: inherit; font-size: 0.85rem; cursor: pointer;
}
.btn-upload:disabled { opacity: 0.5; cursor: not-allowed; }
.gallery-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
.art-card { background: #fff; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.06); }
.art-image { height: 180px; background-size: cover; background-position: center; background-color: #f0f0f0; }
.art-info { padding: 12px; }
.art-info h4 { margin: 0 0 4px; font-size: 0.88rem; }
.art-cat { font-size: 0.75rem; color: #888; }
.empty { color: #999; text-align: center; padding: 40px; }
</style>
