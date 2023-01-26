import telebot
from config import *
from extensions import Converter, APIException
import traceback

bot = telebot.TeleBot(TOKEN)
# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start'])
def command_start(message: telebot.types.Message):
    bot.reply_to(message, f"Этот бот поможет тебе узнать нынешний курс выбранных валют, напиши /help, {message.from_user.first_name}")
#    bot.send_message(message.chat.id, "Чем помочь?", parse_mode='html')

@bot.message_handler(commands=['help'])
def command_help(message: telebot.types.Message):
    bot.reply_to(message, f"Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту надо перевести>\
<количество первой валюты>\nУвидеть список всех доступных валют: /values")

@bot.message_handler(commands=['values'])
def command_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    commands = message.text.split(' ')
    try:
        if len(commands) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Converter.get_price(*commands)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)

# Обрабатывается все документы и аудиозаписи и фото
@bot.message_handler(content_types=['document', 'audio', 'photo'])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, f'Хороший мем:D, {message.from_user.first_name}')

bot.polling(none_stop=True)













