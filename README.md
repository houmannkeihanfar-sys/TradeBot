# 🤖 AI Trading Bot — Autonomous Multi-Agent Trading System

> **A comprehensive, AI-powered trading system that learns strategies from social media, analyzes markets, and executes trades on MetaTrader 5 — built with Python, local-first, free, and open-source.**

[![Python 3.14](https://img.shields.io/badge/Python-3.14-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://microsoft.com)
[![MT5](https://img.shields.io/badge/MetaTrader-5-orange.svg)](https://www.metatrader5.com)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Modules](#modules)
- [Strategy System](#strategy-system)
- [Risk Management](#risk-management)
- [Video Analysis](#video-analysis)
- [Security](#security)
- [Technology Stack](#technology-stack)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project is an **autonomous AI trading system** designed to:

1. **Learn** trading strategies from social media (Instagram, Telegram, YouTube, Twitter/X)
2. **Analyze** video content to extract trading strategies, indicators, and rules
3. **Validate** strategies through backtesting and paper trading
4. **Execute** trades on MetaTrader 5 with proper risk management
5. **Monitor** economic news and market conditions
6. **Evaluate** its own performance and improve over time

### 💡 Why This Project?

- **No paid APIs** — uses free tiers, local tools, and open-source software
- **Local-first** — all data stays on your machine
- **Multi-market** — Forex, Gold, Crypto, Indices
- **Multi-broker** — works with any MT5 broker
- **Multi-timeframe** — analyzes all timeframes simultaneously
- **User-friendly** — web dashboard, Telegram notifications
- **Portable** — all knowledge stored in transferable formats (JSON, SQLite, Markdown)

---

## ✨ Key Features

### 🧠 Intelligent Strategy Learning
- Analyzes Instagram posts, Telegram channels, YouTube videos
- Extracts trading strategies from video content (audio + visual)
- Uses Google Gemini API for video understanding
- Supports OCR for chart analysis
- Maintains a structured knowledge base of learned strategies

### 📊 Strategy Engine
- Converts learned strategies into executable rules
- Multiple strategy consensus system (confidence voting)
- Entry/exit conditions with timestamp evidence
- Automatic strategy scoring and ranking
- Backtesting on historical data

### ⚠️ Risk Management (Deterministic)
- Independent from AI — pure Python calculations
- Position sizing based on account balance and risk %
- Half-Kelly Criterion for optimal sizing
- Session-based risk limits
- Maximum drawdown protection
- Correlation analysis between positions

### 🔗 MetaTrader 5 Integration
- Works with any MT5 broker
- Account info, positions, orders
- Real-time price feeds
- Automated trade execution
- No password storage — runtime input only

### 📈 Trading Panel (Web Dashboard)
- Local web interface (FastAPI + HTMX)
- Account overview, positions, P&L
- Strategy management
- Backtest results
- Risk metrics
- One-click refresh

### 🔔 Notifications
- Telegram bot integration
- Trade opened/closed alerts
- Signal notifications
- Daily performance reports

### 📰 News Monitor
- Economic calendar integration
- News sentiment analysis
- Trading session detection
- High-impact event alerts

### 🔄 Self-Evaluation
- Decision → Result → Error Analysis → Lesson Learned
- Performance tracking per strategy
- Win rate, profit factor, Sharpe ratio
- Automatic strategy adjustment suggestions

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    🧠 Orchestrator                           │
│                   (Python Core)                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📱 Social Media Scraper                                     │
│     ├── Instagram (instagrapi)                               │
│     ├── Telegram (telethon)                                  │
│     ├── YouTube (yt-dlp)                                     │
│     └── Web (Agent Reach / Jina)                             │
│                                                              │
│  🎬 Video Analysis Agent                                     │
│     ├── Gemini API (video understanding)                     │
│     ├── Whisper (speech-to-text)                             │
│     └── OCR (frame extraction)                               │
│                                                              │
│  📚 Knowledge Base (SQLite + Markdown + JSON)                │
│     ├── Strategies                                           │
│     ├── Brokers                                              │
│     ├── Lessons Learned                                      │
│     └── Verified Facts                                       │
│                                                              │
│  🔬 Strategy Engine                                          │
│     ├── Strategy Extraction                                  │
│     ├── Rule Conversion                                      │
│     ├── Consensus Voting                                     │
│     └── Confidence Scoring                                   │
│                                                              │
│  📊 Backtesting Engine                                       │
│     ├── Historical Data                                      │
│     ├── Walk-Forward Analysis                                │
│     ├── Monte Carlo Simulation                               │
│     └── Performance Metrics                                  │
│                                                              │
│  ⚠️ Risk Engine (Deterministic)                              │
│     ├── Position Sizing                                      │
│     ├── Drawdown Protection                                  │
│     ├── Session Limits                                       │
│     └── Correlation Analysis                                 │
│                                                              │
│  🔗 MT5 Connector                                            │
│     ├── Account Info                                         │
│     ├── Price Feeds                                          │
│     ├── Order Execution                                      │
│     └── Position Management                                  │
│                                                              │
│  📈 Trading Panel (Web Dashboard)                            │
│     ├── Account Overview                                     │
│     ├── Position Monitor                                     │
│     ├── Strategy Manager                                     │
│     └── Backtest Results                                     │
│                                                              │
│  🔔 Notifications (Telegram Bot)                            │
│  📰 News Monitor                                             │
│  🔄 Self-Evaluation Loop                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
trading-bot/
├── main.py                    # Entry point
├── config/
│   ├── settings.py            # Global settings
│   ├── account.yaml           # Account config (git-ignored)
│   └── account.yaml.example   # Example config
├── src/
│   ├── core/
│   │   └── orchestrator.py    # Main orchestrator
│   ├── connectors/
│   │   └── mt5_connector.py   # MetaTrader 5 connection
│   ├── risk/
│   │   └── risk_engine.py     # Risk management (deterministic)
│   ├── knowledge/
│   │   └── database.py        # Knowledge base (SQLite)
│   ├── panel/
│   │   └── app.py             # Web dashboard (FastAPI)
│   ├── notifications/
│   │   └── telegram_bot.py    # Telegram notifications
│   ├── backtesting/           # Backtesting engine
│   ├── strategies/            # Strategy management
│   ├── learning/              # Learning loop
│   ├── scrapers/              # Social media scrapers
│   └── trading/               # Trading execution
├── scripts/
│   ├── 01_video_analyzer.py   # Video analysis with Whisper
│   ├── 02_telegram_reader.py  # Telegram channel reader
│   ├── 03_mt5_connector.py    # MT5 connection test
│   ├── 04_ea_generator.py     # Expert Advisor generator
│   ├── 05_risk_engine.py      # Risk calculation
│   ├── 06_web_reader.py       # Web content reader
│   ├── 07_gemini_video_analyzer.py  # Gemini video analysis
│   └── README.md              # Scripts documentation
├── strategies/
│   └── ict_strategy.json      # Example strategy
├── templates/
│   └── dashboard.html         # Web dashboard template
├── docs/
│   ├── ARCHITECTURE.md        # Architecture documentation
│   ├── DECISIONS.md           # Technical decisions log
│   ├── STRATEGIES.md          # Strategy documentation
│   ├── KNOWLEDGE_BASE.md      # Knowledge base guide
│   ├── LESSONS_CRITICAL.md    # Critical lessons learned
│   ├── IMPROVEMENT_REVIEW.md  # Code review & improvements
│   ├── LEARNING_METHODOLOGY.md # How the system learns
│   └── TRANSFER_FILE.md       # Project transfer documentation
├── .gitignore                 # Git ignore rules
├── .env.example               # Environment variables template
└── requirements.txt           # Python dependencies
```

---

## 🚀 Quick Start

### Prerequisites

- **Windows 10/11**
- **Python 3.14+**
- **MetaTrader 5** installed with a broker account
- **VPN** (for regions with API restrictions)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/trading-bot.git
cd trading-bot

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file
cp .env.example .env
# Edit .env with your values

# 5. Copy account config
cp config/account.yaml.example config/account.yaml
# Edit config/account.yaml with your broker details

# 6. Run the bot
python main.py
```

### Usage

```bash
# Run the web dashboard
python main.py panel

# Analyze a video
python scripts/07_gemini_video_analyzer.py path/to/video.mp4 YOUR_API_KEY

# Read a Telegram post
python scripts/02_telegram_reader.py ChannelName 465

# Test MT5 connection
python scripts/03_mt5_connector.py
```

---

## ⚙️ Configuration

### Environment Variables (.env)

| Variable | Description | Required |
|----------|-------------|----------|
| `MT5_LOGIN` | MT5 account number | Yes |
| `MT5_SERVER` | Broker server name | Yes |
| `TELEGRAM_API_ID` | Telegram API ID | For Telegram |
| `TELEGRAM_API_HASH` | Telegram API hash | For Telegram |
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | For notifications |
| `GEMINI_API_KEY` | Google Gemini API key | For video analysis |
| `PROXY_SOCKS5` | SOCKS5 proxy URL | If behind firewall |

### Getting API Keys

| Service | URL | Cost |
|---------|-----|------|
| Telegram API | https://my.telegram.org | Free |
| Telegram Bot | @BotFather on Telegram | Free |
| Gemini API | https://aistudio.google.com/apikey | Free tier |
| MetaTrader 5 | Broker website | Free (demo) |

---

## 📦 Modules

### 🔗 MT5 Connector (`src/connectors/mt5_connector.py`)

Connects to MetaTrader 5 for:
- Account information (balance, equity, margin)
- Symbol information (spread, lot size, contract)
- Real-time price feeds
- Position management (open/close)
- Historical data (OHLCV)

**Key Design:** Passwords are never stored — entered at runtime only.

### ⚠️ Risk Engine (`src/risk/risk_engine.py`)

Deterministic risk management:
- **Position sizing** based on account balance and risk %
- **Half-Kelly Criterion** for optimal bet sizing
- **Session-based limits** (Asian/London/NY/Overlap)
- **Drawdown protection** (daily and total)
- **Correlation analysis** between open positions

### 📚 Knowledge Base (`src/knowledge/database.py`)

SQLite database with 15+ tables:
- Strategies, Brokers, Trades, Backtests
- News, Concepts, Lessons Learned
- Decisions, Permissions, Sources
- Verified/Unverified claims

### 📈 Trading Panel (`src/panel/app.py`)

Local web dashboard (FastAPI):
- Account overview
- Open positions
- Strategy management
- Backtest results
- Risk metrics
- One-click refresh

---

## 📊 Strategy System

### How Strategies Are Learned

1. **Input:** Video, Instagram post, Telegram message, or manual entry
2. **Extraction:** AI analyzes content and extracts trading rules
3. **Validation:** Rules are checked for completeness and consistency
4. **Storage:** Strategy saved in structured JSON format
5. **Backtesting:** Strategy tested on historical data
6. **Scoring:** Performance metrics calculated
7. **Consensus:** Multiple strategies voted on for each signal

### Strategy Format

```json
{
  "name": "ICT Silver Bullet",
  "market": "Forex",
  "symbols": ["EURUSD", "GBPUSD"],
  "timeframe": "M15",
  "bias": "bullish",
  "entry": {
    "condition": "Price touches FVG at key level",
    "confirmation": "Bullish engulfing candle",
    "session": "London/NY overlap"
  },
  "stop_loss": "Below order block",
  "take_profit": "1:3 risk-reward minimum",
  "risk_per_trade": "1%",
  "confidence": 0.75
}
```

---

## ⚠️ Risk Management

### Default Settings (Configurable)

| Setting | Default | Description |
|---------|---------|-------------|
| Risk per trade | 1% | Maximum risk per single trade |
| Max daily drawdown | 5% | Stop trading if daily loss exceeds |
| Max total drawdown | 10% | Emergency stop |
| Max concurrent trades | 5 | Based on broker limits |
| Min risk-reward | 1:1.5 | Minimum acceptable RR ratio |

### Smart Defaults

The system automatically adjusts risk based on:
- Account balance
- Broker constraints
- Strategy confidence
- Market volatility
- Trading session

### Position Sizing Formula

```
Risk Amount = Balance × Risk%
Lot Size = Risk Amount / (Stop Loss in Pips × Pip Value)
```

---

## 🎬 Video Analysis

### How It Works

1. **Upload video** to the `videos/` folder
2. **Run analyzer** with Gemini API or Whisper
3. **Extract:** spoken dialogue + visual content
4. **Identify:** trading concepts, indicators, rules
5. **Structure:** convert to executable strategy
6. **Verify:** cross-check with multiple sources

### Supported Formats

- MP4, MKV, AVI (video)
- YouTube URLs (direct via Gemini)
- Instagram reels
- Telegram video messages

---

## 🔒 Security

### What We Never Store

- ❌ Passwords
- ❌ API keys in code
- ❌ Login credentials
- ❌ Session tokens
- ❌ Personal information

### What We Store (Locally)

- ✅ Account number (in config, git-ignored)
- ✅ Server name (public information)
- ✅ Encrypted sessions (for Telegram API)
- ✅ Trading history and logs

### Best Practices

1. **Never commit** `config/account.yaml` or `.env`
2. **Use demo accounts** for testing
3. **Enable 2FA** on all API accounts
4. **Review permissions** regularly
5. **Keep software updated**

---

## 🛠️ Technology Stack

| Component | Technology | License |
|-----------|-----------|---------|
| **Language** | Python 3.14 | PSF |
| **MT5 Connection** | MetaTrader5 | Free |
| **Web Dashboard** | FastAPI + HTMX + Tailwind | MIT |
| **Database** | SQLite (via Python stdlib) | Public Domain |
| **Video Analysis** | Google Gemini API | Free tier |
| **Speech-to-Text** | OpenAI Whisper | MIT |
| **Telegram** | Telethon | MIT |
| **Social Media** | Agent Reach (MIT) | MIT |
| **Risk Engine** | Custom (deterministic) | MIT |
| **Charts** | TradingView Lightweight Charts | Apache 2.0 |
| **Agent Framework** | Pydantic AI + LangGraph | MIT |

---

## 🗺️ Roadmap

### Phase 1: Foundation ✅
- [x] Project structure
- [x] Knowledge base (SQLite)
- [x] MT5 connector
- [x] Risk engine
- [x] Web dashboard
- [x] Telegram notifications

### Phase 2: Learning 🔄
- [ ] Video analysis with Gemini
- [ ] Instagram scraper integration
- [ ] Telegram channel reader
- [ ] Strategy extraction engine
- [ ] Backtesting engine

### Phase 3: Execution 🔜
- [ ] Trading engine
- [ ] Multi-strategy consensus
- [ ] Automated trade execution
- [ ] Session management

### Phase 4: Intelligence 🔜
- [ ] Self-evaluation loop
- [ ] Performance optimization
- [ ] News integration
- [ ] Economic calendar
- [ ] Sentiment analysis

### Phase 5: Scale 🔜
- [ ] Multi-broker support
- [ ] Cloud deployment option
- [ ] Advanced analytics
- [ ] Mobile app

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

### Development Setup

```bash
# Clone and setup
git clone https://github.com/houmannkeihanfar-sys/TradeBot
cd trading-bot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

---

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

**This software is for educational and research purposes only.**

- Trading involves substantial risk of loss
- Past performance does not guarantee future results
- Always use demo accounts for testing
- Never trade with money you cannot afford to lose
- The authors are not responsible for any financial losses

---

## 🙏 Acknowledgments

- [MetaTrader 5](https://www.metatrader5.com/) — Trading platform
- [Agent Reach](https://github.com/Panniantong/Agent-Reach) — Social media access
- [Google Gemini](https://ai.google.dev/) — Video understanding
- [OpenAI Whisper](https://github.com/openai/whisper) — Speech-to-text
- [FastAPI](https://fastapi.tiangolo.com/) — Web framework
- [TradingView](https://www.tradingview.com/) — Charting technology

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the [docs/](docs/) folder for detailed documentation

---

**Built with ❤️ for the trading community**
