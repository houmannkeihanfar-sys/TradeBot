"""
Panel — داشبورد وب محلی
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import MetaTrader5 as mt5
from datetime import datetime

app = FastAPI(title="Trading Bot Panel")
templates = Jinja2Templates(directory="templates")

# MT5 connection
MT5_CONNECTED = False


def get_mt5_data():
    """دریافت داده‌ها از MT5"""
    if not MT5_CONNECTED:
        return None
    
    account = mt5.account_info()
    positions = mt5.positions_get()
    symbol = mt5.symbol_info("EURUSD.")
    tick = mt5.symbol_info_tick("EURUSD.")
    
    return {
        "account": {
            "login": account.login if account else 0,
            "balance": account.balance if account else 0,
            "equity": account.equity if account else 0,
            "margin": account.margin if account else 0,
            "margin_free": account.margin_free if account else 0,
            "profit": account.profit if account else 0,
            "leverage": account.leverage if account else 0,
        },
        "positions": [
            {
                "ticket": p.ticket,
                "symbol": p.symbol,
                "type": "BUY" if p.type == 0 else "SELL",
                "volume": p.volume,
                "price_open": p.price_open,
                "sl": p.sl,
                "tp": p.tp,
                "profit": p.profit,
            }
            for p in (positions or [])
        ],
        "price": {
            "bid": tick.bid if tick else 0,
            "ask": tick.ask if tick else 0,
            "spread": symbol.spread if symbol else 0,
        } if tick and symbol else None,
    }


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """داشبورد اصلی"""
    data = get_mt5_data()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "data": data,
        "connected": MT5_CONNECTED,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })


@app.get("/api/account")
async def api_account():
    """API: اطلاعات حساب"""
    data = get_mt5_data()
    if data is None:
        return {"error": "MT5 not connected"}
    return data["account"]


@app.get("/api/positions")
async def api_positions():
    """API: پوزیشن‌های باز"""
    data = get_mt5_data()
    if data is None:
        return {"error": "MT5 not connected"}
    return data["positions"]


@app.post("/connect")
async def connect_mt5(login: int, password: str, server: str):
    """اتصال به MT5"""
    global MT5_CONNECTED
    if not mt5.initialize():
        return {"error": "MT5 initialize failed"}
    if not mt5.login(login, password=password, server=server):
        return {"error": "Login failed"}
    MT5_CONNECTED = True
    return {"status": "connected"}
