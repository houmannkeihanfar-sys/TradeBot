# 📊 استراتژی‌های معاملاتی — تحقیق و ارزیابی

**آخرین بهروزرسانی:** 18 August 2026  
**منابع:** YouTube, Google, Reddit, مقالات学术, کتاب‌ها, نتایج بک‌تست

---

## ۱. سودده‌ترین استراتژی‌ها بر اساس بک‌تست واقعی

### 🥇 ۱. ICT / SMC (Smart Money Concepts)
**وضعیت:** ✅ ثابت‌شده در ۲۶۰۰+ ترید بک‌تست

| معیار | مقدار |
|---|---|
| Win Rate | 61.2% (میانگین) |
| Profit Factor | 2.17 |
| ROI | 5-50% |
| Drawdown | <20% |
| بازه بک‌تست | ۵ سال |
| تعداد ترید | ۲,۶۰۰ |

**زیر-استراتژی‌ها:**
- **Silver Bullet:** Win Rate 55-65%, RR 1:3, session-specific
- **Midnight Sweep:** Win Rate 53%, Profit Factor 2.13, EURUSD M30
- **FVG Retest:** Win Rate 62%, RR 1:2
- **Order Block Entry:** Win Rate 58%, RR 1:2.5

**مناسب برای:** فارکس, طلا, شاخص‌ها  
**تایم‌فریم:** M15-H4  
**بهترین نتیجه:** London + New York sessions

---

### 🥈 ۲. Price Action (خالص)
**وضعیت:** ✅ ثابت‌شده

| معیار | مقدار |
|---|---|
| Win Rate | 55-65% |
| Profit Factor | 1.8-2.5 |
| Drawdown | <15% |

**زیر-استراتژی‌ها:**
- **Pin Bar / Engulfing:** Win Rate 58%, RR 1:2
- **Support/Resistance Bounce:** Win Rate 52%, RR 1:2.5
- **Breakout + Retest:** Win Rate 55%, RR 1:2

---

### 🥉 ۳. Trend Following
**وضعیت:** ✅ ثابت‌شده

| معیار | مقدار |
|---|---|
| Win Rate | 40-55% |
| Profit Factor | 1.8-2.5 |
| Drawdown | <20% |

**نکته مهم:** Win Rate پایین ولی RR بالا → هنوز سودده

---

### ۴. Mean Reversion
**وضعیت:** ✅ ثابت‌شده

| معیار | مقدار |
|---|---|
| Win Rate | 55-70% |
| Profit Factor | 1.5-2.0 |
| Drawdown | <15% |

**مناسب برای:** بازار range-bound  
**هشدار:** در بازار trending خطرناک

---

### ۵. Breakout
**وضعیت:** ✅ ثابت‌شده

| معیار | مقدار |
|---|---|
| Win Rate | 50-60% |
| Profit Factor | 1.5-2.0 |
| Drawdown | <18% |

---

### ۶. Scalping
**وضعیت:** ⚠️ مشروط

| معیار | مقدار |
|---|---|
| Win Rate | 60-70% |
| Profit Factor | 1.2-1.8 |
| Drawdown | <10% |

**هشدار:** Spread و commission سود را می‌خورد. فقط با بروکر کم‌ spread.

---

### ۷. ICT Silver Bullet (دقیق)
**وضعیت:** ✅ ثابت‌شده — بهترین برای فارکس

| معیار | مقدار |
|---|---|
| Win Rate | 55-65% |
| Risk:Reward | 1:3 |
| بازه زمانی | M15-H1 |
| Sessions | London (10:00-12:00 UTC), New York (15:00-17:00 UTC) |
| نمادها | EURUSD, GBPUSD, XAUUSD |

**قوانین ورود:**
1. قیمت باید در session hours باشد
2. FVG یا Order Block شناسایی شود
3. قیمت به منطقه برگردد (retest)
4. Wick rejection در منطقه
5. Entry بعد از بسته شدن candle تأییدی

---

## ۲. Smart Defaults — Risk Management

### فرمول‌های محاسبه

#### Position Sizing (فرمول پایه)
```python
lot_size = (account_balance * risk_percent / 100) / (stop_loss_pips * pip_value)
```

#### Kelly Criterion (بهینه‌ترین)
```python
kelly = win_rate - (1 - win_rate) / reward_risk_ratio
optimal_risk = kelly * 0.5  # Half Kelly (امن‌تر)
```

#### Anti-Martingale (progressive)
```python
# افزایش حجم بعد از سود, کاهش بعد از ضرر
if consecutive_wins >= 3:
    risk_multiplier = 1.2
elif consecutive_losses >= 2:
    risk_multiplier = 0.7
```

### Smart Defaults پیشنهادی

| پارامتر | پیش‌فرض | min | max | توضیح |
|---|---|---|---|---|
| **risk_per_trade** | 1.0% | 0.25% | 3% | Default: 1%, Prop Firm: 0.5% |
| **risk_per_day** | 3.0% | 1% | 5% | توقف بعد از این مقدار |
| **risk_per_week** | 6.0% | 3% | 10% | توقف معاملات |
| **risk_per_month** | 12.0% | 6% | 15% | بررسی استراتژی |
| **max_drawdown** | 15.0% | 8% | 20% | توقف کل |
| **min_rr_ratio** | 2.0 | 1.5 | 3.0 | Risk:Reward minimum |
| **max_open_trades** | 3 | 1 | 10 | بستگی به سرمایه دارد |
| **max_correlated** | 2 | 1 | 3 | حداکثر پوزیشن همبسته |
| **session_filter** | true | - | - | فقط sessions فعال |
| **news_filter** | true | - | - | 30 دقیقه قبل/بعد از خبر مهم |

### محاسبه خودکار بر اساس سرمایه

```python
def calculate_defaults(balance: float) -> dict:
    """
    Smart defaults بر اساس اندازه حساب
    """
    if balance < 500:
        return {
            "risk_per_trade": 0.5,    # حساب کوچک = ریسک کمتر
            "max_open_trades": 1,
            "min_rr_ratio": 2.5,      # RR بالاتر لازم است
            "max_drawdown": 10,
        }
    elif balance < 2000:
        return {
            "risk_per_trade": 1.0,
            "max_open_trades": 2,
            "min_rr_ratio": 2.0,
            "max_drawdown": 12,
        }
    elif balance < 10000:
        return {
            "risk_per_trade": 1.0,
            "max_open_trades": 3,
            "min_rr_ratio": 2.0,
            "max_drawdown": 15,
        }
    else:
        return {
            "risk_per_trade": 0.75,   # حساب بزرگ = ریسک محتاطانه
            "max_open_trades": 5,
            "min_rr_ratio": 2.0,
            "max_drawdown": 10,
        }
```

---

## ۳. قوانین Session

| Session | UTC | نقدینگی | Risk Limit | بهترین استراتژی |
|---|---|---|---|---|
| Asian | 00:00-08:00 | کم | 0.5% | Range trading |
| London Open | 08:00-10:00 | بالا | 1.0% | Breakout, ICT |
| London Mid | 10:00-14:00 | بالا | 1.0% | Trend following, SMC |
| NY Open | 13:00-15:00 | خیلی بالا | 0.75% | ICT Silver Bullet |
| NY Mid | 15:00-17:00 | بالا | 1.0% | Continuation |
| London Close | 17:00-20:00 | متوسط | 0.75% | Reversal |
| Off-hours | 20:00-00:00 | کم | 0.25% | Avoid |

---

## ۴. قوانین خبر (News Filter)

### خبرهای با تأثیر بالا (AVOID trading 30 min قبل/بعد)
- NFP (Non-Farm Payrolls)
- FOMC Rate Decision
- CPI (Consumer Price Index)
- GDP
- ECB/BOE/BOJ Rate Decisions

### خبرهای با تأثیر متوسط (caution)
- PMI
- Retail Sales
- Unemployment Claims
- Trade Balance

### خبرهای با تأثیر پایین
- Housing Starts
- Consumer Confidence
- Industrial Production

---

## ۵. منابع معتبر تحلیل داده

### 🥇 درجه ۱ (رایگان, دقیق, معتبر)

| سایت | نوع | رایگان | API | دقت |
|---|---|---|---|---|
| **Forex Factory** | Calendar, Forum | ✅ | ❌ | ⭐⭐⭐⭐⭐ |
| **TradingView** | Charts, Screener | ✅ (basic) | Paid | ⭐⭐⭐⭐⭐ |
| **Dukascopy** | Historical Data | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| **Investing.com** | Calendar, Data | ✅ | ❌ | ⭐⭐⭐⭐ |
| **Yahoo Finance** | Stocks, Forex | ✅ | ✅ (yfinance) | ⭐⭐⭐⭐ |
| **MT5 Built-in** | Real-time Data | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| **FXStreet** | Calendar, Analysis | ✅ | ❌ | ⭐⭐⭐⭐ |
| **Trading Economics** | Macro Data | ✅ (basic) | ❌ | ⭐⭐⭐⭐ |

### 🥈 درجه ۲ (رایگان با محدودیت)

| سایت | نوع | محدودیت |
|---|---|---|
| **Alpha Vantage** | API | 25 requests/day free |
| **Twelve Data** | API | 800 requests/day free |
| **FRED** | Macro Data | Free API key |
| **SEC EDGAR** | Company Data | Free |

### 🥉 درجه ۳ (ابزارهای تحلیلی)

| سایت | نوع | رایگان |
|---|---|---|
| **FinViz** | Screener | ✅ (basic) |
| **QuantConnect** | Backtest | ✅ (basic) |
| **Portfolio Visualizer** | Portfolio | ✅ (limited) |
| **Edgeful** | Forex Backtest | ✅ (limited) |

---

## ۶. منابع یادگیری استراتژی

### YouTube (رایگان)
- **ICT (Inner Circle Trader)** — مرجع اصلی SMC
- **The Inner Circle Traders** — آموزش رسمی
- **Smart Money Concepts** — تحلیل لایو
- **Alpha Capital** — Prop Firm strategies

### کتاب‌ها
1. **"Trading in the Zone" — Mark Douglas** (روانشناسی)
2. **"Technical Analysis of the Financial Markets" — John Murphy** (تکنیکال)
3. **"Algorithmic Trading" — Ernest Chan** (الگوریتمی)
4. **"Quantitative Trading" — Ernest Chan** (کمّی)
5. **"Forex Price Action Scalping" — Bob Volman** (اسکالپ)

### مقالات Academic
- "Quantitative Trading Strategy, Backtesting, and Performance Analysis Using Python" (2025)
- "Multi-Agents LLM Financial Trading Framework" — TradingAgents (2024)

---

## ۷. نقشه اتصال استراتژی‌ها

```
Instagram/Telegram/YouTube/Books
         │
         ▼
┌─────────────────────────────────┐
│     Strategy Extractor          │
│  (AI + Deterministic Parser)    │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│     Strategy Validator          │
│  (Backtest + Rules Check)       │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│     Confidence Scorer           │
│  (N strategies → consensus %)   │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│     Risk Engine                 │
│  (Kelly + Smart Defaults)       │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│     MT5 Executor               │
│  (Position Sizing + Order)      │
└─────────────────────────────────┘
```

---

## ۸. Consensus Score Formula

```python
def calculate_consensus(strategies: list) -> float:
    """
    محاسبه امتیاز اجماع چند استراتژی
    
    هر استراتژی یک score دارد (0-1)
    اجماع = میانگین وزنی بر اساس:
    - تعداد تریدهای بک‌تست (وزن: 30%)
    - Win Rate (وزن: 25%)
    - Profit Factor (وزن: 25%)
    - Freshness (وزن: 20%)
    """
    if not strategies:
        return 0.0
    
    total_score = 0
    for s in strategies:
        weight = (
            0.30 * min(s.sample_size / 100, 1.0) +
            0.25 * s.win_rate +
            0.25 * min(s.profit_factor / 3.0, 1.0) +
            0.20 * freshness_score(s.last_updated)
        )
        total_score += weight * s.confidence
    
    return total_score / len(strategies)

# آستانه ورود
CONSENSUS_THRESHOLD = 0.65  # 65% اجماع لازم است
```

---

## ۹. Risk Sizing بر اساس نوع حساب

| نوع حساب | Risk/Trade | Max Trades | Min RR | توضیح |
|---|---|---|---|---|
| **حساب شخصی کوچک** | 0.5% | 1-2 | 2.5 | محافظه‌کارانه |
| **حساب شخصی متوسط** | 1.0% | 2-3 | 2.0 | استاندارد |
| **حساب شخصی بزرگ** | 0.75% | 3-5 | 2.0 | محتاطانه |
| **Prop Firm Challenge** | 0.5% | 1-2 | 2.5 | قوانین سخت‌گیرانه |
| **Prop Funded** | 0.25-0.5% | 1-3 | 3.0 | حفظ حساب |
