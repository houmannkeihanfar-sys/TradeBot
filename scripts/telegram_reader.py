"""
Telegram Channel Reader
اتصال به کانال تلگرام و خواندن محتوا
"""
import asyncio
import os
import sys
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

# API credentials - from environment variables
# Get yours from: https://my.telegram.org
API_ID = int(os.environ.get("TELEGRAM_API_ID", 0))
API_HASH = os.environ.get("TELEGRAM_API_HASH", "")
PHONE = os.environ.get("TELEGRAM_PHONE", "")

# Session file - temporary
SESSION_NAME = "trading_bot_session"


async def main():
    """اتصال به تلگرام و خواندن پست"""
    
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    print("اتصال به تلگرام...")
    await client.start(phone=PHONE)
    
    if not await client.is_user_authorized():
        print("کد OTP به تلگرام شما ارسال شد.")
        code = input("کد را وارد کنید: ")
        await client.sign_in(PHONE, code)
    
    print("اتصال برقرار شد!")
    
    # Read channel posts
    channel_username = "Pashacapitall"
    target_post = 465
    
    print(f"\nدر حال خواندن پست {target_post} از کانال {channel_username}...")
    
    try:
        channel = await client.get_entity(channel_username)
        
        # Get messages around the target post
        messages = await client.get_messages(channel, limit=10, max_id=target_post + 5)
        
        for msg in messages:
            if msg.id >= target_post - 2 and msg.id <= target_post + 2:
                print(f"\n{'='*60}")
                print(f"پست #{msg.id}")
                print(f"تاریخ: {msg.date}")
                print(f"{'='*60}")
                
                if msg.text:
                    print(f"متن:\n{msg.text}")
                
                if msg.media:
                    if isinstance(msg.media, MessageMediaPhoto):
                        print("📷 تصویر دارد")
                        await client.download_media(msg, file=f"media/post_{msg.id}.jpg")
                        print(f"ذخیره شد: media/post_{msg.id}.jpg")
                    
                    elif isinstance(msg.media, MessageMediaDocument):
                        doc = msg.media.document
                        if doc.mime_type.startswith('video'):
                            print(f"🎥 ویدیو ({doc.size / 1024 / 1024:.1f} MB)")
                            await client.download_media(msg, file=f"media/post_{msg.id}.mp4")
                            print(f"ذخیره شد: media/post_{msg.id}.mp4")
                        elif doc.mime_type.startswith('image'):
                            print("📷 تصویر")
                            await client.download_media(msg, file=f"media/post_{msg.id}.jpg")
                        else:
                            print(f"📎 فایل: {doc.mime_type}")
                            await client.download_media(msg, file=f"media/post_{msg.id}")
                
                if msg.reply_to:
                    print(f"پاسخ به پست #{msg.reply_to.reply_to_msg_id}")
    
    except Exception as e:
        print(f"خطا: {e}")
    
    await client.disconnect()
    print("\nاتصال قطع شد.")


if __name__ == "__main__":
    asyncio.run(main())
