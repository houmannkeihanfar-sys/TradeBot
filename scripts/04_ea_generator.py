"""
04 - EA Generator
تولید Expert Advisor برای MetaTrader 5
نحوه اجرا: python scripts/04_ea_generator.py <strategy_name>
"""
import json
import sys
from pathlib import Path
from datetime import datetime


def generate_ea(strategy_config):
    """تولید کد MQL5 Expert Advisor"""
    
    name = strategy_config.get("name", "TradingBot")
    magic = strategy_config.get("magic", 20260819)
    risk_percent = strategy_config.get("risk_percent", 1.0)
    max_positions = strategy_config.get("max_positions", 3)
    timeframes = strategy_config.get("timeframes", ["H1"])
    symbols = strategy_config.get("symbols", ["XAUUSD"])
    
    # Generate entry conditions
    entry_conditions = strategy_config.get("entry_conditions", [])
    entry_code = "\n".join([f"      // {c}" for c in entry_conditions])
    
    # Generate exit conditions
    exit_conditions = strategy_config.get("exit_conditions", [])
    exit_code = "\n".join([f"      // {c}" for c in exit_conditions])
    
    ea_code = f'''//+------------------------------------------------------------------+
//|                                          {name}.mq5
//|                                          Trading Bot EA
//|                                          Generated: {datetime.now().isoformat()}
//+------------------------------------------------------------------+
#property copyright "Trading Bot"
#property link      ""
#property version   "1.00"
#property strict

#include <Trade\\Trade.mqh>

input double RiskPercent = {risk_percent};      // Risk per trade (%)
input int    MaxPositions = {max_positions};     // Max open positions
input int    MagicNumber = {magic};             // Magic number
input int    Slippage = 20;                     // Slippage points

CTrade trade;
int totalSignals = 0;
int totalTrades = 0;

//+------------------------------------------------------------------+
//| Expert initialization function                                     |
//+------------------------------------------------------------------+
int OnInit()
{{
   trade.SetExpertMagicNumber(MagicNumber);
   trade.SetDeviationInPoints(Slippage);
   
   Print("{name} initialized. Risk: ", RiskPercent, "%, Max Positions: ", MaxPositions);
   
   // Save init to file
   SaveToFile("init", "EA Started: " + TimeToString(TimeCurrent()));
   
   return(INIT_SUCCEEDED);
}}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                   |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{{
   Print("{name} deinitialized. Reason: ", reason);
}}

//+------------------------------------------------------------------+
//| Calculate position size based on risk                              |
//+------------------------------------------------------------------+
double CalculateLotSize(double slDistance)
{{
   double accountBalance = AccountInfoDouble(ACCOUNT_BALANCE);
   double riskAmount = accountBalance * RiskPercent / 100.0;
   
   double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   double lotStep = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double maxLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   
   if(tickValue == 0 || tickSize == 0 || slDistance == 0)
      return minLot;
   
   double lots = riskAmount / (slDistance / tickSize * tickValue);
   
   // Normalize to lot step
   lots = MathFloor(lots / lotStep) * lotStep;
   lots = MathMax(lots, minLot);
   lots = MathMin(lots, maxLot);
   
   return NormalizeDouble(lots, 2);
}}

//+------------------------------------------------------------------+
//| Count current open positions                                       |
//+------------------------------------------------------------------+
int CountPositions()
{{
   int count = 0;
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {{
      if(PositionGetSymbol(i) == _Symbol)
         if(PositionGetInteger(POSITION_MAGIC) == MagicNumber)
            count++;
   }}
   return count;
}}

//+------------------------------------------------------------------+
//| Save results to file for panel                                     |
//+------------------------------------------------------------------+
void SaveToFile(string type, string data)
{{
   string filename = "trading_results.json";
   
   // Read existing data
   string existing = "";
   int handle = FileOpen(filename, FILE_READ | FILE_TXT | FILE_ANSI | FILE_COMMON);
   if(handle != INVALID_HANDLE)
   {{
      while(!FileIsEnding(handle))
         existing += FileReadString(handle);
      FileClose(handle);
   }}
   
   // Write new data
   handle = FileOpen(filename, FILE_WRITE | FILE_TXT | FILE_ANSI | FILE_COMMON);
   if(handle != INVALID_HANDLE)
   {{
      FileWriteString(handle, data);
      FileClose(handle);
   }}
}}

//+------------------------------------------------------------------+
//| Expert tick function                                              |
//+------------------------------------------------------------------+
void OnTick()
{{
   // Check if we have room for more positions
   if(CountPositions() >= MaxPositions)
      return;
   
   // ============================================
   // STRATEGY LOGIC GOES HERE
   // ============================================
   
   // Entry conditions:
{entry_code}
   
   // Exit conditions:
{exit_code}
   
   // Example: Save signal to file
   // SaveToFile("signal", "Signal: BUY " + _Symbol + " at " + DoubleToString(_Ask, _Digits));
}}

//+------------------------------------------------------------------+
//| Get current spread                                                |
//+------------------------------------------------------------------+
int GetSpread()
{{
   return (int)SymbolInfoInteger(_Symbol, SYMBOL_SPREAD);
}}

//+------------------------------------------------------------------+
//| Check if trading is allowed                                       |
//+------------------------------------------------------------------+
bool IsTradeAllowed()
{{
   if(!TerminalInfoInteger(TERMINAL_TRADE_ALLOWED))
      return false;
   if(!MQLInfoInteger(MQL_TRADE_ALLOWED))
      return false;
   return true;
}}
'''
    return ea_code


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/04_ea_generator.py <strategy_config.json>")
        print("Example: python scripts/04_ea_generator.py strategies/ict_strategy.json")
        sys.exit(1)
    
    config_path = sys.argv[1]
    
    if not Path(config_path).exists():
        print(f"Config not found: {config_path}")
        sys.exit(1)
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # Generate EA
    ea_code = generate_ea(config)
    
    # Save EA file
    output_dir = Path("ea")
    output_dir.mkdir(exist_ok=True)
    
    ea_name = config.get("name", "TradingBot")
    ea_path = output_dir / f"{ea_name}.mq5"
    
    with open(ea_path, "w", encoding="utf-8") as f:
        f.write(ea_code)
    
    print(f"EA generated: {ea_path}")
    print(f"Copy to MT5: MQL5/Experts/{ea_name}.mq5")
    print(f"Then compile in MetaEditor and attach to chart.")


if __name__ == "__main__":
    main()
