"""
01 - Video Analyzer
استخراج صدا از ویدیو و متن‌نویسی با Whisper
نحوه اجرا: python scripts/01_video_analyzer.py <path_to_video>
"""
import sys
import os
import subprocess
import json
from pathlib import Path

def get_ffmpeg_path():
    """پیدا کردن مسیر ffmpeg"""
    # Check tools directory
    tools_ffmpeg = Path(__file__).parent.parent / "tools" / "ffmpeg.exe"
    if tools_ffmpeg.exists():
        return str(tools_ffmpeg)
    # Check PATH
    import shutil
    path_ffmpeg = shutil.which("ffmpeg")
    if path_ffmpeg:
        return path_ffmpeg
    return "ffmpeg"

def extract_audio(video_path, output_path="temp_audio.wav"):
    """استخراج صدا از ویدیو با ffmpeg"""
    ffmpeg = get_ffmpeg_path()
    cmd = [
        ffmpeg, "-i", video_path,
        "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1",
        output_path, "-y"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ffmpeg error: {result.stderr}")
        return None
    return output_path

def transcribe_with_whisper(audio_path, model_size="base"):
    """متن‌نویسی با Whisper"""
    try:
        import whisper
        model = whisper.load_model(model_size)
        result = model.transcribe(audio_path, language="fa")
        return result["text"]
    except ImportError:
        print("Whisper نصب نیست. اجرا کن: pip install openai-whisper")
        return None

def analyze_strategy(text):
    """تحلیل استراتژی از متن"""
    keywords = {
        "entry": ["ورود", "entry", "buy", "sell", "long", "short", "باز کردن"],
        "exit": ["خروج", "exit", "close", "بستن", "بستن پوزیشن"],
        "stop_loss": ["حد ضرر", "stop loss", "sl", "استاپ"],
        "take_profit": ["حد سود", "take profit", "tp", "سود"],
        "timeframe": ["تایم فریم", "timeframe", "m1", "m5", "m15", "h1", "h4", "daily"],
        "indicator": ["اندیکاتور", "indicator", "rsi", "macd", "ema", "sma", "bollinger"],
        "risk": ["ریسک", "risk", "مدیریت سرمایه", "lot", "حجم"],
    }
    
    found = {}
    text_lower = text.lower()
    for category, words in keywords.items():
        found[category] = [w for w in words if w in text_lower]
    
    return found

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/01_video_analyzer.py <video_path>")
        print("Example: python scripts/01_video_analyzer.py videos/video.mp4")
        sys.exit(1)
    
    video_path = sys.argv[1]
    
    if not os.path.exists(video_path):
        print(f"File not found: {video_path}")
        sys.exit(1)
    
    print(f"Analyzing: {video_path}")
    
    # Step 1: Extract audio
    print("Step 1: Extracting audio...")
    audio_path = extract_audio(video_path)
    if not audio_path:
        print("Failed to extract audio. Make sure ffmpeg is installed.")
        sys.exit(1)
    
    # Step 2: Transcribe
    print("Step 2: Transcribing...")
    text = transcribe_with_whisper(audio_path)
    if not text:
        print("Failed to transcribe.")
        sys.exit(1)
    
    # Step 3: Save transcription
    output_dir = Path("data/transcriptions")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    video_name = Path(video_path).stem
    txt_path = output_dir / f"{video_name}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Transcription saved: {txt_path}")
    
    # Step 4: Analyze strategy
    print("Step 4: Analyzing strategy...")
    analysis = analyze_strategy(text)
    
    analysis_path = output_dir / f"{video_name}_analysis.json"
    with open(analysis_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    print(f"Analysis saved: {analysis_path}")
    
    # Step 5: Cleanup
    if os.path.exists(audio_path):
        os.remove(audio_path)
    
    print("\nDone! Results:")
    print(f"  Text: {txt_path}")
    print(f"  Analysis: {analysis_path}")

if __name__ == "__main__":
    main()
