<template>
  <div class="lp">
    <!-- Scroll progress hairline -->
    <div class="lp-progress" ref="scrollbar" aria-hidden="true"></div>

    <!-- ═══════════════════════════════════════════════════════════
         HERO — آتلیه‌ی زنده
    ═══════════════════════════════════════════════════════════ -->
    <section class="hero" ref="hero">
      <div class="hero__bg" aria-hidden="true">
        <div class="hero__grain"></div>
        <div class="hero__orb hero__orb--a"></div>
        <div class="hero__orb hero__orb--b"></div>
        <div class="hero__orb hero__orb--c"></div>
        <div class="hero__halo"></div>
        <div class="hero__lines">
          <span v-for="n in 7" :key="n"></span>
        </div>
      </div>
      <canvas class="hero__dust" ref="dust" aria-hidden="true"></canvas>

      <div class="container hero__grid">
        <!-- متن -->
        <div class="hero__copy">
          <div class="hero__eyebrow rise" style="animation-delay: 0.05s">
            <span class="hero__eyebrow-dot"></span>
            <span>آموزشگاه آزاد هنرهای تجسمی یاشیل آرت</span>
          </div>

          <h1 class="hero__title">
            <span class="hero__line rise" style="animation-delay: 0.15s">جایی که</span>
            <span class="hero__line rise" style="animation-delay: 0.28s">
              <span class="hero__word-gold fd">هنر</span>&nbsp;زنده می‌شود
            </span>
            <span class="hero__line hero__line--sub rise" style="animation-delay: 0.42s">
              و هر قلمی، داستانی تازه می‌آفریند
            </span>
          </h1>

          <p class="hero__sub rise" style="animation-delay: 0.56s">
            از نقاشی رنگ‌روغن تا مجسمه‌سازی، از خوشنویسی تا سفال — در کنار
            برترین اساتید، با دست‌هایی که کار می‌کنند و آتلیه‌هایی که نفس می‌کشند.
          </p>

          <div class="hero__actions rise" style="animation-delay: 0.7s">
            <router-link to="/courses" class="lp-btn lp-btn--gold">
              <span>شروع مسیر هنری</span>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
            </router-link>
            <router-link to="/gallery" class="lp-btn lp-btn--ghost">گالری آثار</router-link>
          </div>

          <div class="hero__facts rise" style="animation-delay: 0.84s">
            <div class="hero__fact">
              <b>۵۰۰+</b><span>هنرجوی فعال</span>
            </div>
            <i class="hero__fact-sep"></i>
            <div class="hero__fact">
              <b>۵۰+</b><span>دوره و کارگاه</span>
            </div>
            <i class="hero__fact-sep"></i>
            <div class="hero__fact">
              <b>۱۲</b><span>رشته تخصصی</span>
            </div>
          </div>
        </div>

        <!-- تابلو -->
        <div class="hero__stage" ref="stage">
          <div class="stage-frame">
            <div class="stage-frame__inner">
              <div class="stage-art" ref="stageArt">
                <div class="stage-art__wash stage-art__wash--a"></div>
                <div class="stage-art__wash stage-art__wash--b"></div>
                <div class="stage-art__wash stage-art__wash--c"></div>
                <svg class="stage-art__drawing" viewBox="0 0 420 520" fill="none" aria-hidden="true">
                  <circle cx="210" cy="200" r="150" stroke="rgba(233,211,164,.5)" stroke-width="1.4" stroke-dasharray="2 10" stroke-linecap="round" />
                  <circle cx="210" cy="200" r="96" stroke="rgba(233,211,164,.85)" stroke-width="1.2" stroke-dasharray="60 34 4 34" stroke-linecap="round" class="stage-art__spin" />
                  <path d="M46 452 C 120 372, 150 396, 214 330 S 330 236, 374 186" stroke="#E39B7A" stroke-width="13" stroke-linecap="round" opacity=".85" />
                  <path d="M40 482 C 132 400, 200 428, 262 366 S 342 300, 388 252" stroke="#E9D3A4" stroke-width="5" stroke-linecap="round" opacity=".55" />
                  <path d="M84 208 C 130 150, 200 130, 246 168 S 302 236, 252 286" stroke="rgba(240,240,220,.5)" stroke-width="2" stroke-linecap="round" />
                  <circle cx="210" cy="128" r="7" fill="#E9D3A4" />
                  <circle cx="128" cy="352" r="5" fill="#E39B7A" />
                  <circle cx="300" cy="300" r="9" fill="none" stroke="#E9D3A4" stroke-width="2" />
                  <circle cx="96" cy="252" r="4" fill="#fff" opacity=".7" />
                </svg>
                <span class="stage-art__gesso"></span>
              </div>
            </div>
          </div>
          <span class="stage-chip stage-chip--a">نقاشی رنگ‌روغن</span>
          <span class="stage-chip stage-chip--b">کارگاه سفال</span>
          <span class="stage-chip stage-chip--c">آتلیه باز هر جمعه</span>
          <div class="stage-seal" aria-hidden="true"><span>ی</span></div>
        </div>
      </div>

      <div class="hero__cue" aria-hidden="true">
        <span class="hero__cue-line"></span>
        <span>اسکرول</span>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════
         MARQUEE
    ═══════════════════════════════════════════════════════════ -->
    <div class="marquee" aria-hidden="true">
      <div class="marquee__track">
        <div v-for="set in 2" :key="set" class="marquee__set">
          <span v-for="d in ticker" :key="d" class="marquee__item">
            <b>{{ d }}</b>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.4 7.6L22 12l-7.6 2.4L12 22l-2.4-7.6L2 12l7.6-2.4z"/></svg>
          </span>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════
         MANIFESTO + شمارنده‌ها
    ═══════════════════════════════════════════════════════════ -->
    <section class="manifesto">
      <div class="container manifesto__grid">
        <div class="manifesto__copy">
          <div class="lp-eyebrow rv"><span>فلسفهٔ ما</span></div>
          <h2 class="lp-title rv" style="--d: 80ms">
            هنر <span class="tl">آموختنی</span> است؛<br />
            مثل هر زبان دیگری
          </h2>
          <p class="manifesto__lead rv" style="--d: 160ms">
            یاشیل آرت فقط یک کلاس نیست؛ یک <b>آتلیه‌ی باز</b> است. جایی که
            هنرجو کنار هنرمند می‌نشیند، ابزار را دست می‌گیرد و از همان جلسهٔ
            اول، خلق می‌کند — چون باور داریم هنر با دیدن یاد گرفته نمی‌شود؛
            با <b>انجام دادن</b>.
          </p>

          <div class="manifesto__points">
            <div class="m-point rv" style="--d: 120ms">
              <span class="m-point__mark">۰۱</span>
              <div>
                <h4>استودیوهای زنده</h4>
                <p>آموزش در فضای کارگاه واقعی، با نور، ابزار و بومِ واقعی</p>
              </div>
            </div>
            <div class="m-point rv" style="--d: 220ms">
              <span class="m-point__mark">۰۲</span>
              <div>
                <h4>کلاس‌های کوچک</h4>
                <p>حداکثر ۱۵ نفر تا استاد، چشم‌به‌چشمِ هر هنرجو باشد</p>
              </div>
            </div>
            <div class="m-point rv" style="--d: 320ms">
              <span class="m-point__mark">۰۳</span>
              <div>
                <h4>گواهینامهٔ معتبر</h4>
                <p>پایان هر دوره، گواهی قابل استعلام متناسب با همان رشته</p>
              </div>
            </div>
          </div>
        </div>

        <div class="manifesto__visual rv" style="--d: 200ms">
          <div class="m-collage">
            <div class="m-collage__back"></div>
            <div class="m-collage__tile m-collage__tile--1">
              <span>برس و بوم</span>
            </div>
            <div class="m-collage__tile m-collage__tile--2">
              <span>گِل و دست</span>
            </div>
            <div class="m-collage__stamp fd">ی</div>
          </div>
          <p class="m-caption">«هر اثر، امضای لحظه‌ای است که در آن نفس کشیده‌ایم.»</p>
        </div>
      </div>

      <!-- شمارنده‌ها -->
      <div class="container">
        <div class="counters">
          <div class="counter rv" v-for="(c, i) in counters" :key="c.label" :style="{ '--d': i * 90 + 'ms' }">
            <div class="counter__num">
              <b class="js-count" :data-to="c.to">{{ c.prefix }}</b><span v-if="c.suffix">{{ c.suffix }}</span>
            </div>
            <span class="counter__label">{{ c.label }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════
         ATELIER — سکشن سینماییِ چسبان به اسکرول
    ═══════════════════════════════════════════════════════════ -->
    <section class="atelier" ref="atelier">
      <div class="atelier__words" aria-hidden="true">
        <span v-for="(s, i) in atelierSteps" :key="s.word" class="atelier__word fd" :class="{ 'is-on': i === step }">{{ s.word }}</span>
      </div>
      <div class="atelier__pin" ref="pin">
        <div class="atelier__bg" aria-hidden="true">
          <span class="atelier__orb atelier__orb--a"></span>
          <span class="atelier__orb atelier__orb--b"></span>
        </div>

        <div class="atelier__art" ref="artWrap">
          <canvas class="atelier__dust" ref="atelDust" aria-hidden="true"></canvas>
          <div class="atelier__frame" ref="artFrame">
            <svg class="atelier__core" ref="artCore" viewBox="0 0 420 520" fill="none" aria-hidden="true">
              <defs>
                <linearGradient id="lpG1" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0" stop-color="#2b5547" />
                  <stop offset="1" stop-color="#14352c" />
                </linearGradient>
                <linearGradient id="lpG2" x1="0" y1="1" x2="1" y2="0">
                  <stop offset="0" stop-color="#C96F4A" />
                  <stop offset="1" stop-color="#E9D3A4" />
                </linearGradient>
              </defs>
              <rect width="420" height="520" fill="url(#lpG1)" />
              <path d="M0 470 C 110 430, 150 452, 250 428 S 380 440, 420 402 L 420 520 L 0 520 Z" fill="#0b1915" opacity=".6" />
              <circle cx="212" cy="212" r="150" fill="none" stroke="rgba(233,211,164,.5)" stroke-width="1.5" stroke-dasharray="3 12" stroke-linecap="round" />
              <g class="atelier__spinner">
                <circle cx="212" cy="212" r="118" fill="none" stroke="url(#lpG2)" stroke-width="2" stroke-dasharray="170 200" stroke-linecap="round" />
                <circle cx="212" cy="94" r="5" fill="#E9D3A4" />
              </g>
              <path d="M56 438 C 130 358, 168 388, 232 322 S 336 232, 380 182" stroke="#E39B7A" stroke-width="16" stroke-linecap="round" opacity=".9" />
              <path d="M46 470 C 150 388, 210 420, 280 356 S 372 296, 404 268" stroke="#E9D3A4" stroke-width="5" stroke-linecap="round" opacity=".6" />
              <path d="M88 190 C 138 122, 220 104, 268 148 S 320 226, 258 290" stroke="rgba(255,247,232,.75)" stroke-width="2.4" stroke-linecap="round" />
              <circle cx="96" cy="120" r="8" fill="#E9D3A4" opacity=".9" />
              <circle cx="330" cy="330" r="14" fill="none" stroke="#E39B7A" stroke-width="3" />
              <circle cx="120" cy="330" r="3.5" fill="#fff" opacity=".8" />
              <circle cx="330" cy="150" r="3" fill="#E9D3A4" opacity=".8" />
              <circle cx="212" cy="380" r="2.6" fill="#E39B7A" opacity=".9" />
            </svg>
            <div class="atelier__gloss" ref="artGloss"></div>
          </div>
          <div class="atelier__ring" ref="artRing" aria-hidden="true"></div>
        </div>

        <div class="atelier__copy">
          <div class="lp-eyebrow lp-eyebrow--light">مسیر یک اثر</div>
          <h2 class="atelier__title">
            هر شاهکار، از یک
            <span class="tl">ضربه قلم</span> شروع شد
          </h2>
          <p class="atelier__intro">
            ما تو را تا لحظه‌ای همراهی می‌کنیم که اثرت از دیوار آتلیه به
            دیوار گالری برسد — سه ایستگاه، یک مسیر.
          </p>

          <div class="atelier__steps">
            <div
              v-for="(s, i) in atelierSteps"
              :key="s.word"
              class="a-step"
              :class="{ 'is-active': i === step }"
            >
              <div class="a-step__head">
                <b class="a-step__num">{{ s.n }}</b>
                <h3>{{ s.title }}</h3>
                <span class="a-step__bar"><i :class="{ full: i < step }"></i></span>
              </div>
              <p>{{ s.text }}</p>
            </div>
          </div>

          <router-link to="/courses" class="lp-btn lp-btn--gold lp-btn--sm">
            مسیرت را انتخاب کن
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
          </router-link>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════
         DISCIPLINES — گرید هنری
    ═══════════════════════════════════════════════════════════ -->
    <section class="disciplines">
      <div class="container">
        <div class="lp-head">
          <div>
            <div class="lp-eyebrow rv">رشته‌های آموزشی</div>
            <h2 class="lp-title rv" style="--d: 80ms">
              دنیای هنر، <span class="tl">بی‌پایان</span> است
            </h2>
          </div>
          <p class="lp-head__note rv" style="--d: 160ms">
            دوره‌های منظم و کارگاه‌های کوتاه‌مدت و بلندمدت؛ از نخستین خط تا
            تکنیک‌های پیشرفته، در هر سن و هر سطحی.
          </p>
        </div>

        <div class="bento">
          <router-link
            v-for="(disc, i) in disciplines"
            :key="disc.id"
            to="/courses"
            class="bento__card rv"
            :class="'bento__card--' + (i + 1)"
            :style="{ '--d': (i % 3) * 90 + 'ms', '--grad': disc.gradient }"
          >
            <span class="bento__bg"></span>
            <span class="bento__glyph" aria-hidden="true"></span>
            <span class="bento__icon">{{ disc.icon }}</span>
            <div class="bento__txt">
              <h3>{{ disc.name }}</h3>
              <span>{{ disc.course_count }} دوره فعال</span>
            </div>
            <span class="bento__arrow">←</span>
          </router-link>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════
         مسیر یادگیری (سطوح)
    ═══════════════════════════════════════════════════════════ -->
    <section class="pathway">
      <div class="container">
        <div class="lp-head lp-head--center">
          <div class="lp-eyebrow rv">آغاز از هر نقطـه</div>
          <h2 class="lp-title rv" style="--d: 80ms">
            مسیرت را از <span class="tl">همین امروز</span> شروع کن
          </h2>
          <p class="rv" style="--d: 140ms">
            برنامهٔ آموزشی انعطاف‌پذیر؛ هم ساعت‌های ثابت و هم کلاس‌های هماهنگ‌شده با زمان تو.
          </p>
        </div>

        <div class="levels">
          <div
            v-for="(lv, i) in levels"
            :key="lv.key"
            class="level rv"
            :style="{ '--d': i * 110 + 'ms', '--tone': lv.tone }"
          >
            <span class="level__stripe"></span>
            <span class="level__index fd">{{ lv.index }}</span>
            <div class="level__icon">{{ lv.icon }}</div>
            <h3>{{ lv.title }}</h3>
            <p>{{ lv.desc }}</p>
            <ul>
              <li v-for="f in lv.items" :key="f">{{ f }}</li>
            </ul>
            <router-link to="/courses" class="level__link">
              مشاهدهٔ دوره‌های این سطح ←
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- دوره‌های شاخص (داده واقعی) -->
    <section class="featured" v-if="featuredCourses.length">
      <div class="container">
        <div class="lp-head">
          <div>
            <div class="lp-eyebrow">دوره‌های شاخص</div>
            <h2 class="lp-title">این روزها، آتلیه‌ها <span class="tl">پر از رنگ</span> است</h2>
          </div>
          <router-link to="/courses" class="lp-link">مشاهدهٔ همهٔ دوره‌ها ←</router-link>
        </div>
      </div>
      <div class="courserow">
        <router-link
          v-for="(c, i) in featuredCourses"
          :key="c.id"
          :to="`/courses/${c.id}/${c.slug}`"
          class="ccard rv"
          :style="{ '--d': (i % 4) * 70 + 'ms' }"
        >
          <div class="ccard__thumb">
            <img v-if="c.thumbnail" :src="c.thumbnail" :alt="c.title" loading="lazy" />
            <div v-else class="ccard__ph">
              <svg viewBox="0 0 80 80" fill="none" aria-hidden="true"><path d="M8 62 C 24 50, 30 56, 44 44 S 64 28, 72 18" stroke="currentColor" stroke-width="5" stroke-linecap="round"/><circle cx="24" cy="26" r="5" fill="currentColor"/></svg>
            </div>
            <span class="ccard__level">{{ c.level_display || c.level }}</span>
          </div>
          <div class="ccard__body">
            <span class="ccard__cat">{{ c.category_name || 'دورهٔ تخصصی' }}</span>
            <h3>{{ c.title }}</h3>
            <div class="ccard__meta">
              <span>⏱ {{ c.duration_weeks }} هفته</span>
              <span>👥 {{ c.enrolled_count }}/{{ c.max_students }}</span>
            </div>
            <div class="ccard__foot">
              <b v-if="c.price">{{ fmt(c.discount_price || c.price) }} تومان</b>
              <b v-else>رایگان</b>
              <span class="ccard__go">←</span>
            </div>
          </div>
        </router-link>
      </div>
    </section>

    <!-- کارگاه‌ها -->
    <section class="workshops" v-if="upcomingWorkshops.length">
      <div class="container">
        <div class="lp-head lp-head--dark">
          <div>
            <div class="lp-eyebrow lp-eyebrow--light">کارگاه‌های ویژه</div>
            <h2 class="lp-title lp-title--light">رویدادهای <span class="tl">پیشِ رو</span></h2>
          </div>
          <router-link to="/workshops" class="lp-link lp-link--light">همهٔ کارگاه‌ها ←</router-link>
        </div>
        <div class="workshops__grid">
          <router-link
            v-for="(ws, i) in upcomingWorkshops"
            :key="ws.id"
            :to="`/workshops/${ws.id}/${ws.slug}`"
            class="wcard rv"
            :style="{ '--d': i * 110 + 'ms' }"
          >
            <div class="wcard__date">
              <b>{{ ws.start_date }}</b>
            </div>
            <div class="wcard__content">
              <div class="wcard__chips">
                <span>{{ ws.duration_type_display }}</span>
                <span v-if="ws.is_online">آنلاین</span>
                <span v-else>حضوری</span>
              </div>
              <h3>{{ ws.title }}</h3>
              <p>{{ ws.start_time }} · {{ ws.location || 'آموزشگاه یاشیل آرت' }}</p>
              <div class="wcard__foot">
                <b>{{ fmt(ws.price) }} تومان</b>
                <span class="wcard__cap">{{ ws.available_spots }} ظرفیت باقی‌مانده</span>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════
         GALLERY — همیشه حاضر (با داده یا قاب‌های هنری)
    ═══════════════════════════════════════════════════════════ -->
    <section class="gallery-sec">
      <div class="container">
        <div class="lp-head">
          <div>
            <div class="lp-eyebrow rv">گالری یاشیل</div>
            <h2 class="lp-title rv" style="--d: 80ms">
              دیواری از <span class="tl">دست‌ها</span>ی هنرجویان و اساتید
            </h2>
          </div>
          <router-link to="/gallery" class="lp-link rv" style="--d: 160ms">ورود به گالری ←</router-link>
        </div>
      </div>
      <div class="gallery-sec__strip">
        <router-link
          v-for="(g, i) in galleryItems"
          :key="'g' + i"
          to="/gallery"
          class="gwork rv"
          :class="'gwork--' + ((i % 5) + 1)"
          :style="{ '--d': (i % 5) * 80 + 'ms' }"
        >
          <img v-if="g.image" :src="g.image" :alt="g.title" loading="lazy" />
          <div v-else class="gwork__art" :style="{ '--grad': g.gradient }">
            <svg viewBox="0 0 60 80" fill="none" aria-hidden="true"><path d="M8 64 C 20 50, 26 58, 38 44 S 54 26, 58 18" stroke="currentColor" stroke-width="4" stroke-linecap="round"/><circle cx="46" cy="20" r="3" fill="currentColor"/></svg>
            <b class="fd">{{ g.big }}</b>
          </div>
          <div class="gwork__overlay">
            <h4>{{ g.title }}</h4>
            <span>{{ g.artist_name || g.note }}</span>
          </div>
        </router-link>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════
         TESTIMONIALS
    ═══════════════════════════════════════════════════════════ -->
    <section class="voices">
      <div class="container">
        <div class="lp-head lp-head--center">
          <div class="lp-eyebrow rv">از زبان هنرجوها</div>
          <h2 class="lp-title rv" style="--d: 80ms">صدای <span class="tl">کارگاه</span> را بشنو</h2>
        </div>
        <div class="voices__grid">
          <figure v-for="(t, i) in testimonials" :key="i" class="voice rv" :style="{ '--d': i * 120 + 'ms' }">
            <span class="voice__mark fd">”</span>
            <blockquote>{{ t.text }}</blockquote>
            <figcaption>
              <span class="voice__avatar" :style="{ background: avatarColors[i % avatarColors.length] }">{{ t.name.charAt(0) }}</span>
              <div>
                <b>{{ t.name }}</b>
                <span>{{ t.course }}</span>
              </div>
            </figcaption>
          </figure>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════
         CTA پایانی
    ═══════════════════════════════════════════════════════════ -->
    <section class="final-cta">
      <div class="final-cta__bg" aria-hidden="true">
        <span class="final-cta__ring final-cta__ring--a"></span>
        <span class="final-cta__ring final-cta__ring--b"></span>
        <span class="final-cta__ring final-cta__ring--c"></span>
        <div class="hero__grain"></div>
      </div>
      <div class="container">
        <div class="final-cta__inner">
          <span class="final-cta__kicker fd">یاشیل آرت</span>
          <h2 class="final-cta__title">
            قلم را زمین نگذار؛
            <span class="tl">بوم</span> منتظر توست
          </h2>
          <p>
            اولین جلسهٔ مشاوره و تعیین سطح، رایگان است. بیا، ببین و انتخاب کن —
            صندلیِ کنار پنجره هنوز خالی است.
          </p>
          <div class="final-cta__actions">
            <router-link to="/register" class="lp-btn lp-btn--gold lp-btn--lg">ثبت‌نام رایگان</router-link>
            <router-link to="/contact" class="lp-btn lp-btn--ghost lp-btn--lg">مشاورهٔ مسیر هنری</router-link>
          </div>
          <div class="final-cta__chips">
            <span>گواهینامهٔ قابل استعلام</span>
            <span>کلاس‌های کوچک</span>
            <span>آتلیهٔ باز</span>
          </div>
          <router-link to="/shop" class="final-cta__shop">
            و اگر به آثارِ آماده علاقه داری، <b>فروشگاه یاشیل</b> همیشه باز است ←
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import api from "@/services/api";

const clamp = (v, min, max) => Math.min(max, Math.max(min, v));

export default {
  name: "LandingPage",
  data() {
    return {
      featuredCourses: [],
      galleryArtworks: [],
      upcomingWorkshops: [],
      step: 0,
      avatarColors: ["#2d6a4f", "#a67c52", "#c4725a", "#16324a", "#6c5ce7", "#b3452c"],
      counters: [
        { to: 500, suffix: "+", label: "هنرجوی فعال" },
        { to: 50, suffix: "+", label: "دوره و کارگاه" },
        { to: 15, suffix: "+", label: "سال تجربه" },
        { to: 12, suffix: "", label: "رشتهٔ تخصصی" },
      ],
      ticker: ["نقاشی", "خوشنویسی", "مجسمه‌سازی", "سفالگری", "عکاسی", "گرافیک", "طراحی", "هنر دیجیتال", "آبرنگ", "معماری داخلی"],
      atelierSteps: [
        { n: "۰۱", word: "خلق", title: "از نخستین ضربه", text: "بدون پیش‌نیاز وارد می‌شوی؛ استاد کنارت می‌نشیند و اولین خط را با تو می‌کشد. اشتباه اینجا نه‌تنها ایراد نیست، بخشی از تمرین است." },
        { n: "۰۲", word: "تمرین", title: "آتلیه‌ی باز، هر روز", text: "بین جلسه‌ها، آتلیه برای تمرین آزاد است. ابزار و بوم در دسترس‌اند و اساتید در ساعات مشخص، برای رفع اشکال کنارت می‌مانند." },
        { n: "۰۳", word: "نمایش", title: "از دیوار کارگاه تا گالری", text: "آثار برگزیده در گالری یاشیل به نمایش گذاشته می‌شوند؛ با گواهی پایان دوره و فرصت عرضهٔ اثر در فروشگاه آموزشگاه." },
      ],
      disciplines: [
        { id: 1, name: "نقاشی", icon: "🎨", course_count: 12, gradient: "radial-gradient(120% 120% at 20% 0%, #2f6152 0%, #14352c 58%, #0d241d 100%)" },
        { id: 2, name: "خوشنویسی", icon: "🖋", course_count: 8, gradient: "radial-gradient(120% 120% at 80% 0%, #d8b57e 0%, #a67c52 55%, #5f4323 100%)" },
        { id: 3, name: "مجسمه‌سازی", icon: "🗿", course_count: 5, gradient: "radial-gradient(120% 120% at 20% 0%, #cf7b5e 0%, #a34f33 55%, #5c2314 100%)" },
        { id: 4, name: "سفالگری", icon: "🏺", course_count: 4, gradient: "radial-gradient(120% 120% at 30% 10%, #9a7a5a 0%, #6f5336 55%, #3a2a17 100%)" },
        { id: 5, name: "عکاسی", icon: "📷", course_count: 7, gradient: "radial-gradient(120% 120% at 80% 0%, #274d68 0%, #14283c 55%, #0a1520 100%)" },
        { id: 6, name: "طراحی و گرافیک", icon: "✏️", course_count: 10, gradient: "radial-gradient(120% 120% at 30% 0%, #6b5a9e 0%, #43356e 55%, #241a44 100%)" },
      ],
      levels: [
        {
          key: "beginner", index: "۰۱", icon: "🌱", tone: "#3f7a5f", title: "مبتدی — از صفر",
          desc: "نیازی به تجربه نیست؛ فقط علاقه کافی است.",
          items: ["آشنایی با ابزار و متریال", "خط، فرم و ترکیب‌بندی", "پروژه‌های قدم‌به‌قدم"],
        },
        {
          key: "intermediate", index: "۰۲", icon: "🎯", tone: "#b8860b", title: "متوسط — تکنیک",
          desc: "برای کسانی که پایه را دارند و عمق می‌خواهند.",
          items: ["تکنیک‌های پیشرفتهٔ هر رشته", "کار از طبیعت و مدل زنده", "نقد و تحلیل آثار"],
        },
        {
          key: "advanced", index: "۰۳", icon: "🔥", tone: "#c96f4a", title: "پیشرفته — حرفه‌ای",
          desc: "آماده‌سازی برای نمایشگاه و فروش اثر.",
          items: ["سبک شخصی و پرتفولیو", "کیوریت و آماده‌سازی اثر", "همراهی تا اولین نمایشگاه"],
        },
      ],
      fallbackGallery: [
        { title: "آبرنگ روی کاغذ", big: "ب", gradient: "linear-gradient(160deg,#e8b46b,#c96f4a)", note: "اثر هنرجوی دورهٔ آبرنگ" },
        { title: "سیاه‌قلم", big: "ق", gradient: "linear-gradient(160deg,#3a3f4b,#171b23)", note: "اثر هنرجوی دورهٔ طراحی" },
        { title: "سفال دست‌ساز", big: "خ", gradient: "linear-gradient(160deg,#b98d5e,#6f5336)", note: "اثر کارگاه سفالگری" },
        { title: "خوشنویسی نستعلیق", big: "ی", gradient: "linear-gradient(160deg,#1f4b43,#0d241d)", note: "اثر هنرجوی دورهٔ خوشنویسی" },
        { title: "رنگ‌روغن", big: "ش", gradient: "linear-gradient(160deg,#9c4a6b,#4d1f38)", note: "اثر استاد مهمان گالری" },
        { title: "عکس چاپ دستی", big: "ا", gradient: "linear-gradient(160deg,#33556e,#152a3f)", note: "اثر هنرجوی دورهٔ عکاسی" },
      ],
      testimonials: [
        { name: "مریم احمدی", course: "دورهٔ نقاشی پیشرفته", text: "محیط آموزشگاه فوق‌العاده الهام‌بخش است. استاد رحمتی با صبر زیاد، تکنیک‌های پیشرفتهٔ رنگ‌روغن را قدم‌به‌قدم با من جلو رفت." },
        { name: "علی محمدی", course: "دورهٔ خوشنویسی", text: "از صفر شروع کردم و بعد از شش ماه توانستم آثار قابل ارائه خلق کنم. انعطاف ساعت کلاس‌ها برای من که شاغل هستم، نجات‌بخش بود." },
        { name: "سارا کریمی", course: "کارگاه مجسمه‌سازی", text: "کارگاه‌های کوتاه‌مدت عالی‌اند؛ تجربهٔ عملی واقعی و آشنایی با یک شبکهٔ هنری که هنوز هم با آن در ارتباطم." },
      ],
    };
  },
  computed: {
    galleryItems() {
      const items = [];
      (this.galleryArtworks || []).slice(0, 6).forEach((a) => items.push(a));
      let i = 0;
      while (items.length < 6) {
        items.push({ ...this.fallbackGallery[i % this.fallbackGallery.length], _fallback: true });
        i += 1;
      }
      return items.slice(0, 6);
    },
  },
  methods: {
    fmt(p) {
      return p ? new Intl.NumberFormat("fa-IR").format(p) : "۰";
    },
    /* ---------- بارگذاری داده ---------- */
    async loadCourses() {
      try {
        const { data } = await api.get("/courses/", { params: { is_featured: true } });
        this.featuredCourses = (data.results || data).slice(0, 8);
      } catch (e) { /* بی‌صدا */ }
    },
    async loadGallery() {
      try {
        const { data } = await api.get("/gallery/artworks/", { params: { is_featured: true } });
        this.galleryArtworks = (data.results || data).slice(0, 6);
      } catch (e) { /* بی‌صدا */ }
    },
    async loadWorkshops() {
      try {
        const { data } = await api.get("/workshops/", { params: { status: "upcoming" } });
        this.upcomingWorkshops = (data.results || data).slice(0, 3);
      } catch (e) { /* بی‌صدا */ }
    },

    /* ---------- ابزار موشن ---------- */
    prefersReduced() {
      return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    },
    isMobile() {
      return window.innerWidth < 820;
    },
    fmtFaNum(v) {
      return new Intl.NumberFormat("fa-IR").format(Math.round(v));
    },

    setupMotion() {
      if (this.prefersReduced()) {
        this.$el.classList.add("is-reduced");
        return; // همه‌چیز بدون موشن دیده می‌شود
      }
      const mobile = this.isMobile();
      this.bindScroll();
      this.setupReveals();
      this.setupCounters();
      if (!mobile) {
        this.initDust();
        this.setupStagePointer();
      }
      this.setupAtelier(!mobile);
      window.addEventListener("resize", this.onResize, { passive: true });
    },
    onResize() {
      if (this.isMobile()) {
        if (this.dust) this.stopDust();
      } else if (!this.dust) {
        this.initDust();
      }
    },

    bindScroll() {
      this.scrollTicking = false;
      this.onScroll = () => {
        if (this.scrollTicking) return;
        this.scrollTicking = true;
        window.requestAnimationFrame(() => {
          this.tick();
          this.scrollTicking = false;
        });
      };
      window.addEventListener("scroll", this.onScroll, { passive: true });
      this.tick();
    },

    /* پارالاکس تابلؤ هیرو با نشانگر موس */
    applyHeroPointer() {
      if (!this.pointer) return;
      const stage = this.$refs.stage;
      if (!stage) return;
      this.pointer.x += (this.pointer.tx - this.pointer.x) * 0.08;
      this.pointer.y += (this.pointer.ty - this.pointer.y) * 0.08;
      stage.style.transform = `translate3d(${(this.pointer.x * -20).toFixed(2)}px, ${(this.pointer.y * -14).toFixed(2)}px, 0)`;
    },

    tick() {
      const doc = document.documentElement;
      const max = doc.scrollHeight - window.innerHeight;
      const y = window.scrollY;
      const progress = max > 0 ? y / max : 0;
      const bar = this.$refs.scrollbar;
      if (bar) bar.style.transform = `scaleX(${progress})`;
      this.scrubAtelier();
      this.applyHeroPointer();
      this.parallaxLayers();
    },

    /* افکت‌های Reveal با IntersectionObserver */
    setupReveals() {
      const els = this.$el.querySelectorAll(".rv");
      if (!els.length) return;
      if (!("IntersectionObserver" in window)) {
        els.forEach((el) => el.classList.add("in"));
        return;
      }
      this.io = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("in");
              this.io.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
      );
      els.forEach((el) => this.io.observe(el));
    },

    /* شمارنده‌های اعداد فارسی */
    setupCounters() {
      const els = this.$el.querySelectorAll(".js-count");
      if (!els.length) return;
      const run = (el) => {
        const to = parseFloat(el.dataset.to || "0");
        const t0 = performance.now();
        const dur = 1500;
        const ease = (t) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t));
        const frame = (now) => {
          const p = clamp((now - t0) / dur, 0, 1);
          el.textContent = this.fmtFaNum(to * ease(p));
          if (p < 1) window.requestAnimationFrame(frame);
        };
        window.requestAnimationFrame(frame);
      };
      if (!("IntersectionObserver" in window)) {
        els.forEach(run);
        return;
      }
      this.countIO = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              run(entry.target);
              this.countIO.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.4 }
      );
      els.forEach((el) => this.countIO.observe(el));
    },

    /* ذرات طلایی هیرو */
    initDust() {
      const canvas = this.$refs.dust;
      if (!canvas) return;
      const hero = this.$refs.hero;
      const ctx = canvas.getContext("2d");
      if (!ctx) return;
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const W = (canvas.width = Math.floor(hero.clientWidth * dpr));
      const H = (canvas.height = Math.floor(hero.clientHeight * dpr));
      canvas.style.width = hero.clientWidth + "px";
      canvas.style.height = hero.clientHeight + "px";
      const N = clamp(Math.floor((hero.clientWidth * hero.clientHeight) / 26000), 24, 85);
      const parts = Array.from({ length: N }, () => ({
        x: Math.random() * W,
        y: Math.random() * H,
        r: (0.4 + Math.random() * 1.6) * dpr,
        vy: (0.05 + Math.random() * 0.22) * dpr,
        ph: Math.random() * Math.PI * 2,
        sp: 0.004 + Math.random() * 0.012,
        gold: Math.random() > 0.28,
      }));
      this.dust = { ctx, parts, W, H, raf: 0 };
      const draw = () => {
        if (this.dust === undefined) return;
        const { ctx: c, parts: p, W: w, H: h } = this.dust;
        c.clearRect(0, 0, w, h);
        for (const pt of p) {
          pt.y -= pt.vy;
          pt.ph += pt.sp;
          if (pt.y < -6) { pt.y = h + 6; pt.x = Math.random() * w; }
          const tw = 0.35 + 0.65 * Math.abs(Math.sin(pt.ph));
          c.beginPath();
          c.arc(pt.x, pt.y, pt.r, 0, Math.PI * 2);
          c.fillStyle = pt.gold
            ? `rgba(233,211,164,${0.5 * tw})`
            : `rgba(255,247,232,${0.35 * tw})`;
          c.fill();
        }
        this.dust.raf = window.requestAnimationFrame(draw);
      };
      draw();
    },
    stopDust() {
      if (this.dust) {
        window.cancelAnimationFrame(this.dust.raf);
        this.dust = undefined;
      }
    },

    /* پارالاکس نشانگر موس روی تابلو هیرو */
    setupStagePointer() {
      const stage = this.$refs.stage;
      if (!stage) return;
      this.pointer = { tx: 0, ty: 0, x: 0, y: 0 };
      const hero = this.$refs.hero;
      const onMove = (e) => {
        const r = hero.getBoundingClientRect();
        this.pointer.tx = (e.clientX - r.left) / r.width - 0.5;
        this.pointer.ty = (e.clientY - r.top) / r.height - 0.5;
      };
      const onLeave = () => { this.pointer.tx = 0; this.pointer.ty = 0; };
      hero.addEventListener("mousemove", onMove, { passive: true });
      hero.addEventListener("mouseleave", onLeave, { passive: true });
      this.pointerCleanup = () => {
        hero.removeEventListener("mousemove", onMove);
        hero.removeEventListener("mouseleave", onLeave);
      };
    },

    /* بخش چسبانِ آتلیه — پاک‌کردن/چرخش/ذرات با اسکرول */
    setupAtelier(withDust) {
      this.atelierW = { p: 0 };
      if (withDust) {
        const canvas = this.$refs.atelDust;
        if (canvas) {
          const ctx = canvas.getContext("2d");
          if (ctx) {
            const dpr = Math.min(window.devicePixelRatio || 1, 2);
            const pin = this.$refs.pin;
            const W = (canvas.width = Math.floor(pin.clientWidth * dpr));
            const H = (canvas.height = Math.floor(pin.clientHeight * dpr));
            canvas.style.width = pin.clientWidth + "px";
            canvas.style.height = pin.clientHeight + "px";
            this.atelierDust = {
              ctx, W, H, raf: 0,
              parts: Array.from({ length: 46 }, () => ({
                x: Math.random() * W, y: Math.random() * H,
                r: (0.5 + Math.random() * 1.8) * dpr,
                vx: (Math.random() - 0.5) * 0.12 * dpr,
                vy: (0.06 + Math.random() * 0.2) * dpr,
                ph: Math.random() * Math.PI * 2,
              })),
            };
          }
        }
      }
    },
    drawAtelierDust() {
      const d = this.atelierDust;
      if (!d) return;
      const c = d.ctx;
      c.clearRect(0, 0, d.W, d.H);
      const a = Math.sin(this.atelierW.p * Math.PI); // اوج در میانه
      c.globalAlpha = a * 0.85;
      for (const pt of d.parts) {
        pt.x += pt.vx; pt.y -= pt.vy; pt.ph += 0.01;
        if (pt.y < -6) { pt.y = d.H + 6; }
        if (pt.x < -6) pt.x = d.W + 6; else if (pt.x > d.W + 6) pt.x = -6;
        c.beginPath();
        c.arc(pt.x, pt.y, pt.r * (0.6 + 0.4 * Math.abs(Math.sin(pt.ph))), 0, Math.PI * 2);
        c.fillStyle = "#e9d3a4";
        c.fill();
      }
      c.globalAlpha = 1;
    },

    scrubAtelier() {
      const el = this.$refs.atelier;
      if (!el || !this.$refs.pin) return;
      const rect = el.getBoundingClientRect();
      const vh = window.innerHeight;
      if (rect.bottom < 0 || rect.top > vh) return;
      const span = el.offsetHeight - vh;
      const p = clamp(-rect.top / (span || 1), 0, 1);
      this.atelierW.p = p;

      const frame = this.$refs.artFrame;
      const core = this.$refs.artCore;
      const ring = this.$refs.artRing;
      const gloss = this.$refs.artGloss;

      if (frame) {
        // ورود محو → شارپ
        const blur = Math.max(0, (0.16 - p) / 0.16) * 9;
        // خروج: کمی بزرگ و محو
        const scale = 1 + p * 0.1;
        const leaving = p > 0.86 ? (p - 0.86) / 0.14 : 0;
        const outBlur = leaving * 6;
        const outOp = 1 - leaving * 0.35;
        const py = (0.5 - p) * 26;
        frame.style.transform = `translate3d(0, ${py}px, 0) scale(${scale})`;
        frame.style.filter = `blur(${blur + outBlur}px)`;
        frame.style.opacity = outOp;
      }
      if (core) core.style.transform = `rotate(${-18 + p * 36}deg)`;
      if (ring) ring.style.transform = `translate(-50%, -50%) rotate(${p * 360}deg)`;
      if (gloss) {
        gloss.style.opacity = clamp(0.25 - Math.abs(p - 0.5) * 0.5, 0, 0.25);
      }
      const next = p >= 0.66 ? 2 : p >= 0.33 ? 1 : 0;
      if (next !== this.step) this.step = next;
      if (this.atelierDust) this.drawAtelierDust();
    },

    parallaxLayers() {
      const vh = window.innerHeight;
      const els = this.$el.querySelectorAll("[data-plx]");
      for (const el of els) {
        const r = el.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) continue;
        const speed = parseFloat(el.getAttribute("data-plx") || "0");
        const delta = (r.top + r.height / 2 - vh / 2) * speed;
        el.style.transform = `translate3d(0, ${delta.toFixed(1)}px, 0)`;
      }
    },

    teardown() {
      this.stopDust();
      if (this.atelierDust) window.cancelAnimationFrame(this.atelierDust.raf);
      window.removeEventListener("scroll", this.onScroll);
      window.removeEventListener("resize", this.onResize);
      if (this.io) this.io.disconnect();
      if (this.countIO) this.countIO.disconnect();
      if (this.pointerCleanup) this.pointerCleanup();
    },
  },
  created() {
    this.loadCourses();
    this.loadGallery();
    this.loadWorkshops();
  },
  mounted() {
    this.setupMotion();
  },
  beforeDestroy() {
    this.teardown();
  },
};
</script>

<style scoped>
/* ═══════════════════════════════════════════════════════════════
   پایه
═══════════════════════════════════════════════════════════════ */
.lp {
  --ink: #0d1512;
  --ink-2: #101d18;
  --pine: #1f4b43;
  --pine-deep: #14352c;
  --gold: #c9a96e;
  --gold-l: #e9d3a4;
  --gold-deep: #a07f45;
  --terra: #c96f4a;
  --terra-l: #e39b7a;
  --cream: #f7f1e6;
  --sand: #efe6d3;
  --paper: #fffdf8;
  --line: rgba(20, 26, 18, 0.1);
  --muted: #6f6a5c;
  --muted-d: rgba(247, 241, 230, 0.58);
  --font-display: "Amiri", "Vazirmatn", Tahoma, serif;
  font-family: "Vazirmatn", Tahoma, sans-serif;
  background: var(--cream);
  color: #1c1b17;
  overflow-x: hidden;
}
.fd { font-family: var(--font-display); }
.tl {
  color: var(--gold-deep);
  position: relative;
  white-space: nowrap;
}
.is-reduced *,
.is-reduced .rv { transition: none !important; animation: none !important; }
.is-reduced .rv { opacity: 1; transform: none; }

.container { max-width: 1280px; margin: 0 auto; padding: 0 24px; }
.lp-progress {
  position: fixed; top: 0; right: 0; left: 0; height: 3px;
  background: linear-gradient(90deg, var(--gold), var(--terra), var(--gold));
  transform: scaleX(0); transform-origin: 0 0; z-index: 300;
}

/* Reveal */
.rv { opacity: 0; transform: translateY(34px); transition: opacity 0.9s cubic-bezier(0.16, 1, 0.3, 1), transform 0.9s cubic-bezier(0.16, 1, 0.3, 1); transition-delay: var(--d, 0ms); will-change: opacity, transform; }
.rv.in { opacity: 1; transform: translateY(0); }

.lp-eyebrow {
  display: inline-flex; align-items: center; gap: 10px;
  font-size: 0.8rem; font-weight: 800; letter-spacing: 0.06em;
  color: var(--gold-deep); margin-bottom: 18px;
}
.lp-eyebrow::before { content: ""; width: 26px; height: 2px; background: var(--gold); }
.lp-eyebrow--light { color: var(--gold-l); }
.lp-eyebrow--light::before { background: var(--gold); }

.lp-title {
  font-size: clamp(1.9rem, 4.2vw, 3.1rem);
  font-weight: 900; line-height: 1.35; letter-spacing: -0.01em;
  color: #17150f; margin: 0 0 20px;
}
.lp-title--light { color: #fff; }
.lp-head { display: flex; justify-content: space-between; align-items: flex-end; gap: 28px; margin-bottom: 54px; }
.lp-head--center { flex-direction: column; align-items: center; text-align: center; }
.lp-head--center > p { color: var(--muted); max-width: 560px; margin: 0; }
.lp-head__note { color: var(--muted); max-width: 330px; margin: 0 0 12px; font-size: 0.95rem; line-height: 1.9; }

.lp-link { font-weight: 800; font-size: 0.92rem; color: var(--pine); transition: color 0.2s; margin-bottom: 8px; display: inline-block; }
.lp-link:hover { color: var(--gold-deep); }
.lp-link--light { color: var(--gold-l); }
.lp-link--light:hover { color: #fff; }

/* دکمه‌ها */
.lp-btn {
  display: inline-flex; align-items: center; gap: 10px; justify-content: center;
  padding: 15px 30px; border-radius: 14px; font-size: 0.98rem; font-weight: 800;
  border: none; text-decoration: none; cursor: pointer;
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s, background 0.3s, color 0.3s, border-color 0.3s;
}
.lp-btn--gold {
  background: linear-gradient(135deg, var(--gold-l), var(--gold) 55%, var(--gold-deep));
  color: #131005;
  box-shadow: 0 10px 30px rgba(201, 169, 110, 0.35);
}
.lp-btn--gold:hover { transform: translateY(-3px); box-shadow: 0 16px 44px rgba(201, 169, 110, 0.5); }
.lp-btn--ghost { background: transparent; border: 1.5px solid rgba(201, 169, 110, 0.45); color: var(--gold-l); }
.lp-btn--ghost:hover { border-color: var(--gold-l); background: rgba(201, 169, 110, 0.1); transform: translateY(-3px); }
.lp-btn--sm { padding: 12px 22px; font-size: 0.9rem; }
.lp-btn--lg { padding: 17px 40px; font-size: 1.05rem; }

/* ═══════════════════════════════════════════════════════════════
   HERO
═══════════════════════════════════════════════════════════════ */
.hero {
  position: relative;
  min-height: calc(100vh - 165px);
  display: flex; align-items: center;
  background:
    radial-gradient(130% 90% at 82% -10%, #1d4234 0%, transparent 55%),
    radial-gradient(110% 80% at 8% 110%, #0e241c 0%, transparent 60%),
    linear-gradient(150deg, #0d1713 0%, #0f241b 55%, #0a1410 100%);
  overflow: hidden;
  padding: 96px 0 84px;
}
.hero__bg { position: absolute; inset: 0; pointer-events: none; }
.hero__grain {
  position: absolute; inset: 0; opacity: 0.5;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.05'/%3E%3C/svg%3E");
  pointer-events: none;
}
.hero__orb { position: absolute; border-radius: 50%; filter: blur(90px); animation: lpFloat 16s ease-in-out infinite; }
.hero__orb--a { width: 480px; height: 480px; background: rgba(45, 106, 79, 0.45); top: -180px; left: -120px; }
.hero__orb--b { width: 420px; height: 420px; background: rgba(201, 169, 110, 0.22); bottom: -140px; right: -80px; animation-delay: 5s; }
.hero__orb--c { width: 300px; height: 300px; background: rgba(196, 111, 74, 0.16); top: 34%; right: 30%; animation-delay: 9s; }
@keyframes lpFloat { 0%, 100% { transform: translate(0, 0) scale(1); } 50% { transform: translate(28px, -34px) scale(1.06); } }

.hero__halo {
  position: absolute; width: 700px; height: 700px; border-radius: 50%;
  top: 18%; left: -190px;
  background: radial-gradient(circle, rgba(233, 211, 164, 0.12) 0%, transparent 62%);
}
.hero__lines { position: absolute; inset: 0; display: flex; justify-content: space-evenly; }
.hero__lines span { width: 1px; height: 100%; background: linear-gradient(to bottom, transparent, rgba(233, 211, 164, 0.05) 30%, rgba(233, 211, 164, 0.08) 60%, transparent); }
.hero__dust { position: absolute; inset: 0; pointer-events: none; z-index: 1; }

.hero__grid {
  position: relative; z-index: 2; width: 100%;
  display: grid; grid-template-columns: 1.05fr 0.95fr;
  gap: 40px; align-items: center;
}

/* ورود خط‌به‌خط */
.rise { opacity: 0; animation: lpRise 1s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
@keyframes lpRise { from { opacity: 0; transform: translateY(38px); } to { opacity: 1; transform: translateY(0); } }
.is-reduced .rise { animation: none; opacity: 1; }

.hero__eyebrow { display: inline-flex; align-items: center; gap: 12px; color: rgba(233, 211, 164, 0.85); font-size: 0.84rem; font-weight: 600; margin-bottom: 26px; }
.hero__eyebrow-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--gold); box-shadow: 0 0 0 5px rgba(201, 169, 110, 0.18); }

.hero__title { margin: 0 0 22px; }
.hero__line { display: block; font-size: clamp(3rem, 6.6vw, 5.6rem); font-weight: 900; line-height: 1.15; color: #fbf6ea; letter-spacing: -0.02em; }
.hero__line--sub { font-size: clamp(1.05rem, 2.2vw, 1.6rem); font-weight: 500; color: rgba(247, 241, 230, 0.62); margin-top: 12px; letter-spacing: 0; }
.hero__word-gold {
  font-weight: 700;
  background: linear-gradient(120deg, #f4e3ba 0%, var(--gold) 45%, #fff3d8 60%, var(--gold-deep) 100%);
  background-size: 220% auto;
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent; color: transparent;
  animation: lpShine 7s linear infinite;
}
@keyframes lpShine { to { background-position: 220% center; } }

.hero__sub { font-size: 1.04rem; line-height: 2.05; color: rgba(247, 241, 230, 0.66); max-width: 500px; margin: 0 0 34px; }
.hero__actions { display: flex; gap: 14px; margin-bottom: 42px; flex-wrap: wrap; }
.hero__facts { display: flex; align-items: center; gap: 22px; flex-wrap: wrap; }
.hero__fact { display: flex; flex-direction: column; }
.hero__fact b { font-size: 1.35rem; color: var(--gold-l); font-weight: 900; }
.hero__fact span { font-size: 0.78rem; color: rgba(247, 241, 230, 0.5); }
.hero__fact-sep { width: 1px; height: 36px; background: rgba(233, 211, 164, 0.22); }

/* تابلو */
.hero__stage { position: relative; display: flex; justify-content: center; perspective: 1200px; will-change: transform; }
.stage-frame {
  position: relative; width: min(420px, 86%); aspect-ratio: 4 / 5.1;
  padding: 16px;
  background: linear-gradient(160deg, #3a332a, #171410 70%);
  border-radius: 8px;
  box-shadow: 0 44px 90px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.08);
}
.stage-frame::before {
  content: ""; position: absolute; inset: 8px;
  border: 1px solid rgba(233, 211, 164, 0.22); border-radius: 4px; pointer-events: none;
}
.stage-frame::after {
  content: "یاشیل آرت"; position: absolute; bottom: 2px; left: 50%; transform: translateX(-50%);
  font-size: 0.55rem; letter-spacing: 0.3em; color: rgba(233, 211, 164, 0.5);
}
.stage-frame__inner { width: 100%; height: 100%; border-radius: 3px; overflow: hidden; position: relative; background: #0f1713; }
.stage-art { position: absolute; inset: 0; }
.stage-art__wash { position: absolute; border-radius: 50%; filter: blur(30px); }
.stage-art__wash--a { width: 74%; height: 44%; background: radial-gradient(circle, rgba(46, 107, 94, 0.85), transparent 70%); top: 8%; right: -12%; }
.stage-art__wash--b { width: 70%; height: 46%; background: radial-gradient(circle, rgba(196, 111, 74, 0.7), transparent 70%); bottom: 6%; left: -14%; }
.stage-art__wash--c { width: 55%; height: 32%; background: radial-gradient(circle, rgba(233, 211, 164, 0.5), transparent 70%); top: 44%; right: 26%; }
.stage-art__drawing { position: absolute; inset: 0; width: 100%; height: 100%; }
.stage-art__spin { animation: lpSpinSlow 46s linear infinite; transform-box: fill-box; transform-origin: center; }
@keyframes lpSpinSlow { to { transform: rotate(360deg); } }
.stage-art__gesso {
  position: absolute; inset: 0;
  background-image: radial-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1.4px);
  background-size: 9px 9px; opacity: 0.5; mix-blend-mode: overlay;
}
.stage-seal {
  position: absolute; left: -6px; bottom: 6%; width: 58px; height: 58px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, var(--terra), #9c4a2c); color: #fff;
  font-size: 1.6rem; font-weight: 700; box-shadow: 0 12px 30px rgba(196, 111, 74, 0.4);
  border: 3px solid #1a120c; z-index: 3;
}
.stage-chip {
  position: absolute; z-index: 4; padding: 8px 15px; border-radius: 40px;
  background: rgba(15, 23, 19, 0.92); border: 1px solid rgba(233, 211, 164, 0.3);
  color: var(--gold-l); font-size: 0.74rem; font-weight: 700;
  box-shadow: 0 14px 34px rgba(0, 0, 0, 0.45); backdrop-filter: blur(6px);
  animation: lpChipFloat 7s ease-in-out infinite;
}
.stage-chip--a { top: 9%; right: -14px; animation-delay: 0s; }
.stage-chip--b { bottom: 30%; left: -36px; animation-delay: 2.4s; }
.stage-chip--c { bottom: -12px; right: 10%; animation-delay: 4.6s; }
@keyframes lpChipFloat { 0%, 100% { transform: translateY(0) rotate(-1deg); } 50% { transform: translateY(-9px) rotate(1deg); } }

.hero__cue {
  position: absolute; bottom: 22px; left: 50%; transform: translateX(-50%);
  display: flex; flex-direction: column; align-items: center; gap: 8px; z-index: 3;
  color: rgba(247, 241, 230, 0.45); font-size: 0.7rem;
}
.hero__cue-line { width: 1px; height: 44px; background: linear-gradient(to bottom, var(--gold), transparent); animation: lpCue 2s ease-in-out infinite; }
@keyframes lpCue { 0%, 100% { opacity: 0.3; transform: scaleY(0.55); transform-origin: top; } 50% { opacity: 1; transform: scaleY(1); } }

/* ═══════════════════════════════════════════════════════════════
   MARQUEE
═══════════════════════════════════════════════════════════════ */
.marquee {
  background: linear-gradient(120deg, #0a1410, #122a20 45%, #0a1410);
  border-block: 1px solid rgba(201, 169, 110, 0.25);
  padding: 15px 0; overflow: hidden;
}
.marquee__track { display: flex; width: max-content; animation: lpMarquee 36s linear infinite; }
.marquee:hover .marquee__track { animation-play-state: paused; }
@keyframes lpMarquee { from { transform: translateX(0); } to { transform: translateX(-50%); } }
.marquee__set { display: flex; align-items: center; }
.marquee__item {
  display: inline-flex; align-items: center; gap: 16px; padding: 0 22px;
  font-size: 0.95rem; font-weight: 800; color: rgba(247, 241, 230, 0.78);
  white-space: nowrap;
}
.marquee__item svg { color: var(--gold); opacity: 0.7; }

/* ═══════════════════════════════════════════════════════════════
   MANIFESTO
═══════════════════════════════════════════════════════════════ */
.manifesto { padding: 130px 0 100px; background: var(--cream); position: relative; }
.manifesto::before {
  content: ""; position: absolute; top: 0; right: 0; width: 32vw; height: 32vw; max-width: 420px; max-height: 420px;
  background: radial-gradient(circle, rgba(201, 169, 110, 0.14), transparent 65%);
  pointer-events: none;
}
.manifesto__grid { display: grid; grid-template-columns: 1.05fr 0.95fr; gap: 70px; align-items: center; position: relative; }
.manifesto__lead { font-size: 1.06rem; line-height: 2.1; color: #4c463b; margin: 0 0 38px; }
.manifesto__lead b { color: var(--pine); }
.manifesto__points { display: flex; flex-direction: column; gap: 22px; }
.m-point { display: flex; gap: 18px; align-items: flex-start; }
.m-point__mark {
  flex-shrink: 0; width: 44px; height: 44px; border-radius: 13px;
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(150deg, var(--pine), var(--pine-deep));
  color: var(--gold-l); font-size: 0.78rem; font-weight: 800;
  box-shadow: 0 8px 18px rgba(31, 75, 67, 0.25);
}
.m-point h4 { font-size: 1.02rem; font-weight: 800; margin: 0 0 4px; }
.m-point p { font-size: 0.88rem; color: var(--muted); line-height: 1.8; margin: 0; }

.manifesto__visual { position: relative; }
.m-collage { position: relative; height: 500px; }
.m-collage__back {
  position: absolute; inset: 34px -20px -20px 34px;
  border: 2px dashed rgba(160, 127, 69, 0.4); border-radius: 20px;
}
.m-collage__tile {
  position: absolute; border-radius: 18px; overflow: hidden;
  display: flex; align-items: flex-end; padding: 20px;
  box-shadow: 0 30px 70px rgba(40, 30, 12, 0.22);
  border: 8px solid #fff;
  transform: rotate(var(--r, 0deg));
  transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.m-collage__tile:hover { transform: rotate(0deg) scale(1.03); z-index: 5; }
.m-collage__tile span { color: #fff; font-weight: 800; font-size: 0.9rem; text-shadow: 0 2px 14px rgba(0, 0, 0, 0.4); }
.m-collage__tile--1 {
  width: 62%; height: 62%; top: 4%; right: 0; --r: 2deg;
  background:
    radial-gradient(90% 60% at 30% 0%, rgba(46, 107, 94, 0.9), transparent 60%),
    radial-gradient(80% 70% at 80% 100%, rgba(196, 111, 74, 0.85), transparent 65%),
    linear-gradient(150deg, #2b5547, #12291f);
}
.m-collage__tile--1::after {
  content: ""; position: absolute; inset: 0;
  background:
    radial-gradient(circle at 70% 30%, rgba(233, 211, 164, 0.35) 0 8%, transparent 9%),
    radial-gradient(circle at 22% 66%, rgba(255, 255, 255, 0.18) 0 5%, transparent 6%),
    radial-gradient(circle at 58% 78%, rgba(233, 211, 164, 0.2) 0 6%, transparent 7%);
}
.m-collage__tile--2 {
  width: 55%; height: 48%; bottom: 0; left: 0; --r: -3deg; z-index: 2;
  background:
    radial-gradient(100% 90% at 60% 0%, rgba(233, 211, 164, 0.5), transparent 60%),
    linear-gradient(150deg, #b98d5e, #6f5336);
}
.m-collage__tile--2::after {
  content: ""; position: absolute; inset: 14%;
  border-radius: 50%;
  background: radial-gradient(circle, transparent 46%, rgba(58, 42, 23, 0.55) 47% 49%, transparent 50% 61%, rgba(58, 42, 23, 0.45) 62% 64%, transparent 65%);
}
.m-collage__stamp {
  position: absolute; top: 34%; left: 26%; z-index: 3;
  width: 86px; height: 86px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(140deg, var(--terra), #a04a2c);
  color: #fff7ea; font-size: 2.6rem; border: 6px solid var(--cream);
  box-shadow: 0 16px 40px rgba(196, 111, 74, 0.45);
  transform: rotate(-8deg);
}
.m-caption {
  margin-top: 26px; text-align: center; font-family: var(--font-display);
  font-size: 1.2rem; color: #7a7262;
}

/* شمارنده‌ها */
.counters {
  margin-top: 90px; display: grid; grid-template-columns: repeat(4, 1fr);
  border: 1px solid var(--line); border-radius: 22px; overflow: hidden;
  background: var(--paper);
  box-shadow: 0 18px 50px rgba(45, 33, 12, 0.08);
}
.counter { padding: 34px 20px; text-align: center; position: relative; }
.counter + .counter::before { content: ""; position: absolute; right: 0; top: 22%; height: 56%; width: 1px; background: var(--line); }
.counter__num { font-size: clamp(2rem, 3.6vw, 2.9rem); font-weight: 900; color: var(--pine); display: flex; align-items: baseline; justify-content: center; gap: 2px; font-variant-numeric: tabular-nums; }
.counter__num span { color: var(--gold-deep); }
.counter__label { font-size: 0.85rem; color: var(--muted); }

/* ═══════════════════════════════════════════════════════════════
   ATELIER — سکشن سینمایی
═══════════════════════════════════════════════════════════════ */
.atelier {
  position: relative;
  height: 360vh;
  background: linear-gradient(170deg, #0a1410 0%, #0e221a 40%, #10281e 60%, #0a1410 100%);
}
.atelier__words { position: absolute; inset: 0; pointer-events: none; overflow: hidden; }
.atelier__word {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  font-size: clamp(11rem, 30vw, 26rem); line-height: 1; font-weight: 700;
  color: transparent; -webkit-text-stroke: 1.5px rgba(233, 211, 164, 0.13);
  opacity: 0; transition: opacity 0.7s ease, -webkit-text-stroke-color 0.7s ease;
  user-select: none; white-space: nowrap;
}
.atelier__word.is-on { opacity: 1; -webkit-text-stroke-color: rgba(233, 211, 164, 0.26); }
.atelier__pin {
  position: sticky; top: 0; height: 100vh;
  display: grid; grid-template-columns: 1.02fr 0.98fr; gap: 44px; align-items: center;
  overflow: hidden; padding: 0 40px;
}
.atelier__bg { position: absolute; inset: 0; }
.atelier__orb { position: absolute; border-radius: 50%; filter: blur(100px); }
.atelier__orb--a { width: 560px; height: 560px; background: rgba(45, 106, 79, 0.3); top: -160px; right: -120px; }
.atelier__orb--b { width: 480px; height: 480px; background: rgba(201, 169, 110, 0.12); bottom: -180px; left: -100px; }

.atelier__art { position: relative; display: flex; align-items: center; justify-content: center; height: 78vh; }
.atelier__frame {
  position: relative; width: min(400px, 78%); aspect-ratio: 4 / 5.1;
  padding: 14px;
  background: linear-gradient(160deg, #33291d, #151008);
  border-radius: 6px; box-shadow: 0 60px 120px rgba(0, 0, 0, 0.55);
  will-change: transform, filter, opacity;
}
.atelier__frame::before { content: ""; position: absolute; inset: 7px; border: 1px solid rgba(233, 211, 164, 0.3); border-radius: 3px; pointer-events: none; z-index: 2; }
.atelier__core { display: block; width: 100%; height: 100%; border-radius: 2px; will-change: transform; }
.atelier__spinner { transform-box: fill-box; transform-origin: center; animation: lpSpinSlow 30s linear infinite; }
.atelier__gloss {
  position: absolute; inset: 0; z-index: 1; pointer-events: none; border-radius: 2px; opacity: 0;
  background: radial-gradient(90% 60% at 50% 50%, rgba(255, 248, 230, 0.16), transparent 70%);
  mix-blend-mode: screen;
}
.atelier__ring {
  position: absolute; top: 50%; left: 50%; width: 150%; max-width: 640px; aspect-ratio: 1;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  border: 1px dashed rgba(233, 211, 164, 0.35);
  will-change: transform; pointer-events: none;
}
.atelier__ring::after {
  content: ""; position: absolute; top: -5px; left: 50%; width: 10px; height: 10px; border-radius: 50%;
  background: var(--terra); box-shadow: 0 0 18px rgba(196, 111, 74, 0.8);
}
.atelier__dust { position: absolute; inset: 0; pointer-events: none; z-index: 5; }

.atelier__copy { position: relative; z-index: 3; max-width: 520px; }
.atelier__title { font-size: clamp(1.9rem, 3.6vw, 3rem); font-weight: 900; line-height: 1.4; color: #fff; margin: 0 0 14px; }
.atelier__intro { color: var(--muted-d); line-height: 2; font-size: 0.98rem; margin: 0 0 34px; }
.atelier__steps { display: flex; flex-direction: column; margin-bottom: 34px; }
.a-step { padding: 0; margin-bottom: 18px; transition: opacity 0.4s; }
.a-step:not(.is-active) p { opacity: 0; max-height: 0; margin: 0; overflow: hidden; transition: all 0.45s cubic-bezier(0.16, 1, 0.3, 1); }
.a-step.is-active p { opacity: 1; max-height: 160px; margin-top: 10px; transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.15s; }
.a-step__head { display: flex; align-items: center; gap: 14px; }
.a-step__num {
  width: 42px; height: 42px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  border: 1.5px solid rgba(233, 211, 164, 0.35); color: rgba(247, 241, 230, 0.6);
  font-size: 0.85rem; transition: all 0.35s;
}
.a-step.is-active .a-step__num {
  background: linear-gradient(140deg, var(--gold-l), var(--gold-deep)); color: #14100a;
  border-color: transparent; box-shadow: 0 0 0 6px rgba(201, 169, 110, 0.15);
}
.a-step h3 { font-size: 1.12rem; color: rgba(247, 241, 230, 0.55); transition: color 0.3s; margin: 0; }
.a-step.is-active h3 { color: #fff; }
.a-step__bar { flex: 1; height: 2px; background: rgba(233, 211, 164, 0.14); border-radius: 2px; overflow: hidden; }
.a-step__bar i { display: block; height: 100%; width: 0; background: linear-gradient(90deg, var(--gold), var(--terra)); transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
.a-step__bar i.full { width: 100%; }
.a-step p { color: var(--muted-d); font-size: 0.93rem; line-height: 1.95; padding-right: 56px; }

/* ═══════════════════════════════════════════════════════════════
   DISCIPLINES / BENTO
═══════════════════════════════════════════════════════════════ */
.disciplines { padding: 120px 0 130px; background: var(--paper); }
.bento { display: grid; grid-template-columns: repeat(4, 1fr); grid-auto-rows: 215px; gap: 18px; }
.bento__card {
  position: relative; overflow: hidden; border-radius: 22px; text-decoration: none; color: #fff;
  box-shadow: 0 14px 40px rgba(28, 22, 8, 0.1);
  transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.45s;
}
.bento__card--1 { grid-column: span 2; grid-row: span 2; }
.bento__card--4 { grid-column: span 1; grid-row: span 2; }
.bento__card--5 { grid-column: span 2; grid-row: span 1; }
.bento__bg {
  position: absolute; inset: 0; background: var(--grad, #1f4b43);
  transition: transform 0.8s cubic-bezier(0.16, 1, 0.3, 1), filter 0.8s;
}
.bento__card:hover { transform: translateY(-7px); box-shadow: 0 26px 60px rgba(24, 18, 6, 0.22); }
.bento__card:hover .bento__bg { transform: scale(1.1) rotate(0.4deg); filter: saturate(1.2); }
.bento__glyph {
  position: absolute; inset: 0; opacity: 0.5;
  background:
    radial-gradient(120% 90% at 110% -10%, rgba(255, 255, 255, 0.2), transparent 45%),
    radial-gradient(90% 70% at -10% 115%, rgba(0, 0, 0, 0.35), transparent 55%);
  transition: opacity 0.5s;
}
.bento__glyph::after {
  content: ""; position: absolute; top: -40%; left: -16%; width: 130%; height: 130%;
  background: repeating-conic-gradient(from 0deg at 78% 26%, transparent 0deg 12deg, rgba(255, 255, 255, 0.06) 12deg 14deg);
  border-radius: 50%;
}
.bento__icon {
  position: absolute; top: 22px; right: 22px; width: 46px; height: 46px;
  display: flex; align-items: center; justify-content: center;
  background: rgba(255, 255, 255, 0.16); border-radius: 14px; font-size: 1.3rem;
  backdrop-filter: blur(4px); border: 1px solid rgba(255, 255, 255, 0.2);
}
.bento__txt { position: absolute; bottom: 20px; right: 22px; }
.bento__txt h3 { font-size: 1.25rem; font-weight: 900; margin: 0 0 3px; }
.bento__txt span { font-size: 0.78rem; color: rgba(255, 255, 255, 0.72); }
.bento__card--1 .bento__txt h3 { font-size: 2rem; }
.bento__arrow {
  position: absolute; left: 18px; bottom: 18px; width: 38px; height: 38px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  background: rgba(255, 255, 255, 0.14); font-size: 1rem;
  transform: translateX(6px); opacity: 0; transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.bento__card:hover .bento__arrow { transform: translateX(0); opacity: 1; }

/* ═══════════════════════════════════════════════════════════════
   PATHWAY / LEVELS
═══════════════════════════════════════════════════════════════ */
.pathway { padding: 120px 0 110px; background: var(--cream); }
.levels { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; }
.level {
  position: relative; background: #fff; border: 1px solid var(--line); border-radius: 22px;
  padding: 42px 30px 30px; overflow: hidden;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s;
}
.level:hover { transform: translateY(-8px); box-shadow: 0 24px 60px rgba(42, 30, 8, 0.12); }
.level__stripe { position: absolute; top: 0; right: 0; left: 0; height: 5px; background: var(--tone); }
.level__index { position: absolute; top: 18px; left: 24px; font-size: 4.2rem; line-height: 1; color: rgba(20, 26, 18, 0.06); font-weight: 700; }
.level__icon { font-size: 2rem; margin-bottom: 18px; display: block; }
.level h3 { font-size: 1.18rem; font-weight: 900; margin: 0 0 10px; }
.level p { font-size: 0.9rem; color: var(--muted); line-height: 1.8; margin: 0 0 20px; }
.level ul { list-style: none; padding: 0; margin: 0 0 26px; display: flex; flex-direction: column; gap: 9px; }
.level li { position: relative; padding-right: 26px; font-size: 0.88rem; color: #4a443a; }
.level li::before { content: ""; position: absolute; right: 0; top: 9px; width: 7px; height: 7px; border-radius: 50%; background: var(--tone); }
.level__link { font-size: 0.9rem; font-weight: 800; color: var(--tone); }

/* ═══════════════════════════════════════════════════════════════
   FEATURED COURSES
═══════════════════════════════════════════════════════════════ */
.featured { padding: 0 0 120px; background: var(--cream); }
.courserow {
  display: flex; gap: 22px; overflow-x: auto; padding: 6px 30px 26px;
  scroll-snap-type: x proximity; scrollbar-width: none;
}
.courserow::-webkit-scrollbar { display: none; }
.ccard {
  flex: 0 0 290px; background: #fff; border-radius: 20px; overflow: hidden;
  text-decoration: none; color: inherit; border: 1px solid var(--line);
  scroll-snap-align: start;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s;
}
.ccard:hover { transform: translateY(-8px); box-shadow: 0 26px 60px rgba(34, 24, 6, 0.14); }
.ccard__thumb { position: relative; aspect-ratio: 16/10; overflow: hidden; }
.ccard__thumb img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
.ccard:hover .ccard__thumb img { transform: scale(1.07); }
.ccard__ph {
  width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
  color: rgba(31, 75, 67, 0.4); background: linear-gradient(150deg, #2b5547, #12291f);
}
.ccard__ph svg { width: 52px; color: rgba(233, 211, 164, 0.8); }
.ccard__level {
  position: absolute; top: 12px; right: 12px; padding: 5px 12px; border-radius: 30px;
  background: rgba(10, 16, 12, 0.72); color: var(--gold-l); font-size: 0.7rem; font-weight: 700;
  backdrop-filter: blur(6px);
}
.ccard__body { padding: 18px 20px 20px; }
.ccard__cat { font-size: 0.72rem; font-weight: 800; color: var(--pine); letter-spacing: 0.03em; }
.ccard__body h3 { font-size: 1.02rem; font-weight: 800; line-height: 1.55; margin: 6px 0 10px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.ccard__meta { display: flex; gap: 14px; font-size: 0.78rem; color: #98917f; margin-bottom: 14px; }
.ccard__foot { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--line); padding-top: 13px; }
.ccard__foot b { font-size: 0.9rem; font-weight: 900; }
.ccard__go { width: 32px; height: 32px; border-radius: 50%; background: var(--sand); display: flex; align-items: center; justify-content: center; transition: all 0.3s; }
.ccard:hover .ccard__go { background: var(--pine); color: #fff; }

/* ═══════════════════════════════════════════════════════════════
   WORKSHOPS
═══════════════════════════════════════════════════════════════ */
.workshops { padding: 130px 0; background: linear-gradient(170deg, #0a1410, #10281e 50%, #0a1410); }
.workshops__grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; }
.wcard {
  display: flex; background: rgba(21, 33, 26, 0.85); border: 1px solid rgba(233, 211, 164, 0.12);
  border-radius: 20px; overflow: hidden; text-decoration: none; color: inherit;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.4s;
}
.wcard:hover { transform: translateY(-6px); border-color: rgba(233, 211, 164, 0.35); }
.wcard__date {
  width: 104px; flex-shrink: 0; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(160deg, rgba(201, 169, 110, 0.16), transparent);
  border-left: 1px solid rgba(233, 211, 164, 0.12);
  font-size: 0.78rem; color: var(--gold-l); text-align: center; padding: 0 8px; line-height: 1.7;
}
.wcard__date b { display: block; font-size: 0.9rem; font-weight: 800; }
.wcard__content { padding: 24px; display: flex; flex-direction: column; }
.wcard__chips { display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }
.wcard__chips span { padding: 4px 11px; border-radius: 30px; background: rgba(233, 211, 164, 0.14); color: var(--gold-l); font-size: 0.7rem; font-weight: 700; }
.wcard__content h3 { font-size: 1.1rem; font-weight: 800; color: #fff; margin: 0 0 8px; }
.wcard__content p { font-size: 0.82rem; color: rgba(247, 241, 230, 0.45); margin: 0 0 18px; }
.wcard__foot { margin-top: auto; display: flex; justify-content: space-between; align-items: center; }
.wcard__foot b { color: var(--gold-l); font-weight: 900; font-size: 0.95rem; }
.wcard__cap { font-size: 0.7rem; color: rgba(247, 241, 230, 0.4); }

/* ═══════════════════════════════════════════════════════════════
   GALLERY
═══════════════════════════════════════════════════════════════ */
.gallery-sec { padding: 130px 0 120px; background: var(--paper); }
.gallery-sec__strip {
  display: grid; grid-template-columns: repeat(6, 1fr); grid-auto-rows: 230px; gap: 12px;
  padding: 0 30px; margin-top: 12px;
}
.gwork { position: relative; border-radius: 14px; overflow: hidden; text-decoration: none; display: block; }
.gwork--1 { grid-column: span 2; grid-row: span 2; }
.gwork--2 { grid-column: span 1; }
.gwork--3 { grid-column: span 1; grid-row: span 2; }
.gwork--4 { grid-column: span 2; }
.gwork--5 { grid-column: span 1; grid-row: span 2; }
.gwork img, .gwork__art { width: 100%; height: 100%; object-fit: cover; transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1); }
.gwork__art {
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px;
  background: var(--grad); color: rgba(255, 250, 240, 0.85);
}
.gwork__art svg { width: 34px; opacity: 0.9; }
.gwork__art b { font-size: clamp(2.4rem, 4vw, 4rem); color: rgba(255, 250, 240, 0.35); line-height: 1; }
.gwork:hover img, .gwork:hover .gwork__art { transform: scale(1.07); }
.gwork__overlay {
  position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: flex-end;
  padding: 18px; opacity: 0; transition: opacity 0.35s;
  background: linear-gradient(to top, rgba(8, 13, 10, 0.82), transparent 62%);
}
.gwork:hover .gwork__overlay { opacity: 1; }
.gwork__overlay h4 { color: #fff; font-size: 0.95rem; margin: 0 0 3px; font-weight: 800; }
.gwork__overlay span { color: rgba(255, 255, 255, 0.6); font-size: 0.76rem; }

/* ═══════════════════════════════════════════════════════════════
   VOICES
═══════════════════════════════════════════════════════════════ */
.voices { padding: 120px 0; background: var(--cream); }
.voices__grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; }
.voice {
  position: relative; margin: 0; background: #fff; border: 1px solid var(--line);
  border-radius: 22px; padding: 34px 30px;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s;
}
.voice:hover { transform: translateY(-6px); box-shadow: 0 22px 54px rgba(40, 30, 10, 0.1); }
.voice__mark { position: absolute; top: 10px; left: 26px; font-size: 5.6rem; line-height: 1; color: rgba(201, 169, 110, 0.22); }
.voice blockquote { margin: 0 0 24px; font-size: 0.95rem; line-height: 2; color: #4c463b; }
.voice figcaption { display: flex; align-items: center; gap: 12px; }
.voice__avatar { width: 46px; height: 46px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 800; flex-shrink: 0; }
.voice figcaption b { display: block; font-size: 0.92rem; }
.voice figcaption div span { font-size: 0.76rem; color: var(--muted); }

/* ═══════════════════════════════════════════════════════════════
   CTA پایانی
═══════════════════════════════════════════════════════════════ */
.final-cta { position: relative; padding: 150px 0 130px; background: linear-gradient(165deg, #0a1410, #123024 55%, #0a1410); overflow: hidden; text-align: center; }
.final-cta__bg { position: absolute; inset: 0; pointer-events: none; }
.final-cta__ring { position: absolute; border: 1px solid rgba(233, 211, 164, 0.16); border-radius: 50%; }
.final-cta__ring--a { width: 640px; height: 640px; left: 50%; top: 50%; transform: translate(-50%, -50%); border-style: dashed; animation: lpSpinSlow 80s linear infinite; }
.final-cta__ring--b { width: 880px; height: 880px; left: 50%; top: 50%; transform: translate(-50%, -50%); opacity: 0.5; }
.final-cta__ring--c { width: 330px; height: 330px; left: 12%; bottom: -140px; border-color: rgba(196, 111, 74, 0.3); }
.final-cta__inner { position: relative; z-index: 2; max-width: 800px; margin: 0 auto; }
.final-cta__kicker { display: inline-block; font-size: 1.5rem; color: var(--gold-l); margin-bottom: 10px; }
.final-cta__title { font-size: clamp(2rem, 5vw, 3.6rem); font-weight: 900; line-height: 1.4; color: #fff; margin: 0 0 18px; }
.final-cta__inner p { color: var(--muted-d); line-height: 2; margin: 0 auto 40px; max-width: 560px; }
.final-cta__actions { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
.final-cta__chips { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-top: 36px; }
.final-cta__chips span { font-size: 0.76rem; color: rgba(247, 241, 230, 0.55); border: 1px solid rgba(233, 211, 164, 0.2); border-radius: 30px; padding: 7px 16px; }
.final-cta__shop { display: inline-block; margin-top: 38px; color: rgba(247, 241, 230, 0.5); font-size: 0.9rem; transition: color 0.3s; }
.final-cta__shop b { color: var(--gold-l); }
.final-cta__shop:hover { color: #fff; }

/* ═══════════════════════════════════════════════════════════════
   RESPONSIVE
═══════════════════════════════════════════════════════════════ */
@media (max-width: 1080px) {
  .hero__grid { grid-template-columns: 1fr; gap: 64px; }
  .hero__stage { min-height: 0; }
  .stage-frame { width: min(340px, 80%); }
  .stage-chip--a { right: 4%; }
  .stage-chip--b { left: 2%; }
  .manifesto__grid { grid-template-columns: 1fr; gap: 90px; }
  .m-collage { height: 420px; }
  .atelier__pin { grid-template-columns: 1fr; gap: 6px; padding: 40px 24px; align-content: center; }
  .atelier__art { height: 38vh; }
  .atelier__frame { width: min(240px, 60%); }
  .atelier__copy { max-width: 100%; text-align: center; }
  .atelier__copy .lp-eyebrow { justify-content: center; }
  .a-step p { padding-right: 0; }
  .a-step { text-align: right; }
  .levels { grid-template-columns: 1fr; }
  .workshops__grid { grid-template-columns: 1fr; }
  .voices__grid { grid-template-columns: 1fr; }
}
@media (max-width: 860px) {
  .bento { grid-template-columns: repeat(2, 1fr); grid-auto-rows: 180px; }
  .bento__card--1 { grid-column: span 2; grid-row: span 2; }
  .bento__card--4 { grid-column: span 2; grid-row: span 1; }
  .bento__card--5 { grid-column: span 1; }
  .counters { grid-template-columns: repeat(2, 1fr); }
  .counter + .counter::before { display: none; }
  .counter { border-bottom: 1px solid var(--line); }
  .counter:nth-child(n + 3) { border-bottom: none; }
  .gallery-sec__strip { grid-template-columns: repeat(4, 1fr); grid-auto-rows: 170px; padding: 0 14px; }
  .gwork--1 { grid-column: span 2; grid-row: span 2; }
  .gwork--3, .gwork--5 { grid-row: span 1; }
  .lp-head { flex-direction: column; align-items: flex-start; gap: 6px; margin-bottom: 38px; }
  .lp-head--center { align-items: center; }
}
@media (max-width: 600px) {
  .hero { min-height: auto; padding: 64px 0 100px; }
  .hero__actions { flex-direction: column; }
  .lp-btn { width: 100%; }
  .hero__facts { gap: 14px; justify-content: space-between; }
  .stage-frame { width: min(300px, 92%); }
  .stage-chip--c { display: none; }
  .hero__cue { display: none; }
  .manifesto { padding: 84px 0 70px; }
  .bento { grid-template-columns: 1fr; grid-auto-rows: 190px; }
  .bento__card--1, .bento__card--4, .bento__card--5 { grid-column: span 1; grid-row: span 1; }
  .counters { grid-template-columns: 1fr 1fr; }
  .m-collage { height: 340px; }
  .m-collage__stamp { width: 64px; height: 64px; font-size: 1.9rem; }
  .atelier { height: 300vh; }
  .atelier__pin { gap: 20px; }
  .atelier__art { height: 30vh; }
  .atelier__frame { width: min(200px, 55%); }
  .atelier__ring { display: none; }
  .a-step.is-active p { max-height: 220px; }
  .ccard { flex-basis: 260px; }
  .gallery-sec__strip { grid-template-columns: repeat(2, 1fr); grid-auto-rows: 150px; }
  .gwork--1 { grid-column: span 2; grid-row: span 1; }
  .gwork--4 { grid-column: span 2; }
  .final-cta { padding: 110px 0; }
}
</style>
