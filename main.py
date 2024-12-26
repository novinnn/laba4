import telebot
bot = telebot.predweather_bot('7315210266:AAGbGDYkPTrvq0sQGgofRwfxoBxTqJWxQew')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Напиши название города.')



@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()

bot.polling(none_stop=True)