import telebot
from telebot import types
from datetime import date
import telebot
import gspread


bot_token = '5643771313:AAHAi7S5ujJI3a84Qzq3mFuoqeUS9nR5MNs'
bot = telebot.TeleBot('5643771313:AAHAi7S5ujJI3a84Qzq3mFuoqeUS9nR5MNs')
gs = gspread.service_account(filename="D:\Telegram_bot\my-project-1-374720-925986fe998a.json")
sh = gs.open_by_key('16G9YGziSIl0lSSjb9AlHyFJcqvv3B_noUdIeHAIVZuc')
worksheet = sh.sheet1

res = worksheet.get_all_records()
print(res)


#авторизация ID
def auth(func):

    async def wrapper(message):
        """if message['from']['id'] !=1030616550:
        return await message.reply("Access denied", reply=False)"""
        return await func(message)

    return wrapper


#Отработка /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_1 = types.KeyboardButton("Hello")
    item_2 = types.KeyboardButton("Записать расход")
    item_3 = types.KeyboardButton("Удалить расход")
    item_4 = types.KeyboardButton("Другое")

    markup.add(item_1, item_2, item_3, item_4)

    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Я - твой виртуальный помощник Расходайзер. "
                          "Я буду вести учёт твоих расходов.".format(message.from_user), reply_markup = markup)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == 'Hello':
        bot.send_message(message.chat.id, f"И тебе привет, {message.from_user.first_name}! Выбери, что ты хочешь сделать", parse_mode='html')
    elif message.text == 'Записать расход':
        try:
            today = date.today().strftime("%d.%m.%Y")
            category, price = message.text.split("-", 1)
            text_message = f"На {today} в таблицу добавлена запись: категория - {category}, сумма - {price}"
            bot.send_message(message.chat.id, text_message)

            sh = gc.open_by_key(gs_id)
            sh.sheet1.append_row([today, category, price])
        except:
            bot.send_message(message.chat.id, 'ОШИБКА! Неправильный формат данных!')

        bot.send_message(message.chat.id, 'Введите расход через дефис в формате [КАТЕГОРИЯ-СУММА]:')


bot.polling(none_stop=True, interval=0)