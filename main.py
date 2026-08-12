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
    
    # Validasi sederhana apakah pesan terlihat seperti cookie Netflix
    if "NetflixId=" not in cookie_text:
        bot.reply_to(message, "❌ Format tidak valid. Harap kirimkan string cookie Netflix yang lengkap (harus mengandung NetflixId).")
        return

    processing_msg = bot.reply_to(message, "⏳ Sedang memproses dan mengekstrak token...")

    try:
        nftoken_result = None
        
        # Pisahkan cookie berdasarkan titik koma (;)
        cookie_pairs = cookie_text.split(";")
        for pair in cookie_pairs:
            if "=" in pair:
                key, value = pair.strip().split("=", 1)
                if key == "NetflixId":
                    # Decode URL (mengubah %3D menjadi =, dll)
                    decoded_val = urllib.parse.unquote(value)
                    
                    # Di dalam NetflixId, token nftoken biasanya diekstrak dari bagian value-nya.
                    # Jika formatnya mengandung parameter atau nilai tertentu, kita ambil bagian kodenya.
                    nftoken_result = decoded_val
                    break

        if nftoken_result:
            response_text = (
                f"✅ **Berhasil Mendapatkan Token!**\n\n"
                f"🔑 **nftoken / NetflixId Decoded:**\n`{nftoken_result}`"
            )
        else:
            response_text = "❌ Gagal menemukan parameter NetflixId di dalam cookie tersebut."

        bot.edit_message_text(response_text, chat_id=message.chat.id, message_id=processing_msg.message_id, parse_mode="Markdown")

    except Exception as e:
        bot.edit_message_text(f"❌ Terjadi kesalahan: `{str(e)}`", chat_id=message.chat.id, message_id=processing_msg.message_id, parse_mode="Markdown")

print("Bot Telegram ekstraktor cookie aktif...")
bot.infinity_polling()
