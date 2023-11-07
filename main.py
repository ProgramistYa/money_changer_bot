import telebot
from telebot import types

from config import *
from extensions import Converter, APIException
import traceback

# import time


# Можно попробовать добавить смайлики флагов на валюту
# import emoji
# print(emoji.emojize('Python is :thumbs_up:'))

bot = telebot.TeleBot(TOKEN)

# создание кнопки соприжжение с моим ключом
add_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
buttons = []
for val in keys.keys():
    buttons.append(types.KeyboardButton(val.capitalize()))
add_markup.add(*buttons)


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start'])
def command_start(message: telebot.types.Message):
    bot.reply_to(message, f"<b>Этот бот поможет тебе узнать нынешний курс восьми выбранных валют.</b> "
                          f"\nНапиши /help, {message.from_user.first_name}", parse_mode="html")


#    bot.send_message(message.chat.id, "Чем помочь?", parse_mode='html')

# Для завершения программы командой /stop
@bot.message_handler(commands=['stop'])
def stop_command(message):
    bot.reply_to(message, f"Прощай {message.from_user.first_name}")


@bot.message_handler(commands=['help'])
def command_help(message: telebot.types.Message):
    bot.reply_to(message, f"Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту надо перевести>\
<количество первой валюты>\nУвидеть список всех доступных валют: /values")
    text = "Так же есть команда /convert для ступенчатого конвертирования. \nТак же можно остановить бота командой /stop"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def command_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = f'<b>Выберите валюту, из которой конвертировать:</b>'
    bot.send_message(message.chat.id, text, reply_markup=add_markup, parse_mode="html")
    bot.register_next_step_handler(message, base_handler)


def base_handler(message: telebot.types.Message):
    base = message.text.strip()
    text = f'<b>Выберите валюту, в которую конвертировать:</b>'
    bot.send_message(message.chat.id, text, reply_markup=add_markup, parse_mode="html")
    bot.register_next_step_handler(message, sym_handler, base)


def sym_handler(message: telebot.types.Message, base):
    sym = message.text.strip()
    text = f'<b>Напишите сумму конвертации:</b>'
    bot.send_message(message.chat.id, text, parse_mode="html")
    bot.register_next_step_handler(message, amount_handler, base, sym)


def amount_handler(message: telebot.types.Message, base, sym):
    amount = message.text.strip()
    try:
        new_price = Converter.get_price(base, sym, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации: \n{e}')
    else:
        text = f'Цена {amount} {base} в {sym} : {new_price}'
        bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    commands = message.text.split(' ')
    try:
        if len(commands) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Converter.get_price(*commands)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n Напиши команду /help{e}")
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
