<template>
  <div class="sema-landing">
    <!-- FIXED SEMA IMAGE - Spins on scroll -->
    <div class="fixed-sema" :style="semaStyle">
      <div class="sema-canvas">
        <!-- Dervish 1 (Center - White) -->
        <div class="dervish d1" :style="{ transform: `rotate(${scrollY * 0.8}deg)` }">
          <div class="dervish-body">
            <div class="dervish-head"></div>
            <div class="dervish-hat"></div>
            <div class="dervish-arms">
              <div class="arm arm-left"></div>
              <div class="arm arm-right"></div>
            </div>
            <div class="dervish-skirt"></div>
          </div>
        </div>
        <!-- Dervish 2 (Left - Blue) -->
        <div class="dervish d2" :style="{ transform: `rotate(${-scrollY * 0.6}deg)` }">
          <div class="dervish-body blue">
            <div class="dervish-head"></div>
            <div class="dervish-hat"></div>
            <div class="dervish-arms">
              <div class="arm arm-left"></div>
              <div class="arm arm-right"></div>
            </div>
            <div class="dervish-skirt"></div>
          </div>
        </div>
        <!-- Dervish 3 (Right - Blue) -->
        <div class="dervish d3" :style="{ transform: `rotate(${scrollY * 0.7}deg)` }">
          <div class="dervish-body blue">
            <div class="dervish-head"></div>
            <div class="dervish-hat"></div>
            <div class="dervish-arms">
              <div class="arm arm-left"></div>
              <div class="arm arm-right"></div>
            </div>
            <div class="dervish-skirt"></div>
          </div>
        </div>
        <!-- Spiral effect -->
        <div class="spiral" :style="{ transform: `rotate(${scrollY * 0.4}deg)` }"></div>
        <!-- Particles -->
        <div class="sema-particles" :style="{ opacity: particleOpacity }">
          <span v-for="n in 16" :key="n" class="sp" :style="spStyle(n)"></span>
        </div>
      </div>
    </div>

    <!-- SCROLLABLE CONTENT -->
    <div class="content">
      <!-- HERO -->
      <section class="hero">
        <div class="hero-bg">
          <div class="bg-orb b1"></div>
          <div class="bg-orb b2"></div>
          <div class="bg-orb b3"></div>
        </div>
        <div class="container hero-inner">
          <div class="hero-text" data-scroll="fade-up">
            <span class="hero-label">
              <span class="dot"></span>
              آموزشگاه آزاد هنرهای تجسمی یاشیل
            </span>
            <h1>
              <span class="thin">جایی که</span>
              <span class="bold">
                <span class="magic">هنر</span>
              </span>
              <span class="medium">زندگی می‌شود</span>
            </h1>
            <p>از نقاشی تا مجسمه‌سازی — مسیر یادگیری هنر را اینجا شروع کنید</p>
            <div class="btns">
              <router-link to="/courses" class="btn-gold">مشاهده دوره‌ها</router-link>
              <router-link to="/gallery" class="btn-ghost">گالری آثار</router-link>
            </div>
          </div>
        </div>
      </section>

      <!-- MARQUEE -->
      <div class="marquee">
        <div class="marquee-track">
          <span v-for="n in 2" :key="n">
            <span>🎨 نقاشی</span>
            <span>✍️ خوشنویسی</span>
            <span>🗿 مجسمه‌سازی</span>
            <span>📸 عکاسی</span>
            <span>🖌️ گرافیک</span>
            <span>🏺 سفالگری</span>
          </span>
        </div>
      </div>

      <!-- CATEGORIES -->
      <section class="section">
        <div class="container">
          <div class="sec-hdr" data-scroll="fade-up">
            <div class="accent"></div>
            <h2>رشته‌های <span class="hl-r">آموزشی</span></h2>
          </div>
          <div class="cat-row">
            <router-link
              v-for="(cat, i) in courseCategories"
              :key="cat.id"
              :to="`/courses?category=${cat.id}`"
              class="cat-card"
              data-scroll="fade-up"
              :data-delay="i * 80"
            >
              <div class="cat-icon" :style="{ background: grads[i % grads.length] }">{{ cat.icon || '🎭' }}</div>
              <h3>{{ cat.name }}</h3>
              <span>{{ cat.course_count }} دوره</span>
            </router-link>
          </div>
        </div>
      </section>

      <!-- COURSES -->
      <section class="section alt">
        <div class="container">
          <div class="sec-hdr" data-scroll="fade-up">
            <div class="accent"></div>
            <h2>محبوب‌ترین <span class="hl-p">دوره‌ها</span></h2>
          </div>
          <div class="course-row">
            <router-link
              v-for="(c, i) in featuredCourses"
              :key="c.id"
              :to="`/courses/${c.id}/${c.slug}`"
              class="crd"
              data-scroll="fade-up"
              :data-delay="i * 100"
            >
              <div class="crd-img">
                <img v-if="c.thumbnail" :src="c.thumbnail" :alt="c.title" />
                <div v-else class="crd-ph">🎨</div>
              </div>
              <div class="crd-body">
                <span class="crd-cat">{{ c.category_name }}</span>
                <h3>{{ c.title }}</h3>
                <div class="crd-meta">
                  <span>⏱ {{ c.duration_weeks }} هفته</span>
                  <span>👤 {{ c.enrolled_count }}/{{ c.max_students }}</span>
                </div>
                <span class="crd-price">{{ c.discount_price ? fmt(c.discount_price) + ' تومان' : c.price ? fmt(c.price) + ' تومان' : 'رایگان' }}</span>
              </div>
            </router-link>
          </div>
          <div class="ctr" data-scroll="fade-up">
            <router-link to="/courses" class="lnk">مشاهده همه دوره‌ها ←</router-link>
          </div>
        </div>
      </section>

      <!-- INSTRUCTORS -->
      <section class="section">
        <div class="container">
          <div class="sec-hdr" data-scroll="fade-up">
            <div class="accent"></div>
            <h2>اساتید <span class="hl-g">ما</span></h2>
          </div>
          <div class="inst-row">
            <router-link
              v-for="(inst, i) in instructors"
              :key="inst.id"
              :to="`/instructors/${inst.id}/${inst.slug}`"
              class="inst-crd"
              data-scroll="fade-up"
              :data-delay="i * 100"
            >
              <div class="inst-av" :style="{ borderColor: avClrs[i % avClrs.length] }">
                <img v-if="inst.photo" :src="inst.photo" :alt="inst.display_name" />
                <div v-else class="inst-i" :style="{ background: avClrs[i % avClrs.length] }">{{ inst.display_name.charAt(0) }}</div>
              </div>
              <h3>{{ inst.display_name }}</h3>
              <div class="inst-tags">
                <span v-for="s in (inst.specializations || []).slice(0, 2)" :key="s">{{ s }}</span>
              </div>
              <div class="inst-m">
                <span>⭐ {{ inst.rating }}</span>
                <span>👤 {{ inst.students_count }}</span>
              </div>
            </router-link>
          </div>
        </div>
      </section>

      <!-- GALLERY -->
      <section class="section dark">
        <div class="container">
          <div class="sec-hdr" data-scroll="fade-up">
            <div class="accent"></div>
            <h2>گالری <span class="hl-y">آثار هنری</span></h2>
          </div>
          <div class="gal-row">
            <div
              v-for="(art, i) in galleryArtworks"
              :key="art.id"
              class="gal-item"
              data-scroll="scale-in"
              :data-delay="i * 80"
              @click="openArtwork(art)"
            >
              <img :src="art.image" :alt="art.title" loading="lazy" />
              <div class="gal-ov">
                <span>{{ art.title }}</span>
                <small>{{ art.artist_name }}</small>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- WORKSHOPS -->
      <section class="section alt">
        <div class="container">
          <div class="sec-hdr" data-scroll="fade-up">
            <div class="accent"></div>
            <h2>کارگاه‌های <span class="hl-o">ویژه</span></h2>
          </div>
          <div class="ws-row">
            <router-link
              v-for="(ws, i) in upcomingWorkshops"
              :key="ws.id"
              :to="`/workshops/${ws.id}/${ws.slug}`"
              class="ws-crd"
              data-scroll="fade-up"
              :data-delay="i * 120"
            >
              <div class="ws-top" :style="{ background: wsGrads[i % wsGrads.length] }">
                <span>{{ ws.duration_type_display }}</span>
                <span>{{ ws.start_date }}</span>
              </div>
              <div class="ws-body">
                <h3>{{ ws.title }}</h3>
                <div class="ws-m">
                  <span>⏰ {{ ws.start_time }}</span>
                  <span>📍 {{ ws.location || (ws.is_online ? 'آنلاین' : 'حضوری') }}</span>
                </div>
                <div class="ws-p">
                  <span>{{ fmt(ws.price) }} تومان</span>
                  <span v-if="ws.available_spots > 0" class="sp">{{ ws.available_spots }} ظرفیت</span>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </section>

      <!-- WHY + CTA -->
      <section class="section dark cta">
        <div class="cta-bg">
          <div class="orb o1"></div>
          <div class="orb o2"></div>
        </div>
        <div class="container">
          <div class="why-row" data-scroll="fade-up">
            <div class="why-c" v-for="(item, i) in whyItems" :key="i">
              <div class="why-ic" :style="{ background: whyClrs[i] }">{{ item.icon }}</div>
              <h3>{{ item.title }}</h3>
              <p>{{ item.desc }}</p>
            </div>
          </div>
          <div class="cta-ct" data-scroll="fade-up">
            <h2>آماده شروع <span class="hl-y">مسیر هنری</span> خود هستید؟</h2>
            <div class="cta-b">
              <router-link to="/courses" class="btn-gold">مشاهده دوره‌ها</router-link>
              <router-link to="/contact" class="btn-ghost light">تماس با ما</router-link>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "LandingPage",
  data() {
    return {
      scrollY: 0,
      courseCategories: [],
      featuredCourses: [],
      instructors: [],
      galleryArtworks: [],
      upcomingWorkshops: [],
      grads: ["linear-gradient(135deg,#ff6b6b,#c0392b)","linear-gradient(135deg,#6c5ce7,#a29bfe)","linear-gradient(135deg,#00b894,#55efc4)","linear-gradient(135deg,#fdcb6e,#f39c12)","linear-gradient(135deg,#e84393,#fd79a8)","linear-gradient(135deg,#0984e3,#74b9ff)"],
      avClrs: ["#ff6b6b","#6c5ce7","#00b894","#e84393","#0984e3","#fdcb6e"],
      wsGrads: ["linear-gradient(135deg,#e84393,#fd79a8)","linear-gradient(135deg,#0984e3,#74b9ff)","linear-gradient(135deg,#00b894,#55efc4)"],
      whyClrs: ["rgba(255,107,107,0.12)","rgba(108,92,231,0.12)","rgba(0,184,148,0.12)","rgba(253,203,110,0.12)"],
      whyItems: [
        { icon: "🎓", title: "اساتید مجرب", desc: "تیمی از بهترین هنرمندان با سال‌ها تجربه" },
        { icon: "🎨", title: "کارگاه عملی", desc: "آموزش همراه با تمرین عملی" },
        { icon: "📜", title: "گواهینامه معتبر", desc: "گواهینامه پایان دوره قابل استعلام" },
        { icon: "🖼️", title: "گالری و نمایشگاه", desc: "فرصت نمایش آثار هنری" },
      ],
    };
  },
  computed: {
    semaStyle() {
      const p = Math.min(1, this.scrollY / 1000);
      const opacity = this.scrollY < 50 ? 1 : Math.max(0.2, 1 - p * 0.8);
      const scale = 0.5 + p * 0.6;
      const blur = p > 0.8 ? (p - 0.8) * 12 : 0;
      return {
        opacity,
        transform: `scale(${scale})`,
        filter: blur > 0 ? `blur(${blur}px)` : 'none',
      };
    },
    particleOpacity() {
      if (this.scrollY < 100) return 0;
      if (this.scrollY > 800) return 0;
      return Math.min(1, (this.scrollY - 100) / 200);
    },
  },
  methods: {
    fmt(p) { return p ? new Intl.NumberFormat("fa-IR").format(p) : "0"; },
    openArtwork(a) { this.$router.push(`/gallery/${a.id}/${a.slug}`); },
    spStyle(n) {
      const angle = (n / 16) * Math.PI * 2;
      const dist = 100 + Math.random() * 80;
      const size = 3 + Math.random() * 6;
      const colors = ["#ff6b6b","#6c5ce7","#00b894","#fdcb6e","#e84393","#0984e3"];
      return {
        width: `${size}px`, height: `${size}px`,
        background: colors[n % colors.length],
        transform: `translate(${Math.cos(angle) * dist}px, ${Math.sin(angle) * dist}px)`,
      };
    },
    handleScroll() { this.scrollY = window.scrollY; },
    setupObserver() {
      const obs = new IntersectionObserver((entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            const d = parseInt(e.target.dataset.delay || "0");
            setTimeout(() => e.target.classList.add("visible"), d);
          }
        });
      }, { threshold: 0.1 });
      document.querySelectorAll("[data-scroll]").forEach((el) => obs.observe(el));
    },
    async loadCategories() { try { const { data } = await api.get("/courses/categories/"); this.courseCategories = data; } catch (e) {} },
    async loadCourses() { try { const { data } = await api.get("/courses/", { params: { is_featured: true } }); this.featuredCourses = (data.results || data).slice(0, 4); } catch (e) {} },
    async loadInstructors() { try { const { data } = await api.get("/instructors/", { params: { is_featured: true } }); this.instructors = (data.results || data).slice(0, 4); } catch (e) {} },
    async loadGallery() { try { const { data } = await api.get("/gallery/artworks/", { params: { is_featured: true } }); this.galleryArtworks = (data.results || data).slice(0, 5); } catch (e) {} },
    async loadWorkshops() { try { const { data } = await api.get("/workshops/", { params: { status: "upcoming" } }); this.upcomingWorkshops = (data.results || data).slice(0, 3); } catch (e) {} },
  },
  mounted() {
    window.addEventListener("scroll", this.handleScroll, { passive: true });
    this.$nextTick(() => this.setupObserver());
  },
  beforeDestroy() { window.removeEventListener("scroll", this.handleScroll); },
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
.hl-r{color:#ff6b6b}.hl-p{color:#6c5ce7}.hl-g{color:#00b894}.hl-o{color:#f39c12}.hl-y{color:#fdcb6e}

/* SCROLL ANIMATIONS */
[data-scroll]{opacity:0;transition:all .8s cubic-bezier(.16,1,.3,1)}
[data-scroll="fade-up"]{transform:translateY(50px)}
[data-scroll="scale-in"]{transform:scale(.85)}
[data-scroll].visible{opacity:1!important;transform:none!important}

/* ============================================
   FIXED SEMA - Whirling Dervishes
   ============================================ */
.fixed-sema {
  position: fixed;
  top: 50%;
  right: 6%;
  transform: translateY(-50%);
  z-index: 10;
  pointer-events: none;
  transition: opacity .3s, transform .3s, filter .3s;
}

.sema-canvas {
  position: relative;
  width: 380px;
  height: 380px;
}

/* Dervish Base */
.dervish {
  position: absolute;
  transition: transform .05s linear;
}

.d1 { top: 20%; left: 30%; }
.d2 { top: 25%; left: 5%; }
.d3 { top: 20%; right: 5%; }

.dervish-body {
  position: relative;
  width: 120px;
  height: 160px;
}

/* Head */
.dervish-head {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 24px;
  height: 24px;
  background: #f5e6d3;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0,0,0,.2);
}

/* Hat (Sikke) */
.dervish-hat {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  width: 16px;
  height: 20px;
  background: #8b7355;
  border-radius: 3px 3px 0 0;
  clip-path: polygon(20% 100%, 80% 100%, 65% 0%, 35% 0%);
}

.dervish-body.blue .dervish-hat {
  background: #2980b9;
}

/* Arms */
.dervish-arms {
  position: absolute;
  top: 30px;
  left: 0;
  width: 100%;
  height: 60px;
}

.arm {
  position: absolute;
  top: 0;
  width: 50px;
  height: 6px;
  background: #f5e6d3;
  border-radius: 3px;
  transform-origin: right center;
}

.dervish-body.blue .arm {
  background: #3498db;
}

.arm-left {
  right: 50%;
  transform: rotate(-45deg);
  transform-origin: right center;
}

.arm-right {
  left: 50%;
  transform: rotate(45deg);
  transform-origin: left center;
}

/* Skirt */
.dervish-skirt {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 55px solid transparent;
  border-right: 55px solid transparent;
  border-bottom: 90px solid #f0f0f0;
  border-radius: 0 0 50% 50%;
  filter: drop-shadow(0 4px 12px rgba(0,0,0,.15));
}

.dervish-body.blue .dervish-skirt {
  border-bottom-color: #2980b9;
}

/* Spiral Effect */
.spiral {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 200px;
  height: 200px;
  border: 2px dashed rgba(255, 107, 107, 0.15);
  border-radius: 50%;
  transition: transform .05s linear;
}

.spiral::before {
  content: '';
  position: absolute;
  inset: 20px;
  border: 2px dashed rgba(108, 92, 231, 0.1);
  border-radius: 50%;
}

.spiral::after {
  content: '';
  position: absolute;
  inset: 40px;
  border: 2px dashed rgba(0, 184, 148, 0.08);
  border-radius: 50%;
}

/* Particles */
.sema-particles {
  position: absolute;
  top: 50%;
  left: 50%;
  transition: opacity .3s;
}

.sp {
  position: absolute;
  border-radius: 50%;
  transition: transform .5s cubic-bezier(.16,1,.3,1);
}

/* ============================================
   CONTENT
   ============================================ */
.content { position: relative; z-index: 5; }

/* HERO */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: #0a0a1a;
  overflow: hidden;
}

.hero-bg { position: absolute; inset: 0; }

.bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
}

.b1 { width: 400px; height: 400px; background: rgba(255,107,107,.15); top: -100px; right: 20%; animation: orbFloat 12s ease infinite; }
.b2 { width: 350px; height: 350px; background: rgba(108,92,231,.1); bottom: -80px; left: 10%; animation: orbFloat 15s ease infinite 3s; }
.b3 { width: 300px; height: 300px; background: rgba(0,184,148,.08); top: 40%; left: 40%; animation: orbFloat 10s ease infinite 6s; }

@keyframes orbFloat {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(30px, -30px); }
}

.hero-inner {
  position: relative;
  z-index: 1;
  max-width: 550px;
  padding-right: 420px;
}

.hero-label {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: rgba(255,255,255,.5);
  font-size: .88rem;
  margin-bottom: 20px;
}

.dot {
  width: 8px; height: 8px;
  background: #ff6b6b;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(255,107,107,.4); }
  50% { box-shadow: 0 0 0 8px rgba(255,107,107,0); }
}

.hero-text h1 { color: white; margin-bottom: 20px; }
.thin { display: block; font-size: 1.3rem; font-weight: 300; opacity: .5; }
.bold { display: block; font-size: 5rem; font-weight: 900; line-height: 1.1; }

.magic {
  background: linear-gradient(135deg, #ff6b6b, #fdcb6e, #6c5ce7, #00b894, #ff6b6b);
  background-size: 400% 400%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradFlow 8s ease infinite;
}

@keyframes gradFlow {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.medium { display: block; font-size: 2.2rem; font-weight: 700; margin-top: 8px; }
.hero-text p { color: rgba(255,255,255,.45); font-size: 1.05rem; line-height: 1.8; margin-bottom: 28px; }
.btns { display: flex; gap: 14px; }

.btn-gold {
  display: inline-flex; align-items: center; padding: 14px 32px; border-radius: 10px;
  font-weight: 700; color: #0a0a1a;
  background: linear-gradient(135deg, #ff6b6b, #fdcb6e);
  transition: transform .3s, box-shadow .3s;
}
.btn-gold:hover { transform: translateY(-3px); box-shadow: 0 8px 32px rgba(255,107,107,.4); }

.btn-ghost {
  display: inline-flex; align-items: center; padding: 14px 32px; border-radius: 10px;
  font-weight: 600; color: white; border: 1px solid rgba(255,255,255,.2);
  transition: all .3s;
}
.btn-ghost:hover { background: rgba(255,255,255,.08); }
.btn-ghost.light { border-color: rgba(255,255,255,.3); }

/* MARQUEE */
.marquee { background: #ff6b6b; padding: 12px 0; overflow: hidden; }
.marquee-track { display: flex; gap: 40px; animation: scroll 20s linear infinite; white-space: nowrap; }
.marquee-track span span { font-size: .95rem; font-weight: 700; color: white; }
@keyframes scroll { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

/* SECTIONS */
.section { padding: 80px 0; border-top: 1px solid #eee; }
.section:nth-child(odd) { background: white; }
.section.alt { background: #faf7f2; }
.section.dark { background: #0a0a1a; }

.sec-hdr { text-align: center; margin-bottom: 40px; }
.accent { width: 50px; height: 4px; background: linear-gradient(90deg, #ff6b6b, #6c5ce7); border-radius: 2px; margin: 0 auto 14px; }
.sec-hdr h2 { font-size: 1.8rem; color: #1a1a2e; }
.section.dark .sec-hdr h2 { color: white; }

/* CATEGORIES */
.cat-row { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 14px; }
.cat-card { text-align: center; padding: 24px 14px; background: white; border-radius: 14px; border: 1px solid #eee; transition: all .3s; }
.cat-card:hover { transform: translateY(-6px); box-shadow: 0 12px 32px rgba(0,0,0,.08); }
.cat-icon { width: 56px; height: 56px; border-radius: 14px; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; font-size: 1.5rem; }
.cat-card h3 { font-size: .92rem; margin-bottom: 4px; }
.cat-card span { font-size: .75rem; color: #888; }

/* COURSES */
.course-row { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }
.crd { border-radius: 14px; overflow: hidden; background: white; border: 1px solid #eee; transition: all .3s; }
.crd:hover { transform: translateY(-6px); box-shadow: 0 12px 32px rgba(0,0,0,.1); }
.crd-img { aspect-ratio: 16/10; overflow: hidden; }
.crd-img img { width: 100%; height: 100%; object-fit: cover; transition: transform .5s; }
.crd:hover .crd-img img { transform: scale(1.08); }
.crd-ph { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; background: linear-gradient(135deg, #ff6b6b10, #6c5ce710); }
.crd-body { padding: 14px; }
.crd-cat { font-size: .72rem; font-weight: 600; color: #6c5ce7; }
.crd-body h3 { font-size: .92rem; margin: 4px 0; }
.crd-meta { display: flex; gap: 12px; font-size: .78rem; color: #888; margin-bottom: 8px; }
.crd-price { font-weight: 800; font-size: .88rem; }

.ctr { text-align: center; margin-top: 32px; }
.lnk { display: inline-flex; padding: 12px 28px; border: 2px solid #1a1a2e; border-radius: 10px; font-weight: 700; font-size: .9rem; color: #1a1a2e; transition: all .3s; }
.lnk:hover { background: #1a1a2e; color: white; }

/* INSTRUCTORS */
.inst-row { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px; }
.inst-crd { text-align: center; padding: 28px 16px; background: white; border-radius: 14px; border: 1px solid #eee; transition: all .3s; }
.inst-crd:hover { transform: translateY(-6px); box-shadow: 0 12px 32px rgba(0,0,0,.08); }
.inst-av { width: 80px; height: 80px; border-radius: 50%; border: 3px solid; overflow: hidden; margin: 0 auto 12px; }
.inst-av img { width: 100%; height: 100%; object-fit: cover; }
.inst-i { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.6rem; font-weight: 700; }
.inst-crd h3 { font-size: .92rem; margin-bottom: 8px; }
.inst-tags { display: flex; gap: 4px; justify-content: center; flex-wrap: wrap; margin-bottom: 10px; }
.inst-tags span { background: #f0f0f0; padding: 2px 8px; border-radius: 8px; font-size: .7rem; font-weight: 600; color: #888; }
.inst-m { display: flex; gap: 12px; justify-content: center; font-size: .78rem; color: #888; }

/* GALLERY */
.gal-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
.gal-item { position: relative; border-radius: 10px; overflow: hidden; cursor: pointer; aspect-ratio: 1; }
.gal-item:first-child { grid-column: 1 / 3; grid-row: 1 / 3; aspect-ratio: auto; }
.gal-item img { width: 100%; height: 100%; object-fit: cover; transition: transform .5s; }
.gal-item:hover img { transform: scale(1.1); }
.gal-ov { position: absolute; inset: 0; background: linear-gradient(transparent 40%, rgba(10,10,26,.9)); display: flex; flex-direction: column; justify-content: flex-end; padding: 12px; opacity: 0; transition: opacity .3s; color: white; }
.gal-item:hover .gal-ov { opacity: 1; }
.gal-ov span { font-weight: 700; font-size: .85rem; }
.gal-ov small { font-size: .75rem; color: rgba(255,255,255,.7); }

/* WORKSHOPS */
.ws-row { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.ws-crd { border-radius: 14px; overflow: hidden; background: white; border: 1px solid #eee; transition: all .3s; }
.ws-crd:hover { transform: translateY(-6px); box-shadow: 0 12px 32px rgba(0,0,0,.08); }
.ws-top { padding: 14px 18px; display: flex; justify-content: space-between; color: white; font-size: .82rem; font-weight: 600; }
.ws-body { padding: 16px; }
.ws-body h3 { font-size: .95rem; margin-bottom: 8px; }
.ws-m { display: flex; gap: 12px; font-size: .78rem; color: #888; margin-bottom: 10px; }
.ws-p { display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: .88rem; }
.sp { font-size: .75rem; color: #00b894; font-weight: 600; }

/* WHY + CTA */
.why-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 60px; }
.why-c { text-align: center; padding: 28px 16px; background: rgba(255,255,255,.05); border-radius: 14px; border: 1px solid rgba(255,255,255,.1); }
.why-ic { width: 52px; height: 52px; border-radius: 14px; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; font-size: 1.5rem; }
.why-c h3 { font-size: .95rem; color: white; margin-bottom: 6px; }
.why-c p { font-size: .82rem; color: rgba(255,255,255,.5); line-height: 1.6; }

.cta-ct { text-align: center; }
.cta-ct h2 { font-size: 2rem; color: white; margin-bottom: 24px; }
.cta-b { display: flex; gap: 14px; justify-content: center; }
.cta-bg { position: absolute; inset: 0; }
.orb { position: absolute; border-radius: 50%; filter: blur(80px); }
.o1 { width: 400px; height: 400px; background: rgba(255,107,107,.2); top: -100px; right: -100px; }
.o2 { width: 300px; height: 300px; background: rgba(108,92,231,.2); bottom: -100px; left: -100px; }

/* RESPONSIVE */
@media (max-width: 1100px) {
  .fixed-sema { display: none; }
  .hero-inner { padding-right: 0; }
}

@media (max-width: 640px) {
  .hero { min-height: auto; padding: 80px 0 60px; }
  .bold { font-size: 2.5rem; }
  .medium { font-size: 1.4rem; }
  .btns { flex-direction: column; align-items: center; }
  .btn-gold, .btn-ghost { width: 100%; justify-content: center; }
  .cat-row { grid-template-columns: repeat(2, 1fr); }
  .course-row { grid-template-columns: 1fr; }
  .inst-row { grid-template-columns: 1fr 1fr; }
  .gal-row { grid-template-columns: repeat(2, 1fr); }
  .gal-item:first-child { grid-column: auto; grid-row: auto; }
  .ws-row { grid-template-columns: 1fr; }
  .why-row { grid-template-columns: 1fr; }
  .cta-ct h2 { font-size: 1.4rem; }
  .cta-b { flex-direction: column; align-items: center; }
}
</style>
