import datetime
import json
import time

import surrogates
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.utils import executor

from json_creator import make_rasp_json
from rasp_parser import get_rasp
from xl_reader import read_excel

lesson_types = {
    "1": surrogates.decode('\uD83D\uDFE9'),
    "2": surrogates.decode('\uD83D\uDFE6'),
    "3": surrogates.decode('\uD83D\uDFE5'),
    "4": surrogates.decode('\uD83D\uDFE8')
}

days = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье"
]

Token = '5677926444:AAFUXCXR5xX9PRDJVO0dihz_6oEE0SBrrsA'
bot = Bot(token=Token)
dp = Dispatcher(bot)

button1 = KeyboardButton("Сегодня")
button2 = KeyboardButton("Завтра")
button3 = KeyboardButton("Загрузить данные")
button4 = KeyboardButton("Номер недели")
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row(button1, button2).row(button3, button4)


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    try:
        time.sleep(0.5)
        await bot.send_message(message.from_user.id, "Привет. Сначала загрузи данные, потом смотри расписание",
                               reply_markup=keyboard)
        await message.delete()
    except:
        print('error')


@dp.message_handler(text='Загрузить данные')
async def send_week(message: types.Message):
    current_date = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=4)))
    week = int(current_date.strftime('%W')) - 34
    try:
        if current_date.weekday() == 6:
            get_rasp(week + 1)
            read_excel(week + 1)
            make_rasp_json(week + 1)
        else:
            get_rasp(week)
            read_excel(week)
            make_rasp_json(week)
        time.sleep(0.5)
        await bot.send_message(message.from_user.id, "Данные загружены")
    except:
        time.sleep(0.5)
        await bot.send_message(message.from_user.id, "Что-то пошло не так")


@dp.message_handler(text='Номер недели')
async def collect_data(message: types.Message):
    current_date = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=4)))
    week = int(current_date.strftime('%W')) - 34
    try:
        time.sleep(0.5)
        await bot.send_message(message.from_user.id, str(week))
    except:
        time.sleep(0.5)
        await bot.send_message(message.from_user.id, "Что-то пошло не так")


@dp.message_handler(text=['Сегодня', 'Завтра'])
async def today(message: Message):
    current_date = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=4)))

    if message.text == 'Сегодня':
        num_day = current_date.weekday()
    else:
        if current_date.weekday() == 6:
            num_day = 0
        else:
            num_day = current_date.weekday() + 1

    this_day = days[num_day]
    with open("rasp.json", "r", encoding="utf8") as file:
        rasp = json.load(file)
    try:
        for item in rasp[this_day]:
            if len(item) == 2:
                text = f"{item[0]['time']} - {item[0]['name']}\n{item[0]['place']}{lesson_types[item[0]['type']]}\n{item[0]['teacher']}\n{item[0]['group']}\n\n{item[1]['time']} - {item[1]['name']}{lesson_types[item[1]['type']]}\n{item[1]['place']}\n{item[1]['teacher']}\n{item[1]['group']}"
            elif item["name"] == '':
                continue
            else:
                text = f"{item['time']} - {item['name']}{lesson_types[item['type']]}\n{item['place']}\n{item['teacher']}\n{item['group']}"
            time.sleep(0.5)
            await bot.send_message(message.from_user.id, text)
    except:
        if num_day == 6:
            time.sleep(0.5)
            await bot.send_message(message.from_user.id, 'В этот день выходной')
        else:
            time.sleep(0.5)
            await bot.send_message(message.from_user.id, "Ошибка. Загрузите данные")


executor.start_polling(dp, skip_updates=True)
