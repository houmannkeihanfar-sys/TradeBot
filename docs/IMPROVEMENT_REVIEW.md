# 📋 بررسی بهبود — تحلیل ایرادات و پیشنهادات Stack

**تاریخ:** 18 August 2026  
**وضعیت:** فاز بهبود — هیچ نصب یا تغییری انجام نشده  
**هدف:** شناسایی مشکلات Stack پیشنهادی و ارائه راه‌حل بهتر

---

## ۱. خلاصه الزامات کاربر (آنچه واقعاً می‌خواهد)

کاربر یک سیستم **عمومی و قابل انتقال** می‌خواهد که:

1. از اینستاگرام و منابع مختلف استراتژی یاد بگیرد
2. اگر در ویدیو لینک تلگرام یا منبع دیگری هست، برود و محتوا را بگیرد
3. هر مفهوم ناشناخته را مثل یک مبتدی بخواند و یاد بگیرد
4. به هر بروکری وصل شود، قوانینش را بخواند، شرایط حساب و بونوس را بررسی کند
5. با مدیریت ریسک صحیح روی متاتریدر 5 ترید کند
6. برای هر مبلغ سرمایه‌ای قابل پیاده‌سازی باشد
7. پنل محلی داشته باشد (اطلاعات حساب، پوزیشن‌ها، تاریخچه)
8. نوتیفیکیشن تلگرام داشته باشد
9. ۲۴ ساعته کار کند (با قابلیت فیلتر ساعات پر نقدینگی)
10. هر روز یاد بگیرد و بهبود یابد
11. چند استراتژی همزمان → اجماع → سیگنال نهایی با درصد اعتماد
12. **ابزار عمومی** باشد — هر شخصی بتواند روی هر بازاری استفاده کند
13. **کمترین توکن** مصرف شود
14. **هیچ هزینه‌ای** نداشته باشد (رایگان، open source، local-first)
15. اطلاعات و دانش **قابل انتقال** به AI دیگر باشد
16. کاربر **دانش فنی محدودی** دارد — سیستم باید ساده باشد

---

## ۲. ایرادات شناسایی‌شده در Stack پیشنهادی

### 🔴 ایراد ۱: OpenBB — License تغییر کرده

**وضعیت واقعی:**
- OpenBB در مه 2024 license را از MIT به **AGPL** تغییر داد
- Terminal قدیمی sunsetted شده (حذف شده)
- نسخه فعلی (ODP) یک محصول تجاری با free tier محدود است
- Reddit: "Is OpenBB not free anymore?" — کاربران گیج شده‌اند

**نتیجه:** OpenBB دیگر ۱۰۰٪ رایگان و open source نیست.  
**راه‌حل:** جایگزین با **yfinance + Alpha Vantage + Twelve Data** (همگی واقعاً رایگان)

---

### 🔴 ایراد ۲: QuantConnect Lean — MT5 ندارد

**وضعیت واقعی:**
- Lean engine از MT5 به‌صورت native پشتیبانی **نمی‌کند**
- adapter社区ی (MTsocketAPI) ناقص و قدیمی است
- Live trading از طریق Lean نیاز به حساب QuantConnect cloud دارد (پولی)
- Lean بیشتر روی بورس آمریکا (NYSE, NASDAQ) تمرکز دارد

**نتیجه:** Lean برای پروژه ما مناسب نیست چون:
1. MT5 connection ندارد
2. Live trading بدون cloud ممکن نیست
3. فارکس coverage محدود

**راه‌حل:** استفاده مستقیم از **MetaTrader5 Python library** + **vectorbt** برای backtest

---

### 🔴 ایراد ۳: MetaTrader5 Python library — محدودیت‌های واقعی

**وضعیت واقعی:**
- فقط روی **Windows** کار می‌کند (macOS/Linux نه)
- نیاز به **MT5 terminal نصب و باز** دارد
- همزمان فقط به **یک حساب** می‌تواند وصل شود
- برای هر بروکر جدید، MT5 terminal آن بروکر باید نصب باشد

**نتیجه:** برای "ابزار عمومی" بودن، این یک محدودیت جدی است.

**راه‌حل:**
- فاز ۱: فقط MT5 (ساده، کار می‌کند)
- فاز ۲: اضافه کردن MetaApi (cloud API برای MT5 — رایگان تا حدی)
- فاز ۳: سایر broker APIs (cTrader, DXtrade و...)

---

### 🟡 ایراد ۴: instagrapi — خطر بن شدن

**وضعیت واقعی:**
- Instagram فعالانه scrapers را بلاک می‌کند
- instagrapi از private API استفاده می‌کند → خطر ban حساب
- Rate limits سخت‌گیرانه (5-15 دقیقه soft ban, ساعات hard ban)

**نتیجه:** اگر از حساب اصلی کاربر استفاده شود، خطر ban وجود دارد.

**راه‌حل:**
1. از **حساب فرعی** (نه اصلی) استفاده شود
2. **Human-in-the-loop**: وقتی نیاز به login باشد، کاربر تأیید کند
3. **حالت امن**: فقط لینک‌هایی که کاربر می‌فرستد بررسی شوند (نه اسکن خودکار کل پیج)
4. **Instagram Graph API** (رسمی): اگر پیج خود کاربر باشد → رسمی و امن

---

### 🟡 ایراد ۵: LangGraph — dependency سنگین

**وضعیت واقعی:**
- LangGraph کل LangChain ecosystem را با خود می‌آورد (~50+ packages)
- برای patternهای ساده (if/else, sequential) overkill است
- Reddit: "build agents with raw python or use frameworks?"

**نتیجه:** اگر patternهای ساده باشند، LangChain اضافی است.

**راه‌حل:**
- **Pydantic AI** به‌تنهایی برای agentهای ساده کافی است
- **LangGraph** فقط وقتی لازم است که workflow پیچیده باشد (checkpoint, resume, human-in-the-loop)
- ترکیب: Pydantic AI برای agents + LangGraph فقط برای orchestrator اصلی

---

### 🟡 ایراد ۶: Ollama روی i5-2410M — عملی نیست

**وضعیت واقعی:**
- i5-2410M (2011) — 2 هسته واقعی
- بدون AVX2 — محدودیت instruction set
- RAM احتمالاً 4-8GB
- Ollama با مدل 3B روی CPU: **10-30 tokens/second** (خیلی کند)
- برای تصمیم‌گیری real-time trading مناسب نیست

**نتیجه:** Local LLM روی این سخت‌افزار برای trading کاربردی نیست.

**راه‌حل:**
- **APIهای رایگان** برای کارهای سنگین:
  - Google Gemini API (رایگان)
  - Mistral API (رایگان)
  - Groq API (رایگان، سریع)
  - Anthropic free tier
- **Local فقط برای کارهای سبک**: sentiment analysis, classification
- **FinBERT** برای sentiment (CPU-friendly, 110M params)

---

### 🟡 ایراد ۷: UI — پیچیدگی غیرضروری

**وضعیت واقعی:**
- shadcn/ui + React = نیاز به Node.js, npm, TypeScript, React
- کاربر دانش فنی محدودی دارد
- برای یک پنل محلی محلی، این stack سنگین است

**نتیجه:** پنل باید ساده باشد.

**راه‌حل:**
- **فاز ۱ (ساده):** FastAPI + Jinja2 templates + HTMX + Tailwind CSS
  - بدون Node.js
  - بدون React
  - سریع و ساده
  - کاملاً رایگان
- **فاز ۲ (پیشرفته):** اگر لازم شد، React + shadcn/ui اضافه شود

---

### 🟡 ایراد ۸: ۲۴ ساعته — بازار فارکس تعطیل است

**وضعیت واقعی:**
- فارکس شنبه-یکشنبه تعطیل است
- sessions مختلف: Asian, European, American
- نقدینگی در ساعات مختلف فرق دارد

**نتیجه:** "۲۴ ساعته" باید فقط شامل ساعات بازار باشد.

**راه‌حل:**
- فیلتر زمانی خودکار بر اساس session
- European session: 08:00-17:00 UTC (بهترین برای فارکس)
- American session: 13:00-22:00 UTC
- Asian session: 00:00-08:00 UTC (کمترین نقدینگی)

---

### 🟢 ایراد ۹: Multi-broker — پیچیدگی عظیم

**وضعیت واقعی:**
- هر بروکر: spread متفاوت, leverage متفاوت, rules متفاوت
- هر حساب: bonus متفاوت, margin متفاوت
- خواندن قوانین از پنل بروکر = scraping پیچیده

**نتیجه:** Multi-broker یک پروژه عظیم است. نباید از اول انجام شود.

**راه‌حل:**
- فاز ۱: فقط یک بروکر (Aron Markets)
- فاز ۲: اضافه کردن بروکرهای بعدی
- هر بروکر = یک adapter مجزا

---

### 🟢 ایراد ۱۰: Knowledge Portability — فرمت ذخیره‌سازی

**وضعیت واقعی:**
- کاربر می‌خواهد اگر credit تمام شد یا AI دیگری بخواهد، اطلاعات قابل انتقال باشد
- SQLite خوب است ولی schema باید مستند باشد
- JSON/Markdown بهتر از binary formats هستند

**نتیجه:** فرمت ذخیره‌سازی باید readable و documentable باشد.

**راه‌حل:**
- **SQLite** برای structured data
- **Markdown files** برای knowledge base (قابل خواندن توسط هر AI)
- **JSON** برای configuration
- **docs/DECISIONS.md** — تمام تصمیمات ثبت شود
- **docs/KNOWLEDGE_BASE.md** — دانش استخراج‌شده

---

## ۳. Stack بهبودیافته (پیشنهاد نهایی)

### مقایسه قبل و بعد

| Component | قبل (پیشنهاد اولیه) | بعد (بهبودیافته) | دلیل تغییر |
|---|---|---|---|
| **Trading Engine** | QuantConnect Lean | **MetaTrader5 library + custom** | Lean MT5 ندارد |
| **Backtest** | vectorbt + Lean | **vectorbt + backtesting.py** | ساده‌تر، واقعاً رایگان |
| **Financial Data** | OpenBB | **yfinance + Alpha Vantage + MT5** | OpenBB AGPL شده |
| **UI Panel** | shadcn/ui + React | **FastAPI + HTMX + Tailwind** | ساده‌تر، بدون Node.js |
| **Agent Core** | LangGraph + Pydantic AI | **Pydantic AI + LangGraph (فقط orchestration)** | سبک‌تر |
| **Local LLM** | Ollama (3B models) | **APIهای رایگان + FinBERT** | CPU خیلی ضعیف |
| **Instagram** | instagrapi | **instagrapi (حساب فرعی) + manual link** | خطر ban |
| **Browser** | Playwright + Browser Use | **Playwright + Browser Use (فقط وقتی لازم)** | سادگی |
| **Browser Agent** | Browser Use | **Browser Use + instagrapi fallback** | انعطاف |

---

## ۴. معماری بهبودیافته

```
┌─────────────────────────────────────────────────────┐
│                   🧠 Orchestrator                    │
│              (Pydantic AI + LangGraph)               │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📱 Learning Engine                                  │
│  ├── Instagram Scraper (instagrapi)                 │
│  ├── Link Extractor (تگرام، منابع)                  │
│  ├── Video Content Extractor                        │
│  ├── Concept Learner (API رایگان)                   │
│  └── Knowledge Saver (SQLite + Markdown)            │
│                                                     │
│  📊 Strategy Engine                                  │
│  ├── Strategy Extractor (از محتوا)                  │
│  ├── Strategy Parser (تبدیل به قوانین)              │
│  ├── Backtester (vectorbt)                          │
│  ├── Consensus Engine (چند استراتژی → اجماع)       │
│  └── Confidence Scorer                              │
│                                                     │
│  ⚠️ Risk Engine (100% Deterministic)                │
│  ├── Position Sizing                                │
│  ├── Drawdown Monitor                               │
│  ├── Exposure Calculator                            │
│  ├── Broker Rules Reader                            │
│  └── Account Limits Checker                         │
│                                                     │
│  🔗 MT5 Connector                                   │
│  ├── Account Info                                   │
│  ├── Open/Close Trades                              │
│  ├── Price Data                                     │
│  ├── Symbol Properties                              │
│  └── Trade History                                  │
│                                                     │
│  🤖 Trading Executor                                │
│  ├── Signal Generator                               │
│  ├── Order Manager                                  │
│  ├── Position Monitor                               │
│  └── Session Filter (ساعت بازار)                   │
│                                                     │
│  📰 Research Engine                                 │
│  ├── News Monitor (Twitter, RSS)                    │
│  ├── Sentiment Analysis (FinBERT)                   │
│  ├── Broker Research                                │
│  └── Source Validator                               │
│                                                     │
│  📈 Panel (FastAPI + HTMX)                          │
│  ├── Account Dashboard                              │
│  ├── Open Positions                                 │
│  ├── Trade History                                  │
│  ├── Strategy Performance                           │
│  └── Broker Info                                    │
│                                                     │
│  📲 Telegram Notifier                               │
│  ├── Trade Alerts                                   │
│  ├── Daily Report                                   │
│  └── Error Notifications                            │
│                                                     │
│  🧠 Memory (SQLite + Markdown + DuckDB)             │
│  ├── Strategies                                     │
│  ├── Decisions                                      │
│  ├── Lessons                                        │
│  ├── Broker Rules                                   │
│  └── Knowledge Base                                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## ۵. ترتیب اجرای پیشنهادی (بازبینی‌شده)

| مرحله | کار | وابستگی | اولویت |
|---|---|---|---|
| ۱ | ساختار پروژه + Memory (SQLite + Markdown) | - | 🔴 |
| ۲ | MT5 Connector (اتصال حساب Aron) | مرحله ۱ | 🔴 |
| ۳ | Risk Engine (deterministic) | مرحله ۱ | 🔴 |
| ۴ | Strategy Engine (extract + parse) | مرحله ۱ | 🟡 |
| ۵ | Instagram Scraper (safety mode) | مرحله ۱ | 🟡 |
| ۶ | Backtester (vectorbt) | مرحله ۴ | 🟡 |
| ۷ | Trading Executor (MT5 orders) | مرحله ۲+۳ | 🟡 |
| ۸ | Panel (FastAPI + HTMX) | مرحله ۲ | 🟢 |
| ۹ | Telegram Notifier | مرحله ۷ | 🟢 |
| ۱۰ | News Monitor | مرحله ۱ | 🟢 |
| ۱۱ | Consensus Engine | مرحله ۶+۷ | 🟢 |
| ۱۲ | Self-Evaluation Loop | مرحله ۱۱ | 🟢 |
| ۱۳ | Multi-broker (فقط وقتی اولی stable شد) | مرحله ۷ | ⚪ |

---

## ۶. AI Models پیشنهادی (رایگان)

| کار | مدل/Service | رایگان؟ | سرعت |
|---|---|---|---|
| **Reasoning/Planning** | Google Gemini Flash | ✅ رایگان | سریع |
| **Text Extraction** | Mistral Small | ✅ رایگان | سریع |
| **Sentiment** | FinBERT (local) | ✅ رایگان | سریع |
| **Coding** | Groq (Llama 3.1) | ✅ رایگان | خیلی سریع |
| **Vision/OCR** | Gemini Flash (vision) | ✅ رایگان | سریع |
| **Classification** | FinBERT (local) | ✅ رایگان | سریع |
| **Complex Analysis** | Claude/GPT (فقط وقتی لازم) | ⚠️ پولی | آهسته |

---

## ۷. لیست نهایی Dependencies

### Python Packages (همگی رایگان)

```
# Core
pydantic-ai          # Agent framework (MIT)
langgraph            # Orchestrator (فقط اگر لازم باشد) (MIT)

# MT5
MetaTrader5          # اتصال به متاتریدر (فقط Windows)

# Data
yfinance             # Historical data (Apache 2.0)
requests             # HTTP calls
feedparser           # RSS feeds

# Backtesting
vectorbt             # Vectorized backtest (MIT)

# Technical Analysis
TA-Lib               # 200+ indicators (BSD)
pandas-ta            # Fallback indicators (MIT)

# Instagram
instagrapi           # Instagram scraper (MIT)

# Browser
playwright           # Browser automation (Apache 2.0)
browser-use          # AI browser agent (MIT)

# Web Panel
fastapi              # Backend (MIT)
uvicorn              # Server (BSD)
jinja2               # Templates (BSD)
htmx                 # Frontend interactivity (MIT)
tailwindcss          # CSS (MIT)

# Telegram
python-telegram-bot  # Bot notifications (GPL-3.0)

# Database
sqlite3              # Built-in Python
duckdb               # Analytics (MIT)

# Sentiment
transformers         # FinBERT (Apache 2.0)
torch                # ML backend (BSD)

# Utilities
python-dotenv        # Env vars (BSD)
pydantic             # Data validation (MIT)
```

### NOT Needed

```
# حذف شده:
openbb               # AGPL + تجاری
quantconnect-lean    # MT5 ندارد
flask                # FastAPI جایگزین شد
react / node.js      # HTMX جایگزین شد
ollama               # CPU خیلی ضعیف
```

---

## ۸. مستندات ضروری برای انتقال

هر فایل زیر باید ذخیره شود تا AI دیگری بتواند پروژه را ادامه دهد:

| فایل | محتوا |
|---|---|
| `docs/MASTER_SPECIFICATION.md` | سند مادر پروژه (ترجمه/خلاصه) |
| `docs/IMPROVEMENT_REVIEW.md` | همین فایل |
| `docs/ARCHITECTURE.md` | معماری کلی |
| `docs/DECISIONS.md` | تمام تصمیمات فنی |
| `docs/LESSONS.md` | درس‌آموخته‌ها |
| `docs/KNOWLEDGE_BASE.md` | دانش استخراج‌شده |
| `docs/BROKER_RULES.md` | قوانین بروکرها |
| `docs/STRATEGIES.md` | استراتژی‌های یادگرفته‌شده |
| `config/settings.yaml` | تنظیمات پروژه |
| `requirements.txt` | Dependencies |
| `README.md` | راهنمای اجرا |

---

## ۹. سؤالات باقیمانده (قبل از اجرا)

### سؤالات فنی:
1. **MT5 نصب است؟** — آیا متاتریدر 5 روی سیستم شما نصب و باز است؟
2. **RAM** — چقدر RAM دارید؟ (برای FinBERT و تحلیل لازم است)
3. **اینترنت** — اتصال پایدار دارید؟ (برای API calls)

### سؤالات استراتژی:
4. **xBB Score** — وقتی چند استراتژی اجماع دارند، حداقل چند درصد اعتماد لازم است برای ورود؟
5. **حداکثر ریسک** — در هر ترید حداکثر چند درصد سرمایه ریسک شود؟ (۱٪؟ ۲٪؟)
6. **حداکثر پوزیشن** — همزمان حداکثر چند پوزیشن باز باشد؟

### سؤالات عملی:
7. **اینستاگرام** — آیا حساب فرعی برای scraper دارید یا باید ایجاد کنم؟
8. **تلگرام** — آیا Bot تلگرام ایجاد کرده‌اید یا باید راهنمایی کنم؟
9. **ساعت کار** — آیا می‌خواهید فقط در ساعات خاصی ترید شود؟

---

## ۱۰. خلاصه تغییرات Stack

```
قبل:  QuantConnect Lean + OpenBB + shadcn/ui + React + Ollama
بعد:  MetaTrader5 + vectorbt + FastAPI + HTMX + APIهای رایگان

قبل:  ۱۵+ dependency سنگین
بعد:  ۱۲+ dependency سبک

قبل:  نیاز به Node.js
بعد:  فقط Python

قبل:  Local LLM (غیرعملی روی CPU قدیمی)
بعد:  APIهای رایگان + FinBERT local

قبل:  License مشکل‌دار (AGPL)
بعد:  همه MIT/Apache/BSD
```
