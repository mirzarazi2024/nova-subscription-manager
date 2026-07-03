# راهنمای API موردنیاز پنل‌ها + تنظیم هدر هر پنل

## Hiddify (نسخه OpenAPI شما)
بر اساس سندی که دادی:
- Security header: `Hiddify-API-Key`
- endpoint پایه تست: `/{proxy_path}/api/v2/admin/user/`

### برای تست چه چیزی لازم داری؟
1. `base_url` پنل هیدیفای (مثلا `https://hiddify.example.com`)
2. `proxy_path` اگر پنل دارد (مثلا `admin`)
3. `API Key` ادمین
4. header درست:
   - `api_header_name = Hiddify-API-Key`
   - `api_prefix =` خالی

### تست دستی از سرور NSM (سرور جدا)
```bash
curl -i -H "Hiddify-API-Key: <API_KEY>" \
  "https://<HIDDIFY_HOST>/<PROXY_PATH>/api/v2/admin/user/"
```

---

## برای سایر پنل‌ها (قابل انتخاب در UI)
در NSM الان برای هر پنل می‌توانی تنظیم کنی:
- `api_header_name`
- `api_prefix` (مثل Bearer)
- `proxy_path`
- `test_endpoint`

### پیش‌فرض‌ها
- hiddify: `Hiddify-API-Key` + بدون prefix + `/api/v2/admin/user/`
- marzban: `Authorization` + `Bearer` + `/api/system`
- 3x-ui: `Authorization` + `Bearer` + `/panel/api/inbounds/list`
- xray: `Authorization` + `Bearer` + `/api/health`

> اگر نسخه پنلت متفاوت بود، همین فیلدها را در Dashboard > Panels تغییر بده.

---

## اجرای روی سرور مجزا از هیدیفای
کاملاً پشتیبانی می‌شود. فقط:
1. NSM باید route شبکه به Hiddify داشته باشد.
2. Firewall/SG اجازه بدهد.
3. SSL معتبر باشد (یا موقتاً verify_ssl=false برای تست داخلی).
4. Test Connection در Dashboard باید success بدهد.
