"""
07 - Gemini Video Analyzer (New API)
تحلیل ویدیو با Google Gemini API - پکیج جدید google-genai
نحوه اجرا: python scripts/07_gemini_video_analyzer.py <video_path> <api_key>
"""
import sys
import json
import os
import time
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Install: pip install google-genai")
    sys.exit(1)

# Proxy config
PROXY_URL = os.environ.get("HTTPS_PROXY", os.environ.get("ALL_PROXY", ""))


PASS1_PROMPT = """Analyze this entire trading video.

Extract ALL information from both:
1. Spoken dialogue (Farsi/Arabic/English)
2. Visual content (charts, indicators, text on screen)

Do not summarize yet.

For every important event provide:
- timestamp
- exact spoken claim
- visual observation  
- chart information
- detected trading concept
- confidence (0-1)

Clearly distinguish between:
- EXPLICIT (said directly)
- VISUAL (seen on chart/screen)
- INFERRED (implied but not stated)
- UNKNOWN (cannot determine)

Output as structured JSON."""

PASS2_PROMPT = """Using only the evidence extracted from the video, reconstruct the trading strategy.

Identify:
- Market (forex, gold, crypto, etc.)
- Symbol(s)
- Timeframe(s)
- Market condition required
- Bias logic
- Setup type
- Entry conditions (all of them)
- Confirmation conditions
- Stop loss method
- Take profit method
- Risk management rules
- Position sizing rules
- Trade management rules
- Exit conditions
- Invalidations
- Filters
- Session timing
- News avoidance rules

For every rule provide its timestamp and evidence source.
If a rule is not explicitly stated, mark it as UNKNOWN.
Never invent a missing rule.

Output as structured JSON."""

PASS3_PROMPT = """Convert the extracted strategy into deterministic, backtestable rules.

Separate into:
1. EXPLICIT RULES (directly stated)
2. INFERRED RULES (logically derived)
3. AMBIGUOUS RULES (could mean multiple things)
4. MISSING RULES (need more information)

For each rule provide:
- rule_text
- category (entry/exit/risk/filter/etc)
- confidence
- evidence_timestamps
- backtest_ready (true/false)
- notes

Then produce:
- A list of questions that must be answered before backtesting
- A list of assumptions made
- Risk parameters with defaults

Output as structured JSON."""


def analyze_video(video_path, api_key, output_dir="data/video_analysis"):
    """تحلیل ویدیو با Gemini"""
    
    # Try to create client with proxy
    try:
        import httpx
        http_client = httpx.Client(proxy=PROXY_URL)
        client = genai.Client(api_key=api_key, http_options={'client': http_client})
    except Exception:
        client = genai.Client(api_key=api_key)
    
    # Upload video
    print(f"Uploading video: {video_path}")
    uploaded_file = client.files.upload(file=video_path)
    print(f"Uploaded: {uploaded_file.name}")
    
    # Wait for processing
    print("Waiting for video processing...")
    while uploaded_file.state.name == "PROCESSING":
        time.sleep(5)
        uploaded_file = client.files.get(name=uploaded_file.name)
        print(f"  Status: {uploaded_file.state.name}")
    
    if uploaded_file.state.name == "FAILED":
        print(f"Video processing failed: {uploaded_file.state.name}")
        return None
    
    print(f"Video ready: {uploaded_file.state.name}")
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    results = {}
    
    # Pass 1: Raw extraction
    print("\n=== Pass 1: Raw Extraction ===")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[PASS1_PROMPT, uploaded_file]
    )
    pass1_text = response.text
    results["pass1_raw"] = pass1_text
    
    with open(f"{output_dir}/pass1_raw.txt", "w", encoding="utf-8") as f:
        f.write(pass1_text)
    print(f"Saved: {output_dir}/pass1_raw.txt")
    
    # Pass 2: Strategy reconstruction
    print("\n=== Pass 2: Strategy Reconstruction ===")
    pass2_input = f"Based on this video analysis:\n\n{pass1_text}\n\n{PASS2_PROMPT}"
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[pass2_input, uploaded_file]
    )
    pass2_text = response.text
    results["pass2_strategy"] = pass2_text
    
    with open(f"{output_dir}/pass2_strategy.txt", "w", encoding="utf-8") as f:
        f.write(pass2_text)
    print(f"Saved: {output_dir}/pass2_strategy.txt")
    
    # Pass 3: Backtest rules
    print("\n=== Pass 3: Backtest Rules ===")
    pass3_input = f"Based on this strategy analysis:\n\n{pass2_text}\n\n{PASS3_PROMPT}"
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[pass3_input]
    )
    pass3_text = response.text
    results["pass3_backtest"] = pass3_text
    
    with open(f"{output_dir}/pass3_backtest.txt", "w", encoding="utf-8") as f:
        f.write(pass3_text)
    print(f"Saved: {output_dir}/pass3_backtest.txt")
    
    # Save combined results
    with open(f"{output_dir}/full_analysis.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nSaved: {output_dir}/full_analysis.json")
    
    # Delete uploaded file
    client.files.delete(name=uploaded_file.name)
    print("Uploaded file deleted.")
    
    return results


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/07_gemini_video_analyzer.py <video_path> <api_key>")
        print("Example: python scripts/07_gemini_video_analyzer.py videos/video.mp4 YOUR_API_KEY")
        print("\nGet API key: https://aistudio.google.com/apikey")
        sys.exit(1)
    
    video_path = sys.argv[1]
    api_key = sys.argv[2]
    
    if not os.path.exists(video_path):
        print(f"File not found: {video_path}")
        sys.exit(1)
    
    analyze_video(video_path, api_key)


if __name__ == "__main__":
    main()
