# Coded by why-id
# GresiXploiter
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import threading
import time

# Token dari BotFather
TOKEN = 'token'

bot = telebot.TeleBot(TOKEN)

# Menyimpan pasangan chat
pasangan = {}
daftar_tunggu = []
pesan_terkirim = {}
pesan_menunggu = {}

# Membuat custom keyboard yang dinamis
def buat_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    cari_button = KeyboardButton('🚀 ғɪɴᴅ ᴀ ᴘᴀʀᴛɴᴇʀ')
    stop_button = KeyboardButton('⛔️ ʟᴇᴀᴠᴇ ᴘᴀʀᴛɴᴇʀ')
    hapus_button = KeyboardButton('❌ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴄʜᴀᴛ')
    markup.add(cari_button, stop_button, hapus_button)
    return markup

# Handler untuk perintah /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = buat_keyboard()
    bot.send_message(message.chat.id, "𝘚𝘦𝘭𝘢𝘮𝘢𝘵 𝘥𝘢𝘵𝘢𝘯𝘨,\n𝘜𝘯𝘵𝘶𝘬 𝘮𝘦𝘯𝘦𝘮𝘶𝘬𝘢𝘯 𝘱𝘢𝘳𝘵𝘯𝘦𝘳 𝘬𝘭𝘪𝘬 𝘱𝘢𝘥𝘢 𝘱𝘪𝘭𝘪𝘩𝘢𝘯 𝘮𝘦𝘯𝘶", reply_markup=markup)

# Handler untuk perintah Cari
@bot.message_handler(func=lambda message: message.text == '🚀 ғɪɴᴅ ᴀ ᴘᴀʀᴛɴᴇʀ')
def cari(message):
    user_id = message.chat.id
    if user_id in pasangan:
        bot.send_message(message.chat.id, '𝘈𝘯𝘥𝘢 𝘴𝘶𝘥𝘢𝘩 𝘵𝘦𝘳𝘩𝘶𝘣𝘶𝘯𝘨 𝘥𝘦𝘯𝘨𝘢𝘯 𝘱𝘢𝘳𝘵𝘯𝘦𝘳')
        return

    if daftar_tunggu and daftar_tunggu[0] != user_id:
        partner_id = daftar_tunggu.pop(0)
        pasangan[user_id] = partner_id
        pasangan[partner_id] = user_id
        pesan_terkirim[user_id] = []
        pesan_terkirim[partner_id] = []
        # Hapus pesan "Menunggu partner..." jika ada
        if user_id in pesan_menunggu:
            bot.delete_message(chat_id=user_id, message_id=pesan_menunggu[user_id])
            del pesan_menunggu[user_id]
        if partner_id in pesan_menunggu:
            bot.delete_message(chat_id=partner_id, message_id=pesan_menunggu[partner_id])
            del pesan_menunggu[partner_id]
        bot.send_message(user_id, '𝘈𝘯𝘥𝘢 𝘵𝘦𝘭𝘢𝘩 𝘵𝘦𝘳𝘩𝘶𝘣𝘶𝘯𝘨 𝘥𝘦𝘯𝘨𝘢𝘯 𝘱𝘢𝘳𝘵𝘯𝘦𝘳 🤓\n𝘔𝘶𝘭𝘢𝘪𝘭𝘢𝘩 𝘮𝘦𝘯𝘨𝘰𝘣𝘳𝘰𝘭')
        bot.send_message(partner_id, '𝘈𝘯𝘥𝘢 𝘵𝘦𝘭𝘢𝘩 𝘵𝘦𝘳𝘩𝘶𝘣𝘶𝘯𝘨 𝘥𝘦𝘯𝘨𝘢𝘯 𝘱𝘢𝘳𝘵𝘯𝘦𝘳 🤓\n𝘔𝘶𝘭𝘢𝘪𝘭𝘢𝘩 𝘮𝘦𝘯𝘨𝘰𝘣𝘳𝘰𝘭')
    else:
        sent_message = bot.send_message(message.chat.id, '𝘚𝘦𝘥𝘢𝘯𝘨 𝘮𝘦𝘯𝘤𝘢𝘳𝘪 𝘱𝘢𝘳𝘵𝘯𝘦𝘳')
        pesan_menunggu[user_id] = sent_message.message_id
        daftar_tunggu.append(user_id)

# Handler untuk perintah Stop untuk memutuskan koneksi
@bot.message_handler(func=lambda message: message.text == '⛔️ ʟᴇᴀᴠᴇ ᴘᴀʀᴛɴᴇʀ')
def stop(message):
    user_id = message.chat.id
    if user_id in pasangan:
        partner_id = pasangan.pop(user_id)
        pasangan.pop(partner_id, None)
        pesan_terkirim.pop(user_id, None)
        pesan_terkirim.pop(partner_id, None)
        bot.send_message(partner_id, '𝘗𝘢𝘳𝘵𝘯𝘦𝘳 𝘵𝘦𝘭𝘢𝘩 𝘮𝘦𝘯𝘪𝘯𝘨𝘨𝘢𝘭𝘬𝘢𝘯 𝘈𝘯𝘥𝘢')
        bot.send_message(message.chat.id, '𝘈𝘯𝘥𝘢 𝘵𝘦𝘭𝘢𝘩 𝘮𝘦𝘯𝘪𝘯𝘨𝘨𝘢𝘭𝘬𝘢𝘯 𝘱𝘢𝘳𝘵𝘯𝘦𝘳')
    else:
        bot.send_message(message.chat.id, '𝘈𝘯𝘥𝘢 𝘣𝘦𝘭𝘶𝘮 𝘵𝘦𝘳𝘩𝘶𝘣𝘶𝘯𝘨 𝘥𝘦𝘯𝘨𝘢𝘯 𝘱𝘢𝘳𝘵𝘯𝘦𝘳')

# Fungsi Hapus
def delete_confirmation_message(chat_id, message_id, delay):
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        pass

# Handler untuk perintah Hapus untuk menghapus semua pesan yang dikirimkan
@bot.message_handler(func=lambda message: message.text == '❌ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴄʜᴀᴛ')
def hapus(message):
    user_id = message.chat.id
    if user_id in pasangan and user_id in pesan_terkirim:
        partner_id = pasangan[user_id]
        try:
            for message_id in pesan_terkirim[user_id]:
                bot.delete_message(chat_id=partner_id, message_id=message_id)
            sent_message = bot.send_message(user_id, '𝘚𝘦𝘮𝘶𝘢 𝘱𝘦𝘴𝘢𝘯 𝘥𝘦𝘯𝘨𝘢𝘯 𝘱𝘢𝘳𝘵𝘯𝘦𝘳 𝘵𝘦𝘭𝘢𝘩 𝘵𝘦𝘳𝘩𝘢𝘱𝘶𝘴')
            pesan_terkirim[user_id] = []
            # Hapus dalam 5 Detik
            threading.Thread(target=delete_confirmation_message, args=(user_id, sent_message.message_id, 5)).start()
        except Exception as e:
            bot.send_message(user_id, f'Gagal menghapus pesan: {str(e)}')
    else:
        bot.send_message(user_id, '𝘈𝘯𝘥𝘢 𝘣𝘦𝘭𝘶𝘮 𝘵𝘦𝘳𝘩𝘶𝘣𝘶𝘯𝘨 𝘥𝘦𝘯𝘨𝘢𝘯 𝘱𝘢𝘳𝘵𝘯𝘦𝘳')

# Handler untuk menangani pesan teks dan media
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'audio', 'voice'])
def message_handler(message):
    user_id = message.chat.id
    if user_id in pasangan:
        partner_id = pasangan[user_id]
        try:
            if message.content_type == 'text':
                sent_message = bot.send_message(partner_id, message.text)
            elif message.content_type == 'photo':
                sent_message = bot.send_photo(partner_id, message.photo[-1].file_id, caption=message.caption)
            elif message.content_type == 'video':
                sent_message = bot.send_video(partner_id, message.video.file_id, caption=message.caption)
            elif message.content_type == 'document':
                sent_message = bot.send_document(partner_id, message.document.file_id, caption=message.caption)
            elif message.content_type == 'audio':
                sent_message = bot.send_audio(partner_id, message.audio.file_id, caption=message.caption)
            elif message.content_type == 'voice':
                sent_message = bot.send_voice(partner_id, message.voice.file_id, caption=message.caption)

            # Menyimpan ID pesan yang dikirim
            pesan_terkirim[user_id].append(sent_message.message_id)
        except Exception as e:
            bot.send_message(user_id, f'Terjadi kesalahan saat mengirim pesan: {str(e)}')
    else:
        bot.send_message(message.chat.id, '𝘈𝘯𝘥𝘢 𝘣𝘦𝘭𝘶𝘮 𝘵𝘦𝘳𝘩𝘶𝘣𝘶𝘯𝘨 𝘥𝘦𝘯𝘨𝘢𝘯 𝘱𝘢𝘳𝘵𝘯𝘦𝘳')

if __name__ == '__main__':
    bot.polling()
