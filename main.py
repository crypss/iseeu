import os
import urllib.parse
import telebot

# Mengambil token bot dari Environment Variable (GitHub Secrets)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ Token bot belum diset di Environment Variable!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_cookie(message):
    cookie_text = message.text.strip()
    
    if "NetflixId=" not in cookie_text:
        bot.reply_to(message, "❌ Format tidak valid. Harap kirimkan string cookie Netflix yang mengandung NetflixId.")
        return

    processing_msg = bot.reply_to(message, "⏳ Mengekstrak nftoken...")

    try:
        extracted_token = None
        
        # Pisahkan berdasarkan titik koma (;)
        cookie_pairs = cookie_text.split(";")
        for pair in cookie_pairs:
            if "=" in pair:
                key, value = pair.strip().split("=", 1)
                if key == "NetflixId":
                    # Decode URL cookie
                    decoded_val = urllib.parse.unquote(value)
                    
                    # Pecah parameter di dalam NetflixId (v=3&ct=...&pg=...)
                    params = decoded_val.split("&")
                    for p in params:
                        if p.startswith("ct="):
                            extracted_token = p.split("=", 1)[1]
                            break
                    break

        if extracted_token:
            response_text = f"`{extracted_token}`"
        else:
            response_text = "❌ Gagal menemukan parameter ct/token di dalam cookie."

        bot.edit_message_text(response_text, chat_id=message.chat.id, message_id=processing_msg.message_id, parse_mode="Markdown")

    except Exception as e:
        bot.edit_message_text(f"❌ Error: `{str(e)}`", chat_id=message.chat.id, message_id=processing_msg.message_id, parse_mode="Markdown")

print("Bot ekstraktor nftoken aktif...")
bot.infinity_polling()
