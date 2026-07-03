# Panel API Setup Wizard

برای اینکه NSM هنگام اجرا API پنل‌ها را از کاربر بگیرد، اسکریپت زیر اضافه شده:

```bash
make setup-panels
# یا
python3 infra/scripts/setup_panels.py
```

## رفتار اسکریپت
- API و URL پنل Hiddify را **الزامی** می‌گیرد.
- سپس به‌صورت اختیاری API پنل‌های آینده را می‌گیرد:
  - Marzban
  - 3x-ui
  - Xray
- خروجی را در فایل زیر ذخیره می‌کند:
  - `backend/config/panels.json`

## امنیت
- این فایل شامل API Key است.
- فایل در `.gitignore` قرار گرفته و نباید commit شود.

## فرمت فایل
نمونه در:
- `backend/config/panels.example.json`

## استفاده در Backend
Backend از `PANEL_CONFIG_PATH` (پیش‌فرض `config/panels.json`) می‌خواند.
در `HiddifyClient`، اگر پنل hiddify تعریف شده باشد، همان استفاده می‌شود.

## APIهای موردنیاز و نحوه دریافت
برای اینکه دقیقاً بدانی چه API لازم است و چطور توکن بگیری:
- `docs/hiddify-api-requirements.md`

## تست اتصال قبل از ذخیره
- از مسیر Dashboard > Panels بخش `Test Connection` را بزنید.
- برای Hiddify پاسخ موفق باید معمولاً 200 باشد.
