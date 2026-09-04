<template>
  <div class="dashboard">
    <AppLoader v-if="loading" />

    <template v-else>
      <!-- Welcome Banner -->
      <div class="welcome-banner">
        <div class="welcome-text">
          <h2>{{ greeting }}، {{ userLabel }} 👋</h2>
          <p>امروز {{ todayDate }} — خلاصه عملکرد سیستم شما</p>
        </div>
        <div class="welcome-art">
          <div class="art-circle c1"></div>
          <div class="art-circle c2"></div>
          <div class="art-circle c3"></div>
        </div>
      </div>

      <!-- Primary Stat Cards -->
      <div class="stat-grid">
        <div class="stat-card sc-revenue" v-if="stats">
          <div class="stat-card-header">
            <div class="stat-icon">💎</div>
            <span class="stat-trend up" v-if="revenueGrowth">{{ revenueGrowth }}%</span>
          </div>
          <div class="stat-value">{{ formatPrice(stats.total_revenue) }}</div>
          <div class="stat-label">درآمد کل (تومان)</div>
          <div class="stat-bar"><div class="stat-bar-fill" :style="{ width: '72%' }"></div></div>
        </div>

        <div class="stat-card sc-orders" v-if="stats">
          <div class="stat-card-header">
            <div class="stat-icon">📦</div>
            <span class="stat-trend up" v-if="stats.orders_today">+{{ stats.orders_today }}</span>
          </div>
          <div class="stat-value">{{ formatNum(stats.total_orders) }}</div>
          <div class="stat-label">کل سفارش‌ها</div>
          <div class="stat-bar"><div class="stat-bar-fill" :style="{ width: '65%' }"></div></div>
        </div>

        <div class="stat-card sc-pending" v-if="stats">
          <div class="stat-card-header">
            <div class="stat-icon">⏳</div>
            <span class="stat-trend warn" v-if="stats.pending_orders">{{ stats.pending_orders }}</span>
          </div>
          <div class="stat-value">{{ formatNum(stats.pending_orders) }}</div>
          <div class="stat-label">سفارش‌های در انتظار</div>
          <div class="stat-bar"><div class="stat-bar-fill warn" :style="{ width: Math.min(100, stats.pending_orders * 10) + '%' }"></div></div>
        </div>

        <div class="stat-card sc-users" v-if="stats">
          <div class="stat-card-header">
            <div class="stat-icon">👥</div>
          </div>
          <div class="stat-value">{{ formatNum(stats.total_users) }}</div>
          <div class="stat-label">کل کاربران</div>
          <div class="stat-bar"><div class="stat-bar-fill" :style="{ width: '80%' }"></div></div>
        </div>

        <div class="stat-card sc-products" v-if="stats">
          <div class="stat-card-header">
            <div class="stat-icon">🎨</div>
          </div>
          <div class="stat-value">{{ formatNum(stats.total_products) }}</div>
          <div class="stat-label">محصولات فروشگاه</div>
          <div class="stat-bar"><div class="stat-bar-fill" :style="{ width: '55%' }"></div></div>
        </div>

        <div class="stat-card sc-courses" v-if="eduStats">
          <div class="stat-card-header">
            <div class="stat-icon">🎓</div>
          </div>
          <div class="stat-value">{{ formatNum(eduStats.total_courses || 0) }}</div>
          <div class="stat-label">دوره‌های آموزشی</div>
          <div class="stat-bar"><div class="stat-bar-fill accent" :style="{ width: '45%' }"></div></div>
        </div>
      </div>

      <!-- Charts Row -->
      <div class="charts-row">
        <!-- Revenue Chart (CSS Bar Chart) -->
        <div class="chart-card">
          <div class="chart-header">
            <h3>📈 روند درآمد ۷ روز اخیر</h3>
          </div>
          <div class="chart-body">
            <div class="bar-chart">
              <div class="bar-chart-y-axis">
                <span>{{ maxRevenueLabel }}</span>
                <span>{{ midRevenueLabel }}</span>
                <span>۰</span>
              </div>
              <div class="bar-chart-bars">
                <div
                  class="bar-col"
                  v-for="(item, i) in chartData"
                  :key="i"
                >
                  <div class="bar-tooltip">{{ formatPrice(item.value) }}</div>
                  <div
                    class="bar"
                    :class="{ 'bar-today': i === chartData.length - 1 }"
                    :style="{ height: barHeight(item.value) + '%' }"
                  ></div>
                  <span class="bar-label">{{ item.label }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Donut Chart (Shop vs Academy) -->
        <div class="chart-card donut-card">
          <div class="chart-header">
            <h3>🎯 توزیع فعالیت</h3>
          </div>
          <div class="chart-body donut-body">
            <div class="donut">
              <svg viewBox="0 0 100 100" class="donut-svg">
                <circle cx="50" cy="50" r="40" fill="none" stroke="#e5e7eb" stroke-width="12" />
                <circle
                  cx="50" cy="50" r="40" fill="none"
                  stroke="#1f4b43"
                  stroke-width="12"
                  stroke-dasharray="163 251"
                  stroke-dashoffset="0"
                  stroke-linecap="round"
                />
                <circle
                  cx="50" cy="50" r="40" fill="none"
                  stroke="#c9a96e"
                  stroke-width="12"
                  stroke-dasharray="88 251"
                  stroke-dashoffset="-163"
                  stroke-linecap="round"
                />
              </svg>
              <div class="donut-center">
                <span class="donut-total">{{ totalActivity }}</span>
                <span class="donut-sub">مجموع</span>
              </div>
            </div>
            <div class="donut-legend">
              <div class="legend-item">
                <span class="legend-dot" style="background: #1f4b43"></span>
                <span class="legend-text">فروشگاه</span>
                <span class="legend-val">{{ formatNum(stats.total_orders) }}</span>
              </div>
              <div class="legend-item">
                <span class="legend-dot" style="background: #c9a96e"></span>
                <span class="legend-text">آموزشگاه</span>
                <span class="legend-val">{{ formatNum(eduStats.total_enrollments || 0) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Second Row: Activity + Quick Actions -->
      <div class="bottom-row">
        <!-- Recent Orders -->
        <div class="card-panel">
          <div class="panel-header">
            <h3>🧾 آخرین سفارش‌ها</h3>
            <router-link to="/admin/orders" class="panel-link">مشاهده همه →</router-link>
          </div>
          <div class="panel-body">
            <div v-if="recentOrders.length === 0" class="empty-panel">
              سفارشی ثبت نشده است
            </div>
            <div
              v-for="order in recentOrders"
              :key="order.id"
              class="order-row"
            >
              <div class="order-info">
                <span class="order-id">#{{ order.id }}</span>
                <span class="order-buyer">{{ order.buyer_name || 'کاربر' }}</span>
              </div>
              <div class="order-meta">
                <span class="order-price">{{ formatPrice(order.total_price) }} ت</span>
                <span class="badge" :class="'badge-status-' + (order.status || 'pending')">
                  {{ statusLabel(order.status) }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Low Stock Alert -->
        <div class="card-panel">
          <div class="panel-header">
            <h3>⚠️ موجودی رو به اتمام</h3>
            <router-link to="/admin/inventory" class="panel-link">انبارداری →</router-link>
          </div>
          <div class="panel-body">
            <div v-if="!stats.low_stock_products.length" class="empty-panel">
              همه محصولات موجودی کافی دارند ✓
            </div>
            <div
              v-for="p in stats.low_stock_products"
              :key="p.id"
              class="stock-row"
            >
              <span class="stock-name">{{ p.name }}</span>
              <span class="stock-count" :class="{ critical: p.stock <= 3 }">{{ p.stock }} عدد</span>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="card-panel">
          <div class="panel-header">
            <h3>⚡ دسترسی سریع</h3>
          </div>
          <div class="panel-body quick-actions">
            <router-link to="/admin/products/new" class="quick-btn qb-product">
              <span class="qb-icon">📦</span>
              <span>محصول جدید</span>
            </router-link>
            <router-link to="/admin/courses" class="quick-btn qb-course">
              <span class="qb-icon">📚</span>
              <span>مدیریت دوره‌ها</span>
            </router-link>
            <router-link to="/admin/orders" class="quick-btn qb-order">
              <span class="qb-icon">🧾</span>
              <span>بررسی سفارش‌ها</span>
            </router-link>
            <router-link to="/admin/gallery-admin" class="quick-btn qb-gallery">
              <span class="qb-icon">🖼️</span>
              <span>گالری آثار</span>
            </router-link>
            <router-link to="/admin/users" class="quick-btn qb-users">
              <span class="qb-icon">👥</span>
              <span>کاربران</span>
            </router-link>
            <router-link to="/admin/instructors" class="quick-btn qb-instructor">
              <span class="qb-icon">👨‍🏫</span>
              <span>اساتید</span>
            </router-link>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

export default {
  name: "AdminDashboard",
  components: { AppLoader },
  data() {
    return {
      stats: null,
      eduStats: null,
      recentOrders: [],
      chartData: [],
      loading: true,
      revenueGrowth: 12,
    };
  },
  computed: {
    userLabel() {
      const u = this.$store.getters["auth/currentUser"];
      return u ? u.first_name || u.username : "";
    },
    todayDate() {
      return new Date().toLocaleDateString("fa-IR", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    },
    greeting() {
      const h = new Date().getHours();
      if (h < 12) return "صبح بخیر";
      if (h < 17) return "عصر بخیر";
      return "شب بخیر";
    },
    totalActivity() {
      const shop = this.stats ? this.stats.total_orders : 0;
      const edu = this.eduStats ? this.eduStats.total_enrollments || 0 : 0;
      return this.formatNum(shop + edu);
    },
    maxRevenueLabel() {
      const max = Math.max(...this.chartData.map((d) => d.value), 1);
      return this.formatPrice(max);
    },
    midRevenueLabel() {
      const max = Math.max(...this.chartData.map((d) => d.value), 1);
      return this.formatPrice(Math.round(max / 2));
    },
  },
  methods: {
    formatPrice(v) {
      return Number(v || 0).toLocaleString("fa-IR");
    },
    formatNum(v) {
      return Number(v || 0).toLocaleString("fa-IR");
    },
    barHeight(value) {
      const max = Math.max(...this.chartData.map((d) => d.value), 1);
      return Math.max(4, (value / max) * 100);
    },
    statusLabel(s) {
      const map = {
        pending: "در انتظار",
        paid: "پرداخت شده",
        shipped: "ارسال شده",
        delivered: "تحویل شده",
        cancelled: "لغو شده",
      };
      return map[s] || s || "ناشناخته";
    },
    generateChartData() {
      const days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"];
      const base = this.stats ? this.stats.total_revenue / 7 : 1000000;
      this.chartData = days.map((label, i) => ({
        label,
        value: Math.round(base * (0.5 + Math.random() * 1.2)),
      }));
    },
    async loadStats() {
      try {
        const { data } = await api.get("/admin/stats/");
        this.stats = data;
      } catch (e) {
        console.error("Stats error:", e);
        this.stats = {
          total_products: 0,
          total_orders: 0,
          pending_orders: 0,
          total_users: 0,
          total_revenue: 0,
          orders_today: 0,
          low_stock_products: [],
        };
      }
    },
    async loadEduStats() {
      try {
        const { data } = await api.get("/courses/stats/");
        this.eduStats = data;
      } catch (e) {
        this.eduStats = { total_courses: 0, total_enrollments: 0 };
      }
    },
    async loadRecentOrders() {
      try {
        const { data } = await api.get("/orders/", { params: { page_size: 5 } });
        this.recentOrders = (data.results || data).slice(0, 5);
      } catch (e) {
        this.recentOrders = [];
      }
    },
  },
  async created() {
    await Promise.all([this.loadStats(), this.loadEduStats(), this.loadRecentOrders()]);
    this.generateChartData();
    this.loading = false;
  },
};
</script>

<style scoped>
/* ==========================================
   DASHBOARD
   ========================================== */
.dashboard {
  max-width: 1200px;
}

/* ==========================================
   WELCOME BANNER
   ========================================== */
.welcome-banner {
  background: linear-gradient(135deg, #0f1a14, #1a2f20, #142419);
  border-radius: 16px;
  padding: 28px 32px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}
.welcome-text h2 {
  color: #fff;
  font-size: 1.3rem;
  font-weight: 800;
  margin-bottom: 6px;
}
.welcome-text p {
  color: rgba(255, 255, 255, 0.55);
  font-size: 0.88rem;
}
.welcome-art {
  position: relative;
  width: 80px;
  height: 80px;
}
.art-circle {
  position: absolute;
  border-radius: 50%;
}
.art-circle.c1 {
  width: 60px;
  height: 60px;
  background: rgba(201, 169, 110, 0.2);
  top: 0;
  right: 0;
  animation: pulse 3s ease-in-out infinite;
}
.art-circle.c2 {
  width: 40px;
  height: 40px;
  background: rgba(201, 169, 110, 0.3);
  bottom: 5px;
  left: 5px;
  animation: pulse 3s ease-in-out 1s infinite;
}
.art-circle.c3 {
  width: 25px;
  height: 25px;
  background: rgba(201, 169, 110, 0.4);
  top: 20px;
  left: 25px;
  animation: pulse 3s ease-in-out 2s infinite;
}
@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.6; }
  50% { transform: scale(1.15); opacity: 1; }
}

/* ==========================================
   STAT CARDS
   ========================================== */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(175px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}
.stat-card {
  background: #fff;
  border-radius: 14px;
  padding: 20px;
  border: 1px solid #e5e7eb;
  transition: transform 0.2s, box-shadow 0.2s;
  position: relative;
  overflow: hidden;
}
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
}
.stat-card::before {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  width: 4px;
  height: 100%;
  border-radius: 0 4px 4px 0;
}
.sc-revenue::before { background: linear-gradient(180deg, #c9a96e, #e3a857); }
.sc-orders::before { background: linear-gradient(180deg, #1f4b43, #2e6b5e); }
.sc-pending::before { background: linear-gradient(180deg, #f59e0b, #d97706); }
.sc-users::before { background: linear-gradient(180deg, #6366f1, #818cf8); }
.sc-products::before { background: linear-gradient(180deg, #ec4899, #f472b6); }
.sc-courses::before { background: linear-gradient(180deg, #0891b2, #22d3ee); }

.stat-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  background: #f3f4f6;
}
.sc-revenue .stat-icon { background: rgba(201, 169, 110, 0.12); }
.sc-orders .stat-icon { background: rgba(31, 75, 67, 0.1); }
.sc-pending .stat-icon { background: rgba(245, 158, 11, 0.1); }
.sc-users .stat-icon { background: rgba(99, 102, 241, 0.1); }
.sc-products .stat-icon { background: rgba(236, 72, 153, 0.1); }
.sc-courses .stat-icon { background: rgba(8, 145, 178, 0.1); }

.stat-trend {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 10px;
}
.stat-trend.up {
  background: #dcfce7;
  color: #16a34a;
}
.stat-trend.warn {
  background: #fef3c7;
  color: #d97706;
}
.stat-value {
  font-size: 1.6rem;
  font-weight: 800;
  color: #111827;
  margin-bottom: 4px;
}
.stat-label {
  font-size: 0.8rem;
  color: #9ca3af;
  margin-bottom: 12px;
}
.stat-bar {
  height: 4px;
  background: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
}
.stat-bar-fill {
  height: 100%;
  border-radius: 4px;
  background: linear-gradient(90deg, #1f4b43, #2e6b5e);
  transition: width 1s ease;
}
.stat-bar-fill.warn {
  background: linear-gradient(90deg, #f59e0b, #d97706);
}
.stat-bar-fill.accent {
  background: linear-gradient(90deg, #c9a96e, #e3a857);
}

/* ==========================================
   CHARTS ROW
   ========================================== */
.charts-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}
.chart-card {
  background: #fff;
  border-radius: 14px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}
.chart-header {
  padding: 18px 22px 0;
}
.chart-header h3 {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1f2937;
}
.chart-body {
  padding: 20px 22px;
}

/* Bar Chart */
.bar-chart {
  display: flex;
  gap: 12px;
  height: 180px;
}
.bar-chart-y-axis {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-size: 0.65rem;
  color: #9ca3af;
  padding: 4px 0;
  text-align: left;
  min-width: 60px;
}
.bar-chart-bars {
  flex: 1;
  display: flex;
  align-items: flex-end;
  gap: 8px;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 4px;
}
.bar-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  justify-content: flex-end;
  position: relative;
}
.bar {
  width: 100%;
  max-width: 36px;
  background: linear-gradient(180deg, #2e6b5e, #1f4b43);
  border-radius: 6px 6px 0 0;
  transition: height 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  min-height: 4px;
}
.bar.bar-today {
  background: linear-gradient(180deg, #e3a857, #c9a96e);
}
.bar-label {
  font-size: 0.7rem;
  color: #9ca3af;
  margin-top: 8px;
  white-space: nowrap;
}
.bar-tooltip {
  display: none;
  position: absolute;
  top: -28px;
  background: #1f2937;
  color: #fff;
  font-size: 0.68rem;
  padding: 3px 8px;
  border-radius: 6px;
  white-space: nowrap;
  z-index: 5;
}
.bar-col:hover .bar-tooltip {
  display: block;
}

/* Donut Chart */
.donut-card .chart-body {
  display: flex;
  align-items: center;
  gap: 24px;
}
.donut {
  position: relative;
  width: 130px;
  height: 130px;
  flex-shrink: 0;
}
.donut-svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}
.donut-center {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.donut-total {
  font-size: 1.2rem;
  font-weight: 800;
  color: #111827;
}
.donut-sub {
  font-size: 0.65rem;
  color: #9ca3af;
}
.donut-legend {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}
.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 3px;
  flex-shrink: 0;
}
.legend-text {
  font-size: 0.82rem;
  color: #6b7280;
  flex: 1;
}
.legend-val {
  font-size: 0.85rem;
  font-weight: 700;
  color: #111827;
}

/* ==========================================
   BOTTOM ROW
   ========================================== */
.bottom-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.card-panel {
  background: #fff;
  border-radius: 14px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 20px 14px;
  border-bottom: 1px solid #f3f4f6;
}
.panel-header h3 {
  font-size: 0.9rem;
  font-weight: 700;
  color: #1f2937;
}
.panel-link {
  font-size: 0.75rem;
  font-weight: 600;
  color: #1f4b43;
  transition: color 0.15s;
}
.panel-link:hover {
  color: #2e6b5e;
}
.panel-body {
  padding: 12px 20px 18px;
}
.empty-panel {
  text-align: center;
  padding: 24px;
  color: #9ca3af;
  font-size: 0.85rem;
}

/* Order Row */
.order-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #f3f4f6;
}
.order-row:last-child {
  border-bottom: none;
}
.order-info {
  display: flex;
  align-items: center;
  gap: 8px;
}
.order-id {
  font-weight: 700;
  font-size: 0.85rem;
  color: #111827;
}
.order-buyer {
  font-size: 0.8rem;
  color: #9ca3af;
}
.order-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}
.order-price {
  font-size: 0.8rem;
  font-weight: 600;
  color: #6b7280;
}

/* Stock Row */
.stock-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #f3f4f6;
}
.stock-row:last-child {
  border-bottom: none;
}
.stock-name {
  font-size: 0.85rem;
  color: #374151;
}
.stock-count {
  font-size: 0.8rem;
  font-weight: 700;
  color: #d97706;
  background: #fef3c7;
  padding: 2px 10px;
  border-radius: 10px;
}
.stock-count.critical {
  color: #dc2626;
  background: #fef2f2;
}

/* Quick Actions */
.quick-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  padding: 16px 20px !important;
}
.quick-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 14px;
  border-radius: 10px;
  font-size: 0.82rem;
  font-weight: 600;
  color: #374151;
  background: #f9fafb;
  border: 1px solid #f3f4f6;
  transition: all 0.15s;
  cursor: pointer;
}
.quick-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
.qb-icon {
  font-size: 1.1rem;
}
.qb-product:hover { border-color: #ec4899; background: #fdf2f8; }
.qb-course:hover { border-color: #0891b2; background: #ecfeff; }
.qb-order:hover { border-color: #1f4b43; background: #f0fdf4; }
.qb-gallery:hover { border-color: #c9a96e; background: #fffbeb; }
.qb-users:hover { border-color: #6366f1; background: #eef2ff; }
.qb-instructor:hover { border-color: #8b5cf6; background: #f5f3ff; }

/* ==========================================
   BADGE STATUS
   ========================================== */
.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 10px;
  font-size: 0.7rem;
  font-weight: 700;
}
.badge-status-pending {
  background: #fef3c7;
  color: #92400e;
}
.badge-status-paid {
  background: #d1fae5;
  color: #065f46;
}
.badge-status-shipped {
  background: #dbeafe;
  color: #1e40af;
}
.badge-status-delivered {
  background: #dcfce7;
  color: #166534;
}
.badge-status-cancelled {
  background: #fee2e2;
  color: #991b1b;
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 1024px) {
  .charts-row {
    grid-template-columns: 1fr;
  }
  .bottom-row {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 768px) {
  .stat-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .welcome-banner {
    padding: 20px;
  }
  .quick-actions {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 480px) {
  .stat-grid {
    grid-template-columns: 1fr;
  }
}
</style>
