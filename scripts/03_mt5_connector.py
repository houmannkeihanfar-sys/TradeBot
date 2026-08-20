"""
03 - MT5 Connector (EA-Based)
اتصال به MT5 از طریق Expert Advisor - بدون ذخیره رمز
نحوه اجرا: python scripts/03_mt5_connector.py <command> [args]
"""
import sys
import json
from datetime import datetime
from pathlib import Path

try:
    import MetaTrader5 as mt5
except ImportError:
    print("MetaTrader5 not installed. Run: pip install MetaTrader5")
    sys.exit(1)

def connect():
    """اتصال به MT5 (فقط initialize - نیاز به login جداگانه نداره)"""
    if not mt5.initialize():
        error = mt5.last_error()
        print(f"MT5 initialize failed: {error}")
        return False
    print(f"MT5 connected: {mt5.terminal_info().name}")
    return True

def get_account():
    """دریافت اطلاعات حساب"""
    info = mt5.account_info()
    if info is None:
        return {"error": "Not connected"}
    return {
        "login": info.login,
        "name": info.name,
        "server": info.server,
        "balance": info.balance,
        "equity": info.equity,
        "margin": info.margin,
        "margin_free": info.margin_free,
        "margin_level": info.margin_level,
        "leverage": info.leverage,
        "currency": info.currency,
        "profit": info.profit,
    }

def get_positions():
    """پوزیشن‌های باز"""
    positions = mt5.positions_get()
    if positions is None:
        return []
    return [{
        "ticket": p.ticket,
        "symbol": p.symbol,
        "type": "BUY" if p.type == mt5.ORDER_TYPE_BUY else "SELL",
        "volume": p.volume,
        "price_open": p.price_open,
        "price_current": p.price_current,
        "sl": p.sl,
        "tp": p.tp,
        "profit": p.profit,
        "swap": p.swap,
        "time": datetime.fromtimestamp(p.time).isoformat(),
    } for p in positions]

def get_rates(symbol, timeframe, count=100):
    """داده‌های OHLCV"""
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None:
        return []
    return [{
        "time": datetime.fromtimestamp(r["time"]).isoformat(),
        "open": r["open"],
        "high": r["high"],
        "low": r["low"],
        "close": r["close"],
        "volume": r["tick_volume"],
    } for r in rates]

def get_symbol_info(symbol):
    """اطلاعات نماد"""
    info = mt5.symbol_info(symbol)
    if info is None:
        return None
    return {
        "name": info.name,
        "digits": info.digits,
        "spread": info.spread,
        "point": info.point,
        "lot_min": info.volume_min,
        "lot_max": info.volume_max,
        "lot_step": info.volume_step,
        "trade_mode": info.trade_mode,
        "contract_size": info.trade_contract_size,
    }

def open_position(symbol, order_type, volume, sl=0, tp=0, comment=""):
    """باز کردن پوزیشن"""
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        return {"error": "No tick data"}
    
    price = tick.ask if order_type == "BUY" else tick.bid
    type_mt5 = mt5.ORDER_TYPE_BUY if order_type == "BUY" else mt5.ORDER_TYPE_SELL
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": type_mt5,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 20260819,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(request)
    if result is None:
        return {"error": "Order send failed"}
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return {"error": result.comment}
    return {"success": True, "order": result.order}

def close_position(ticket):
    """بستن پوزیشن"""
    position = mt5.positions_get(ticket=ticket)
    if not position:
        return {"error": "Position not found"}
    position = position[0]
    
    tick = mt5.symbol_info_tick(position.symbol)
    if tick is None:
        return {"error": "No tick data"}
    
    price = tick.bid if position.type == mt5.ORDER_TYPE_BUY else tick.ask
    type_close = mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": position.symbol,
        "volume": position.volume,
        "type": type_close,
        "position": ticket,
        "price": price,
        "deviation": 20,
        "magic": 20260819,
        "comment": "close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(request)
    if result and result.retcode == mt5.TRADE_RETCODE_DONE:
        return {"success": True}
    return {"error": result.comment if result else "Failed"}

def save_results(data, filename):
    """ذخیره نتایج در فایل"""
    output_dir = Path("data/mt5")
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {filepath}")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/03_mt5_connector.py connect")
        print("  python scripts/03_mt5_connector.py account")
        print("  python scripts/03_mt5_connector.py positions")
        print("  python scripts/03_mt5_connector.py rates <symbol> [timeframe] [count]")
        print("  python scripts/03_mt5_connector.py symbol <symbol>")
        print("  python scripts/03_mt5_connector.py buy <symbol> <volume> [sl] [tp]")
        print("  python scripts/03_mt5_connector.py sell <symbol> <volume> [sl] [tp]")
        print("  python scripts/03_mt5_connector.py close <ticket>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "connect":
        if connect():
            save_results(get_account(), "account_info.json")
    
    elif command == "account":
        if connect():
            data = get_account()
            print(json.dumps(data, indent=2))
            save_results(data, "account_info.json")
    
    elif command == "positions":
        if connect():
            data = get_positions()
            print(json.dumps(data, indent=2))
            save_results(data, "positions.json")
    
    elif command == "rates":
        if len(sys.argv) < 3:
            print("Usage: python scripts/03_mt5_connector.py rates <symbol> [timeframe] [count]")
            sys.exit(1)
        symbol = sys.argv[2]
        tf_map = {"M1": 1, "M5": 5, "M15": 15, "M30": 30, "H1": 16385, "H4": 16388, "D1": 16408}
        tf = tf_map.get(sys.argv[3] if len(sys.argv) > 3 else "H1", 16385)
        count = int(sys.argv[4]) if len(sys.argv) > 4 else 100
        if connect():
            data = get_rates(symbol, tf, count)
            save_results(data, f"rates_{symbol}.json")
    
    elif command == "symbol":
        if len(sys.argv) < 3:
            print("Usage: python scripts/03_mt5_connector.py symbol <symbol>")
            sys.exit(1)
        if connect():
            data = get_symbol_info(sys.argv[2])
            print(json.dumps(data, indent=2))
    
    elif command in ("buy", "sell"):
        if len(sys.argv) < 4:
            print(f"Usage: python scripts/03_mt5_connector.py {command} <symbol> <volume> [sl] [tp]")
            sys.exit(1)
        symbol = sys.argv[2]
        volume = float(sys.argv[3])
        sl = float(sys.argv[4]) if len(sys.argv) > 4 else 0
        tp = float(sys.argv[5]) if len(sys.argv) > 5 else 0
        if connect():
            order_type = "BUY" if command == "buy" else "SELL"
            result = open_position(symbol, order_type, volume, sl, tp, "auto")
            print(json.dumps(result, indent=2))
    
    elif command == "close":
        if len(sys.argv) < 3:
            print("Usage: python scripts/03_mt5_connector.py close <ticket>")
            sys.exit(1)
        if connect():
            result = close_position(int(sys.argv[2]))
            print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")
    
    mt5.shutdown()

if __name__ == "__main__":
    main()
