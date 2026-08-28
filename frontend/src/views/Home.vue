<template>
  <div class="home">
    <HeroSlider />
    <CategoryGrid :categories="categories" />

    <!-- بنر تخفیف -->
    <section class="container discount-banner">
      <div class="discount-banner__inner">
        <div class="discount-banner__text">
          <span class="discount-banner__emoji">🏷️</span>
          <div>
            <h3>فروش ویژه پایان فصل</h3>
            <p>تا ۳۰٪ تخفیف روی محصولات منتخب — فرصت محدود!</p>
          </div>
        </div>
        <router-link to="/products?has_discount=true" class="btn btn-accent">
          مشاهده محصولات تخفیف‌دار ←
        </router-link>
      </div>
    </section>

    <!-- محصولات ویژه -->
    <section class="container featured-section">
      <div class="section-heading">
        <div>
          <span class="eyebrow">پیشنهاد یاشیل آرت</span>
          <h2>محصولات ویژه</h2>
        </div>
        <router-link to="/products" class="see-all">مشاهده همه ←</router-link>
      </div>

      <!-- Skeleton Loading -->
      <div v-if="loading" class="product-grid">
        <div v-for="n in 8" :key="n" class="skeleton-card">
          <div class="skeleton-image"></div>
          <div class="skeleton-body">
            <div class="skeleton-line short"></div>
            <div class="skeleton-line medium"></div>
            <div class="skeleton-line long"></div>
          </div>
        </div>
      </div>

      <div v-else class="product-grid">
        <ProductCard v-for="p in featured" :key="p.id" :product="p" />
      </div>
    </section>

    <!-- چرا یاشیل آرت -->
    <section class="why-us-section">
      <div class="container">
        <div class="section-heading-center">
          <span class="eyebrow">چرا یاشیل آرت؟</span>
          <h2>مزایای خرید از ما</h2>
        </div>
        <div class="why-us-grid">
          <div class="why-us-card">
            <div class="why-us-icon">🚚</div>
            <h4>ارسال رایگان</h4>
            <p>ارسال رایگان برای سفارش‌های بالای ۵۰۰ هزار تومان</p>
          </div>
          <div class="why-us-card">
            <div class="why-us-icon">✅</div>
            <h4>ضمانت اصالت</h4>
            <p>تمام محصولات با ضمانت اصالت و کیفیت عرضه می‌شوند</p>
          </div>
          <div class="why-us-card">
            <div class="why-us-icon">🔄</div>
            <h4>بازگشت آسان</h4>
            <p>امکان بازگشت کالا تا ۷ روز پس از تحویل</p>
          </div>
          <div class="why-us-card">
            <div class="why-us-icon">🎧</div>
            <h4>پشتیبانی ۲۴ ساعته</h4>
            <p>تیم پشتیبانی ما در تمام ساعات شبانه‌روز آماده کمک است</p>
          </div>
        </div>
      </div>
    </section>

    <!-- نظرات مشتریان -->
    <section class="testimonials-section">
      <div class="container">
        <div class="section-heading-center">
          <span class="eyebrow">نظرات مشتریان</span>
          <h2>مشتریان ما چه می‌گویند؟</h2>
        </div>
        <div class="testimonials-grid">
          <div v-for="review in testimonials" :key="review.id" class="testimonial-card card">
            <div class="testimonial-stars">
              <span v-for="s in 5" :key="s" class="star" :class="{ filled: s <= review.rating }">★</span>
            </div>
            <p class="testimonial-text">"{{ review.comment }}"</p>
            <div class="testimonial-author">
              <div class="testimonial-avatar">{{ review.user_display_name.charAt(0) }}</div>
              <div>
                <span class="testimonial-name">{{ review.user_display_name }}</span>
                <span class="testimonial-product">خریدار محصول «{{ review.product_name }}»</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- بنر تماس -->
    <section class="container contact-banner">
      <div class="contact-banner__inner">
        <div class="contact-banner__text">
          <span class="contact-banner__emoji">💬</span>
          <div>
            <h3>سوالی دارید؟</h3>
            <p>با ما در تماس باشید — پشتیبانی ۲۴ ساعته</p>
          </div>
        </div>
        <a href="tel:02191000000" class="btn btn-primary">
          ☎ ۰۲۱-۹۱۰۰۰۰۰۰
        </a>
      </div>
    </section>
  </div>
</template>

<script>
import api from "@/services/api";
import ProductCard from "@/components/ProductCard.vue";
import HeroSlider from "@/components/HeroSlider.vue";
import CategoryGrid from "@/components/CategoryGrid.vue";

export default {
  name: "HomeView",
  components: {
    ProductCard,
    HeroSlider,
    CategoryGrid,
  },
  data() {
    return {
      featured: [],
      loading: true,
      testimonials: [],
    };
  },
  computed: {
    categories() {
      return this.$store.state.products.categories;
    },
  },
  async created() {
    this.$store.dispatch("products/fetchCategories");

    // بارگذاری محصولات ویژه
    try {
      const { data } = await api.get("/products/", { params: { is_featured: true } });
      this.featured = data.results || data;
    } catch (e) {
      this.$store.dispatch("notify", { message: "بارگذاری محصولات ویژه ناموفق بود.", type: "error" });
    } finally {
      this.loading = false;
    }

    // بارگذاری نظرات مشتریان
    try {
      const { data } = await api.get("/reviews/", { params: { page_size: 3 } });
      const reviews = (data.results || data).slice(0, 3);
      // دریافت نام محصول برای هر نظر
      for (const r of reviews) {
        try {
          const { data: prod } = await api.get(`/products/${r.product}/`);
          r.product_name = prod.name;
        } catch (e) {
          r.product_name = "محصول";
        }
      }
      this.testimonials = reviews;
    } catch (e) {
      this.testimonials = [];
    }
  },
};
</script>

<style scoped>
/* ========== بنر تخفیف ========== */
.discount-banner {
  padding: 0 20px;
  margin-top: 40px;
}

.discount-banner__inner {
  background: linear-gradient(135deg, #e3a857 0%, #c98a3b 100%);
  border-radius: var(--radius-lg);
  padding: 28px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  box-shadow: 0 8px 30px rgba(227, 168, 87, 0.25);
}

.discount-banner__text {
  display: flex;
  align-items: center;
  gap: 16px;
}

.discount-banner__emoji {
  font-size: 2.2rem;
}

.discount-banner__text h3 {
  font-size: 1.2rem;
  color: #1a1a2e;
  margin-bottom: 4px;
}

.discount-banner__text p {
  font-size: 0.9rem;
  color: rgba(26, 26, 46, 0.8);
  margin: 0;
}

.discount-banner .btn-accent {
  background: #1a1a2e;
  color: #fbbf24;
  white-space: nowrap;
  font-size: 0.9rem;
}

.discount-banner .btn-accent:hover {
  background: #2a2a4e;
  transform: translateY(-2px);
}

/* ========== محصولات ویژه ========== */
.featured-section {
  padding: 50px 20px 60px;
}

.section-heading {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 28px;
}

.section-heading h2 {
  font-size: 1.5rem;
  margin-top: 6px;
}

.see-all {
  font-weight: 700;
  color: var(--color-primary);
  font-size: 0.88rem;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

/* ========== Skeleton Loading ========== */
.skeleton-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  overflow: hidden;
}

.skeleton-image {
  aspect-ratio: 1/1;
  background: linear-gradient(110deg, var(--color-sand) 30%, var(--color-bg) 50%, var(--color-sand) 70%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton-body {
  padding: 14px;
}

.skeleton-line {
  height: 12px;
  border-radius: 6px;
  margin-bottom: 10px;
  background: linear-gradient(110deg, var(--color-sand) 30%, var(--color-bg) 50%, var(--color-sand) 70%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton-line.short { width: 40%; }
.skeleton-line.medium { width: 70%; }
.skeleton-line.long { width: 55%; }

@keyframes shimmer { to { background-position: -200% 0; } }

/* ========== چرا یاشیل آرت ========== */
.why-us-section {
  padding: 60px 0;
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

.section-heading-center {
  text-align: center;
  margin-bottom: 36px;
}

.section-heading-center h2 {
  font-size: 1.5rem;
  margin-top: 8px;
}

.why-us-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.why-us-card {
  text-align: center;
  padding: 30px 20px;
  border-radius: var(--radius);
  transition: all 0.25s ease;
}

.why-us-card:hover {
  background: var(--color-bg);
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(31, 75, 67, 0.08);
}

.why-us-icon {
  font-size: 2.5rem;
  margin-bottom: 14px;
}

.why-us-card h4 {
  font-size: 1rem;
  margin-bottom: 8px;
  color: var(--color-primary);
}

.why-us-card p {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  line-height: 1.6;
  margin: 0;
}

/* ========== نظرات مشتریان ========== */
.testimonials-section {
  padding: 60px 0;
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.testimonial-card {
  padding: 28px;
  border-radius: var(--radius);
}

.testimonial-stars {
  display: flex;
  gap: 2px;
  margin-bottom: 14px;
}

.star {
  color: var(--color-border);
  font-size: 1.1rem;
}

.star.filled {
  color: #f59e0b;
}

.testimonial-text {
  font-size: 0.92rem;
  color: var(--color-text);
  line-height: 1.7;
  margin: 0 0 18px;
  font-style: italic;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 10px;
}

.testimonial-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.testimonial-name {
  display: block;
  font-weight: 700;
  font-size: 0.88rem;
}

.testimonial-product {
  display: block;
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

/* ========== بنر تماس ========== */
.contact-banner {
  padding: 0 20px;
  margin-bottom: 60px;
}

.contact-banner__inner {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  border-radius: var(--radius-lg);
  padding: 28px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  color: white;
  box-shadow: 0 8px 30px rgba(31, 75, 67, 0.25);
}

.contact-banner__text {
  display: flex;
  align-items: center;
  gap: 16px;
}

.contact-banner__emoji {
  font-size: 2.2rem;
}

.contact-banner__text h3 {
  font-size: 1.2rem;
  color: white;
  margin-bottom: 4px;
}

.contact-banner__text p {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

.contact-banner .btn-primary {
  background: white;
  color: var(--color-primary);
  white-space: nowrap;
  font-size: 0.9rem;
  font-weight: 700;
}

.contact-banner .btn-primary:hover {
  background: var(--color-sand);
  transform: translateY(-2px);
}

/* ========== ریسپانسیو ========== */
@media (max-width: 860px) {
  .why-us-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .testimonials-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .discount-banner__inner,
  .contact-banner__inner {
    flex-direction: column;
    text-align: center;
    padding: 24px 20px;
  }

  .discount-banner__text,
  .contact-banner__text {
    flex-direction: column;
    gap: 10px;
  }

  .why-us-grid {
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }

  .why-us-card {
    padding: 20px 12px;
  }

  .why-us-icon {
    font-size: 2rem;
  }
}
</style>