# 📦 فایل انتقال کامل — Trading Bot Project

**تاریخ:** 18 August 2026  
**وضعیت:** فاز طراحی + بهبود — قبل از اجرا  
**هدف:** انتقال کامل پروژه به هر هوش مصنوعی دیگر

---

## خلاصه اجرایی

### پروژه چیست؟
یک **ربات معامله‌گر هوشمند عمومی** که:
- از اینستاگرام، تلگرام، یوتیوب، کتاب و هر منبعی استراتژی یاد بگیرد
- به متاتریدر 5 هر بروکری وصل شود
- با مدیریت ریسک صحیح خودش ترید کند
- برای هر مبلغ سرمایه‌ای قابل پیاده‌سازی باشد
- ۲۴ ساعته کار کند (با فیلتر sessions)
- هر روز یاد بگیرد و بهبود یابد
- **ابزار عمومی** باشد — هر شخصی بتواند استفاده کند

### وضعیت فعلی
- ✅ تحقیق کامل شده
- ✅ Stack نهایی انتخاب شده
- ✅ ایرادات شناسایی و راه‌حل داده شده
- ✅ استراتژی‌ها ارزیابی شده
- ✅ مستندات ذخیره شده
- ⏳ **قبل از اجرا — منتظر تأیید کاربر**

### محدودیت‌های سخت‌افزاری
- CPU: Intel Core i5-2410M (2011) — بدون AVX2
- RAM: نامشخص (احتمالاً 4-8GB)
- GPU: ندارد
- OS: Windows 10+
- Runtime: Python 3.14 ✅, Node.js v24 ✅

---

## Stack نهایی

| Component | انتخاب | License | دلیل |
|---|---|---|---|
| **Agent** | Pydantic AI + LangGraph | MIT | Type-safe + stateful workflows |
| **Trading** | MetaTrader5 library | - | مستقیم به MT5 |
| **Backtest** | vectorbt | MIT | سریع, vectorized |
| **Data** | MT5 + yfinance + Dukascopy | Free | واقعاً رایگان |
| **Panel** | FastAPI + HTMX + Tailwind | MIT | بدون Node.js |
| **Browser** | Playwright + Browser Use | Apache/MIT | سریع + AI-native |
| **Instagram** | instagrapi | MIT | سریع‌ترین |
| **Telegram** | python-telegram-bot | GPL | بهترین |
| **DB** | SQLite + DuckDB + Markdown | Free | سبک + portable |
| **TA** | TA-Lib + pandas-ta | BSD/MIT | 200+ indicators |
| **AI** | Gemini/Mistral/Groq (free) + FinBERT (local) | Free | CPU-friendly |
| **Risk** | Custom deterministic | - | 100% deterministic |
| **Sentiment** | FinBERT (ProsusAI) | Apache | 110M params, CPU OK |

---

## استراتژی‌های اصلی (بک‌تست شده)

### ICT / SMC
- Win Rate: 61.2%
- Profit Factor: 2.17
- تعداد بک‌تست: 2,600 trades
- بهترین: Silver Bullet (55-65% WR, RR 1:3)

### Price Action
- Win Rate: 55-65%
- Profit Factor: 1.8-2.5

### Trend Following
- Win Rate: 40-55%
- Profit Factor: 1.8-2.5

---

## Risk Management — Smart Defaults

```python
# Default values (قابل تنظیم توسط کاربر)
RISK_PER_TRADE = 1.0      # درصد
RISK_PER_DAY = 3.0        # درصد
RISK_PER_WEEK = 6.0       # درصد
MAX_DRAWDOWN = 15.0       # درصد
MIN_RR_RATIO = 2.0        # Risk:Reward
MAX_OPEN_TRADES = 3       # تعداد
CONSENSUS_THRESHOLD = 0.65 # 65% اجماع لازم

# Kelly Criterion ( Half Kelly = safer )
def kelly_fraction(win_rate, reward_risk):
    return (win_rate - (1 - win_rate) / reward_risk) * 0.5
```

---

## منابع داده رایگان

| منبع | نوع | API |
|---|---|---|
| MT5 Built-in | Real-time + Historical | ✅ |
| Dukascopy | Historical tick/OHLCV | ✅ |
| yfinance | Stocks, Forex | ✅ |
| Forex Factory | Calendar | ❌ (web) |
| TradingView | Charts | ✅ (basic) |
| Alpha Vantage | Market Data | ✅ (25/day) |
| FRED | Macro | ✅ |

---

## فایل‌های پروژه

```
trading-bot/
├── docs/
│   ├── MASTER_SPECIFICATION_FA.md    ← سند مادر (ترجمه)
│   ├── IMPROVEMENT_REVIEW.md         ← تحلیل ایرادات Stack
│   ├── ARCHITECTURE.md               ← معماری کلی
│   ├── DECISIONS.md                  ← ۱۴ تصمیم فنی
│   ├── KNOWLEDGE_BASE.md             ← مفاهیم + بروکرها
│   ├── STRATEGIES.md                 ← استراتژی‌ها + بک‌تست
│   ├── TRANSFER_FILE.md              ← همین فایل
│   └── LESSONS.md                    ← درس‌آموخته‌ها
├── config/
│   └── settings.yaml                 ← تنظیمات
├── src/
│   ├── core/                         ← Orchestrator
│   ├── connector/                    ← MT5, Browser
│   ├── knowledge/                    ← Memory, DB
│   ├── risk/                         ← Risk Engine
│   ├── strategy/                     ← Strategy Engine
│   ├── learning/                     ← Instagram, Sources
│   ├── trading/                      ← Executor
│   ├── panel/                        ← Web UI
│   └── notifier/                     ← Telegram
├── main.py                           ← Entry point
├── requirements.txt                  ← Dependencies
└── README.md                         ← راهنما
```

---

## نقشه راه

| مرحله | کار | اولویت |
|---|---|---|
| ۱ | ساختار پروژه + Memory | 🔴 |
| ۲ | MT5 Connector | 🔴 |
| ۳ | Risk Engine | 🔴 |
| ۴ | Strategy Engine | 🟡 |
| ۵ | Instagram Scraper | 🟡 |
| ۶ | Backtester | 🟡 |
| ۷ | Trading Executor | 🟡 |
| ۸ | Panel | 🟢 |
| ۹ | Telegram | 🟢 |
| ۱۰ | News Monitor | 🟢 |
| ۱۱ | Consensus Engine | 🟢 |
| ۱۲ | Self-Evaluation | 🟢 |

---

## سؤالات باقیمانده

1. MT5 نصب و باز است؟
2. RAM چقدر است؟
3. حساب فرعی اینستاگرام؟
4. Bot تلگرام؟
5. حداکثر ریسک هر ترید؟ (فعلاً 1%)

---

## نحوه استفاده از این فایل

1. این فایل را به AI دیگر بدهید
2. AI جدید ابتدا docs/ را بخواند
3. سپس از مرحله ۱ شروع کند
4. هر تغییری در DECISIONS.md ثبت شود
5. هر درسی در LESSONS.md اضافه شود

**این فایل آخرین وضعیت پروژه را در تاریخ 18 August 2026 نشان می‌دهد.**
