"""
Trading Bot — نقطه ورود اصلی
"""

import sys
import os
import MetaTrader5 as mt5

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from connector.mt5_connector import MT5Connector
from risk.risk_engine import RiskEngine


def main():
    print("=" * 60)
    print("🤖 Trading Bot — شروع")
    print("=" * 60)
    
    # Initialize connector
    connector = MT5Connector()
    
    # Connect to MT5
    print("\n📡 اتصال به متاتریدر 5...")
    login = int(input("🔑 شماره حساب: ").strip())
    server = input("🌐 نام سرور (مثلاً AronMarkets-Demo): ").strip()
    password = input("🔑 رمز عبور: ").strip()
    
    if not connector.connect(login, password, server):
        print("❌ اتصال ناموفق!")
        return
    
    print("✅ اتصال موفق!")
    
    # Get account info
    account = connector.get_account_info()
    print(f"\n📊 اطلاعات حساب:")
    print(f"   حساب: {account['login']}")
    print(f"   نام: {account['name']}")
    print(f"   مانده: ${account['balance']:.2f}")
    print(f"   اکوئیتی: ${account['equity']:.2f}")
    print(f"   اهرم: 1:{account['leverage']}")
    
    # Get main symbols
    print(f"\n📈 نمادهای اصلی:")
    main_symbols = ['EURUSD.', 'GBPUSD.', 'USDJPY.', 'XAUUSD.']
    for sym in main_symbols:
        info = connector.get_symbol_info(sym)
        tick = connector.get_tick(sym)
        if info and tick:
            print(f"   {sym:12} | Bid: {tick['bid']:10.5f} | Spread: {tick['spread']}")
    
    # Get current positions
    positions = connector.get_positions()
    print(f"\n📋 پوزیشن‌های باز: {len(positions)}")
    
    # Initialize risk engine
    risk = RiskEngine()
    optimal = risk.calculate_optimal_risk(account['balance'])
    print(f"\n⚠️ Risk Defaults (بر اساس مانده ${account['balance']:.2f}):")
    print(f"   ریسک هر ترید: {optimal['risk_per_trade']}%")
    print(f"   حداکثر پوزیشن: {optimal['max_open_trades']}")
    print(f"   حداقل RR: {optimal['min_rr_ratio']}")
    print(f"   حداکثر دراوداون: {optimal['max_drawdown']}%")
    
    # Demo trade
    print("\n" + "=" * 60)
    print("📝 آیا می‌خواهید یک ترید دمو انجام دهید؟")
    print("   (فقط برای تست اتصال)")
    choice = input("   بله/خیر: ").strip().lower()
    
    if choice in ['بله', 'yes', 'y']:
        print("\n🟢 باز کردن BUY EURUSD 0.01...")
        ticket = connector.open_position(
            symbol="EURUSD.",
            order_type="BUY",
            volume=0.01,
            comment="Trading Bot Test"
        )
        if ticket:
            print(f"✅ پوزیشن باز شد! Ticket: {ticket}")
            positions = connector.get_positions()
            for p in positions:
                print(f"   {p['type']} {p['symbol']} {p['volume']} @ {p['price_open']}")
        else:
            print("❌ خطا در باز کردن پوزیشن")
    
    # Start panel
    print("\n" + "=" * 60)
    print("🌐 راه‌اندازی پنل وب...")
    print("   http://localhost:5000")
    print("   (Ctrl+C برای خروج)")
    print("=" * 60)
    
    # Run FastAPI
    import uvicorn
    from src.panel.app import app, MT5_CONNECTED
    
    # Set connected state
    import src.panel.app as panel_app
    panel_app.MT5_CONNECTED = True
    
    uvicorn.run(app, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
