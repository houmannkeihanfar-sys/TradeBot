"""
MT5 Connector — اتصال به متاتریدر 5
"""

import MetaTrader5 as mt5
from datetime import datetime
from typing import Optional, List, Dict, Any


class MT5Connector:
    def __init__(self):
        self.connected = False
        self.login = None
        self.password = None
        self.server = None
    
    def connect(self, login: int, password: str, server: str) -> bool:
        """اتصال به MT5"""
        if not mt5.initialize():
            error = mt5.last_error()
            print(f"MT5 initialize failed: {error}")
            return False
        
        authorized = mt5.login(login, password=password, server=server)
        if not authorized:
            error = mt5.last_error()
            print(f"MT5 login failed: {error}")
            mt5.shutdown()
            return False
        
        self.connected = True
        self.login = login
        self.password = password
        self.server = server
        return True
    
    def disconnect(self):
        """قطع اتصال"""
        mt5.shutdown()
        self.connected = False
    
    def get_account_info(self) -> Dict[str, Any]:
        """اطلاعات حساب"""
        info = mt5.account_info()
        if info is None:
            return {}
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
            "company": info.company,
            "profit": info.profit,
        }
    
    def get_symbol_info(self, symbol: str) -> Optional[Dict[str, Any]]:
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
    
    def get_tick(self, symbol: str) -> Optional[Dict[str, float]]:
        """قیمت لحظه‌ای"""
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return None
        return {
            "bid": tick.bid,
            "ask": tick.ask,
            "spread": round((tick.ask - tick.bid) / mt5.symbol_info(symbol).point),
        }
    
    def get_rates(self, symbol: str, timeframe: int, count: int = 100) -> List[Dict]:
        """داده‌های OHLCV"""
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
        if rates is None:
            return []
        return [
            {
                "time": datetime.fromtimestamp(r["time"]),
                "open": r["open"],
                "high": r["high"],
                "low": r["low"],
                "close": r["close"],
                "volume": r["tick_volume"],
            }
            for r in rates
        ]
    
    def get_positions(self) -> List[Dict[str, Any]]:
        """پوزیشن‌های باز"""
        positions = mt5.positions_get()
        if positions is None:
            return []
        return [
            {
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
                "time": datetime.fromtimestamp(p.time),
            }
            for p in positions
        ]
    
    def open_position(self, symbol: str, order_type: str, volume: float,
                      sl: float = 0, tp: float = 0, comment: str = "") -> Optional[int]:
        """باز کردن پوزیشن"""
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return None
        
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
            "magic": 20260818,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        result = mt5.order_send(request)
        if result is None:
            return None
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Order failed: {result.comment}")
            return None
        return result.order
    
    def close_position(self, ticket: int) -> bool:
        """بستن پوزیشن"""
        position = mt5.positions_get(ticket=ticket)
        if not position:
            return False
        position = position[0]
        
        tick = mt5.symbol_info_tick(position.symbol)
        if tick is None:
            return False
        
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
            "magic": 20260818,
            "comment": "close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        result = mt5.order_send(request)
        return result is not None and result.retcode == mt5.TRADE_RETCODE_DONE
    
    def get_all_symbols(self) -> List[str]:
        """لیست همه نمادها"""
        symbols = mt5.symbols_get()
        if symbols is None:
            return []
        return [s.name for s in symbols]
