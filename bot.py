import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import datetime
from aiogram.types import ContentType, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InputFile, Message
import surrogates

from json_creator import make_rasp_json
from rasp_parser import get_rasp
from xl_reader import read_excel

lesson_types = {
    "1": surrogates.decode('\uD83D\uDFE9'),
    "2": surrogates.decode('\uD83D\uDFE6'),
    "3": surrogates.decode('\uD83D\uDFE5'),
    "4": surrogates.decode('\uD83D\uDFE8')
}
# %uD83D%uDFE5//%uD83D%uDFE6//%uD83D%uDFE9//%uD83D%uDFE8
days = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота"
]

# proxy = 'socks5://45.139.187.21:45656'
Token = '5677926444:AAFUXCXR5xX9PRDJVO0dihz_6oEE0SBrrsA'
bot = Bot(token=Token)
dp = Dispatcher(bot)

button1 = KeyboardButton("Сегодня")
button2 = KeyboardButton("Завтра")
button3 = KeyboardButton("Загрузить данные")
button4 = KeyboardButton("Номер недели")
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row(button1, button2).add(button4).add(button3)

current_date = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=4)))
week = int(current_date.strftime('%W')) - 34


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Привет. Сначала загрузи данные, потом смотри расписание",
                               reply_markup=keyboard)
        await message.delete()
    except:
        print('error')


@dp.message_handler(text='Загрузить данные')
async def send_week(message: types.Message):
    try:
        get_rasp()
        read_excel()
        make_rasp_json()
        await bot.send_message(message.from_user.id, "Данные загружены")
    except:
        await bot.send_message(message.from_user.id, "Что-то пошло не так")


@dp.message_handler(text='Номер недели')
async def collect_data(message: types.Message):
    try:

        await bot.send_message(message.from_user.id, week)
    except:
        await bot.send_message(message.from_user.id, "Что-то пошло не так")


@dp.message_handler(text='Сегодня')
async def today(message: Message):
    num_day = current_date.weekday()
    this_day = days[num_day]
    with open("rasp.json", "r", encoding="utf8") as file:
        rasp = json.load(file)

    for item in rasp[this_day]:
        if len(item) == 2:
            text = f"{item[0]['time']} - {item[0]['name']}\n{item[0]['place']}{lesson_types[item[0]['type']]}\n{item[0]['teacher']}\n{item[0]['group']}\n\n{item[1]['time']} - {item[1]['name']}{lesson_types[item[1]['type']]}\n{item[1]['place']}\n{item[1]['teacher']}\n{item[1]['group']}"
        elif item["name"] == '':
            continue
        else:
            text = f"{item['time']} - {item['name']}{lesson_types[item['type']]}\n{item['place']}\n{item['teacher']}\n{item['group']}"

        await bot.send_message(message.from_user.id, text)


@dp.message_handler(text='Завтра')
async def tomorrow(message: Message):
    num_day = current_date.weekday() + 1
    this_day = days[num_day]
    with open("rasp.json", "r", encoding="utf8") as file:
        rasp = json.load(file)

    for item in rasp[this_day]:
        if len(item) == 2:
            text = f"{item[0]['time']} - {item[0]['name']}\n{item[0]['place']}{lesson_types[item[0]['type']]}\n{item[0]['teacher']}\n{item[0]['group']}\n\n{item[1]['time']} - {item[1]['name']}{lesson_types[item[1]['type']]}\n{item[1]['place']}\n{item[1]['teacher']}\n{item[1]['group']}"
        elif item["name"] == '':
            continue
        else:
            text = f"{item['time']} - {item['name']}{lesson_types[item['type']]}\n{item['place']}\n{item['teacher']}\n{item['group']}"
        await bot.send_message(message.from_user.id, text)


executor.start_polling(dp, skip_updates=True)
