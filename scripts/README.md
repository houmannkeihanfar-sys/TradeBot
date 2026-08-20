# Scripts Index
فهرست اسکریپت‌های قابل استفاده مجدد

## نحوه استفاده
```bash
cd <your_project_path>\trading-bot
venv\Scripts\python.exe scripts/<script_name> <args>
```

## اسکریپت‌ها

| # | اسکریپت | کاربرد | دستور |
|---|---------|--------|-------|
| 01 | `01_video_analyzer.py` | تحلیل ویدیو و استخراج استراتژی | `python scripts/01_video_analyzer.py <video_path>` |
| 02 | `02_telegram_reader.py` | خواندن پست تلگرام | `python scripts/02_telegram_reader.py <channel> <post_id>` |
| 03 | `03_mt5_connector.py` | اتصال و مدیریت MT5 | `python scripts/03_mt5_connector.py <command>` |
| 04 | `04_ea_generator.py` | تولید Expert Advisor | `python scripts/04_ea_generator.py <config.json>` |
| 05 | `05_risk_engine.py` | محاسبات ریسک | `python scripts/05_risk_engine.py <command>` |
| 06 | `06_web_reader.py` | خواندن محتوای وب | `python scripts/06_web_reader.py <url>` |

## دستورات MT5 (اسکریپت 03)

```bash
# اتصال و ذخیره اطلاعات حساب
python scripts/03_mt5_connector.py connect

# دریافت اطلاعات حساب
python scripts/03_mt5_connector.py account

# پوزیشن‌های باز
python scripts/03_mt5_connector.py positions

# داده‌های قیمت
python scripts/03_mt5_connector.py rates XAUUSD H1 100

# خرید
python scripts/03_mt5_connector.py buy XAUUSD 0.01

# فروش
python scripts/03_mt5_connector.py sell XAUUSD 0.01

# بستن پوزیشن
python scripts/03_mt5_connector.py close 12345678
```

## دستورات Risk Engine (اسکریپت 05)

```bash
# محاسبه حجم پوزیشن
python scripts/05_risk_engine.py calculate 2650.00 2640.00 2670.00 10000

# بررسی دراوداون
python scripts/05_risk_engine.py check_drawdown 9500 10000

# محاسبه Kelly Criterion
python scripts/05_risk_engine.py kelly 60 200 100
```

## خواندن وب (اسکریپت 06)

```bash
# خواندن یک صفحه
python scripts/06_web_reader.py https://example.com/article

# خواندن مقاله ترید
python scripts/06_web_reader.py https://www.investopedia.com/strategy
```

## نکات امنیتی
- رمز عبور ذخیره **نمی‌شود**
- اطلاعات حساس فقط در memory
- فایل‌های نتایج در `data/` ذخیره می‌شوند
- هر بار اجرا، نتایج قبلی را بازنویسی می‌کند
