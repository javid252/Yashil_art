<template>
  <section class="category-section">
    <div class="container">
      <div class="category-wrapper">
        <div class="section-title-badge">
          <span class="title-line"></span>
          <span class="title-text">دسته‌بندی‌ها</span>
          <span class="title-line"></span>
        </div>
        <div class="category-grid">
          <router-link
            v-for="cat in categories"
            :key="cat.id"
            :to="`/products?category=${cat.slug}`"
            class="category-item"
          >
            <div class="category-image">
              <img
                v-if="cat.image"
                :src="cat.image"
                :alt="cat.name"
              />
              <span v-else class="category-emoji">
                {{ cat.icon || "🛍️" }}
              </span>
            </div>
            <div class="category-name">{{ cat.name }}</div>
            <div v-if="cat.product_count > 0" class="category-count">
              {{ cat.product_count }} محصول
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "CategoryGrid",
  props: {
    categories: {
      type: Array,
      default: () => [],
    },
  },
};
</script>

<style scoped>
.category-section {
  padding: 40px 0 50px;
}

.category-wrapper {
  position: relative;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 40px 32px 36px;
  box-shadow: var(--shadow-sm);
}

.section-title-badge {
  position: absolute;
  top: -14px;
  right: 32px;
  display: flex;
  align-items: center;
  gap: 10px;
  z-index: 2;
}

.title-text {
  background: var(--color-primary);
  color: #fff;
  font-size: 0.95rem;
  font-weight: 700;
  padding: 6px 20px;
  border-radius: 6px;
  white-space: nowrap;
  line-height: 1;
}

.title-line {
  display: block;
  width: 40px;
  height: 2px;
  background: var(--color-primary);
  border-radius: 1px;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 28px;
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 16px 8px;
  border-radius: var(--radius);
  transition: all 0.25s ease;
  text-decoration: none;
}

.category-item:hover {
  transform: translateY(-6px);
  box-shadow: 0 10px 28px rgba(31, 75, 67, 0.12);
  background: var(--color-bg);
}

.category-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--color-sand);
  border: 3px solid var(--color-surface);
  box-shadow: 0 4px 14px rgba(31, 75, 67, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s ease;
}

.category-item:hover .category-image {
  border-color: var(--color-accent);
  box-shadow: 0 6px 20px rgba(227, 168, 87, 0.2);
}

.category-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.category-emoji {
  font-size: 2.2rem;
}

.category-name {
  font-weight: 700;
  font-size: 0.9rem;
  color: var(--color-text);
  text-align: center;
}

.category-count {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  font-weight: 500;
}

.category-item:hover .category-name {
  color: var(--color-primary);
}

@media (max-width: 600px) {
  .category-wrapper {
    padding: 36px 16px 24px;
    border-radius: var(--radius);
  }

  .section-title-badge {
    right: 16px;
    top: -12px;
  }

  .title-text {
    font-size: 0.85rem;
    padding: 5px 14px;
  }

  .title-line {
    width: 24px;
  }

  .category-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }

  .category-image {
    width: 80px;
    height: 80px;
  }

  .category-emoji {
    font-size: 1.8rem;
  }

  .category-name {
    font-size: 0.8rem;
  }

  .category-count {
    font-size: 0.7rem;
  }
}
</style>