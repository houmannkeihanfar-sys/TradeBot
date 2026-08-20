"""
Trading Bot - Knowledge Base (SQLite)
Stores all learned strategies, sources, decisions, broker rules, etc.
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config.settings import DB_PATH


def get_db():
    """Get database connection."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Initialize all tables."""
    conn = get_db()
    c = conn.cursor()

    # === STRATEGIES ===
    c.execute("""
    CREATE TABLE IF NOT EXISTS strategies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        source TEXT,
        source_url TEXT,
        timeframe TEXT,
        market TEXT,
        description TEXT,
        rules_json TEXT,
        indicators_json TEXT,
        win_rate REAL,
        risk_reward REAL,
        max_drawdown_pct REAL,
        backtest_trades INTEGER,
        backtest_profit_pct REAL,
        confidence REAL DEFAULT 0.5,
        status TEXT DEFAULT 'new',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # === SOURCES ===
    c.execute("""
    CREATE TABLE IF NOT EXISTS sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT,
        url TEXT,
        platform TEXT,
        credibility_score REAL DEFAULT 0.5,
        last_checked TIMESTAMP,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # === BROKERS ===
    c.execute("""
    CREATE TABLE IF NOT EXISTS brokers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        website TEXT,
        regulation TEXT,
        min_deposit REAL,
        max_leverage TEXT,
        spread_type TEXT,
        commission TEXT,
        swap_free INTEGER DEFAULT 0,
        bonus_info TEXT,
        pros TEXT,
        cons TEXT,
        rating REAL,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # === BROKER RULES (per account type) ===
    c.execute("""
    CREATE TABLE IF NOT EXISTS broker_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        broker_id INTEGER,
        account_type TEXT,
        min_lot REAL,
        max_lot REAL,
        max_concurrent_trades INTEGER,
        max_lot_size REAL,
        margin_call_pct REAL,
        stop_out_pct REAL,
        allowed_symbols TEXT,
        trading_hours TEXT,
        notes TEXT,
        FOREIGN KEY (broker_id) REFERENCES brokers(id)
    )""")

    # === ACCOUNTS ===
    c.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        broker_id INTEGER,
        account_number TEXT,
        server TEXT,
        account_type TEXT,
        balance REAL,
        equity REAL,
        margin REAL,
        free_margin REAL,
        leverage TEXT,
        currency TEXT,
        bonus_amount REAL DEFAULT 0,
        bonus_conditions TEXT,
        last_synced TIMESTAMP,
        FOREIGN KEY (broker_id) REFERENCES brokers(id)
    )""")

    # === TRADES ===
    c.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        strategy_id INTEGER,
        symbol TEXT,
        trade_type TEXT,
        volume REAL,
        open_price REAL,
        close_price REAL,
        stop_loss REAL,
        take_profit REAL,
        profit REAL,
        commission REAL,
        swap REAL,
        open_time TIMESTAMP,
        close_time TIMESTAMP,
        status TEXT DEFAULT 'open',
        confidence_pct REAL,
        strategies_used TEXT,
        notes TEXT,
        FOREIGN KEY (account_id) REFERENCES accounts(id),
        FOREIGN KEY (strategy_id) REFERENCES strategies(id)
    )""")

    # === BACKTESTS ===
    c.execute("""
    CREATE TABLE IF NOT EXISTS backtests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        strategy_id INTEGER,
        symbol TEXT,
        timeframe TEXT,
        start_date TEXT,
        end_date TEXT,
        total_trades INTEGER,
        winning_trades INTEGER,
        losing_trades INTEGER,
        win_rate REAL,
        profit_factor REAL,
        max_drawdown_pct REAL,
        sharpe_ratio REAL,
        net_profit REAL,
        avg_win REAL,
        avg_loss REAL,
        details_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (strategy_id) REFERENCES strategies(id)
    )""")

    # === NEWS & EVENTS ===
    c.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        source TEXT,
        url TEXT,
        impact TEXT,
        currency TEXT,
        event_time TIMESTAMP,
        summary TEXT,
        market_reaction TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # === CONCEPTS (learned terms) ===
    c.execute("""
    CREATE TABLE IF NOT EXISTS concepts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        term TEXT NOT NULL,
        definition TEXT,
        category TEXT,
        source TEXT,
        related_strategies TEXT,
        examples TEXT,
        verified INTEGER DEFAULT 0,
        confidence REAL DEFAULT 0.5,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # === LESSONS LEARNED ===
    c.execute("""
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        title TEXT,
        description TEXT,
        source_trade_id INTEGER,
        impact TEXT,
        action_required TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (source_trade_id) REFERENCES trades(id)
    )""")

    # === DECISIONS ===
    c.execute("""
    CREATE TABLE IF NOT EXISTS decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        context TEXT,
        decision TEXT,
        reasoning TEXT,
        result TEXT,
        was_correct INTEGER,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # === USER PREFERENCES ===
    c.execute("""
    CREATE TABLE IF NOT EXISTS user_preferences (
        key TEXT PRIMARY KEY,
        value TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # === PERMISSIONS ===
    c.execute("""
    CREATE TABLE IF NOT EXISTS permissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT,
        status TEXT DEFAULT 'pending',
        reason TEXT,
        granted_at TIMESTAMP,
        expires_at TIMESTAMP
    )""")

    # === SOURCES TO SCRAPE (dynamic) ===
    c.execute("""
    CREATE TABLE IF NOT EXISTS scrape_targets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT,
        url TEXT,
        username TEXT,
        category TEXT,
        priority INTEGER DEFAULT 5,
        last_scraped TIMESTAMP,
        active INTEGER DEFAULT 1,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    conn.commit()
    conn.close()
    print("Knowledge Base initialized successfully.")


# === Helper Functions ===

def add_strategy(name, source=None, source_url=None, timeframe=None, market=None,
                 description=None, rules=None, indicators=None):
    """Add a new strategy to the knowledge base."""
    conn = get_db()
    conn.execute("""
        INSERT INTO strategies (name, source, source_url, timeframe, market,
                              description, rules_json, indicators_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, source, source_url, timeframe, market, description,
          json.dumps(rules) if rules else None,
          json.dumps(indicators) if indicators else None))
    conn.commit()
    strategy_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return strategy_id


def add_source(name, source_type=None, url=None, platform=None, credibility=0.5):
    """Add a new knowledge source."""
    conn = get_db()
    conn.execute("""
        INSERT INTO sources (name, type, url, platform, credibility_score)
        VALUES (?, ?, ?, ?, ?)
    """, (name, source_type, url, platform, credibility))
    conn.commit()
    conn.close()


def add_broker(name, **kwargs):
    """Add broker info."""
    conn = get_db()
    cols = ["name"] + list(kwargs.keys())
    vals = [name] + list(kwargs.values())
    placeholders = ", ".join(["?"] * len(vals))
    col_names = ", ".join(cols)
    conn.execute(f"INSERT INTO brokers ({col_names}) VALUES ({placeholders})", vals)
    conn.commit()
    conn.close()


def add_concept(term, definition=None, category=None, source=None):
    """Add a learned concept."""
    conn = get_db()
    conn.execute("""
        INSERT INTO concepts (term, definition, category, source)
        VALUES (?, ?, ?, ?)
    """, (term, definition, category, source))
    conn.commit()
    conn.close()


def add_news(title, source=None, url=None, impact=None, currency=None,
             event_time=None, summary=None):
    """Add news item."""
    conn = get_db()
    conn.execute("""
        INSERT INTO news (title, source, url, impact, currency, event_time, summary)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, source, url, impact, currency, event_time, summary))
    conn.commit()
    conn.close()


def search_strategies(market=None, timeframe=None, min_confidence=None):
    """Search strategies with filters."""
    conn = get_db()
    query = "SELECT * FROM strategies WHERE 1=1"
    params = []
    if market:
        query += " AND market = ?"
        params.append(market)
    if timeframe:
        query += " AND timeframe = ?"
        params.append(timeframe)
    if min_confidence:
        query += " AND confidence >= ?"
        params.append(min_confidence)
    results = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in results]


if __name__ == "__main__":
    init_db()
