import telebot
import requests
import json

bot = telebot.TeleBot('7315210266:AAGbGDYkPTrvq0sQGgofRwfxoBxTqJWxQew')
API = '655865144727ccc1ab938df295d320d7'

# Хранилище избранных городов
user_favorites = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Напиши название города или используй команды /addfavorite, /favorites.')

@bot.message_handler(commands=['addfavorite'])
def add_favorite(message):
    bot.send_message(message.chat.id, 'Напиши название города, чтобы добавить его в избранное.')
    bot.register_next_step_handler(message, save_favorite)

def save_favorite(message):
    city = message.text.strip().lower()
    user_id = message.chat.id

    # Проверяем, есть ли пользователь в словаре
    if user_id not in user_favorites:
        user_favorites[user_id] = []

    # Добавляем город в избранное, если его там ещё нет
    if city not in user_favorites[user_id]:
        user_favorites[user_id].append(city)
        bot.reply_to(message, f'Город {city} добавлен в избранное!')
    else:
        bot.reply_to(message, f'Город {city} уже есть в избранном.')

@bot.message_handler(commands=['favorites'])
def show_favorites(message):
    user_id = message.chat.id
    favorites = user_favorites.get(user_id, [])

    if favorites:
        bot.send_message(message.chat.id, 'Ваши избранные города:\n' + '\n'.join(favorites))
    else:
        bot.send_message(message.chat.id, 'У вас пока нет избранных городов.')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Погода сейчас: {temp}°C')
        image = 'sun.png' if temp > 5.0 else 'sunny.png'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, f'Город указан неверно.')

bot.polling(none_stop=True)
