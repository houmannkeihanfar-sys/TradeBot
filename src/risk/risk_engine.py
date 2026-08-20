"""
Risk Engine — محاسبه حجم و ریسک (100% Deterministic)
"""


class RiskEngine:
    def __init__(self):
        # Smart Defaults
        self.risk_per_trade = 1.0      # درصد
        self.risk_per_day = 3.0        # درصد
        self.risk_per_week = 6.0       # درصد
        self.max_drawdown = 15.0       # درصد
        self.min_rr_ratio = 2.0        # Risk:Reward
        self.max_open_trades = 3
        self.max_correlated = 2
    
    def calculate_position_size(self, account_balance: float, risk_percent: float,
                                 stop_loss_pips: float, pip_value: float = 10.0) -> float:
        """محاسبه حجم پوزیشن (lot)"""
        if stop_loss_pips <= 0 or pip_value <= 0:
            return 0.0
        
        risk_amount = account_balance * (risk_percent / 100)
        lot_size = risk_amount / (stop_loss_pips * pip_value)
        return round(lot_size, 2)
    
    def kelly_fraction(self, win_rate: float, reward_risk_ratio: float) -> float:
        """محاسبه Kelly Criterion (Half Kelly = safer)"""
        if reward_risk_ratio <= 0:
            return 0.0
        kelly = win_rate - (1 - win_rate) / reward_risk_ratio
        return max(0, kelly * 0.5)  # Half Kelly
    
    def calculate_optimal_risk(self, balance: float) -> dict:
        """Smart defaults بر اساس اندازه حساب"""
        if balance < 500:
            return {
                "risk_per_trade": 0.5,
                "max_open_trades": 1,
                "min_rr_ratio": 2.5,
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
                "risk_per_trade": 0.75,
                "max_open_trades": 5,
                "min_rr_ratio": 2.0,
                "max_drawdown": 10,
            }
    
    def calculate_rr(self, entry: float, stop_loss: float, take_profit: float) -> float:
        """محاسبه Risk:Reward ratio"""
        risk = abs(entry - stop_loss)
        reward = abs(take_profit - entry)
        if risk == 0:
            return 0.0
        return round(reward / risk, 2)
    
    def check_daily_risk(self, daily_loss: float, account_balance: float) -> bool:
        """بررسی ریسک روزانه"""
        daily_risk = abs(daily_loss) / account_balance * 100
        return daily_risk < self.risk_per_day
    
    def check_max_drawdown(self, peak_balance: float, current_equity: float) -> bool:
        """بررسی حداکثر دراوداون"""
        if peak_balance == 0:
            return True
        drawdown = (peak_balance - current_equity) / peak_balance * 100
        return drawdown < self.max_drawdown
    
    def can_open_trade(self, open_trades: int, balance: float) -> bool:
        """آیا می‌توان پوزیشن جدید باز کرد؟"""
        optimal = self.calculate_optimal_risk(balance)
        return open_trades < optimal["max_open_trades"]
