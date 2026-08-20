# 📝 Decision Log — Trading Bot

**هدف:** ثبت تمام تصمیمات فنی برای قابلیت انتقال به AI دیگر

---

## Decision 001: Agent Framework
**تاریخ:** 2026-08-18
**تصمیم:** Pydantic AI + LangGraph (فقط orchestration)
**دلیل:** Pydantic AI سبک و type-safe است. LangGraph فقط برای workflow پیچیده (checkpoint, resume) لازم است.
**جایگزین رد شده:** CrewAI (کنترل کمتر), AutoGen (در حال transition)
**وضعیت:** ✅ تأیید شده

---

## Decision 002: Trading Engine
**تاریخ:** 2026-08-18
**تصمیم:** MetaTrader5 Python library مستقیم
**دلیل:** MT5 terminal نصب است. Python library رسمی و رایگان است.
**جایگزین رد شده:** QuantConnect Lean (MT5 ندارد), MetaApi (پولی)
**وضعیت:** ✅ تأیید شده

---

## Decision 003: Backtesting
**تاریخ:** 2026-08-18
**تصمیم:** vectorbt (primary) + backtesting.py (fallback)
**دلیل:** vectorbt سریع و MIT license. backtesting.py AGPL ولی برای research OK.
**جایگزین رد شده:** QuantConnect Lean (MT5 ندارد)
**وضعیت:** ✅ تأیید شده

---

## Decision 004: Financial Data
**تاریخ:** 2026-08-18
**تصمیم:** MT5 built-in + yfinance + Alpha Vantage
**دلیل:** OpenBB AGPL شده و تجاری. yfinance رایگان و ساده.
**جایگزین رد شده:** OpenBB (AGPL + تجاری)
**وضعیت:** ✅ تأیید شده

---

## Decision 005: UI Panel
**تاریخ:** 2026-08-18
**تصمیم:** FastAPI + HTMX + Tailwind CSS
**دلیل:** بدون Node.js. ساده. سریع. رایگان.
**جایگزین رد شده:** shadcn/ui + React (نیاز به Node.js, پیچیده)
**وضعیت:** ✅ تأیید شده

---

## Decision 006: AI Models
**تاریخ:** 2026-08-18
**تصمیم:** APIهای رایگان (Gemini, Mistral, Groq) + FinBERT local
**دلیل:** CPU i5-2410M بدون AVX2 — Ollama غیرعملی. APIهای رایگان کافی هستند.
**جایگزین رد شده:** Ollama (CPU خیلی ضعیف), OpenAI (پولی)
**وضعیت:** ✅ تأیید شده

---

## Decision 007: Instagram Scraper
**تاریخ:** 2026-08-18
**تصمیم:** instagrapi (حساب فرعی) + manual link input
**دلیل:** instagrapi سریع‌ترین و MIT. حساب فرعی برای جلوگیری از ban.
**جایگزین رد شده:** instaloader (قدیمی‌تر), Instagram Graph API (نیاز به app approval)
**وضعیت:** ✅ تأیید شده

---

## Decision 008: Browser Automation
**تاریخ:** 2026-08-18
**تصمیم:** Playwright + Browser Use (فقط وقتی لازم)
**دلیل:** Playwright سریع‌ترین. Browser Use برای AI browser agent.
**جایگزین رد شده:** Selenium (قدیمی‌تر, کندتر)
**وضعیت:** ✅ تأیید شده

---

## Decision 009: Database
**تاریخ:** 2026-08-18
**تصمیم:** SQLite + DuckDB + Markdown files
**دلیل:** SQLite برای structured data. DuckDB برای analytics. Markdown برای portability.
**جایگزین رد شده:** PostgreSQL (نیاز به server), MongoDB (نیاز به server)
**وضعیت:** ✅ تأیید شده

---

## Decision 010: Risk Engine
**تاریخ:** 2026-08-18
**تصمیم:** Custom deterministic engine
**دلیل:** Risk باید 100% deterministic باشد. وابسته به LLM نباشد.
**جایگزین رد شده:** Riskfolio-Lib (پیچیده, portfolio-focused)
**وضعیت:** ✅ تأیید شده

---

## Decision 011: Technical Analysis
**تاریخ:** 2026-08-18
**تصمیم:** TA-Lib (primary) + pandas-ta (fallback)
**دلیل:** TA-Lib 200+ indicators, BSD, C core سریع.
**جایگزین رد شده:** custom indicators (زمان‌بر)
**وضعیت:** ✅ تأیید شده

---

## Decision 012: Telegram Notifications
**تاریخ:** 2026-08-18
**تصمیم:** python-telegram-bot
**دلیل:** بهترین و most-maintained. GPL-3.0 (برای bot شخصی OK).
**جایگزین رد شده:** pyTelegramBotAPI (کمتر maintained)
**وضعیت:** ✅ تأیید شده

---

## Decision 013: Sentiment Analysis
**تاریخ:** 2026-08-18
**تصمیم:** FinBERT (ProsusAI/finbert) locally
**دلیل:** 110M params, CPU-friendly, Apache 2.0, مخصوص finance.
**جایگزین رد شده:** GPT API (پولی), VADER (ساده, دقیق نیست)
**وضعیت:** ✅ تأیید شده

---

## Decision 014: Language
**تاریخ:** 2026-08-18
**تصمیم:** Python 3.14 (از قبل نصب شده)
**دلیل:** همه libraries Python دارند. ساده‌ترین.
**وضعیت:** ✅ تأیید شده

---

## Decision 015: Default Risk Per Trade
**تاریخ:** 2026-08-18
**تصمیم:** 1% پیش‌فرض (قابل تنظیم 0.25% تا 3%)
**دلیل:** استاندارد صنعتی. حساب‌های کوچک: 0.5%, Prop Firm: 0.25-0.5%
**خودکار:** بر اساس اندازه حساب محاسبه می‌شود
**وضعیت:** ✅ تأیید شده

---

## Decision 016: Consensus Threshold
**تاریخ:** 2026-08-18
**تصمیم:** 65% اجماع برای ورود به ترید
**دلیل:** اگر ۳ استراتژی موافق باشند (61% + 58% + 55%) → میانگین ~58% → نیاز به 65% برای تأیید
**وضعیت:** ✅ تأیید شده

---

## Decision 017: Primary Strategy
**تاریخ:** 2026-08-18
**تصمیم:** ICT/SMC به‌عنوان استراتژی اصلی
**دلیل:** بهترین نتایج بک‌تست (WR 61.2%, PF 2.17, 2600 trades)
**تایم‌فریم:** M15-H4
**sessions:** London + New York
**وضعیت:** ✅ تأیید شده

---

## Decision 018: Data Sources
**تاریخ:** 2026-08-18
**تصمیم:** MT5 + Dukascopy + yfinance
**دلیل:** همه واقعاً رایگان. OpenBB حذف شد (AGPL).
**وضعیت:** ✅ تأیید شده
**تاریخ:** 2026-08-18
**تصمیم:** Python 3.14 (از قبل نصب شده)
**دلیل:** همه libraries Python دارند. ساده‌ترین.
**وضعیت:** ✅ تأیید شده
