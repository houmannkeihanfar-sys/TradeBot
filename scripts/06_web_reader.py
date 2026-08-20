"""
06 - Web Reader
خواندن و تحلیل محتوای وب
نحوه اجرا: python scripts/06_web_reader.py <url>
"""
import json
import sys
import requests
from pathlib import Path


def read_url(url):
    """خواندن محتوای صفحه با Jina Reader"""
    jina_url = f"https://r.jina.ai/{url}"
    
    headers = {
        "Accept": "text/plain",
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        response = requests.get(jina_url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.text
        else:
            return f"Error: HTTP {response.status_code}"
    except Exception as e:
        return f"Error: {e}"


def analyze_trading_content(text):
    """تحلیل محتوای مالی/ترید"""
    keywords = {
        "strategy": ["strategy", "setup", "ستاپ", "استراتژی"],
        "entry": ["entry", "ورود", "buy", "sell", "long", "short"],
        "exit": ["exit", "خروج", "close", "بستن"],
        "stop_loss": ["stop loss", "sl", "حد ضرر", "استاپ"],
        "take_profit": ["take profit", "tp", "حد سود"],
        "timeframe": ["timeframe", "تایم فریم", "m1", "m5", "m15", "h1", "h4", "daily"],
        "indicator": ["rsi", "macd", "ema", "sma", "bollinger", "atr", "pivot"],
        "risk": ["risk", "ریسک", "position sizing", "lot size", "volume"],
        "pattern": ["pattern", "الگو", "engulfing", "pin bar", "doji", "hammer"],
        "structure": ["structure", "market structure", "order block", "fvg", "gap", "liquidity"],
    }
    
    found = {}
    text_lower = text.lower()
    for category, words in keywords.items():
        matches = [w for w in words if w in text_lower]
        if matches:
            found[category] = matches
    
    return found


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/06_web_reader.py <url>")
        print("Example: python scripts/06_web_reader.py https://example.com/article")
        sys.exit(1)
    
    url = sys.argv[1]
    
    print(f"Reading: {url}")
    content = read_url(url)
    
    if content.startswith("Error"):
        print(content)
        sys.exit(1)
    
    # Save content
    output_dir = Path("data/web")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    from urllib.parse import urlparse
    domain = urlparse(url).netloc.replace(".", "_")
    txt_path = output_dir / f"{domain}.txt"
    
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Content saved: {txt_path}")
    
    # Analyze
    analysis = analyze_trading_content(content)
    if analysis:
        print("\nTrading keywords found:")
        for cat, words in analysis.items():
            print(f"  {cat}: {', '.join(words)}")
    
    # Save analysis
    analysis_path = output_dir / f"{domain}_analysis.json"
    with open(analysis_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    print(f"\nAnalysis saved: {analysis_path}")


if __name__ == "__main__":
    main()
