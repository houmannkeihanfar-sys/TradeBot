"""
02 - Telegram Channel Reader
خواندن پست‌های کانال تلگرام
نحوه اجرا: python scripts/02_telegram_reader.py <channel> <post_id>
"""
import asyncio
import sys
import os
from pathlib import Path

# API credentials - from my.telegram.org
# Get yours from: https://my.telegram.org
API_ID = int(os.environ.get("TELEGRAM_API_ID", 0))
API_HASH = os.environ.get("TELEGRAM_API_HASH", "")
PHONE = os.environ.get("TELEGRAM_PHONE", "")

async def read_post(channel, post_id):
    """خواندن یک پست خاص از کانال"""
    from telethon import TelegramClient
    from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
    
    session_name = "scripts/telegram_session"
    client = TelegramClient(session_name, API_ID, API_HASH)
    
    print(f"Connecting to Telegram...")
    await client.start(phone=PHONE)
    
    if not await client.is_user_authorized():
        print("OTP code sent to your Telegram.")
        code = input("Enter code: ")
        await client.sign_in(PHONE, code)
    
    print(f"Connected! Reading post #{post_id} from @{channel}...")
    
    try:
        entity = await client.get_entity(channel)
        messages = await client.get_messages(entity, limit=5, max_id=post_id + 3)
        
        results = []
        for msg in messages:
            if msg.id >= post_id - 1 and msg.id <= post_id + 1:
                result = {
                    "id": msg.id,
                    "date": str(msg.date),
                    "text": msg.text or "",
                    "media_type": None,
                    "media_path": None,
                }
                
                if msg.media:
                    if isinstance(msg.media, MessageMediaPhoto):
                        result["media_type"] = "photo"
                        media_dir = Path("media")
                        media_dir.mkdir(exist_ok=True)
                        path = await client.download_media(msg, file=f"media/post_{msg.id}.jpg")
                        result["media_path"] = str(path)
                    
                    elif isinstance(msg.media, MessageMediaDocument):
                        doc = msg.media.document
                        if doc.mime_type.startswith('video'):
                            result["media_type"] = "video"
                            media_dir = Path("media")
                            media_dir.mkdir(exist_ok=True)
                            path = await client.download_media(msg, file=f"media/post_{msg.id}.mp4")
                            result["media_path"] = str(path)
                            result["media_size_mb"] = round(doc.size / 1024 / 1024, 1)
                        elif doc.mime_type.startswith('image'):
                            result["media_type"] = "image"
                            media_dir = Path("media")
                            media_dir.mkdir(exist_ok=True)
                            path = await client.download_media(msg, file=f"media/post_{msg.id}.jpg")
                            result["media_path"] = str(path)
                        else:
                            result["media_type"] = doc.mime_type
                
                results.append(result)
                print(f"\nPost #{msg.id}:")
                if msg.text:
                    print(f"Text: {msg.text[:200]}...")
                if result["media_type"]:
                    print(f"Media: {result['media_type']} -> {result['media_path']}")
        
        # Save results
        import json
        output_path = Path(f"data/telegram/post_{post_id}.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\nResults saved: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    await client.disconnect()

def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/02_telegram_reader.py <channel> <post_id>")
        print("Example: python scripts/02_telegram_reader.py Pashacapitall 465")
        sys.exit(1)
    
    channel = sys.argv[1]
    post_id = int(sys.argv[2])
    
    asyncio.run(read_post(channel, post_id))

if __name__ == "__main__":
    main()
