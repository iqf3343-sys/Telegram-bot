import telebot
from telebot import types

# Bot tokeni
TOKEN = "8223970166:AAHNaM98j-cClSd8k1kQihIXeZ79gCHObnc"
bot = telebot.TeleBot(TOKEN)

# Majburiy obuna kanallari
CHANNELS = ["@Mister_savdo", "@Mister_pubg"]

# Start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if check_sub(user_id):
        bot.send_message(message.chat.id, "✅ Botga xush kelibsiz! Kod yuboring.")
    else:
        markup = types.InlineKeyboardMarkup()
        for ch in CHANNELS:
            markup.add(types.InlineKeyboardButton(f"➕ Obuna bo‘lish: {ch}", url=f"https://t.me/{ch[1:]}"))
        markup.add(types.InlineKeyboardButton("✅ Obunani tekshirish", callback_data="check_subs"))
        bot.send_message(message.chat.id, "❌ Avval kanallarga obuna bo‘ling:", reply_markup=markup)

# Obunani tekshirish
@bot.callback_query_handler(func=lambda call: call.data == "check_subs")
def check_subs(call):
    user_id = call.from_user.id
    if check_sub(user_id):
        bot.send_message(call.message.chat.id, "✅ Obuna tasdiqlandi! Endi kod yuboring.")
    else:
        bot.answer_callback_query(call.id, "❌ Hali hammasiga obuna bo‘lmadingiz.")

# Kodlarni qabul qilish
@bot.message_handler(func=lambda m: True)
def get_code(message):
    codes = {
        "123": "🎬 Kino 1: https://example.com/1",
        "456": "🎬 Kino 2: https://example.com/2",
        "pubg": "🎮 PUBG cheat: https://example.com/pubg"
    }
    text = message.text.strip()
    if text in codes:
        bot.send_message(message.chat.id, codes[text])
    else:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri kod!")

# Obuna tekshirish funksiyasi
def check_sub(user_id):
    for ch in CHANNELS:
        try:
            member = bot.get_chat_member(ch, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except:
            return False
    return True

bot.polling()
