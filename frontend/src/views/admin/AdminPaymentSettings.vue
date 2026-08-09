<template>
  <div class="admin-payment-settings">
    <h1>تنظیمات پرداخت</h1>

    <AppLoader v-if="loading" />

    <div v-else class="settings-grid">
      <!-- Card transfer -->
      <div class="card settings-card">
        <div class="toggle-row">
          <div>
            <h3>کارت‌به‌کارت</h3>
            <p class="text-muted">مشتری مبلغ را واریز می‌کند و تصویر رسید را برای تایید شما آپلود می‌کند.</p>
          </div>
          <label class="toggle-switch">
            <input type="checkbox" v-model="form.card_transfer_enabled" />
            <span class="toggle-switch__slider"></span>
          </label>
        </div>

        <template v-if="form.card_transfer_enabled">
          <div class="field">
            <label>شماره کارت</label>
            <input v-model="form.card_number" type="text" placeholder="6037-9977-XXXX-XXXX" />
          </div>
          <div class="field">
            <label>نام صاحب حساب</label>
            <input v-model="form.card_holder_name" type="text" />
          </div>
          <div class="field">
            <label>نام بانک (اختیاری)</label>
            <input v-model="form.bank_name" type="text" />
          </div>
          <div class="field">
            <label>توضیح اضافه برای مشتری (اختیاری)</label>
            <textarea v-model="form.card_transfer_instructions" rows="2"></textarea>
          </div>
        </template>
      </div>

      <!-- Online gateway -->
      <div class="card settings-card">
        <div class="toggle-row">
          <div>
            <h3>درگاه آنلاین (زرین‌پال)</h3>
            <p class="text-muted">مشتری مستقیم از درگاه پرداخت آنلاین می‌کند و بلافاصله سفارش پرداخت‌شده ثبت می‌شود.</p>
          </div>
          <label class="toggle-switch">
            <input type="checkbox" v-model="form.online_gateway_enabled" />
            <span class="toggle-switch__slider"></span>
          </label>
        </div>

        <template v-if="form.online_gateway_enabled">
          <div class="field">
            <label>Merchant ID زرین‌پال</label>
            <input v-model="form.zarinpal_merchant_id" type="text" placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" />
            <p class="text-muted field-hint">از پنل زرین‌پال خودتان (merchant.zarinpal.com) بگیرید.</p>
          </div>
          <label class="checkbox-label">
            <input v-model="form.zarinpal_sandbox" type="checkbox" />
            حالت آزمایشی (Sandbox) — تا وقتی Merchant ID واقعی و تاییدشده ندارید روشن نگه دارید
          </label>
        </template>
      </div>
    </div>

    <button class="btn btn-primary save-btn" :disabled="saving" @click="save">
      {{ saving ? "در حال ذخیره..." : "ذخیره تنظیمات پرداخت" }}
    </button>
  </div>
</template>

<script>
import api from "@/services/api";
import AppLoader from "@/components/AppLoader.vue";

export default {
  name: "AdminPaymentSettings",
  components: { AppLoader },
  data() {
    return {
      loading: true,
      saving: false,
      form: {
        card_transfer_enabled: false, card_number: "", card_holder_name: "", bank_name: "",
        card_transfer_instructions: "", online_gateway_enabled: false,
        zarinpal_merchant_id: "", zarinpal_sandbox: true,
      },
    };
  },
  async created() {
    try {
      const { data } = await api.get("/admin/payments-settings/");
      this.form = data;
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async save() {
      this.saving = true;
      try {
        const { data } = await api.patch("/admin/payments-settings/", this.form);
        this.form = data;
        this.$store.dispatch("notify", { message: "تنظیمات پرداخت ذخیره شد." });
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
.admin-payment-settings h1 {
  font-size: 1.4rem;
  margin-bottom: 20px;
}
.settings-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
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
}
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.82rem;
  line-height: 1.6;
}
.save-btn {
  display: block;
}

@media (max-width: 900px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }
}
</style>