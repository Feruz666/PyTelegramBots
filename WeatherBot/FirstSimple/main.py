import telebot 
import config
import random
import requests
import os

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

PORT = int(os.environ.get('PORT', 5000))


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('media/sticker.webp', 'rb')

    bot.send_sticker(message.chat.id, sti)

    #keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("◙ Random value")
    item2 = types.KeyboardButton("How its going?")
    item3 = types.KeyboardButton("Send video")

    markup.add(item1, item2, item3)


    bot.send_message(message.chat.id, "Welcome my friend, {0.first_name}!\n I am - <b>{1.first_name}</b> and I will try to show you weather ☺".format(message.from_user, bot.get_me()),
    parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text', 'video', 'photo'])
def someFunc(message):
    if message.chat.type == 'private':
        if message.text == '◙ Random value':
            bot.send_message(message.chat.id, str(random.randint(0,100)))
        elif message.text == 'How its going?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("fine", callback_data='good')
            item2 = types.InlineKeyboardButton("Not well", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'I am fine, what about you?', reply_markup=markup)

        #sending VIDEO
        elif message.text == 'Send video':

            bot.send_video(chat_id=message.chat.id, data=open('media/vid2.mp4', 'rb'), supports_streaming=True)

        else:

            try:
                url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(message.text,config.API_KEY_OPENWEATHER)

                city_weather = requests.get(url).json()

                weather = {
                    'city' : city_weather['name'],
                    'temperature' : city_weather['main']['temp'],
                    'description' : city_weather['weather'][0]['description'],
                }

                bot.send_message(message.chat.id, 'Response:\n {0} \n {1:.2f}° \n {2}'.format(weather["city"],weather["temperature"]-273,weather["description"]))
            except KeyError:
                bot.send_message(message.chat.id, 'I dont know city you wrote')
            
            else:
                bot.send_message(message.chat.id, 'Oops ^^')

            

            
            

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'So, that is good ☻')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Shit happens')

            #remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="How its going?",
            reply_markup=None) 
            
            #show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="That is test notification!!!♦")

    except Exception as e:
        print(repr(e))


#RUN
# bot.polling(none_stop=True)
