<template>
  <div class="gallery-page">
    <div class="container">
      <div class="page-header">
        <span class="eyebrow">گالری آثار هنری</span>
        <h1>گالری یاشیل آرت</h1>
        <p>آثار هنری خلق شده توسط هنرجویان و اساتید آموزشگاه</p>
      </div>

      <!-- Filters -->
      <div class="filters-bar">
        <div class="filter-group">
          <select v-model="filters.category" @change="loadArtworks">
            <option value="">همه دسته‌ها</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
        </div>
        <div class="filter-group">
          <select v-model="filters.medium" @change="loadArtworks">
            <option value="">همه تکنیک‌ها</option>
            <option value="painting">نقاشی</option>
            <option value="sculpture">مجسمه‌سازی</option>
            <option value="calligraphy">خوشنویسی</option>
            <option value="digital">دیجیتال آرت</option>
            <option value="photography">عکاسی</option>
            <option value="pottery">سفالگری</option>
            <option value="mixed">تکنیک ترکیبی</option>
          </select>
        </div>
        <div class="filter-group">
          <select v-model="filters.ordering" @change="loadArtworks">
            <option value="-created_at">جدیدترین</option>
            <option value="-likes_count">محبوب‌ترین</option>
            <option value="-views_count">پربازدیدترین</option>
          </select>
        </div>
        <label class="filter-checkbox">
          <input type="checkbox" v-model="filters.forSale" @change="loadArtworks" />
          فقط آثار قابل فروش
        </label>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="masonry-grid">
        <div v-for="n in 8" :key="n" class="gallery-skeleton"></div>
      </div>

      <!-- Gallery Grid -->
      <div v-else-if="artworks.length" class="masonry-grid">
        <div
          v-for="artwork in artworks"
          :key="artwork.id"
          class="gallery-item"
          @click="openArtwork(artwork)"
        >
          <img :src="artwork.image" :alt="artwork.title" loading="lazy" />
          <div class="gallery-item-overlay">
            <div class="overlay-top">
              <span class="overlay-medium">{{ artwork.medium_display }}</span>
              <span v-if="artwork.is_for_sale && !artwork.is_sold" class="overlay-sale">فروشی</span>
              <span v-if="artwork.is_sold" class="overlay-sold">فروخته شده</span>
            </div>
            <div class="overlay-bottom">
              <h3>{{ artwork.title }}</h3>
              <span class="overlay-artist">{{ artwork.artist_name }}</span>
              <div class="overlay-stats">
                <span>❤️ {{ artwork.likes_count }}</span>
                <span>👁 {{ artwork.views_count }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty -->
      <div v-else class="empty-state">
        <div class="icon">🖼️</div>
        <p>اثری یافت نشد</p>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination">
        <button :disabled="currentPage <= 1" @click="changePage(currentPage - 1)">قبلی</button>
        <span>{{ currentPage }} / {{ totalPages }}</span>
        <button :disabled="currentPage >= totalPages" @click="changePage(currentPage + 1)">بعدی</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "GalleryPage",
  data() {
    return {
      artworks: [],
      categories: [],
      loading: true,
      currentPage: 1,
      totalPages: 1,
      filters: {
        category: "",
        medium: "",
        ordering: "-created_at",
        forSale: false,
      },
    };
  },
  methods: {
    async loadCategories() {
      try {
        const { data } = await api.get("/gallery/categories/");
        this.categories = data;
      } catch (e) { console.error(e); }
    },
    async loadArtworks() {
      this.loading = true;
      try {
        const params = { page: this.currentPage, ordering: this.filters.ordering };
        if (this.filters.category) params.category = this.filters.category;
        if (this.filters.medium) params.medium = this.filters.medium;
        if (this.filters.forSale) params.is_for_sale = true;

        const { data } = await api.get("/gallery/artworks/", { params });
        this.artworks = data.results || data;
        this.totalPages = Math.ceil((data.count || this.artworks.length) / 12);
      } catch (e) { console.error(e); }
      finally { this.loading = false; }
    },
    openArtwork(artwork) {
      this.$router.push(`/gallery/${artwork.id}/${artwork.slug}`);
    },
    changePage(page) {
      this.currentPage = page;
      this.loadArtworks();
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
  },
  created() {
    this.loadCategories();
    this.loadArtworks();
  },
};
</script>

<style scoped>
.gallery-page { padding: 40px 0 60px; }
.page-header { text-align: center; margin-bottom: 30px; }
.page-header h1 { font-size: 2rem; margin-top: 10px; }
.page-header p { color: var(--color-text-muted); margin-top: 10px; }

.filters-bar {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  align-items: flex-end;
  margin-bottom: 30px;
  padding: 14px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
}

.filter-group select {
  padding: 8px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.88rem;
  background: var(--color-bg);
}

.filter-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.88rem;
  cursor: pointer;
}

.masonry-grid {
  columns: 3;
  column-gap: 16px;
}

.gallery-item {
  break-inside: avoid;
  margin-bottom: 16px;
  border-radius: var(--radius);
  overflow: hidden;
  position: relative;
  cursor: pointer;
}

.gallery-item img {
  width: 100%;
  display: block;
  transition: transform 0.5s ease;
}

.gallery-item:hover img {
  transform: scale(1.05);
}

.gallery-item-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(transparent 40%, rgba(0,0,0,0.85));
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 16px;
  opacity: 0;
  transition: opacity 0.3s ease;
  color: white;
}

.gallery-item:hover .gallery-item-overlay {
  opacity: 1;
}

.overlay-top {
  display: flex;
  gap: 8px;
  justify-content: flex-start;
}

.overlay-medium {
  background: rgba(255,255,255,0.2);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
}

.overlay-sale {
  background: #e3a857;
  color: #1f4b43;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
}

.overlay-sold {
  background: rgba(179,69,44,0.9);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
}

.overlay-bottom h3 { font-size: 1rem; margin-bottom: 4px; }
.overlay-artist { font-size: 0.82rem; color: rgba(255,255,255,0.8); }
.overlay-stats { display: flex; gap: 14px; font-size: 0.8rem; margin-top: 8px; }

.gallery-skeleton {
  break-inside: avoid;
  margin-bottom: 16px;
  height: 200px;
  border-radius: var(--radius);
  background: linear-gradient(110deg, var(--color-sand) 30%, var(--color-bg) 50%, var(--color-sand) 70%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.pagination { display: flex; justify-content: center; align-items: center; gap: 20px; margin-top: 40px; }
.pagination button { padding: 8px 20px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); background: var(--color-surface); font-family: inherit; }
.pagination button:disabled { opacity: 0.5; cursor: not-allowed; }

@keyframes shimmer { to { background-position: -200% 0; } }

@media (max-width: 800px) { .masonry-grid { columns: 2; } }
@media (max-width: 500px) { .masonry-grid { columns: 1; } }
</style>
