"""
Trading Bot - Configuration
"""
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "knowledge.db"
STRATEGIES_DIR = DATA_DIR / "strategies"
BACKTESTS_DIR = DATA_DIR / "backtests"
TRADES_DIR = DATA_DIR / "trades"

# Create directories
for d in [DATA_DIR, STRATEGIES_DIR, BACKTESTS_DIR, TRADES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# MT5 Config
MT5_CONFIG = {
    "server": "AronMarkets-Demo",
    "login": None,  # Set via env or panel
    "password": None,  # Set via env or panel
    "timeout": 10000,
}

# Risk Management Defaults
RISK_DEFAULTS = {
    "max_risk_per_trade_pct": 2.0,
    "max_daily_drawdown_pct": 5.0,
    "max_total_drawdown_pct": 10.0,
    "max_concurrent_trades": 5,
    "risk_reward_minimum": 1.5,
}

# Telegram Config
TELEGRAM_CONFIG = {
    "bot_token": None,  # Set via env
    "chat_id": None,  # Set via env
}

# Trading Hours (UTC)
TRADING_SESSIONS = {
    "asian": {"start": 0, "end": 8},
    "london": {"start": 7, "end": 16},
    "new_york": {"start": 13, "end": 22},
    "overlap": {"start": 13, "end": 16},  # London + NY overlap
}

# AI/LLM Config
AI_CONFIG = {
    "use_free_models": True,
    "preferred_providers": ["ollama", "groq", "huggingface"],
    "max_tokens_per_query": 4096,
    "cache_enabled": True,
}
