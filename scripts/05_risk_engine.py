"""
05 - Risk Engine
محاسبات مدیریت ریسک - حجم پوزیشن، دراوداون، ریسک
نحوه اجرا: python scripts/05_risk_engine.py <command> [args]
"""
import json
import sys
from pathlib import Path


class RiskEngine:
    """موتور مدیریت ریسک"""
    
    def __init__(self, balance=10000, risk_percent=1.0, max_drawdown=20.0):
        self.balance = balance
        self.risk_percent = risk_percent
        self.max_drawdown = max_drawdown
        self.initial_balance = balance
    
    def calculate_lot_size(self, entry_price, stop_loss, symbol_info=None):
        """محاسبه حجم پوزیشن بر اساس ریسک"""
        if stop_loss == 0 or entry_price == 0:
            return 0.01
        
        sl_distance = abs(entry_price - stop_loss)
        risk_amount = self.balance * self.risk_percent / 100.0
        
        # Default contract size for forex
        contract_size = 100000
        point_value = 0.0001
        
        if symbol_info:
            contract_size = symbol_info.get("contract_size", 100000)
            point_value = symbol_info.get("point", 0.0001)
        
        # Calculate lots
        risk_per_lot = sl_distance * contract_size
        if risk_per_lot == 0:
            return 0.01
        
        lots = risk_amount / risk_per_lot
        
        # Normalize
        lots = max(0.01, round(lots, 2))
        
        return lots
    
    def calculate_sl_tp(self, entry_price, direction, sl_pips, tp_pips, point=0.0001):
        """محاسبه حد ضرر و سود"""
        if direction == "BUY":
            sl = entry_price - (sl_pips * point)
            tp = entry_price + (tp_pips * point)
        else:
            sl = entry_price + (sl_pips * point)
            tp = entry_price - (tp_pips * point)
        
        return round(sl, 5), round(tp, 5)
    
    def check_drawdown(self, current_balance):
        """بررسی دراوداون"""
        drawdown = ((self.initial_balance - current_balance) / self.initial_balance) * 100
        
        if drawdown >= self.max_drawdown:
            return {"allowed": False, "drawdown": drawdown, "message": "Max drawdown reached!"}
        
        return {"allowed": True, "drawdown": drawdown, "message": f"Drawdown: {drawdown:.1f}%"}
    
    def position_sizing(self, entry, sl, tp, account_balance=None):
        """محاسبه کامل حجم و ریسک"""
        balance = account_balance or self.balance
        
        sl_distance = abs(entry - sl)
        tp_distance = abs(tp - entry)
        
        risk_amount = balance * self.risk_percent / 100.0
        lots = self.calculate_lot_size(entry, sl)
        
        # Risk to Reward ratio
        rr_ratio = tp_distance / sl_distance if sl_distance > 0 else 0
        
        return {
            "lots": lots,
            "sl_distance_pips": round(sl_distance * 10000, 1),
            "tp_distance_pips": round(tp_distance * 10000, 1),
            "risk_amount": round(risk_amount, 2),
            "rr_ratio": round(rr_ratio, 2),
            "risk_percent": self.risk_percent,
        }


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/05_risk_engine.py calculate <entry> <sl> <tp> [balance]")
        print("  python scripts/05_risk_engine.py check_drawdown <current_balance> [initial]")
        print("  python scripts/05_risk_engine.py kelly <win_rate> <avg_win> <avg_loss>")
        sys.exit(1)
    
    command = sys.argv[1]
    engine = RiskEngine()
    
    if command == "calculate":
        if len(sys.argv) < 5:
            print("Usage: python scripts/05_risk_engine.py calculate <entry> <sl> <tp> [balance]")
            sys.exit(1)
        
        entry = float(sys.argv[2])
        sl = float(sys.argv[3])
        tp = float(sys.argv[4])
        balance = float(sys.argv[5]) if len(sys.argv) > 5 else 10000
        
        engine.balance = balance
        result = engine.position_sizing(entry, sl, tp)
        print(json.dumps(result, indent=2))
    
    elif command == "check_drawdown":
        current = float(sys.argv[2])
        initial = float(sys.argv[3]) if len(sys.argv) > 3 else 10000
        engine.initial_balance = initial
        result = engine.check_drawdown(current)
        print(json.dumps(result, indent=2))
    
    elif command == "kelly":
        if len(sys.argv) < 5:
            print("Usage: python scripts/05_risk_engine.py kelly <win_rate> <avg_win> <avg_loss>")
            sys.exit(1)
        
        win_rate = float(sys.argv[2]) / 100
        avg_win = float(sys.argv[3])
        avg_loss = float(sys.argv[4])
        
        # Kelly Criterion
        if avg_loss == 0:
            print("Avg loss cannot be zero")
            sys.exit(1)
        
        b = avg_win / avg_loss
        kelly = (win_rate * b - (1 - win_rate)) / b
        half_kelly = kelly / 2
        
        result = {
            "kelly_percent": round(kelly * 100, 2),
            "half_kelly_percent": round(half_kelly * 100, 2),
            "recommendation": f"Use {round(half_kelly * 100, 2)}% (half Kelly for safety)",
        }
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
