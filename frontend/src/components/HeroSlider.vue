<template>
  <section v-if="slides.length" class="hero-slider">
    <div class="slider-container">
      <!-- اسلایدها با کراس فید -->
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

    <!-- Controls -->
    <template v-if="slides.length > 1">
      <button class="slider-prev" @click="previous">‹</button>
      <button class="slider-next" @click="next">›</button>

      <div class="slider-dots">
        <button
          v-for="(item, index) in slides"
          :key="item.id"
          :class="{ active: index === currentIndex }"
          @click="goTo(index)"
        ></button>
      </div>
    </template>
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
      direction: "next",
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
      this.direction = "next";
      this.exitIndex = this.currentIndex;
      this.currentIndex = (this.currentIndex + 1) % this.slides.length;
    },

    previous() {
      this.direction = "prev";
      this.exitIndex = this.currentIndex;
      this.currentIndex =
        (this.currentIndex - 1 + this.slides.length) % this.slides.length;
    },

    goTo(index) {
      if (index === this.currentIndex) return;
      this.direction = index > this.currentIndex ? "next" : "prev";
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
  height: 330px;
}

.slider-container {
  position: relative;
  width: 100%;
  height: 100%;
}

/* ========== هر اسلاید کاملاً همپوشان ========== */
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

/* ========== تصویر ========== */
.slide-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.slide-bg img {
  width: 100%;
  height: 330px;
  object-fit: cover;
  transform: translateX(100%);
  transition: transform 0.8s cubic-bezier(0.65, 0, 0.35, 1);
}

.slide-active .slide-bg img {
  transform: translateX(0);
}

.slide-exit .slide-bg img {
  transform: translateX(var(--exit-direction, -100%));
}

.overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.7) 0%, rgba(0, 0, 0, 0.3) 100%);
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
  max-width: 560px;
  color: white;
}

.hero-content > * {
  opacity: 0;
  transform: translateX(40px);
  transition: all 0.6s cubic-bezier(0.65, 0, 0.35, 1);
}

.slide-active .hero-content .eyebrow {
  transition-delay: 0.3s;
  opacity: 1;
  transform: translateX(0);
}

.slide-active .hero-content h1 {
  transition-delay: 0.6s;
  opacity: 1;
  transform: translateX(0);
}

.slide-active .hero-content p {
  transition-delay: 0.9s;
  opacity: 1;
  transform: translateX(0);
}

.slide-active .hero-content .hero-actions {
  transition-delay: 1.2s;
  opacity: 1;
  transform: translateX(0);
}

.slide-exit .hero-content > * {
  transform: translateX(var(--exit-direction, -40px));
  opacity: 0;
}

/* ========== بقیه استایل‌ها ========== */
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
  margin-bottom: 12px;
}

.hero-content h1 {
  font-size: 2.8rem;
  font-weight: 700;
  line-height: 1.2;
  margin: 15px 0;
  color: white;
  text-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
}

.hero-content p {
  font-size: 1.15rem;
  color: rgba(255, 255, 255, 0.85);
  margin-bottom: 30px;
  line-height: 1.6;
  max-width: 480px;
}

.hero-actions {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 32px;
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

/* ========== کنترل‌ها ========== */
.slider-prev,
.slider-next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  font-size: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.slider-prev {
  right: 25px;
}

.slider-next {
  left: 25px;
}

.slider-prev:hover,
.slider-next:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-50%) scale(1.1);
}

.slider-dots {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  display: flex;
  gap: 10px;
}

.slider-dots button {
  width: 12px;
  height: 12px;
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
  transform: scale(1.3);
}

/* ========== ریسپانسیو ========== */
@media (max-width: 768px) {
  .hero-slider {
    height: 250px;
  }

  .slide-bg img {
    height: 250px;
  }

  .hero-content h1 {
    font-size: 1.8rem;
  }

  .hero-content p {
    font-size: 0.95rem;
  }

  .hero-content {
    max-width: 100%;
    text-align: center;
  }

  .hero-content p {
    max-width: 100%;
  }

  .hero-actions {
    justify-content: center;
  }

  .slider-prev,
  .slider-next {
    width: 35px;
    height: 35px;
    font-size: 1.3rem;
  }

  .slider-prev {
    right: 10px;
  }

  .slider-next {
    left: 10px;
  }
}
</style>