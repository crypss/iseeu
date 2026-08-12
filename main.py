import os
import time
import telebot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Mengambil token dari Environment Variable sistem komputer/server
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ Token bot belum diset! Harap atur environment variable TELEGRAM_BOT_TOKEN terlebih dahulu.")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_inspect(message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(message, "❌ Kirimkan URL yang valid.")
        return

    processing_msg = bot.reply_to(message, "⏳ Mengambil link mp4...")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get(url)
        time.sleep(3)

        playlist_data = driver.execute_script("return window.playlist;")

        links_1080_720 = []
        if playlist_data and "sources" in playlist_data:
            for src in playlist_data["sources"]:
                label = src.get("label")
                file_url = src.get("file")
                
                if label in ["4K", "4k", "2160", "1440", "1080", "720"] and file_url:
                    links_1080_720.append(f"**{label}p**:\n`{file_url}`")

        if links_1080_720:
            response_text = "\n\n".join(links_1080_720)
        else:
            response_text = "❌ Link MP4 tidak ditemukan."

        bot.edit_message_text(response_text, chat_id=message.chat.id, message_id=processing_msg.message_id, parse_mode="Markdown")

    except Exception as e:
        bot.edit_message_text(f"❌ Error: `{str(e)}`", chat_id=message.chat.id, message_id=processing_msg.message_id, parse_mode="Markdown")
    
    finally:
        if driver:
            driver.quit()

print("Bot aktif...")
bot.infinity_polling()
