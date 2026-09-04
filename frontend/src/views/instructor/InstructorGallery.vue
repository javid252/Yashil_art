<template>
  <div class="instructor-gallery">
    <h2>🖼️ گالری آثار هنری</h2>
    <div v-if="artworks.length" class="gallery-grid">
      <div v-for="a in artworks" :key="a.id" class="art-card">
        <div class="art-image" :style="{ backgroundImage: 'url(' + a.image + ')' }"></div>
        <div class="art-info">
          <h4>{{ a.title }}</h4>
          <p class="art-student">{{ a.student_name }}</p>
          <span class="art-cat">{{ a.category_display || a.category }}</span>
        </div>
      </div>
    </div>
    <p v-else class="empty">هنوز اثری ثبت نشده.</p>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "InstructorGallery",
  data() {
    return { artworks: [] };
  },
  async mounted() {
    try {
      const { data } = await api.get("/gallery/artworks/");
      this.artworks = Array.isArray(data) ? data : [];
    } catch { /* silent */ }
  },
};
</script>

<style scoped>
.instructor-gallery h2 { margin-bottom: 16px; color: #1a2f1e; }
.gallery-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; }
.art-card { background: #fff; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.06); }
.art-image { height: 200px; background-size: cover; background-position: center; background-color: #f0f0f0; }
.art-info { padding: 12px; }
.art-info h4 { margin: 0 0 4px; font-size: 0.9rem; }
.art-student { font-size: 0.78rem; color: #888; margin: 2px 0; }
.art-cat { font-size: 0.72rem; color: #999; }
.empty { color: #999; text-align: center; padding: 40px; }
</style>
