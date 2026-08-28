<template>
  <div class="container product-detail-page">
    <AppLoader v-if="loading" />

    <div v-else-if="product" class="product-detail fade-in">
      <div class="gallery">
        <div class="gallery__main">
          <img v-if="activeImage" :src="activeImage" :alt="product.name" />
          <div v-else class="gallery__placeholder">📦</div>
        </div>
        <div v-if="product.images.length > 1" class="gallery__thumbs">
          <button
            v-for="img in product.images"
            :key="img.id"
            class="gallery__thumb"
            :class="{ active: activeImage === img.image }"
            @click="activeImage = img.image"
          >
            <img :src="img.image" :alt="product.name" />
          </button>
        </div>
      </div>

      <div class="info">
        <span class="text-muted">{{ product.category && product.category.name }}</span>
        <h1>{{ product.name }}</h1>
        <router-link v-if="product.vendor_slug" :to="`/store/${product.vendor_slug}`" class="vendor-link">
          🏪 فروشنده: {{ product.vendor_name }}
        </router-link>

        <!-- Rating Summary -->
        <div v-if="product.reviews_count > 0" class="rating-summary">
          <div class="rating-stars">
            <span v-for="s in 5" :key="s" class="star" :class="{ filled: s <= Math.round(product.average_rating) }">★</span>
          </div>
          <span class="rating-text">{{ product.average_rating }} از ۵</span>
          <span class="rating-count">({{ product.reviews_count }} نظر)</span>
        </div>

        <div class="price-row">
          <span class="price">{{ formatPrice(currentPrice) }} تومان</span>
          <span v-if="product.discount_price" class="price-old">{{ formatPrice(product.price) }}</span>
          <span v-if="product.discount_percent" class="badge badge-accent">{{ product.discount_percent }}%-</span>
        </div>

        <p class="description">{{ product.description }}</p>

        <div v-if="variantGroups.length" class="variant-groups">
          <div v-for="group in variantGroups" :key="group.name" class="variant-group">
            <label>{{ group.name }}</label>
            <div class="variant-options">
              <button
                v-for="opt in group.options"
                :key="opt.id"
                class="variant-option"
                :class="{ active: selectedVariantId === opt.id, disabled: opt.stock === 0 }"
                :disabled="opt.stock === 0"
                @click="selectedVariantId = opt.id"
              >
                {{ opt.value }}
              </button>
            </div>
          </div>
        </div>

        <div class="qty-row">
          <label>تعداد</label>
          <div class="qty-control">
            <button @click="quantity = Math.max(1, quantity - 1)">−</button>
            <span>{{ quantity }}</span>
            <button @click="quantity = Math.min(maxStock, quantity + 1)">+</button>
          </div>
          <span class="text-muted stock-note">{{ maxStock }} عدد موجود</span>
        </div>

        <button class="btn btn-primary btn-block add-to-cart" :disabled="maxStock === 0" @click="addToCart">
          {{ maxStock === 0 ? "ناموجود" : "افزودن به سبد خرید" }}
        </button>
      </div>
    </div>

    <!-- Rating Distribution Bar -->
    <div v-if="product && product.reviews_count > 0" class="rating-distribution card">
      <h3>امتیازات و نظرات</h3>
      <div class="dist-row" v-for="s in [5,4,3,2,1]" :key="s">
        <span class="dist-label">{{ s }} ★</span>
        <div class="dist-bar"><div class="dist-fill" :style="{ width: product.rating_distribution[s].percent + '%' }"></div></div>
        <span class="dist-count">{{ product.rating_distribution[s].count }}</span>
      </div>
    </div>

    <!-- Reviews Section -->
    <div v-if="product" class="reviews-section">
      <h2 class="section-title">نظرات کاربران</h2>

      <!-- Review Form -->
      <div v-if="isAuthenticated" class="review-form card">
        <h4>نظر خودتان را بنویسید</h4>
        <div class="review-rating-input">
          <span class="rating-label">امتیاز:</span>
          <div class="stars-input">
            <button
              v-for="s in 5"
              :key="s"
              class="star-btn"
              :class="{ filled: s <= newReview.rating }"
              @click="newReview.rating = s"
            >★</button>
          </div>
        </div>
        <input v-model="newReview.title" type="text" class="review-title-input" placeholder="عنوان نظر (اختیاری)" />
        <textarea v-model="newReview.comment" class="review-textarea" rows="3" placeholder="نظر خود را بنویسید..."></textarea>
        <button class="btn btn-primary" :disabled="!newReview.rating || !newReview.comment" @click="submitReview">
          ثبت نظر
        </button>
      </div>
      <div v-else class="login-prompt card">
        <p>برای ثبت نظر باید <router-link to="/login">وارد شوید</router-link>.</p>
      </div>

      <!-- Reviews List -->
      <div v-if="reviewsLoading" class="text-muted" style="padding: 20px;">در حال بارگذاری...</div>
      <div v-else-if="reviews.length === 0" class="empty-reviews">
        <p>هنوز نظری ثبت نشده. اولین نفری باشید که نظر می‌دهید!</p>
      </div>
      <div v-else class="reviews-list">
        <div v-for="review in reviews" :key="review.id" class="review-item card">
          <div class="review-header">
            <div class="review-user">
              <div class="avatar">{{ review.user_display_name.charAt(0) }}</div>
              <div>
                <span class="review-name">{{ review.user_display_name }}</span>
                <span class="review-date">{{ formatDate(review.created_at) }}</span>
              </div>
            </div>
            <div class="review-stars">
              <span v-for="s in 5" :key="s" class="star small" :class="{ filled: s <= review.rating }">★</span>
            </div>
          </div>
          <h4 v-if="review.title" class="review-title">{{ review.title }}</h4>
          <p class="review-comment">{{ review.comment }}</p>
        </div>
      </div>
    </div>

    <!-- Similar Products -->
    <div v-if="similarProducts.length > 0" class="similar-section">
      <h2 class="section-title">محصولات مشابه</h2>
      <div class="similar-grid">
        <ProductCard v-for="p in similarProducts" :key="p.id" :product="p" />
      </div>
    </div>

    <div v-if="!loading && !product" class="empty-state">
      <div class="icon">😕</div>
      <p>محصول یافت نشد.</p>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";
import ProductCard from "@/components/ProductCard.vue";

export default {
  name: "ProductDetailView",
  components: { AppLoader, ProductCard },
  data() {
    return {
      product: null,
      loading: true,
      activeImage: null,
      selectedVariantId: null,
      quantity: 1,
      reviews: [],
      reviewsLoading: false,
      similarProducts: [],
      newReview: { rating: 0, title: "", comment: "" },
    };
  },
  computed: {
    isAuthenticated() {
      return this.$store.getters["auth/isAuthenticated"];
    },
    variantGroups() {
      if (!this.product) return [];
      const groups = {};
      this.product.variants.forEach((v) => {
        if (!groups[v.attribute_name]) groups[v.attribute_name] = [];
        groups[v.attribute_name].push(v);
      });
      return Object.entries(groups).map(([name, options]) => ({ name, options }));
    },
    selectedVariant() {
      if (!this.product) return null;
      return this.product.variants.find((v) => v.id === this.selectedVariantId) || null;
    },
    currentPrice() {
      if (!this.product) return 0;
      const base = Number(this.product.final_price);
      return this.selectedVariant ? base + Number(this.selectedVariant.price_modifier) : base;
    },
    maxStock() {
      if (!this.product) return 0;
      return this.selectedVariant ? this.selectedVariant.stock : this.product.stock;
    },
  },
  async created() {
    await this.fetchProduct();
  },
  watch: {
    "$route.params.slug"() {
      this.fetchProduct();
    },
  },
  methods: {
    formatPrice(value) {
      return Number(value).toLocaleString("fa-IR");
    },
    formatDate(dateStr) {
      const d = new Date(dateStr);
      return d.toLocaleDateString("fa-IR");
    },
    async fetchProduct() {
      this.loading = true;
      try {
        const { data } = await api.get(`/products/${this.$route.params.id}/`);
        this.product = data;
        const main = data.images.find((i) => i.is_main) || data.images[0];
        this.activeImage = main ? main.image : null;
        if (this.variantGroups.length) {
          const firstAvailable = this.variantGroups[0].options.find((o) => o.stock > 0);
          this.selectedVariantId = firstAvailable ? firstAvailable.id : this.variantGroups[0].options[0].id;
        }
        this.quantity = 1;
        this.fetchReviews();
        this.fetchSimilar();
      } catch (e) {
        this.product = null;
      } finally {
        this.loading = false;
      }
    },
    async fetchReviews() {
      this.reviewsLoading = true;
      try {
        const { data } = await api.get("/reviews/", { params: { product: this.product.id } });
        this.reviews = data.results || data;
      } catch (e) { this.reviews = []; }
      finally { this.reviewsLoading = false; }
    },
    async fetchSimilar() {
      try {
        const { data } = await api.get(`/products/${this.product.id}/similar/`);
        this.similarProducts = data.results || data;
      } catch (e) { this.similarProducts = []; }
    },
    async submitReview() {
      if (!this.newReview.rating || !this.newReview.comment) return;
      try {
        await api.post("/reviews/", {
          product: this.product.id,
          rating: this.newReview.rating,
          title: this.newReview.title,
          comment: this.newReview.comment,
        });
        this.newReview = { rating: 0, title: "", comment: "" };
        this.$store.dispatch("notify", { message: "نظر شما با موفقیت ثبت شد." });
        this.fetchReviews();
        // Refresh product for updated rating
        const { data } = await api.get(`/products/${this.$route.params.id}/`);
        this.product = data;
      } catch (e) {
        this.$store.dispatch("notify", { message: "ثبت نظر ناموفق بود.", type: "error" });
      }
    },
    addToCart() {
      if (this.variantGroups.length && !this.selectedVariant) {
        this.$store.dispatch("notify", { message: "لطفاً یک گزینه انتخاب کنید.", type: "error" });
        return;
      }
      this.$store.dispatch("cart/addItem", {
        product_id: this.product.id,
        variant_id: this.selectedVariant ? this.selectedVariant.id : null,
        quantity: this.quantity,
        name: this.product.name,
        image: this.activeImage,
        price: this.currentPrice,
        variant_label: this.selectedVariant
          ? `${this.selectedVariant.attribute_name}: ${this.selectedVariant.value}`
          : "",
      });
      this.$store.dispatch("notify", { message: "به سبد خرید اضافه شد." });
    },
  },
};
</script>

<style scoped>
.product-detail-page { padding: 36px 20px 60px; }
.product-detail { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; }
.gallery__main { aspect-ratio: 1/1; background: var(--color-sand); border-radius: var(--radius); overflow: hidden; }
.gallery__main img { width: 100%; height: 100%; object-fit: cover; }
.gallery__placeholder { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 4rem; }
.gallery__thumbs { display: flex; gap: 10px; margin-top: 12px; }
.gallery__thumb { width: 64px; height: 64px; border-radius: var(--radius-sm); overflow: hidden; border: 2px solid transparent; padding: 0; cursor: pointer; }
.gallery__thumb.active { border-color: var(--color-accent); }
.gallery__thumb img { width: 100%; height: 100%; object-fit: cover; }

.info h1 { font-size: 1.7rem; margin: 8px 0 14px; }
.vendor-link { display: inline-block; font-size: 0.83rem; font-weight: 700; color: var(--color-primary); background: var(--color-sand); padding: 5px 12px; border-radius: 20px; margin-bottom: 16px; }
.price-row { display: flex; align-items: center; gap: 12px; margin-bottom: 18px; }
.price-row .price { font-size: 1.4rem; color: var(--color-primary); }
.description { color: var(--color-text-muted); margin-bottom: 22px; }

/* Rating */
.rating-summary { display: flex; align-items: center; gap: 8px; margin-bottom: 16px; }
.rating-stars { display: flex; gap: 2px; }
.star { color: var(--color-border); font-size: 1.1rem; }
.star.filled { color: #f59e0b; }
.star.small { font-size: 0.9rem; }
.rating-text { font-weight: 700; font-size: 0.9rem; }
.rating-count { color: var(--color-text-muted); font-size: 0.82rem; }

/* Rating Distribution */
.rating-distribution { padding: 24px; margin: 40px 0; border-radius: var(--radius); }
.rating-distribution h3 { margin: 0 0 16px; font-size: 1.1rem; }
.dist-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.dist-label { width: 36px; font-size: 0.82rem; font-weight: 700; text-align: center; }
.dist-bar { flex: 1; height: 8px; background: var(--color-sand); border-radius: 4px; overflow: hidden; }
.dist-fill { height: 100%; background: #f59e0b; border-radius: 4px; transition: width 0.4s; }
.dist-count { width: 28px; text-align: center; font-size: 0.82rem; color: var(--color-text-muted); }

/* Variants */
.variant-groups { margin-bottom: 20px; }
.variant-group { margin-bottom: 14px; }
.variant-group label { display: block; font-size: 0.85rem; font-weight: 700; margin-bottom: 8px; }
.variant-options { display: flex; flex-wrap: wrap; gap: 8px; }
.variant-option { border: 1.5px solid var(--color-border); background: var(--color-surface); border-radius: var(--radius-sm); padding: 8px 16px; font-size: 0.87rem; font-weight: 600; cursor: pointer; }
.variant-option.active { border-color: var(--color-primary); background: var(--color-primary); color: #fff; }
.variant-option.disabled { opacity: 0.4; text-decoration: line-through; }

/* Quantity */
.qty-row { display: flex; align-items: center; gap: 14px; margin-bottom: 22px; }
.qty-row label { font-size: 0.85rem; font-weight: 700; }
.qty-control { display: flex; align-items: center; border: 1.5px solid var(--color-border); border-radius: var(--radius-sm); overflow: hidden; }
.qty-control button { width: 34px; height: 34px; background: var(--color-sand); border: none; font-size: 1rem; font-weight: 700; cursor: pointer; }
.qty-control span { width: 40px; text-align: center; font-weight: 700; }
.stock-note { font-size: 0.8rem; }

/* Reviews */
.reviews-section { margin-top: 48px; }
.section-title { font-size: 1.3rem; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 2px solid var(--color-border); }

.review-form { padding: 24px; margin-bottom: 24px; border-radius: var(--radius); }
.review-form h4 { margin: 0 0 16px; }
.review-rating-input { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.rating-label { font-weight: 700; font-size: 0.88rem; }
.stars-input { display: flex; gap: 4px; }
.star-btn { background: none; border: none; font-size: 1.5rem; color: var(--color-border); cursor: pointer; transition: color 0.15s; padding: 0; }
.star-btn.filled { color: #f59e0b; }
.review-title-input { width: 100%; padding: 10px 14px; border: 1.5px solid var(--color-border); border-radius: var(--radius-sm); font-family: inherit; font-size: 0.9rem; margin-bottom: 12px; }
.review-title-input:focus { outline: none; border-color: var(--color-primary); }
.review-textarea { width: 100%; padding: 10px 14px; border: 1.5px solid var(--color-border); border-radius: var(--radius-sm); font-family: inherit; font-size: 0.9rem; resize: vertical; margin-bottom: 12px; }
.review-textarea:focus { outline: none; border-color: var(--color-primary); }

.login-prompt { padding: 20px; text-align: center; border-radius: var(--radius); }
.login-prompt a { color: var(--color-primary); font-weight: 700; }

.reviews-list { display: flex; flex-direction: column; gap: 16px; }
.review-item { padding: 20px; border-radius: var(--radius); }
.review-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.review-user { display: flex; align-items: center; gap: 10px; }
.avatar { width: 36px; height: 36px; border-radius: 50%; background: var(--color-primary); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.9rem; }
.review-name { display: block; font-weight: 700; font-size: 0.88rem; }
.review-date { font-size: 0.78rem; color: var(--color-text-muted); }
.review-stars { display: flex; gap: 1px; }
.review-title { margin: 0 0 6px; font-size: 0.95rem; }
.review-comment { margin: 0; color: var(--color-text-muted); font-size: 0.9rem; line-height: 1.7; }
.empty-reviews { text-align: center; padding: 30px; color: var(--color-text-muted); }

/* Similar Products */
.similar-section { margin-top: 48px; }
.similar-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px; }

/* Empty */
.empty-state { text-align: center; padding: 80px 20px; }
.empty-state .icon { font-size: 3rem; margin-bottom: 12px; }

@media (max-width: 800px) {
  .product-detail { grid-template-columns: 1fr; gap: 26px; }
  .similar-grid { grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; }
}
</style>