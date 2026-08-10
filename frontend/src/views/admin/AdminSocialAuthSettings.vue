<template>
  <div class="admin-social-settings">
    <h1>ورود اجتماعی</h1>

    <AppLoader v-if="loading" />

    <div v-else class="settings-grid">
      <!-- Google -->
      <div class="card settings-card">
        <div class="toggle-row">
          <div>
            <h3>ورود با گوگل</h3>
            <p class="text-muted">مشتری با یک کلیک روی حساب گوگل خودش وارد می‌شود.</p>
          </div>
          <label class="toggle-switch">
            <input type="checkbox" v-model="form.google_enabled" />
            <span class="toggle-switch__slider"></span>
          </label>
        </div>

        <template v-if="form.google_enabled">
          <div class="field">
            <label>Google Client ID</label>
            <input v-model="form.google_client_id" type="text" placeholder="xxxxx.apps.googleusercontent.com" />
            <p class="text-muted field-hint">
              از Google Cloud Console → APIs &amp; Services → Credentials بسازید.
              Authorized JavaScript origins باید دقیقاً آدرس همین سایت باشد.
            </p>
          </div>
        </template>
      </div>

      <!-- Telegram -->
      <div class="card settings-card">
        <div class="toggle-row">
          <div>
            <h3>ورود با تلگرام</h3>
            <p class="text-muted">مشتری با ویجت رسمی ورود تلگرام، حساب خودش را تایید می‌کند.</p>
          </div>
          <label class="toggle-switch">
            <input type="checkbox" v-model="form.telegram_enabled" />
            <span class="toggle-switch__slider"></span>
          </label>
        </div>

        <template v-if="form.telegram_enabled">
          <div class="field">
            <label>یوزرنیم ربات (بدون @)</label>
            <input v-model="form.telegram_bot_username" type="text" placeholder="YashilArtBot" />
          </div>
          <div class="field">
            <label>توکن ربات</label>
            <input v-model="form.telegram_bot_token" type="text" placeholder="123456:ABC-DEF..." />
            <p class="text-muted field-hint">
              یک ربات با @BotFather بسازید، توکن را اینجا بگذارید، و با دستور
              <code>/setdomain</code> دامنه همین سایت را برای ربات ثبت کنید.
            </p>
          </div>
        </template>
      </div>

      <!-- SMS OTP -->
      <div class="card settings-card">
        <div class="toggle-row">
          <div>
            <h3>ورود با کد پیامکی</h3>
            <p class="text-muted">مشتری شماره موبایل می‌دهد و با کد یک‌بارمصرف پیامکی وارد می‌شود.</p>
          </div>
          <label class="toggle-switch">
            <input type="checkbox" v-model="form.sms_otp_enabled" />
            <span class="toggle-switch__slider"></span>
          </label>
        </div>

        <template v-if="form.sms_otp_enabled">
          <div class="field">
            <label>سرویس‌دهنده پیامک</label>
            <select v-model="form.sms_provider">
              <option value="kavenegar">کاوه‌نگار</option>
            </select>
          </div>
          <div class="field">
            <label>کلید API</label>
            <input v-model="form.sms_api_key" type="text" />
          </div>
          <div class="field">
            <label>شماره خط ارسال (اختیاری)</label>
            <input v-model="form.sms_sender_line" type="text" />
          </div>
        </template>
      </div>
    </div>

    <button class="btn btn-primary save-btn" :disabled="saving" @click="save">
      {{ saving ? "در حال ذخیره..." : "ذخیره تنظیمات" }}
    </button>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

export default {
  name: "AdminSocialAuthSettings",
  components: { AppLoader },
  data() {
    return {
      loading: true,
      saving: false,
      form: {
        google_enabled: false, google_client_id: "",
        telegram_enabled: false, telegram_bot_username: "", telegram_bot_token: "",
        sms_otp_enabled: false, sms_provider: "kavenegar", sms_api_key: "", sms_sender_line: "",
      },
    };
  },
  async created() {
    try {
      const { data } = await api.get("/admin/social-auth-settings/");
      this.form = data;
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async save() {
      this.saving = true;
      try {
        const { data } = await api.patch("/admin/social-auth-settings/", this.form);
        this.form = data;
        this.$store.dispatch("notify", { message: "تنظیمات ذخیره شد." });
      } catch (e) {
        this.$store.dispatch("notify", { message: "ذخیره تنظیمات ناموفق بود.", type: "error" });
      } finally {
        this.saving = false;
      }
    },
  },
};
</script>

<style scoped>
.admin-social-settings h1 {
  font-size: 1.4rem;
  margin-bottom: 20px;
}
.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}
.settings-card {
  padding: 22px;
}
.toggle-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}
.toggle-row h3 {
  font-size: 0.95rem;
  margin-bottom: 6px;
}
.toggle-row p {
  font-size: 0.8rem;
  line-height: 1.6;
}
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 46px;
  height: 26px;
  flex-shrink: 0;
}
.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.toggle-switch__slider {
  position: absolute;
  cursor: pointer;
  inset: 0;
  background: var(--color-border);
  border-radius: 30px;
  transition: 0.2s;
}
.toggle-switch__slider::before {
  content: "";
  position: absolute;
  width: 20px;
  height: 20px;
  right: 3px;
  top: 3px;
  background: #fff;
  border-radius: 50%;
  transition: 0.2s;
}
.toggle-switch input:checked + .toggle-switch__slider {
  background: var(--color-primary);
}
.toggle-switch input:checked + .toggle-switch__slider::before {
  transform: translateX(-20px);
}
.field-hint {
  font-size: 0.76rem;
  margin-top: 4px;
  line-height: 1.6;
}
.field-hint code {
  background: var(--color-sand);
  padding: 1px 5px;
  border-radius: 4px;
}
.save-btn {
  display: block;
}
</style>