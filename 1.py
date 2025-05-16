import telebot
import requests
import json
bot = telebot.TeleBot('#your key')
API = '#your API' #use yours API key in site openweathermap, you can take him after registration 
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'привет рад тебя видеть! напиши название города')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')     
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Сейчас погода: {temp} градусов Цельсия')
        
        image = 'sun.png' if temp > 5.0 else 'cloud.png'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, f'Город указан не верно, попробуйте ещё раз')
        bot.register_next_step_handler(message, get_weather)

bot.polling(none_stop=True)