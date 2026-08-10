<template>
  <div v-if="hasAnyMethod" class="social-auth">
    <div class="social-auth__divider"><span>یا</span></div>

    <div v-if="settings.google_enabled" class="social-auth__block">
      <div ref="googleBtn" class="google-btn-container"></div>
    </div>

    <div v-if="settings.telegram_enabled" class="social-auth__block">
      <div ref="telegramContainer" class="telegram-widget-container"></div>
    </div>

    <div v-if="settings.sms_otp_enabled" class="social-auth__block">
      <button v-if="!smsOpen" type="button" class="btn btn-outline btn-block" @click="smsOpen = true">
        📱 ورود با کد پیامکی
      </button>

      <div v-else class="sms-panel">
        <div v-if="smsError" class="field-error">{{ smsError }}</div>

        <template v-if="!codeSent">
          <div class="field">
            <label>شماره موبایل</label>
            <input v-model="phoneNumber" type="tel" placeholder="09123456789" />
          </div>
          <button class="btn btn-primary btn-block" :disabled="sendingCode" @click="requestCode">
            {{ sendingCode ? "در حال ارسال..." : "ارسال کد" }}
          </button>
        </template>

        <template v-else>
          <div class="field">
            <label>کد ارسال‌شده به {{ phoneNumber }}</label>
            <input v-model="code" type="text" maxlength="6" placeholder="------" />
          </div>
          <button class="btn btn-primary btn-block" :disabled="verifying" @click="verifyCode">
            {{ verifying ? "در حال بررسی..." : "تایید و ورود" }}
          </button>
          <button type="button" class="link-btn" @click="codeSent = false">شماره را عوض کن</button>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "SocialAuthPanel",
  data() {
    return {
      settings: {
        google_enabled: false, google_client_id: "",
        telegram_enabled: false, telegram_bot_username: "",
        sms_otp_enabled: false,
      },
      smsOpen: false,
      phoneNumber: "",
      code: "",
      codeSent: false,
      sendingCode: false,
      verifying: false,
      smsError: "",
    };
  },
  computed: {
    hasAnyMethod() {
      return this.settings.google_enabled || this.settings.telegram_enabled || this.settings.sms_otp_enabled;
    },
  },
  async created() {
    try {
      const { data } = await api.get("/auth/social/settings/");
      this.settings = data;
    } catch (e) {
      // اگر این درخواست شکست بخورد، فقط بخش ورود اجتماعی نمایش داده نمی‌شود
    }
  },
  mounted() {
    this.$nextTick(() => {
      if (this.settings.google_enabled) this.mountGoogleButton();
    });
  },
  watch: {
    "settings.google_enabled"(enabled) {
      if (enabled) this.$nextTick(this.mountGoogleButton);
    },
    "settings.telegram_enabled"(enabled) {
      if (enabled) this.$nextTick(this.mountTelegramWidget);
    },
  },
  methods: {
    async mountGoogleButton() {
      if (!this.settings.google_client_id) return;
      await this.loadScript("https://accounts.google.com/gsi/client");
      if (!window.google || !window.google.accounts) return;
      window.google.accounts.id.initialize({
        client_id: this.settings.google_client_id,
        callback: this.handleGoogleCredential,
      });
      window.google.accounts.id.renderButton(this.$refs.googleBtn, {
        theme: "outline", size: "large", text: "continue_with", locale: "fa", width: 280,
      });
    },
    mountTelegramWidget() {
      if (!this.settings.telegram_bot_username || !this.$refs.telegramContainer) return;
      window.onTelegramAuth = (user) => this.handleTelegramAuth(user);
      const script = document.createElement("script");
      script.src = "https://telegram.org/js/telegram-widget.js?22";
      script.setAttribute("data-telegram-login", this.settings.telegram_bot_username);
      script.setAttribute("data-size", "large");
      script.setAttribute("data-onauth", "onTelegramAuth(user)");
      script.setAttribute("data-request-access", "write");
      script.async = true;
      this.$refs.telegramContainer.innerHTML = "";
      this.$refs.telegramContainer.appendChild(script);
    },
    loadScript(src) {
      return new Promise((resolve, reject) => {
        if (document.querySelector(`script[src="${src}"]`)) return resolve();
        const script = document.createElement("script");
        script.src = src;
        script.async = true;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
      });
    },
    async handleGoogleCredential(response) {
      try {
        const { data } = await api.post("/auth/social/google/", { credential: response.credential });
        await this.completeLogin(data);
      } catch (e) {
        this.$store.dispatch("notify", { message: "ورود با گوگل ناموفق بود.", type: "error" });
      }
    },
    async handleTelegramAuth(user) {
      try {
        const { data } = await api.post("/auth/social/telegram/", user);
        await this.completeLogin(data);
      } catch (e) {
        this.$store.dispatch("notify", { message: "ورود با تلگرام ناموفق بود.", type: "error" });
      }
    },
    async requestCode() {
      this.smsError = "";
      this.sendingCode = true;
      try {
        await api.post("/auth/social/sms/request/", { phone_number: this.phoneNumber });
        this.codeSent = true;
        this.$store.dispatch("notify", { message: "کد تایید ارسال شد." });
      } catch (e) {
        this.smsError = (e.response && e.response.data && (e.response.data.detail || e.response.data.phone_number)) || "ارسال کد ناموفق بود.";
      } finally {
        this.sendingCode = false;
      }
    },
    async verifyCode() {
      this.smsError = "";
      this.verifying = true;
      try {
        const { data } = await api.post("/auth/social/sms/verify/", {
          phone_number: this.phoneNumber, code: this.code,
        });
        await this.completeLogin(data);
      } catch (e) {
        this.smsError = (e.response && e.response.data && e.response.data.detail) || "کد نادرست است.";
      } finally {
        this.verifying = false;
      }
    },
    async completeLogin(data) {
      await this.$store.dispatch("auth/applySocialLogin", data);
      this.$store.dispatch("notify", { message: "خوش آمدید!" });
      const redirect = this.$route.query.redirect || "/";
      this.$router.push(redirect);
    },
  },
};
</script>

<style scoped>
.social-auth {
  margin-top: 22px;
}
.social-auth__divider {
  display: flex;
  align-items: center;
  text-align: center;
  color: var(--color-text-muted);
  font-size: 0.78rem;
  margin-bottom: 18px;
}
.social-auth__divider::before,
.social-auth__divider::after {
  content: "";
  flex: 1;
  height: 1px;
  background: var(--color-border);
}
.social-auth__divider span {
  padding: 0 10px;
}
.social-auth__block {
  margin-bottom: 12px;
  display: flex;
  justify-content: center;
}
.google-btn-container,
.telegram-widget-container {
  width: 100%;
  display: flex;
  justify-content: center;
}
.sms-panel {
  width: 100%;
}
.link-btn {
  display: block;
  width: 100%;
  text-align: center;
  background: none;
  border: none;
  color: var(--color-primary);
  font-size: 0.8rem;
  margin-top: 10px;
  font-family: inherit;
}
</style>