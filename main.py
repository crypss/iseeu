import os
import urllib.parse
import telebot

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

    processing_msg = bot.reply_to(message, "⏳ Mengonversi format nftoken...")

    try:
        raw_ct = None
        
        # Pisahkan berdasarkan titik koma (;)
        cookie_pairs = cookie_text.split(";")
        for pair in cookie_pairs:
            if "=" in pair:
                key, value = pair.strip().split("=", 1)
                if key == "NetflixId":
                    decoded_val = urllib.parse.unquote(value)
                    params = decoded_val.split("&")
                    for p in params:
                        if p.startswith("ct="):
                            raw_ct = p.split("=", 1)[1]
                            break
                    break

        if raw_ct:
            # Mengubah format Base64 URL-safe (simbol - dan _) 
            # menjadi format standard Base64 (simbol + dan /)
            standard_b64 = raw_ct.replace("-", "+").replace("_", "/")
            
            # Menambahkan padding '=' jika panjangnya kurang pas kelipatan 4
            padding_needed = len(standard_b64) % 4
            if padding_needed:
                standard_b64 += "=" * (4 - padding_needed)

            response_text = f"`{standard_b64}`"
        else:
            response_text = "❌ Gagal menemukan parameter ct di dalam cookie."

        bot.edit_message_text(response_text, chat_id=message.chat.id, message_id=processing_msg.message_id, parse_mode="Markdown")

    except Exception as e:
        bot.edit_message_text(f"❌ Error: `{str(e)}`", chat_id=message.chat.id, message_id=processing_msg.message_id, parse_mode="Markdown")

print("Bot konversi nftoken aktif...")
bot.infinity_polling()
