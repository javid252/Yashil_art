<template>
  <section v-if="slides.length" class="hero-slider">
    <div class="slider-container">
      <div
        v-for="(slide, index) in slides"
        :key="slide.id"
        class="slide"
        :class="{
          'slide-active': index === currentIndex,
          'slide-exit': index === exitIndex,
        }"
      >
        <div class="slide-bg">
          <img :src="slide.image" :alt="slide.title" />
          <div class="overlay"></div>
        </div>

        <div class="slide-content">
          <div class="container hero-container">
            <div class="hero-content">
              <span v-if="slide.label" class="eyebrow">{{ slide.label }}</span>
              <h1>{{ slide.title }}</h1>
              <p v-if="slide.description">{{ slide.description }}</p>
              <div class="hero-actions">
                <template v-if="slide.primary_button_text">
                  <a v-if="isExternalLink(slide.primary_button_link)" :href="slide.primary_button_link" class="btn btn-accent" target="_blank" rel="noopener">
                    {{ slide.primary_button_text }}
                  </a>
                  <router-link v-else :to="slide.primary_button_link || '/'" class="btn btn-accent">
                    {{ slide.primary_button_text }}
                  </router-link>
                </template>
                <template v-if="slide.secondary_button_text">
                  <a v-if="isExternalLink(slide.secondary_button_link)" :href="slide.secondary_button_link" class="btn btn-outline" target="_blank" rel="noopener">
                    {{ slide.secondary_button_text }}
                  </a>
                  <router-link v-else :to="slide.secondary_button_link || '/'" class="btn btn-outline">
                    {{ slide.secondary_button_text }}
                  </router-link>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- فقط نقاط ناوبری -->
    <div v-if="slides.length > 1" class="slider-dots">
      <button
        v-for="(item, index) in slides"
        :key="item.id"
        :class="{ active: index === currentIndex }"
        @click="goTo(index)"
      ></button>
    </div>
  </section>
</template>

<script>
import api from "@/services/api";

export default {
  name: "HeroSlider",

  data() {
    return {
      currentIndex: 0,
      exitIndex: null,
      timer: null,
      slides: [],
    };
  },

  async created() {
    try {
      const { data } = await api.get("/content/hero-slides/");
      this.slides = data.results || data;
    } catch (e) {
      this.slides = [];
    }
  },

  mounted() {
    this.$watch(
      "slides",
      (slides) => {
        if (slides.length > 1) this.startSlider();
      },
      { immediate: true }
    );
  },

  beforeDestroy() {
    clearInterval(this.timer);
  },

  methods: {
    isExternalLink(link) {
      return !!link && /^https?:\/\//.test(link);
    },
    next() {
      this.exitIndex = this.currentIndex;
      this.currentIndex = (this.currentIndex + 1) % this.slides.length;
    },

    goTo(index) {
      if (index === this.currentIndex) return;
      this.exitIndex = this.currentIndex;
      this.currentIndex = index;
    },

    startSlider() {
      clearInterval(this.timer);
      this.timer = setInterval(() => {
        this.next();
      }, 5000);
    },
  },
};
</script>

<style scoped>
.hero-slider {
  position: relative;
  width: 100%;
  overflow: hidden;
  background: #1a1a2e;
  height: 420px;
}

.slider-container {
  position: relative;
  width: 100%;
  height: 100%;
}

/* ========== هر اسلاید ========== */
.slide {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.8s ease, visibility 0.8s ease;
}

.slide-active {
  opacity: 1;
  visibility: visible;
  z-index: 2;
}

.slide-exit {
  opacity: 0;
  visibility: hidden;
  z-index: 1;
}

/* ========== تصویر — کراس‌فید ساده ========== */
.slide-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.slide-bg img {
  width: 100%;
  height: 420px;
  object-fit: cover;
  transition: opacity 0.8s ease;
}

.slide-active .slide-bg img {
  opacity: 1;
}

.slide-exit .slide-bg img {
  opacity: 0;
}

.overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.7) 0%, rgba(0, 0, 0, 0.25) 100%);
  z-index: 1;
}

/* ========== محتوای نوشته ========== */
.slide-content {
  position: absolute;
  inset: 0;
  z-index: 2;
  display: flex;
  align-items: center;
}

.hero-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.hero-content {
  max-width: 600px;
  color: white;
}

.hero-content > * {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s cubic-bezier(0.65, 0, 0.35, 1);
}

.slide-active .hero-content .eyebrow {
  transition-delay: 0.2s;
  opacity: 1;
  transform: translateY(0);
}

.slide-active .hero-content h1 {
  transition-delay: 0.4s;
  opacity: 1;
  transform: translateY(0);
}

.slide-active .hero-content p {
  transition-delay: 0.6s;
  opacity: 1;
  transform: translateY(0);
}

.slide-active .hero-content .hero-actions {
  transition-delay: 0.8s;
  opacity: 1;
  transform: translateY(0);
}

.slide-exit .hero-content > * {
  transform: translateY(-20px);
  opacity: 0;
}

/* ========== استایل‌های محتوا ========== */
.eyebrow {
  display: inline-block;
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: #fbbf24;
  background: rgba(251, 191, 36, 0.15);
  padding: 6px 16px;
  border-radius: 30px;
  margin-bottom: 14px;
}

.hero-content h1 {
  font-size: 2.8rem;
  font-weight: 800;
  line-height: 1.25;
  margin: 14px 0;
  color: white;
  text-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
}

.hero-content p {
  font-size: 1.15rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.85);
  margin-bottom: 28px;
  line-height: 1.7;
  max-width: 500px;
}

.hero-actions {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.btn {
  padding: 13px 34px;
  border-radius: 50px;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s ease;
}

.btn-accent {
  background: #fbbf24;
  color: #1a1a2e;
}

.btn-accent:hover {
  background: #fcd34d;
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(251, 191, 36, 0.3);
}

.btn-outline {
  background: transparent;
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.btn-outline:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: white;
  transform: translateY(-2px);
}

/* ========== نقاط ناوبری ========== */
.slider-dots {
  position: absolute;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  display: flex;
  gap: 12px;
}

.slider-dots button {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.5);
  background: transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
}

.slider-dots button.active {
  background: #fbbf24;
  border-color: #fbbf24;
  transform: scale(1.2);
}

.slider-dots button:hover {
  border-color: #fbbf24;
  transform: scale(1.2);
}

/* ========== ریسپانسیو ========== */
@media (max-width: 768px) {
  .hero-slider {
    height: 320px;
  }

  .slide-bg img {
    height: 320px;
  }

  .hero-content {
    max-width: 100%;
    text-align: center;
  }

  .hero-content h1 {
    font-size: 1.8rem;
  }

  .hero-content p {
    font-size: 0.95rem;
    max-width: 100%;
  }

  .hero-actions {
    justify-content: center;
  }

  .slider-dots {
    bottom: 16px;
    gap: 10px;
  }

  .slider-dots button {
    width: 12px;
    height: 12px;
  }
}
</style>