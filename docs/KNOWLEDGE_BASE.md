# 🧠 Knowledge Base — Trading Bot

**هدف:** ذخیره دانش استخراج‌شده از منابع مختلف. قابل انتقال به AI دیگر.

---

## مفاهیم پایه

### Fair Value Gap (FVG)
- **تعریف:** فاصله بین candle high قبلی و candle low بعدی (در روند صعودی)
- **استفاده:** مناطق احتمالی برگشت قیمت
- **منبع:** pashacapital.ir (Instagram)
- **وضعیت:** verified
- **confidence:** high

### Liquidity Sweep
- **تعریف:** قیمت از سطح مهم رد می‌شود و برمی‌گردد (stop hunt)
- **استفاده:** تشخیص false breakout
- **منبع:** pashacapital.ir
- **وضعیت:** verified
- **confidence:** high

### Market Structure Break (MSB)
- **تعریف:** تغییر در الگوی high/low ها (trend reversal signal)
- **استفاده:** تشخیص تغییر روند
- **منبع:** pashacapital.ir
- **وضعیت:** verified
- **confidence:** high

### Order Blocks
- **تعریف:** مناطقی که institutional orders زیادی ثبت شده
- **استفاده:** مناطق حمایت/مقاومت قوی
- **منبع:** ICT (Inner Circle Trader)
- **وضعیت:** verified
- **confidence:** medium-high

### Prop Firm Passing Strategy
- **تعریف:** استراتژی‌های خاص برای پاس کردن چالش prop firm
- **استفاده:** مدیریت ریسک ویژه prop firm
- **منبع:** pashacapital.ir
- **وضعیت:** verified
- **confidence:** medium

---

## جلسات بازار

### Asian Session
- **ساعت:** 00:00 - 08:00 UTC
- **نقدینگی:** کم
- **بهترین برای:** scalping در ranges
- **نمادها:** USDJPY, AUDUSD, NZDUSD

### European Session (London)
- **ساعت:** 08:00 - 17:00 UTC
- **نقدینگی:** بالا
- **بهترین برای:** trend following, breakout
- **نمادها:** EURUSD, GBPUSD, EURGBP

### American Session (New York)
- **ساعت:** 13:00 - 22:00 UTC
- **نقدینگی:** بالا
- **بهترین برای:** continuation, reversal
- **نمادها:** EURUSD, USDJPY, XAUUSD

### Overlap (London + New York)
- **ساعت:** 13:00 - 17:00 UTC
- **نقدینگی:** خیلی بالا
- **بهترین برای:** همه استراتژی‌ها
- **هشدار:** بیشترین نوسان

---

## مدیریت ریسک

### قوانین پایه
- حداکثر ریسک هر ترید: 1-2% سرمایه
- حداکثر ریسک روزانه: 5% سرمایه
- حداکثر ریسک هفتگی: 10% سرمایه
- Risk:Reward minimum: 1:2
- Drawdown limit: 15% (توقف معاملات)

### Position Sizing Formula
```
Lot Size = (Account Balance × Risk%) / (Stop Loss in pips × Pip Value)
```

### Session Rules
- Asian: حداکثر 0.5% risk per trade
- European: حداکثر 1% risk per trade
- American: حداکثر 1% risk per trade
- Overlap: حداکثر 0.5% risk per trade (نوسان بالا)

---

## بروکرها

### Aron Markets (فعلی)
- **نوع:** STP/ECN
- **حداقل سپرده:** $100
- **حداکثر اهرم:** 1:500
- **ابزارها:** فارکس, فلزات, شاخص‌ها
- **Spread:** ~1.2 pips
- **Commission:** $0
- **Swap Free:** ✅ بله
- **Bonus:** ✅ موجود
- **ساعت معاملات فارکس:** Mon-Fri 00:05-23:55

---

## منابع اخبار

### Primary Sources
- **Twitter/X:** حساب‌های تحلیلی معتبر
- **RSS Feeds:** CNBC, Reuters, Bloomberg (free feeds)
- **Economic Calendar:** investing.com (free)
- **Forex Factory:** forexfactory.com (free)

### Secondary Sources
- **Instagram:** pashacapital.ir (آموزشی)
- **Telegram:** کانال‌های تحلیلی
- **YouTube:** تحلیل‌های لایو

---

## درس‌آموخته‌ها

### L001: هر ادعایی قبل از ذخیره باید اعتبارسنجی شود
- **تاریخ:** 2026-08-18
- **منبع:** Master Specification
- **اهمیت:** high

### L002: Instagram scrapers خطر ban دارند
- **تاریخ:** 2026-08-18
- **منبع:** تحقیق فنی
- **اهمیت:** high
- **راه‌حل:** حساب فرعی + human-in-the-loop

### L003: CPU قدیمی Local LLM را غیرعملی می‌کند
- **تاریخ:** 2026-08-18
- **منبع:** تحقیق فنی
- **اهمیت:** high
- **راه‌حل:** APIهای رایگان + FinBERT local

### L004: QuantConnect Lean MT5 ندارد
- **تاریخ:** 2026-08-18
- **منبع:** تحقیق فنی
- **اهمیت:** high
- **راه‌حل:** MetaTrader5 library مستقیم

### L005: OpenBB دیگر MIT نیست
- **تاریخ:** 2026-08-18
- **منبع:** تحقیق فنی + Reddit
- **اهمیت:** medium
- **راه‌حل:** yfinance + Alpha Vantage

### L006: Win Rate بالا ≠ سوددهی بالا
- **تاریخ:** 2026-08-18
- **منبع:** تحقیق استراتژی‌ها
- **اهمیت:** high
- **教训:** Trend Following با WR 40% می‌تواند سودده‌تر از Scalping با WR 70% باشد (اگر RR بالا باشد)

### L007: Kelly Criterion نصف بهتر است
- **تاریخ:** 2026-08-18
- **منبع:** تحقیق risk management
- **اهمیت:** high
- **教训:** Full Kelly ریسک خیلی بالایی دارد. Half Kelly امن‌تر و تقریباً به همان اندازه سودده.

### L008: Dukascopy بهترین منبع داده رایگان فارکس
- **تاریخ:** 2026-08-18
- **منبع:** تحقیق data sources
- **اهمیت:** medium
- **教训:** Historical tick data رایگان با کیفیت بالا

### L009: Consensus بین چند استراتژی بهتر از یک استراتژی است
- **تاریخ:** 2026-08-18
- **منبع:** تحقیق multi-strategy
- **اهمیت:** high
- **教训:** ۳ استراتژی با WR 55-65% → consensus 65% → سیگنال قوی‌تر
