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

    <div v-else class="empty-state">
      <div class="icon">😕</div>
      <p>محصول یافت نشد.</p>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

export default {
  name: "ProductDetailView",
  components: { AppLoader },
  data() {
    return {
      product: null,
      loading: true,
      activeImage: null,
      selectedVariantId: null,
      quantity: 1,
    };
  },
  computed: {
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
      } catch (e) {
        this.product = null;
      } finally {
        this.loading = false;
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
.product-detail-page {
  padding: 36px 20px 60px;
}
.product-detail {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
}
.gallery__main {
  aspect-ratio: 1/1;
  background: var(--color-sand);
  border-radius: var(--radius);
  overflow: hidden;
}
.gallery__main img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.gallery__placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
}
.gallery__thumbs {
  display: flex;
  gap: 10px;
  margin-top: 12px;
}
.gallery__thumb {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  border: 2px solid transparent;
  padding: 0;
}
.gallery__thumb.active {
  border-color: var(--color-accent);
}
.gallery__thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.info h1 {
  font-size: 1.7rem;
  margin: 8px 0 14px;
}
.vendor-link {
  display: inline-block;
  font-size: 0.83rem;
  font-weight: 700;
  color: var(--color-primary);
  background: var(--color-sand);
  padding: 5px 12px;
  border-radius: 20px;
  margin-bottom: 16px;
}
.price-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
}
.price-row .price {
  font-size: 1.4rem;
  color: var(--color-primary);
}
.description {
  color: var(--color-text-muted);
  margin-bottom: 22px;
}
.variant-groups {
  margin-bottom: 20px;
}
.variant-group {
  margin-bottom: 14px;
}
.variant-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 700;
  margin-bottom: 8px;
}
.variant-options {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.variant-option {
  border: 1.5px solid var(--color-border);
  background: var(--color-surface);
  border-radius: var(--radius-sm);
  padding: 8px 16px;
  font-size: 0.87rem;
  font-weight: 600;
}
.variant-option.active {
  border-color: var(--color-primary);
  background: var(--color-primary);
  color: #fff;
}
.variant-option.disabled {
  opacity: 0.4;
  text-decoration: line-through;
}
.qty-row {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 22px;
}
.qty-row label {
  font-size: 0.85rem;
  font-weight: 700;
}
.qty-control {
  display: flex;
  align-items: center;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  overflow: hidden;
}
.qty-control button {
  width: 34px;
  height: 34px;
  background: var(--color-sand);
  border: none;
  font-size: 1rem;
  font-weight: 700;
}
.qty-control span {
  width: 40px;
  text-align: center;
  font-weight: 700;
}
.stock-note {
  font-size: 0.8rem;
}

@media (max-width: 800px) {
  .product-detail {
    grid-template-columns: 1fr;
    gap: 26px;
  }
}
</style>
