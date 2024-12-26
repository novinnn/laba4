import telebot
import requests
import json

bot = telebot.TeleBot('7315210266:AAGbGDYkPTrvq0sQGgofRwfxoBxTqJWxQew')
API = '655865144727ccc1ab938df295d320d7'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Напиши название города.')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.statud_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Погода сейчас: {data["main"]["temp"]}')
        image = 'sunny.png' if temp > 5.0 else 'sun.png'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, f'Город указан не верно.')

bot.polling(none_stop=True)