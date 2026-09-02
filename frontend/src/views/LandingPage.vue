<template>
  <div class="landing">
    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- HERO — Immersive full-screen section                       -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section class="hero" ref="hero">
      <div class="hero__bg">
        <div class="hero__grain"></div>
        <div class="hero__orb hero__orb--1"></div>
        <div class="hero__orb hero__orb--2"></div>
        <div class="hero__orb hero__orb--3"></div>
        <div class="hero__lines">
          <span v-for="n in 8" :key="n"></span>
        </div>
      </div>

      <div class="hero__content">
        <div class="hero__tag">
          <span class="hero__tag-line"></span>
          <span class="hero__tag-text">آموزشگاه آزاد هنرهای تجسمی</span>
        </div>

        <h1 class="hero__title">
          <span class="hero__title-line hero__title-line--1">جایی که</span>
          <span class="hero__title-line hero__title-line--2">
            <span class="hero__title-accent">هنر</span>
          </span>
          <span class="hero__title-line hero__title-line--3">زندگی می‌شود</span>
        </h1>

        <p class="hero__subtitle">
          از نقاشی تا مجسمه‌سازی، از خوشنویسی تا گرافیک — مسیر یادگیری هنر
          را در کنار برترین اساتید ایران آغاز کنید.
        </p>

        <div class="hero__actions">
          <router-link to="/courses" class="hero__btn hero__btn--primary">
            <span>مشاهده دوره‌ها</span>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </router-link>
          <router-link to="/gallery" class="hero__btn hero__btn--ghost">
            <span>گالری آثار</span>
          </router-link>
        </div>

        <div class="hero__stats">
          <div class="hero__stat">
            <span class="hero__stat-num">۵۰۰+</span>
            <span class="hero__stat-label">هنرجو</span>
          </div>
          <div class="hero__stat-divider"></div>
          <div class="hero__stat">
            <span class="hero__stat-num">۵۰+</span>
            <span class="hero__stat-label">دوره فعال</span>
          </div>
          <div class="hero__stat-divider"></div>
          <div class="hero__stat">
            <span class="hero__stat-num">۱۵+</span>
            <span class="hero__stat-label">سال تجربه</span>
          </div>
        </div>
      </div>

      <div class="hero__visual">
        <div class="hero__canvas">
          <div class="hero__art-piece hero__art-piece--1"></div>
          <div class="hero__art-piece hero__art-piece--2"></div>
          <div class="hero__art-piece hero__art-piece--3"></div>
          <div class="hero__art-piece hero__art-piece--4"></div>
          <div class="hero__art-piece hero__art-piece--5"></div>
          <div class="hero__ring"></div>
        </div>
      </div>

      <div class="hero__scroll">
        <div class="hero__scroll-line"></div>
        <span>اسکرول کنید</span>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- MARQUEE — Disciplines ticker                                -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <div class="marquee-section">
      <div class="marquee">
        <div class="marquee__track">
          <span v-for="n in 3" :key="n" class="marquee__items">
            <span class="marquee__item">🎨 نقاشی</span>
            <span class="marquee__dot">◆</span>
            <span class="marquee__item">✍️ خوشنویسی</span>
            <span class="marquee__dot">◆</span>
            <span class="marquee__item">🗿 مجسمه‌سازی</span>
            <span class="marquee__dot">◆</span>
            <span class="marquee__item">📸 عکاسی</span>
            <span class="marquee__dot">◆</span>
            <span class="marquee__item">🖌️ گرافیک</span>
            <span class="marquee__dot">◆</span>
            <span class="marquee__item">🏺 سفالگری</span>
            <span class="marquee__dot">◆</span>
            <span class="marquee__item">🎭 هنرهای دیجیتال</span>
            <span class="marquee__dot">◆</span>
          </span>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- PHILOSOPHY — Split layout                                   -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section class="philosophy">
      <div class="container">
        <div class="philosophy__grid">
          <div class="philosophy__text">
            <span class="section-tag">فلسفه ما</span>
            <h2 class="section-title">
              هنر یک <span class="text-accent">سفر</span> است،<br />
              نه یک مقصد
            </h2>
            <p class="philosophy__desc">
              ما باور داریم هر انسانی خلاق به دنیا می‌آید. آموزشگاه یاشیل آرت
              جایی است که این خلاقیت شکوفا می‌شود — با ترکیب آموزش حرفه‌ای،
              فضای الهام‌بخش و راهنمایی اساتیدی که خود هنرمندان برجسته‌ای هستند.
            </p>
            <div class="philosophy__features">
              <div class="philosophy__feature">
                <div class="philosophy__feature-icon">🎯</div>
                <div>
                  <h4>آموزش عملی</h4>
                  <p>بیش از ۷۰٪ زمان کلاس به تمرین عملی اختصاص دارد</p>
                </div>
              </div>
              <div class="philosophy__feature">
                <div class="philosophy__feature-icon">👥</div>
                <div>
                  <h4>کلاس‌های کوچک</h4>
                  <p>حداکثر ۱۵ هنرجو در هر کلاس برای توجه فردی</p>
                </div>
              </div>
              <div class="philosophy__feature">
                <div class="philosophy__feature-icon">🏆</div>
                <div>
                  <h4>گواهینامه معتبر</h4>
                  <p>صدور گواهینامه پایان دوره قابل استعلام</p>
                </div>
              </div>
            </div>
          </div>
          <div class="philosophy__visual">
            <div class="philosophy__img-grid">
              <div class="philosophy__img philosophy__img--1">
                <div class="philosophy__img-inner" style="background: linear-gradient(135deg, #2d6a4f, #1b4332);">
                  <span>🎨</span>
                </div>
              </div>
              <div class="philosophy__img philosophy__img--2">
                <div class="philosophy__img-inner" style="background: linear-gradient(135deg, #c9a96e, #a67c52);">
                  <span>✏️</span>
                </div>
              </div>
              <div class="philosophy__img philosophy__img--3">
                <div class="philosophy__img-inner" style="background: linear-gradient(135deg, #c4725a, #8b3a2a);">
                  <span>🖌️</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- DISCIPLINES — Bento grid                                   -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section class="disciplines">
      <div class="container">
        <div class="disciplines__header">
          <span class="section-tag">رشته‌های آموزشی</span>
          <h2 class="section-title">
            دنیای هنر <span class="text-accent">بی‌پایان</span> است
          </h2>
        </div>

        <div class="bento">
          <router-link
            v-for="(disc, i) in disciplines"
            :key="disc.id"
            :to="`/courses?category=${disc.id}`"
            class="bento__card"
            :class="`bento__card--${i + 1}`"
          >
            <div class="bento__card-bg" :style="{ background: disc.gradient }"></div>
            <div class="bento__card-content">
              <span class="bento__icon">{{ disc.icon }}</span>
              <h3 class="bento__name">{{ disc.name }}</h3>
              <span class="bento__count">{{ disc.course_count }} دوره فعال</span>
            </div>
            <div class="bento__card-hover">
              <span>مشاهده دوره‌ها ←</span>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- FEATURED COURSES — Horizontal scroll cards                 -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section class="featured" v-if="featuredCourses.length">
      <div class="container">
        <div class="featured__header">
          <div>
            <span class="section-tag">محبوب‌ترین دوره‌ها</span>
            <h2 class="section-title">دوره‌های <span class="text-accent">ویژه</span></h2>
          </div>
          <router-link to="/courses" class="featured__see-all">
            مشاهده همه ←
          </router-link>
        </div>
      </div>

      <div class="featured__scroll">
        <div class="featured__track">
          <router-link
            v-for="(c, i) in featuredCourses"
            :key="c.id"
            :to="`/courses/${c.id}/${c.slug}`"
            class="course-card"
          >
            <div class="course-card__img">
              <img v-if="c.thumbnail" :src="c.thumbnail" :alt="c.title" />
              <div v-else class="course-card__placeholder">
                <span>🎨</span>
              </div>
              <div class="course-card__level">{{ c.level_display || c.level }}</div>
            </div>
            <div class="course-card__body">
              <span class="course-card__category">{{ c.category_name }}</span>
              <h3 class="course-card__title">{{ c.title }}</h3>
              <div class="course-card__meta">
                <span>⏱ {{ c.duration_weeks }} هفته</span>
                <span>👤 {{ c.enrolled_count }}/{{ c.max_students }}</span>
              </div>
              <div class="course-card__footer">
                <span class="course-card__price">
                  {{ c.discount_price ? fmt(c.discount_price) + ' تومان' : c.price ? fmt(c.price) + ' تومان' : 'رایگان' }}
                </span>
                <span class="course-card__arrow">←</span>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- INSTRUCTORS — Spotlight section                            -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section class="instructors" v-if="instructors.length">
      <div class="container">
        <div class="instructors__header">
          <span class="section-tag">اساتید ما</span>
          <h2 class="section-title">
            هنرمندان <span class="text-accent">بزرگ</span>، معلمان <span class="text-accent">بزرگ‌تر</span>
          </h2>
        </div>

        <div class="instructors__grid">
          <router-link
            v-for="(inst, i) in instructors"
            :key="inst.id"
            :to="`/instructors/${inst.id}/${inst.slug}`"
            class="instructor-card"
          >
            <div class="instructor-card__avatar" :style="{ borderColor: avatarColors[i % avatarColors.length] }">
              <img v-if="inst.photo" :src="inst.photo" :alt="inst.display_name" />
              <div v-else class="instructor-card__initial" :style="{ background: avatarColors[i % avatarColors.length] }">
                {{ inst.display_name.charAt(0) }}
              </div>
            </div>
            <div class="instructor-card__info">
              <h3>{{ inst.display_name }}</h3>
              <div class="instructor-card__specs">
                <span v-for="s in (inst.specializations || []).slice(0, 2)" :key="s">{{ s }}</span>
              </div>
              <div class="instructor-card__stats">
                <span>⭐ {{ inst.rating }}</span>
                <span>{{ inst.students_count }} هنرجو</span>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- GALLERY — Masonry grid                                     -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section class="gallery-section" v-if="galleryArtworks.length">
      <div class="container">
        <div class="gallery-section__header">
          <div>
            <span class="section-tag">گالری آثار</span>
            <h2 class="section-title">آثار <span class="text-accent">هنری</span> هنرجویان و اساتید</h2>
          </div>
          <router-link to="/gallery" class="gallery-section__see-all">
            مشاهده گالری ←
          </router-link>
        </div>
      </div>

      <div class="masonry">
        <div
          v-for="(art, i) in galleryArtworks"
          :key="art.id"
          class="masonry__item"
          :class="`masonry__item--${(i % 4) + 1}`"
          @click="$router.push(`/gallery/${art.id}/${art.slug}`)"
        >
          <img :src="art.image" :alt="art.title" loading="lazy" />
          <div class="masonry__overlay">
            <h4>{{ art.title }}</h4>
            <span>{{ art.artist_name }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- WORKSHOPS                                                  -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section class="workshops" v-if="upcomingWorkshops.length">
      <div class="container">
        <div class="workshops__header">
          <span class="section-tag">کارگاه‌های ویژه</span>
          <h2 class="section-title">رویدادهای <span class="text-accent">پیش رو</span></h2>
        </div>

        <div class="workshops__grid">
          <router-link
            v-for="(ws, i) in upcomingWorkshops"
            :key="ws.id"
            :to="`/workshops/${ws.id}/${ws.slug}`"
            class="workshop-card"
          >
            <div class="workshop-card__accent" :style="{ background: workshopGradients[i % 3] }"></div>
            <div class="workshop-card__content">
              <div class="workshop-card__badges">
                <span class="workshop-card__badge">{{ ws.duration_type_display }}</span>
                <span class="workshop-card__badge workshop-card__badge--date">{{ ws.start_date }}</span>
              </div>
              <h3 class="workshop-card__title">{{ ws.title }}</h3>
              <div class="workshop-card__details">
                <span>⏰ {{ ws.start_time }}</span>
                <span>📍 {{ ws.location || (ws.is_online ? 'آنلاین' : 'حضوری') }}</span>
              </div>
              <div class="workshop-card__footer">
                <span class="workshop-card__price">{{ fmt(ws.price) }} تومان</span>
                <span v-if="ws.available_spots > 0" class="workshop-card__spots">
                  {{ ws.available_spots }} ظرفیت باقی‌مانده
                </span>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- TESTIMONIALS                                               -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section class="testimonials">
      <div class="container">
        <div class="testimonials__header">
          <span class="section-tag">نظرات هنرجویان</span>
          <h2 class="section-title">چه می‌<span class="text-accent">گویند</span>؟</h2>
        </div>

        <div class="testimonials__grid">
          <div class="testimonial-card" v-for="(t, i) in testimonials" :key="i">
            <div class="testimonial-card__quote">"</div>
            <p class="testimonial-card__text">{{ t.text }}</p>
            <div class="testimonial-card__author">
              <div class="testimonial-card__avatar" :style="{ background: avatarColors[i % avatarColors.length] }">
                {{ t.name.charAt(0) }}
              </div>
              <div>
                <h4>{{ t.name }}</h4>
                <span>{{ t.course }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- WHY US — Features                                          -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section class="why-us">
      <div class="container">
        <div class="why-us__header">
          <span class="section-tag">چرا یاشیل آرت؟</span>
          <h2 class="section-title">مزیت‌های <span class="text-accent">ما</span></h2>
        </div>

        <div class="why-us__grid">
          <div class="why-card" v-for="(item, i) in whyItems" :key="i">
            <div class="why-card__number">{{ String(i + 1).padStart(2, '0') }}</div>
            <div class="why-card__icon">{{ item.icon }}</div>
            <h3>{{ item.title }}</h3>
            <p>{{ item.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- CTA                                                        -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section class="cta-section">
      <div class="cta-section__bg">
        <div class="cta-section__orb cta-section__orb--1"></div>
        <div class="cta-section__orb cta-section__orb--2"></div>
      </div>
      <div class="container">
        <div class="cta-section__content">
          <h2>آماده شروع <span class="text-accent-light">مسیر هنری</span> خود هستید؟</h2>
          <p>همین الان ثبت‌نام کنید و اولین قدم را بردارید</p>
          <div class="cta-section__actions">
            <router-link to="/courses" class="cta-btn cta-btn--primary">ثبت‌نام در دوره‌ها</router-link>
            <router-link to="/contact" class="cta-btn cta-btn--ghost">تماس با ما</router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "LandingPage",
  data() {
    return {
      courseCategories: [],
      featuredCourses: [],
      instructors: [],
      galleryArtworks: [],
      upcomingWorkshops: [],
      avatarColors: ["#2d6a4f", "#c9a96e", "#c4725a", "#1a1a2e", "#6c5ce7", "#0984e3"],
      workshopGradients: ["linear-gradient(135deg, #c4725a, #8b3a2a)", "linear-gradient(135deg, #2d6a4f, #1b4332)", "linear-gradient(135deg, #c9a96e, #a67c52)"],
      disciplines: [
        { id: 1, name: "نقاشی", icon: "🎨", course_count: 12, gradient: "linear-gradient(135deg, #2d6a4f 0%, #1b4332 100%)" },
        { id: 2, name: "خوشنویسی", icon: "✍️", course_count: 8, gradient: "linear-gradient(135deg, #c9a96e 0%, #a67c52 100%)" },
        { id: 3, name: "مجسمه‌سازی", icon: "🗿", course_count: 5, gradient: "linear-gradient(135deg, #c4725a 0%, #8b3a2a 100%)" },
        { id: 4, name: "عکاسی", icon: "📸", course_count: 7, gradient: "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)" },
        { id: 5, name: "گرافیک", icon: "🖌️", course_count: 10, gradient: "linear-gradient(135deg, #6c5ce7 0%, #5541d9 100%)" },
        { id: 6, name: "سفالگری", icon: "🏺", course_count: 4, gradient: "linear-gradient(135deg, #e17055 0%, #d63031 100%)" },
      ],
      testimonials: [
        { name: "مریم احمدی", course: "دوره نقاشی پیشرفته", text: "محیط آموزشگاه فوق‌العاده الهام‌بخش است. استاد رحمتی با صبر و حوصله زیاد، تکنیک‌های پیشرفته نقاشی را آموزش می‌دهند." },
        { name: "علی محمدی", course: "دوره خوشنویسی", text: "از صفر شروع کردم و الان بعد از ۶ ماه می‌توانم آثار حرفه‌ای خلق کنم. بهترین تصمیم زندگیم بود." },
        { name: "سارا کریمی", course: "کارگاه مجسمه‌سازی", text: "کارگاه‌های کوتاه‌مدت عالی هستند. تجربه عملی بسیار ارزشمندی بود و با دوستان هنرمند زیادی آشنا شدم." },
      ],
      whyItems: [
        { icon: "🎓", title: "اساتید مجرب", desc: "تیمی از بهترین هنرمندان ایران با سال‌ها تجربه تدریس و خلق آثار هنری" },
        { icon: "🎨", title: "کارگاه عملی", desc: "بیش از ۷۰٪ زمان آموزش به تمرین و کار عملی اختصاص دارد" },
        { icon: "📜", title: "گواهینامه معتبر", desc: "صدور گواهینامه پایان دوره قابل استعلام و معتبر نزد مراکز فرهنگی" },
        { icon: "🖼️", title: "گالری و نمایشگاه", desc: "فرصت نمایش آثار هنری در گالری آموزشگاه و نمایشگاه‌های عمومی" },
        { icon: "🤝", title: "شبکه هنری", desc: "عضویت در جامعه بزرگ هنرمندان و هنرجویان آموزشگاه" },
        { icon: "💰", title: "هزینه مناسب", desc: "شهریه‌های مقرون‌به‌صرفه با امکان پرداخت اقساطی" },
      ],
    };
  },
  methods: {
    fmt(p) {
      return p ? new Intl.NumberFormat("fa-IR").format(p) : "0";
    },
    async loadCategories() {
      try {
        const { data } = await api.get("/courses/categories/");
        this.courseCategories = data;
      } catch (e) { /* silent */ }
    },
    async loadCourses() {
      try {
        const { data } = await api.get("/courses/", { params: { is_featured: true } });
        this.featuredCourses = (data.results || data).slice(0, 6);
      } catch (e) { /* silent */ }
    },
    async loadInstructors() {
      try {
        const { data } = await api.get("/instructors/", { params: { is_featured: true } });
        this.instructors = (data.results || data).slice(0, 4);
      } catch (e) { /* silent */ }
    },
    async loadGallery() {
      try {
        const { data } = await api.get("/gallery/artworks/", { params: { is_featured: true } });
        this.galleryArtworks = (data.results || data).slice(0, 8);
      } catch (e) { /* silent */ }
    },
    async loadWorkshops() {
      try {
        const { data } = await api.get("/workshops/", { params: { status: "upcoming" } });
        this.upcomingWorkshops = (data.results || data).slice(0, 3);
      } catch (e) { /* silent */ }
    },
  },
  created() {
    this.loadCategories();
    this.loadCourses();
    this.loadInstructors();
    this.loadGallery();
    this.loadWorkshops();
  },
};
</script>

<style scoped>
.landing {
  font-family: "Vazirmatn", Tahoma, sans-serif;
  --accent: #c9a96e;
  --accent-light: #e8d5a8;
  --dark: #0f1410;
  --dark-card: #161d18;
  --cream: #faf7f2;
  --forest: #2d6a4f;
  --terracotta: #c4725a;
  background: var(--cream);
  color: #1a1a1a;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}

.text-accent { color: #c9a96e; }
.text-accent-light { color: #f0dbb4; }

.section-tag {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--accent);
  text-transform: uppercase;
  margin-bottom: 16px;
}
.section-tag::before {
  content: "";
  width: 24px;
  height: 2px;
  background: var(--accent);
  display: inline-block;
}

.section-title {
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  font-weight: 900;
  line-height: 1.3;
  color: #1a1a1a;
  margin-bottom: 24px;
}

/* ═══════════════════════════════════════════════════════════════ */
/* HERO                                                           */
/* ═══════════════════════════════════════════════════════════════ */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: linear-gradient(160deg, #0a1a12 0%, #0f2a1c 30%, #1a2f1e 60%, #0f1f14 100%);
  overflow: hidden;
  padding: 120px 0 80px;
}

.hero__bg {
  position: absolute;
  inset: 0;
}

.hero__grain {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
  opacity: 0.5;
  pointer-events: none;
}

.hero__orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
}
.hero__orb--1 {
  width: 600px;
  height: 600px;
  background: rgba(45, 106, 79, 0.4);
  top: -200px;
  right: 10%;
  animation: float 15s ease-in-out infinite;
}
.hero__orb--2 {
  width: 500px;
  height: 500px;
  background: rgba(201, 169, 110, 0.3);
  bottom: -100px;
  left: 5%;
  animation: float 12s ease-in-out infinite 4s;
}
.hero__orb--3 {
  width: 400px;
  height: 400px;
  background: rgba(196, 114, 90, 0.25);
  top: 40%;
  left: 40%;
  animation: float 18s ease-in-out infinite 8s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(30px, -40px) scale(1.05); }
}

.hero__lines {
  position: absolute;
  inset: 0;
  display: flex;
  justify-content: space-evenly;
  pointer-events: none;
}
.hero__lines span {
  width: 1px;
  height: 100%;
  background: linear-gradient(to bottom, transparent, rgba(201, 169, 110, 0.06), transparent);
}

.hero__content {
  position: relative;
  z-index: 2;
  max-width: 640px;
  padding-left: 40px;
  padding-right: 40px;
}

.hero__tag {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 28px;
}
.hero__tag-line {
  width: 40px;
  height: 2px;
  background: #c9a96e;
}
.hero__tag-text {
  font-size: 0.85rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
  letter-spacing: 0.05em;
}

.hero__title {
  margin-bottom: 24px;
}
.hero__title-line {
  display: block;
}
.hero__title-line--1 {
  font-size: clamp(1rem, 2vw, 1.4rem);
  font-weight: 300;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 4px;
}
.hero__title-line--2 {
  font-size: clamp(4rem, 10vw, 8rem);
  font-weight: 900;
  line-height: 1;
  margin-bottom: 4px;
}
.hero__title-accent {
  background: linear-gradient(135deg, #c9a96e, #f0dbb4, #e8a547);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: shimmer 6s ease-in-out infinite;
  text-shadow: 0 0 60px rgba(201, 169, 110, 0.3);
}
@keyframes shimmer {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
.hero__title-line--3 {
  font-size: clamp(1.4rem, 3vw, 2.2rem);
  font-weight: 700;
  color: rgba(255, 255, 255, 0.95);
}

.hero__subtitle {
  font-size: 1.05rem;
  line-height: 1.9;
  color: rgba(255, 255, 255, 0.65);
  margin-bottom: 36px;
  max-width: 480px;
}

.hero__actions {
  display: flex;
  gap: 16px;
  margin-bottom: 48px;
}

.hero__btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 700;
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  text-decoration: none;
}
.hero__btn--primary {
  background: linear-gradient(135deg, #c9a96e, #e8a547);
  color: #0a1a12;
}
.hero__btn--primary:hover {
  background: linear-gradient(135deg, #e8d5a8, #f0c96e);
  transform: translateY(-3px);
  box-shadow: 0 12px 40px rgba(201, 169, 110, 0.45);
}
.hero__btn--ghost {
  border: 2px solid rgba(201, 169, 110, 0.4);
  color: #c9a96e;
}
.hero__btn--ghost:hover {
  border-color: #c9a96e;
  background: rgba(201, 169, 110, 0.1);
}

.hero__stats {
  display: flex;
  align-items: center;
  gap: 28px;
}
.hero__stat {
  text-align: center;
}
.hero__stat-num {
  display: block;
  font-size: 1.8rem;
  font-weight: 900;
  color: #c9a96e;
}
.hero__stat-label {
  font-size: 0.82rem;
  color: rgba(255, 255, 255, 0.6);
}
.hero__stat-divider {
  width: 1px;
  height: 40px;
  background: rgba(201, 169, 110, 0.25);
}

/* Hero Visual — Art canvas */
.hero__visual {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
  pointer-events: none;
  width: 600px;
  height: 600px;
  opacity: 0.3;
}

.hero__canvas {
  position: relative;
  width: 100%;
  height: 100%;
}

.hero__art-piece {
  position: absolute;
  border-radius: 50%;
}
.hero__art-piece--1 {
  width: 200px;
  height: 200px;
  top: 10%;
  left: 50%;
  background: radial-gradient(circle, var(--accent), transparent);
  animation: orbit 20s linear infinite;
}
.hero__art-piece--2 {
  width: 150px;
  height: 150px;
  top: 30%;
  right: 10%;
  background: radial-gradient(circle, var(--terracotta), transparent);
  animation: orbit 25s linear infinite reverse;
}
.hero__art-piece--3 {
  width: 120px;
  height: 120px;
  bottom: 20%;
  left: 20%;
  background: radial-gradient(circle, var(--forest), transparent);
  animation: orbit 18s linear infinite 3s;
}
.hero__art-piece--4 {
  width: 80px;
  height: 80px;
  top: 60%;
  left: 60%;
  background: radial-gradient(circle, rgba(108, 92, 231, 0.6), transparent);
  animation: orbit 15s linear infinite 6s;
}
.hero__art-piece--5 {
  width: 60px;
  height: 60px;
  top: 15%;
  left: 15%;
  background: radial-gradient(circle, rgba(232, 213, 168, 0.5), transparent);
  animation: orbit 22s linear infinite 2s;
}

.hero__ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  height: 300px;
  border: 2px solid rgba(201, 169, 110, 0.35);
  border-radius: 50%;
  animation: spin 30s linear infinite;
}

@keyframes orbit {
  0% { transform: rotate(0deg) translateX(80px) rotate(0deg); }
  100% { transform: rotate(360deg) translateX(80px) rotate(-360deg); }
}

@keyframes spin {
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

/* Hero scroll indicator */
.hero__scroll {
  position: absolute;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  z-index: 2;
}
.hero__scroll-line {
  width: 1px;
  height: 40px;
  background: linear-gradient(to bottom, #c9a96e, transparent);
  animation: scrollPulse 2s ease-in-out infinite;
}
@keyframes scrollPulse {
  0%, 100% { opacity: 0.4; transform: scaleY(0.6); }
  50% { opacity: 1; transform: scaleY(1); }
}
.hero__scroll span {
  font-size: 0.72rem;
  color: rgba(255, 255, 255, 0.5);
  letter-spacing: 0.1em;
}

/* ═══════════════════════════════════════════════════════════════ */
/* MARQUEE                                                        */
/* ═══════════════════════════════════════════════════════════════ */
.marquee-section {
  background: linear-gradient(160deg, #0a1a12, #0f2a1c);
  border-top: 1px solid rgba(201, 169, 110, 0.2);
  border-bottom: 1px solid rgba(201, 169, 110, 0.2);
  padding: 18px 0;
  overflow: hidden;
}
.marquee {
  overflow: hidden;
}
.marquee__track {
  display: flex;
  gap: 0;
  animation: marqueeScroll 30s linear infinite;
  white-space: nowrap;
}
.marquee__items {
  display: flex;
  align-items: center;
  gap: 24px;
  padding-right: 24px;
}
.marquee__item {
  font-size: 0.92rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.7);
}
.marquee__dot {
  color: #c9a96e;
  font-size: 0.5rem;
  opacity: 0.6;
}
@keyframes marqueeScroll {
  from { transform: translateX(0); }
  to { transform: translateX(-33.33%); }
}

/* ═══════════════════════════════════════════════════════════════ */
/* PHILOSOPHY                                                     */
/* ═══════════════════════════════════════════════════════════════ */
.philosophy {
  padding: 120px 0;
}
.philosophy__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}
.philosophy__desc {
  font-size: 1.05rem;
  line-height: 1.9;
  color: #555;
  margin-bottom: 40px;
}
.philosophy__features {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.philosophy__feature {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}
.philosophy__feature-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(45, 106, 79, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}
.philosophy__feature h4 {
  font-size: 0.95rem;
  font-weight: 700;
  margin-bottom: 4px;
}
.philosophy__feature p {
  font-size: 0.85rem;
  color: #777;
  line-height: 1.6;
}

.philosophy__img-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 200px 200px;
  gap: 16px;
}
.philosophy__img {
  border-radius: 16px;
  overflow: hidden;
}
.philosophy__img--1 {
  grid-row: 1 / 3;
}
.philosophy__img-inner {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.philosophy__img:hover .philosophy__img-inner {
  transform: scale(1.05);
}

/* ═══════════════════════════════════════════════════════════════ */
/* DISCIPLINES — Bento Grid                                      */
/* ═══════════════════════════════════════════════════════════════ */
.disciplines {
  padding: 120px 0;
  background: linear-gradient(180deg, #0a1a12, #0f2a1c, #0a1a12);
}
.disciplines .section-title {
  color: white;
}
.disciplines__header {
  margin-bottom: 60px;
}

.bento {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: 220px 220px;
  gap: 16px;
}
.bento__card {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  text-decoration: none;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.bento__card:hover {
  transform: scale(1.02);
}
.bento__card--1 { grid-column: 1 / 3; }
.bento__card--4 { grid-column: 2 / 4; }
.bento__card--2 { border-left: 3px solid #c9a96e; }
.bento__card--5 { border-left: 3px solid #c9a96e; }

.bento__card-bg {
  position: absolute;
  inset: 0;
  transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.bento__card:hover .bento__card-bg {
  transform: scale(1.05);
}

.bento__card-content {
  position: relative;
  z-index: 1;
  padding: 32px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}
.bento__icon {
  font-size: 2.5rem;
  margin-bottom: 16px;
}
.bento__name {
  font-size: 1.4rem;
  font-weight: 900;
  color: white;
  margin-bottom: 8px;
}
.bento__count {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.6);
}

.bento__card-hover {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}
.bento__card:hover .bento__card-hover {
  opacity: 1;
}
.bento__card-hover span {
  color: white;
  font-weight: 700;
  font-size: 0.95rem;
}

/* ═══════════════════════════════════════════════════════════════ */
/* FEATURED COURSES                                               */
/* ═══════════════════════════════════════════════════════════════ */
.featured {
  padding: 120px 0;
}
.featured__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 40px;
}
.featured__see-all {
  font-size: 0.92rem;
  font-weight: 700;
  color: #2d6a4f;
  text-decoration: none;
  transition: color 0.2s;
}
.featured__see-all:hover {
  color: #c9a96e;
}

.featured__scroll {
  overflow-x: auto;
  padding: 0 24px 20px;
  scrollbar-width: none;
}
.featured__scroll::-webkit-scrollbar { display: none; }

.featured__track {
  display: flex;
  gap: 24px;
  min-width: max-content;
}

.course-card {
  width: 300px;
  flex-shrink: 0;
  border-radius: 16px;
  overflow: hidden;
  background: white;
  border: 1px solid #eee;
  text-decoration: none;
  color: inherit;
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.course-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
}

.course-card__img {
  aspect-ratio: 16 / 10;
  overflow: hidden;
  position: relative;
}
.course-card__img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.course-card:hover .course-card__img img {
  transform: scale(1.08);
}
.course-card__placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #f5f0e8, #ebe5d8);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
}
.course-card__level {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(0, 0, 0, 0.65);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 700;
  backdrop-filter: blur(8px);
}

.course-card__body {
  padding: 20px;
}
.course-card__category {
  font-size: 0.75rem;
  font-weight: 700;
  color: #2d6a4f;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.course-card__title {
  font-size: 1rem;
  font-weight: 800;
  margin: 8px 0;
  line-height: 1.4;
}
.course-card__meta {
  display: flex;
  gap: 16px;
  font-size: 0.8rem;
  color: #999;
  margin-bottom: 16px;
}
.course-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.course-card__price {
  font-weight: 900;
  font-size: 0.95rem;
  color: var(--dark);
}
.course-card__arrow {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--cream);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  transition: all 0.2s;
}
.course-card:hover .course-card__arrow {
  background: #2d6a4f;
  color: white;
}

/* ═══════════════════════════════════════════════════════════════ */
/* INSTRUCTORS                                                    */
/* ═══════════════════════════════════════════════════════════════ */
.instructors {
  padding: 120px 0;
  background: #f5f0e8;
}
.instructors__header {
  margin-bottom: 60px;
}
.instructors__grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.instructor-card {
  text-align: center;
  padding: 36px 24px;
  background: white;
  border-radius: 20px;
  text-decoration: none;
  color: inherit;
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  border: 1px solid transparent;
}
.instructor-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.1);
  border-color: #c9a96e;
}

.instructor-card__avatar {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  border: 3px solid;
  overflow: hidden;
  margin: 0 auto 20px;
}
.instructor-card__avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.instructor-card__initial {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2rem;
  font-weight: 900;
}

.instructor-card__info h3 {
  font-size: 1.05rem;
  font-weight: 800;
  margin-bottom: 10px;
}
.instructor-card__specs {
  display: flex;
  gap: 6px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 12px;
}
.instructor-card__specs span {
  background: #f5f0e8;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.72rem;
  font-weight: 600;
  color: #777;
}
.instructor-card__stats {
  display: flex;
  gap: 12px;
  justify-content: center;
  font-size: 0.82rem;
  color: #999;
}

/* ═══════════════════════════════════════════════════════════════ */
/* GALLERY — Masonry                                              */
/* ═══════════════════════════════════════════════════════════════ */
.gallery-section {
  padding: 120px 0;
}
.gallery-section__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 48px;
}
.gallery-section__see-all {
  font-size: 0.92rem;
  font-weight: 700;
  color: #2d6a4f;
  text-decoration: none;
}
.gallery-section__see-all:hover {
  color: #c9a96e;
}

.masonry {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 200px;
  gap: 12px;
  padding: 0 24px;
}
.masonry__item {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
}
.masonry__item--1 { grid-row: span 2; }
.masonry__item--4 { grid-row: span 2; }

.masonry__item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.masonry__item:hover img {
  transform: scale(1.08);
}

.masonry__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.75), transparent 60%);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 20px;
  opacity: 0;
  transition: opacity 0.3s;
}
.masonry__item:hover .masonry__overlay {
  opacity: 1;
}
.masonry__overlay h4 {
  color: white;
  font-size: 0.95rem;
  font-weight: 700;
  margin-bottom: 4px;
}
.masonry__overlay span {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
}

/* ═══════════════════════════════════════════════════════════════ */
/* WORKSHOPS                                                      */
/* ═══════════════════════════════════════════════════════════════ */
.workshops {
  padding: 120px 0;
  background: linear-gradient(180deg, #0f2a1c, #0a1a12);
}
.workshops .section-title { color: white; }
.workshops__header { margin-bottom: 60px; }

.workshops__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.workshop-card {
  position: relative;
  background: rgba(22, 29, 24, 0.8);
  border-radius: 20px;
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  border: 1px solid rgba(201, 169, 110, 0.1);
  backdrop-filter: blur(10px);
}
.workshop-card:hover {
  transform: translateY(-6px);
  border-color: rgba(201, 169, 110, 0.2);
}

.workshop-card__accent {
  height: 4px;
}
.workshop-card__content {
  padding: 28px;
}
.workshop-card__badges {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}
.workshop-card__badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 700;
  background: rgba(201, 169, 110, 0.18);
  color: #c9a96e;
}
.workshop-card__badge--date {
  background: rgba(255, 255, 255, 0.06);
  color: rgba(255, 255, 255, 0.5);
}
.workshop-card__title {
  font-size: 1.15rem;
  font-weight: 800;
  color: white;
  margin-bottom: 16px;
  line-height: 1.4;
}
.workshop-card__details {
  display: flex;
  gap: 16px;
  font-size: 0.82rem;
  color: rgba(255, 255, 255, 0.4);
  margin-bottom: 20px;
}
.workshop-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.workshop-card__price {
  font-weight: 900;
  color: #c9a96e;
  font-size: 1rem;
}
.workshop-card__spots {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.35);
}

/* ═══════════════════════════════════════════════════════════════ */
/* TESTIMONIALS                                                   */
/* ═══════════════════════════════════════════════════════════════ */
.testimonials {
  padding: 120px 0;
  background: #f5f0e8;
}
.testimonials__header {
  margin-bottom: 60px;
}
.testimonials__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.testimonial-card {
  background: white;
  border-radius: 20px;
  padding: 36px;
  position: relative;
  border: 1px solid #eee;
}
.testimonial-card__quote {
  font-size: 4rem;
  font-weight: 900;
  color: #c9a96e;
  line-height: 1;
  margin-bottom: 8px;
  opacity: 0.5;
}
.testimonial-card__text {
  font-size: 0.95rem;
  line-height: 1.8;
  color: #555;
  margin-bottom: 24px;
}
.testimonial-card__author {
  display: flex;
  align-items: center;
  gap: 12px;
}
.testimonial-card__avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 900;
  font-size: 0.9rem;
}
.testimonial-card__author h4 {
  font-size: 0.9rem;
  font-weight: 700;
}
.testimonial-card__author span {
  font-size: 0.78rem;
  color: #999;
}

/* ═══════════════════════════════════════════════════════════════ */
/* WHY US                                                         */
/* ═══════════════════════════════════════════════════════════════ */
.why-us {
  padding: 120px 0;
}
.why-us__header {
  margin-bottom: 60px;
}
.why-us__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.why-card {
  padding: 36px;
  border-radius: 20px;
  background: white;
  border: 1px solid #eee;
  position: relative;
  overflow: hidden;
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.why-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.08);
  border-color: #c9a96e;
}
.why-card__number {
  position: absolute;
  top: 16px;
  left: 20px;
  font-size: 3rem;
  font-weight: 900;
  color: rgba(0, 0, 0, 0.03);
  line-height: 1;
}
.why-card__icon {
  font-size: 2rem;
  margin-bottom: 20px;
}
.why-card h3 {
  font-size: 1.1rem;
  font-weight: 800;
  margin-bottom: 10px;
}
.why-card p {
  font-size: 0.88rem;
  color: #777;
  line-height: 1.7;
}

/* ═══════════════════════════════════════════════════════════════ */
/* CTA                                                            */
/* ═══════════════════════════════════════════════════════════════ */
.cta-section {
  position: relative;
  padding: 140px 0;
  background: linear-gradient(160deg, #0a1a12 0%, #1a3a2a 50%, #0f2a1c 100%);
  overflow: hidden;
}
.cta-section__bg {
  position: absolute;
  inset: 0;
}
.cta-section__orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
}
.cta-section__orb--1 {
  width: 500px;
  height: 500px;
  background: rgba(201, 169, 110, 0.15);
  top: -200px;
  right: -100px;
}
.cta-section__orb--2 {
  width: 400px;
  height: 400px;
  background: rgba(45, 106, 79, 0.12);
  bottom: -150px;
  left: -100px;
}

.cta-section__content {
  position: relative;
  z-index: 1;
  text-align: center;
}
.cta-section__content h2 {
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  font-weight: 900;
  color: white;
  margin-bottom: 16px;
}
.cta-section__content p {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 40px;
}
.cta-section__actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}
.cta-btn {
  display: inline-flex;
  align-items: center;
  padding: 16px 36px;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s;
}
.cta-btn--primary {
  background: linear-gradient(135deg, #c9a96e, #e8a547);
  color: #0a1a12;
}
.cta-btn--primary:hover {
  background: linear-gradient(135deg, #e8d5a8, #f0c96e);
  transform: translateY(-2px);
}
.cta-btn--ghost {
  border: 2px solid rgba(201, 169, 110, 0.3);
  color: #c9a96e;
}
.cta-btn--ghost:hover {
  border-color: #c9a96e;
  background: rgba(201, 169, 110, 0.08);
}

/* ═══════════════════════════════════════════════════════════════ */
/* RESPONSIVE                                                     */
/* ═══════════════════════════════════════════════════════════════ */
@media (max-width: 1024px) {
  .hero__visual { display: none; }
  .hero__content { padding-right: 0; max-width: 100%; }
  .philosophy__grid { grid-template-columns: 1fr; gap: 60px; }
  .philosophy__visual { display: none; }
  .bento { grid-template-columns: repeat(2, 1fr); grid-template-rows: auto; }
  .bento__card--1, .bento__card--4 { grid-column: auto; }
  .instructors__grid { grid-template-columns: repeat(2, 1fr); }
  .masonry { grid-template-columns: repeat(2, 1fr); grid-auto-rows: 180px; }
  .masonry__item--1, .masonry__item--4 { grid-row: span 1; }
  .workshops__grid { grid-template-columns: 1fr; }
  .testimonials__grid { grid-template-columns: 1fr; }
  .why-us__grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 640px) {
  .hero { padding: 100px 0 60px; min-height: auto; }
  .hero__actions { flex-direction: column; }
  .hero__btn { width: 100%; justify-content: center; }
  .hero__stats { gap: 16px; }
  .hero__stat-num { font-size: 1.4rem; }
  .bento { grid-template-columns: 1fr; }
  .instructors__grid { grid-template-columns: 1fr; }
  .masonry { grid-template-columns: 1fr 1fr; grid-auto-rows: 150px; }
  .why-us__grid { grid-template-columns: 1fr; }
  .cta-section__actions { flex-direction: column; align-items: center; }
  .cta-btn { width: 100%; justify-content: center; max-width: 300px; }
  .featured__header { flex-direction: column; align-items: flex-start; gap: 16px; }
  .gallery-section__header { flex-direction: column; align-items: flex-start; gap: 16px; }
}
</style>
