<template>
  <div class="student-certs">
    <h2>🏆 گواهینامه‌های من</h2>
    <div v-if="certificates.length" class="certs-grid">
      <div v-for="cert in certificates" :key="cert.id" class="cert-card">
        <div class="cert-icon">🎓</div>
        <h3>{{ cert.course_title }}</h3>
        <p class="cert-date">تاریخ صدور: {{ formatDate(cert.issued_at) }}</p>
        <p class="cert-code">کد: {{ cert.certificate_code }}</p>
        <button class="btn-download" @click="downloadCert(cert)">📥 دانلود</button>
      </div>
    </div>
    <p v-else class="empty">هنوز گواهینامه‌ای دریافت نکرده‌اید.</p>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "StudentCertificates",
  data() {
    return { certificates: [] };
  },
  methods: {
    formatDate(d) {
      if (!d) return "—";
      return new Date(d).toLocaleDateString("fa-IR");
    },
    async downloadCert(cert) {
      try {
        const { data } = await api.get(`/certificates/${cert.id}/download/`, { responseType: "blob" });
        const url = URL.createObjectURL(data);
        const a = document.createElement("a");
        a.href = url;
        a.download = `certificate-${cert.certificate_code}.pdf`;
        a.click();
        URL.revokeObjectURL(url);
      } catch { /* silent */ }
    },
  },
  async mounted() {
    try {
      const { data } = await api.get("/certificates/my-certificates/");
      this.certificates = Array.isArray(data) ? data : [];
    } catch { /* silent */ }
  },
};
</script>

<style scoped>
.student-certs h2 { margin-bottom: 16px; color: #1a2f1e; }
.certs-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 18px; }
.cert-card {
  background: #fff; border-radius: 12px; padding: 24px; text-align: center;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06); border-top: 3px solid #c9a96e;
}
.cert-icon { font-size: 2.5rem; margin-bottom: 12px; }
.cert-card h3 { margin: 0 0 8px; font-size: 0.95rem; }
.cert-date, .cert-code { font-size: 0.82rem; color: #888; margin: 4px 0; }
.btn-download {
  margin-top: 12px; padding: 8px 20px; background: #c9a96e; color: #fff;
  border: none; border-radius: 8px; font-family: inherit; font-size: 0.82rem; cursor: pointer;
}
.btn-download:hover { background: #b8944f; }
.empty { color: #999; text-align: center; padding: 40px; }
</style>
