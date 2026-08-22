<template>
  <router-link :to="`/products/${product.id}/${product.slug}`" class="product-card card">
    <div class="product-card__image-wrap">
      <img
        v-if="product.main_image"
        :src="product.main_image"
        :alt="product.name"
        class="product-card__image"
      />
      <div v-else class="product-card__image product-card__image--placeholder">📦</div>
      <span v-if="product.discount_percent" class="badge badge-accent product-card__discount">
        {{ product.discount_percent }}%-
      </span>
      <span v-if="!product.in_stock" class="badge badge-muted product-card__oos">ناموجود</span>
    </div>
    <div class="product-card__body">
      <span class="text-muted product-card__category">{{ product.category_name }}</span>
      <h3 class="product-card__title">{{ product.name }}</h3>
      <span v-if="product.vendor_name" class="product-card__vendor">🏪 {{ product.vendor_name }}</span>
      <div class="product-card__price">
        <span class="price">{{ formatPrice(product.final_price) }} تومان</span>
        <span v-if="product.discount_price" class="price-old">{{ formatPrice(product.price) }}</span>
      </div>
    </div>
  </router-link>
</template>

<script>
export default {
  name: "ProductCard",
  props: {
    product: { type: Object, required: true },
  },
  methods: {
    formatPrice(value) {
      return Number(value).toLocaleString("fa-IR");
    },
  },
};
</script>

<style scoped>
.product-card {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.product-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-3px);
}
.product-card__image-wrap {
  position: relative;
  aspect-ratio: 1 / 1;
  background: var(--color-sand);
}
.product-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.product-card__image--placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.4rem;
}
.product-card__discount {
  position: absolute;
  top: 10px;
  right: 10px;
}
.product-card__oos {
  position: absolute;
  top: 10px;
  left: 10px;
}
.product-card__body {
  padding: 14px 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.product-card__category {
  font-size: 0.72rem;
}
.product-card__title {
  font-size: 0.95rem;
  font-weight: 700;
  line-height: 1.4;
  min-height: 2.6em;
}
.product-card__vendor {
  font-size: 0.72rem;
  color: var(--color-primary);
  font-weight: 600;
}
.product-card__price {
  margin-top: 4px;
  display: flex;
  align-items: baseline;
  gap: 8px;
}
</style>
