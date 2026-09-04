<template>
  <div class="instructor-profile">
    <h2>👤 پروفایل استاد</h2>
    <div class="profile-card">
      <form @submit.prevent="saveProfile">
        <div class="form-group">
          <label>نام</label>
          <input v-model="form.first_name" type="text" placeholder="نام" />
        </div>
        <div class="form-group">
          <label>نام خانوادگی</label>
          <input v-model="form.last_name" type="text" placeholder="نام خانوادگی" />
        </div>
        <div class="form-group">
          <label>شماره موبایل</label>
          <input v-model="form.phone_number" type="text" placeholder="شماره موبایل" />
        </div>
        <div class="form-group">
          <label>رزومه</label>
          <textarea v-model="form.bio" placeholder="سوابق تدریس و هنری..." rows="4"></textarea>
        </div>
        <button type="submit" class="btn-save" :disabled="saving">
          {{ saving ? 'در حال ذخیره...' : 'ذخیره تغییرات' }}
        </button>
        <span v-if="saved" class="save-ok">✅ ذخیره شد</span>
      </form>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
import { mapGetters } from "vuex";

export default {
  name: "InstructorProfile",
  data() {
    return {
      form: { first_name: "", last_name: "", phone_number: "", bio: "" },
      saving: false,
      saved: false,
    };
  },
  computed: {
    ...mapGetters("auth", ["currentUser"]),
  },
  methods: {
    async saveProfile() {
      this.saving = true;
      this.saved = false;
      try {
        await api.patch("/auth/me/", this.form);
        await this.$store.dispatch("auth/fetchProfile");
        this.saved = true;
        setTimeout(() => (this.saved = false), 2000);
      } catch { /* silent */ }
      this.saving = false;
    },
  },
  mounted() {
    if (this.currentUser) {
      this.form = {
        first_name: this.currentUser.first_name || "",
        last_name: this.currentUser.last_name || "",
        phone_number: this.currentUser.phone_number || "",
        bio: this.currentUser.bio || "",
      };
    }
  },
};
</script>

<style scoped>
.instructor-profile h2 { margin-bottom: 16px; color: #1a2f1e; }
.profile-card {
  background: #fff; border-radius: 12px; padding: 28px; max-width: 500px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 0.82rem; font-weight: 700; color: #555; margin-bottom: 6px; }
.form-group input, .form-group textarea {
  width: 100%; padding: 10px 14px; border: 1px solid #ddd; border-radius: 8px;
  font-family: inherit; font-size: 0.88rem; box-sizing: border-box;
}
.form-group textarea { resize: vertical; }
.btn-save {
  padding: 10px 24px; background: #4a2c7a; color: #fff; border: none;
  border-radius: 8px; font-family: inherit; font-size: 0.88rem; cursor: pointer;
}
.btn-save:disabled { opacity: 0.5; }
.save-ok { margin-right: 12px; color: #27ae60; font-size: 0.85rem; }
</style>
